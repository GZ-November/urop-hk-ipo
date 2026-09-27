# 配发结果公告抽取任务：3952.HK Zhejiang Laifual Drive Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**29/06/2026 21:17**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0629/2026062902089.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"3952.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Hong Kong Stock 
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents 
of this announcement, make no representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the prospectus dated June 22, 2026 (the “Prospectus”) issued by Zhejiang Laifual Drive Co., Ltd. (浙江來
福諧波傳動股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an offer or an invitation to induce an offer 
by any person to acquire, purchase or subscribe for any of the securities of the Company. This announcement is not a 
prospectus. Potential investors should read the Prospectus for detailed information about the Global Offering described 
below before deciding whether or not to invest in the Offer Shares. Any investment decision in relation to the Offer 
Shares should be taken solely in reliance on the information provided in the Prospectus.
In connection with the Global Offering, CMB International Securities Limited (or its affiliates or any person acting for 
it), as the stabilizing manager (the “Stabilizing Manager”), on behalf of the Underwriters, to the extent permitted by 
the applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect transactions 
with a view to stabilizing or supporting the market price of the H Shares at such price, in such amounts and in such 
manners as the Stabilizing Manager, its affiliates or any person acting for it may determine and at a level higher than 
that which might otherwise prevail in the open market for a limited period after the Listing Date. However, there is 
no obligation on the Stabilizing Manager (or its affiliates or any person acting for it) to conduct any such stabilizing 
action. Such stabilizing actions, if taken, (a) will be conducted at the absolute discretion of the Stabilizing Manager 
(or its affiliates or any person acting for it) and in what the Stabilizing Manager (or its affiliates or any person acting 
for it) reasonably regards as the best interest of our Company, (b) may be discontinued at any time, and (c) is required 
to be brought to an end within 30 days of the last day for lodging applications under the Hong Kong Public Offering 
(which is Saturday, July 25, 2026). Such stabilization action, if taken, may be effected in all jurisdictions where it is 
permissible to do so, in each case in compliance with all applicable laws, rules and regulatory requirements, including 
the Securities and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made 
under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering (which is Saturday, July 25, 2026). 
After this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the price of 
the H Shares, could fall.
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
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions set out in 
the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not 
resident in Hong Kong.
Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinator (for itself and on behalf of the 
Hong Kong Underwriter) shall be entitled to terminate its obligations under the Hong Kong Underwriting Agreement 
with immediate effect upon the occurrence of any of the events set out in the paragraph headed “Underwriting – 
Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus 
at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Tuesday. 
June 30, 2026).

<<<PAGE 2>>>
2
Zhejiang Laifual Drive Co., Ltd.
浙江來福諧波傳動股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under
the Global Offering
:
13,441,900 H Shares (subject to the
 Over-allotment Option)
Number of Hong Kong Offer Shares
:
2,688,400 H Shares (as adjusted after 
 reallocation)
Number of International Offer Shares
:
10,753,500 H Shares (as adjusted after 
 reallocation and subject to the 
 Over-allotment Option)
Final Offer Price
:
HK$85.50 per H Share, plus brokerage of 
 1%, SFC transaction levy of 0.0027%, 
 Stock Exchange trading fee of 0.00565% and 
 AFRC transaction levy of 0.00015%
Nominal value
:
RMB1.00 per H Share
Stock code
:
3952
Sole Sponsor, Sponsor-Overall Coordinator, Sole Global Coordinator,
Sole Bookrunner and Sole Lead Manager

<<<PAGE 3>>>
3
Zhejiang Laifual Drive Co., Ltd.
浙江來福諧波傳動股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated June 22, 2026 (the “Prospectus”) issued by 
Zhejiang Laifual Drive Co., Ltd. (浙江來福諧波傳動股份有限公司) (the “Company”).
SUMMARY
Warning: In view of high concentration of shareholding in a small number of H 
Shareholders, H Shareholders and prospective investors should be aware that the price of 
the H Shares could move substantially even with a small number of H Shares traded and 
should exercise extreme caution when dealing in the H Shares.
Company information
Stock code
3952
Stock short name
LAIFUAL
Dealings commencement date
June 30, 2026*
* see note at the end of the announcement
Price Information
Final Offer Price
HK$85.50
Offer Price Range
HK$77.00-HK$85.50
Offer Price Adjustment exercised
N/A
Offer Shares and Share Capital
Number of Offer Shares (before exercise of 
 the Over-allotment Option)
13,441,900
Number of Offer Shares in the Hong Kong 
 Public Offering (after reallocation)
2,688,400
Number of Offer Shares in the International 
 Offering (after reallocation)
10,753,500
Number of issued shares upon Listing
 (before exercise of the Over-allotment
 Option)
103,398,787
Over-allocation
Number of Offer Shares over-allocated
2,016,200
Proceeds
Gross proceeds Note
HK$1,149.3 million
 Less: Estimated listing expenses payable 
based on Final Offer Price
HK$76.2 million
Net proceeds
HK$1,073.1 million
Note: Gross proceeds refers to the amount to which the issuer is entitled receive. For details of the use of proceeds, please refer to the 
section headed “Future Plans and Use of Proceeds” in the Prospectus. Assuming the Over-allotment Option is not exercised.

