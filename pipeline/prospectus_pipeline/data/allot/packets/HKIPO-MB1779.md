# 配发结果公告抽取任务：1779.HK LongBio Pharma (Suzhou) Co., Ltd. - B - H Shares

- 公告：Announcement of Allotment Results
- 刊发时间（港交所元数据）：**04/06/2026 22:24**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0604/2026060402923.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"1779.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia) or any other 
jurisdiction where such distribution is prohibited by law. This announcement does not constitute or form a part of any 
offer to sell or solicitation of an offer to buy, to purchase or subscribe for securities nor shall there be any sale of Offer 
Shares in the United States or in any other jurisdictions in which such offer or solicitation would be unlawful. The 
securities mentioned herein have not been, and will not be, registered under the United States Securities Act of 1933 as 
amended from time to time (the “U.S. Securities Act”) or any state securities law of the United States. The securities 
may not be offered, sold, pledged, or transferred within the United States or to, or for the account or benefit of U.S. 
persons (as defined in Regulation S under the U.S. Securities Act (“Regulation S”)) except pursuant to an exemption 
from, or in a transaction not subject to, the registration requirements of the U.S. Securities Act and in compliance 
with any applicable state securities laws. There will be no public offering of securities in the United States. The Offer 
Shares are being offered and sold outside the United States in offshore transactions in reliance on Regulation S under 
the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities of the Company. This announcement is not a prospectus. Potential investors should read the 
prospectus dated May 28, 2026 (the “Prospectus”) of LongBio Pharma (Suzhou) Co., Ltd. (天辰生物醫藥(蘇州)股
份有限公司) (the “Company”) carefully for detailed information about the Company and the Global Offering before 
deciding whether or not to invest in the Offer Shares. Any investment decision in relation to the Global Offering 
should be taken solely in reliance on the information in the Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
In connection with the Global Offering, Sinolink Securities (Hong Kong) Company Limited, as the stabilizing manager 
(the “Stabilizing Manager”), its affiliates or any person acting for it, may, to the extent permitted by applicable laws 
of Hong Kong or elsewhere, over-allocate or effect transactions with a view to stabilizing or maintaining the market 
price of the Shares at a level higher than that which might otherwise prevail for a limited period after the Listing 
Date. However, there is no obligation on the Stabilizing Manager (its affiliates or any person acting for it) to conduct 
any such stabilizing action. Such stabilizing action, if taken, (a) will be conducted at the absolute discretion of the 
Stabilizing Manager (its affiliates or any person acting for it) and in what the Stabilizing Manager reasonably regards 
as the best interest of the Company, (b) may be discontinued at any time and (c) is required to be brought to an end 
within 30 days of the last day for lodging applications under the Hong Kong Public Offering. Such stabilization action, 
if commenced, may be effected in all jurisdictions where it is permissible to do so, in each case in compliance with 
all applicable laws, rules and regulatory requirements, including the Securities and Futures (Price Stabilizing) Rules 
(Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities and Futures Ordinance (Chapter 
571 of the Laws of Hong Kong).
Potential investors should be aware that stabilizing action cannot be taken to support the price of the Shares for longer 
than the stabilization period which begins on the Listing Date, and is expected to expire on Thursday, July 2, 2026, 
the 30th day after the last day for the lodging of applications under the Hong Kong Public Offering. After this date, no 
further stabilizing action may be taken, demand for the Shares, and therefore the price of the Shares, could fall.
Potential investors of the Offer Shares should note that the Sole Sponsor-Overall Coordinator (for itself and on behalf 
of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting 
Agreement upon the occurrence of any of the events set out in the paragraph headed “Underwriting — Underwriting 
Arrangements — Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior to 8:00 
a.m. (Hong Kong time) on the Listing Date (which is currently expected to be Friday, June 5, 2026).

<<<PAGE 2>>>
2
LongBio Pharma (Suzhou) Co., Ltd.
天辰生物醫藥（蘇州）股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the Global 
Offering
:
14,193,150 H Shares (subject to the
 Over-allotment Option)
Number of Hong Kong Offer Shares
:
1,419,350 H Shares
Number of International Offer Shares
:
12,773,800 H Shares (subject to
 the Over-allotment Option)
Offer Price
:
HK$96.06 per H Share, plus brokerage of 
 1.0%, SFC transaction levy of 0.0027%, 
 AFRC transaction levy of 0.00015% and 
 Stock Exchange trading fee of 0.00565%
Nominal value
:
RMB1.00 per H Share
Stock Code
:
01779
Sole Sponsor, Sole Sponsor-Overall Coordinator, Overall Coordinator, Joint Global 
Coordinator, Joint Bookrunner and Joint Lead Manager
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and
Joint Lead Managers

<<<PAGE 3>>>
3
LongBio Pharma (Suzhou) Co., Ltd.
天辰生物醫藥（蘇州）股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Warning: In view of high concentration of shareholding in a small number of H 
Shareholders, Shareholders and prospective investors should be aware that the price of 
the H Shares could move substantially even with a small number of H Shares traded and 
should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
01779
Stock short name
LONGBIO-B
Dealings commencement date
June 5, 2026*
* 
see note at the end of the announcement
Price Information
Final Offer Price
HK$96.06
Offer Shares and Share Capital
Number of Offer Shares (before exercise of the 
 Over-allotment Option)
14,193,150 H Shares
Number of Offer Shares in Hong Kong Public Offering
1,419,350 H Shares
Number of Offer Shares in International Offering 
 (before exercise of the Over-allotment Option)
12,773,800 H Shares
Number of issued Shares upon Listing (before exercise of 
 the Over-allotment Option)
74,193,150 Shares
Over-allocation
Number of Offer Shares over-allocated
2,128,950 H Shares
Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases in the 
secondary market at prices that do not exceed the Offer Price or through deferred delivery or a combination of these 
means. In the event the Over-allotment Option is exercised, an announcement will be made on the Stock Exchange’s 
website.
Proceeds
Gross proceeds (Note)
HK$1,363.4 million
 Less: Estimated listing expenses payable based on Offer 
  Price
HK$108.5 million
Net proceeds
HK$1,254.9 million
Note: Gross proceeds refer to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The 
Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if 
any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus 
on a pro rata basis.

<<<PAGE 4>>>
4
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
266,377
No. of successful applications
28,057
Subscription level
4,762.58 times
Reallocation
N/A
No. of Offer Shares initially available under the Hong Kong 
 Public Offering
1,419,350 H Shares
No. of Offer Shares reallocated from the International Offering
0
Final no. of Offer Shares under the Hong Kong Public Offering
1,419,350 H Shares
% of Offer Shares under the Hong Kong Public Offering to the 
 Global Offering
10.00%
Note: For details of the final allocation of Offer Shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/IPOResult to perform a search by identification document number or www.hkeipo.hk/IPOResult 
for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
80
Subscription Level
10.94 times
No. of Offer Shares initially available under the International 
 Offering
12,773,800 H Shares
No. of Offer Shares reallocated to the Hong Kong Public Offering
0
Final no. of Offer Shares under the International Offering
12,773,800 H Shares
% of Offer Shares under the International Offering to the Global 
 Offering
90.00%
The Directors confirm that, to the best of their knowledge, information and belief, save for 
consents under paragraphs 1C(1) and 1C(2) of Appendix F1 to the Listing Rules (the “Placing 
Guidelines”) and under Chapters 2.3 and 4.15 of the Guide for New Listing Applicants (“Guide”) 
granted by the Stock Exchange to permit the Company to, among other things, allocate certain 
Offer Shares in the International Offering to certain close associates of existing Shareholders and 
certain connected clients, (i) none of the Offer Shares subscribed by the placees and the public 
have been financed directly or indirectly by the Company, any of the Directors, chief executive 
of the Company, Controlling Shareholders, substantial Shareholders, existing Shareholders of the 
Company or any of its subsidiaries or their respective close associates; and (ii) none of the placees 
and the public who have purchased the Offer Shares are accustomed to taking instructions from 
the Company, any of the Directors, chief executive of the Company, Controlling Shareholders, 
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries or their 
respective close associates in relation to the acquisition, disposal, voting or other disposition of H 
Shares registered in his/her/its name or otherwise held by him/her/it.

<<<PAGE 5>>>
5
The placees in the International Offering include the following:
Cornerstone Investors
Investor Note 1
No. of Offer 
Shares 
allocated
% of Offer 
Shares 
(assuming the 
Over-allotment 
Option is 
not exercised)
% of total 
issued share 
capital in the 
Company after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is 
not exercised)
Existing 
shareholders 
or their close 
associates
OrbiMed Genesis Master Fund, L.P. (“OrbiMed Genesis”) Note 2
969,900
6.83%
1.31%
No
The Biotech Growth Trust PLC (“BIOG”) Note 2
497,150
3.50%
0.67%
No
TruMed Health Innovation Fund LP (“TruMed Innovation Fund”) Note 3
692,650
4.88%
0.93%
Yes
TruMed Healthcare Master Fund (“TruMed Master Fund”) Note 3
285,200
2.01%
0.38%
Yes
Shanghai Gaoyi Asset Management Partnership (Limited Partnership) 
 (上海高毅資產管理合夥企業(有限合夥)) (“Shanghai Gaoyi”) and 
 Huatai Capital Investment Limited (“HTCI”) (in connection with 
 Huatai Back-to-back TRS and the Huatai Client TRS)
978,050
6.89%
1.32%
No
Wisdomshire Asset Management Co., Ltd* (上海睿郡資產管理有限公司) 
 (“Wisdomshire AM”) and HTCI (in connection with Huatai Back-to-back 
 TRS and the Huatai Client TRS)
652,000
4.59%
0.88%
No
Foresight Global Superior Choice SPC — Vision Fund 1 SP (“Vision Fund 1”) Note 4
474,650
3.34%
0.64%
No
Foresight Global Superior Choice SPC — Global Superior Choice Fund 1 SP 
 (“GSC Fund 1”) Note 4
258,900
1.82%
0.35%
No
Foresight Global Superior Choice SPC — Horizon Fund 1 SP  
 (“Horizon Fund 1”) Note 4
40,750
0.29%
0.05%
No
Foresight Global Superior Choice SPC — Horizon Next Fund SP 
 (“Horizon Next Fund”) Note 4
40,750
0.29%
0.05%
No
Fullgoal Fund Management Co., Ltd. (富國基金管理有限公司)  
 (“Fullgoal Fund”) Note 5
685,450
4.83%
0.92%
No
Fullgoal Asset Management (HK) Limited (富國資產管理(香港)有限公司) 
 (“Fullgoal HK”) Note 5
129,550
0.91%
0.17%
No
Value Partners Hong Kong Limited (“VPHKL”) Note 6
570,400
4.02%
0.77%
No
Value Partners Limited (“VPL”) Note 6
81,500
0.57%
0.11%
No
Greater Bay Area Development Fund Management Limited for and on behalf of the 
 managed account of Mega Prime Development Limited (“Mega Prime”)
407,500
2.87%
0.55%
No
FR M CONSULTING CO., LTD (“FR M”)
163,000
1.15%
0.22%
No
Yuanfeng Future Growth Private Equity Securities Investment Fund* 
 (源峰遠景成長私募證券投資基金) (“Yuanfeng Future Growth Fund”) 
 and China Galaxy International Investment Company Limited (“CGII”) 
 (in connection with the Yuanfeng OTC Swaps)
163,000
1.15%
0.22%
No
Total
7,090,400
49.96%
9.56%

<<<PAGE 6>>>
6
Notes:
(1) 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in 
the Prospectus.
(2) 
As disclosed in the Prospectus, OrbiMed Genesis is an exempted limited partnership incorporated in the 
Cayman Islands. OrbiMed Genesis GP LLC (“Genesis GP”) is the general partner of OrbiMed Genesis. 
OrbiMed Advisors LLC (“OrbiMed Advisors”) is the managing member of Genesis GP. BIOG is a publicly 
listed trust organized under the laws of England. OrbiMed Capital LLC (“OrbiMed Capital”) is the portfolio 
manager of BIOG. OrbiMed Advisors and OrbiMed Capital exercise voting and investment power through 
a management committee comprised of Carl L. Gordon, Sven H. Borho, and W. Carter Neild, all of whom 
are Independent Third Parties. The management committee has sole discretion in exercising such voting and 
investment power on behalf of OrbiMed Advisors and OrbiMed Capital.
(3) 
As disclosed in the Prospectus, TruMed Innovation Fund is a limited partnership incorporated in the Cayman 
Island. Its general partner is TruMed Health Innovation Fund GP Limited, which is wholly owned by Ms. 
Ting Wang. TruMed Master Fund is a healthcare-focused pooled investment fund managed by TruMed 
Investment Management Limited as investment manager with discretionary authority. TruMed Investment 
Management Limited is wholly owned by Ms. Ting Wang. TruMed Innovation Fund and TruMed Master 
Fund are therefore under the common control of Ms. Ting Wang. Each of TruMed Innovation Fund and 
TruMed Master Fund is a close associate of Hainan Renze Zhenji Venture Capital Fund Partnership Enterprise 
(Limited Partnership) (海南仁澤真寄創業投資基金合夥企業（有限合夥）), which holds approximately 0.30% 
of the total issued Shares immediately prior to the Global Offering. The Stock Exchange has given consent 
under paragraph 1C(2) of the Placing Guidelines to permit each of TruMed Innovation Fund and TruMed 
Master Fund to participate in the International Offering as a Cornerstone Investor. Please refer to the section 
headed “Waivers from Strict Compliance with Listing Rules and Exemption from Strict Compliance with the 
Companies (Winding Up and Miscellaneous Provisions) Ordinance” in the Prospectus and “Others/Additional 
Information” in this announcement for details.
(4) 
As disclosed in the Prospectus, Vision Fund 1, GSC Fund 1, Horizon Fund 1 and Horizon Next Fund are all 
sub funds of Foresight Global Superior Choice SPC.
(5) 
As disclosed in the Prospectus, Fullgoal HK is a wholly owned subsidiary of Fullgoal Fund.
(6) 
As disclosed in the Prospectus, VPHKL and VPL are wholly-owned subsidiaries of Value Partners Group 
Limited, a company listed on the Stock Exchange (stock code: 806). Each of VPHKL and VPL is a connected 
client of GF Securities (Hong Kong) Brokerage Limited. The Stock Exchange has given consent under 
paragraph 1C(1) of the Placing Guidelines in relation to the allocation of Offer Shares to each of VPHKL 
and VPL as Cornerstone Investors. Please refer to the section headed “Waivers from Strict Compliance with 
Listing Rules and Exemption from Strict Compliance with the Companies (Winding Up and Miscellaneous 
Provisions) Ordinance” in the Prospectus and “Others/Additional Information” in this announcement for 
details.

<<<PAGE 7>>>
7
Allottees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares
(assuming the 
Over-allotment 
Option is 
not exercised)
% of total issued 
share capital in 
the Company 
after the 
Global Offering 
(assuming the 
Over-allotment 
Option is 
not exercised)
Relationship
Allottees with consent under paragraph 1C(2) of the Placing Guidelines under Chapters 2.3 and 4.15 of the Guide in relation to allocation of Offer 
Shares to close associates of existing Shareholders Note 1
TruMed Innovation Fund
692,650
4.88%
0.93%
A close associate of an 
existing Shareholder
TruMed Master Fund
285,200
2.01%
0.38%
A close associate of an 
existing Shareholder
O F CAPITAL TECH LPF (“OFC Tech”)
16,100
0.11%
0.02%
A close associate of an 
existing Shareholder
Changshu Kunsheng Equity Investment Fund Partnership Enterprise 
 (Limited Partnership) (常熟昆晟股權投資基金合夥企業
 (有限合夥)) (“Changshu Kunsheng”) Note 2
806,850
5.68%
1.09%
A close associate of an 
existing Shareholder
Changshu Guofa Venture Capital Co., Ltd. (常熟市國發創業投資
 有限公司) (“Changshu Guofa”) Note 2
403,400
2.84%
0.54%
A close associate of an 
existing Shareholder
Allottees with consents under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide in relation to allocations to connected clients Note 3
VPHKL
570,400
4.02%
0.77%
A connected client
VPL
81,500
0.57%
0.11%
A connected client
GF International Investment Management Limited 
 (“GF International Investment”) Note 4
806,850
5.68%
1.09%
A connected client
E Fund Management Co., Ltd. (“E Fund”) Note 5
57,450
0.40%
0.08%
A connected client
E Fund Management (Hong Kong) Co., Ltd. (“E Fund HK”) Note 5
7,100
0.05%
0.01%
A connected client
GF Securities Asset Management (Guangdong) Co., Ltd. 
 (“GF Securities AM”) Note 4
8,500
0.06%
0.01%
A connected client
Orient Asset Management (Hong Kong) Limited (“Orient AM”)
800
0.01%
0.001%
A connected client

<<<PAGE 8>>>
8
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares
(assuming the 
Over-allotment 
Option is 
not exercised)
% of total issued 
share capital in 
the Company 
after the 
Global Offering 
(assuming the 
Over-allotment 
Option is 
not exercised)
Relationship
Notes:
(1) 
The Stock Exchange has given a consent under paragraph 1C(2) of the Placing Guidelines and Chapters 
2.3 and 4.15 of Guide permit Offer Shares be placed the above placees who are close associates of existing 
Shareholders. Please refer to the section headed “Others/Additional Information” in this announcement.
(2) 
Changshu Kunsheng is a limited partnership established in the PRC, whose general partner is Changshu 
Kaisheng Southeast Entrepreneurship Investment Management Co., Ltd. (常熟開晟東南創業投資管理有限公
司) (“Changshu Kaisheng”) with 1% partnership interest therein. Changshu Guofa is a company established 
in the PRC with limited liability. Changshu Kaisheng and Changshu Guofa are all indirectly wholly-owned 
by the Bureau of Finance of Changshu (Changshu Municipal Government State-owned Assets Supervision 
and Administration Office) (常熟市財政局(常熟市政府國有資產監督管理辦公室)) (“Changshu SASAO”). 
Changshu Kunsheng and Changshu Guofa subscribed for the H Shares through certain Qualified Domestic 
Institutional Investors.
(3) 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide in 
relation to allocations to connected clients, please refer to the section headed “Others/Additional Information” 
in this announcement.
(4) 
GF International Investment is an indirect non-wholly owned subsidiary of GF Securities Co., Ltd. (廣發証
券股份有限公司) (“GF Securities”), a company listed on the Shezhen Stock Exchange (stock code: 000776.
SZ). GF Securities AM is a direct wholly-owned subsidiary of GF Securities. Please refer to the section 
headed “Others/Additional Information” in this announcement for details.
(5) 
E Fund HK is a wholly-owned subsidiary of E Fund. Please refer to the section headed “Others/Additional 
Information” in this announcement for details.

<<<PAGE 9>>>
9
LOCK-UP UNDERTAKINGS
Cornerstone Investors
Name
Number of Shares 
held in the Company 
subject to lock-up 
undertakings 
upon Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
% of total issued 
share capital in the 
Company subject to 
lock-up undertakings 
upon Listing 
(assuming the Over-
allotment Option is 
not exercised)
Last day subject 
to the lock-up 
undertakings Note 1
OrbiMed Genesis
969,900 H Shares
1.33%
1.31%
December 4, 2026
BIOG
497,150 H Shares
0.68%
0.67%
December 4, 2026
TruMed Innovation Fund
692,650 H Shares
0.95%
0.93%
December 4, 2026
TruMed Master Fund
285,200 H Shares
0.39%
0.38%
December 4, 2026
Shanghai Gaoyi and HTCI (in connection with Huatai 
 Back-to-back TRS and the Huatai Client TRS)
978,050 H Shares
1.34%
1.32%
December 4, 2026
Wisdomshire AM and HTCI (in connection with 
 Huatai Back-to-back TRS and the Huatai 
 Client TRS)
652,000 H Shares
0.89%
0.88%
December 4, 2026
Vision Fund 1
474,650 H Shares
0.65%
0.64%
December 4, 2026
GSC Fund 1
258,900 H Shares
0.35%
0.35%
December 4, 2026
Horizon Fund 1
40,750 H Shares
0.06%
0.05%
December 4, 2026
Horizon Next Fund
40,750 H Shares
0.06%
0.05%
December 4, 2026
Fullgoal Fund
685,450 H Shares
0.94%
0.92%
December 4, 2026
Fullgoal HK
129,550 H Shares
0.18%
0.17%
December 4, 2026
VPHKL
570,400 H Shares
0.78%
0.77%
December 4, 2026
VPL
81,500 H Shares
0.11%
0.11%
December 4, 2026
Mega Prime
407,500 H Shares
0.56%
0.55%
December 4, 2026
FR M
163,000 H Shares
0.22%
0.22%
December 4, 2026
Yuanfeng Future Growth Fund and CGII 
 (in connection with the Yuanfeng OTC Swaps)
163,000 H Shares
0.22%
0.22%
December 4, 2026
Subtotal
7,090,400 H Shares
9.72%
9.56%
Note:
(1) 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on December 
4, 2026, being six months following the Listing Date. The Cornerstone Investors will cease to be prohibited 
from disposing of or transferring H Shares subscribed for pursuant to the relevant cornerstone investment 
agreements after the indicated date.

<<<PAGE 10>>>
10
Controlling Shareholders
Name
Number of 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
% of total issued 
share capital in 
the Company 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings Note 1
Liu Heng (劉恒)
8,447,692 H Shares
11.58%
11.39%
June 4, 2027
Sun Bill Nai-chau  
(孫乃超)
6,668,921 H Shares
9.14%
8.99%
June 4, 2027
Suzhou Taiwu Enterprise 
Management Partnership 
(Limited Partnership)  
(蘇州泰悟企業管理合夥
企業(有限合夥))
4,899,364 H Shares
6.72%
6.60%
June 4, 2027
Sun Cecily Rou-yun  
(周若芸)
3,643,748 H Shares
5.00%
4.91%
June 4, 2027
Shanghai Rising Suns 
Biomedical Inc. (上海 
九日生物醫藥有限公司)
2,154,243 H Shares
2.95%
2.90%
June 4, 2027
PharMab, Inc. (旭華 
(上海)生物研發中心 
有限公司)
683,191 H Shares
0.94%
0.92%
June 4, 2027
Total
26,497,159 H Shares
36.33%
35.71%
Note:
(1) 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law. The 
required lock-up for the Controlling Shareholders ends on June 4, 2027, being twelve months following 
the Listing Date. Pursuant to Rule 10.07 of the Listing Rules, each of the Controlling Shareholders has 
undertaken to the Stock Exchange and the Company that, he, she or it shall comply with the applicable lock-
up requirements. For further details, please refer to the section headed “Underwriting – Undertakings to 
the Stock Exchange Pursuant to the Listing Rules – Undertakings by our Controlling Shareholders” in the 
Prospectus.

<<<PAGE 11>>>
11
Other Existing Shareholders (including the Pre-IPO Investors as defined in the “History, 
Development and Corporate Structure” section of the Prospectus)
Name
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
Number of H Shares 
held in the Company 
as a % of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
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
Last day subject 
to the lock-up 
undertakings 
Note 1 and Note 2
Huzhou Youxing Venture Capital 
 Partnership Enterprise (Limited 
 Partnership) (湖州友星創業投
 資合夥企業(有限合夥)) 
 (“Huzhou Youxing”) Note 3
7,021,810 H Shares
9.63%
9.46%
June 4, 2027
Suzhou Youxin Venture Capital 
 Partnership Enterprise (Limited 
 Partnership) (蘇州友信創業投資
 合夥企業(有限合夥) 
 (“Suzhou Youxin”) Note 3
3,203,667 H Shares
4.39%
4.32%
June 4, 2027
Suzhou Lianrui Venture Capital 
 Partnership Enterprise (Limited 
 Partnership) (蘇州連銳創業投資
 合夥企業(有限合夥)) 
 (“Suzhou Lianrui”) Note 3
1,641,884 H Shares
2.25%
2.21%
June 4, 2027
Huzhou Youcheng Venture Capital 
 Partnership Enterprise (Limited 
 Partnership (湖州友成創業投資
 合夥企業(有限合夥)) 
 (“Huzhou Youcheng”) Note 3
866,867 H Shares
1.19%
1.17%
June 4, 2027
Fuhai Ancheng Bohui (Bozhou) 
 Healthcare Equity Investment 
 Fund Partnership Enterprise 
 (Limited Partnership) (富海安誠博
 暉(亳州)醫療股權投資基金
 合夥企業(有限合夥)) 
 (“OFC Bohui Fund”) Note 4
3,077,490 H Shares
4.22%
4.15%
June 4, 2027
China SME Development Fund 
 (Chengdu) Jiaozi Venture Capital 
 Investment Partnership Enterprise 
 (Limited Partnership) (中小企業
 發展基金(成都)交子創業投資
 合夥企業(有限合夥)) 
 (“OFC Jiaozi Fund”) Note 4
1,171,447 H Shares
1.61%
1.58%
June 4, 2027
Huzhou Yongshi Huijin Venture 
 Capital Partnership Enterprise 
 (Limited Partnership) (湖州永石
 匯金創業投資合夥企業(有限合夥)) 
 (“Yongshi Huijin”) Note 5
1,025,832 (including 
512,916 H Shares)
0.70%
1.38%
June 4, 2027

<<<PAGE 12>>>
12
Name
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
Number of H Shares 
held in the Company 
as a % of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
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
Last day subject 
to the lock-up 
undertakings 
Note 1 and Note 2
Huzhou Yongshi Weizhen Venture 
 Capital Investment Partnership 
 Enterprise (Limited Partnership) 
 (湖州永石唯真創業投資合夥企業
 (有限合夥) 
 (“Yongshi Weizhen”) Note 5
1,499,932 (including 
749,966 H Shares) 
1.03% 
2.02% 
June 4, 2027
HLC VGC Partners HK II Limited 
 (“HLC”) Note 6
1,290,964 H Shares
1.77%
1.74%
June 4, 2027
Qingdao Hongyi Investment 
 Partnership (Limited Partnership) 
 (青島弘熠投資合夥企業(有限
 合夥)) (“Qingdao Hongyi”) Note 6
1,099,710 H Shares
1.51%
1.48%
June 4, 2027
QM282 Limited
1,921,283 H Shares
2.63%
2.59%
June 4, 2027
Qingdao CSPC Sangel New Drug 
 Investment Partnership Enterprise 
 (Limited Partnership) (青島石藥仙
 瞳新藥投資合夥企業(有限合夥))
1,538,745 H Shares
2.11%
2.07%
June 4, 2027
Shanghai Lingang Pioneer Innovation 
 Private Equity Investment Fund 
 Partnership L.P. (上海臨港
 啟創生科私募投資基金
 合夥企業(有限合夥))
1,045,922 H Shares
1.43%
1.41%
June 4, 2027
Changshu Southeast Industrial 
 Investment Co., Ltd. (常熟東南
 產業投資有限公司) 
 (“Southeast Investment”) Note 7
1,025,832 H Shares
1.41%
1.38%
June 4, 2027
Changshu Wuyue Angel Venture 
 Capital Partnership Enterprise 
 (Limited Partnership) (常熟吳越
 天使創業投資合夥企業(有限合夥)) 
 (“Changshu Wuyue Angel”) Note 7
390,484 H Shares
0.54%
0.53%
June 4, 2027
Shanxi Securities Alternative Investment 
 Ltd (山證創新投資有限公司)
954,287 H Shares
1.31%
1.29%
June 4, 2027
Anhui Anyuan Modern Health 
 Industry Investment Center 
 (Limited Partnership) (安徽安元現
 代健康產業投資中心(有限合夥))
820,662 H Shares
1.13%
1.11%
June 4, 2027

<<<PAGE 13>>>
13
Name
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
Number of H Shares 
held in the Company 
as a % of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
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
Last day subject 
to the lock-up 
undertakings 
Note 1 and Note 2
Hangzhou Beicheng Venture Capital 
 Partnership (Limited Partnership 
 Enterprise) (杭州貝橙創業投資
 合夥企業(有限合夥))
747,085 H Shares
1.02%
1.01%
June 4, 2027
Changshu Sanyi No. 1 Venture Capital 
 Partnership Enterprise (Limited 
 Partnership) (常熟三奕壹號創業
 投資合夥企業(有限合夥))
727,654 H Shares
1.00%
0.98%
June 4, 2027
Hangzhou Qiming Rongjing Equity 
 Investment Partnership Enterprise 
 (Limited Partnership) (杭州啟明
 融晶股權投資合夥企業(有限合夥)) 
 (“Qiming Rongjing”) Note 8
384,255 H Shares
0.53%
0.52%
June 4, 2027
Suzhou Qiming Rongqian Equity 
 Investment Partnership (Limited 
 Partnership Enterprise) (蘇州啟明
 融乾股權投資合夥企業(有限合夥)) 
 (“Qiming Rongqian”) Note 8
256,176 H Shares
0.35%
0.35%
June 4, 2027
Hefei Hongta Industrial Investment 
 Partnership (Limited Partnership) 
 (合肥弘沓產業投資合夥企業
 (有限合夥))
585,726 H Shares
0.80%
0.79%
June 4, 2027
Shenzhen Sangel Shunchuang 
 Biomedical Angel Investment 
 Partnership Enterprise (Limited 
 Partnership) (深圳仙瞳順創生物
 醫療天使投資合夥企業(有限合夥))
512,913 H Shares
0.70%
0.69%
June 4, 2027
Shenzhen Xinsheng Huachuang 
 Enterprise Management Partnership 
 (Limited Partnership) (深圳市新生
 華創企業管理合夥企業(有限合夥))
512,913 H Shares
0.70%
0.69%
June 4, 2027
Hainan Renze Zhenji Venture Capital 
 Fund Partnership Enterprise 
 (Limited Partnership) (海南仁澤真
 寄創業投資基金合夥企業
 (有限合夥))
179,301 H Shares
0.25%
0.24%
June 4, 2027
Total
33,502,841 
(including 
32,239,959 H 
Shares)
44.21%
45.16%

<<<PAGE 14>>>
14
Notes:
(1) 
Under the applicable PRC laws, all existing Shareholders (including Pre-IPO Investors) are subject to a lock-
up period of twelve months following the Listing Date.
(2) 
The numbers of Shares held by OFC Bohui Fund, OFC Jiaozi Fund, Southeast Investment, Changshu Wuyue 
Angel and Hainan Renze in the table above do not take into account the Shares to be subscribed by their 
respective close associates in the Global Offering. The Company has applied to the Stock Exchange for, and 
the Stock Exchange has given to the Company, a consent under paragraph 1C(2) of the Placing Guidelines 
permit the Company to allocate such Offer Shares in the International Offering to their respective close 
associates. For details, please refer to the sections headed “Allottees with Waivers/Consents Obtained” and 
“Others/Additional Information” in this announcement.
(3) 
As disclosed in the Prospectus, each of Huzhou Youxing, Suzhou Youxin, Suzhou Lianrui and Huzhou 
Youcheng is a limited partnership established in the PRC, and the executive partner and fund manager of 
which is Shanghai Tongrui Investment Management Company Limited.
(4) 
As disclosed in the Prospectus, OFC Bohui Fund and OFC Jiaozi Fund, both of which are limited partnerships 
established in the PRC, are venture capital investment funds whose investment and asset management 
affairs are managed and controlled by its respective fund managers, being Oriental Fortune (Wuhu) Equity 
Investment Fund Management Enterprise (Limited Partnership) (東方富海(蕪湖)股權投資基金管理企業
(有限合夥)) (“OFC Wuhu”) and Shenzhen Oriental Fortune Venture Capital Investment Management Co., 
Ltd. (深圳市東方富海創業投資管理有限公司) (“OFC VC Investment”). Each of OFC VC Investment and 
OFC Wuhu is a direct or indirect wholly owned subsidiary of Shenzhen Oriental Fortune Capital Investment 
Management Co., Ltd. (深圳市東方富海投資管理股份有限公司) (“Oriental Fortune Capital”). OFC Wuhu 
is owned by Oriental Fortune Capital and OFC VC Investment as to 95% and 5%, respectively, and OFC VC 
Investment is in turn wholly owned by Oriental Fortune Capital.
(5) 
As disclosed in the Prospectus, each of Yongshi Huijin and Yongshi Weizhen is limited partnership 
established in the PRC, and the executive partner and fund manager of which is Huzhou Yongshi Equity 
Investment Management Co., Ltd. (湖州永石股權投資管理有限公司).
(6) 
As disclosed in the Prospectus, HLC is a company incorporated in Hong Kong with limited liability, and it 
is wholly owned by HLC VGC Fund IV L.P.. HLC VGC Fund IV L.P. is an exempted limited partnership 
established under the laws of the Cayman Islands and is ultimately managed by its general partner HLC VGC 
GP IV Limited, and in turn ultimately controlled by Mr. WANG Hui (王暉). Qingdao Hongyi is a limited 
partnership established in the PRC and managed by its executive partner, Shanghai Hehong Jinghui Equity 
Investment Management Co., Ltd. (上海合弘景暉股權投資管理有限公司) (“Shanghai Hehong Jinghui”). 
Shanghai Hehong Jinghui is also ultimately controlled by Mr. WANG Hui (王暉) and is owned as to 72% by 
him.
(7) 
As disclosed in the Prospectus, Southeast Investment is a company established in the PRC with limited 
liability. It is owned by Changshu Southeast Investment Holding Co., Ltd. (常熟市東南投資控股有限公司) 
as to 99.96%, which is in turn indirectly wholly owned by Changshu SASAO. Changshu Wuyue Angel is a 
limited partnership established in the PRC. Among the limited partners of Changshu Wuyue Angel, Changshu 
Investment Holdings Group Co., Ltd. (常熟市投資控股集團有限公司) holds approximately 52.89% of the 
partnership interests. Changshu Investment Holdings Group Co., Ltd. is wholly owned by Changshu State-
owned Capital Investment and Operation Group Co., Ltd. (常熟市國有資本投資運營集團有限公司) which is 
in turn wholly owned by Changshu SASAO. The executive partner of Changshu Wuyue Angel is Changshu 
Qixin Venture Capital Partnership (Limited Partnership) (常熟啟新創業投資合夥企業(有限合夥)), which 
is owned as to 35% by Changshu Guofa as its executive partner and as to 35% by SIP Oriza Seed Fund 
Management Co., LTD. (蘇州工業園區元禾原點創業投資管理有限公司). Changshu Guofa is indirectly 
wholly-owned by the Changshu SASAO.
(8) 
As disclosed in the Prospectus, Qiming Rongjing and Qiming Rongqian are limited partnerships established 
in the PRC, with their general partner being Suzhou Qikun Venture Capital Partnership (Limited Partnership) 
(蘇州啟坤創業投資合夥企業(有限合夥)).

<<<PAGE 15>>>
15
PLACEE CONCENTRATION ANALYSIS
Placees
* Number of H
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
Option is 
exercised and 
new H Shares 
are issued)
Allotment as % 
of total Offer 
Shares 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment as % 
of total Offer 
Shares 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares 
are issued)
Number of
H Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
% of total 
issued share 
capital upon 
Listing 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares 
are issued)
Top 1
1,467,050
11.5%
9.8%
10.3%
9.0%
1,467,050
2.0%
1.9%
Top 5
5,513,100
43.2%
37.0%
38.8%
33.8%
6,929,416
9.3%
9.1%
Top 10
9,144,850
71.6%
61.4%
64.4%
56.0%
10,561,166
14.2%
13.8%
Top 25
13,735,500
107.5%
92.2%
96.8%
84.2%
15,151,816
20.4%
19.9%
Note:
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholders
* Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering 
(assuming no 
exercise of 
the Over-
allotment 
Option)
Allotment 
as % of 
International 
Offering 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares 
are issued)
Allotment as 
% of total 
Offer Shares 
(assuming no 
exercise of 
the Over-
allotment 
Option)
Allotment as 
% of total 
Offer Shares 
(assuming 
the Over-
allotment 
Option is 
exercised and 
new H 
Shares are 
issued)
Number of
H Shares 
held upon 
Listing
% of total 
number 
of issued 
H Shares 
upon Listing 
(assuming 
no exercise 
of the Over-
allotment 
Option)
% of total 
number of 
issued 
H Shares 
upon Listing 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares 
are issued)
Number 
of Shares 
held upon 
Listing
Top 1
–
0.0%
0.0%
0.0%
0.0%
26,497,159
36.3%
35.3%
26,497,159
Top 5
1,226,350
9.6%
8.2%
8.6%
7.5%
48,513,664
66.5%
64.6%
48,513,664
Top 10
3,671,250
28.7%
24.6%
25.9%
22.5%
55,860,775
76.6%
74.4%
57,123,657
Top 25
9,812,850
76.8%
65.8%
69.1%
60.1%
67,524,142
92.6%
90.0%
68,787,024
Note:
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 16>>>
16
SHAREHOLDER CONCENTRATION ANALYSIS
All Shareholders
* Number of 
H Shares 
allotted
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
Option is 
exercised and 
new H Shares 
are issued)
Allotment as 
% of total 
Offer Shares 
(assuming no 
exercise of the 
Over-allotment 
Option)
Allotment as % 
of total Offer 
Shares (assuming 
the Over-
allotment Option 
is exercised and 
new H Shares 
are issued)
Number of
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
% of total 
issued share 
capital upon 
Listing 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares 
are issued)
Top 1
–
0.0%
0.0%
0.0%
0.0%
26,497,159
35.7%
34.7%
Top 5
1,226,350
9.6%
8.2%
8.6%
7.5%
48,513,664
65.4%
63.6%
Top 10
3,671,250
28.7%
24.6%
25.9%
22.5%
57,123,657
77.0%
74.8%
Top 25
9,812,850
76.8%
65.8%
69.1%
60.1%
68,787,024
92.7%
90.1%
Note:
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon 
Listing.

