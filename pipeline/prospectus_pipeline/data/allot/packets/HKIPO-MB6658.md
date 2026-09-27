# 配发结果公告抽取任务：6658.HK Liuliumei Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**12/06/2026 22:38**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0612/2026061202100.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6658.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited
(the
“Stock
Exchange”)
and
Hong
Kong
Securities
Clearing
Company
Limited
(“HKSCC”) take no responsibility for the contents of this announcement, make no
representation as to its accuracy or completeness and expressly disclaim any liability
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of
the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or
into the United States (including its territories and possessions, any state of the United
States and the District of Columbia). This announcement does not constitute or form a part
of any offer or solicitation to purchase or subscribe for securities in the United States or in
any other jurisdictions. The securities mentioned herein have not been, and will not be,
registered under the United States Securities Act of 1933 as amended from time to time (the
“U.S. Securities Act”) or securities law of any state or other jurisdiction of the United
States. The securities may not be offered, sold, pledged or otherwise transferred within the
United States except pursuant to an exemption from the registration requirements of the
U.S. Securities Act and in compliance with any applicable state securities laws, or outside
the United States unless in compliance with Regulation S under the U.S. Securities Act.
There will be no public offer of securities in the United States.
This announcement is for information purposes only and does not constitute an invitation or
offer to acquire, purchase or subscribe for securities. This announcement is not a
prospectus. Potential investors should read the prospectus dated June 5, 2026(the
“Prospectus”) issued by Liuliumei Co., Ltd. (溜溜梅股份有限公司) (the “Company”)
for detailed information about the Global Offering described below before deciding whether
or not to invest in the H Shares thereby being offered. Any investment decision in relation to
the Offer Shares should be taken solely in reliance on the information in the Prospectus. The
Company has not been and will not be registered under the U.S. Investment Company Act of
1940, as amended.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the
same meanings as those defined in the Prospectus.
No stabilizing manager will be appointed, and it is anticipated that no stabilization
activities will be carried out in relation to the Global Offering.
Potential investors of the Offer Shares should note that the Overall Coordinators (for
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate
their obligations under the Hong Kong Underwriting Agreement with immediate effect upon
the occurrence of any of the events set out in the section headed “Underwriting —
Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for
Termination” in the Prospectus at any time prior to 8: 00 a.m. (Hong Kong time) on the
Listing Date (which is currently expected to be on Monday, June 15, 2026).
– 1 –

<<<PAGE 2>>>
Liuliumei Co., Ltd.
溜溜梅股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the
Global Offering
:
11,464,100 H Shares
Number of Hong Kong Offer Shares
:
1,146,500 H Shares
Number of International Offer Shares
:
10,317,600 H Shares
Offer Price
:
HK$43.58 per H Share plus brokerage of
1.0%, SFC transaction levy of
0.0027%, Stock Exchange trading fee of
0.00565% and AFRC transaction levy
of 0.00015%
Nominal value
:
RMB1.00 per H Share
Stock Code
:
6658
Joint Sponsors, Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and
Joint Lead Managers
Joint Bookrunners and Joint Lead Managers
Зࡋ⳪暲
@:9)
– 2 –

