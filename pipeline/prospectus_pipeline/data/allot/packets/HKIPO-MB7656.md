# 配发结果公告抽取任务：7656.HK Reconova Technologies Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**07/07/2026 21:41**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0707/2026070701895.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"7656.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined herein, capitalized terms used in this announcement shall have the
same meanings as those defined in the Hong Kong prospectus dated June 29, 2026 (the
“Prospectus”) Reconova Technologies Co., Ltd. (廈門瑞為信息技術股份有限公司) (the
“Company”).
This announcement is for information purposes only and does not constitute an invitation or
offer to acquire, purchase or subscribe for any securities. This announcement is not a
prospectus. Potential investors should read the Prospectus for detailed information about
the Global Offering described below before deciding whether or not to invest in the Offer
Shares. Any investment decision in relation to the Offer Shares should be taken solely in
reliance on the information provided in the Prospectus.
This announcement does not constitute an offer to sell or the solicitation of an offer to buy
nor shall there be any sale of Offer Shares in any jurisdiction in which such offer,
solicitation or sales would be unlawful. This announcement is not for release, publication,
distribution, directly or indirectly, in or into the United States for sale or solicitation to
purchase or subscribe for securities in the United States or any other jurisdictions. The
Offer Shares have not been, and will not be, registered under the United States Securities
Act of 1933, as amended, supplemented or modified from time to time (the “U.S. Securities
Act”) or any state securities law of the United States and may not be offered, sold, pledged,
transferred or delivered within the United States, except pursuant to an exemption from, or
in a transaction not subject to, the registration requirements of the U.S. Securities Act and
state securities laws of the United States. The Offer Shares are being offered and sold
outside of the United States as offshore transactions in accordance with Regulation S under
the U.S. Securities Act and the applicable laws of each jurisdiction where those offers and
sales occur. There will not be and is not currently intended to be any public offering of
securities of the Company in the United States.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms
and conditions set out in the Prospectus. The Hong Kong Offer Shares will not be offered to
any person who is outside Hong Kong and/or not resident in Hong Kong. Potential investors
of the Offer Shares should note that the Joint Sponsor-Overall Coordinators (for
themselves and on behalf of the other Hong Kong Underwriters) shall be entitled to
terminate the Hong Kong Underwriting Agreement with immediate effect upon the
occurrence of any of the events set out in “Underwriting — Underwriting Arrangements
and Expenses — The Hong Kong Public Offering — Grounds for Termination” in the
Prospectus at any time at or prior to 8: 00 a.m. on the Listing Date.
– 1 –

<<<PAGE 2>>>
Reconova Technologies Co., Ltd.
廈門瑞為信息技術股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Total number of Offer Shares under
the Global Offering
:
28,087,000 H Shares
Number of Hong Kong Offer Shares
:
5,617,400 H Shares (after reallocation)
Number of International Offer Shares
:
22,469,600 H Shares (after reallocation)
Offer Price
:
HK$21.66 per H Share, plus brokerage of
1%, SFC transaction levy of 0.0027%,
Stock Exchange trading fee of 0.00565%
and AFRC transaction levy of 0.00015%
(payable in full on application and subject
to refund on final pricing)
Nominal value
:
RMB0.20 per H Share
Stock code
:
7656
Joint Sponsors, Joint Sponsor-Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers
– 2 –

<<<PAGE 3>>>
RECONOVA TECHNOLOGIES CO., LTD.
廈門瑞為信息技術股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the
same meanings as those defined in the prospectus dated June 29, 2026 (the “Prospectus”)
issued by Reconova Technologies Co., Ltd. (the “Company”).
Warning: In view of high concentration of shareholding in a small number of
Shareholders, H Shareholders and prospective investors should be aware that the price
of the H Shares could move substantially even with a small number of H Shares traded
and should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company Information
Stock code
7656
Stock short name
RECONOVA
Dealings commencement date
July 8, 2026*
*
see note at the end of the announcement
Price Information
Offer Price
HK$21.66
Offer Shares and Share Capital
Number of Offer Shares
28,087,000
Number of Offer Shares in Hong Kong Public
Offering (after reallocation)
5,617,400
Number of Offer Shares in International Offering
(after reallocation)
22,469,600
Number of issued shares upon Listing
305,292,905
Proceeds
Gross proceeds (Note)
HK$608.4 million
Less: Estimated listing expenses payable based on
Offer Price
HK$(79.3) million
Net proceeds
HK$529.1 million
Note: Gross proceeds refers to the amount to which the Company is entitled to receive.
For details of the use of proceeds, please refer to the section headed “Future Plans and
Use of Proceeds” of the Prospectus.
– 3 –