<<<PAGE 17>>>
17
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
Pool A
Number 
of H Shares 
applied for
Number 
of valid 
applications
Basis of allocation/ballot
Approximate 
percentage  
allotted of the  
total number  
of H Shares  
applied for
50
51,154
1,024 out of 51,154 applicants to receive 50 H Shares
2.00%
100
27,227
679 out of 27,227 applicants to receive 50 H Shares
1.25%
150
5,797
165 out of 5,797 applicants to receive 50 H Shares
0.95%
200
5,425
169 out of 5,425 applicants to receive 50 H Shares
0.78%
250
4,451
149 out of 4,451 applicants to receive 50 H Shares
0.67%
300
3,614
128 out of 3,614 applicants to receive 50 H Shares
0.59%
350
2,817
105 out of 2,817 applicants to receive 50 H Shares
0.53%
400
2,587
100 out of 2,587 applicants to receive 50 H Shares
0.48%
450
1,718
69 out of 1,718 applicants to receive 50 H Shares
0.45%
500
17,860
741 out of 17,860 applicants to receive 50 H Shares
0.41%
600
2,605
115 out of 2,605 applicants to receive 50 H Shares
0.37%
700
2,131
99 out of 2,131 applicants to receive 50 H Shares
0.33%
800
2,255
109 out of 2,255 applicants to receive 50 H Shares
0.30%
900
2,417
121 out of 2,417 applicants to receive 50 H Shares
0.28%
1,000
12,501
647 out of 12,501 applicants to receive 50 H Shares
0.26%
1,500
5,728
337 out of 5,728 applicants to receive 50 H Shares
0.20%
2,000
5,249
338 out of 5,249 applicants to receive 50 H Shares
0.16%
2,500
3,749
259 out of 3,749 applicants to receive 50 H Shares
0.14%
3,000
3,635
267 out of 3,635 applicants to receive 50 H Shares
0.12%
3,500
2,555
197 out of 2,555 applicants to receive 50 H Shares
0.11%
4,000
2,555
205 out of 2,555 applicants to receive 50 H Shares
0.10%
4,500
2,094
175 out of 2,094 applicants to receive 50 H Shares
0.09%
5,000
4,918
424 out of 4,918 applicants to receive 50 H Shares
0.09%
6,000
3,647
333 out of 3,647 applicants to receive 50 H Shares
0.08%
7,000
2,614
251 out of 2,614 applicants to receive 50 H Shares
0.07%
8,000
2,314
232 out of 2,314 applicants to receive 50 H Shares
0.06%
9,000
2,165
225 out of 2,165 applicants to receive 50 H Shares
0.06%
10,000
14,544
1,559 out of 14,544 applicants to receive 50 H Shares
0.05%
20,000
9,347
1,249 out of 9,347 applicants to receive 50 H Shares
0.03%
30,000
7,263
1,103 out of 7,263 applicants to receive 50 H Shares
0.03%
40,000
5,370
894 out of 5,370 applicants to receive 50 H Shares
0.02%
50,000
9,667
1,726 out of 9,667 applicants to receive 50 H Shares
0.02%
Total
231,973
Total number of Pool A successful applicants: 14,194