<<<PAGE 3>>>
LIULIUMEI CO., LTD./溜溜梅股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the
same meanings as those defined in the prospectus dated June 5, 2026 (the “Prospectus”)
issued by Liuliumei Co., Ltd. (溜溜梅股份有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of
Shareholders, Shareholders and prospective investors should be aware that the price of
the H Shares could move substantially even with a small number of the H Shares traded
and should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
6658
Stock short name
LIULIUMEI
Dealings commencement date
June 15, 2026*
*
see note at the end of the announcement
Price Information
Offer Price
HK$43.58
Offer Shares and Share Capital
Number of Offer Shares
11,464,100
Final Number of Offer Shares in Hong Kong Public Offering
1,146,500
Final Number of Offer Shares in International Offering
10,317,600
Number of issued Shares upon Listing
78,811,208
Over-allocation
No. of Offer Shares over-allocated
0
Note:
There has been no over-allocation of Offer Shares in the International Placing. Therefore, the
Over-allotment Option will not be exercised.
Proceeds
Gross proceedsNote
HK$499.6 million
Less: Estimated listing expenses payable based on the Offer Price
HK$59.5 million
Net proceeds
HK$440.1 million
Note:
Gross proceeds refer to the amount which the Company is entitled to receive. For details of the use
of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the
Prospectus.
– 3 –

<<<PAGE 4>>>
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
180,507
No. of successful applications
11,465
Subscription level
6,586.73 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong
Kong Public Offering
1,146,500
Final no. of Offer Shares under the Hong Kong Public
Offering
1,146,500
% of Offer Shares under the Hong Kong Public
Offering to the Global Offering
10%
Note:
For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can
refer to www.eipo.com.hk/eIPOAllotment to perform a search by identification number or
www.eipo.com.hk/eIPOAllotment for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
64
Subscription level
2.64 times
No. of Offer Shares initially available under the
International Offering
10,317,600
Final no. of Offer Shares under the International
Offering
10,317,600
% of Offer Shares under the International Offering to
the Global Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for
(a) a waiver under Rule 10.04 of the Listing Rules and a consent under paragraph 1C(2) of
Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock
Exchange to permit H Shares in the International Offering to be placed to Fanchang
Revitalization, a close associate of Huaan Fund and Xingnong Fund (collectively, the
“Existing Shareholders”), as a Cornerstone Investor; and (b) a consent under paragraph
1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing Applicants
to permit the Company to allocate certain Offer Shares in the International Offering to
connected clients, (i) none of the Offer Shares subscribed by the placees and the public have
been financed directly or indirectly by the Company, any of the Directors, chief executive of
the Company, Controlling Shareholders, substantial Shareholders, existing Shareholders of
the Company or any of its subsidiaries or their respective close associates; and (ii) none of
the placees and the public who have purchased the Offer Shares are accustomed to taking
instructions from the Company, any of the Directors, chief executive of the Company,
Controlling Shareholders, substantial Shareholders, existing Shareholders of the Company
or any of its subsidiaries or their respective close associates in relation to the acquisition,
disposal, voting or other disposition of the H Shares registered in his/her/its name or
otherwise held by him/her/it.
– 4 –

<<<PAGE 5>>>
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of Offer
Shares allocated
Approximate %
of the Offer
Shares
Approximate %
of total issued
share capital
after the Global
Offering
Existing
Shareholders or
their close
associatesNote 2
Fanchang RevitalizationNote 1
1,610,000
14.04%
2.04%
YesNote 2
Top New
1,777,100
15.50%
2.26%
No
Total
3,387,100
29.55%
4.30%
Notes:
1.
The Offer Shares subscribed for by Fanchang Revitalization as a Cornerstone Investor are subject to
lock-up restrictions as indicated below. For details, please refer to the section headed “Lock-up
Undertakings — Cornerstone Investors” in this announcement.
2.
As disclosed in the section headed “Waivers from Strict Compliance with the Listing Rules” in the
Prospectus, solely for the purpose of the Global Offering, Fanchang Revitalization is considered to be
a close associate of the Existing Shareholders (i.e., Wuhu Huaan Zhanxin Equity Investment Fund
Partnership (Limited Partnership)* (蕪湖華安戰新股權投資基金合夥企業（有限合夥）(“Huaan
Fund”) and Wuhu Fanchang District Xingnong Industrial Investment Fund Co., Ltd.* (蕪湖市繁昌區
興農產業投資基金有限公司) (“Xingnong Fund”)), which in aggregate hold less than 5% voting rights
of the Company. For details of the prior waiver under Rule 10.04 of the Listing Rules and consent
under paragraph 1C(2) of the Placing Guidelines in relation to subscription of H Shares by a close
associate of an existing Shareholder as a Cornerstone Investor, please refer to the section headed
“Others/Additional Information — Allocation of Offer Shares to a close associate of Existing
Shareholders as a cornerstone investor” in this announcement.
– 5 –

<<<PAGE 6>>>
Allottees with Consents Obtained
Investor
No. of Offer
Shares allocated
% of the Offer
Shares
% of total
issued share
capital after the
Global Offering
Relationship
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for
New Listing Applicants in relation to allocations to connected clientsNote 1
CSI Capital Management
Limited (“CSICM”)
520,000
4.54%
0.66%
Connected
client as a
placee
CITIC Securities Asset
Management Company
Limited (“CITICS AM”)
20,000
0.17%
0.03%
Connected
client as a
placee
Note:
1.
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the
Guide for New Listing Applicants in relation to allocations to connected clients, please refer to the
sections headed “Others/Additional Information — Placing to connected clients with a consent under
paragraph 1C(1) of the Placing Guidelines” in this announcement.
LOCK-UP UNDERTAKINGS
Controlling Shareholders
NameNote 1
Number and
description of
Shares held in
the Company
subject to
lock-up
undertakings
upon Listing
% of total
issued H Shares
after the Global
Offering subject
to lock-up
undertakings
Note 2
% of
shareholding in
the Company
subject to
lock-up
undertakings
Last day
subject to the
lock-up
undertakings
Note 3
Mr. Yang
59,108,359
H Shares
75.00%
75.00%
June 14, 2027
Ms. Li
59,108,359
H Shares
75.00%
75.00%
June 14, 2027
Jurun Investment
24,600,000
H Shares
31.21%
31.21%
June 14, 2027
Kaixuan Star
3,600,000
H Shares
4.57%
4.57%
June 14, 2027
Kailai Star
2,400,000
H Shares
3.05%
3.05%
June 14, 2027
– 6 –

<<<PAGE 7>>>
NameNote 1
Number and
description of
Shares held in
the Company
subject to
lock-up
undertakings
upon Listing
% of total
issued H Shares
after the Global
Offering subject
to lock-up
undertakings
Note 2
% of
shareholding in
the Company
subject to
lock-up
undertakings
Last day
subject to the
lock-up
undertakings
Note 3
Notes:
1.
For illustrative purposes only, this subsection lists only those members of the Controlling Shareholders
who hold Shares directly in the Company. Pursuant to Rule 10.07 of the Listing Rules, each
Controlling Shareholder (namely, Mr. Yang, Ms. Li, Jurun Investment, Kaixuan Star, Kailai Star and
Liuliu Star) has undertaken to the Stock Exchange and the Company that, except pursuant to the
Global Offering, it/he/she will not, and shall procure that the relevant registered holder(s) will not,
without the prior written consent of the Stock Exchange or unless otherwise permitted under the
Listing Rules, at any time in the period commencing on the date by reference to which disclosure of
its/his shareholding is made in the Prospectus and ending on the date which is six months from the
Listing Date (the “First Six Month Period”), either directly or indirectly, dispose of, nor enter into
any agreement to dispose of or otherwise create any options, rights, interests or encumbrances in
respect of, any of the securities of the Company in respect of which it/he is shown by the Prospectus
to be the beneficial owner; or, during the period of six months immediately following the expiry of
such six-month period(the “Second Six Month Period”), directly or indirectly dispose of, nor enter
into any agreement to dispose of or otherwise create any options, rights, interests or encumbrances in
respect of, any such securities if, immediately following such disposal or upon the exercise or
enforcement of any such options, rights, interests or encumbrances, it/he would cease to be a
Controlling Shareholder of the Company (or would together with other Controlling Shareholders cease
to be Controlling Shareholders of the Company). For further details, please refer to the section
headed “Underwriting — Lock Up Arrangement — Undertakings to the Stock Exchange pursuant to
the Listing Rules — (B) Undertakings by Each of Our Controlling Shareholders” in the Prospectus.
2.
Upon completion of the Global Offering, 67,347,108 Unlisted Shares are converted into H Shares on a
one-for-one basis.
3.
The expiry day of the lock-up period shown in the table above is pursuant to the PRC Company Law.
In accordance with the relevant Listing Rule, the required lock-up for First Six Month Period ends on
December 14, 2026 and the Second Six Month Period ends on June 14, 2027.
– 7 –

<<<PAGE 8>>>
Cornerstone Investors
Name
Number and
description of
Shares held in
the Company
subject to
lock-up
undertakings
upon Listing
% of total Offer
Shares after the
Global Offering
subject to
lock-up
undertakings
% of
shareholding in
the Company
subject to
lock-up
undertakings
Last day
subject to the
lock-up
undertakings
Note 1
Fanchang Revitalization
1,610,000
H Shares
14.04%
2.04%
March 14, 2027
Top New
1,777,100
H Shares
15.50%
2.26%
March 14, 2027
Note:
1.
In accordance with the relevant cornerstone investment agreements, the required lock-up periods will
end on March 14, 2027. The Cornerstone Investors will cease to be prohibited from disposing of or
transferring the H Shares subscribed for pursuant to the relevant cornerstone investment agreements
after the indicated date.
Pre-IPO Investors
Name
Number and
description of
Shares held in
the Company
subject to
lock-up
undertakings
upon Listing
% of total
issued H Shares
after the Global
Offering subject
to lock-up
undertakings
Note 1
% of
shareholding in
the Company
subject to
lock-up
undertakings
Last day
subject to the
lock-up
undertakings
Note 2
Shenzhen Junrong
3,715,170 H
Shares
4.71%
4.71%
June 14, 2027
Nuoxiang Dongchen
1,361,977 H
Shares
1.73%
1.73%
June 14, 2027
Huaan Fund
1,210,646 H
Shares
1.54%
1.54%
June 14, 2027
Xingnong Fund
1,059,315 H
Shares
1.34%
1.34%
June 14, 2027
Nuoxiang Jinhong
891,641 H
Shares
1.13%
1.13%
June 14, 2027
Notes:
1.
Upon completion of the Global Offering, 67,347,108 Unlisted Shares are converted into H Shares on a
one-for-one basis.
2.
The expiry day of the lock-up period shown in the table above is pursuant to the PRC Company Law.
– 8 –

<<<PAGE 9>>>
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of
H Shares
allotted
Allotment as
% of the
International
Offering
Allotment as
% of total
Offer Shares
Number of
H Shares
held upon
Listing
% of total
issued share
capital upon
Listing
Top 1
1,777,100
17.22%
15.50%
1,777,100
2.25%
Top 5
5,495,700
53.27%
47.94%
7,765,661
9.85%
Top 10
7,284,200
70.60%
63.54%
9,554,161
12.12%
Top 25
9,421,100
91.31%
82.18%
11,691,061
14.83%
Note:
*
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
Number of
H Shares
allotted
Allotment as
% of the
International
Offering
Allotment as
% of total
Offer Shares
Number of
H Shares
held upon
Listing
% of total
issued share
capital upon
Listing
Top 1
—
—
—
59,108,359
75.00%
Top 5
3,387,100
32.83%
29.55%
69,842,567
88.62%
Top 10
6,015,700
58.31%
52.47%
73,362,808
93.09%
Top 25
9,146,100
88.65%
79.78%
76,493,208
97.06%
Note:
*
Ranking of H Shareholders is based on the number of H Shares held by the Shareholders upon Listing.
SHAREHOLDERS CONCENTRATION ANALYSIS
Shareholders*
Number of
H Shares
allotted
Allotment as
% of the
International
Offering
Allotment as
% of total
Offer Shares
Number of
H Shares
held upon
Listing
Number of
Shares held
upon Listing
% of total
issued share
capital upon
Listing
Top 1
—
—
—
59,108,359
59,108,359
75.00%
Top 5
3,387,100
32.83%
29.55%
69,842,567
69,842,567
88.62%
Top 10
6,015,700
58.31%
52.47%
73,362,808
73,362,808
93.09%
Top 25
9,146,100
88.65%
79.78%
76,493,208
76,493,208
97.06%
Notes:
*
Ranking of Shareholders is based on the number of Shares held by the Shareholders upon Listing.
– 9 –

<<<PAGE 10>>>
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications
made by the public will be conditionally allocated on the basis set out below:
NO. OF H
SHARES
APPLIED FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED OF
THE TOTAL NO.
OF H SHARES
APPLIED FOR
POOL A
100
32,294
485 out of 32,294 to receive 100 Shares
1.50%
200
29,943
454 out of 29,943 to receive 100 Shares
0.76%
300
5,619
86 out of 5,619 to receive 100 Shares
0.51%
400
5,393
84 out of 5,393 to receive 100 Shares
0.39%
500
4,675
73 out of 4,675 to receive 100 Shares
0.31%
600
2,275
36 out of 2,275 to receive 100 Shares
0.26%
700
2,004
32 out of 2,004 to receive 100 Shares
0.23%
800
1,612
26 out of 1,612 to receive 100 Shares
0.20%
900
1,655
27 out of 1,655 to receive 100 Shares
0.18%
1,000
11,045
182 out of 11,045 to receive 100 Shares
0.16%
1,500
3,375
58 out of 3,375 to receive 100 Shares
0.11%
2,000
6,216
113 out of 6,216 to receive 100 Shares
0.09%
2,500
2,711
51 out of 2,711 to receive 100 Shares
0.08%
3,000
2,091
41 out of 2,091 to receive 100 Shares
0.07%
3,500
1,575
32 out of 1,575 to receive 100 Shares
0.06%
4,000
1,582
34 out of 1,582 to receive 100 Shares
0.05%
4,500
1,977
44 out of 1,977 to receive 100 Shares
0.05%
5,000
2,397
55 out of 2,397 to receive 100 Shares
0.05%
6,000
1,896
47 out of 1,896 to receive 100 Shares
0.04%
7,000
1,654
43 out of 1,654 to receive 100 Shares
0.04%
8,000
1,475
41 out of 1,475 to receive 100 Shares
0.03%
9,000
1,517
45 out of 1,517 to receive 100 Shares
0.03%
10,000
7,970
248 out of 7,970 to receive 100 Shares
0.03%
20,000
5,494
261 out of 5,494 to receive 100 Shares
0.02%
30,000
3,206
205 out of 3,206 to receive 100 Shares
0.02%
40,000
2,498
200 out of 2,498 to receive 100 Shares
0.02%
50,000
2,560
247 out of 2,560 to receive 100 Shares
0.02%
60,000
1,750
197 out of 1,750 to receive 100 Shares
0.02%
70,000
1,877
242 out of 1,877 to receive 100 Shares
0.02%
80,000
1,481
215 out of 1,481 to receive 100 Shares
0.02%
90,000
1,296
210 out of 1,296 to receive 100 Shares
0.02%
100,000
9,089
1,619 out of 9,089 to receive 100 Shares
0.02%
Total
162,202
Total number of Pool A successful applicants: 5,733
– 10 –

<<<PAGE 11>>>
NO. OF H
SHARES
APPLIED FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED OF
THE TOTAL NO.
OF H SHARES
APPLIED FOR
POOL B
150,000
6,257
1,388 out of 6,257 to receive 100 Shares
0.01%
200,000
2,683
676 out of 2,683 to receive 100 Shares
0.01%
250,000
1,665
470 out of 1,665 to receive 100 Shares
0.01%
300,000
1,136
355 out of 1,136 to receive 100 Shares
0.01%
350,000
885
303 out of 885 to receive 100 Shares
0.01%
400,000
697
260 out of 697 to receive 100 Shares
0.01%
450,000
1,319
532 out of 1,319 to receive 100 Shares
0.01%
573,200
3,663
1,748 out of 3,663 to receive 100 Shares
0.01%
Total
18,305
Total number of Pool B successful applicants: 5,732
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules in respect of which waiver and
consent has been obtained, the Company has complied with the Listing Rules and
guidance materials in relation to the placing, allotment and listing of the H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the
placees or the public (as the case may be) directly or indirectly for each Offer Share
subscribed for or purchased by them is the same as the final Offer Price in addition to any
brokerage, AFRC transaction levy, SFC transaction levy and Stock Exchange trading fee
payable.
– 11 –

<<<PAGE 12>>>
OTHERS/ADDITIONAL INFORMATION
Allocation of Offer Shares to a close associate of Existing Shareholders as a cornerstone
investor
The Company has applied to the Stock Exchange for, and the Stock Exchange has
granted to the Company, a consent under paragraph 1C(2) of Appendix F1 to the Listing
Rules to allow Fanchang Revitalization, being a close associate of the Existing
Shareholders, to participate in the Global Offering as a cornerstone investor. Please
refer to the section headed “Waivers From Strict Compliance with the Listing Rules —
Consent under paragraph 1C(2) of Appendix F1 to the Listing Rules in respect of
subscription of Offer Shares by a close associate of an existing shareholder as a
cornerstone investor” in the Prospectus for details.
Such allocations of Offer Shares are in compliance with all the conditions under the
consent granted by the Stock Exchange.
For details of the allocations of Offer Shares to Fanchang Revitalization, please refer to
the section headed “Allotment Results Details — International Offering — Cornerstone
Investors” in this announcement.
Placing to connected clients with a consent under paragraph 1C(1) of the Placing Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients
of their connected distributors pursuant to the Placing Guidelines as placees. Please refer
to the section headed “Allotment Results Details — International Offering — Allottees
with Consents Obtained” in this announcement for details. The Company has applied to
the Stock Exchange for, and the Stock Exchange has granted, consents under paragraph
1C(1) of the Placing Guidelines to permit the Company to allocate such Offer Shares in
the International Offering to the connected clients as placees. The allocations of Offer
Shares to such connected clients are in compliance with all the conditions under the
consent granted by the Stock Exchange. Details of the placement to connected clients as
placees are set out below:
No.
Connected
Distributor
Connected Client
Relationship
Whether the
connected client is a
collective investment
scheme which is not
authorized by the
SFC or is expected
to hold the Offer
Shares on behalf of
such scheme
Whether the
Connected Client will
hold the beneficial
interests of the Offer
Shares on a
non-discretionary basis
or discretionary basis
for independent third
parties
Number of Offer
Shares to be
allocated to the
Connected Client
Approximate
percentage of total
number of Offer
Shares under the
Global Offering
Approximate
percentage of total
issued share capital
immediately
following
completion of the
Global Offering
1.
CLSA Limited
(CLSA)
CSI Capital Management
Limited (“CSICM”)
(Note 1)
CSI Capital is a member of
the same group of
companies as CLSA
Limited
N
N
520,000
4.54%
0.66%
2.
CLSA Limited
(CLSA)
CITIC Securities Asset
Management Company
Limited (CITICS AM)
(Note 2)
CITICS AM is a member
of the same group of
companies as CLSA
Limited
Y
Y
20,000
0.17%
0.03%
– 12 –

<<<PAGE 13>>>
Notes:
1.
CSICM and CITIC Securities Company Limited will enter into a series of cross border OTC swap
transactions (the “OTC Swaps”) with the investment managers, who act for and on behalf of certain
ultimate clients (collectively, the “CSICM Ultimate Clients”), pursuant to which CSICM will hold the
Offer Shares to be subscribed for and on behalf of the investment managers on a nondiscretionary
basis to hedge the OTC Swaps while the economic risks and returns of the underlying Offer Shares are
passed to the CSICM Ultimate Clients, subject to customary fees and commissions. CSICM will not
take part in any economic returns or bear any economic losses in relation to the Offer Shares. The
OTC Swaps will be fully funded by the CSICM Ultimate Clients. Each of the investment managers
and their ultimate beneficial owner is independent from each of the Company, its subsidiaries and
substantial shareholders. The CSICM Ultimate Clients for purpose of this placee subscription
include:
睿元進取一號私募證券投資基金
(“Ruiyuan
Fund”)
and
睿景金瑞6號私募證券投資基金,
(“Ruijing Fund”), which are managed by Shenzhen Qianhai Ruijing Kaiyuan Capital Management
Co., Ltd. (深圳前海睿景開元基金管理有限公司) (“Shenzhen Qianhai”). No ultimate beneficial owner
holds 30% or more interest in Ruiyuan Fund. The ultimate beneficial owner holds 30% or more
interest in Ruijing Fund is Liao Chang (廖暢). Cai Zhiguo (蔡志國) and Zhang Lili (張麗麗) each
holds 30% or more interest in Shenzhen Qianhai.
2.
CITICS AM is a member of the same group of companies as CLSA. CITICS AM will hold the Offer
Shares in its capacity as the discretionary fund manager managing the funds on behalf of their
investors (the “CITICS AM Ultimate Clients”), each of which is, to the best knowledge of CITICS
AM, (i) an independent third party of the Company, its subsidiaries, its substantial shareholders,
CITICS AM, CLSA and the companies which are members of the same group of companies as CLSA;
and (ii) a collective investment scheme which is not authorized by the SFC. No ultimate beneficial
owner holds 30% or more interest in the funds.
The details of the CITICS AM Ultimate Clients are as follow.
No.
Fund Name
Fund
Manager
UBO of
Fund Manager
Limited Partner/
Shareholding
holding 30% or
more in the
CITICS AM
Ultimate Clients
1.
CITIC SECURITIES COMPANY
LIMITED-XINHANG ZHIYUAN
NO.1 (中信證券信航致遠1號集合資產
管理計劃)
CITICS AM
CITIC Securities
Company Limited
N/A
2.
CITIC SECURITIES COMPANY
LIMITED-XINHANG ZHIYUAN
NO.3 (中信證券信航致遠3號集合資產
管理計劃)
CITICS AM
CITIC Securities
Company Limited
N/A
To the best of knowledge of CITICS AM and after making all reasonable enquiries,
CITICS AM Ultimate Client, together with each of their ultimate beneficial owners, is an
independent third party of the Company, its subsidiaries, its substantial shareholders,
CITICS AM, CLSA and the companies which are members of the same group of CLSA.
– 13 –

<<<PAGE 14>>>
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong
Limited and Hong Kong Securities Clearing Company Limited take no responsibility for
the contents of this announcement, make no representation as to its accuracy or
completeness and expressly disclaim any liability whatsoever for any loss howsoever
arising from or in reliance upon the whole or any part of the contents of this
announcement.
This announcement is not for release, publication or distribution, directly or indirectly, in
or into the United States (including its territories and possessions, any state of the United
States and the District of Columbia or any other jurisdiction where such distribution is
prohibited by laws). This announcement does not constitute or form a part of any offer or
solicitation to purchase or subscribe for securities in the United States or in any other
jurisdictions. The securities mentioned herein have not been, and will not be, registered
under the United States Securities Act of 1933 as amended from time to time (the “U.S.
Securities Act”) or securities law of any state or other jurisdiction of the United States.
The securities may not be offered, sold, pledged or otherwise transferred within the United
States except pursuant to an exemption from the registration requirements of the U.S.
Securities Act and in compliance with any applicable state securities laws. The Offer
Shares are being offered and sold solely outside the United States in offshore transactions
in reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation
or offer to acquire, purchase or subscribe for securities. This announcement is not a
prospectus. Potential investors should read the Prospectus dated June 5, 2026 issued by
Liuliumei Co., Ltd. (溜溜梅股份有限公司) for detailed information about the Global
Offering described below before deciding whether or not to invest in the Offer Shares
thereby being offered.
*
Potential investors of the Offer Shares should note that the Joint Sponsors and the
Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters)
shall be entitled to terminate their obligations under the Hong Kong Underwriting
Agreement with immediate effect upon the occurrence of any of the events set out in
the section headed “Underwriting — Underwriting Arrangements and Expenses —
Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any
time prior to 8: 00 a.m. (Hong Kong time) on the Listing Date (which is currently
expected to be on June 15, 2026).
– 14 –

<<<PAGE 15>>>
PUBLIC FLOAT AND FREE FLOAT
Out of the 67,347,108 H Shares to be converted from Domestic Shares and listed on the
Stock Exchange following the Global Offering: (i) 8,238,749 H Shares, representing
approximately 10.45% of the total issued share capital of our Company immediately
after the Global Offering, which will be held by Shenzhen Junrong, Nuoxiang Dongchen,
Nuoxiang Jinhong, Huaan Fund and Xingnong Fund, will be counted towards the public
float; and (ii) 59,108,359 H Shares, representing approximately 75.00% of the total
issued share capital of our Company immediately after the Global Offering, which will be
held by Mr. Yang, Ms. Li, Jurun Investment, Kaixuan Star and Kailai Star, who/which
are core connected persons of our Company, will not be counted towards the public float.
Based on the Offer Price of HK$43.58 per Offer Share, immediately following the
conversion of the Domestic Shares into H Shares and completion of the Global Offering,
the expected market capitalization of the H Shares at the time of Listing will be
approximately HK$3.44 billion. To the best knowledge of our Directors, upon
completion of the Global Offering and Conversion of the Domestic Shares into H
Shares, 19,702,849 H Shares held or controlled by our Shareholders who are not our core
connected persons, representing 25.0001% of the total issued H Shares, will be counted
towards the public float which is higher than 25%, the minimum prescribed percentage of
H Shares required to be held in public hands under Rule 19A.13A(1) of the Listing Rules
applicable to the Company. Therefore, the Company will be able to meet the public float
requirement under Rule 19A.13A of the Listing Rules at the time of the Listing.
FREE FLOAT
Based on the Offer Price of HK$43.58 per Offer Share, it is expected that 8,077,000 H
Shares will not be subject to any disposal restrictions (whether under contract, the
Listing Rules, applicable laws or otherwise), representing approximately 10.25% of our
total issued share capital upon Listing and a market capitalization of approximately
HK$352.0 million. Therefore, our Company will be able to satisfy the free float
requirement under Rule 19A.13C(1)(a) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8: 00 a.m. on Monday,
June 15, 2026 (Hong Kong time), provided that the Global Offering has become
unconditional and the right of termination described in the section headed “Underwriting
— Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds
for Termination” in the Prospectus has not been exercised. Investors who trade the H
Shares on the basis of publicly available allocation details prior to the receipt of H Share
certificates or prior to the H Share certificates becoming valid evidence of title do so
entirely at their own risk.
– 15 –

<<<PAGE 16>>>
Assuming that the Global Offering becomes unconditional at or before 8: 00 a.m. on
Monday, June 15, 2026 (Hong Kong time), it is expected that dealings in the H Shares on
the Stock Exchange will commence at 9: 00 a.m. on Monday, June 15, 2026 (Hong Kong
time). The H Shares will be traded in board lots of 100 H Shares each, and the stock code
of the H Shares will be 6658.
By order of the Board
Liuliumei Co., Ltd.
溜溜梅股份有限公司
Mr. Yang Fan
Chairman of the Board and Chief Executive Officer
Hong Kong, June 12, 2026
As at the date of this announcement, the Board comprises (i) Mr. Yang Fan, Mr. Ning
Pengfei, Ms. Hu Yan, Mr. Gou Bin and Mr. Mei Huixiang as executive Directors; (ii) Mr.
Xu Lianzheng as non-executive Directors; and (iii) Mr. Liu Feng, Mr. Xiong Hui and Mr.
Lu Jian as independent non-executive Directors.
– 16 –