<<<PAGE 4>>>
4
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
182,737
No. of successful applications
26,884
Subscription level
4,571.99 times
Claw-back triggered
Yes
No. of Offer Shares initially available under the Hong Kong Public Offering
672,100
No. of Offer Shares reallocated from the International Offering (claw-back)
2,016,300
Final no. of Offer Shares under the Hong Kong Public Offering (after claw-
back)
2,688,400
% of Offer Shares under the Hong Kong Public Offering to the Global 
Offering
20%
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors can 
refer to www.hkeipo.hk/IPOResult to perform a search by name or identification number or 
www.hkeipo.hk/IPOResult for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
93
Subscription level
7.89 times
No. of Offer Shares initially available under the International Offering
12,769,800
No. of Offer Shares reallocated to the Hong Kong Public Offering
2,016,300
Final no. of Offer Shares under the International Offering (after claw-back)
10,753,500
% of Offer Shares under the International Offering to the Global Offering
80%
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a 
consent under paragraph 1C(1) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) 
and Chapter 4.15 of the Guide for New Listing Applicants granted by the Stock Exchange to permit 
the Company to allocate certain Offer Shares to a connected client; and (b) a waiver under Rule 
10.04 of the Listing Rules and a consent under paragraph 1C(2) of the Placing Guidelines granted 
by the Stock Exchange to permit the Company to allocate certain Offer Shares to a close associate 
of an existing Shareholder,  (i) none of the Offer Shares subscribed by the placees and the public 
have been financed directly or indirectly by the Company, any of the Directors, chief executive 
of the Company, the Single Largest Group of Shareholders, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates; and (ii) 
none of the placees and the public who have purchased the Offer Shares are accustomed to taking 
instructions from the Company, any of the Directors, chief executive of the Company, the Single 
Largest Group of Shareholders, substantial Shareholders, existing Shareholders of the Company or 
any of its subsidiaries or their respective close associates in relation to the acquisition, disposal, 
voting or other disposition of Shares registered in his/her/its name or otherwise held by him/her/it.

<<<PAGE 5>>>
5
The placees in the International Offering include the following:
Cornerstone Investors
Investor (Note 1)
Number of 
Offer Shares 
purchased
% of Offer 
Shares (Note 2)
% of total 
issued H 
Shares after 
the Global 
Offering (Note 2)
% of total 
issued share 
capital after 
the Global 
Offering (Note 2)
Existing 
Shareholders 
or their close 
associates
OAKTREE CAPITAL 
MANAGEMENT, L.P.
916,400
6.82%
0.89%
0.89%
No
Alphahill Capital Limited
916,400
6.82%
0.89%
0.89%
No
HARVEST GLOBAL INVESTMENTS 
LIMITED (嘉實國際資產管理有限公司)
733,100
5.45%
0.71%
0.71%
No
CDH Global Frontier Ventures Limited
641,400
4.77%
0.62%
0.62%
No
E Fund Management Co., Ltd/
E FUND MANAGEMENT (HONG KONG) 
CO., LIMITED (易方達資產管理(香港)
有限公司)
458,200
3.41%
0.44%
0.44%
No
Eurus Holdings SPC acting for and on 
behalf of OAAM Diversified Opportunities 
IV S.P.
274,900
2.05%
0.27%
0.27%
No
LBC HK Opportunity Fund Limited
274,900
2.05%
0.27%
0.27%
No
Dream’ee (Hong Kong) Open-ended 
Fund Company
274,900
2.05%
0.27%
0.27%
No
Factorial Master Fund
274,900
2.05%
0.27%
0.27%
No
Oasis Investments II Master Fund Ltd.
274,900
2.05%
0.27%
0.27%
No
Subtotal
5,040,000
37.52%
4.90%
4.90%
Notes: 
1. 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in 
the Prospectus.
2. 
Assuming the Over-allotment Option is not exercised.

<<<PAGE 6>>>
6
Allottees with Waivers/Consents Obtained
Investor
Number 
of Offer 
Shares 
allocated
% of 
Offer 
Shares 
(Note 1)
% of total 
issued H 
Shares 
after 
the Global 
Offering (Note 1)
% of total 
issued 
share 
capital 
after 
the Global 
Offering (Note 1)
Relationship
Allottee with waiver from strict compliance under Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of 
the Placing Guidelines in relation to allocations to a close associate of an existing Shareholder
ZIJINNING Limited 
Partnership (Notes 2, 3)
165,000
1.23%
0.16%
0.16%
A close associate of an 
existing Shareholder
Allottees with consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to connected clients
CMBI (Singapore) Pte. 
Limited (Note 4)
91,000
0.68%
0.09%
0.09%
Connected client 
as a placee
Huatai Capital Investment 
Limited (Note 4)
4,600
0.03%
0.004%
0.004%
Connected client 
as a placee
Notes:
1. 
Assuming the Over-allotment Option is not exercised.
2. 
Zhuji Rushan Huian Venture Capital Partnership (L.P.) (諸暨如山匯安創業投資合夥企業(有限合夥)) 
(“Rushan Huian”) is an existing Shareholder. The general partner of Rushan Huian is Zhejiang Rushan 
Huijin Private Equity Fund Management Co., Ltd. (浙江如山匯金私募基金管理有限公司), which is 
ultimately owned and controlled by Zijin Mining Group Company Limited (紫金礦業集團股份有限公司) 
(stock code: 601899.SZ and 02899.HK). ZIJINNING Limited Partnership is wholly owned by Zijin Mining 
Group Company Limited, and hence it is a close associate of Rushan Huian.
3. 
For details of the consents under paragraph 1C(2) of the Placing Guidelines and Chapter 4.15 of the 
Guide for New Listing Applicant in relation to allocations to a close associate of an existing Shareholder, 
please refer to the paragraph headed “Others/Additional Information — Placing to a close associate of an 
existing Shareholder with prior waiver under Rule 10.04 and consent under paragraph 1C(2) of the Placing 
Guidelines” in this announcement.
4. 
Saved as listed out, the H Shares placed to such allottees are held on behalf of independent third parties 
(as defined in Chapter 4.15 of the Guide for New Listing Applicants) and are in compliance with all the 
conditions under the consent granted by the Stock Exchange. For details of the consent under paragraph 1C(1) 
of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations 
to connected clients, please refer to the paragraph headed “Others/Additional Information — Placing to 
connected clients with prior consents under paragraph 1C(1) of the Placing Guidelines” in this announcement.