<<<PAGE 18>>>
18
Pool B
Number 
of H Shares 
applied for
Number 
of valid 
applications
Basis of allocation/ballot
Approximate 
percentage  
allotted of the  
total number  
of H Shares  
applied for
60,000
8,776
2,107 out of 8,776 applicants to receive 50 H Shares
0.02%
70,000
3,101
824 out of 3,101 applicants to receive 50 H Shares
0.02%
80,000
2,312
671 out of 2,312 applicants to receive 50 H Shares
0.02%
90,000
1,923
603 out of 1,923 applicants to receive 50 H Shares
0.02%
100,000
8,879
2,980 out of 8,879 applicants to receive 50 H Shares
0.02%
200,000
4,254
2,249 out of 4,254 applicants to receive 50 H Shares
0.01%
300,000
1,758
1,213 out of 1,758 applicants to receive 50 H Shares
0.01%
400,000
976
813 out of 976 applicants to receive 50 H Shares
0.01%
500,000
630
608 out of 630 applicants to receive 50 H Shares
0.01%
600,000
429
50 H Shares plus 38 out of 429 applicants to  
 receive an additional 50 H Shares
0.01%
709,650
1,366
50 H Shares plus 292 out of 1,366 applicants to  
 receive an additional 50 H Shares
0.01%
Total
34,404
Total number of Pool B successful applicants: 13,863
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the Offer Price in addition to any brokerage, AFRC transaction 
levy, SFC transaction levy and Stock Exchange trading fee payable.