<<<PAGE 4>>>
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
Number of valid applications
169,551
Number of successful applications
23,352
Subscription level
3,646.06 times
Claw-back triggered
Yes
Number of Offer Shares initially available under the
Hong Kong Public Offering
1,404,400
Final number of Offer Shares under the Hong Kong
Public Offering (after reallocation)
5,617,400
% of Offer Shares under the Hong Kong Public
Offering to the Global Offering
20.00%
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering,
investors can refer to http://www.hkeipo.hk/iporesult to perform a search by name or
identification number or http://www.hkeipo.hk/iporesult for the full list of allottees.
INTERNATIONAL OFFERING
Number of placees
105
Subscription Level
3.08 times
Number of Offer Shares initially available under the
International Offering
26,682,600
Final number of Offer Shares under the International
Offering (after reallocation)
22,469,600
% of Offer Shares under the International Offering to
the Global Offering
80.00%
The Directors confirm that, to the best of their knowledge, information and belief, save for,
a consent under paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing
Guidelines”) granted by the Stock Exchange to permit the Company to place certain H
Shares in the International Offering to a close associate of an existing Shareholder, (i)
none of the Offer Shares subscribed by the placees and the public have been financed
directly or indirectly by the Company, any of the Directors, chief executive, controlling
shareholders, substantial shareholders, existing shareholders of the Company or any of its
subsidiaries or their respective close associates; and (ii) none of the placees and the public
who have purchased the Offer Shares are accustomed to taking instructions from the
Company, any of the Directors, chief executive of the Company, controlling shareholders,
substantial shareholders, existing shareholders of the Company or any of its subsidiaries or
their respective close associates in relation to the acquisition, disposal, voting or other
disposition of Shares registered in his/her/its name or otherwise held by him/her/it.
– 4 –

<<<PAGE 5>>>
The placees in the International Offering include the following:
Allottee with Consent Obtained
Investor
Number of
Offer Shares
allocated
% of Offer
Shares
% of total H
Shares after
the Global
Offering
% of total
issued share
capital after
the Global
Offering
Relationship
Allottee with consent under paragraph 1C(2) of the Placing Guidelines in relation to subscription for H
Shares by a close associate of an existing minority shareholder as placee(Note 1)
Hong Kong BoYue
International Investment
Fund Co., Limited
(“Hong Kong BoYue”)
(Note 2)
5,500,000
19.58%
2.01%
1.80%
A close
associate of
an existing
Shareholder
Notes:
1.
See section headed “Others/Additional Information — Placing to a close associate of an existing
Shareholder with a consent under paragraph 1C(2) of the Placing Guidelines” in this announcement
for further details.
2.
Hong Kong BoYue is a wholly-owned subsidiary of Shenzhen BoYue International Investment Fund
Co., Ltd. (深圳博約國際投貸基金有限公司) (“Shenzhen BoYue”). The fund manager of Shenzhen
BoYue is Shenzhen BoYue Capital Management Co., Ltd. (深圳博約投貸資本管理有限公司), which is
ultimately controlled by State-owned Assets Supervision and Administration Commission of the
People’s
Government
of
Shenzhen
Municipality
(深圳市人民政府國有資產監督管理委員會)
(“Shenzhen SASAC”). Shenzhen SASAC is the ultimate controller of the managing general partner
and fund manager of Shenzhen Investment Holdings Capital, an existing Shareholder of the Company.
As such, Hong Kong BoYue is a close associate of an existing Shareholder.
– 5 –