<<<PAGE 7>>>
7
LOCK-UP UNDERTAKINGS
Key Persons (as defined under Rule 18C.14 of the Listing Rules)
Name
Number of 
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
(Note 1)
% of 
shareholding in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing 
(Note 1)
Last day 
subject to 
the lock-up 
undertakings (Note 2)
Mr. Zhang Jie (張傑) (“Mr. 
Zhang”)
3,712,072
3,712,072
3.59%
3.59%
June 29, 2027
Shengzhou Laifu Investment 
Management Partnership 
(Limited Partnership) (嵊州市
來福投資管理合夥企業(有限合
夥)) (“Laifu Investment”) (Note 3)
21,098,226
21,098,226
20.40%
20.40%
June 29, 2027
Shengzhou Jieyang Information 
Consulting Partnership (Limited 
Partnership) (嵊州市傑陽信
息諮詢合夥企業(有限合夥)) 
(“Jieyang Information”) (Note 4)
4,578,577
4,578,577
4.43%
4.43%
June 29, 2027
Subtotal
29,388,875
29,388,875
28.42%
28.42%
Notes:
1. 
Assuming the Over-allotment Option is not exercised.
2. 
Pursuant to the applicable PRC law, within the 12 months following the Listing Date, all existing Shareholders 
(including the Pre-IPO Investors) are prohibited from disposing of any of the Shares held by them. Pursuant 
to Rule 18C.14(1) of the Listing Rules, the required lock-up period commences on the date by reference to 
which disclosure of their shareholdings in the Company is made in the Prospectus and end on the date upon 
the expiry of 12 months from the Listing Date, being the same date on which the restriction against disposal of 
Shares under the applicable PRC laws ends.
3. 
The general partner of Laifu Investment is Shengzhou Shunhe Information Consulting Co., Ltd. (嵊州市順
和信息諮詢有限公司) (“Shengzhou Shunhe”), a company which is held as to 99% by Mr. Zhang and 1% 
by Ms. Qian Songyu (錢松魚), a former employee of the Group. Ms. Qian Songyu served as the Company’s 
financial head at the early stage of its establishment and invested his own funds to acquire a 1% equity interest 
in Shengzhou Shunhe in connection with the Company’s early development and equity incentive arrangements. 
The limited partners of Laifu Investment consists of Mr. Zhang, who held approximately 58.83% of limited 
partnership interests, and 12 individuals who are Independent Third Parties. Except for Mr. Zhang, whose 
interests in the Company through his control over the general partner of Laifu Investment shall be subject to 
disposal restrictions pursuant to Rule 18C.14 of the Listing Rules, none of the 12 individuals holds 30% or 
more interest in Laifu Investment or is a Director, senior management and core R&D employee of the Group.
4. 
Jieyang information was established as the Group’s employee share ownership platform, under which the 
eligible participants (including our executive Directors, Mr. Zhang, Mr. Wu Di, Ms. Wang Haiying and Mr. 
Zhang Han, our senior management Ms. Xue Wei and Mr. Zhou Wenjun as well as a core R&D employee of 
the Group) were awarded partnership interest in the Employee Share Ownership Platforms. Mr. Zhang held 
general partnership interests in Jieyang Information as to 70.57%, Mr. Wu Di, Ms. Wang Haiying, Mr. Zhang 
Han, Ms. Xue Wei, Mr. Zhou Wenjun and Mr. Shen Zhongfu held limited partnership interests in Jieyang 
Information as to 1.09%, 0.55%, 2.18%, 0.66%, 1.31% and 1.31%, respectively. Mr. Zhang, Mr. Wu Di, 
Ms. Wang Haiying and Mr. Zhang Han serve as the Company’s executive Directors. Ms. Xue Wei and Mr. 
Zhou Wenjun are the Company’s senior management members. Mr. Shen Zhongfu, the deputy director of 
our Laifual-Chongqing University Institute, operations director and process engineering department manager, 
is the Group’s core R&D employee for the purpose of Rule 18C.14 of the Listing Rules. All the above 
executive Directors, senior management members and key persons of the Company shall be subject to disposal 
restrictions pursuant to Rule 18C.14 of the Listing Rules. Please refer to the section headed “History and 
Corporate Structure — Employee Share Ownership Platform” of the Prospectus for further details.