<<<PAGE 19>>>
19
OTHERS/ADDITIONAL INFORMATION
Allocation of Offer Shares to Certain Existing Shareholders and/or Their Close Associates
As Cornerstone Investors
The Company has sought, and the Stock Exchange has given, a consent under paragraph 1C(2) of 
the Placing Guidelines to permit TruMed Master Fund and TruMed Innovation Fund (collectively, 
the “TruMed Funds”) to participate in the Global Offering as Cornerstone Investors on the 
following basis as set out in Paragraph 18 of Chapter 2.3 and Chapter 4.15 of the Guide, subject to 
the conditions as follows:
(a) 
the Company will comply with the public float requirement under Rule 19A.13A and the free 
float requirement under Rule 19A.13C of the Listing Rules;
(b) 
the Offer Shares to be subscribed by and allocated to TruMed Master Fund and TruMed 
Innovation Fund (each a close associate of an existing Shareholder) as cornerstone investors 
under the Global Offering will be at the Offer Price and on substantially the same terms as 
other cornerstone investors (including being subject to a six-month lock up arrangement 
following the Listing), and TruMed Funds will pay and settle in full for the Offer Shares 
before dealings commence on the Listing Date;
(c) 
the Company, the Sole Sponsor and the Overall Coordinators confirm that no preferential 
treatment has been, nor will be, given to each of TruMed Funds as a cornerstone investor by 
virtue of its relationship with the Company in any allocation in the Global Offering, other 
than the preferential treatment of assured entitlement under the cornerstone investment with 
TruMed Funds which follows the principles set out in Chapters 2.3 and 4.15 of the Guide, 
and that the terms of the cornerstone investment agreement of TruMed Funds are substantially 
the same as the other cornerstone investment agreements;
(d) 
each of the Company, the Sole Sponsor and the Overall Coordinators has provided the Stock 
Exchange with written confirmations in accordance with Chapters 2.3 and 4.15 of the Guide; 
and
(e) 
details of the allocation of the Offer Shares to each of TruMed Funds as a cornerstone 
investor in the Global Offering have been disclosed in the allotment results announcement of 
the Company.
Such allocations of Offer Shares to the close associates of an existing Shareholder are in 
compliance with all the conditions under the consent given by the Stock Exchange.

