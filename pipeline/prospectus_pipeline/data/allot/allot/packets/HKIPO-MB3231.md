# 配发结果公告抽取任务：3231.HK Excelland Robotics (Wuxi) Co. Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**08/09/2026 19:59**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0908/2026090800985.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"3231.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC“) take no responsibility
for the contents of this announcement, make no representation as to its accuracy or completeness and
expressly disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon
the whole or any part of the contents of this announcement.
Unless otherwise defined in this announcement, capitalised terms used herein shall have the same
meanings as those defined in the prospectus dated 31 August 2026 (the “Prospectus”) issued by
Excelland Robotics (Wuxi) Co. Ltd. (優地機器人（無錫）股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an offer or an invitation
to induce an offer by any person to acquire, purchase or subscribe for any securities of the Company.
This announcement is not a prospectus. Potential investors should read the Prospectus for detailed
information about the Company and the Global Offering described below before deciding whether or
not to invest in the Offer Shares. Any investment decision in relation to the Offer Shares should be
taken solely in reliance on the information in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the
United States (including its territories and possessions, any state of the United States and the District
of Columbia) or any other jurisdiction where such distribution is prohibited by law. This
announcement does not, and is not intended to, constitute or form a part of any offer to sell or
solicitation of an offer to buy, to purchase or subscribe for securities nor shall there be any sale of
Offer Shares in the United States or in any other jurisdictions in which such offer or solicitation
would be unlawful. The Offer Shares have not been, and will not be, registered under the United States
Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or any state securities
law of the United States. The securities may not be offered, sold, pledged, or transferred within the
United States or to, or for the account or benefit of U.S. persons (as defined in Regulation S under
the U.S. Securities Act (“Regulation S“)) except pursuant to an exemption from, or in a transaction
not subject to, the registration requirements of the U.S. Securities Act and in compliance with any
applicable state securities laws. There will be no public offering of the Offer Shares in the United
States. The Offer Shares are being offered and sold outside the United States in offshore transactions
in reliance on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, Silver Nile Global Investments Limited acts as the Sole
Sponsor and the Sponsor-Overall Coordinator; and Silver Nile Global Investments Limited, CEB
International Capital Corporation Limited and CMBC Securities Company Limited act as Overall
Coordinators.
Potential investors of the Offer Shares should note that the Sole Sponsor and the Overall Coordinators
(for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence
of any of the events set out in the paragraph headed “Underwriting — Underwriting Arrangements
and Expenses — Hong Kong Public Offering - Grounds for Termination” in the Prospectus at any time
prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on
Wednesday, 9 September 2026).
−1 −

<<<PAGE 2>>>
Excelland Robotics (Wuxi) Co. Ltd.
優地機器人（無錫）股份有限公司
(A joint stock company incorporated in the People’s Republic of China with
limited liability)
GLOBAL OFFERING
Number of Offer Shares under the
Global Offering
:
45,000,000 H Shares
Number of Hong Kong Offer Shares
:
2,781,800 H Shares (as adjusted
after reallocation)
Number of International Offer
Shares
:
42,218,200 H Shares (as adjusted
after reallocation)
Final Offer Price
:
HK$14.45 per H Share, plus
brokerage of 1.0%, SFC
transaction levy of 0.0027%, Stock
Exchange trading fee of 0.00565%
and AFRC transaction levy of
0.00015% (payable in full on
application in Hong Kong dollars
and subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock Code
:
3231
Sole Sponsor
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners
and Joint Lead Managers
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers
−2 −

<<<PAGE 3>>>
Excelland Robotics (Wuxi) Co. Ltd.
優地機器人（無錫）股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall
have the same meanings as those defined in the prospectus dated 31 August 2026 (the
“Prospectus”) issued by Excelland Robotics (Wuxi) Co. Ltd. (優地機器人（無錫）股
份有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of
Shareholders, Shareholders and prospective investors should be aware that
the price of the H Shares could move substantially even with a small number
of H Shares traded and should exercise extreme caution when dealing in the
H Shares.
SUMMARY
Company information
Stock code
3231
Stock short name
EXCELLAND ROBOT
Dealings commencement date
9 September 2026*
*see note at the end of the announcement
Price Information
Offer Price
HK$14.45
Offer Shares and Share Capital
Number of Offer Shares
45,000,000 H Shares
Number of Offer Shares in Hong Kong Public
Offering (as adjusted after reallocation)
2,781,800 H Shares
Number of Offer Shares in International Offering
(as adjusted after reallocation)
42,218,200 H Shares
Number of issued Shares upon Listing
416,368,421 Shares
Proceeds
Gross proceeds
HK$650.2 million
Less: Estimated listing expenses payable based
on the Offer Price
HK$73.6 million
Net proceeds
HK$576.6 million
Note: Gross proceeds refer to the amount to which the issuer is entitled to receive. For details of
the use of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the
Prospectus.
−3 −

<<<PAGE 4>>>
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
27,933
No. of successful applications
7,239
Subscription level
140.02 times
Claw-back triggered
No
No. of Offer Shares initially available under the Hong
Kong Public Offering
2,250,000
No. of Offer Shares reallocated from the
International Offering
531,800
Final no. of Offer Shares under the Hong Kong
Public Offering (after reallocation)
2,781,800
% of final no. of Offer Shares under the Hong Kong
Public Offering to the Global Offering
6.18%
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can
refer
to
www.eipo.com.hk/eIPOAllotment
to
perform
a
search
by
identification
number
or
www.eipo.com.hk/eIPOAllotment for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
87
Subscription level
0.99 times
No. of Offer Shares initially available under the
International Offering
42,750,000
No. of Offer Shares reallocated to the Hong Kong
Public Offering
531,800
Final no. of Offer Shares under the International
Offering (after reallocation)
42,218,200
% of final no. of Offer Shares under the
International Offering to the Global Offering
93.82%
The Directors confirm that, to the best of their knowledge, information and belief,
save for waivers from strict compliance with Rule 10.04 of the Listing Rules and a
consent under paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing
Guidelines”) granted by the Stock Exchange to permit H Shares in the International
Offering to be placed to certain existing shareholders and/or their close associates,
(i) none of the Offer Shares subscribed by the placees and the public have been
financed directly or indirectly by the Company, any of the Directors, chief executive
of the Company, the Single Largest Group of Shareholders, substantial Shareholders,
existing Shareholders of the Company or any of its subsidiaries or their respective
−4 −

<<<PAGE 5>>>
close associates; (ii) none of the placees and the public who have purchased the
Offer Shares are accustomed to taking instructions from the Company, any of the
Directors, chief executive of the Company, the Single Largest Group of Shareholders,
substantial Shareholders, existing Shareholders of the Company or any of its
subsidiaries or their respective close associates in relation to the acquisition,
disposal, voting or other disposition of Shares registered in his/her/its name or
otherwise held by him/her/it; (iii) there is no side agreement or arrangement between
the Company, any of the Directors, chief executive of the Company, the Single
Largest Group of Shareholders, substantial shareholders, existing Shareholders of
the Company or any of its subsidiaries or their respective close associates, on one
hand, and the public subscribers or the placees who have subscribed for the Offer
Shares, on the other hand; and (iv) no rebate has been, directly or indirectly,
provided by the Company, any of the Directors, chief executive of the Company, the
Single
Largest
Group
of
Shareholders,
substantial
Shareholders,
existing
Shareholders of the Company or any of its subsidiaries or their respective close
associates, or syndicate members, or any other brokers involved in the Global
Offering, to any public investors in the Hong Kong Public Offering or placees in the
International Offering.
The placees in the International Offering include the following:
Cornerstone Investors
Investor Note 1
No. of Offer
Shares
allocated
% of Offer
Shares
% of total
issued H
Shares after
the Global
Offering
% of total
issued Shares
after the
Global
Offering
Existing
shareholders
or their
close
associates
SensePower
Management
Limited
(“SensePower”)
1,089,600
2.42%
0.39%
0.26%
Yes
CYGG Holding
Limited
(“CYGG”)
544,800
1.21%
0.19%
0.13%
Yes
Total
1,634,400
3.63%
0.58%
0.39%
Note:
For further details of the Cornerstone Investors, please refer to the section headed
“Cornerstone Investors” in the Prospectus.
−5 −

<<<PAGE 6>>>
Allottees with Waivers/Consents Obtained
Investor
No. of Offer
Shares
allocated
% of Offer
Shares
% of total
issued H
Shares after
the Global
Offering
% of total
issued Shares
after the
Global
Offering Relationship
Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and
consent under paragraph 1C(2) of the Placing Guidelines in relation to subscription for
Offer Shares by existing minority shareholders and/or its close associates as cornerstone
investors Note 1
Cornerstone Investors
SensePower
1,089,600
2.42%
0.39%
0.26% A
cornerstone
investor and
a close
associate of
an existing
minority
shareholder
CYGG
544,800
1.21%
0.19%
0.13% A
cornerstone
investor and
a close
associate of
an existing
minority
shareholder
Total
1,634,400
3.63%
0.58%
0.39%
Note:
1.
See “Waivers From Strict Compliance with Listing Rules — Waiver Under Rule 10.04 and
Consent under Paragraph 1C(2) of Appendix F1 to the Listing Rules in respect of
Subscriptions of Offer Shares by Existing Shareholders and/or its Close Associates as
Cornerstone Investors” of the Prospectus and the section headed “Others / Additional
Information — Placing to existing shareholders and/or its close associates with a prior waiver
under Rule 10.04 and consent under paragraph 1C(2) of the Placing Guidelines” in this
announcement for further details.
−6 −

<<<PAGE 7>>>
LOCK-UP UNDERTAKINGS
Key Persons (as defined under Rule 18C.14 of the Listing Rules)
Name
Capacity
Number of
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
% of
shareholding
in the
Company
subject to
lock-up
undertakings
upon Listing
Last day subject to
the lock-up
undertakings Note 1
Mr. LU Ying
Co-founder,
Chairman of the
Board, Executive
Director and
Chief Executive
Officer
13,525,400
Shares
—
3.25% 8 September 2027
Shenzhen Eagle
Field
Management
Consulting
Centre (L.P.) (深
圳鷹田管理諮詢
中心(有限合夥))
(“Eagle Field
Platform”)
Share Incentive
Platform
controlled by Mr.
LU Ying
22,595,650
Shares Note 2
—
5.43% 8 September 2027
Chengdu
Excelland
Technology Co.,
Ltd. (成都優地技
術有限公司)
(“Chengdu
Excelland”)
A member of the
Single Largest
Group of
Shareholders,
which is
controlled by Mr.
LU Ying
53,188,450
Shares Note 3
—
12.77% 8 September 2027
Mr. GU
Zhenjiang
Co-founder,
Executive
Director,
President and
General Manager
16,035,600
Shares
—
3.85% 8 September 2027
Mr. LIU Dazhi
Co-founder
10,790,150
Shares
—
2.59% 8 September 2027
Mr. LUO Pei
Co-founder and
R&D vice
president
4,508,350
Shares
—
1.08% 8 September 2027
Mr. XIA Ge
Co-founder and
R&D vice
president
3,389,400
Shares
—
0.82% 8 September 2027
Subtotal
124,033,000
Shares
—
29.79%
−7 −

<<<PAGE 8>>>
Notes:
1.
Pursuant to the applicable PRC laws, all existing Shareholders are not permitted to dispose
of any of the Shares held by them within 12 months following the Listing Date. In accordance
with Rule 18C.14(1) of the Listing Rules, the required lock-up period for key persons
commences on the date by reference to which disclosure of its shareholding is made in the
Prospectus and end on the date which is 12 months from the Listing Date, i.e. 8 September
2027, being the same date on which the restriction against disposal of Shares under the
applicable PRC laws ends.
2.
As of the date of this announcement, Mr. LU Ying was the general partner of Eagle Field
Platform and held approximately 43.07% of partnership interest, who was responsible for its
overall management and was entitled to exercise the voting rights held by Eagle Field
Platform at his full and absolute discretion. As of the date of this announcement, there are two
limited partners in Eagle Field Platform. Ms. LIU Wei (the executive Director of the Company)
owned approximately 28.63% of the limited partnership interests in Eagle Field Platform,
which will be subject to disposal restrictions pursuant to Rule 18C.14 of the Listing Rules. Mr.
Chai owned approximately 28.30% of the limited partnership interests in Eagle Field
Platform.
3.
As of the date of this announcement, Chengdu Excelland was owned as to 98.52% by Youdi
Ruifeng and 1.48% by Ms. LIU Wei. As of the date of this announcement, Youdi Ruifeng was
wholly owned by Excelland Holdings, which was in turn wholly owned by Eagle Field
Holdings, the sole shareholder of which was Mr. LU Ying. Each of Youdi Ruifeng, Excelland
Holdings and Eagle Field Holdings will be subject to disposal restrictions pursuant to Rule
18C.14 of the Listing Rules.
−8 −

<<<PAGE 9>>>
Pathfinder SIIs
Name Note 1
Number of
Shares held
in the
Company
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
% of
shareholding
in the
Company
subject to
lock-up
undertakings
upon Listing
Last day subject to
the lock-up
undertakings Note 2
Beijing Legend Chengye
Equity Investment
Partnership (L.P.) (北京君聯
成業股權投資合夥企業
(有限合夥)) (“Legend
Chengye”)
29,775,900 H
Shares
10.55%
7.15% 8 September 2027
Rajax Network Technology
(Shanghai) Co., Ltd. (拉扎斯
網絡科技(上海)有限公司)
(“Rajax”)
29,342,250 H
Shares
10.40%
7.05% 8 September 2027
Hainan Yunfeng Fund Centre
(L.P.) (海南雲鋒基金中心(有
限合夥)) (“Hainan
Yunfeng”)
23,750,650 H
Shares
8.42%
5.70% 8 September 2027
Subtotal
82,868,800
Shares
(including
82,868,800 H
Shares)
29.37%
19.9%
Notes:
1.
Each of the Shareholders listed in the above table is a Pathfinder SII of the Company as
defined under Chapter 2.5 of the Guide for New Listing Applicants.
2.
In accordance with Rule 18C.14(2) of the Listing Rules, the required lock-up period
commences on the date by reference to which disclosure of its shareholding is made in the
Prospectus and ends on the date which is six months from the Listing Date, i.e. 8 March 2027.
In addition to the lockup requirement under Rule 18C.14(2) of the Listing Rules, all existing
Shareholders are not permitted to dispose of any of the Shares held by them within 12 months
following the Listing Date, i.e. ending on 8 September 2027, as required under the applicable
PRC laws.
−9 −

<<<PAGE 10>>>
Single Largest Group of Shareholders
Name Note 1
Capacity
Number of
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
% of
shareholding
in the
Company
subject to
lock-up
undertakings
upon Listing
Last day subject to
the lock-up
undertakings Note 2
Mr. LU Ying
Beneficial
Interest
13,525,400
Shares
—
3.25% 8 September 2027
Eagle Field
Platform
Beneficial
Interest
22,595,650
Shares Note 3
—
5.43% 8 September 2027
Chengdu
Excelland
Beneficial
Interest
53,188,450
Shares Note 4
—
12.77% 8 September 2027
Mr. GU
Zhenjiang
Beneficial
Interest
16,035,600
Shares
—
3.85% 8 September 2027
Mr. LIU Dazhi
Beneficial
Interest
10,790,150
Shares
—
2.59% 8 September 2027
Mr. LUO Pei
Beneficial
Interest
4,508,350
Shares
—
1.08% 8 September 2027
Mr. XIA Ge
Beneficial
Interest
3,389,400
Shares
—
0.82% 8 September 2027
Subtotal
124,033,000
Shares
—
29.79%
Notes:
1.
For illustrative purposes only, this subsection lists only those members of the Single Largest
Group of Shareholders who hold Shares directly in the Company. Pursuant to the Hong Kong
Underwriting Agreement, each member of the Single Largest Group of Shareholders (namely,
Mr. LU Ying, Chengdu Excelland, Mr. GU Zhenjiang, Mr. LIU Dazhi, Mr. LUO Pei, Mr. XIA
Ge, Youdi Ruifeng (Beijing) Co., Ltd. (優地瑞峰(北京)有限公司), Excelland Hong Kong
Holdings Limited (優地香港控股有限公司), EAGLE FIELD Holdings Limited (鷹田控股有限
公司) and Eagle Field Platform) has undertaken to each of the Company, the Overall
Coordinators, the Joint Global Coordinators, the Joint Bookrunners, the Joint Lead Managers,
the Hong Kong Underwriters, the Capital Market Intermediaries and the Sole Sponsor that,
without the prior written consent of the Sole Sponsor and the Overall Coordinators (for
themselves and on behalf of the Hong Kong Underwriters) and unless in compliance with the
Listing Rules, he or it shall, and shall procure that the relevant registered holders of the
Shares in which he or it is beneficially interested shall, comply with the applicable lock-up
requirements.
For
further
details,
please
refer
to
the
section
headed
“Underwriting
—Undertakings Pursuant to the Hong Kong Underwriting Agreement — Undertakings by our
Single Largest Group of Shareholders” in the Prospectus.
2.
In accordance with the Hong Kong Underwriting Agreement, the required lock-up period
commences on the date of the Hong Kong Underwriting Agreement and ending on, and
including, the date that is 12 months after the Listing Date, i.e. 8 September 2027.
−10 −

<<<PAGE 11>>>
3.
As of the date of this announcement, Mr. LU Ying was the general partner of Eagle Field Platform and
held approximately 43.07% of partnership interest, who was responsible for its overall management and
was entitled to exercise the voting rights held by Eagle Field Platform at his full and absolute discretion.
As of the date of this announcement, there are two limited partners in Eagle Field Platform. Ms. LIU Wei
(the executive Director of the Company) owned approximately 28.63% of the limited partnership interests
in Eagle Field Platform, which will be subject to lock-up requirement under the Hong Kong Underwriting
Agreement. Mr. Chai owned approximately 28.30% of the limited partnership interests in Eagle Field
Platform.
4.
As of the date of this announcement, Chengdu Excelland was owned as to 98.52% by Youdi Ruifeng and
1.48% by Ms. LIU Wei. As of the date of this announcement, Youdi Ruifeng was wholly owned by
Excelland Holdings, which was in turn wholly owned by Eagle Field Holdings, the sole shareholder of
which was Mr. LU Ying. Each of Youdi Ruifeng, Excelland Holdings and Eagle Field Holdings will be
subject to lock-up requirement under the Hong Kong Underwriting Agreement.
Existing Shareholders (other than the Key Persons, the Pathfinder SIIs and the
Single Largest Group of Shareholders)
Name Note 1
Number of
Shares held
in the
Company
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
% of
shareholding
in the
Company
subject to
lock-up
undertakings
upon Listing
Last day subject to
the lock-up
undertakings Note 2
Jiujiang Youdi Technology
Industry Investment
Partnership (L.P.) (九江優地
科技產業投資合夥企業
(有限合夥)) (“Jiujiang
Youdi”)
21,875,000 H
Shares
7.75%
5.25% 8 September 2027
Beijing New Hengji
Investment Management
Group Co., Ltd. (北京新恒基
投資管理集團有限公司)
(“New Hengji Investment”)
20,378,050 H
Shares
7.22%
4.89% 8 September 2027
Wuhan Zhongbang
Hongxiang Equity
Investment Partnership (L.P.)
(武漢眾邦鴻翔股權投資合夥
企業(有限合夥))
(“Zhongbang Hongxiang”)
14,743,050 H
Shares
5.22%
3.54% 8 September 2027
Chongqing Guanda Holding
Group Co., Ltd. (重慶冠達控
股集團有限公司)
(“Chongqing Guanda”)
10,649,800 H
Shares
3.77%
2.56% 8 September 2027
−11 −

<<<PAGE 12>>>
Name Note 1
Number of
Shares held
in the
Company
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
% of
shareholding
in the
Company
subject to
lock-up
undertakings
upon Listing
Last day subject to
the lock-up
undertakings Note 2
Yangzhou Huajian
Chengding Equity
Investment Partnership (L.P.)
(揚州市華建誠鼎股權投資合
夥企業(有限合夥))
(“Huajian Chengding”)
9,260,650 H
Shares
3.28%
2.22% 8 September 2027
Wuxi Shangwei Venture
Capital Partnership (L.P.)
(無錫尚惟創業投資合夥企業
(有限合夥)) (“Wuxi
Shangwei”)
8,350,300 H
Shares
2.96%
2.01% 8 September 2027
Guizhou Guiyang Big Data
Science and Innovation City
Industry Development
Investment Fund Partnership
(L.P.) (貴州貴陽大數據科創
城產業發展投資基金合夥企
業(有限合夥)) (“Guiyang
Innovation City”)
7,656,250 H
Shares
2.71%
1.84% 8 September 2027
Suzhou Wuzhong Suodao
Heshi Industrial Investment
Partnership (L.P.) (蘇州吳中
索道合勢產業投資合夥企業
(有限合夥)) (“Wuzhong
Suodao”)
7,435,400 H
Shares
2.63%
1.79% 8 September 2027
Chaohu High Quality
Development Equity
Investment Partnership (L.P.)
(巢湖市高質量發展股權投資
合夥企業(有限合夥))
(“Chaohu High Quality”)
6,235,250 H
Shares
2.21%
1.50% 8 September 2027
Wuxi Fengling No.1 Venture
Capital Partnership (L.P.)
(無錫豐瓴壹號創業投資合夥
企業(有限合夥)) (“Wuxi
Fengling”)
5,556,250 H
Shares
1.97%
1.33% 8 September 2027
−12 −

<<<PAGE 13>>>
Name Note 1
Number of
Shares held
in the
Company
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
% of
shareholding
in the
Company
subject to
lock-up
undertakings
upon Listing
Last day subject to
the lock-up
undertakings Note 2
Jiaxing Suodao Boshi Equity
Investment Partnership (L.P.)
(嘉興索道搏勢股權投資合夥
企業(有限合夥)) (“Jiaxing
Suodao”)
5,351,150 H
Shares
1.90%
1.29% 8 September 2027
Zhaoqing Xijiang Innovation
and Entrepreneurship Fund
Partnership (L.P.) (肇慶市西
江創新創業基金合夥企業
(有限合夥)) (“Xijiang
Innovation”)
5,180,921
Shares
—
1.24% 8 September 2027
Chengdu Ceyuan Detou
Qingyue Xingguang Venture
Capital Partnership (L.P.)
(成都策源德投青樾星光創業
投資合夥企業有限合夥))
(“Chengdu Ceyuan”)
4,921,875
Shares
—
1.18% 8 September 2027
Hunan Wuba Qianmo Equity
Investment Fund Partnership
(L.P.) (湖南五八阡陌股權投
資基金合夥企業(有限合夥))
(“Wuba Qianmo”)
4,630,150 H
Shares
1.64%
1.11% 8 September 2027
Jianhu Yuehu Emerging
Industry Fund Partnership
(L.P.) (建湖縣悅湖新興產業
基金合夥企業(有限合夥)
(“Yuehu Industry Fund”)
4,375,000 H
Shares
1.55%
1.05% 8 September 2027
BTG Hotels (Group) Co.,
Ltd. (北京首旅酒店(集團)股
份有限公司) (“BTG Hotels
Group”)
3,971,100 H
Shares
1.41%
0.95% 8 September 2027
Yinfeng Rongjin (Beijing)
Investment Management Co.,
Ltd. (銀豐融金(北京)投資管
理有限公司(“Yinfeng
Rongjin”)
3,628,450 H
Shares
1.29%
0.87% 8 September 2027
−13 −

<<<PAGE 14>>>
Name Note 1
Number of
Shares held
in the
Company
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
% of
shareholding
in the
Company
subject to
lock-up
undertakings
upon Listing
Last day subject to
the lock-up
undertakings Note 2
Wuxi Economic
Development Zone Xinzhi
Venture Capital Partnership
(L.P.) (無錫經開區新智創業
投資合夥企業(有限合夥)
(“Wuxi Xinzhi”)
3,340,400 H
Shares
1.18%
0.80% 8 September 2027
Mr. ZHOU Liang
2,732,450 H
Shares
0.97%
0.66% 8 September 2027
Suzhou Yishang Equity
Investment Partnership (L.P.)
(蘇州毅商股權投資合夥企業
(有限合夥)) (“Yishang
Equity”)
2,627,100 H
Shares
0.93%
0.63% 8 September 2027
Anhui Xunfei Yunchuang
Science and Technology Co.,
Ltd. (安徽訊飛雲創科技有限
公司) (“Xunfei
Yunchuang”)
2,529,450 H
Shares
0.90%
0.61% 8 September 2027
Mr. SHEN Gefei
1,904,700 H
Shares
0.67%
0.46% 8 September 2027
Pernod Ricard Hong Kong
Limited (保樂力加香港有限
公司) (“Pernod Ricard”)
1,897,350 H
Shares
0.67%
0.46% 8 September 2027
Shenzhen Qianhai
Shengyangsheng Financial
Services Co., Ltd. (深圳前海
升陽升金融服務有限公司)
(“Qianhai
Shengyangsheng”)
1,558,900 H
Shares
0.55%
0.37% 8 September 2027
Huazhu Investment
(Shanghai)Co., Ltd.
(華住投資(上海)有限公司)
(“Huazhu Investment”)
1,192,800 H
Shares
0.42%
0.29% 8 September 2027
Green Tree Inns Hotel
(China) Management Co.,
Ltd. (格林豪泰酒店(中國)有
限公司) (“GreenTree”)
1,192,800 H
Shares
0.42%
0.29% 8 September 2027
−14 −

<<<PAGE 15>>>
Name Note 1
Number of
Shares held
in the
Company
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
% of
shareholding
in the
Company
subject to
lock-up
undertakings
upon Listing
Last day subject to
the lock-up
undertakings Note 2
Zhongjiang High-Tech
Industrial Development Co.,
Ltd. (中江高新產業開發有限
公司) (“Zhongjiang
High-Tech”)
328,125 H
Shares
0.12%
0.08% 8 September 2027
Ms. SHAO Jing
280,000 H
Shares
0.10%
0.07% 8 September 2027
Deyang Kaizhou Investment
and Development Co., Ltd.
(德陽市凱州投資開發有限責
任公司) (“Deyang
Kaizhou”)
218,750 H
Shares
0.08%
0.05% 8 September 2027
Ms. ZHANG Min
185,150 H
Shares
0.07%
0.04% 8 September 2027
Mr. CAI Yi
140,000 H
Shares
0.05%
0.03% 8 September 2027
Ms. DANG Bin
140,000 H
Shares
0.05%
0.03% 8 September 2027
Subtotal
164,466,621
Shares
(including
154,363,825
H Shares)
54.69%
39.50%
Notes:
1.
For details of the background of relevant Shareholders, please refer to the section headed
“History, Development and Corporate Structure”.
2.
Pursuant to the applicable PRC laws, all existing Shareholders (including the Pre-IPO
Investors) are not permitted to dispose of any of the Shares held by them within 12 months
following the Listing Date.
−15 −

<<<PAGE 16>>>
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
% of total
issued H
Shares after
the Global
Offering
subject to
lock-up
undertakings
upon Listing
% of
shareholding
in the
Company
subject to
lock-up
undertakings
upon Listing
Last day subject to
the lock-up
undertakings Note 2
SensePower
1,089,600
H Shares
0.39%
0.26% 8 June 2027
CYGG
544,800
H Shares
0.19%
0.13% 8 June 2027
Total
1,634,400
Shares
(including
1,634,400
H Shares)
0.58%
0.39%
Notes:
1.
In accordance with the relevant cornerstone investment agreements, the required
lock-up ends immediately upon the lapse of nine months after the Listing Date (i.e. on
8 June 2027). The Cornerstone Investors will cease to be prohibited from disposing
of or transferring H Shares subscribed for pursuant to the relevant cornerstone
investment agreements after the indicated date.
PLACEE CONCENTRATION ANALYSIS
Placees Note 1
Number of
H Shares
allotted
Allotment as
% of
International
Offering
Allotment
as % of
total Offer
Shares
Number of
Shares
held upon
Listing
% of total
issued
share
capital
upon
Listing
Top 1
10,276,800
24.34%
22.84%
10,276,800
2.47%
Top 5
28,856,800
68.35%
64.13%
28,856,800
6.93%
Top 10
39,537,600
93.65%
87.86%
39,537,600
9.50%
Top 25 Note 2
42,205,800
99.97%
93.79%
68,710,950
16.50%
Notes:
1.
Ranking of placees is based on the number of H Shares allotted to the placees.
2.
For the purpose of the placee concentration analysis, (i) all Shares held by SensePower and
Jiujiang Youdi are aggregated; (ii) all Shares held by CYGG and Wuba Qianmo are aggregated.
−16 −

<<<PAGE 17>>>
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders Note 1
Number of
H Shares
allotted
Allotment as
% of
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
% of total
issued H
Shares
capital
upon
Listing
Number of
Shares held
upon
Listing
Top 1
0
0.00%
0.00%
29,775,900
10.55%
29,775,900
Top 5 Note 2
1,089,600
2.58%
2.42% 126,211,450
44.72% 126,211,450
Top 10 Note 3
11,366,400
26.92%
25.26% 188,388,700
66.75% 188,388,700
Top 25 Note 4
37,201,800
88.12%
82.67% 260,239,300
92.21% 260,239,300
Notes:
1.
Ranking of H Shareholders is based on the number of H Shares held by H Shareholders upon
Listing.
2.
For the purpose of the H shareholder concentration analysis, all Shares held by SensePower and
Jiujiang Youdi are aggregated.
3.
For the purpose of the H shareholders concentration analysis, all Shares held by Wuxi Fengling,
Wuxi Shangwei and Wuxi Xinzhi are aggregated.
4.
For the purpose of the H shareholder concentration analysis, all Shares held by CYGG and Wuba
Qianmo are aggregated.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders Note 1
Number of
H Shares
allotted
Allotment as
% of
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
Number of
Shares held
upon
Listing
% of total
issued
share
capital
upon
Listing
Top 1 Note 2
0
0.00%
0.00%
0 124,033,000
29.79%
Top 5 Note 3
1,089,600
2.58%
2.42% 105,833,400 229,866,400
55.21%
Top 10 Note 4
11,366,400
26.92%
25.26% 179,128,050 303,161,050
72.81%
Top 25 Note 5
30,491,200
72.22%
67.76% 250,796,250 384,932,046
92.45%
Notes:
1.
Ranking of Shareholders is based on the number of Shares (of H Shares and unlisted Shares) held
by the Shareholders upon Listing.
2.
For the purpose of the shareholders concentration analysis, all Shares held by the Single Largest
Group of Shareholders are aggregated.
3.
For the purpose of the shareholder concentration analysis, all Shares held by SensePower and
Jiujiang Youdi are aggregated.
4.
For the purpose of the shareholders concentration analysis, all Shares held by Wuxi Fengling,
Wuxi Shangwei and Wuxi Xinzhi are aggregated.
5.
For the purpose of the shareholder concentration analysis, all Shares held by CYGG and Wuba
Qianmo are aggregated.
−17 −

<<<PAGE 18>>>
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid
applications made by the public will be conditionally allocated on the basis set out
below:
NO. OF
SHARES
APPLIED
FOR
NO. OF VALID
APPLICATIONS BASIS OF ALLOTMENT / BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED OF
THE TOTAL
NO. OF
SHARES
APPLIED FOR
POOL A
200
11,610 2,844 out of 11,610 to receive 200 Shares
24.50%
400
4,090 1,014 out of 4,090 to receive 200 Shares
12.40%
600
1,527 379 out of 1,527 to receive 200 Shares
8.27%
800
729 182 out of 729 to receive 200 Shares
6.24%
1,000
1,328 332 out of 1,328 to receive 200 Shares
5.00%
1,200
491 123 out of 491 to receive 200 Shares
4.18%
1,400
343 86 out of 343 to receive 200 Shares
3.58%
1,600
318 80 out of 318 to receive 200 Shares
3.14%
1,800
235 60 out of 235 to receive 200 Shares
2.84%
2,000
1,917 490 out of 1,917 to receive 200 Shares
2.56%
3,000
616 158 out of 616 to receive 200 Shares
1.71%
4,000
499 128 out of 499 to receive 200 Shares
1.28%
5,000
579 149 out of 579 to receive 200 Shares
1.03%
6,000
364 94 out of 364 to receive 200 Shares
0.86%
7,000
220 57 out of 220 to receive 200 Shares
0.74%
8,000
219 57 out of 219 to receive 200 Shares
0.65%
9,000
110 29 out of 110 to receive 200 Shares
0.59%
10,000
779 206 out of 779 to receive 200 Shares
0.53%
20,000
413 110 out of 413 to receive 200 Shares
0.27%
30,000
221 59 out of 221 to receive 200 Shares
0.18%
40,000
166 45 out of 166 to receive 200 Shares
0.14%
50,000
113 31 out of 113 to receive 200 Shares
0.11%
60,000
96 27 out of 96 to receive 200 Shares
0.09%
70,000
68 20 out of 68 to receive 200 Shares
0.08%
80,000
64 19 out of 64 to receive 200 Shares
0.07%
90,000
44 14 out of 44 to receive 200 Shares
0.07%
100,000
176 57 out of 176 to receive 200 Shares
0.06%
150,000
133 44 out of 133 to receive 200 Shares
0.04%
200,000
92 31 out of 92 to receive 200 Shares
0.03%
250,000
89 30 out of 89 to receive 200 Shares
0.03%
27,649 Total number of Pool A successful
applicants: 6,955
−18 −

<<<PAGE 19>>>
NO. OF
SHARES
APPLIED
FOR
NO. OF VALID
APPLICATIONS BASIS OF ALLOTMENT / BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED OF
THE TOTAL
NO. OF
SHARES
APPLIED FOR
POOL B
300,000
111 4,800 Shares plus 36 out of 111 to receive
additional 200 Shares
1.62%
350,000
24 4,800 Shares plus 8 out of 24 to receive
additional 200 Shares
1.39%
400,000
30 4,800 Shares plus 11 out of 30 to receive
additional 200 Shares
1.22%
500,000
18 4,800 Shares plus 7 out of 18 to receive
additional 200 Shares
0.98%
600,000
18 4,800 Shares plus 8 out of 18 to receive
additional 200 Shares
0.81%
700,000
10 4,800 Shares plus 5 out of 10 to receive
additional 200 Shares
0.70%
800,000
13 4,800 Shares plus 7 out of 13 to receive
additional 200 Shares
0.61%
900,000
7 4,800 Shares plus 4 out of 7 to receive
additional 200 Shares
0.55%
1,000,000
3 4,800 Shares plus 2 out of 3 to receive
additional 200 Shares
0.49%
1,125,000
50 5,000 Shares
0.44%
284 Total number of Pool B successful
applicants: 284
As of the date of this announcement, the relevant subscription monies previously
deposited in the designated nominee accounts have been remitted back to the
accounts of all HKSCC participants. Investors should contact their relevant brokers
for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or
in respect of which consent has been obtained, the Company has complied with the
Listing Rules and guidance materials in relation to the placing, allotment and listing
of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by
the placees or the public (as the case may be) directly or indirectly for each Offer
Share subscribed for or purchased by them was the same as the Offer Price in
addition to any brokerage, AFRC transaction levy, SFC transaction levy and Stock
Exchange trading fee payable.
−19 −

<<<PAGE 20>>>
The Directors and the Overall Coordinators confirm that at least 50% of the total
number of the Offer Shares have been allocated to and taken up by independent price
setting investors in compliance with Rule 18C.08 of the Listing Rules.
The Directors further confirm that at least 20% of the issued share capital of the
Company will be held by sophisticated independent investors at the time of Listing
in compliance with Chapter 2.5 of the Guide for New Listing Applicants.
OTHERS / ADDITIONAL INFORMATION
Reallocation
As the International Offer Shares are undersubscribed and the Hong Kong Public
Offering has been over-subscribed by more than 140.02 times of the total number of
Offer
Shares
initially
available
under
the
Hong
Kong
Public
Offering,
the
reallocation procedure as disclosed in the section headed “Structure of the Global
Offering — The Hong Kong Public Offering — Reallocation” in the Prospectus has
been applied.
The number of Offer Shares initially available under the Hong Kong Public Offering
is 2,250,000 H Shares, representing approximately 5% of the total number of Offer
Shares initially available under the Global Offering. As a result of such reallocation,
the final number of Offer Shares under the Hong Kong Public Offering is adjusted
to 2,781,800 Offer Shares, representing approximately 6.18% of the total number of
Offer Shares initially available under the Global Offering.
Placing to existing shareholders and/or its close associates with a prior waiver
under Rule 10.04 and consent under paragraph 1C(2) of the Placing Guidelines
The Company has applied for a waiver under Rule 10.04 of the Listing Rules and a
consent under paragraph 1C(2) of Appendix F1 to the Listing Rules, in respect of the
proposed subscription by SensePower and CYGG (collectively, the “Existing
Shareholder CI Participants”) for Offer Shares as cornerstone investors under the
International Offering. The Stock Exchange has agreed to grant the requested waiver
and consent subject to the conditions that:
(a) the allocation to the Existing Shareholder CI Participants will not affect the
Company’s ability to satisfy relevant requirements under Rules 19A.13A(1),
18C.08 and 19A.13C(1) of the Listing Rules, respectively;
(b) the requirement of minimum prescribed percentage of public shareholders as
required by Rule 8.08(1) of the Listing Rules will be fulfilled upon the Listing;
−20 −

<<<PAGE 21>>>
(c) the Company and the Sole Sponsor confirm that no preferential treatment has
been, or will be, directly or indirectly, given to the Existing Shareholder CI
Participants by virtue of their relationship with the Company in connection with
any allocation under the Global Offering, other than the preferential treatment
of assured entitlement at the Offer Price under their respective cornerstone
investments, and no other preferential terms have been or will be granted to them
by virtue of their existing shareholder status; and that the terms of the
cornerstone investment agreement entered into by the two Existing Shareholder
CI Participants are substantially the same as each other;
(d) details of the subscription of the Offer Shares by the Existing Shareholder CI
Participants
as
cornerstone
investors
under
the
International
Offering
is
disclosed in the Prospectus, and details of the final allocation will be disclosed
in the this allotment results announcement.
For details of the allocations of Offer Shares to Existing Shareholder CI Participants,
please refer to the section headed “Allotment Results Details — International
Offering — Allotees with Waivers/Consents Obtained” in this announcement.
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong
Limited
and
Hong
Kong
Securities
Clearing
Company
Limited
take
no
responsibility for the contents of this announcement, make no representation as to
its accuracy or completeness and expressly disclaim any liability whatsoever for
any loss howsoever arising from or in reliance upon the whole or any part of the
contents of this announcement.
This announcement is not for release, publication, distribution, directly or
indirectly, in or into the United States (including its territories and possessions,
any state of the United States and the District of Columbia). This announcement
does not, and is not intended to, constitute or form a part of any offer to sell or
solicitation to purchase or subscribe for any securities in the United States. The
Offer Shares have not been, and will not be, registered under the United States
Securities Act of 1933, as amended (the “U.S. Securities Act”) or securities law
of any state or other jurisdiction of the United States and may not be offered, sold,
pledged or otherwise transferred within the United States, except pursuant to an
available exemption from, or in a transaction not subject to, the registration
requirements of the U.S. Securities Act. There will be no public offer of the Offer
Shares in the United States.
The Offer Shares are being offered and sold solely outside the United States in
offshore transactions in reliance on Regulation S under the U.S. Securities Act.
−21 −

<<<PAGE 22>>>
This announcement is for information purposes only and does not constitute an
invitation
or
offer
to
acquire,
purchase
or
subscribe
for
securities.
This
announcement is not a prospectus. Potential investors should read the Prospectus
dated 31 August 2026 issued by the Company for detailed information about the
Global Offering described below before deciding whether or not to invest in the H
Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Sole Sponsor and the
Overall
Coordinator
(for
themselves
and
on
behalf
of
the
Hong
Kong
Underwriters) shall be entitled to terminate their obligations under the Hong
Kong Underwriting Agreement with immediate effect upon the occurrence of any
of the events set out in the section headed “Underwriting — Underwriting
Arrangements and Expenses — Hong Kong Public Offering — Grounds for
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time)
on the Listing Date (which is currently expected to be on Wednesday, 9 September
2026).
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering and based on the Offer
Price of HK$14.45 per H Share:
(1) 282,232,625 H Shares represents approximately 67.78% of the total issued share
capital of the Company will be counted towards the public float for the purpose
of Rule 19A.13A of the Listing Rules, which is higher than the prescribed
percentage of H Shares required to be held in public hands of 24.93% under Rule
19A.13A of the Listing Rules.
(2) excluding the Offer Shares to be allocated to the Cornerstone Investors that are
subject to a lock-up period of nine months following the Listing Date and the H
Shares to be converted from Unlisted Shares that are subjected to a lock-up
period of 12 months following the Listing Date, the Company’s H Shares to be
counted towards the free float upon Listing will be 43,365,600 H Shares. Based
on the Offer Price of HK$14.45 per H Share, the free float of the Company
represents approximately 10.42% of the total issued share capital of the
Company at the time of Listing with a market value of approximately
HK$626.63 million. Accordingly, the Company will satisfy the free float
requirement under Rule 19A.13C(1) of the Listing Rules.
The Directors confirm that, immediately following completion of the Global
Offering: (i) no placee will, individually, be placed more than 10% of the enlarged
issued share capital of the Company immediately after the Global Offering; (ii) there
will not be any new substantial Shareholder immediately after the Global Offering;
−22 −

<<<PAGE 23>>>
(iii) the three largest public Shareholders do not hold more than 50% of the H Shares
in public hands at the time of Listing in compliance with Rules 8.08(3) and 8.24 of
the Listing Rules; and (iv) there will be at least 300 Shareholders at the time of
Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
H Share certificates will only become valid evidence of title at 8:00 a.m. on
Wednesday, 9 September 2026 (Hong Kong time), provided that the Global Offering
has become unconditional and the right of termination described in the section
headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong
Public Offering - Grounds for Termination” in the Prospectus has not been exercised.
Investors who trade H Shares on the basis of publicly available allocation details
prior to the receipt of H Share certificates or prior to the H Share certificates
becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. in
Hong Kong on Wednesday, 9 September 2026 (Hong Kong time), it is expected that
dealings in the H Shares on the Stock Exchange will commence at 9:00 a.m. on
Wednesday, 9 September 2026 (Hong Kong time). The H Shares will be traded in
board lots of 200 H Shares each and the stock code of the H Shares will be 3231.
By order of the Board
Excelland Robotics (Wuxi) Co. Ltd.
(優地機器人(無錫)股份有限公司)
Mr. LU Ying
Chairman, Executive Director and Chief Executive Officer
Hong Kong, 8 September 2026
As at the date of this announcement, the Board comprises (i) Mr. LU Ying, Mr. GU Zhenjiang, Ms. LIU
Wei and Ms. NIU Yue as executive Directors; (ii) Mr. ZHANG Yufu as non-executive Director; (iii) Mr.
ZOU Bo, Mr. GUO Huaijiang and Mr. CHEUNG Yikman, as the proposed independent non-executive
Directors.
−23 −