<<<PAGE 6>>>
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
Number of H
Shares held in
the Company
subject to
lock-up
undertakings
upon Listing
% of
shareholding
in the
Company
subject to
lock-up upon
Listing
Last day subject to
the lock-up
undertakings(Note 1)
ZHAN Donghui
(“Mr. Zhan”)
Founder, chairman
of the Board and
executive Director
76,884,535
76,884,535
25.18%
July 7, 2027
SU Xiaosheng
Chief scientist
12,047,500
12,047,500
3.95%
July 7, 2027
HAN Songguang
Executive Director
and general
manager of
intelligent vehicle
link business unit
3,781,625
3,781,625
1.24%
July 7, 2027
Shenzhen Ruiyuan
Technology Centre
Partnership (Limited
Partnership) (深圳瑞元
科技中心合夥企業（有限
合夥）) (“Ruiyuan
Technology
Partnership”)(Note 2)
Share incentive
platform controlled
by Mr. Zhan
10,827,935
10,827,935
3.55%
July 7, 2027
Shenzhen Ruiyuan
Technology Centre
Partnership (Limited
Partnership) (深圳瑞遠
科技中心合夥企業（有限
合夥）) (“Shenzhen
Ruiyuan Technology
Partnership”)(Note 2)
Share incentive
platform controlled
by Mr. Zhan
10,827,935
10,827,935
3.55%
July 7, 2027
Shenzhen Ruiyitong
Technology Partnership
Enterprise (Limited
Partnership) (深圳瑞億
瞳科技合夥企業（有限合
夥）) (“Ruiyitong
Technology
Partnership”)(Note 2)
Share incentive
platform controlled
by Mr. Zhan
2,733,290
2,733,290
0.90%
July 7, 2027
Total
117,102,820
117,102,820
38.37%
– 6 –

<<<PAGE 7>>>
Name
Capacity
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
% of
shareholding
in the
Company
subject to
lock-up upon
Listing
Last day subject to
the lock-up
undertakings(Note 1)
Notes:
1.
The lock-up period commencing on the date by reference to which disclosure of its shareholding is made in the
Prospectus and ending on the date which is 12 months from the Listing Date, i.e. July 7, 2027.
2.
As of the date of this announcement, Mr. Zhan (the founder) is the sole general partner of Ruiyuan Technology
Partnership, Shenzhen Ruiyuan Technology Partnership and Ruiyitong Technology Partnership. Therefore, such
partnership interests held by Mr. Zhan shall be subject to disposal restrictions pursuant to Rule 18C.14 of the
Listing Rules.
Pathfinder SIIs (as defined under Rule 18C.14 of the Listing Rules)
Name(Note 1)
Capacity
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
% of
shareholding
in the
Company
subject to
lock-up upon
Listing
Last day subject to
the lock-up
undertakings(Note 2)
Nanjing SAIF Equity
Investment Fund (L.P.)
(“Nanjing SAIF”)
Pathfinder SII
8,101,395
8,101,395
2.65%
January 7, 2027
Nantong Merchants
Jianghai Industry
Development Fund
Partnership (L.P.)
(“Nantong Jianghai
Fund”)
Pathfinder SII
9,242,730
9,242,730
3.03%
January 7, 2027
Sichuan Cooperation
Innovation Fund
Pathfinder SII
7,326,270
7,326,270
2.40%
January 7, 2027
Hangzhou Fuyang
SAIF Yi’an Equity
Investment Partnership
(Limited Partnership)
(“SAIF Yi’an”)
(together with Nanjing
SAIF, the “Sai Fu
Investors”)
Pathfinder SII
2,012,530
2,012,530
0.66%
January 7, 2027
– 7 –