<<<PAGE 20>>>
20
As Placees
The Company has applied, and the Stock Exchange has given, a consent under paragraph 1C(2) of 
the Placing Guidelines to permit certain close associates of existing Shareholders to participate in 
the Global Offering as placees on the following basis as set out in Paragraph 18 of Chapter 2.3 and 
Chapter 4.15 of the Guide, subject to the following conditions:
(a) 
None of the Permitted Participants, together with the involved existing Shareholder, is, and 
will be, a core connected person of the Company, the allocation to the Permitted Participants 
will not affect the Company’s ability to satisfy the public float requirement under Rule 
19A.13A of the Listing Rules and the free float requirement under Rule 19A.13C of the 
Listing Rules;
(b) 
each of the Sole Sponsor and the Overall Coordinators confirms that no preferential treatment 
in allocation has been, nor will be, given to each of OFC Tech, Changshu Kunsheng 
and Changshu Guofa by virtue of their respective relationship with the relevant existing 
Shareholders of the Company;
(c) 
the Company confirms that no preferential treatment in allocation has been, nor will be, given 
to each of OFC Tech, Changshu Kunsheng and Changshu Guofa by virtue of their respective 
relationship with the relevant existing Shareholders of the Company;
(d) 
each of the Company, the Sole Sponsor and the Overall Coordinators has provided the Stock 
Exchange with written confirmations in accordance with Chapters 2.3 and 4.15 of the Guide; 
and
(e) 
the relevant information in respect of the allocation to the Permitted Participants has been 
disclosed in the allotment results announcement.
For details of the allocations of Offer Shares to certain existing Shareholders and/or their close 
associates, please refer to the section headed “Allotment Results Details – International Offering – 
Allottees with Waivers/Consents Obtained” in this announcement.