<<<PAGE 8>>>
8
Pathfinder SIIs
Name(Note 1)
Number of 
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
(Note 2)
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing 
(Note 2)
Last day 
subject to 
the lock-up 
undertakings (Note 3)
Hubei Lenovo Yangtze 
River Technology Industrial 
Fund Partnership (Limited 
Partnership) (湖北省聯想長江
科技產業基金合夥企業(有限
合夥))
5,082,259
5,082,259
4.92%
4.92%
June 29, 2027
CDBC Manufacturing Industry 
Transformation and Upgrading 
Fund (Limited Partnership) (國
開製造業轉型升級基金(有限
合夥))
8,995,689
8,995,689
8.70%
8.70%
June 29, 2027
Subtotal
14,077,948
14,077,948
13.62%
13.62%
Notes:
1. 
Each of the Shareholders listed in the above table is a Pathfinder SII of the Company as defined under 
Chapter 2.5 of the Guide for New Listing Applicants. Please refer to the section headed “History and 
Corporate Structure – Capitalization of our Company” in the Prospectus for further details.
2. 
Assuming the Over-allotment Option is not exercised.
3. 
Pursuant to the applicable PRC law, within the 12 months following the Listing Date, i.e. June 29, 2027, all 
existing Shareholders (including the Pre-IPO Investors) are prohibited from disposing of any of the Shares 
held by them. Pursuant to Rule 18C.14(2) of the Listing Rules, the required lock-up period commences on 
the date by reference to which disclosure of their respective shareholdings in the Company is made in the 
Prospectus and ends on the date upon the expiry of six months from the Listing Date, i.e. December 29, 2026.

<<<PAGE 9>>>
9
Existing Shareholders (other than the Key Persons and the Pathfinder SIIs)
Name(Note 1)
Number of 
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
(Note 2)
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing 
(Note 2)
Last day 
subject to 
the lock-up 
undertakings (Note 3)
Beta Achieve Limited (越焯有
限公司)
10,209,771
10,209,771
9.87%
9.87%
June 29, 2027
Guozhong SME Development 
Private Equity Investment 
Fund Partnership (Limited 
Partnership) (深圳國中中小企
業發展私募股權投資基金合夥
企業(有限合夥))
6,715,833
6,715,833
6.50%
6.50%
June 29, 2027
Zhuji Rushan Huian Venture 
Capital Partnership (L.P.) (諸
暨如山匯安創業投資合夥企業
(有限合夥))
6,259,616
6,259,616
6.05%
6.05%
June 29, 2027
Redview Capital Investment 
XIV Limited
5,453,345
5,453,345
5.27%
5.27%
June 29, 2027
China Electronics CICC 
(Xiamen) Intelligent Industry 
Equity Investment Fund 
Partnership (L.P) (中電中金(廈
門)智能產業股權投資基金合
夥企業(有限合夥))
5,082,259
5,082,259
4.92%
4.92%
June 29, 2027
Guozhong SME Fund Haian 
Huijun Jincai Phase I Industrial 
Investment Partnership 
Enterprise (L.P.) (海安惠浚金
財一期產業投資合夥企業(有
限合夥))
3,490,118
3,490,118
3.38%
3.38%
June 29, 2027
Suzhou Sushang Joint Venture 
Capital Partnership (L.P) (蘇
州蘇商聯合產業投資合夥企業
(有限合夥))
3,182,091
3,182,091
3.08%
3.08%
June 29, 2027

<<<PAGE 10>>>
10
Name(Note 1)
Number of 
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
(Note 2)
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing 
(Note 2)
Last day 
subject to 
the lock-up 
undertakings (Note 3)
Shanghai Hongyu Aviation 
Industry Equity Investment 
Partnership (L.P) (上海泓宇航
空產業股權投資合夥企業(有
限合夥))
3,182,092
3,182,092
3.08%
3.08%
June 29, 2027
Tianjin Haihe Furui Equity 
Investment Fund Partnership 
(L.P) (天津海河福睿股權投資
基金合夥企業(有限合夥))
1,551,956
1,551,956
1.50%
1.50%
June 29, 2027
Hangzhou Runxin Dianjing 
Equity Investment Partnership 
(L.P) (杭州潤心點精股權投資
合夥企業(有限合夥))
1,362,983
1,362,983
1.32%
1.32%
June 29, 2027
Subtotal
46,490,064
46,490,064
44.97%
44.97%
Notes:
1. 
Please refer to the Prospectus for further details.
2. 
Assuming the Over-allotment Option is not exercised.
3. 
The expiry date of the lock-up period shown in the table above is pursuant to applicable PRC laws.