<<<PAGE 8>>>
Name(Note 1)
Capacity
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
% of
shareholding
in the
Company
subject to
lock-up upon
Listing
Last day subject to
the lock-up
undertakings(Note 2)
Greenland Financial
Holdings Group
Company Limited
(“Greenland Financial
Holdings Group”)
Pathfinder SII
14,060,463
10,784,332
4.61%
January 7, 2027
Shanghai Hongyu
Aviation Industry
Equity Investment
Partnership (Limited
Partnership) (“Hon
Universe Aviation
Industry Fund”)
(together with Sichuan
Cooperation
Innovation Fund, the
“Shanghai SASAC
Investors”)
Pathfinder SII
9,717,910
9,717,910
3.18%
January 7, 2027
Total
50,461,298
47,185,167
16.53%
Notes:
1.
Each of Nanjing SAIF, Nantong Jianghai Fund, Sichuan Cooperation Innovation Fund, SAIF Yi’an, Greenland
Financial Holdings Group and Hon Universe Aviation Industry Fund is a pathfinder SII of the Company as
defined under Chapter 2.5 of the Guide for New Listing Applicants. Please refer to the section headed “History,
Development and Corporate Structure — Capitalisation of our Company” in the Prospectus for further details.
2.
In accordance with Rule 18C.14(2) of the Listing Rules, the required lock-up period commences on the date by
reference to which disclosure of its shareholding is made in the Prospectus and ends on the date which is six
months from the Listing Date, i.e. January 7, 2027. In addition to the lock-up requirement under Rule 18C.14(2)
of the Listing Rules, all existing Shareholders shall not dispose of any of the Shares held by them within the 12
months following the Listing Date, i.e. July 7, 2027, as required under the applicable PRC laws.
– 8 –

<<<PAGE 9>>>
Controlling Shareholders
Name
Number of Shares
held in the
Company subject
to lock-up
undertakings upon
Listing
Number of H
Shares held in the
Company subject
to lock-up
undertakings upon
Listing
% of
shareholding in
the Company
subject to lock-up
upon Listing
Last day subject
to the lock-up
undertakingsNote 1
Mr. Zhan
76,884,535
76,884,535
25.18%
July 7, 2027
SU Xiaosheng
12,047,500
12,047,500
3.95%
July 7, 2027
CHI Chang
3,781,700
3,781,700
1.24%
July 7, 2027
HAN Songguang
3,781,625
3,781,625
1.24%
July 7, 2027
Ruiyuan Technology
Partnership
10,827,935
10,827,935
3.55%
July 7, 2027
Shenzhen Ruiyuan
Technology Partnership
10,827,935
10,827,935
3.55%
July 7, 2027
Ruiyitong Technology
Partnership
2,733,290
2,733,290
0.90%
July 7, 2027
Total
120,884,520
120,884,520
39.61%
Note:
1.
All existing Shareholders (including the Controlling Shareholders) shall not dispose of any of the
Shares held by them within 12 months following the Listing Date as required under the applicable
PRC laws.
Other Existing Shareholders
NameNote 1
Number of Shares
held in the
Company subject to
lock-up
undertakings upon
Listing
Number of H
Shares held in the
Company subject to
lock-up
undertakings upon
Listing
% of shareholding
in the Company
subject to
lock-up upon
Listing(Note 1)
Last day subject to
the lock-up
undertakings(Note 2)
Wuxi ST Zhihang
Investment Management
Centre (Limited
Partnership) (“SWLVC”)
16,857,145
16,857,145
5.52%
July 7, 2027
Tibet Score Race Equity
Investment Centre (L.P.)
(“TSREIC (L.P.)”)
16,161,845
11,313,292
5.29%
July 7, 2027
Intel Asia Pacific Research
and Development Ltd.
(“Intel”)
12,688,175
12,688,175
4.16%
July 7, 2027
CITICS Securities
Investment Co., Ltd.
(“CITIC Securities
Investment”)
8,101,395
8,101,395
2.65%
July 7, 2027
– 9 –

