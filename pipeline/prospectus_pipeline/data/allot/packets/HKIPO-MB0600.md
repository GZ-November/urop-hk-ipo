# 配发结果公告抽取任务：0600.HK Axera Semiconductor Co., Ltd. - H shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**09/02/2026 22:42**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0209/2026020901278.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"0600.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”) and Hong 
Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents of this announcement, make no 
representation as to its accuracy or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising 
from or in reliance upon the whole or any part of the contents of this announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those defined in 
the Hong Kong prospectus dated January 30, 2026 (the “Prospectus”) of Axera Semiconductor Co., Ltd. (愛芯元智半導體股份
有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase or 
subscribe for any securities. This announcement is not a prospectus. Potential investors should read the Prospectus for 
detailed information about the Global Offering described below before deciding whether or not to invest in the Offer Shares. 
Any investment decision in relation to the Offer Shares should be taken solely in reliance on the information provided in the 
Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States (including its 
territories and possessions, any state of the United States and the District of Columbia). This announcement does not constitute 
or form a part of any offer or solicitation to purchase or subscribe for securities in the United States or in any other jurisdictions. 
The securities mentioned herein have not been, and will not be, registered under the United States Securities Act of 1933 as 
amended from time to time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the United States. The 
securities may not be offered, sold, pledged or otherwise transferred within the United States or to, or for the account or benefit 
of US persons (as defined in Regulation S), except in transactions exempt from, or not subject to, the registration requirements of 
the U.S. Securities Act. The securities may be offered, sold or delivered only outside the United States in offshore transactions in 
reliance on Regulation S.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited as stabilizing 
manager (the “Stabilization Manager”) (or its affiliates or any person acting for it), on behalf of the Underwriters, the 
extent permitted by the applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect 
transactions with a view to stabilizing or supporting the market price of the H Shares at such price, in such amounts and in such 
manners as the Stabilization Manager, its affiliates or any person acting for it may determine at a level higher than that which 
might otherwise prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilization Manager 
(or its affiliates or any person acting for it) to conduct any such stabilizing action. Such stabilizing action, if taken, (a) will be 
conducted at the absolute discretion of the Stabilization Manager (or its affiliates or any person acting for it) and in what the 
Stabilization Manager reasonably regards as the best interest of our Company, (b) may be discontinued at any time and (c) is 
required to be brought to an end within 30 days of the last day for lodging applications under the Hong Kong Public Offering, 
being Saturday, March 7, 2026. Such Stabilizing action, if taken, may be effected in all jurisdictions where it is permissible 
to do so, in each case in compliance with all applicable laws, rules and regulatory requirements, including the Securities and 
Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities and Futures 
Ordinance (Chapter 571 of the Laws of Hong Kong). Potential investors should be aware that no stabilizing action can be taken 
to support the price of the H Shares for longer than the stabilization period, which will begin on the Listing Date, and is expected 
to expire on the 30th day after the last day for lodging applications under the Hong Kong Public Offering. After this date, when 
no further stabilizing action may be taken, demand for the H Shares, and therefore the price of the H Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to term and conditions set out in the Prospectus. 
The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not resident in Hong Kong. 
Potential investors of the Offer Shares should note that the Joint Sponsors and Overall Coordinators (for themselves and on 
behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the section headed “Underwriting — Underwriting Arrangements and 
Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. on the 
Listing Date (which is currently expected to be on Tuesday, February 10, 2026).

<<<PAGE 2>>>
2
Axera Semiconductor Co., Ltd.
愛芯元智半導體股份有限公司
(a joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares in 
the Global Offering
:
104,915,200 H Shares
Number of Hong Kong Offer Shares
:
10,491,600 H Shares
Number of International Offer Shares
:
94,423,600 H Shares (subject to the Over-
allotment Option)
Offer Price
:
HK$28.20 per H Share, plus brokerage of 
1.0%, SFC transaction levy of 0.0027%, 
AFRC transaction levy of 0.00015% and 
Stock Exchange trading fee of 0.00565% 
(payable in full on application in Hong 
Kong dollars and subject to refund)
Nominal Value
:
RMB1.00 per H Share
Stock Code
:
600
Joint Sponsors, Overall Coordinators, Joint Global Coordinators,  
Joint Bookrunners and Joint Lead Managers
Joint Global Coordinators

<<<PAGE 3>>>
1 
 
 
Axera Semiconductor Co., Ltd.  
愛芯元智半導體股份有限公司 
ANNOUNCEMENT OF ALLOTMENT RESULTS 
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated January 30, 2026 (the “Prospectus”) issued by 
Axera Semiconductor Co., Ltd. (the “Company”). 
 
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
H Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares. 
SUMMARY 
Company information 
Stock code 
600 
Stock short name 
AXERA 
Dealings commencement date 
February 10, 2026* 
* 
see note at the end of the announcement 
 
Price Information 
Final Offer Price 
HKD28.20 
Offer Price Range 
N/A 
Offer Price Adjustment exercised 
N/A 
Offer Shares and Share Capital 
Number of Offer Shares (before exercise of the Over-allotment 
Option) 
104,915,200 
Final Number of Offer Shares in Hong Kong Public Offering 
10,491,600 
Final Number of Offer Shares in International Offering (before the 
exercise of the Over-allotment Option) 
94,423,600 
Number of issued Shares upon Listing (before exercise of the 
Over-allotment Option) 
587,760,481 

<<<PAGE 4>>>
2 
 
 
 
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through deferred 
delivery or a combination of these means. In the event the Over-allotment Option is exercised, an 
announcement will be made on the Stock Exchange's website. 
Note: Gross proceeds refers to the amount to which the Company is entitled to receive assuming the Over-allotment 
Option is not exercised. For details of the use of proceeds, please refer to the section headed “Future Plans and Use 
of Proceeds” of the Prospectus. 
Over-allocation 
No. of Offer Shares over-allocated 
15,737,200 
Proceeds  
Gross proceeds (Note) 
HK$2,958.6 million 
Less: Estimated listing expenses payable based on Final Offer 
Price 
HK$(159.6) million 
Net proceeds 
HK$2,799.0 million 

<<<PAGE 5>>>
3 
 
 
ALLOTMENT RESULTS DETAILS 
HONG KONG PUBLIC OFFERING 
 
No. of valid applications 
85,091 
No. of successful applications 
40,330 
Subscription level 
104.82 times 
Claw-back triggered 
N/A 
No. of Offer Shares initially available under the Hong Kong Public Offering 
10,491,600 
Final no. of Offer Shares under the Hong Kong Public Offering 
10,491,600 
% of Offer Shares under the Hong Kong Public Offering to the Global 
Offering 
10% 
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can refer to www.eipo. 
com.hk/eIPOAllotment to perform a search by identification number or www.eipo.com.hk/eIPOAllotment for the full 
list of allottees. 
 
INTERNATIONAL OFFERING  
 
No. of placees 
138 
Subscription Level 
6.8 times 
No. of Offer Shares initially available under the International Offering 
94,423,600 
Final no. of Offer Shares under the International Offering 
94,423,600 
% of Offer Shares under the International Offering to the Global Offering 
90% 
The Directors confirm that, to the best of their knowledge, information and belief, save for a consent 
under Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to, among other 
things, allocate further H Shares in the International Offering to certain existing Shareholders and/or 
their close associates and the Cornerstone Investors, (i) none of the Offer Shares subscribed by the 
placees and the public have been financed directly or indirectly by the Company, any of the Directors, 
Supervisors, chief executive of the Company, substantial shareholders, existing shareholders of 
the Company or any of its subsidiaries or their respective close associates; and (ii) none of the 
placees and the public who have purchased the Offer Shares are accustomed to taking instructions 
from the Company, any of the Directors, Supervisors, chief executive of the Company, substantial 
shareholders, existing shareholders of the Company or any of its subsidiaries or their respective close 
associates in relation to the acquisition, disposal, voting or other disposition of Shares registered in 
his/her/its name or otherwise held by him/her/it. 

<<<PAGE 6>>>
4 
 
 
The placees in the International Offering include the following: 
Cornerstone Investors 
 
Investor 
No. of Offer 
Shares 
allocated 
Approximate 
% of Offer 
Shares Note 1 
Approximate 
% of total 
issued share 
capital after 
the Global 
Offering Note 1 
Existing 
Shareholders 
or their close 
associates 
WILL semiconductor Limited 
(“OmniVision HK”) Note 2 and Note 3 
9,678,300 
9.22% 
1.65% 
 Yes 
Xin Ma Apparel International Limited 
Note 2 
9,678,300 
9.22% 
1.65% 
No 
JSC International Investment Fund 
SPC (“JSC Investment”) Note 3 
7,466,100 
7.12% 
1.27% 
Yes 
NGS Super Pty Limited 
5,530,400 
5.27% 
0.94% 
No 
Desay SV Automotive 
Singapore Pte. Ltd. Note 2 
2,765,200 
2.64% 
0.47% 
No 
Factorial Master Fund Note 2 
1,935,600 
1.84% 
0.33% 
No 
Hel Ved Master Fund Note 2 
1,935,600 
1.84% 
0.33% 
No 
Valliance Asset Management Limited 
Note 2 
1,935,600 
1.84% 
0.33% 
No 
Alphahill Capital Limited Note 2 
1,382,600 
1.32% 
0.24% 
No 
Joyson Electronics Holdings Hong Kong 
Limited 
1,382,600 
1.32% 
0.24% 
No 
Jupiter Global Master Fund Ltd. Note 2 
1,382,600 
1.32% 
0.24% 
No 
GRANITE ASIA IX VCC (for the 
account of and on behalf of GX 
ACCESS) Note 2 
1,382,600 
1.32% 
0.24% 
No 
Longhorn Note 2 and CICC Financial 
Trading Limited (in connection with 
Longhorn OTC Swaps) Note 4 
1,382,600 
1.32% 
0.24% 
No 
NonaVerse (Hong Kong) Limited Note 2 
1,382,600 
1.32% 
0.24% 
No 
Qingdao Guanlan Note 2 and Guotai Junan 
Investments (Hong Kong) Limited (in 
connection with Guanlan OTC Swaps) Note 5 
1,382,600 
1.32% 
0.24% 
No 
Jinyi Capital Multi-Strategy Fund SPC Ltd. 
553,000  
0.53% 
0.09%  
No 
Total 
51,156,300  
48.76% 
8.70%  
Note: 
1. 
Before any exercise of the Over-allotment Option. 
 
2. 
Only taking into account the Offer Shares allocated to the relevant investors as cornerstone investors under the Global Offering. In 
addition to the Offer Shares subscribed for as Cornerstone Investors, each of such investors was allocated further Offer Shares as 
a placee in the International Offering. Please refer to the section headed “Allotment Results Details – International Offering –
Allotees with Waivers/Consents Obtained” in this announcement for details. Only the Offer Shares subscribed for as Cornerstone 

<<<PAGE 7>>>
5 
 
 
Investors are subject to lock-up as indicated below. For details, please refer to the section headed “Lock-up Undertakings – 
Cornerstone Investors” in this announcement. 
 
3.       WILL semiconductor Limited a close associate of Mr. YU Renrong (虞仁榮) (“Mr. Yu”), an existing Shareholder holding 
approximately 1.12% in the total issued share capital of the Company as of the date of this Announcement. JSC International 
Investment Fund SPC is a close associate of certain shareholders which are ultimately controlled by government or state-owned 
authorities within Zhejiang Province (each not a substantial shareholder of the Company), comprising, collectively, the Zhejiang 
GP Shareholders as defined in the Prospectus. For the waiver under Rule 10.04 of the Listing Rules and a consent under paragraph 
1C(2) of Appendix F1 to the Listing Rules granted by the Hong Kong Stock Exchange  to permit WILL semiconductor Limited and 
JSC International Investment Fund SPC to participate as Cornerstone Investors in the Global Offering to subscribe for the Offer 
Shares to be issued by the Company under the International Offering, see section headed "Waivers and Exemption" of the 
Prospectus. 
 
4.          CICC Financial Trading Limited (“CICC FT”) has entered into cornerstone investment agreements with, among others, the Company, 
China International Capital Corporation Hong Kong Securities Limited (“CICCHKS”), Guotai Junan Capital Limited, BOCOM 
International (Asia) Limited, Guotai Junan Securities (Hong Kong) Limited (“GTJA Securities”) and BOCOM International 
Securities Limited. CICC FT and China International Capital Corporation Limited will enter into a series of cross-border over-the-
counter swap transactions (collectively, the “Longhorn OTC Swaps”) with each other and the ultimate client, namely Shenzhen 
Longhorn Technology Co., Ltd. (深圳市豪恩科技集團股份有限公司), (the“TRS Ultimate Client (Longhorn)”), pursuant to 
which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the Longhorn OTC Swaps while the economic 
risks and returns of the underlying Offer Shares are passed to the TRS Ultimate Client (Longhorn), subject to customary fees and 
commissions. For the consent under paragraph 1C of Appendix F1 to the Listing Rules granted by the Hong Kong Stock Exchange, 
see "Waiver and Exemption - Consent in respect of the Proposed Subscription of H Shares by Certain Cornerstone Investors Who 
Are Connected Clients" for details. 
 
5.          Guotai Junan Investments (Hong Kong) Limited (“GTJA Investment”) has entered into cornerstone investment agreements with, 
among others, the Company, CICCHKS, Guotai Junan Capital Limited, BOCOM International (Asia) Limited, GTJA Securities and 
BOCOM International Securities Limited. Guotai Junan Investment and Guotai Haitong Securities Co., Ltd. (國泰海通證券股份
有限公司) (“GTHT Onshore Parent”) has entered into a series of cross border over-the-counter swap transactions (the 
“Guanlan OTC Swaps”) with each other and the ultimate clients, which include Guanlan Investment Flexible Allocation No. 5 
Private Equity Investment Fund (觀瀾投資靈活配置5 號私募證券投資基金) (the “Guanlan Ultimate Clients”) managed by 
Qingdao Guanlan Investment Management Co., Ltd. (青島觀瀾投資管理有限公司) (“Qingdao Guanlan”), pursuant to which 
GTJA Investment will hold the Offer Shares on a non-discretionary basis to hedge the Guanlan OTC Swaps while the economic 
risks and returns of the underlying Offer Shares are passed to the Guanlan Ultimate Clients, subject to customary fees and 
commissions. For the consent under paragraph 1C of Appendix F1 to the Listing Rules granted by the Hong Kong Stock Exchange, 
see "Waiver and Exemption - Consent in respect of the Proposed Subscription of H Shares by Certain Cornerstone Investors Who 
Are Connected Clients" for details. 
 
Allotees with Waivers/Consents Obtained 
 
Investor 
No. of 
Offer 
Shares 
allocated 
% of 
total 
issued H 
Shares 
after the 
Global 
Offering 
(assumin
g the 
Over-
allotmen
t Option 
is not 
exercised 
% of 
total 
issued 
share 
capital in 
the 
Company 
after the 
Global 
Offering 
(assuming 
the Over-
allotment 
Option is 
not 
exercised) 
Relationship 

<<<PAGE 8>>>
6 
 
 
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to 
allocations of further H Shares to Cornerstone Investors Note 1 - 2 
OmniVision HK Note 3 
4,147,800 
0.71% 
0.71% A close associate of an existing 
Shareholder and a Cornerstone Investor 
Xin Ma Apparel International 
Limited 
6,913,000 
1.18% 
1.18% A Cornerstone Investor and an 
Independent Third Party 
Desay SV Automotive Singapore 
Pte. Ltd. 
1,106,000 
0.19% 
0.19% 
A Cornerstone Investor and an 
Independent Third Party 
Factorial Master Fund 
802,000 
0.14% 
0.14% 
A Cornerstone Investor and an 
Independent Third Parbty 
Hel Ved Master Fund 
885,000 
0.15% 
0.15% 
A Cornerstone Investor and an 
Independent Third Party 
Valliance Asset Management 
Limited 
885,000 
0.15% 
0.15% 
A Cornerstone Investor and an 
Independent Third Party 
Alphahill Capital Limited 
553,000 
0.09% 
0.09% 
A Cornerstone Investor and an 
Independent Third Party 
Jupiter Global Master Fund Ltd. 
553,000 
0.09% 
0.09% 
A Cornerstone Investor and an 
Independent Third Party 
GRANITE ASIA IX VCC (for the 
account of and on behalf of GX 
ACCESS) 
553,000 
0.09% 
0.09% 
A Cornerstone Investor and an 
Independent Third Party 
Longhorn and CICC Financial 
Trading Limited (in connection 
with CICC Longhorn OTC swaps) 
Note 4 
553,000 
0.09% 
0.09% 
A Cornerstone Investor and an 
Independent Third Party 
NonaVerse (Hong Kong) Limited 
670,500 
0.11% 
0.11% 
A Cornerstone Investor and an 
Independent Third Party 
Qingdao Guanlan and GF Global 
Capital Limited ("GFGC") (in 
connection with GF Guanlan OTC 
Swaps) Note 5 
276,000 
0.05% 
0.05% 
A Cornerstone Investor and an 
Independent Third Party 
Allotees with consent under paragraph 1C of the Placing Guidelines and Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations to connected clients Note 6  
CICC FT Note 6 
857,200 
0.15% 
0.15% Connected client 
GTJA Investment Note 7 
3,236,900 
0.55% 
0.55% Connected client 
GFGC Note 8 
276,000 
0.05% 
0.05% Connected client 
Huatai Capital Investment Limited 
(“HTCI”) Note 9 
28,000 
0.00% 
0.00% Connected client 
Fullgoal Fund Management Co., 
Ltd. (“Fullgoal Fund”) Note 10 
276,000 
0.05% 
0.05% Connected client 
Note:  
1. 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the number of Offer Shares 
allocated to the investors as placees in the International Offering. For allocations of Offer Shares to the relevant investors as 
Cornerstone Investors, please refer to the section headed “Allotment Results Details – International Offering – Cornerstone Investors” 
in this announcement. For details of the consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations 
of further H Shares to the existing Shareholders and/or their close associates and Cornerstone Investors, please refer to the section 

<<<PAGE 9>>>
7 
 
 
headed “Others/Additional Information – Allocations of Offer Shares to the Cornerstone Investors with a consent under paragraph 
18 of Chapter 4.15 of the Guide for New Listing Applicants” in this announcement. 
2. 
In respect of the allocations in above table, the Stock Exchange has granted (i) consent under paragraph 18 of  Chapter 4.15 of the 
Guide for New Listing Applicants in relation to allocations of further H Shares to Cornerstone Investors and (ii) consent under 
paragraph 1C of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations to 
connected clients. For details of such waiver and consent, please refer to the section headed “Others / Additional Information" in 
this announcement.  
3. 
The Stock Exchange has granted a waiver from strict compliance with the requirements under Rule 10.04 of the Listing Rules and 
consent under paragraph 1C(2) of the Placing Guidelines with respect to allocations to OmniVision HK as a close associate of an 
existing minority shareholder of the Company and a Cornerstone Investor. See the section headed “Waivers and Exemption” in the 
Prospectus for details. Except for OmniVision HK, none of the allotees with consent under paragraph 18 of Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations of further H Shares to Cornerstone Investors is an existing Shareholder of the 
Company or their close associates. The H Shares to be allocated to OmniVision HK as permitted under the size-based exemption as 
provided in paragraph 18 of Chapter 4.15 of the Guide is expected to be approximately 3.95% of the total number of Offer Shares 
under the Global Offering. 
 
4. 
In connection with the further subscription of the Offer Shares, CICC FT, and China International Capital Corporation Limited will 
enter into a series of cross border over-the-counter swap transactions (collectively, the “CICC Longhorn OTC Swaps”) with, 
among others, each other and the ultimate client, namely Longhorn, pursuant to which CICC FT will hold the Offer Shares (as further 
allocated) on a non-discretionary basis to hedge the CICC Longhorn OTC Swaps while the economic risks and returns of the 
underlying Offer Shares are passed to Longhorn, subject to customary fees and commissions. See note 6 below for details. 
5. 
In connection with the further subscription of the Offer Shares, GF Global Capital Limited (the "GFGC") and GF Securities Co., 
Ltd. will enter into a series of cross border delta one OTC swap transactions (the “GF OTC Swaps”) with each other and the ultimate 
client, Qingdao Guanlan, (the “GFGC Ultimate Client”),pursuant to which GFGC will hold the Offer Shares on a non-discretionary 
basis to hedge the GF OTC Swaps while the economic risks and returns of the underlying Offer Shares are passed to the GFGC 
Ultimate Client, subject to customary fees and commissions. See note 8 below for details.  
6. 
CICC FT and CICCHKS, one of the Overall Coordinators and Underwriters of the Global Offering, are members of the same group 
of companies. Accordingly, CICC FT is a connected client of CICCHKS. Through the CICC OTC Swaps as disclosed in this 
announcement, CICC FT holds 553,000 Offer Shares and 304,200 Offer Shares for Longhorn and Hengde Jinze No. E49, respectively. 
See note 1 under the section headed “Others / Additional Information – Placing to connected clients with a prior consent under 
paragraph 1C(1) of the Placing Guidelines” in this announcement for more details. 
7. 
GTJA Investment and GTJA Securities, one of the Overall Coordinators and Underwriters of the Global Offering, are members of 
the same group of companies. Accordingly, GTJA Investment is a connected client of GTJA Securities. See note 2 under the section 
headed “Others / Additional Information – Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines” in this announcement for more details. 
8. 
GFGC and GF Securities (Hong Kong) Brokerage Limited, one of the Underwriters of the Global Offering, are member of the same 
group of companies. Accordingly, GFGC is a connected client of GF Securities (Hong Kong) Brokerage Limited. See note 3 under 
the section headed “Others / Additional Information – Placing to connected clients with a prior consent under paragraph 1C(1) of 
the Placing Guidelines” in this announcement for more details. 
9. 
Huatai Financial Holdings (Hong Kong) Limited is a non-syndicate distributor in connection with the Global Offering. Huatai 
Financial Holdings (Hong Kong) Limited and HTCI are members of the same group of companies. Accordingly, HTCI is a connected 
client of Huatai Financial Holdings (Hong Kong) Limited. See note 4 under the section headed “Others / Additional Information – 
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines” in this announcement for more 
details. Such number of Offer Shares allocated represents approximately 0.005% of the total issued H Shares after the Global 
Offering (assuming the Over-allotment Option is not exercised, and 0.005% of total issued share capital in the Company after the 
Global Offering (assuming the Over-allotment Option is not exercised). 
10. Fullgoal Fund and GTJA Securities, one of the Overall Coordinators and Underwriters of the Global Offering, are members of the 
same group of companies. Accordingly, Fullgoal Fund is a connected client of GTJA Securities. See note 5 under the section headed 
“Others / Additional Information – Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines” in this announcement for more details. 
 
LOCK-UP UNDERTAKINGS 
 
Single Largest Group of Shareholders 

<<<PAGE 10>>>
8 
 
 
 
Name 
Number of 
shares held 
in the Company 
subject 
to lock-up 
undertakings 
upon 
Listing 
% of 
shareholding in 
the Company 
subject to 
lock-up 
undertakings 
upon 
ListingNote 1 
Last day subject 
to the lock-up 
undertakings 
Jiaxing Zhixin Note 2 
43,104,726  
 
7.33%  
February 9, 2027 Note 3 
Jiaxing Aixin Note 2 
36,165,580  
 
6.15%  
February 9, 2027 Note 3 
Shanghai Bonasi Note 2 
22,906,278  
 
3.90%  
February 9, 2027 Note 3 
Xinsheng Bicheng No.1 Note 
2 
2,978,077  
 
0.51%  
February 9, 2027 Note 3 
Xinsheng Bicheng No.2Note 
2 
1,786,846  
 
0.30% 
February 9, 2027 Note 3 
Xinsheng Bicheng No.3  Note 
2 
1,786,846 
 
0.30% 
February 9, 2027 Note 3 
Xinsheng Bicheng No.4  Note 
2 
1,191,231 
  
0.20% 
February 9, 2027 Note 3 
Subtotal 
109,919,584 
18.70%  
/ 
Notes: 
(1) 
Before any exercise of the Over-allotment Option. 
(2) 
Upon completion of the Global Offering, as a result of the termination of the special rights and the changes in the 
Board composition, Dr. QIU will no longer be able to control the majority of the Board seats of our Company. 
Additionally, assuming the Over-allotment Option is not exercised, Dr. QIU, Shanghai Jinling, Jiaxing Zhixin, Jiaxing 
Aixin, Shanghai Bonasi and Xinsheng Bicheng Platforms will collectively be entitled to exercise voting rights attaching 
to 18.70% of the total issued Shares of our Company. Accordingly, our Company will no longer have any controlling 
shareholder. Instead, Dr. QIU, Shanghai Jinling, Jiaxing Zhixin, Jiaxing Aixin, Shanghai Bonasi and Xinsheng 
Bicheng Platforms will constitute the Single Largest Group of Shareholders upon completion of the Global Offering. 
 

<<<PAGE 11>>>
9 
 
 
(3) 
The expiry day of the lock-up period shown in the table above is pursuant to the PRC Company Law. In accordance 
with the relevant Listing Rule/guidance materials, the required lock-up for the first six-month period ends on August 
9, 2026. 

<<<PAGE 12>>>
10 
 
 
 
Pre-IPO Investors 
 
Name 
Number of 
shares held 
in the Company 
subject 
to lock-up 
undertakings 
upon 
Listing 
% of 
shareholding in 
the Company 
subject to 
lock-up 
undertakings 
upon 
ListingNote 1 
Last day subject to the 
lock-up undertakings 
Weihao Phase III  
31,424,017 
5.35% 
February 9, 2027 Note 2 
Tianjin Weihao  
23,113,306  
3.93% 
February 9, 2027 Note 2 
Weihao Phase IV  
9,083,133 
1.55% 
February 9, 2027 Note 2 
Yiwu Weihao 
5,948,758 
1.01% 
February 9, 2027 Note 2 
Weihao Yunxuan 
4,117,683 
0.70% 
February 9, 2027 Note 2 
Shanghai Ganzhong  
1,191,231  
0.20%  
February 9, 2027 Note 2 
Wuhu Kuangyun  
31,081,389  
5.29%  
February 9, 2027 Note 2 
Qiming Rongxin  
9,212,656 
1.57% 
February 9, 2027 Note 2 
Qiming Rongying  
8,333,333 
1.42% 
February 9, 2027 Note 2 
Qiming Rongke  
6,818,182 
1.16% 
February 9, 2027 Note 2 
Suzhou Qihua  
5,948,758 
1.01% 
February 9, 2027 Note 2 
Beijing Kuxun Technology  
20,188,655 
3.43% 
February 9, 2027 Note 2 
Guangdong Yuntai  
5,985,784 
1.02% 
February 9, 2027 Note 2 
Heju Minghong   
4,000,000 
0.68% 
February 9, 2027 Note 2 
Heju Chongyue  
3,826,453 
0.65% 
February 9, 2027 Note 2 

<<<PAGE 13>>>
11 
 
 
Guangdong Wenquan  
2,478,649 
0.42% 
February 9, 2027 Note 2 
Guangdong Wenjia  
1,560,752 
0.27% 
February 9, 2027 Note 2 
Guangdong Yunqi  
1,400,806 
0.24% 
February 9, 2027 Note 2 
Ningbo Hualing  
17,891,729 
3.04% 
February 9, 2027 Note 2 
Hangzhou Gancheng  
17,298,064 
2.94% 
February 9, 2027 Note 2 
Chongqing Liangjiang Investment  
15,895,484 
2.70% 
February 9, 2027 Note 2 
Chongqing Industrial Investment 
Parent Fund  
15,895,483 
2.70% 
February 9, 2027 Note 2 
Ningbo Zhenhai  
15,313,614 
2.61% 
February 9, 2027 Note 2 
Tencent Investment  
14,376,165 
2.45% 
February 9, 2027 Note 2 
Shaoxing Gansheng  
9,496,664 
1.62% 
February 9, 2027 Note 2 
Suzhou Xingfan  
7,407,407 
1.26% 
February 9, 2027 Note 2 
Beijing Xingfan  
1,487,189 
0.25% 
February 9, 2027 Note 2 
Jiyuan Haoyue 
4,875,659 
0.83% 
February 9, 2027 Note 2 
Jiyuan Haoyuan  
3,615,562 
0.62% 
February 9, 2027 Note 2 
Suzhou Yuanhe Puhua  
4,541,567 
0.77% 
February 9, 2027 Note 2 
Jiangsu Yuanhe Puhua  
3,197,109 
0.54% 
February 9, 2027 Note 2 
Hangzhou Yunsheng  
5,479,497 
0.93% 
February 9, 2027 Note 2 
Hangzhou Yunhua  
1,643,849 
0.28% 
February 9, 2027 Note 2 
Ningbo Fengyuan  
3,835,648 
0.65% 
February 9, 2027 Note 2 
Jinjiang Fengyuan  
2,568,145 
0.44% 
February 9, 2027 Note 2 

<<<PAGE 14>>>
12 
 
 
Tongshang Venture Investment  
5,676,958 
0.97% 
February 9, 2027 Note 2 
Yu Renrong  
5,387,205 
0.92% 
February 9, 2027 Note 2 
Shenzhen Longzhu  
4,613,401 
0.78% 
February 9, 2027 Note 2 
Zhoushan Weixin  
4,008,237 
0.68% 
February 9, 2027 Note 2 
Suzhou Yaotu  
3,189,333 
0.54% 
February 9, 2027 Note 2 
Ningbo Yaotu  
700,403 
0.12% 
February 9, 2027 Note 2 
Tianjin Yuzhi  
3,502,016 
0.60% 
February 9, 2027 Note 2 
Zhoushan Zhixin  
3,422,330 
0.58% 
February 9, 2027 Note 2 
Shanghai Xinju  
3,367,004 
0.57% 
February 9, 2027 Note 2 
Chen Heyu  
2,739,748 
0.47% 
February 9, 2027 Note 2 
Ningbo Huayan  
2,451,411 
0.42% 
February 9, 2027 Note 2 
Yangming Zhixing  
2,191,799 
0.37% 
February 9, 2027 Note 2 
Wanwu Xiamen  
1,885,522 
0.32% 
February 9, 2027 Note 2 
Qingdao Minxin  
1,643,849 
0.28% 
February 9, 2027 Note 2 
Suzhou Juyuan Zhuxin  
1,643,849 
0.28% 
February 9, 2027 Note 2 
Beijing Anrong  
1,400,806 
0.24% 
February 9, 2027 Note 2 
Hefei Shixi  
1,400,806 
0.24% 
February 9, 2027 Note 2 
Yu Jiangyong  
1,116,779 
0.19% 
February 9, 2027 Note 2 
Hangzhou Caitong Hengxin  
1,095,899 
0.19% 
February 9, 2027 Note 2 
Hangzhou Dayu  
670,067 
0.11% 
February 9, 2027 Note 2 
Qianhai Zhiyu  
285,895 
0.05% 
February 9, 2027 Note 2 
Subtotal 
372,925,697 
63.45% 
 
Notes: 
(1) 
Before any exercise of the Over-allotment Option. 
(2) 
The expiry day of the lock-up period shown in the table above is pursuant to the PRC Company Law. 

<<<PAGE 15>>>
13 
 
 
 
Cornerstone Investors 
 
Name 
Number of 
shares held 
in the Company 
subject to 
lock-up 
undertakings 
upon 
Listing 
% of total 
Offer 
Shares  
% of 
shareholding in 
the Company 
subject to lock-up
undertakings
upon ListingNote1
Last day subject 
to the lock-up 
undertakingsNote1 
WILL 
semiconductor 
Limited 
9,678,300 
9.22% 
1.65% 
August 9, 2026 
Xin Ma Apparel 
International Limited 
9,678,300 
9.22% 
1.65% 
August 9, 2026 
JSC International 
Investment Fund 
SPC 
7,466,100 
7.12% 
1.27% 
August 9, 2026 
NGS Super Pty 
Limited 
5,530,400 
5.27% 
0.94% 
August 9, 2026 
Desay SV 
Automotive 
Singapore Pte. Ltd. 
2,765,200 
2.64% 
0.47% 
August 9, 2026 
Factorial Master 
Fund 
1,935,600 
1.84% 
0.33% 
August 9, 2026 
Hel Ved Master 
Fund 
1,935,600 
1.84% 
0.33% 
August 9, 2026 
Valliance Asset 
Management 
Limited 
1,935,600 
1.84% 
0.33% 
August 9, 2026 
Alphahill Capital 
Limited 
1,382,600 
1.32% 
0.24% 
August 9, 2026 
Joyson Electronics 
Holdings Hong 
Kong Limited 
1,382,600 
1.32% 
0.24% 
August 9, 2026 
Jupiter Global 
Master Fund Ltd. 
1,382,600 
1.32% 
0.24% 
August 9, 2026 
GRANITE ASIA IX 
VCC (for the 
account of and on 
behalf of GX 
ACCESS) 
1,382,600 
1.32% 
0.24% 
August 9, 2026 
Longhorn and CICC 
Financial Trading 
Limited (in 
1,382,600 
1.32% 
0.24% 
August 9, 2026 

<<<PAGE 16>>>
14 
 
 
connection with 
Longhorn OTC 
Swaps) 
NonaVerse (Hong 
Kong) Limited 
1,382,600 
1.32% 
0.24% 
August 9, 2026 
Qingdao Guanlan 
and Guotai Junan 
Investments (Hong 
Kong) Limited (in 
connection with 
Guanlan OTC 
Swaps) 
1,382,600 
1.32% 
0.24% 
August 9, 2026 
Jinyi Capital Multi-
Strategy Fund SPC 
Ltd. 
553,000  
0.53% 
0.09%  
August 9, 2026 
Total 
51,156,300  
48.76% 
8.70%  
/ 
Note:  
 
(1) In accordance with the relevant cornerstone investment agreements, the required lock-up period ends on August 9, 2026. 
The Cornerstone Investors will cease to be prohibited from disposing of or transferring H Shares subscribed pursuant to 
the relevant cornerstone investment agreements after the indicated date. 
 
 
.

<<<PAGE 17>>>
15 
 
 
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
Option is fully 
exercised and 
new H Shares 
are issued) 
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
Option is fully 
exercised and 
new H Shares 
are issued) 
Number of H 
Shares held 
upon Listing 
Number of 
H Shares 
held upon 
Listing as % 
of total issued 
share capital 
upon Listing 
(assuming 
no exercise 
of the Over- 
allotment 
Option) 
Number of 
H Shares 
held upon 
Listing as % 
of total issued 
share capital 
upon Listing 
(assuming 
the Over- 
allotment 
Option is fully 
exercised and 
new H Shares 
are issued) 
Top 1 
16,591,300  
17.57% 
15.06% 
15.81% 
13.75% 
16,591,300  
2.82% 
2.75% 
Top 5 
54,345,900  
57.56% 
49.33% 
51.80% 
45.04% 
81,819,576  
13.92% 
13.56% 
Top 10 
72,625,200  
76.91% 
65.93% 
69.22% 
60.19% 
100,098,876  
17.03% 
16.59% 
Top 25 
94,368,500  
99.94% 
85.66% 
89.95% 
78.22% 
121,842,176  
20.73% 
20.19% 
Note: 
 
* 
Ranking of placees is based on the number of Shares allotted to the placees. 

<<<PAGE 18>>>
16 
 
 
H SHAREHOLDER CONCENTRATION ANALYSIS 
 
H 
Sharehold
ers* 
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
exercised 
and new H 
Shares are 
issued) 
Allotment 
as 
% of total 
Offer 
Shares 
(assuming 
no exercise 
of the 
Over- 
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
exercised 
and new H 
Shares are 
issued) 
Number of H 
Shares held 
upon Listing 
Number of 
H 
Shares held 
upon Listing 
as % of 
total issued 
share capital 
upon Listing 
(assuming 
no exercise 
of the Over- 
allotment 
Option) 
Number of 
H 
Shares held 
upon Listing 
as % of 
total issued 
share capital 
upon Listing 
(assuming 
the Over- 
allotment 
Option 
is fully 
exercised 
and new H 
Shares are 
issued) 
Number of  
Shares held 
upon Listing 
Top 1 
- 
0.00% 
0.00% 
0.00% 
0.00% 
109,919,584 
18.70% 
18.21% 109,919,584 
Top 5 
- 
0.00% 
0.00% 
0.00% 
0.00% 
277,982,997 
47.30% 
46.06% 277,982,997 
Top 10 
21,292,200 
22.55% 
19.33% 
20.29% 
17.65% 
384,081,701 
65.35% 
63.64% 384,081,701 
Top 25 
59,875,900 
63.41% 
54.35% 
57.07% 
49.63% 
514,999,300 
87.62% 
85.34% 514,999,300 
Note: 
 
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholder upon Listing. 

<<<PAGE 19>>>
17 
 
 
SHAREHOLDER CONCENTRATION ANALYSIS  
 
Shareholders* 
Number 
of Shares 
allotted 
Allotment 
as % of 
International 
Offering 
(assuming no 
exercise of the 
Over-
allotment 
Option) 
Allotment 
as % of 
International 
Offering 
(assuming the 
Over-
allotment 
Option is fully 
exercised and 
new Shares are 
issued) 
Allotment as 
% of total 
Offer Shares 
(assuming no 
exercise of the 
Over-
allotment 
Option) 
Allotment as 
% of total 
Offer Shares 
(assuming the 
Over-
allotment 
Option is fully 
exercised and 
new Shares 
are 
issued) 
Number of 
Shares held 
upon Listing 
Number of 
Shares held 
upon Listing 
as % of 
total issued 
share capital 
upon Listing 
(assuming no 
exercise of 
the 
Over-
allotment 
Option) 
Number of 
Shares held 
upon Listing 
as % of 
total issued 
share capital 
upon Listing 
(assuming the 
Over-
allotment 
Option is fully 
exercised and 
new Shares are 
issued) 
Top 1 
- 
0.00% 
0.00% 
0.00% 
0.00% 
109,919,584 
18.70% 
18.21% 
Top 5 
- 
0.00% 
0.00% 
0.00% 
0.00% 
277,982,997 
47.30% 
46.06% 
Top 10 
21,292,200 
22.55% 
19.33% 
20.29% 
17.65% 
384,081,701 
65.35% 
63.64% 
Top 25 
59,875,900 
63.41% 
54.35% 
57.07% 
49.63% 
514,999,300 
87.62% 
85.34% 
Note: 
 
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing 

<<<PAGE 20>>>
18 
 
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING 
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 85,091 valid 
applications made by the public will be conditionally allocated on the basis set out below: 
 
Number of 
H Shares 
applied for 
Number of 
valid 
applications 
Basis of allocation/ballot 
Approximate 
% allotted of 
the total no. 
of H Shares 
applied for 
POOL A 
100 
32,414 
5,835 out of 32,414 to receive 100 Shares 
18.00% 
200 
6,251 
1,875 out of 6,251 to receive 100 Shares 
15.00% 
300 
11,011 
4,574 out of 11,011 to receive 100 Shares 
13.85% 
400 
2,084 
1,000 out of 2,084 to receive 100 Shares 
12.00% 
500 
2,672 
1,336 out of 2,672 to receive 100 Shares 
10.00% 
600 
1,037 
560 out of 1,037 to receive 100 Shares 
9.00% 
700 
1,270 
711 out of 1,270 to receive 100 Shares 
8.00% 
800 
937 
562 out of 937 to receive 100 Shares 
7.50% 
900 
531 
344 out of 531 to receive 100 Shares 
7.20% 
1,000 
8,596 
6,017 out of 8,596 to receive 100 Shares 
7.00% 
2,000 
2,597 
2,078 out of 2,597 to receive 100 Shares 
4.00% 
3,000 
2,097 
1,887 out of 2,097 to receive 100 Shares 
3.00% 
4,000 
1,067 
1,024 out of 1,067 to receive 100 Shares 
2.40% 
5,000 
1,025 
100 Shares 
2.00% 
6,000 
530 
100 Shares plus 74 out of 530 to receive additional 100 Shares 
1.90% 
7,000 
414 
100 Shares plus 108 out of 414 to receive additional 100 Shares 
1.80% 
8,000 
408 
100 Shares plus 147 out of 408 to receive additional 100 Shares 
1.70% 
9,000 
311 
100 Shares plus 137 out of 311 to receive additional 100 Shares 
1.60% 
10,000 
2,525 
100 Shares plus 1,263 out of 2,525 to receive additional 100 Shares 
1.50% 
20,000 
1,576 
200 Shares 
1.00% 
30,000 
1,029 
200 Shares plus 257 out of 1,029 to receive additional 100 Shares 
0.75% 
40,000 
561 
200 Shares plus 337 out of 561 to receive additional 100 Shares 
0.65% 
50,000 
450 
300 Shares 
0.60% 
60,000 
291 
300 Shares plus 87 out of 291 to receive additional 100 Shares 
0.55% 
70,000 
273 
300 Shares plus 137 out of 273 to receive additional 100 Shares 
0.50% 
80,000 
197 
400 Shares 
0.50% 
90,000 
125 
400 Shares plus 63 out of 125 to receive additional 100 Shares 
0.50% 
100,000 
1,234 
500 Shares 
0.50% 
 
83,513 
Total number of Pool A successful applicants: 38,752 
 
 
 

<<<PAGE 21>>>
19 
 
 
 
Number of 
H Shares 
applied for 
Number of 
valid 
applications 
Basis of allocation/ballot 
Approximate 
% allotted of 
the total no. 
of H Shares 
applied for 
POOL B 
200,000 
938 
2,300 Shares 
1.15% 
300,000 
230 
2,800 Shares 
0.93% 
400,000 
108 
3,300 Shares 
0.83% 
500,000 
69 
3,600 Shares 
0.72% 
600,000 
32 
4,000 Shares 
0.67% 
700,000 
31 
4,300 Shares 
0.61% 
800,000 
26 
4,700 Shares 
0.59% 
900,000 
8 
5,100 Shares 
0.57% 
1,000,000 
66 
5,400 Shares 
0.54% 
2,000,000 
23 
9,100 Shares 
0.46% 
3,000,000 
16 
12,800 Shares 
0.43% 
5,245,800 
31 
20,800 Shares 
0.40% 
 
1,578 
Total number of Pool B successful applicants: 1,578 
 
 
 

<<<PAGE 22>>>
20 
 
 
 
As of the date of this announcement, the relevant subscription monies previously deposited in the designated 
nominee accounts have been remitted back to the accounts of all HKSCC participants. Investors should 
contact their relevant brokers for any inquiries. 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of which 
consent has been obtained, the Company has complied with the Listing Rules and guidance materials in 
relation to the placing, allotment and listing of the H Shares. 
 
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the Offer Price in addition to any brokerage, AFRC transaction 
levy, SFC transaction levy and Stock Exchange trading fee payable. 
OTHERS / ADDITIONAL INFORMATION 
Allocations of Offer Shares to the Cornerstone Investors with a consent under paragraph 
18 of Chapter 4.15 of the Guide for New Listing Applicants  
The Company has applied to, and the Stock Exchange has granted, a consent under paragraph 18 of 
Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to allocate further Offer 
Shares in the International Offering to certain Cornerstone Investors as placees, subject to the following 
conditions: 
(a) the final offering size of the Global Offering, excluding any over-allocation, will be of a total value of 
at least HK$1 billion; 
(b) the Offer Shares allocated to all existing Shareholders and their close associates (whether as cornerstone 
investors and/or as placees) as permitted under the Size-based Exemption (as defined in the Guide for 
New Listing Applicants) do not exceed 30% of the total number of the H Shares offered under the 
Global Offering; 
(c) the allocation to the Size-based Exemption Participants will not affect the Company’s ability to satisfy 
the public float requirement as prescribed by the Stock Exchange under Rule 8.08 (as amended and 
replaced by Rule 19A.13A) of the Listing Rules; 
(d) each Director, chief executive and Supervisor of the Company confirms that no securities have been 
allocated to them or their respective close associates under the Size-based Exemption;  
(e) details of the allocation to the Size-based Exemption Participants under the Size-based Exemption will be 
disclosed in this announcement; and 
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted by the 
Stock Exchange.  
For details of the allocations of Offer Shares to existing Shareholders and/or their close associates and 
Cornerstone Investors, please refer to the section headed “Allotment Results Details – International 
Offering – Allotees with Waivers/Consents Obtained” in this announcement. 
Placing to connected clients with prior consents under paragraph 1C of the Placing Guidelines  
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, consent 
under paragraph 1C of the Placing Guidelines to permit allocation to connected clients pursuant to the 
Placing Guidelines. The allocation of Offer Shares to such connected clients is in compliance with all the 
conditions under the consents granted by the Stock Exchange. Details of the placement to connected 
clients in placing tranche are set out below. 

<<<PAGE 23>>>
 
 
 
 
No. 
Connected 
Distributor 
Connected 
Client 
Relationship 
Discretionary or 
nondiscretionary 
Whether 
the 
Connected 
Client 
is 
a 
collective 
investment 
scheme which is 
not 
authorised 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
Number of Offer 
Shares 
to 
be 
allocated to the 
Connected 
Client 
Approximate 
percentage 
of 
total number of  
Offer 
Shares 
under 
the 
Global Offering 
(assuming 
no 
exercise of the 
Over-allotment 
Option) 
1.  
CICCHKS 
Note 1 
CICC FT 
CICC FT is a 
member 
of 
the 
same 
group 
of 
CICCHKS. 
Non-discretionary 
No 
Longhorn: 553,000 
0.53% 
Hengde Jinze No. 
E49: 304,200 
0.29% 
2.  
GTJA 
Securities 
Note 2 
 GTJA 
Investment 
GTJA 
Investment is 
a member of 
the 
same 
group 
of 
GTJA 
Securities. 
Non-discretionary 
No 
3,236,900 
3.09% 
3.  
GF 
Securities 
(Hong 
Kong) 
Brokerage 
 GFGC 
GFGC is a 
member 
of 
the 
same 
group of GF 
Securities 
Non-discretionary  
No 
276,000 
0.26% 

<<<PAGE 24>>>
 
 
No. 
Connected 
Distributor 
Connected 
Client 
Relationship 
Discretionary or 
nondiscretionary 
Whether 
the 
Connected 
Client 
is 
a 
collective 
investment 
scheme which is 
not 
authorised 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
Number of Offer 
Shares 
to 
be 
allocated to the 
Connected 
Client 
Approximate 
percentage 
of 
total number of  
Offer 
Shares 
under 
the 
Global Offering 
(assuming 
no 
exercise of the 
Over-allotment 
Option) 
Limited Note 
3 
(Hong Kong) 
Brokerage. 
4. 
HTFH Note 4 
HTCI 
HTCI is a 
member 
of 
the 
same 
group 
of 
HTFH. 
Non-discretionary 
No 
28,000 
 
0.03% 
 
5. 
GTJA 
Securities 
Note 5 
Fullgoal 
Fund 
Management 
Co., 
Ltd. 
(“Fullgoal 
Fund”) 
Fullgoad Fund 
is owned by 
Guotai 
Haitong 
Securities Co., 
Ltd. (SEHK: 
2611) 
(“Guotai 
Haitong”) as 
to 
27.775%. 
GTJA 
Securities is a 
subsidiary of 
Guotai 
Haitong. 
Therefore, 
Fullgoal Fund 
is a member of 
the 
same 
group 
of 
companies as 
Discretionary 
No 
276,000 
0.26% 

<<<PAGE 25>>>
 
 
No. 
Connected 
Distributor 
Connected 
Client 
Relationship 
Discretionary or 
nondiscretionary 
Whether 
the 
Connected 
Client 
is 
a 
collective 
investment 
scheme which is 
not 
authorised 
by the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
Number of Offer 
Shares 
to 
be 
allocated to the 
Connected 
Client 
Approximate 
percentage 
of 
total number of  
Offer 
Shares 
under 
the 
Global Offering 
(assuming 
no 
exercise of the 
Over-allotment 
Option) 
GTJA 
Securities. 
 
__________ 
Notes: 
(1) 
CICC FT and China International Capital Corporation Limited will enter into a series of cross-border over-the-counter swap transactions (collectively, the “CICC 
OTC Swaps”) with each other and the ultimate clients, comprising Shenzhen Longhorn Technology Co., Ltd. (深圳市豪恩科技集团股份有限公司) 
(“Longhorn”) and Hengde Jinze No. E49 Private Securities Investment Fund (恆德金澤E49 號私募證券投資基金) (“Hengde Jinze No. E49”) (the “CICC 
TRS Ultimate Clients”), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis to hedge the CICC OTC Swaps while the economic 
risks and returns of the underlying Offer Shares are passed to the CICC TRS Ultimate Clients, subject to customary fees and commissions. The CICC OTC 
Swaps will be fully funded by the CICC TRS Ultimate Clients. During the terms of the CICC OTC Swaps, all economic returns of the Offer Shares subscribed 
by CICC FT will be passed to the CICC TRS Ultimate Clients and all economic loss shall be borne by the CICC TRS Ultimate Clients through the CICC OTC 
Swaps, and CICC FT will not take part in any economic return or bear any economic loss in relation to the Offer Shares. The CICC OTC Swaps are linked to the 
Offer Shares and the CICC TRS Ultimate Clients may request to early terminate the CICC OTC Swaps at their own discretion, upon which CICC FT may dispose 
of the Offer Shares and settle the CICC OTC Swaps in cash in accordance with the terms and conditions of the CICC OTC Swaps. Despite that CICC FT will 
hold the legal title of the Offer Shares by itself, it will not exercise the voting rights attaching to the relevant Offer Shares during the terms of the CICC OTC 
Swaps according to its internal policy. 
 
Longhorn was founded in 1995. It is a technology group company committed to providing comprehensive solutions for global top-tier customers through 
innovative technology, intelligent products, and high-quality services. Longhorn is held as to approximately 99.026% and 0.974% by CHEN Qingfeng and ZHU 
Zhengchang, each an Independent Third Party. 
 
There is no ultimate beneficial owners holding 30% or more interest in Hengde Jinze No. E49. 
 
To the best of CICC FT’s knowledge having made all reasonable inquiries, each of the CICC TRS Ultimate Clients is an Independent Third Party of CICC FT, 
CICCHKS and the companies which are members of the same group of CICCHKS.  
(2) 
GTJA Investment and Guotai Haitong Securities Co., Ltd. (國泰海通證券股份有限公司) (“GTHT Onshore Parent”) will enter into a series of cross border 
over-the-counter swap transactions (the “GTHT OTC Swaps”) with each other and the ultimate clients, respectively (together, the “GTHT Ultimate Clients”), 

<<<PAGE 26>>>
 
 
pursuant to which GTJA Investment will hold the Offer Shares on a non-discretionary basis to hedge the GTHT OTC Swaps while the economic risks and returns 
of the underlying Offer Shares are passed to the GTHT Ultimate Clients, subject to customary fees and commissions. The GTHT OTC Swaps will be fully funded 
by the GTHT Ultimate Clients, respectively. During the terms of the GTHT OTC Swaps, all economic returns of the Offer Shares subscribed by GTJA Investment 
will be passed to the respective GTHT Ultimate Clients and all economic loss shall be borne by the respective GTHT Ultimate Clients through the GTHT OTC 
Swaps. GTJA Investment will not take part in any economic return or bear any economic loss in relation to the Offer Shares. The GTHT OTC Swaps are linked 
to the Offer Shares. The GTHT Ultimate Clients may request to early terminate the GTHT OTC Swaps at their own discretion, upon which GTJA Investment 
may dispose of the Offer Shares and settle the GTHT OTC Swaps in cash in accordance with the terms and conditions of the GTHT OTC Swaps. Despite that 
GTJA Investment will hold the legal title of the Offer Shares by itself, it will not exercise the voting rights attaching to the relevant Offer Shares during the terms 
of the GTHT OTC Swaps according to its internal policy. 
 
Details of the GTHT Ultimate Clients are set out as follows: 
GTHT Onshore Ultimate Clients 
Ultimate Beneficial Owners (“UBO”) 
Remarks 
Commando 
Commando 
Youyou 
Enjoyment 
Private 
Securities Investment Fund 
N/A 
N/A 
Commando 
No. 
110 
Private 
Securities 
Investment Fund 
GUO Hongqi (郭紅奇) 
UBO with over 30% interest 
Commando 
No. 
108 
Private 
Securities 
Investment Fund 
HUANG Xiaolei (黃曉蕾) 
UBO with over 30% interest 
Commando 
Kangding 
No. 
2 
Active 
Management Private Securities Investment 
Fund 
N/A 
N/A 
Commando HENIU No.1 Private Securities 
Investment Fund 
N/A 
N/A 
Xinhong Commando Ying Active Management 
Private Securities Investment Fund 
DING Ying (丁楹) 
UBO with over 30% interest 
Commando No. 105 Investment Fund 
DING Ying (丁楹) 
UBO with over 30% interest 
Commando No. 003 Active Management 
Private Securities Investment Fund 
N/A 
N/A 
Commando No. 106 Active Management 
Private Securities Investment Fund 
N/A 
N/A 
Commando 
No. 
111 
Private 
Securities 
Investment Fund 
FEI Zhenying (費振英) and ZHOU Kun (周琨) UBO with over 30% interest 
Other GTHT Onshore Ultimate Clients 

<<<PAGE 27>>>
 
 
Yinwan Quanying No.82 Private Securities 
Investment Fund 
N/A 
N/A 
Zhonghe Capital Cultivation 810 Private 
Securities Investment Fund 
N/A 
N/A 
Binghao 
Selected 
Multi-Strategy 
Private 
Securities Investment Fund 
ZHAO Bainian (趙柏年) 
UBO with over 30% interest 
 
 
 
To the best of GTJA Investment’s knowledge, each of the GTHT Ultimate Clients is an Independent Third Party of GTJA Investment, GTHT Onshore Parent 
and the companies which are members of the same group of GTHT Onshore Parent. 
(3) 
GFGC is to invest on non-discretionary basis. GFGC and GF Securities Co., Ltd. will enter into a series of cross border delta one OTC swap transactions (the 
“OTC Swaps”) with each other and the ultimate client, Qingdao Guanlan Investment Management Co., Ltd. (青島觀瀾投資管理有限公司) (“Qingdao 
Guanlan” or the “GFGC Ultimate Client”), pursuant to which GFGC will hold the Offer Shares on a non-discretionary basis to hedge the OTC Swaps while 
the economic risks and returns of the underlying Offer Shares are passed to the GFGC Ultimate Client, subject to customary fees and commissions. The OTC 
swaps will be fully funded by the GFGC Ultimate Client. During the terms of the OTC Swaps, all economic returns of the Offer Shares subscribed by GFGC 
will be passed to the GFGC Ultimate Client and all economic loss shall be borne by the GFGC Ultimate Client through the OTC Swaps, and GFGC will not take 
part in any economic return or bear any economic loss in relation to the Offer Shares. The OTC Swaps are linked to the Offer Shares and the GFGC Ultimate 
Clients may request GFGC to redeem it at its own discretion, upon which GFGC shall dispose of the Offer Shares and settle OTC Swaps in cash in accordance 
with the terms and conditions of the OTC Swap. Despite that GFGC will hold the legal title of the Offer Shares by itself, it will not exercise the voting rights 
attaching to the relevant Offer Shares during the terms of the OTC Swaps according to its internal policy.  
 
GFGC will hold the Offer Shares for and on behalf of one ultimate client on non-discretionary basis, namely Qingdao Guanlan Investment Management Co., 
Ltd. (青島觀瀾投資管理有限公司), where except for ZHANG Yanfeng (張延豐), no ultimate beneficial owners hold 30% or more interest. 
To the best of GFGC’s knowledge, the GFGC Ultimate Client is an Independent Third Party of GFGC, GF Securities (Hong Kong) Brokerage Limited and the 
companies which are members of the same group of GFGC and GF Securities (Hong Kong) Brokerage. 
(4) 
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial public offerings (“IPOs”) in Hong Kong. However, PRC 
investors are permitted to invest in products issued by appropriate domestic securities firms licensed to undertake cross-border derivatives trading activities. In 
connection with such products, the licensed domestic securities firms, through their Hong Kong affiliates, may participate in Hong Kong IPOs either as placees 
or cornerstone investors (the “Cross-border Derivatives Trading Regime”). 
 
Huatai Securities Co., Ltd. (“Huatai Securities”), the shares of which are listed on both the Shanghai Stock Exchange (stock code: 601688) and the Stock 
Exchange (stock code: 6886), is one of the domestic securities firms licensed to undertake cross-border derivatives trading activities. Huatai Securities entered 
into an ISDA agreement (the “ISDA Agreement”) with its indirectly wholly-owned subsidiary, HTCI, to set out the principal terms of any future total return 
swap between Huatai Securities and HTCI. 
HTFH is a non-sydicate distributor in connection with the Global Offering. Pursuant to an ISDA agreement entered into between Huatai Securities and HTCI, 
HTCI, which intends to participate in the Global Offering as a placee, will hold the beneficial interest of the Offer Shares on a non-discretionary basis as the 
single underlying holding under a back-to-back total return swap (“Huatai Back-to-back TRS”) to be entered by HTCI in connection with a Client TRS (as 
defined below) placed by and fully funded (i.e., with no financing provided by HTCI) by Huatai Onshore Ultimate Clients (as defined below), by which, HTCI 

<<<PAGE 28>>>
 
 
will, subject to customary fees and commissions, pass the full economic exposure of the Offer Shares ultimately to the Huatai Onshore Ultimate Clients, which 
in effect, HTCI will hold the beneficial interest of the Offer Shares on behalf of the Huatai Onshore Ultimate Clients. 
HTCI and HTFH are both indirectly wholly-owned subsidiaries of Huatai Securities. Accordingly, HTCI is considered as a “connected client” of HTFH pursuant 
to paragraph 1B(7) of the Placing Guidelines. 
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (the “Huatai Onshore Ultimate Clients”) cannot directly subscribe for the 
Offer Shares but may invest in derivative products issued by domestic securities firms licenced to undertake cross-border derivatives trading activities, such as 
Huatai Securities, with the Offer Shares as the underlying assets. Instead of directly subscribing for the Offer Shares, the Huatai Onshore Ultimate Clients, 
through their investment managers, will place a total return swap order (the “Client TRS”) with Huatai Securities in connection with the Global Offering and 
Huatai Securities will place a Huatai Back-to-back TRS order to HTCI on the terms of the ISDA Agreement. In order to hedge its exposure under the Huatai 
Backto-back TRS, HTCI participates in the Global Offering and subscribes the Offer Shares through placing order with HTFH during the International Offering. 
To the best of HTCI’s knowledge and after making all reasonable enquiries, each of the Huatai Onshore Ultimate Clients is an independent third party of (i) the 
Company, the connected person and/or their respective associates thereof, and (ii) HTCI, HTFH and the companies which are members of the same group of 
HTCI. 
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Huatai Back-to-back TRS in connection with the Client TRS order placed by the Huatai 
Onshore Ultimate Clients. Pursuant to the terms of the contracts of the Huatai Back-to-back TRS and the Client TRS, during the tenor of the Huatai Back-to-
back TRS and the Client TRS, subject to customary fees and commissions, all economic returns of the Offer Shares will be ultimately passed to the Huatai 
Onshore Ultimate Clients through the Huatai Back-to-back TRS and the Client TRS and all economic loss shall be ultimately borne by the Huatai Onshore 
Ultimate Clients. HTCI will not take any economic return or bear any economic loss in relation to the Offer Shares. 
Investment in the Huatai Back-to-back TRS and the Client TRS is similar to the investment in a qualified domestic institutional investor fund (“QDII”) in the 
way that the Huatai Onshore Ultimate Clients would reap all the economic benefits of the underlying Offer Shares, except that a QDII fund would pass through 
the exchange rate exposure on both the notional value of the investment and the profit and loss of the investment. In contrast, the profit and loss of the Huatai 
Back-to-back TRS and the Client TRS factor into account the fluctuation in RMB exchange rate upon termination of the Client TRS by converting the profit and 
loss using the current exchange rate at the time of termination. As such, the Huatai Onshore Ultimate Clients would bear the exchange rate exposure of the profit 
and loss on settlement date. 
The Huatai Onshore Ultimate Clients may exercise an early termination right to terminate the Client TRS at any time from the issue date of the Client TRS which 
should be on or after the date on which the Offer Shares are listed on the Stock Exchange at their own discretions. Upon the termination upon maturity or early 
termination of the Client TRS by the Huatai Onshore Ultimate Clients, HTCI will dispose the Offer Shares on the secondary market and the Huatai Onshore 
Ultimate Clients will receive a final settlement amount in cash in accordance with the terms and conditions of the Huatai Back-to-back TRS and the Client TRS 
which should have taken into account all the economic returns or economic loss in relation to the Offer Shares. If upon the maturity of the Client TRS, the Huatai 
Onshore Ultimate Clients intend to extend the investment period, subject to further agreement between Huatai Securities and the relevant Huatai Onshore Ultimate 
Clients, the term of the Client TRS could be extended by way of a new issuance or a tenor extension. Accordingly, Huatai Securities will extend the term of the 
Huatai Back-to-back TRS by way of a new issuance or a tenor extension. 
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass through the economic exposure to the Huatai Onshore 
Ultimate Clients, each being an onshore client who places a Client TRS order with Huatai Securities in connection with the Global Offering. HTCI will not 
exercise the voting right of the Offer Shares during the tenor of the Huatai Back-to-back TRS. 
During the life of the Client TRS and Huatai Back-to-back TRS, HTCI may continue to hold the Offer Shares in its custodian account, or to hold some or all of 
the Offer Shares in a prime brokerage account for stock borrowing purposes, HTCI will lend out its holding of underlying Offer Shares in the form of stock 

<<<PAGE 29>>>
 
 
borrowing loans consistent with market practice to lower its finance costs, provided that HTCI has the ability to call back the Offer Shares on loan at any time in 
order to satisfy its obligations under the Huatai Back-to-back TRS to ensure the economic interests are ultimately passed to the Huatai Onshore Ultimate Clients. 
Details of the Huatai Onshore Ultimate Clients are set out as follows: 
Huatai Onshore Ultimate Clients 
Ultimate Beneficial Owners (“UBO”) 
Remarks 
Shanghai Weining Private Fund Management 
Co., Ltd. – Weining Qihang No. 1 Private 
Securities Investment Fund* (上海衛寧私募基
金管理有限公司－衛甯啟航 1 號私募證券投
資基金) (“Weining Qihang No. 1”) 
Liu Yutao (劉育濤) 
UBO with over 30% interest 
Shanghai Weining Private Fund Management 
Co., Ltd. – Weining Focus Private Securities 
Investment Fund* (上海衛寧私募基金管理有
限公司－衛寧聚焦私募證券投資基金) 
(“Weining Focus”) 
N/A 
N/A 
 
(5) 
 Fullgoal Fund will hold the Offer Shares in its capacity as the discretionary fund manager on behalf of its investors, each of which is an independent third party 
of the Company, its subsidiaries, its Controlling Shareholders, its substantial shareholders, Fullgoal Fund and GTJA Securities and the companies which are 
members of the same group of GTJA Securities. No ultimate beneficial owner holds 30% or more interest in the underlying investors. 
 
 

<<<PAGE 30>>>
28 
 
 
DISCLAIMERS 
 
 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and Hong 
Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or 
any part of the contents of this announcement. 
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and 
the District of Columbia). This announcement does not constitute or form a part of any offer or 
solicitation to purchase or subscribe for securities in the United States. The securities mentioned 
herein have not been, and will not be, registered under the United States Securities Act of 1933, 
as amended (the “U.S. Securities Act”). The securities may not be offered or sold in the United 
States. 
The Offer Shares are being offered and sold outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or offer to 
acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated January 30, 2026 issued by Axera Semiconductor Co., 
Ltd. for detailed information about the Global Offering described below before deciding whether 
or not to invest in the H Shares thereby being offered. 
* Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate their obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the section headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date 
(which is currently expected to be on Tuesday, February 10, 2026). 
 
PUBLIC FLOAT AND FREE FLOAT 
 
Immediately after the completion of the Global Offering, 354,583,316 H Shares, representing 
approximately 60.33% of the issued share capital of our Company (before any exercise of the Over-
allotment Option) will count towards the public float. Therefore, the number of H shares held in 
public hands is higher than the prescribed percentage of H Shares required to be held in public hands of 
15% under Rule 19A.13A(1) of the Listing Rules, satisfying the minimum percentage requirement in 
compliance with Rule 19A.13A(1) of the Listing Rules.  
 
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the Listing Date. 
As such, H Shares held by the Cornerstone Investors upon the Listing shall not be counted towards the free 
float of the H Shares of the Company at the time of Listing.  Based on the Offer Price of HK$28.20 per 
H Share, the Company satisfies the free float requirement under Rule 19A.13C(1)(b) of the Listing 
Rules. 

<<<PAGE 31>>>
29 
The Directors confirm that, immediately following completion of the Global Offering: (i) the 
Shares will be held by at least 300 Shareholders at the time of Listing, in compliance with Rule 
8.08(2) of the Listing Rules; (ii) the three largest public Shareholders will not hold more than 
50% of the H Shares held in public hands at the time of Listing, in compliance with Rules 8.08(3) 
and 8.24 of the Listing Rules; (iii) no placee will, individually, be placed more than 10% of the 
enlarged issued share capital of the Company immediately after the Global Offering; and (iv) there 
will not be any new substantial Shareholder (as defined in the Listing Rules) immediately after the Global 
Offering. 
COMMENCEMENT OF DEALINGS 
The H Share certificates will only become valid evidence of title at 8:00 a.m. (Hong Kong time) 
on Tuesday, February 10, 2026, provided that (i) the Global Offering has become unconditional in 
all respects, and (ii) the right of termination described in the section headed “Underwriting – 
Underwriting Arrangements and Expenses – Hong Kong Public Offering – Hong Kong Underwriting 
Agreement – Grounds for termination” in the Prospectus has not been exercised. Investors who trade 
H Shares prior to the receipt of H Share certificates or the H Share certificates becoming valid evidence of 
title do so entirely at their own risk. 
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. (Hong Kong 
time) on Tuesday, February 10, 2026, it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. on Tuesday, February 10, 2026. The H Shares will be traded in board 
lots of 100 H Shares each and the stock code of the H Shares will be 600. 
By order of the Board 
Axera Semiconductor Co., Ltd. 
(愛芯元智半導體股份有限公司) 
Dr. QIU Xiaoxin 
Chairman of the Board and Executive Director 
Zhejiang, China, February 9, 2026 
As at the date of this announcement, the Board comprises: (i) Dr. QIU Xiaoxin, Mr. SUN Weifeng, Mr. 
SHI Xiaoye, Mr. WANG Yuan, Mr. ZHAO Changhua* and Mr. LIU Jianwei* as executive Directors; 
(ii) Mr. ZHOU Siyuan, Mr. GU Kaining, Ms. BAI Ting, Mr. WANG Chen and Mr. ZHOU Zhifeng* as
non-executive Directors and (iii) Ms. TAN Ren, Mr. LI Jun, Dr. WANG Xin and Prof. CHEN Xin as
proposed independent non-executive Directors.
*Note: Mr. ZHAO Changhua, Mr. LIU Jianwei and Mr. ZHOU Zhifeng have tendered their
resignations from the directorships of the Company on June 23, 2025 which will take effect upon Listing.