<<<PAGE 11>>>
11
Cornerstone Investors
Name
Number of
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
(Note 1)
% of
shareholding
in the
Company
subject to
lock-up
undertakings
upon Listing 
(Note 1)
Last day
subject to
the lock-up
undertakings 
(Note 2)
OAKTREE CAPITAL 
MANAGEMENT, L.P.
916,400
916,400
0.89%
0.89%
December 29, 2026
Alphahill Capital Limited
916,400
916,400
0.89%
0.89%
December 29, 2026
HARVEST GLOBAL 
INVESTMENTS LIMITED (嘉
實國際資產管理有限公司)
733,100
733,100
0.71%
0.71%
December 29, 2026
CDH Global Frontier Ventures 
Limited
641,400
641,400
0.62%
0.62%
December 29, 2026
E Fund Management Co., Ltd/
E FUND MANAGEMENT 
(HONG KONG) CO., 
LIMITED (易方達資產管理(香
港)有限公司)
458,200
458,200
0.44%
0.44%
December 29, 2026
Eurus Holdings SPC acting 
for and on behalf of OAAM 
Diversified Opportunities IV 
S.P.
274,900
274,900
0.27%
0.27%
December 29, 2026
LBC HK Opportunity Fund 
Limited
274,900
274,900
0.27%
0.27%
December 29, 2026
Dream’ee (Hong Kong) Open-
ended Fund Company
274,900
274,900
0.27%
0.27%
December 29, 2026
Factorial Master Fund
274,900
274,900
0.27%
0.27%
December 29, 2026
Oasis Investments II Master 
Fund Ltd.
274,900
274,900
0.27%
0.27%
December 29, 2026
Subtotal
5,040,000
5,040,000
4.90%
4.90%
Notes:
1. 
Assuming the Over-allotment Option is not exercised.
2. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on December 
29, 2026, being six months following the Listing Date. The Cornerstone Investors will cease to be prohibited 
from disposing of or transferring H Shares subscribed for pursuant to the relevant cornerstone investment 
agreements after the indicated date.

<<<PAGE 12>>>
12
PLACEE CONCENTRATION ANALYSIS
Placees *
Number of 
H Shares 
allotted
Allotment 
as % of 
International
Offering **
Allotment 
as % 
of total Offer 
Shares **
Number of 
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing **
Top 1
916,400
8.52%
6.82%
916,400
0.89%
Top 5
4,120,600
38.32%
30.65%
4,120,600
3.99%
Top 10
6,379,200
59.32%
47.46%
6,379,200
6.17%
Top 25
10,508,400
97.72%
78.18%
10,508,400
10.16%
Note:
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
** 
Assuming the Over-allotment Option is not exercised.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders *
Number of
H Shares 
allotted
Number of H 
Shares 
allocated
under 
International
Offering
Allotment 
as % of 
International
Offering **
Allotment as 
% of total 
Offer 
Shares **
Number of 
H Shares held 
upon Listing
Number of 
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing **
Top 1
–
–
0.00%
0.00%
29,388,875
29,388,875
28.4%
Top 5
165,000
165,000
1.53%
1.23%
61,734,784
61,734,784
59.7%
Top 10
165,000
165,000
1.53%
1.23%
84,024,857
84,024,857
81.3%
Top 25
7,284,200
7,284,200
67.74%
54.19%
97,241,087
97,241,087
94.0%
Note:
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholder upon Listing.
** 
Assuming the Over-allotment Option is not exercised.

<<<PAGE 13>>>
13
SHAREHOLDERS CONCENTRATION ANALYSIS
Shareholders *
Number of
H Shares 
allotted
Number of H 
Shares 
allocated
under 
International
Offering
Allotment 
as % of 
International
Offering **
Allotment as 
% of total 
Offer Shares **
Number of 
H Shares held 
upon Listing
Number of 
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing **
Top 1
–
–
0.00%
0.00%
29,388,875
29,388,875
28.4%
Top 5
165,000
165,000
1.53%
1.23%
61,734,784
61,734,784
59.7%
Top 10
165,000
165,000
1.53%
1.23%
84,024,857
84,024,857
81.3%
Top 25
7,284,200
7,284,200
67.74%
54.19%
97,241,087
97,241,087
94.0%
Note:
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.
** 
Assuming the Over-allotment Option is not exercised.

<<<PAGE 14>>>
14
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Number of 
H Shares 
applied for
Number of 
valid 
applications
Approximate 
percentage 
allotted of the 
total number of 
H Shares 
applied for
Pool A
Basis of allocation/ballot
100
63,206
3,161 out of 63,206 applicants to receive 100 H Shares
5.00%
200
7,754
450 out of 7,754 applicants to receive 100 H Shares
2.90%
300
5,117
324 out of 5,117 applicants to receive 100 H Shares
2.11%
400
3,421
230 out of 3,421 applicants to receive 100 H Shares
1.68%
500
17,665
1,246 out of 17,665 applicants to receive 100 H Shares
1.41%
600
3,061
225 out of 3,061 applicants to receive 100 H Shares
1.23%
700
1,686
128 out of 1,686 applicants to receive 100 H Shares
1.08%
800
1,569
123 out of 1,569 applicants to receive 100 H Shares
0.98%
900
1,051
85 out of 1,051 applicants to receive 100 H Shares
0.90%
1,000
9,827
804 out of 9,827 applicants to receive 100 H Shares
0.82%
1,500
3,021
270 out of 3,021 applicants to receive 100 H Shares
0.60%
2,000
2,946
280 out of 2,946 applicants to receive 100 H Shares
0.48%
2,500
2,049
204 out of 2,049 applicants to receive 100 H Shares
0.40%
3,000
2,182
226 out of 2,182 applicants to receive 100 H Shares
0.35%
3,500
1,633
175 out of 1,633 applicants to receive 100 H Shares
0.31%
4,000
1,511
167 out of 1,511 applicants to receive 100 H Shares
0.28%
4,500
1,303
147 out of 1,303 applicants to receive 100 H Shares
0.25%
5,000
2,915
337 out of 2,915 applicants to receive 100 H Shares
0.23%
6,000
2,387
287 out of 2,387 applicants to receive 100 H Shares
0.20%
7,000
1,934
240 out of 1,934 applicants to receive 100 H Shares
0.18%
8,000
1,644
210 out of 1,644 applicants to receive 100 H Shares
0.16%
9,000
1,239
162 out of 1,239 applicants to receive 100 H Shares
0.15%
10,000
7,917
1,059 out of 7,917 applicants to receive 100 H Shares
0.13%
20,000
5,648
876 out of 5,648 applicants to receive 100 H Shares
0.08%
30,000
4,205
711 out of 4,205 applicants to receive 100 H Shares
0.06%
40,000
2,614
470 out of 2,614 applicants to receive 100 H Shares
0.04%
50,000
4,478
845 out of 4,478 applicants to receive 100 H Shares
0.04%
Total
163,983
Total number of Pool A successful applicants: 13,442