<<<PAGE 10>>>
NameNote 1
Number of Shares
held in the
Company subject to
lock-up
undertakings upon
Listing
Number of H
Shares held in the
Company subject to
lock-up
undertakings upon
Listing
% of shareholding
in the Company
subject to
lock-up upon
Listing(Note 1)
Last day subject to
the lock-up
undertakings(Note 2)
Shihezi Shangshi Growth of
Equity Investment
Partnership (LP) (“SSG”)
3,462,030
—
1.13%
July 7, 2027
Shangshi Growth
Acceleration (Hainan)
Venture Capital Fund
Partnership Enterprise
(Limited Partnership)
(“SSGA”)
4,050,700
—
1.33%
July 7, 2027
Hunan Xingxiang
Zhongzheng Xinying Equity
Investment Fund
Partnership (Limited
Partnership)
6,076,050
3,375,582
1.99%
July 7, 2027
Shenzhen Investment
Holdings Chuangzhi
Technology Private Equity
Venture Capital Fund
Partnership Enterprise
(Limited Partnership)
(“Shenzhen Investment
Holdings Capital”)
6,751,165
6,751,165
2.21%
July 7, 2027
Hualong Jincheng
Investment Co., Ltd.
(“Hualong Investment”)
5,698,910
5,698,910
1.87%
July 7, 2027
DAI Liyi
2,950,050
2,950,050
0.97%
July 7, 2027
Wuxi Hechuang High-tech
Equity Investment
Partnership Enterprise
(Limited Partnership)
(“Wuxi Hechuang
High-tech”)
2,522,640
2,522,640
0.83%
July 7, 2027
Ningbo Gaolue Jucai
Investment Partnership
Enterprise (Limited
Partnership) (“Gaolue
Jucai”)
2,504,480
2,504,480
0.82%
July 7, 2027
– 10 –

<<<PAGE 11>>>
NameNote 1
Number of Shares
held in the
Company subject to
lock-up
undertakings upon
Listing
Number of H
Shares held in the
Company subject to
lock-up
undertakings upon
Listing
% of shareholding
in the Company
subject to
lock-up upon
Listing(Note 1)
Last day subject to
the lock-up
undertakings(Note 2)
Hainan KING TOWER
Intelligent Manufacturing
Phase I Private Equity
Fund Partnership (Limited
Partnership) (“KT
Manufacturing I PE Fund”)
1,620,280
1,620,280
0.53%
July 7, 2027
Hainan Chengmingjia
Venture Capital Partnership
(Limited Partnership)
(“Chengmingjia VC Fund”)
1,565,300
1,565,300
0.51%
July 7, 2027
Putian iRun II Capital
1,350,235
1,350,235
0.44%
July 7, 2027
Jinguan New Energy
272,280
272,280
0.09%
July 7, 2027
Tongxiang Wutong Puhua
Fengqi Venture Capital
Partnership (Limited
Partnership) (“Tongxiang
Puhua”)
5,365,141
—
1.76%
July 7, 2027
Puhua Fengqi (Ningbo)
Venture Capital Fund
Partnership (Limited
Partnership) (“Ningbo
Puhua”)
5,365,141
—
1.76%
July 7, 2027
Hainan Cheng Mingrui
Investment Partnership
(Limited Partnership)
(“Hainan Cheng Mingrui”)
2,497,125
—
0.82%
July 7, 2027
Total
105,860,087
77,570,929
34.67%
Notes:
1.
Please refer to the Prospectus for further details.
2.
The expiry date of the lock-up period shown in the table above is pursuant to applicable PRC laws.
– 11 –

<<<PAGE 12>>>
PLACEE CONCENTRATION ANALYSIS
Placees(Note)
Number of
Shares allotted
Allotment as
% of
International
Offering
Allotment as
% of total
Offer Shares
Number of
Shares held
upon Listing
% of total
issued share
capital
upon Listing
Top 1
6,850,000
30.49%
24.39%
6,850,000
2.24%
Top 5
21,045,000
93.66%
74.93%
27,796,165
9.10%
Top 10
22,312,000
99.30%
79.44%
29,063,165
9.52%
Top 25
22,442,000
99.88%
79.90%
29,193,165
9.56%
Note: Ranking of placees is based on the number of H Shares allotted to the placees.
– 12 –

<<<PAGE 13>>>
H SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholders(Note 1)
Number of
Shares allotted
Allotment as
% of
International
Offering
Allotment as
% of total
Offer Shares
Number of
H Shares held
upon Listing
% of total issued
H Share capital
upon Listing
% of total issued
share capital
upon Listing
Number of
Shares held
upon Listing
Top 1
—
0.00%
0.00%
120,884,520
44.16%
39.60%
120,884,520
Top 5
5,500,000
24.48%
19.58%
179,997,465
65.76%
58.96%
179,997,465
Top 10
5,500,000
24.48%
19.58%
229,553,139
83.86%
75.19%
237,677,823
Top 25
22,262,000
99.08%
79.26%
267,902,616
97.87%
87.75%
281,224,893
Notes:
(1) Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
– 13 –

