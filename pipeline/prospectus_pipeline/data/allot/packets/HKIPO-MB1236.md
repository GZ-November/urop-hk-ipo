# 配发结果公告抽取任务：1236.HK SHENZHEN LDROBOT CO., LTD - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**08/05/2026 22:38**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0508/2026050801854.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"1236.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for any securities. This announcement is not a prospectus. Potential investors should read the prospectus 
dated April 30, 2026 (the “Prospectus”) issued by SHENZHEN LDROBOT CO., LTD（深圳樂動機器人股份有限公
司） (the “Company”) for detailed information about the Global Offering described below before deciding whether or 
not to invest in the H Shares thereby being offered. Any investment decision in relation to the Offer Shares should be 
taken solely in reliance on the information in the Prospectus. The Company has not been and will not be registered 
under the U.S. Investment Company Act of 1940, as amended.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for securities 
in the United States or in any other jurisdictions. The securities mentioned herein have not been, and will not be, 
registered under the United States Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or 
securities law of any state or other jurisdiction of the United States. The securities may not be offered, sold, pledged 
or otherwise transferred within the United States except pursuant to an exemption from the registration requirements 
of the U.S. Securities Act and in compliance with any applicable state securities laws. The securities are being offered 
and sold outside the United States in offshore transactions in accordance with Regulation S under the U.S. Securities 
Act. There will be no public offer of securities in the United States.
In connection with the Global Offering, Haitong International Securities Company Limited as stabilizing manager 
(the “Stabilization Manager”) (or any person acting for it), on behalf of the Underwriters, the extent permitted by 
the applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect transactions 
with a view to stabilizing or supporting the market price of the H Shares at such price, in such amounts and in such 
manners as the Stabilization Manager, or any person acting for it may determine at a level higher than that which 
might otherwise prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilization 
Manager (or any person acting for it) to conduct any such stabilizing action. Such stabilizing action, if taken, (a) 
will be conducted at the absolute discretion of the Stabilization Manager (or any person acting for it) and in what the 
Stabilization Manager reasonably regards as the best interest of our Company, (b) may be discontinued at any time 
and (c) is required to be brought to an end within 30 days of the last day for lodging applications under the Hong 
Kong Public Offering, being Friday, June 5, 2026. Such Stabilizing action, if taken, may be effected in all jurisdictions 
where it is permissible to do so, in each case in compliance with all applicable laws, rules and regulatory requirements, 
including the Securities and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, 
made under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong). Potential investors should 
be aware that no stabilizing action can be taken to support the price of the H Shares for longer than the stabilization 
period, which will begin on the Listing Date, and is expected to expire on the 30th day after the last day for lodging 
applications under the Hong Kong Public Offering. After this date, when no further stabilizing action may be taken, 
demand for the H Shares, and therefore the price of the H Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to term and conditions set out in 
the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not 
resident in Hong Kong. Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinators 
(for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong Kong 
Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the section headed 
“Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” 
in the Prospectus at any time prior to 8:00 a.m. on the Listing Date (which is currently expected to be on Monday, 
May 11, 2026).

<<<PAGE 2>>>
2
SHENZHEN LDROBOT CO., LTD
深圳樂動機器人股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under
the Global Offering
33,333,400 H Shares (subject to the
 Over-allotment Option)
Number of Hong Kong Offer Shares
3,333,400 H Shares (subject to
 adjustment)
Number of International Offer Shares
30,000,000 H Shares (subject to
 adjustment and the Over-allotment
 Option)
Final Offer Price
HK$26.36 per H Share, plus brokerage
 of 1.0%, SFC transaction levy of
 0.0027%, Stock Exchange trading fee
 of 0.00565% and AFRC transaction
 levy of 0.00015% (payable in full on
 application in Hong Kong dollars and
 subject to refund)
Nominal value
RMB0.10 per H Share
Stock code
1236
Joint Sponsors, Sponsor-Overall Coordinators, Joint Global Coordinators,
 Joint Bookrunners and Joint Lead Managers
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners 
and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
SHENZHEN LDROBOT CO., LTD
深圳樂動機器人股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated April 30, 2026 (the “Prospectus”) issued by 
SHENZHEN LDROBOT CO., LTD (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
H Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
1236
Stock short name
LDROBOT
Dealings commencement date
May 11, 2026*
* see note at the end of the announcement
Price Information
Final Offer Price
HKD26.36
Maximum Offer Price
HKD30.00
Offer Shares and Share Capital
Number of Offer Shares (before exercise of the Over-allotment 
Option)
33,333,400
Final Number of Offer Shares in Hong Kong Public Offering
3,333,400
Final Number of Offer Shares in International Offering (before 
the exercise of the Over-allotment Option)
30,000,000
Number of issued Shares upon Listing (before exercise of the 
Over-allotment Option)
333,333,400

<<<PAGE 4>>>
4
Over-allocation
No. of Offer Shares over-allocated
0
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.
Proceeds
Gross proceeds (Note)
HK$878.7 million
 Less: Estimated listing expenses payable based on Final Offer 
  Price
HK$(71.9) million
Net proceeds
HK$806.8 million
Note: Gross proceeds refers to the amount to which the Company is entitled to receive assuming the Over-allotment 
Option is not exercised. For details of the use of proceeds, please refer to the section headed “Future Plans and Use 
of Proceeds” of the Prospectus. The Company will adjust the allocation of the net proceeds from the exercise of the 
Over-allotment Option (if any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” 
of the Prospectus on a pro rata basis.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
296,740
No. of successful applications
16,667
Subscription level
6,707.66 times
Reallocation
No
No. of Offer Shares initially available under the Hong Kong Public 
Offering
3,333,400
No. of Offer Shares reallocated from the International Offering
0
Final no. of Offer Shares under the Hong Kong Public Offering
3,333,400
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering
10.00%
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
www.tricor.com.hk/ipo/result to perform a search by identification number or www.hkeipo.hk/IPOResult for the full 
list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
111
Subscription Level
9.54 times
No. of Offer Shares initially available under the International 
Offering
30,000,000
Final no. of Offer Shares under the International Offering
30,000,000
% of Offer Shares under the International Offering to the Global 
Offering
90.00%
The Directors confirm that, to the best of their knowledge, information and belief, save for a 
consent under Chapter 4.15 of the Guide for New Listing Applicants to permit the Company 
to, among other things, (a) allocate certain Offer Shares in the International Offering to a close 
associate of an existing Shareholder, (b) allocate certain Offer Shares in the International Offering 
to connected clients, (i) none of the Offer Shares subscribed by the placees and the public have 
been financed directly or indirectly by the Company, any of the Directors, chief executive of 
the Company, Controlling Shareholders, substantial Shareholders, existing Shareholders of the 
Company or any of its subsidiaries or their respective close associates; and (ii) none of the placees 
and the public who have purchased the Offer Shares are accustomed to taking instructions from 
the Company, any of the Directors, chief executive of the Company, Controlling Shareholders, 
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries or their 
respective close associates in relation to the acquisition, disposal, voting or other disposition of 
Shares registered in his/her/its name or otherwise held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investor
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
KCH Vision Investment Limited
10,508,200
31.52%
3.15
No
Total
10,508,200
31.52%
3.15
–
Note:
1. 
Before any exercise of the Over-allotment Option.
2. 
For further details of the Cornerstone Investor, please refer to the section headed “Cornerstone Investor” in 
the Prospectus.

<<<PAGE 6>>>
6
Allotees with Waivers/Consents Obtained
Investor
No. of 
Offer 
Shares 
allocated
% of 
Offer 
Shares 
(assuming 
the Over-
allotment 
Option is not 
exercised)
% of total 
issued share 
capital in the 
Company 
after the 
Global 
Offering 
(assuming 
the Over-
allotment 
Option is not 
exercised)
Relationship
Allottee with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent 
under paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by 
a close associate of an existing Shareholder Note 1
Shenzhen Nanshan 
Strategic Emerging 
Industry Investment 
Co., Ltd. (深圳市南
山戰略新興產業投資
有限公司) (“Nanshan 
Strategic”) Note 2
7,587,200
22.76%
2.28%
A placee and a close 
associate of an existing 
Shareholder.
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of 
the Guide for New Listing Applicants in relation to allocations to connected clients Note 1
HTI Financial Solutions 
Limited (“HTIFSL”)
600
0.002%
0.0002%
A connected client of 
Haitong International 
Securities Company 
Limited (“Haitong 
Securities”) and Guotai 
Junan Securities (Hong 
Kong) Limited (“Guotai 
Junan Securities”) as a 
placee.
China Asset 
Management (Hong 
Kong) Limited (“China 
AMC HK”)
2,800
0.008%
0.0008%
A connected client 
of CITIC Securities 
Brokerage (HK) Limited 
(“CITIC Securities”) as 
a placee.

<<<PAGE 7>>>
7
Notes:
1. 
For details of (i) the waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under 
paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by a close associates of an 
existing Shareholder, and (ii) the consent under paragraph 1C of the Placing Guidelines and Chapter 4.15 of 
the Guide for New Listing Applicants in relation to allocations to connected clients, please refer to the section 
headed “Others/ Additional Information” in this announcement.
2. 
Nanshan Strategic is a close associate of Shenzhen High Tech Investment Fuhai Venture Capital Fund Phase I 
Partnership Enterprise (Limited Partnership) (“High Tech Investment Fuhai”), an existing Shareholder. High 
Tech Investment Fuhai is controlled by the State-owned Assets Supervision and Administration Commission of 
the Shenzhen Municipal People’s Government, holding approximately 53.84% interest in Shenzhen High Tech 
Investment Zhengxuan Equity Investment Fund Management Co., Ltd. (深圳市高新投正軒股權投資基金管理有
限公司), being the general partner of High Tech Investment Fuhai. Nanshan Strategic is a company established 
in the PRC and entirely held by State-owned Assets Supervision and Administration Bureau of Nanshan District, 
Shenzhen (Collective Assets Management Bureau of Nanshan District, Shenzhen) (深圳市南山區國有資產監
督管理局(深圳市南山區集體資產管理局)). Hence, the ultimate beneficial owner of each of High Investment 
Fuhai and Nanshan Strategic is PRC governmental body in Shenzhen.

<<<PAGE 8>>>
8
LOCK-UP UNDERTAKINGS
Controlling Shareholders (as defined in the Prospectus)
Name
Number of 
shares held
in the Company
subject 
to lock-up 
undertakings
upon Listing
% of 
shareholding in 
the Company 
subject to
lock-up 
undertakings
upon ListingNote 1
Last day subject 
to the lock-up 
undertakings
ZHOU Wei (周偉)
61,637,700
18.49%
May 10, 2027 Note 2
GUO Gaihua (郭蓋華)
34,227,900
10.27%
May 10, 2027 Note 2
WANG Mingyue (王明月)
2,569,800
0.77%
May 10, 2027 Note 2
Shenzhen Photon Space 
Technology Partnership Enterprise 
(Limited Partnership) (深圳光子
空間科技合夥企業(有限合夥))
20,408,100
6.12%
May 10, 2027 Note 2
Total
118,843,500
35.65%
–
Notes:
(1) 
Before any exercise of the Over-allotment Option.
(2) 
All existing Shareholders (including the Controlling Shareholders) shall not dispose of any of the Shares held 
by them within the 12 months following the Listing Date as required under the applicable PRC laws.
Pre-IPO Investors
Name
Number of 
shares held
in the Company
subject 
to lock-up 
undertakings
upon Listing
% of 
shareholding in 
the Company 
subject to
lock-up 
undertakings
upon 
ListingNote 1
Last day 
subject to the 
lock-up 
undertakings
Tibet Wanqing Investment 
Management Co., Ltd. (西藏萬青
投資管理有限公司)
44,714,700
13.41%
May 10, 2027 Note 2

<<<PAGE 9>>>
9
Name
Number of 
shares held
in the Company
subject 
to lock-up 
undertakings
upon Listing
% of 
shareholding in 
the Company 
subject to
lock-up 
undertakings
upon 
ListingNote 1
Last day 
subject to the 
lock-up 
undertakings
Hunan Huaye Tiancheng Venture 
Capital Partnership Enterprise 
(Limited Partnership) (湖南華業
天成創業投資合夥企業(有限合
夥))
40,583,700
12.18%
May 10, 2027 Note 2
Zhuhai Hengqin Huaye 
Tiancheng Venture Capital 
Partnership Enterprise (Limited 
Partnership) (珠海橫琴華業天成
創業投資合夥企業(有限合夥))
Wuhan Yuanxia Equity 
Investment Partnership (Limited 
Partnership) (武漢源夏股權投資
合夥企業(有限合夥))
9,857,100
2.96%
May 10, 2027 Note 2
Kelamayi Qicheng Investment 
Fund Partnership Enterprise 
(Limited Partnership) (克拉瑪依
啟誠投資基金合夥企業(有限合
夥))
8,886,000
2.67%
May 10, 2027 Note 2
Xinjiang Mingshi Changfeng 
Private Equity Venture Capital 
Fund Partnership Enterprise 
(Limited Partnership) (新疆明時
長風私募創業投資基金合夥企業
(有限合夥))
3,911,400
1.17%
May 10, 2027 Note 2
Shenzhen Pengyuansheng 
Enterprise Management 
Partnership (Limited Partnership) 
(深圳鵬遠昇企業管理合夥企業
(有限合夥))
7,245,000
2.17%
May 10, 2027 Note 2

<<<PAGE 10>>>
10
Name
Number of 
shares held
in the Company
subject 
to lock-up 
undertakings
upon Listing
% of 
shareholding in 
the Company 
subject to
lock-up 
undertakings
upon 
ListingNote 1
Last day 
subject to the 
lock-up 
undertakings
Hangzhou Yuanjing SME 
Development Equity Investment 
Fund Partnership (Limited 
Partnership) (杭州元璟中小企業
發展股權投資基金合夥企業(有
限合夥))
12,214,200
3.66%
May 10, 2027 Note 2
Hangzhou Yuanjing Dingheng 
Equity Investment Fund 
Partnership Enterprise (Limited 
Partnership) (杭州圓璟鼎恆股權
投資基金合夥企業(有限合夥))
Total
127,412,100
38.22%
–
Notes:
(1) 
Before any exercise of the Over-allotment Option.
(2) 
All existing Shareholders (including the Pre-IPO Investors) shall not dispose of any of the Shares held by 
them within the 12 months following the Listing Date as required under the applicable PRC laws.

<<<PAGE 11>>>
11
Other Existing Shareholders
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
shareholding in 
the Company 
subject to 
lock-up 
undertakings 
upon 
ListingNote 1
Last day 
subject to the 
lock-up 
undertakings
Shenzhen Lecheng Technology 
Partnership Enterprise (深圳樂澄
科技合夥企業(有限合夥))
26,226,000
7.87%
May 10, 2027 Note 2
Lianjin Innovation Industry 
Private Equity Investment 
Fund (Shenzhen) Partnership 
Enterprise (Limited Partnership) 
(聯金創新產業私募股權投資基
金(深圳)合夥企業(有限合夥))
6,428,700
1.93%
May 10, 2027 Note 2
Shenzhen Jiuyu Galaxy 
Intelligent Internet Investment 
Fund (Limited Partnership) (深圳
九宇銀河智能互聯投資基金(有
限合夥))
4,305,600
1.29%
May 10, 2027 Note 2
Shenzhen Gongchuang Zhuoxin 
Investment Partnership Enterprise 
(Limited Partnership) (深圳共創
卓信投資合夥企業(有限合夥))
4,285,500
1.29%
May 10, 2027 Note 2
Hainan Houpu Digital 
Technology Co., Ltd. (海南厚普
數字科技有限公司)
2,892,900
0.87%
May 10, 2027 Note 2
Shenzhen High Tech Investment 
Fuhai Venture Capital Fund 
Phase I Partnership Enterprise 
(Limited Partnership) (深圳市高
新投福海創業投資基金一期合夥
企業(有限合夥))
2,551,200
0.77%
May 10, 2027 Note 2
Zhongjin Pucheng Investment 
Co., Ltd. (中金浦成投資
有限公司)
2,142,900
0.64%
May 10, 2027 Note 2

<<<PAGE 12>>>
12
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
shareholding in 
the Company 
subject to 
lock-up 
undertakings 
upon 
ListingNote 1
Last day 
subject to the 
lock-up 
undertakings
Wenrun Growth No. 1 (Zhuhai) 
Equity Investment Fund 
Partnership Enterprise (Limited 
Partnership) (溫潤成長壹號(珠
海)股權投資基金合夥企業(有限
合夥))
2,081,700
0.62%
May 10, 2027 Note 2
Zhuhai Hengqin Qichuang Shared 
Venture Capital Partnership 
(Limited Partnership) (珠海橫琴
齊創共享創業投資合夥企業(有
限合夥))
60,900
0.02%
May 10, 2027 Note 2
WANG Bing (王昞)
1,257,300
0.38%
May 10, 2027 Note 2
Beijing Maker Town Equity 
Investment Fund (Limited 
Partnership) (北京創客小鎮股權
投資基金(有限合夥))
1,190,400
0.36%
May 10, 2027 Note 2

<<<PAGE 13>>>
13
Name
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
shareholding in 
the Company 
subject to 
lock-up 
undertakings 
upon 
ListingNote 1
Last day 
subject to the 
lock-up 
undertakings
Shenzhen Yuanxi Intelligent 
Manufacturing Enterprise 
(Limited Partnership) (深圳源希
智能製造企業(有限合夥))
321,300
0.10%
May 10, 2027 Note 2
Total
53,744,400
16.12%
–
Notes:
(1) 
Before any exercise of the Over-allotment Option.
(2) 
All existing Shareholders (including the Pre-IPO Investors) shall not dispose of any of the Shares held by 
them within the 12 months following the Listing Date as required under the applicable PRC laws.
Cornerstone Investor
Name
Number of 
shares held
in the 
Company
subject to 
lock-up 
undertakings
upon Listing
% of total
Offer Shares
% of 
shareholding in 
the Company
subject to lock-up
undertakings 
upon ListingNote 1
Last day subject
to the lock-up 
undertakingsNote 1
KCH Vision Investment Limited
10,508,200
31.52%
3.15% 
November 10, 2026
Total
10,508,200
31.52%
3.15% 
–
Note:
(1) 
In accordance with the relevant cornerstone investment agreement, the required lock-up period ends on 
November 10, 2026. The Cornerstone Investor will cease to be prohibited from disposing of or transferring H 
Shares subscribed pursuant to the relevant cornerstone investment agreement after the indicated date.

<<<PAGE 14>>>
14
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of
H Shares
allotted
Allotment
as % of
International
Offering
Allotment as
% of total
Offer Shares
Number of H
Shares held
upon Listing
Number of
H Shares
held upon
Listing as %
of total 
issued
share capital
upon Listing
Top 1
10,508,200
35.03%
31.52%
10,508,200
3.15%
Top 5
24,165,000
80.55%
72.49%
26,716,200
8.01%
Top 10
29,608,400
98.69%
88.83%
32,159,600
9.65%
Top 25
29,897,000
99.66%
89.69%
32,448,200
9.73%
Note:
* Ranking of placees is based on the number of Shares allotted to the placees.

<<<PAGE 15>>>
15
H SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholders*
Number of
H Shares
allotted
Allotment
as % of
International
Offering
Allotment
as
% of total
Offer
Shares
Number of
H Shares
held upon
Listing
Number of
H
Shares held
upon Listing
as % of
total issued
share capital
upon Listing
Number of
Shares held
upon Listing
Top 1
0
0.00%
0.00%
118,843,500
35.65%
118,843,500
Top 5
0
0.00%
0.00%
243,165,300
72.95%
243,165,300
Top 10
18,095,400
60.32%
54.29%
294,454,800
88.34%
294,454,800
Top 25
29,305,000
97.68%
87.91%
329,244,100
98.77%
329,244,100
Note:
* Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 16>>>
16
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
Number 
of Shares 
allotted
Allotment 
as % of 
International
Offering 
Allotment 
as % of total 
Offer Shares 
Number of H
 Shares held 
upon Listing
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
Top 1
0
0.00%
0.00%
118,843,500
118,843,500
35.65%
Top 5
0
0.00%
0.00%
243,165,300
243,165,300
72.95%
Top 10
18,095,400
60.32%
54.29%
294,454,800
294,454,800
88.34%
Top 25
29,305,000
97.68%
87.91%
329,244,100
329,244,100
98.77%
Note:
* Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon Listing.

<<<PAGE 17>>>
17
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 296,740 valid 
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
200
80,907
648 out of 80,907 applicants to receive 200 H Shares
0.80%
400
15,128
162 out of 15,128 applicants to receive 200 H Shares
0.54%
600
9,624
122 out of 9,624 applicants to receive 200 H Shares
0.42%
800
6,351
91 out of 6,351 applicants to receive 200 H Shares
0.36%
1,000
8,461
133 out of 8,461 applicants to receive 200 H Shares
0.31%
1,200
3,778
64 out of 3,778 applicants to receive 200 H Shares
0.28%
1,400
3,720
67 out of 3,720 applicants to receive 200 H Shares
0.26%
1,600
14,320
273 out of 14,320 applicants to receive 200 H Shares
0.24%
1,800
2,384
48 out of 2,384 applicants to receive 200 H Shares
0.22%
2,000
12,260
256 out of 12,260 applicants to receive 200 H Shares
0.21%
3,000
9,495
235 out of 9,495 applicants to receive 200 H Shares
0.16%
4,000
5,142
144 out of 5,142 applicants to receive 200 H Shares
0.14%
5,000
3,659
112 out of 3,659 applicants to receive 200 H Shares
0.12%
6,000
3,900
129 out of 3,900 applicants to receive 200 H Shares
0.11%
7,000
2,661
94 out of 2,661 applicants to receive 200 H Shares
0.10%
8,000
2,491
93 out of 2,491 applicants to receive 200 H Shares
0.09%
9,000
2,258
89 out of 2,258 applicants to receive 200 H Shares
0.09%
10,000
15,084
616 out of 15,084 applicants to receive 200 H Shares
0.08%
20,000
9,607
524 out of 9,607 applicants to receive 200 H Shares
0.05%
30,000
7,347
475 out of 7,347 applicants to receive 200 H Shares
0.04%
40,000
5,229
381 out of 5,229 applicants to receive 200 H Shares
0.04%
50,000
4,090
327 out of 4,090 applicants to receive 200 H Shares
0.03%
60,000
3,719
321 out of 3,719 applicants to receive 200 H Shares
0.03%
70,000
3,207
295 out of 3,207 applicants to receive 200 H Shares
0.03%
80,000
2,718
264 out of 2,718 applicants to receive 200 H Shares
0.02%
90,000
2,319
237 out of 2,319 applicants to receive 200 H Shares
0.02%
100,000
20,027
2,134 out of 20,027 applicants to receive 200 H Shares
0.02%
259,886
Total number of Pool A successful applicants: 8,334

<<<PAGE 18>>>
18
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
15,279
1,528 out of 15,279 applicants to receive 200 H Shares
0.01%
300,000
5,720
832 out of 5,720 applicants to receive 200 H Shares
0.01%
400,000
3,294
625 out of 3,294 applicants to receive 200 H Shares
0.01%
500,000
2,444
570 out of 2,444 applicants to receive 200 H Shares
0.01%
600,000
1,769
488 out of 1,769 applicants to receive 200 H Shares
0.01%
700,000
1,274
405 out of 1,274 applicants to receive 200 H Shares
0.01%
800,000
1,011
364 out of 1,011 applicants to receive 200 H Shares
0.01%
900,000
744
298 out of 744 applicants to receive 200 H Shares
0.01%
1,000,000
1,201
530 out of 1,201 applicants to receive 200 H Shares
0.01%
1,200,000
746
390 out of 746 applicants to receive 200 H Shares
0.01%
1,400,000
772
465 out of 772 applicants to receive 200 H Shares
0.01%
1,666,600
2,600
1,838 out of 2,600 applicants to receive 200 H Shares
0.01%
36,854
Total number of Pool B successful applicants: 8,333

<<<PAGE 19>>>
19
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the Offer Price in addition to any brokerage, AFRC transaction 
levy, SFC transaction levy and Stock Exchange trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Placing to existing Shareholders with a waiver from the strict compliance with Rule 10.04 of 
the Listing Rules and a prior consent under paragraph 1C(2) of the Placing Guidelines
The Company has applied to the Stock Exchange, and the Stock Exchange has granted, the waivers 
from the strict compliance with Rule 10.04 of the Listing Rules and consents under paragraph 
1C(2) of the Placing Guidelines to permit the Company to allocate such Offer Shares in the 
International Offering to a close associate of an existing Shareholders on the following grounds 
which are consistent with the conditions as set out in the Chapter 4.15 of the Guide for New 
Listing Applicants:
(i) 
Less than 5%: The Joint Sponsors confirm that High Tech investment Fuhai (the “Existing 
Shareholder”) is interested in less than 5% of the Company’s voting rights prior to the 
completion of the Global Offering;
(ii) Not core connected persons: The Joint Sponsors confirm that the Existing Shareholder is not 
a core connected person (as defined under the Listing Rules) of the Company or any close 
associate (as defined under the Listing Rules) of such core connected person immediately 
prior to or following the Global Offering;
(iii) No right to appoint Directors: The Joint Sponsors confirm that the Existing Shareholder has 
no power to appoint directors of the Company (other than as shareholders of the Company) 
and do not have other special rights that is exercisable in connected with the Global Offering 
prior to its termination;
(iv) No impact on public float: The Joint Sponsors confirm that the allocation to the Existing 
Shareholder or its close associate for which this submission is sought will not affect the 
Company’s ability to satisfy the public float requirement under Rule 8.08 of the Listing 
Rules, as amended and replaced by Rule 19A.13A of the Listing Rules;

<<<PAGE 20>>>
20
(v) 
Disclosure: the relevant information in respect of the allocation to Existing Shareholder will 
be disclosed in the allotment results announcement;
(vi) the Joint Sponsors confirm to the Stock Exchange in writing that based on (i) their 
discussions with the Company; and (ii) the confirmations provided to the Stock Exchange 
by the Company (confirmations (viii) mentioned below), and to the best of their knowledge 
and belief, they have no reason to believe that the Existing Shareholder or its close associate 
received any preferential treatment in the allocation as a placee by virtue of its relationship 
with the Company, and details of the allocation will be disclosed in the allotment results 
announcement;
(vii) the Overall Coordinators confirm to the Stock Exchange in writing that based on (i) their 
discussions with the Company; and (ii) the confirmations provided to the Stock Exchange 
by the Company (confirmations (viii) mentioned below), and to the best of their knowledge 
and belief, they have no reason to believe that the Existing Shareholder or its close associate 
received any preferential treatment in the allocation as a placee by virtue of its relationship 
with the Company; and
(viii) the Company confirms to the Stock Exchange in writing that no preferential treatment has 
been, nor will be, given to the Existing Shareholder or its close associate by virtue of its 
relationship with the Company in any allocation in the placing tranche.
The allocation of Offer Shares to such close associate of existing Shareholder is in compliance 
with all the conditions under the waivers/consents granted by the Stock Exchange.
For details of the allocations of Offer Shares to existing Shareholders, please refer to the section 
headed “Allotment Results Details – International Offering – Allotees with Waivers/Consents 
Obtained” in this announcement.
Placing to connected clients with prior consents under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines.

<<<PAGE 21>>>
21
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a consent under paragraph 1C(1) of the Placing 
Guidelines to permit the Company to allocate such Offer Shares in the International Offering to certain connected clients of distributors. 
The allocation of Offer Shares to such connected clients is in compliance with all the conditions under the consent granted by the Stock 
Exchange. Details of the placement to connected clients are set out below:
No.
Connected Client(s) (4)
Connected 
Distributor(s)
Relationship between the 
Connected Client(s) and 
the Connected Distributor(s)
Whether the 
connected clients 
will hold the 
beneficial interests of 
the Offer Shares on 
a non-discretionary 
basis or discretionary 
basis for independent 
third parties
Number of Offer 
Shares to be allocated 
to the connected client
% of Offer Shares 
allocated to the 
connected client(1)
% of the total 
issued share capital 
in the Company 
after the Global 
Offering(1)
1.
HTIFSL Note 2
Haitong Securities and 
 Guotai Junan 
 Securities
HTIFSL, Haitong Securities and 
 Guotai Junan Securities are 
 members of same group of 
 companies.
Non-discretionary
600
0.002%
0.0002%
2.
China AMC HK Note 3
CITIC Securities
China AMC HK and CITIC 
 Securities are members of the 
 same group of companies.
Discretionary
2,800
0.008%
0.0008%

<<<PAGE 22>>>
22
Note:
(1) 
Before any exercise of the Over-allotment Option.
(2) 
HTIFSL has entered into a total return swap transaction trade (the “HTI TRS”) with Seahawk China Dynamic 
Fund, the ultimate beneficial owner of which is LIANG Hao (梁昊) (the “HTIFSL Ultimate Client”), pursuant 
to which HTIFSL will hold the Offer Shares on a non-discretionary basis as the single underlying holder under 
the HTI TRS. The full economic exposure of the Offer Shares will be passed to the HTIFSL Ultimate Client, 
while HTIFSL will hold the beneficial interest of the Offer Shares on behalf of the HTIFSL Ultimate Client.
Due to its internal policy, HTIFSL will not exercise the voting rights of the Offer Shares during the term of HTI 
TRS.
To the best knowledge of HTIFSL after due enquiry, (i) there is no other ultimate beneficial owner holding 30% 
or more interest in the HTIFSL Ultimate Client; and (ii) the HTIFSL Ultimate Client is an independent third 
party of HTIFSL, Haitong Securities, Guotai Junan Securities and the companies which are members of the 
same group of Haitong Securities and Guotai Junan Securities.
(3) 
China AMC HK is an investment advisor and a delegate of the investment manager of its underlying clients 
(“China AMC HK Ultimate Clients”) and manages assets (in its capacity as an investment advisor of the 
China AMC HK Ultimate Clients) and executes trades (in its capacity as a delegate of the investment manager 
of China AMC HK Ultimate Clients) for on behalf of China AMC HK Ultimate Clients, namely (i) CHINAAMC 
CHINA FOCUS FUND, the ultimate beneficial owner of which is Manulife (International) Limited, holding 
73.17% interest therein; (ii) ChinaAMC Absolute Return Fund SP, the ultimate beneficial owner of which is Mr. 
Li Fung Ming, holding 79.16% interest therein.
To the best knowledge of China AMC HK after due enquiry, (i) there is no other ultimate beneficial owner 
holding 30% or more interest in each of the China AMC HK Ultimate Clients; and (ii) each of the China AMC 
HK Ultimate Clients is an independent third party of China AMC HK, CITIC Securities and the companies 
which are members of the same group of companies as CITIC Securities.

<<<PAGE 23>>>
23
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
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
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated April 30, 2026 issued by SHENZHEN 
LDROBOT CO., LTD for detailed information about the Global Offering described below before 
deciding whether or not to invest in the H Shares thereby being offered.
* The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to term and 
conditions set out in the Prospectus. The Hong Kong Offer Shares will not be offered to any 
person who is outside Hong Kong and/or not resident in Hong Kong. Potential investors of the 
Offer Shares should note that the Sponsor-Overall Coordinators (for themselves and on behalf 
of the Hong Kong Underwriters) shall be entitled to terminate the Hong Kong Underwriting 
Agreement with immediate effect upon the occurrence of any of the events set out in the 
section headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public 
Offering – Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. on the 
Listing Date (which is currently expected to be on Monday, May 11, 2026).
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering, 129,191,500 H Shares, representing 
approximately 38.76% of the issued share capital of our Company (before any exercise of the 
Over-allotment Option) will count towards the public float. Therefore, the number of H shares held 
in public hands is higher than the prescribed percentage of H Shares required to be held in public 
hands of 25% under Rule 8.08(1) (as amended and replaced by Rule 19A.13A) of the Listing 
Rules, satisfying the minimum percentage requirement in compliance with Rule 8.08 (as amended 
and replaced by Rule 19A.13A) of the Listing Rules.

<<<PAGE 24>>>
24
Excluding the Offer Shares to be allocated to the cornerstone investor that are subject to a lock-
up period of six months following the Listing Date and the H Shares to be converted from 
Unlisted Shares that are subjected to a lock-up period of 12 months following the Listing Date, the 
Company’s H Shares to be counted towards the free float upon Listing will be 22,825,200 Shares. 
Based on the Offer Price of HK$26.36 per H Share, the free float of our Company is 6.85% and 
with a market value at the time of the Listing of approximately HK$601.67 million (immediately 
after the completion of the Global Offering and before any exercise of the Over-allotment Option). 
Accordingly, the Company will satisfy the free float requirement under Rule 19A.13C(1) of the 
Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering: (i) the 
Shares will be held by at least 300 Shareholders at the time of Listing, in compliance with Rule 
8.08(2) of the Listing Rules; (ii) the three largest public Shareholders will not hold more than 
50% of the H Shares held in public hands at the time of Listing, in compliance with Rules 8.08(3) 
and 8.24 of the Listing Rules; (iii) no placee will, individually, be placed more than 10% of the 
enlarged issued share capital of the Company immediately after the Global Offering; and (iv) there 
will not be any new substantial Shareholder (as defined in the Listing Rules) immediately after the 
Global Offering.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. (Hong Kong time) 
on Monday, May 11, 2026, provided that (i) the Global Offering has become unconditional 
in all respects, and (ii) the right of termination described in the section headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for 
termination” in the Prospectus has not been exercised. Investors who trade H Shares prior to the 
receipt of H Share certificates or the H Share certificates becoming valid evidence of title do so 
entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. (Hong Kong time) 
on Monday, May 11, 2026, it is expected that dealings in the H Shares on the Stock Exchange will 
commence at 9:00 a.m. on Monday, May 11, 2026 (Hong Kong time). The H Shares will be traded 
in board lots of 200 H Shares each and the stock code of the H Shares will be 1236.
By order of the Board
SHENZHEN LDROBOT CO., LTD
ZHOU Wei
Chairman of the Board
Hong Kong, May 8, 2026
As of the date of this announcement, the Board comprises Mr. ZHOU Wei, Mr. GUO Gaihua 
and Mr. ZHANG Jun as executive directors, Dr. HUANG Xi as non-executive director, and Mr. 
CHENG Hao, Dr. YAN Hongyu and Mr. HONG Kam Le as independent non-executive directors.