<<<PAGE 15>>>
15
Number of 
H Shares 
applied for
Number of 
valid 
applications
Approximate 
percentage 
allotted of the 
total number of 
H Shares 
applied for
Pool B
Basis of allocation/ballot
60,000
6,419
3,852 out of 6,419 applicants to receive 100 H Shares
0.10%
70,000
1,835
1,155 out of 1,835 applicants to receive 100 H Shares
0.09%
80,000
1,283
842 out of 1,283 applicants to receive 100 H Shares
0.08%
90,000
982
669 out of 982 applicants to receive 100 H Shares
0.08%
100,000
2,838
2,009 out of 2,838 applicants to receive 100 H Shares
0.07%
150,000
1,654
1,340 out of 1,654 applicants to receive 100 H Shares
0.05%
200,000
1,035
907 out of 1,035 applicants to receive 100 H Shares
0.04%
250,000
651
619 out of 651 applicants to receive 100 H Shares
0.04%
300,000
345
337 out of 345 applicants to receive 100 H Shares
0.03%
336,000
1,712
100 H Shares
0.03%
Total
18,754
Total number of Pool B successful applicants: 13,442
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.

<<<PAGE 16>>>
16
OTHERS/ADDITIONAL INFORMATION
Reallocation
As the Hong Kong Offer Shares have been oversubscribed by more than 4,571.99 times of the total 
number of Offer Shares initially available under the Hong Kong Public Offering, the reallocation 
procedure as described in the section headed “Structure of the Global Offering — The Hong Kong 
Public Offering — Reallocation” in the Prospectus has been applied.
The number of Offer Shares initially available under the Hong Kong Public Offering is 672,100 
H Shares, representing 5% of the total number of Offer Shares initially available under the Global 
Offering. As a result of such reallocation, the final number of Offer Shares under the Hong Kong 
Public Offering is adjusted to 2,688,400 H Shares, representing approximately 20% of the total 
number of Offer Shares available under the Global Offering.
Each of the Directors, the Sole Sponsor and the Sponsor-Overall Coordinator (for itself and on 
behalf of the Underwriters) confirms that the reallocation of 2,016,300 Offer Shares from the 
International Offering to the Hong Kong Public Offering, which results in the total number of the 
Offer Shares available under the Hong Kong Public Offering to increase to 2,688,400 Offer Shares, 
representing approximately 20% of the number of the Offer Shares initially available under the 
Global Offering, is in compliance with the restrictions set forth under paragraphs 8 and 9 of the 
Chapter 4.14 of the Guide For New Listing Applicants.

<<<PAGE 17>>>
17
Placing to a close associate of an existing Shareholder with a prior waiver under Rule 10.04 
and consent under paragraph 1C(2) of the Placing Guidelines
The Company has applied for a waiver under Rule 10.04 and consent under paragraph 1C(2) of 
the Placing Guidelines, to permit the existing shareholders and/or its close associates to participate 
as placees in the Global Offering to subscribe for the Offer Shares to be issued by the Company 
under the International Offering (together, the “Permitted Participants”). The Stock Exchange 
has agreed to grant the requested waiver and consent subject to the conditions that:
(a) 
the allocation to the Permitted Participants will not affect the Company’s ability to satisfy its 
public float requirement under Rule 8.08(1) (as amended and replaced by Rule 19A.13A) of 
the Listing Rules;
(b) 
the Company and the Sole Sponsor will confirm to the Stock Exchange that no preferential 
treatment has been, nor will be directly or indirectly, given to the Permitted Participants 
by virtue of their relationship with the Company or in any allocation in the International 
Offering;
(c) 
the allocation to the Permitted Participants would not affect the Company’s compliance with 
the price discovery requirement under Rule 18C.08C of the Listing Rules for the following 
reasons:
a. 
sufficient number of Offer Shares will remain available for allocation to the independent 
price setting investors in the placing tranche in accordance with the requirements under 
paragraph 42 of Chapter 2.5 of the Guide; and
b. 
it would not compromise the free float requirement under Rule 19A.13C of the Listing 
Rules, as there will remain sufficient H Shares held by the public and available for 
trading upon Listing; and
(d) 
details of the allocation of the Offer Shares to the Permitted Participants as placees under the 
Global Offering will be disclosed in this allotment results announcement of the Company.
For details of the allocations of Offer Shares to such Permitted Participants, please refer to the 
section headed “Allotment Results Details – International Offering – Allottees with waiver/
consents obtained” in this announcement.