<<<PAGE 14>>>
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders(Note 1)
Number of
Shares allotted
Allotment as
% of
International
Offering
Allotment as
% of total
Offer Shares
Number of
H Shares held
upon Listing
Number of
Shares held
upon Listing
% of total issued
share capital
upon Listing
Top 1
—
0.00%
0.00%
120,884,520
120,884,520
39.60%
Top 5
—
0.00%
0.00%
177,155,749
185,280,433
60.69%
Top 10
5,500,000
24.48%
19.58%
221,451,744
240,306,710
78.71%
Top 25
22,047,000
98.12%
78.50%
267,687,616
299,252,905
98.02%
Notes:
(1) Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon Listing.
– 14 –

<<<PAGE 15>>>
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, 169,551 valid
applications made by the public will be conditionally allocated on the basis set out below:
Pool A:
NUMBER OF H
SHARES
APPLIED FOR
NUMBER OF
VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED OF
THE TOTAL
NUMBER OF H
SHARES APPLIED
FOR
200
68,857
2,066 out of 68,857 applicants to receive 200 H
Shares
3.00%
400
28,373
1,147 out of 28,373 applicants to receive 200 H
Shares
2.02%
600
5,566
268 out of 5,566 applicants to receive 200 H Shares
1.60%
800
1,808
99 out of 1,808 applicants to receive 200 H Shares
1.37%
1,000
3,667
220 out of 3,667 applicants to receive 200 H Shares
1.20%
1,200
1,029
67 out of 1,029 applicants to receive 200 H Shares
1.09%
1,400
963
67 out of 963 applicants to receive 200 H Shares
0.99%
1,600
811
60 out of 811 applicants to receive 200 H Shares
0.92%
1,800
761
59 out of 761 applicants to receive 200 H Shares
0.86%
2,000
14,916
1,205 out of 14,916 applicants to receive 200 H
Shares
0.81%
3,000
2,565
247 out of 2,565 applicants to receive 200 H Shares
0.64%
4,000
3,933
429 out of 3,933 applicants to receive 200 H Shares
0.55%
5,000
1,578
190 out of 1,578 applicants to receive 200 H Shares
0.48%
6,000
998
130 out of 998 applicants to receive 200 H Shares
0.43%
7,000
664
92 out of 664 applicants to receive 200 H Shares
0.40%
8,000
746
110 out of 746 applicants to receive 200 H Shares
0.37%
9,000
684
106 out of 684 applicants to receive 200 H Shares
0.34%
10,000
3,824
618 out of 3,824 applicants to receive 200 H Shares
0.32%
20,000
3,386
737 out of 3,386 applicants to receive 200 H Shares
0.22%
30,000
1,886
489 out of 1,886 applicants to receive 200 H Shares
0.17%
40,000
1,749
513 out of 1,749 applicants to receive 200 H Shares
0.15%
50,000
1,768
571 out of 1,768 applicants to receive 200 H Shares
0.13%
60,000
1,129
394 out of 1,129 applicants to receive 200 H Shares
0.12%
70,000
771
288 out of 771 applicants to receive 200 H Shares
0.11%
80,000
945
374 out of 945 applicants to receive 200 H Shares
0.10%
90,000
588
245 out of 588 applicants to receive 200 H Shares
0.09%
100,000
1,540
670 out of 1,540 applicants to receive 200 H Shares
0.09%
– 15 –