<<<PAGE 21>>>
21
Allocation of Offer Shares to Connected Clients
As Cornerstone Investors
The Company has sought, and the Stock Exchange has given, a consent under paragraph 1C(1) 
of the Placing Guidelines to allow each of VPHKL and VPL to subscribe for Offer Shares as a 
Cornerstone Investor on the following basis as set out in Chapter 4.15 of the Guide, subject to the 
conditions as follows:
(a) 
each of VPHKL and VPL will hold H Shares allocated to it on a discretionary basis and on 
behalf of independent third parties;
(b) 
the relevant cornerstone investment agreement of each of VPHKL and VPL does not contain 
any material terms which are more favorable to it than those in other cornerstone investment 
agreements;
(c) 
no preferential treatment has been, nor will be, given to each of VPHKL and VPL by virtue 
of its relationship with GF Securities (Hong Kong) Brokerage Limited (“GF Securities (Hong 
Kong) Brokerage”) in any allocation of Offer Shares in the Global Offering (other than 
the assured entitlement under the relevant cornerstone investment agreement following the 
principles set out in Chapter 4.15 of the Guide);
(d) 
GF Securities (Hong Kong) Brokerage has not participated, and will not participate, in the 
decision-making process or relevant discussions relating to allocation of Offer Shares to 
VPHKL and VPL as cornerstone investors;
(e) 
each of VPHKL and VPL has confirmed that to the best of its knowledge and belief, it has 
not received and will not receive preferential treatment in the allocation of Offer Shares in 
the Global Offering as cornerstone investors by virtue of its relationship with GF Securities 
(Hong Kong) Brokerage (other than the assured entitlement under the relevant cornerstone 
investment agreement following the principles set out in Chapter 4.15 of the Guide);
(f) 
each of the Company, the Overall Coordinators including GF Securities (Hong Kong) 
Brokerage as one of the Overall Coordinators, VPHKL, VPL and GF Securities (Hong Kong) 
Brokerage has provided the Stock Exchange with written confirmations in accordance with 
Chapter 4.15 of the Guide; and
(g) 
details of the cornerstone investments and details of the allocations have been disclosed in 
the allotment results announcement of the Company.
Such allocations of Offer Shares to connected clients are in compliance with all the conditions 
under the consent given by the Stock Exchange.