<<<PAGE 18>>>
18
Placing to connected clients with prior consents under paragraph 1C(1) of the Placing 
Guidelines 
Under the International Offering, certain Offer Shares were placed to connected clients of certain 
distributors pursuant to the Placing Guidelines. The Company has applied to the Stock Exchange 
for, and the Stock Exchange has granted, a consent under paragraph 1C(1) of the Placing 
Guidelines to permit the Company to allocate such Offer Shares in the International Offering to the 
connected clients. The allocation of Offer Shares to such connected clients is in compliance with 
all the conditions under the consent granted by the Stock Exchange.
Details of the placement to connected clients are set out below:
No.
Connected 
Clients
Connected 
Distributor
Relationship 
between the 
Connected 
Client and the 
Connected 
Distributor
Whether the 
Connected 
Client will hold 
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
Number of 
H Shares to 
be allocated
Approximate 
percentage 
of Offer 
Shares in 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option not 
exercised)
Approximate 
percentage 
of Offer 
Shares in 
the Global 
Offering 
(assuming 
the Over-
allotment 
Option 
exercised)
Approximate 
percentage 
of the total 
issued share 
capital 
immediately 
following 
completion 
of the Global 
Offering 
(assuming 
the Over-
allotment 
Option not 
exercised)
Approximate 
percentage 
of the total 
issued share 
capital 
immediately 
following 
completion 
of the Global 
Offering 
(assuming 
the Over-
allotment 
Option 
exercised)
1
CMBI 
(Singapore) 
Pte. Limited 
(“CMBI 
SG”) 
(1)
CMB 
International 
Capital Limited 
(“CMBI”)
CMBI SG is a 
member of the 
same group with 
CMBI
Discretionary 
basis
91,000
0.677%
0.589%
0.088%
0.086%
2
Huatai 
Capital 
Investment 
Limited 
(“HTCI”)(2)
Huatai Financial 
Holdings (Hong 
Kong) Limited 
(“HTFH”)
HTCI is a 
member of the 
same group of 
companies as 
HTFH
Non-
discretionary 
basis
4,600
0.034%
0.030%
0.004%
0.004%
Notes:
(1) 
CMBI (Singapore) Pte. Limited
CMBI (Singapore) Pte. Limited (“CMBI SG”) will hold the Offer Shares in its capacity as discretionary fund 
manager managing assets on behalf of its underlying client. To the best of CMBI SG’s knowledge after due 
enquiry, the underlying client of CMBI SG is an independent third party of CMBI SG, CMBI and the companies 
which are members of the same group of CMBI. To the best knowledge, information and belief of CMBI SG 
after making all reasonable enquiries, the CMBI SG Ultimate Client is Joy Dragon International Investment 
Limited, whose only ultimate beneficial owner holding 30% or more interest therein is Huang, De’An Tony. 
CMBI SG has confirmed that, to the best of their knowledge, each of the CMBI SG Ultimate Clients and its 
ultimate beneficial owner is an independent third party of CMBI SG, CMBI and the companies which are 
members of the same group of companies as CMBI.

<<<PAGE 19>>>
19
(2) 
Huatai Capital Investment Limited
Huatai Financial Holdings (Hong Kong) Limited (“HTFH”) is a non-syndicate sub-broker in connection 
with the Global Offering. Pursuant to an ISDA Agreement (the “ISDA Agreement”), HTCI, which intends 
to participate in the Global Offering as a placee, will hold the beneficial interest of the Shares on a non-
discretionary basis as the single underlying holder under a back-to-back total return swap (the “Back-to-back 
TRS”) to be entered by HTCI in connection with a Client TRS (as defined below) placed by and fully funded 
(i.e. with no financing provided by HTCI) by the Huatai Ultimate Clients (as defined below), by which, HTCI 
will, subject to customary fees and commissions, pass the full economic exposure of the Shares to the Huatai 
Ultimate Clients, which in effect, HTCI will hold the beneficial interest of the Shares on behalf of the Huatai 
Ultimate Clients. Accordingly, HTCI is considered as a “connected client” of HTFH pursuant to paragraph 13(7) 
of the Placing Guidelines.
The offshore investors (the “Huatai Ultimate Clients”) will place a total return swap order (the “Client TRS”) 
with HTCI in connection with the Company’s IPO. In order to hedge its exposure under the Client TRS, HTCI 
participates in the Company’s IPO and subscribes the Shares through placing order with HTFH during the 
International Offering.
The Huatai Ultimate Clients for purpose of this place subscription include the investment funds, details of which 
is set out below:
Name of Huatai Ultimate Client
Ultimate Beneficial Owner (“UBO”)
LU Liyang
LU Liyang
To the best of our knowledge and after making all reasonable enquiries, the Huatai Ultimate Clients is an 
independent third party of (i) the Company, the connected person or the associates thereof, and (ii) HTCI, 
HTFH and the companies which are members of the same group of HTCI.
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Back-to-back TRS in connection 
with the Client TRS order placed by the Huatai Ultimate Clients. Pursuant to the terms of the contracts of the 
Back-to-back TRS and the Client TRS, during the tenor of the Back-to-back TRS and the Client TRS, subject 
to customary fees and commissions, all economic returns of the Offer Shares will be ultimately passed to the 
Huatai Ultimate Clients through the Back-to-back TRS and the Client TRS and all economic loss shall be 
ultimately borne by the Huatai Ultimate Clients. HTCI will not take any economic return or bear any economic 
loss in relation to the Offer Shares.
The Huatai Ultimate Clients may exercise an early termination right to terminate the Client TRS at any time 
from the issue date of the Client TRS which should be on or after the date on which the Offer Shares are listed 
on the Stock Exchange at its own discretion. Upon the termination upon maturity or early termination of the 
Client TRS by the Huatai Ultimate Clients, HTCI will dispose the Offer Shares on the secondary market and 
the Huatai Ultimate Clients will receive a final settlement amount in cash in accordance with the terms and 
conditions of the Back-to-back TRS and the Client TRS which should have taken into account all the economic 
returns or economic loss in relation to the Offer Shares. If upon the maturity of the Client TRS, the Huatai 
Ultimate Clients intend to extend the investment period, subject to further agreement between HTCI and the 
relevant Huatai Ultimate Clients, the term of the Client TRS could be extended by way of a new issuance or a 
tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass 
through the economic exposure to the Huatai Ultimate Clients, each being an onshore client who places a Client 
TRS order with HTCI in connection with the IPO of the Company. HTCI will not exercise the voting right of 
the Offer Shares during the tenor of the Back-to-back TRS and the Client TRS.
During the life of the Client TRS and Back-to-back TRS, HTCI may continue to hold the Offer Shares in its 
custodian account, or to hold some or all of the Offer Shares in a prime brokerage account for stock borrowing 
purposes, where HTCI will lend out its holding of underlying Offer Shares in the form of stock borrowing loans 
consistent with market practice to lower its finance costs, provided that HTCI has the ability to call back the 
Offer Shares on loan at any time in order to satisfy its obligations under the Back-to-back TRS and Client TRS 
to ensure the economic interests are ultimately passed to the Huatai Ultimate Clients.