<<<PAGE 16>>>
NUMBER OF H
SHARES
APPLIED FOR
NUMBER OF
VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED OF
THE TOTAL
NUMBER OF H
SHARES APPLIED
FOR
120,000
836
393 out of 836 applicants to receive 200 H Shares
0.08%
140,000
659
331 out of 659 applicants to receive 200 H Shares
0.07%
160,000
550
293 out of 550 applicants to receive 200 H Shares
0.07%
180,000
440
247 out of 440 applicants to receive 200 H Shares
0.06%
200,000
2,253
1,319 out of 2,253 applicants to receive 200 H
Shares
0.06%
Total
160,243
Total
number
of
Pool
A
successful
applicants:
14,044
Pool B:
NO. OF SHARES
APPLIED FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED OF
THE TOTAL NO.
OF SHARES
APPLIED FOR
250,000
4,641
200 H Shares plus 1,741 out of 4,641 applicants to
receive an additional 200 H Shares
0.11%
300,000
1,268
200 H Shares plus 567 out of 1,268 applicants to
receive an additional 200 H Shares
0.10%
350,000
457
200 H Shares plus 233 out of 457 applicants to
receive an additional 200 H Shares
0.09%
400,000
470
200 H Shares plus 267 out of 470 applicants to
receive an additional 200 H Shares
0.08%
450,000
215
200 H Shares plus 134 out of 215 applicants to
receive an additional 200 H Shares
0.07%
500,000
416
200 H Shares plus 278 out of 416 applicants to
receive an additional 200 H Shares
0.07%
600,000
233
200 H Shares plus 176 out of 233 applicants to
receive an additional 200 H Shares
0.06%
702,200
1,608
200 H Shares plus 1,339 out of 1,608 applicants to
receive an additional 200 H Shares
0.05%
Total
9,308
Total number of Pool B successful applicants: 9,308
As of the date of this announcement, the relevant subscription monies previously deposited
in the designated nominee accounts have been remitted back to the accounts of all HKSCC
participants. Investors should contact their relevant brokers for any inquiries.
– 16 –

<<<PAGE 17>>>
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in
respect of which consent has been obtained, the Company has complied with the Listing
Rules and guidance materials in relation to the placing, allotment and listing of the H
Shares.
The Directors and the Overall Coordinators confirm that at least 50% of the total
number of the Offer Shares have been allocated to and taken up by independent price
setting investors in compliance with Rule 18C.08 of the Listing Rules.
The Directors further confirm that at least 20% of the issued share capital of the
Company will be held by sophisticated independent investors at the time of Listing in
compliance with Chapter 2.5 of the Guide for New Listing Applicants.
The Directors confirm that, to the best of their knowledge, the consideration paid by the
placees or the public (as the case may be) directly or indirectly for each Offer Share
subscribed for or purchased by them was the same as the Offer Price in addition to any
brokerage, AFRC transaction levy, SFC transaction levy and trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Placing to a close associate of an existing Shareholder with a consent under paragraph
1C(2) of the Placing Guidelines
The Company has applied for a consent under paragraph 1C(2) of Appendix F1 to the
Listing Rules, to permit a close associate of an existing Shareholder to participate as
placee in the Global Offering to subscribe for the Offer Shares to be issued by the
Company under the International Offering. The Stock Exchange has agreed to give the
consent subject to the conditions that:
(a) allocation to Shenzhen Investment Holdings Capital (the “Relevant Existing
Shareholder”) or its close associate will not affect the Company’s ability to satisfy
the public float requirement under Rule 8.08(1) (as amended and replaced by Rule
19A.13A), 18C.08 and 19A.13C(1) of the Listing Rules;
(b) the Company and the Joint Sponsors confirm that no preferential treatment has
been, nor will be, given to the Relevant Existing Shareholder or its close associate by
virtue of its relationship with the Company in any allocation in the International
Offering; and
(c)
the relevant information in respect of the allocation to the Relevant Existing
Shareholder and/or its close associate will be disclosed in the allotment results
announcement of the Company.
The allocation of Offer Shares to such close associate of an existing Shareholder is in
compliance with all the conditions under the consent granted by the Stock Exchange.
For details of the allocation of Offer Shares to close associate of an existing Shareholder,
please refer to the section headed “Allotment Results Details — International Offering —
Allottee with Consent Obtained” in this announcement.
– 17 –