<<<PAGE 22>>>
22
As Placees
Under the International Offering, certain Offer Shares were placed to connected clients of a 
connected distributor pursuant to the Placing Guidelines. Details of the placement to connected 
clients are set out below.
No.
Connected distributor
Connected Client
Relationship with the 
connected distributor
Basis of 
holding 
securities
Number 
of Offer 
Shares 
to be 
allocated
% of total 
Offer 
Shares in 
the Global 
Offering(1)
% of total issued 
shares capital 
immediately upon 
the completion of 
Global Offering(1)
1.
GF Securities (Hong 
Kong) Brokerage 
Limited (“GF 
Securities (Hong 
Kong) Brokerage”)
GF International Investment 
Management Limited 
(“GF International 
Investment”) (2)
GF International Investment 
is a member of the same 
group of companies as GF 
Securities (Hong Kong) 
Brokerage.
Discretionary
806,850
5.68%
1.09%
2.
E Fund Management Co., 
Ltd. (“E Fund”) (3)
E Fund is a member of the 
same group of companies 
as GF Securities (Hong 
Kong) Brokerage.
Discretionary
57,450
0.40%
0.08%
3.
E Fund Management (Hong 
Kong) Co., Ltd. (“E Fund 
HK”) (3)
E Fund HK is a member 
of the same group of 
companies as GF Securities 
(Hong Kong) Brokerage.
Discretionary
7,100
0.05%
0.01%
4.
GF Securities Asset 
Management 
(Guangdong) Co., Ltd. 
(“GF Securities AM”) (4)
GF Securities AM is a 
member of the same 
group of companies as GF 
Securities (Hong Kong) 
Brokerage.
Non-
 discretionary
8,500
0.06%
0.01%
5.
Orient Securities 
(Hong Kong) 
Limited (“Orient 
Securities”)
Orient Asset Management 
(Hong Kong) Limited 
(“Orient AM”) (5)
Orient AM is a member of 
the same group of Orient 
Securities.
Discretionary
800
0.01%
0.001%
Notes:
(1) 
Assuming the Over-allotment Option is not exercised.
(2) 
GF International Investment will hold the Offer Shares in its capacity as the discretionary fund manager managing 
the funds on behalf of their investors (the “GF International Investment Ultimate Clients”). GF International 
Investment is an indirect non-wholly owned subsidiary of GF Securities Co., Ltd. (廣發証券股份有限公司) (“GF 
Securities”), a company listed on the Shenzhen Stock Exchange (stock code: 000776.SZ) and the Stock Exchange 
(stock code: 01776.HK). GF Securities (Hong Kong) Brokerage is an indirect wholly-owned subsidiary of GF 
Securities. Accordingly, GF International Investment is a member of the same group of companies as GF Securities 
(Hong Kong) Brokerage.
GF International Investment is to invest on a discretionary basis on behalf of the GF International Investment 
Ultimate Clients which are independent third parties and no proprietary money is used for the subscribing. To the best 
knowledge of GF International Investment, each of GF International Investment Ultimate Clients is an independent 
third party of the Company, its subsidiaries, its substantial shareholders, GF International Investment, GF Securities 
(Hong Kong) Brokerage and the companies which are members of the same group of companies as GF Securities 
(Hong Kong) Brokerage. No ultimate beneficial owner holds 30% or more interest in the funds.

<<<PAGE 23>>>
23
GF International Investment is investing on behalf of certain collective investment schemes which are not authorized 
by the SFC, details of which are as follow:
Fund Name
Fund Manager
Identity of ultimate beneficial owner (“UBO”) 
holding 30% or more interest
Frontline Investment Master SPC 
– GF Luminous Fund SP
GF International 
Investment
Not applicable as there is no UBO holding 30% or 
more interest
Frontline Investment Master SPC 
– GF Vision Fund SP
GF International 
Investment
Not applicable as there is no UBO holding 30% or 
more interest
Frontline Investment Master SPC 
– GF Bonanza Fund SP
GF International 
Investment
Not applicable as there is no UBO holding 30% or 
more interest
Frontline Investment Master SPC 
– GF Curation Equity Fund SP
GF International 
Investment
Not applicable as there is no UBO holding 30% or 
more interest
Frontline Investment Master SPC 
– Golden Stone Fund SP
GF International 
Investment
Not applicable as there is no UBO holding 30% or 
more interest
Frontline Investment Master SPC 
– GF Navigation Fund SP
GF International 
Investment
Not applicable as there is no UBO holding 30% or 
more interest
In addition to the funds disclosed above, GF International Investment is also expected to hold the Offer Shares on 
behalf of one SFC authorized fund, namely GFI Global Select Equity Fund.
(3) 
Each of E Fund and E Fund HK will hold the Offer Shares in its capacity as the discretionary fund manager 
managing the sub funds on behalf of the underlying clients (the “E Fund Ultimate Clients”). GF Securities (Hong 
Kong) Brokerage is an indirect wholly-owned subsidiary of GF Securities, which in turn holds 22.65% of the issued 
share capital of E Fund. E Fund HK is a wholly-owned subsidiary of E Fund. Therefore, each of E Fund and E Fund 
HK constitutes a member of the same group with GF Securities (Hong Kong) Brokerage.
E Fund and E Fund HK are to invest on discretionary basis on behalf of the E Fund Ultimate Clients which are 
independent third parties and no proprietary money is used for the subscribing. To the best knowledge of E Fund and 
E Fund HK, (i) each of the E Fund Ultimate Clients is an independent third party of the Company, its subsidiaries, 
its substantial shareholders, E Fund, E Fund HK, GF Securities (Hong Kong) Brokerage and the companies which 
are members of the same group of companies as GF Securities (Hong Kong) Brokerage; and (ii) neither E Fund or E 
Fund HK is a collective investment scheme which is not authorised by the SFC.
Details of the E Fund Ultimate Clients are set out below:
Fund Name
Fund 
manager
Identity of ultimate beneficial owner 
(“UBO”) holding 30% or more interest
E Fund Global Asset Allocation 
 Hybrid Fund
E Fund
Not applicable as there is no UBO 
 holding 30% or more interest.
E Fund Global Healthcare Sector 
 Sponsored Hybrid Fund
E Fund
Not applicable as there is no UBO 
 holding 30% or more interest.
E Fund S&P Global Luxury 
 Enhanced Index Fund
E Fund
Not applicable as there is no UBO 
 holding 30% or more interest.
E Fund (HK) Global Allocation 
 Fund SP I
E Fund HK
Cinda Sino-Rock Investment Limited, whose 
 UBO holding 30% or more interest is China 
 Cinda Asset Management Co., Ltd. 
 (stock code: 1359.HK).
E FUND (HK) NEO 
 OPPORTUNITY SP I
E Fund HK
Not applicable as there is no UBO 
 holding 30% or more interest.
E Fund (HK) China Equity 
 Dividend Fund
E Fund HK
Not applicable as there is no UBO 
 holding 30% or more interest.

<<<PAGE 24>>>
24
(4) 
GF Securities AM is a direct wholly-owned subsidiary of GF Securities. GF Securities (Hong Kong) 
Brokerage is an indirect wholly-owned subsidiary of GF Securities. Accordingly, GF Securities AM is a 
member of the same group of companies as GF Securities (Hong Kong) Brokerage.
Each of the ultimate clients of GF Securities AM (the “GF Securities AM Ultimate Clients”) has engaged 
GF Securities AM, an asset manager that is qualified domestic institutional investor as approved by the 
relevant PRC authority, in the name of the asset management plans as disclosed below, to subscribe for and 
hold the Offer Shares as a placee under the International Offering on behalf of the relevant GF Securities AM 
Ultimate Client on a non-discretionary basis. GF Securities AM, in the name of the asset management plans 
as disclosed below, will hold the legal title of the Offer Shares, and the economic risks and return of the 
Offer Shares will pass through to the GF Securities AM Ultimate Clients.
Details of the GF Securities AM Ultimate Clients are set out as below:
Name of the GF Securities AM Ultimate Clients
Name of the asset management plan
Shenwan Hongyuan Group Co., Ltd. (申萬宏源集
團股份有限公司, a company listed on the Stock 
Exchange (stock code: 6806) and the Shenzhen 
Stock Exchange (stock code: 000166))
GF Asset Management Wanxiang No. 1 Single Asset 
Management Plan (廣發資管萬享1號單一資產管理計
劃)
He Wei (賀偉)
GF Asset Management Excellence Diversified 
Allocation No. 37 Single Asset Management Plan (廣
發資管卓越多元配置37號單一資產管理計劃)
Zhonghe Capital Cultivation 920 Private Securities 
Investment Fund (中和資本耕耘920號私募證券投
資基金), whose ultimate beneficial owner is Zhang 
Jingting (張敬庭)
GF Asset Management Hong Kong Equity Diversified 
Strategy No. 7 Single Asset Management Plan 
To the best knowledge of GF Securities AM, (i) each of the GF Securities AM Ultimate Clients is an 
independent third party of the Company, its subsidiaries, its substantial shareholders, GF Securities (Hong 
Kong) Brokerage and the companies which are members of the same group of companies as GF Securities 
(Hong Kong) Brokerage; and (ii) GF Securities AM is not a collective investment scheme which is not 
authorized by the SFC nor is expected to hold the Offer Shares on behalf of such scheme.