<<<PAGE 20>>>
20
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and trading fee payable.
The Directors and the Sponsor-Overall Coordinator confirm that at least 50% of the total number 
of the Offer Shares have been allocated to and taken up by independent price setting investors in 
compliance with Rule 18C.08 of the Listing Rules.
The Directors further confirm that at least 20% of the issued share capital of the Company will be 
held by sophisticated independent investors at the time of Listing in compliance with Chapter 2.5 
of the Guide for New Listing Applicants.
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

<<<PAGE 21>>>
21
This announcement is for information purposes only and does not constitute an invitation or offer 
to acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated June 22, 2026 issued by Zhejiang Laifual Drive Co., 
Ltd. for detailed information about the Global Offering described below before deciding whether 
or not to invest in the Shares thereby being offered.
Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinator 
(for itself and on behalf of the Hong Kong Underwriter) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the 
occurrence of any of the events set out in the paragraph headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Hong Kong Underwriting 
Agreement — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong 
Kong time) on the Listing Date (which is currently expected to be on Tuesday, June 30, 2026).
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering and the conversion of Unlisted 
Shares into H Shares, an aggregate of 74,009,912 H Shares, representing approximately 71.57% 
of the total issued share capital of the Company will be held in the public hands for the purpose of 
Rule 8.08 (as amended by Rule 19A.13A) of the Listing Rules, which is higher than the minimum 
prescribed public float percentage of H Shares required under Rule 19A.13A(1). The minimum 
prescribed public float percentage shall be 16.96% with the expected market value at the time of 
listing over HK$6,000,000,000 but not exceeding HK$30,000,000,000 under the Rule 8.08(1) (as 
amended by Rule 19A.13A), calculated based on the final Offer Price of HK$85.50 per H Share, 
thereby satisfying the minimum public float requirement under Rule 19A.13A(1) of the Listing 
Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, Shares held by the Cornerstone Investors upon the Listing shall not be 
counted towards the free float of the Shares of the Company at the time of Listing. Based on the 
final Offer Price of HK$85.50 per H Share, a market value of approximately HK$718.4 million of 
H Shares for which Listing is sought by the Company that are held by the public and not subject 
to any disposal restrictions at the time of Listing. Therefore, the Company satisfies the free float 
requirement under Rule 19A.13C(1) of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering, (i) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of 
the Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder immediately after the Global Offering; (iii) the three largest public Shareholders 
do not hold more than 50% of the Shares held in the public hands at the time of the Listing in 
compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 
Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.

<<<PAGE 22>>>
22
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, June 30, 
2026 (Hong Kong time), provided that the Global Offering has become unconditional and the right 
of termination described in the paragraph headed “Underwriting — Underwriting Arrangements 
and Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus has 
not been exercised. Investors who trade the H Shares on the basis of publicly available allocation 
details prior to the receipt of H Share certificates or prior to the H Share certificates becoming 
valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. Tuesday, June 30, 
2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange will 
commence at 9:00 a.m. on, June 30, 2026 (Hong Kong time). The H Shares will be traded in board 
lots of 100 H Shares each, and the stock code of the H Shares will be 3952.
By order of our Board
Zhejiang Laifual Drive Co., Ltd.
Mr. Zhang Jie
Chairman of the Board and Executive Director
Hong Kong, June 29, 2026
As of the date of this announcement, the Board comprises: (i) Mr. Zhang Jie, Mr. Wu Di, Ms. 
Wang Haiying and Mr. Zhang Han as executive Directors; (ii) Mr. Cui Zhiyuan, Mr. Huang He and 
Mr. Li Chengsheng as non-executive Directors; and (iii) Mr. Feng Yun, Dr. Li Jun, Mr. Lou Yu 
and Ms. Tian Chunshan as independent non-executive Directors.