<<<PAGE 18>>>
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong
Limited (the “Stock Exchange”) and Hong Kong Securities Clearing Company Limited
(“HKSCC”) take no responsibility for the contents of this announcement, make no
representation as to its accuracy or completeness and expressly disclaim any liability
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part
of the contents of this announcement.
This announcement does not constitute an offer to sell or the solicitation of an offer to buy
nor shall there be any sale of Offer Shares in any jurisdiction in which such offer,
solicitation or sales would be unlawful. This announcement is not for release, publication,
distribution, directly or indirectly, in or into the United States for sale or solicitation to
purchase or subscribe for securities in the United States or any other jurisdictions. The
Offer Shares have not been, and will not be, registered under the United States Securities
Act of 1933, as amended, supplemented or modified from time to time (the “U.S.
Securities Act”) or any state securities law of the United States and may not be offered,
sold, pledged, transferred or delivered within the United States, except pursuant to an
exemption from, or in a transaction not subject to, the registration requirements of the
U.S. Securities Act and state securities laws of the United States. The Offer Shares are
being offered and sold outside of the United States as offshore transactions in accordance
with Regulation S under the U.S. Securities Act and the applicable laws of each
jurisdiction where those offers and sales occur. There will not be and is not currently
intended to be any public offering of securities of the Company in the United States.
The Offer Shares are being offered and sold outside the United States in offshore
transactions in reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation
or offer to acquire, purchase or subscribe for securities. This announcement is not a
prospectus. Potential investors should read the Prospectus dated June 29, 2026 issued by
Reconova Technologies Co., Ltd. for detailed information about the Global Offering
described below before deciding whether or not to invest in the H Shares thereby being
offered.
Potential investors of the Offer Shares should note that the Joint Sponsors and the
Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters)
shall be entitled to terminate their obligations under the Hong Kong Underwriting
Agreement with immediate effect upon the occurrence of any of the events set out in the
paragraph headed “Underwriting — Underwriting Arrangements and Expenses — The
Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any time
prior to 8: 00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to
be on July 8, 2026).
– 18 –

<<<PAGE 19>>>
PUBLIC FLOAT AND FREE FLOAT
Immediately following completion of the Global Offering, based on the Offer Price of
HK$21.66 per H Share, the expected market capitalization upon the Listing is HK$6,613
million and the minimum prescribed public float percentage applicable to the Shares is
22.68%. Immediately following completion of the Global Offering, an aggregate of
152,843,096 H Shares representing approximately 50.06% of the issued share capital of
the Company will be held in the public hands, which is higher than the prescribed
percentage of H Shares required to be held in public hands of 22.68% under Rule
19A.13A(1) of the Listing Rules, satisfying the public float requirement under Rule
19A.13A(1) of the Listing Rules.
Based on the Offer Price of HK$21.66 per H Share, the Company satisfies the free float
requirement under Rule 19A.13C of the Listing Rules.
The Directors confirm that immediately after the completion of the Global Offering, (i)
no placee will, individually, be placed more than 10% of the enlarged issued share capital
of the Company; (ii) there will not be any new substantial shareholder (as defined in the
Listing Rules) of the Company; (iii) the three largest public shareholders of the Company
do not hold more than 50% of the H Shares in public hands at the time of the Listing in
compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least
300 H Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the
Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8: 00 a.m. on
Wednesday, July 8, 2026 (Hong Kong time), provided that the Global Offering has
become unconditional in all respects at or before that time, and the right of termination
described in “Underwriting — Underwriting Arrangements and Expenses — The Hong
Kong Public Offering — Grounds for Termination” in the Prospectus has not been
exercised. Investors who trade the H Shares on the basis of publicly available allocation
details prior to the receipt of H Share certificates or prior to the H Share certificates
becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8: 00 a.m. on
Wednesday, July 8, 2026 (Hong Kong time), it is expected that dealings in the H Shares
on the Stock Exchange will commence at 9: 00 a.m. on Wednesday, July 8, 2026 (Hong
Kong time). The H Shares will be traded in board lots of 200 Shares each, and the stock
code of the Shares will be 7656.
By order of the Board
Reconova Technologies Co., Ltd.
Mr. Zhan Donghui
Chairman, Chief Executive Officer and Executive Director
Hong Kong, July 7, 2026
As of the date of this announcement, the board of directors comprises (i) Mr. Zhan
Donghui and Mr. Han Songguang as executive directors; (ii) Mr. Chen Gen and Ms. Li Jia
as non-executive directors; and (iii) Mr. Sun Xiaobei, Ms. Gu Wenbo and Mr. Tang Ke as
independent non-executive directors.
– 19 –