<<<PAGE 25>>>
25
(5) 
Orient AM will hold the Offer Shares in its capacity as the discretionary fund manager on behalf of its 
underlying clients. Both Orient AM and Orient Securities is a wholly-owned subsidiary of Orient Securities 
International Financial Group Limited. Therefore, Orient AM is a member of the same group of Orient 
Securities. To the best knowledge of Orient AM, (i) each of the underlying clients of Orient AM is an 
independent third party of the Company, its subsidiaries, its substantial shareholders, Orient AM, Orient 
Securities and the companies which are members of the same group of companies as Orient Securities; and 
(ii) no ultimate beneficial owner holds 30% or more interest in each of the underlying clients of Orient AM, 
except that one discretionary account managed by Orient AM, namely Orient Asset Mgt (HK) Ltd-OSR 
Selective No.4, is wholly owned by an individual investor who is an independent third party.
Orient AM is investing on behalf of certain collective investment schemes which are not authorized by the SFC, 
details of which are as follow:
Fund Name
Types and 
values of 
assets under 
management
Whether 
the scheme 
is publicly 
marketed
Scheme 
establishment date
Identities of the general 
partners and the 20 largest 
limited partners of the 
scheme where applicable
Identity of the scheme 
administrator
Relationships among 
the scheme, the ultimate 
beneficial owner(s), Orient 
Securities and the Company
Orient Asset Mgt (HK) 
 Ltd-OSR Selective 
 No.4
Private Fund, 
 US$20 million
No
August 22, 2024
Not applicable as it is not in 
 partnership structure and 
 does not have any general 
 partner or limited partner
Agricultural Bank of 
 China Limited, Hong 
 Kong Branch
The scheme and ultimate 
 beneficial owners are 
 independent third parties 
 of Orient Securities, the 
 Company and the 
 Controlling Shareholders of 
 the Company.
ORIENT SUN RISE 
 FUND SERIES SPC – 
 ORIENT SUN RISE 
 OVERSEAS STABLE 
 FUND SEGREGATED 
 PORTFOLIO
Private Fund, 
 US$5 million
No
November 18, 2025
Not applicable as it is not in 
 partnership structure and 
 does not have any general 
 partner or limited partner
Agricultural Bank of 
 China Limited, Hong 
 Kong Branch
The scheme and ultimate 
 beneficial owners are 
 independent third parties 
 of Orient Securities, the 
 Company and the 
 Controlling Shareholders of 
 the Company.
The Company has applied to the Stock Exchange for, and the Stock Exchange has given, a consent 
under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate such Offer 
Shares in the International Offering to the connected clients listed above. The allocations of Offer 
Shares to such connected clients are in compliance with all the conditions under the consent given 
by the Stock Exchange.

<<<PAGE 26>>>
26
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or 
any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and 
the District of Columbia) or any other jurisdiction where such distribution is prohibited by law. 
This announcement does not constitute or form a part of any offer to sell or solicitation of an 
offer to buy, to purchase or subscribe for securities nor shall there be any sale of Offer Shares 
in the United States or in any other jurisdictions in which such offer or solicitation would be 
unlawful. The securities mentioned herein have not been, and will not be, registered under the 
United States Securities Act or any state securities law of the United States. The securities may 
not be offered, sold, pledged, or transferred within the United States or to, or for the account 
or benefit of U.S. persons (as defined in Regulation S) except pursuant to an exemption from, 
or in a transaction not subject to, the registration requirements of the U.S. Securities Act and in 
compliance with any applicable state securities laws.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities of the Company. This announcement is 
not a prospectus. Potential investors should read the Prospectus dated May 28, 2026 issued 
by LongBio Pharma (Suzhou) Co., Ltd. (天辰生物醫藥(蘇州)股份有限公司) for detailed 
information about the Global Offering described below before deciding whether or not to invest 
in the Offer Shares.
* 
Potential investors of the Offer Shares should note that the Sole Sponsor-Overall Coordinator (for itself and 
on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong 
Kong Underwriting Agreement upon the occurrence of any of the events set out in the paragraph headed 
“Underwriting — Underwriting Arrangements — Hong Kong Public Offering — Grounds for Termination” 
in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently 
expected to be Friday, June 5, 2026).
PUBLIC FLOAT AND FREE FLOAT
Immediately upon completion of the Global Offering (before any exercise of the Over-allotment 
Option) and the conversion of Unlisted Shares into H Shares, an aggregate of 33,698,881 H 
Shares, representing approximately 45.42% of the total issued share capital of the Company will 
be counted towards the public float. Pursuant to Rule 19A.13A(1) of the Listing Rules, where 
the expected market value at the time of Listing exceeds HK$6 billion but not exceeding HK$30 
billion, the minimum number of H shares held by the public at the time of Listing as a percentage 
of the total number of shares in the class to which H shares belong shall be the higher of: (i) the 
percentage that would result in the expected market value of H shares held by the public to be 
HK$1,500,000,000 at the time of Listing; and (ii) 15%. Based on the Offer Price of HK$96.06 per 
Offer Share, the expected market capitalization of the Company’s H Shares would exceed HK$6 
billion and the percentage that would result in the expected market value of H shares held by the 
public to be HK$1,500,000,000 at the time of Listing would be 21.05%. Therefore, the Company 
will be able to meet the minimum public float requirement under Rule 19A.13A(1) of the Listing 
Rules.

<<<PAGE 27>>>
27
Under the applicable PRC laws, all existing Shareholders are subject to a lock-up period of 
twelve months following the Listing Date. Each of the Cornerstone Investors has agreed to 
a lock-up period of six months following the Listing Date. As such, H Shares held by all 
existing Shareholders and the Cornerstone Investors are not counted towards the free float of 
the H Shares at the time of Listing. Based on the Offer Price of HK$96.06 per Offer Share, the 
expected market value of the H Shares held by the public and not subject to disposal restrictions 
exceeds HK$600,000,000. As such, the Company satisfies the free float requirement under Rule 
19A.13C(1)(b) of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering and 
the conversion of Unlisted Shares into H Shares, (i) the three largest public Shareholders do not 
hold more than 50% of the H Shares in public hands at the time of Listing in compliance with 
Rules 8.08(3) and 8.24 of the Listing Rules; (ii) there will not be any new substantial Shareholder 
(as defined in the Listing Rules) immediately after the Global Offering; (iii) no placee will, 
individually, be placed more than 10% of the enlarged issued share capital of the Company 
immediately after the Global Offering; and (iv) there will be at least 300 Shareholders at the time 
of Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Friday, June 5, 
2026 (Hong Kong time), provided that the Global Offering has become unconditional and the right 
of termination described in the section headed “Underwriting — Underwriting Arrangements — 
Hong Kong Public Offering — Grounds for Termination” in the Prospectus has not been exercised. 
Investors who trade the H Shares on the basis of publicly available allocation details prior to the 
receipt of H Share certificates or prior to the H Share certificates becoming valid evidence of title 
do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Friday, June 
5, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange will 
commence at 9:00 a.m. on Friday, June 5, 2026 (Hong Kong time). The H Shares will be traded in 
board lots of 50 H Shares each, and the stock code of the H Shares will be 01779.
By order of the Board
LongBio Pharma (Suzhou) Co., Ltd.
Liu Heng
Chairman of the Board and executive Director
Hong Kong, June 4, 2026
As of the date of this announcement, the Board comprises (i) Dr. LIU Heng, Dr. SUN Bill 
Nai-chau and Mr. XIE Ming as executive Directors; (ii) Mr. LIN Jian, Ms. GU Qin, Dr. XUE Di 
and Dr. CHEN Kan as non-executive Directors; and (iii) Mr. SIU Paul Yu Hay, Mr. RUAN Tim, 
Mr. YANG Chun and Mr. ZHOU Guofang as independent non-executive Directors.
