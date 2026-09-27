# 配发结果公告抽取任务：3752.HK Rokae (Shandong) Robotics Group Inc. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**08/07/2026 21:49**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0708/2026070801234.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"3752.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
defined in the prospectus dated June 30, 2026 (the “Prospectus”) issued by Rokae (Shandong) Robotics Group Inc. (珞
石(山東)機器人集團股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an offer or an invitation to induce an 
offer by any person to acquire, purchase or subscribe for any securities of the Company. This announcement is not a 
prospectus. Potential investors should read the Prospectus for detailed information about the Company and the Global 
Offering described below before deciding whether or not to invest in the H Shares. Any investment decision in relation 
to the Offer Shares should be taken solely in reliance on the information provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not, and is not intended to, constitute or form a part of any offer to sell or solicitation to purchase 
or subscribe for any securities in the United States or in any other jurisdiction. The Offer Shares have not been, and 
will not be, registered under the U.S. Securities Act of 1933, as amended (the “U.S. Securities Act”) or securities law 
of any state or other jurisdiction of the United States and may not be offered, sold, pledged or otherwise transferred 
within the United States, except pursuant to an available exemption from, or in a transaction not subject to, the 
registration requirements of the U.S. Securities Act and in compliance with any applicable state securities laws. There 
will be no public offer of the Offer Shares in the United States. The Offer Shares are being offered and sold solely 
outside the United States in offshore transactions in reliance on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited 
as stabilizing manager (the “Stabilizing Manager”), its affiliates or any person acting for it, on behalf of the 
Underwriters, may over-allocate or effect transactions with a view to stabilizing or supporting the market price of 
the Shares at a level higher than that which might otherwise prevail in an open market for a limited period after the 
Listing Date. However, there is no obligation on the Stabilizing Manager, its affiliates or any person acting for it, 
to conduct any such stabilizing action, which, if commenced, will be conducted at the sole and absolute discretion 
of the Stabilizing Manager, its affiliates or any person acting for it, and may be discontinued at any time. Any such 
stabilizing activity is required to be brought to an end on the 30th day after the last date for lodging applications under 
the Hong Kong Public Offering (which is Wednesday, August 5, 2026). Such stabilization action, if commenced, may 
be effected in all jurisdictions where it is permissible to do so, in each case in compliance with all applicable laws, 
rules and regulatory requirements, including the Securities and Futures (Price Stabilizing) Rules (Chapter 571W of 
the Laws of Hong Kong), as amended, made under the Securities and Futures Ordinance (Chapter. 571 of the Laws of 
Hong Kong).
Potential investors should be aware that stabilizing actions cannot be taken to support the price of the Shares for longer 
than the stabilization period which will begin on the Listing Date and is expected to expire on the 30th day after the 
last day for lodging applications under the Hong Kong Public Offering (which is Wednesday, August 5, 2026). After 
this date, no further stabilizing action may be taken, and demand for the H Shares and therefore the price of the H 
Shares could fall.
Potential investors of the Offer Shares should note that the Joint Sponsors and Sponsor-Overall Coordinators 
(for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong Kong 
Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the section headed 
“Underwriting – Underwriting Arrangements – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on 
Thursday, July 9, 2026).
In connection with the Global Offering, the Company is expected to grant the Over-allotment Option to the 
International Underwriters, exercisable by the Overall Coordinators (for themselves and on behalf of the International 
Underwriters). Pursuant to the Over-allotment Option, the International Underwriters will have the right, exercisable 
by the Overall Coordinators (for themselves and on behalf of the International Underwriters) at any time from the 
Listing Date until 30 days after the last day for lodging applications under the Hong Kong Public Offering (which 
is Wednesday, August 5, 2026), to require the Company to issue and allot up to an additional 3,454,700 H Shares, 
representing 15% of the total number of Offer Shares, at the Offer Price, to cover over-allocations in the International 
Offering, if any.

<<<PAGE 2>>>
2
ROKAE (SHANDONG) ROBOTICS GROUP INC.
珞石( 山東) 機器人集團股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the 
Global Offering
:
23,031,900 H Shares (subject to the  
 Over-allotment Option)
Number of Hong Kong Offer Shares
:
2,303,200 H Shares
Number of International Offer Shares
:
20,728,700 H Shares (subject to the  
 Over-allotment Option)
Offer Price
:
HK$38.00 per H Share, plus brokerage 
 of 1.0%, SFC transaction levy 
 of 0.0027%, AFRC transaction levy 
 of 0.00015%, and Hong Kong 
 Stock Exchange trading fee of 0.00565%
Nominal value
:
RMB0.1 per H Share
Stock code
:
3752
Joint Sponsors, Overall Coordinators, Joint Global Coordinators,  
Joint Bookrunners and Joint Lead Managers
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
ROKAE (SHANDONG) ROBOTICS GROUP INC.
珞石( 山東) 機器人集團股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated June 30, 2026 (the “Prospectus”) issued by Rokae (Shandong) Robotics Group Inc. (珞
石(山東)機器人集團股份有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
3752
Stock short name
ROKAE ROBOTICS
Dealings commencement date
July 9, 2026
Price Information
Offer Price
HK$38.00
Offer Shares and Share Capital
Number of Offer Shares (assuming the Over-allotment 
Option is not exercised)
23,031,900
Number of Offer Shares in Hong Kong Public Offering
2,303,200
Number of Offer Shares in International Offering
20,728,700
Number of issued Shares upon Listing (assuming the 
Over-allotment Option is not exercised)
261,726,190
Over-allocation
No. of Offer Shares over-allocated Note
3,454,700
Note: Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases in the 
secondary market at prices that do not exceed the Offer Price or through deferred delivery or a combination 
of these means. In the event the Over-allotment Option is exercised, an announcement will be made on the 
Stock Exchange’s website.
Proceeds
Gross proceeds Note
HK$875.2 million
Less:  Estimated listing expenses payable based on the 
Offer Price
HK$64.7 million
Net proceeds
HK$810.5 million
Note: Gross proceeds refer to the amount to which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” in the Prospectus. The 
Company will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if 
any) for the purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus 
on a pro rata basis.

<<<PAGE 4>>>
4
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
63,360
No. of successful applications
11,937
Subscription level
156.58 times
Reallocation
N/A
No. of Offer Shares initially available under the Hong Kong 
Public Offering
2,303,200
Final no. of Offer Shares under the Hong Kong Public 
Offering
2,303,200
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering
10.00%
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/IPOResult to perform a search by identification number or www.tricor.com.hk/ipo/result for 
the full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
72
Subscription Level
11.96 times
No. of Offer Shares initially available under the 
International Offering
20,728,700
Final no. of Offer Shares under the International Offering
20,728,700
% of Offer Shares under the International Offering to the 
Global Offering
90.00%
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive of the Company, Controlling Shareholders, 
substantial shareholders, existing shareholders of the Company or any of its subsidiaries or their 
respective close associates; and (ii) none of the placees and the public who have purchased the 
Offer Shares are accustomed to taking instructions from the Company, any of the Directors, 
chief executive of the Company, Controlling Shareholders, substantial shareholders, existing 
shareholders of the Company or any of its subsidiaries or their respective close associates in 
relation to the acquisition, disposal, voting or other disposition of H Shares registered in his/her/its 
name or otherwise held by him/her/it.

<<<PAGE 6>>>
6
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
Option is not 
exercised)
% of total 
issued Shares 
after the 
Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised)
Existing 
shareholders 
or their close 
associates
GF Management Co., Ltd.
（廣發基金管理有限公司）
1,031,000
4.48%
0.39%
No
GF International Investment Management 
Limited（廣發國際資產管理有限公司）
HUATAI CAPITAL INVESTMENT 
LIMITED（華泰資本投資有限公司）
1,237,200
5.37%
0.47%
No
Beijing Financial Street Capital Operation 
Group Co., Ltd.（北京金融街資本運營
集團有限公司）
3,026,600
13.14%
1.16%
No
Yishao Capital Management (HK) Limited
309,300
1.34%
0.12%
No
All View Focus Fund LPF
1,629,000
7.07%
0.62%
No
Total
7,233,100
31.40%
2.76%
Note:
1. 
For details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in the 
Prospectus.

<<<PAGE 7>>>
7
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of 
Shares held or 
controlled in the 
Company subject 
to lock-up 
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
Shares subject 
to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised)
Last day subject to the lock-up 
undertakings Note 1
Mr. Tuo Hua (庹華)
92,572,610 Shares 
(including 
80,637,900 H Shares) Note 2
32.28%
35.37%
July 8, 2027 Note 1
Zoucheng Ruluo Brothers Enterprise 
 Management Consulting 
 Partnership (Limited Partnership) 
 (鄒城如珞兄弟企業管理諮詢
 合夥企業(有限合夥))
20,249,560 H Shares
8.11%
7.74%
July 8, 2027 Note 1
Zoucheng Luoshi Brothers 
 Management Consulting 
 Partnership (Limited Partnership) 
 (鄒城珞石兄弟管理諮詢
 合夥企業(有限合夥))
16,612,760 H Shares
6.65%
6.35%
July 8, 2027 Note 1
Notes:
1. 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law. The required lock-up for the Controlling Shareholders ends on July 8, 2027, 
being the date twelve months following the Listing Date. For illustrative purposes only, this subsection lists only those members of the Controlling Shareholders who hold Shares 
directly in the Company. Pursuant to Rule 10.07 of the Listing Rules, each Controlling Shareholder (namely, Mr. Tuo Hua, Zoucheng Ruluo Brothers Enterprise Management 
Consulting Partnership (Limited Partnership) and Zoucheng Luoshi Brothers Management Consulting Partnership (Limited Partnership)) has undertaken to the Stock Exchange and the 
Company that he or it shall comply with the applicable lock-up requirements. For further details, please refer to the section headed “Underwriting — Underwriting Arrangements — 
Hong Kong Public Offering — Undertakings Pursuant to the Listing Rules — Undertakings by the Controlling Shareholders” in the Prospectus.
2. 
Pursuant to the voting proxy agreements dated August 28, 2018, September 1, 2025, December 27, 2024 (reconfirmed and restated on November 5, 2025) and September 1, 2025, 
respectively, Mr. Tuo Hua is entitled to exercise the voting rights attached to the Shares held by Tibet Meiling Huakai Investment Partnership (Limited Partnership) (西藏梅嶺花開投
資合夥企業(有限合夥)), Hubei Meihua Shengshi Equity Investment Partnership (Limited Partnership) (湖北梅花晟世股權投資合夥企業(有限合夥)), Shandong Zhengfang High-tech 
Industry Holdings Group Co., Ltd. (山東正方高新產業控股集團有限公司) and Jiaxing Yuanshi Equity Investment Partnership (Limited Partnership) (嘉興元石股權投資合夥企業(有
限合夥)). For further details, please refer to the section headed “Relationship with Our Controlling Shareholders” in the Prospectus.

<<<PAGE 8>>>
8
Existing Shareholders (other than Controlling Shareholders) and Pre-IPO Investors
Name
Number of Shares 
held or controlled 
in the Company subject 
to lock-up undertakings 
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
Shares subject to 
lock-up undertakings 
upon Listing 
(assuming the Over-
allotment Option is 
not exercised)
Last day subject 
to the lock-up 
undertakings Note 1
National Manufacturing Transform and 
 Upgrade Fund Co., Ltd. 
 (國家製造業轉型升級基金股份
 有限公司)
23,076,920 H Shares
9.24%
8.82%
July 8, 2027 Note 1
South Hope Industry Co., Ltd. 
 (南方希望實業有限公司)
16,603,330 H Shares
6.65%
6.34%
July 8, 2027 Note 1
Golden Growth III (Hong Kong) Limited 
 (金色成長叁(香港)有限公司)
15,376,670 H Shares
6.16%
5.88%
July 8, 2027 Note 1
Xiang He Fund II, L.P.
14,041,590 H Shares
5.62%
5.36%
July 8, 2027 Note 1
Tibet Meiling Huakai Investment 
 Partnership (Limited Partnership) 
 (西藏梅嶺花開投資合夥企業
 (有限合夥)) Note 2
10,088,680 H Shares
4.04%
3.85%
July 8, 2027 Note 1
Pinghu Jinluo Equity Investment 
 Partnership (Limited Partnership) 
 (平湖金珞股權投資合夥企業
 (有限合夥))
8,790,440 H Shares
3.52%
3.36%
July 8, 2027 Note 1
Tianjin Yuanyi Yongxuan Enterprise 
 Management Center 
 (Limited Partnership)
  (天津遠翼永宣企業管理中心
 (有限合夥))
8,268,100 H Shares
3.31%
3.16%
July 8, 2027 Note 1
TR Victory Limited
7,857,580 H Shares
3.15%
3.00%
July 8, 2027 Note 1
Shenzhen Capital Group Co., Ltd. 
 (深圳市創新投資集團有限公司)
6,936,120 H Shares
2.78%
2.65%
July 8, 2027 Note 1
Jiaxing Yuanshi Equity Investment 
 Partnership (Limited Partnership) 
 (嘉興元石股權投資合夥企業
 (有限合夥)) Note 2
6,897,120 H Shares
2.76%
2.64%
July 8, 2027 Note 1

<<<PAGE 9>>>
9
Name
Number of Shares 
held or controlled 
in the Company subject 
to lock-up undertakings 
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
Shares subject to 
lock-up undertakings 
upon Listing 
(assuming the Over-
allotment Option is 
not exercised)
Last day subject 
to the lock-up 
undertakings Note 1
Zoucheng New Energy Industrial 
 Investment Fund Partnership 
 (Limited Partnership) 
 (鄒城市新動能產業投資基金合夥
 企業)(有限合夥)
5,769,230 H Shares
2.31%
2.20%
July 8, 2027 Note 1
Shandong Zhengfang High-tech Industry 
 Holdings Group Co., Ltd. 
 (山東正方高新產業控股集團
 有限公司) Note 2
4,903,850 H Shares
1.96%
1.87%
July 8, 2027 Note 1
Jining Zoulu Robotics Industrial 
 Investment Partnership 
 (Limited Partnership) 
 (濟寧市鄒魯機器人產業投資合夥企業
 (有限合夥))
4,762,430 H Shares
1.91%
1.82%
July 8, 2027 Note 1
Suzhou Jinsha River United III Equity 
 Investment Partnership 
 (Limited Partnership) 
 (蘇州金沙江聯合三期股權
 投資合夥企業(有限合夥))
4,693,390 H Shares
1.88%
1.79%
July 8, 2027 Note 1
Gongqingcheng Suxiang Venture 
 Investment Partnership 
 (Limited Partnership) 
 (共青城蘇襄創業投資合夥企業
 (有限合夥))
4,434,180 H Shares
1.78%
1.69%
July 8, 2027 Note 1
Yixing Environmental Science Park 
 Guangkong Industrial Investment 
 Partnership (Limited Partnership) 
 (宜興環科園光控產業投資合夥企業
 (有限合夥))
4,105,430 H Shares
1.64%
1.57%
July 8, 2027 Note 1
Tibet Fenglong Xinglian Investment 
 Center (L.P.) 
 (西藏豐隆興聯投資中心(有限合夥))
4,087,500 H Shares
1.64%
1.56%
July 8, 2027 Note 1

<<<PAGE 10>>>
10
Name
Number of Shares 
held or controlled 
in the Company subject 
to lock-up undertakings 
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
Shares subject to 
lock-up undertakings 
upon Listing 
(assuming the Over-
allotment Option is 
not exercised)
Last day subject 
to the lock-up 
undertakings Note 1
Qingkong Yinxing Nantong Venture 
 Investment Fund Partnership 
 (清控銀杏南通創業投資基金合夥企業
 (有限合夥)
2,985,780 H Shares
1.20%
1.14%
July 8, 2027 Note 1
Huida Luxin Venture Investment Fund 
 (Jining) Partnership 
 (Limited Partnership) 
 (惠達魯信創業投資基金(濟寧)合夥
 企業(有限合夥))
2,873,800 H Shares
1.15%
1.10%
July 8, 2027 Note 1
Yankuang Capital Management Co., Ltd. 
 (兖礦資本管理有限公司)
2,823,380 H Shares
1.13%
1.08%
July 8, 2027 Note 1
Jiaxing Tianqi Zefeng Equity Investment 
 Partnership (Limited Partnership) 
 (嘉興天啟澤楓股權投資合夥企業
 (有限合夥))
2,463,260 H Shares
0.99%
0.94%
July 8, 2027 Note 1
Beijing Yitang Hongtu Integrated Circuits 
 and Internet Investment Fund Center 
 (Limited Partnership) 
 (北京屹唐紅土集成電路與互聯網投資
 基金中心(有限合夥))
1,837,080 H Shares
0.74%
0.70%
July 8, 2027 Note 1
Hubei Meihua Shengshi Equity 
 Investment Partnership 
 (Limited Partnership) 
 (湖北梅花晟世股權投資合夥企業
 (有限合夥)) Note 2
1,700,530 H Shares
0.68%
0.65%
July 8, 2027 Note 1
Quanzhou Shanyue Innovation Equity 
 Investment Partnership 
 (Limited Partnership) 
 (泉州山月創新股權投資合夥企業
 (有限合夥))
1,424,490 H Shares
0.57%
0.54%
July 8, 2027 Note 1
Ms. Jiao Shaoling (焦少玲)
820,930 H Shares
0.33%
0.31%
July 8, 2027 Note 1
Mr. Zhang Yong (張勇)
766,350 H Shares
0.31%
0.29%
July 8, 2027 Note 1
Tianjin Qihui Enterprise Management 
 Center (Limited Partnership) 
 (天津啟輝企業管理中心(有限合夥))
505,070 H Shares
0.20%
0.19%
July 8, 2027 Note 1

<<<PAGE 11>>>
11
Name
Number of Shares 
held or controlled 
in the Company subject 
to lock-up undertakings 
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
Shares subject to 
lock-up undertakings 
upon Listing 
(assuming the Over-
allotment Option is 
not exercised)
Last day subject 
to the lock-up 
undertakings Note 1
Ms. Tian Zheng (田爭)
410,460 H Shares
0.16%
0.16%
July 8, 2027 Note 1
Suzhou Zhongxin Botong Jinshi Venture 
 Investment Partnership 
 (Limited Partnership) 
 (蘇州中新博通金世創業投資合夥企業
 (有限合夥))
408,170 H Shares
0.16%
0.16%
July 8, 2027 Note 1
Notes:
1. 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law. The required lock-up for the Existing Shareholders (other than Controlling 
Shareholders) and Pre-IPO Investors ends on July 8, 2027, being the date twelve months following the Listing Date.
2. 
Pursuant to the voting proxy agreements dated August 28, 2018, September 1, 2025, December 27, 2024 (reconfirmed and restated on November 5, 2025) and September 1, 2025, 
respectively, Mr. Tuo Hua is entitled to exercise the voting rights attached to the Shares held by Tibet Meiling Huakai Investment Partnership (Limited Partnership) (西藏梅嶺花開投
資合夥企業(有限合夥)), Hubei Meihua Shengshi Equity Investment Partnership (Limited Partnership) (湖北梅花晟世股權投資合夥企業(有限合夥)), Shandong Zhengfang High-tech 
Industry Holdings Group Co., Ltd. (山東正方高新產業控股集團有限公司) and Jiaxing Yuanshi Equity Investment Partnership (Limited Partnership) (嘉興元石股權投資合夥企業(有
限合夥)). For further details, please refer to the section headed “Relationship with Our Controlling Shareholders” in the Prospectus.

<<<PAGE 12>>>
12
Cornerstone Investors
Investor
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
% of total issued 
Shares subject to 
lock-up undertakings 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)
Last day subject 
to the lock-up 
undertakings Note 1
GF Management Co., Ltd. (廣發基金管理有限公司)
1,031,000
0.39%
January 8, 2027
GF International Investment Management Limited 
(廣發國際資產管理有限公司)
HUATAI CAPITAL INVESTMENT LIMITED 
(華泰資本投資有限公司)
1,237,200
0.47%
January 8, 2027
Beijing Financial Street Capital Operation Group Co., Ltd. 
(北京金融街資本運營集團有限公司)
3,026,600
1.16%
January 8, 2027
Yishao Capital Management (HK) Limited
309,300
0.12%
January 8, 2027
All View Focus Fund LPF
1,629,000
0.62%
January 8, 2027
Note:
1. 
For further information, please refer to the “Cornerstone Investors” section in the Prospectus.
2. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on January 8, 2027. The Cornerstone Investors will cease to be prohibited from 
disposing of or transferring H Shares subscribed for pursuant to the relevant cornerstone investment agreements after the indicated date.
PLACEE CONCENTRATION ANALYSIS
Placees Note 1
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
Option is fully 
exercised and 
new H Shares 
are issued)
Top 1
3,026,600
14.60%
12.52%
13.14%
11.43%
3,026,600
1.16%
1.14%
Top 5
11,338,000
54.70%
46.88%
49.23%
42.81%
11,338,000
4.33%
4.28%
Top 10
18,675,200
90.09%
77.22%
81.08%
70.51%
18,675,200
7.14%
7.04%
Top 25
23,696,200
114.32%
97.99%
102.88%
89.46%
23,696,200
9.05%
8.94%
Note:
1. 
Ranking of placees is based on the number of Shares allotted to the placees.

<<<PAGE 13>>>
13
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders 
Note 1
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
% of total 
issued H Shares 
upon 
Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
% of total 
issued 
H Shares upon 
Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Top 1
0
0.00%
0.00%
0.00%
0.00%
80,637,900
32.28%
31.84%
Top 5
0
0.00%
0.00%
0.00%
0.00%
149,736,410
59.94%
59.13%
Top 10
0
0.00%
0.00%
0.00%
0.00%
200,411,390
80.23%
79.14%
Top 25
17,438,000
84.12%
72.11%
75.71%
65.84%
241,694,770
96.76%
95.44%
 
Note:
1. 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
SHAREHOLDERS CONCENTRATION ANALYSIS
Shareholders 
Note 1
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
Number of 
Shares held 
upon Listing
% of total 
issued Shares 
upon 
Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
% of total 
issued Shares 
upon 
Listing 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new H Shares 
are issued)
Top 1
0
0.00%
0.00%
0.00%
0.00%
80,637,900
92,572,610
35.37%
34.91%
Top 5
0
0.00%
0.00%
0.00%
0.00%
149,736,410
161,671,120
61.77%
60.97%
Top 10
0
0.00%
0.00%
0.00%
0.00%
200,411,390
212,346,100
81.13%
80.08%
Top 25
17,438,000
84.12%
72.11%
75.71%
65.84%
241,694,770
253,629,480
96.91%
95.64%
Note:
1. 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon 
Listing.

<<<PAGE 14>>>
14
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 63,360 valid 
applications made by the public will be conditionally allocated on the basis set out below:
Pool A
Number of 
H Shares 
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
100
31,222
3,123 out of 31,222 to receive 100 H Shares
10.00%
200
12,125
1,547 out of 12,125 to receive 100 H Shares
6.38%
300
2,481
365 out of 2,481 to receive 100 H Shares
4.90%
400
703
115 out of 703 to receive 100 H Shares
4.09%
500
1,078
190 out of 1,078 to receive 100 H Shares
3.53%
600
422
80 out of 422 to receive 100 H Shares
3.16%
700
267
53 out of 267 to receive 100 H Shares
2.84%
800
380
79 out of 380 to receive 100 H Shares
2.60%
900
196
43 out of 196 to receive 100 H Shares
2.44%
1,000
4,782
1,075 out of 4,782 to receive 100 H Shares
2.25%
1,500
822
213 out of 822 to receive 100 H Shares
1.73%
2,000
742
213 out of 742 to receive 100 H Shares
1.44%
2,500
739
230 out of 739 to receive 100 H Shares
1.24%
3,000
552
183 out of 552 to receive 100 H Shares
1.11%
3,500
232
81 out of 232 to receive 100 H Shares
1.00%
4,000
268
98 out of 268 to receive 100 H Shares
0.91%
4,500
177
68 out of 177 to receive 100 H Shares
0.85%
5,000
530
210 out of 530 to receive 100 H Shares
0.79%
6,000
398
168 out of 398 to receive 100 H Shares
0.70%
7,000
243
109 out of 243 to receive 100 H Shares
0.64%
8,000
276
129 out of 276 to receive 100 H Shares
0.58%
9,000
153
75 out of 153 to receive 100 H Shares
0.54%
10,000
1,225
618 out of 1,225 to receive 100 H Shares
0.50%
20,000
637
410 out of 637 to receive 100 H Shares
0.32%
30,000
507
377 out of 507 to receive 100 H Shares
0.25%
40,000
224
184 out of 224 to receive 100 H Shares
0.21%
50,000
638
567 out of 638 to receive 100 H Shares
0.18%
60,000
137
130 out of 137 to receive 100 H Shares
0.16%
70,000
86
100 H Shares
0.14%
80,000
95
100 H Shares plus 5 out of 95 applicants to receive an additional 100 H Shares
0.13%
90,000
65
100 H Shares plus 6 out of 65 applicants to receive an additional 100 H Shares
0.12%
100,000
464
100 H Shares plus 62 out of 464 applicants to receive an additional 100 H Shares
0.11%
Total
62,866
Total number of Pool A successful applicants: 11,443

<<<PAGE 15>>>
15
Pool B
Number of 
H Shares 
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
200,000
297
1,600 H Shares
0.80%
300,000
63
2,100 H Shares
0.70%
400,000
29
2,600 H Shares
0.65%
500,000
31
3,100 H Shares
0.62%
600,000
13
3,600 H Shares
0.60%
700,000
9
4,100 H Shares
0.59%
800,000
12
4,600 H Shares
0.58%
900,000
2
5,000 H Shares
0.56%
1,000,000
8
5,400 H Shares
0.54%
1,151,600
30
6,000 H Shares plus 5 out of 30 applicants to receive 
 an additional 100 H Shares
0.52%
Total
494
Total number of Pool B successful applicants: 494
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the Offer Price in addition to any brokerage, AFRC transaction 
levy, SFC transaction levy and trading fee payable.

<<<PAGE 16>>>
16
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the 
“Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no 
responsibility for the contents of this announcement, make no representation as to its accuracy 
or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising 
from or in reliance upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and the 
District of Columbia). This announcement does not, and is not intended to, constitute or form a 
part of any offer to sell or solicitation to purchase or subscribe for any securities in the United 
States or in any other jurisdiction. The Offer Shares have not been, and will not be, registered 
under the U.S. Securities Act of 1933, as amended (the “U.S. Securities Act”) or securities law 
of any state or other jurisdiction of the United States and may not be offered, sold, pledged or 
otherwise transferred within the United States, except pursuant to an available exemption from, 
or in a transaction not subject to, the registration requirements of the U.S. Securities Act and in 
compliance with any applicable state securities laws. There will be no public offer of the Offer 
Shares in the United States.
The Offer Shares are being offered and sold solely outside the United States in offshore 
transactions in reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an offer or an 
invitation to induce an offer by any person to acquire, purchase or subscribe for any securities 
of the Company. This announcement is not a prospectus. Potential investors should read the 
Prospectus dated June 30, 2026 issued by the Company for detailed information about the 
Company and the Global Offering described below before deciding whether or not to invest in 
the Shares. Any investment decision in relation to the Offer Shares should be taken solely in 
reliance on the information provided in the Prospectus.
* 
Potential investors of the Offer Shares should note that the Joint Sponsors and Sponsor-
Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall 
be entitled to terminate the Hong Kong Underwriting Agreement with immediate effect 
upon the occurrence of any of the events set out in the section headed “Underwriting – 
Underwriting Arrangements – Hong Kong Public Offering – Grounds for Termination” in 
the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which 
is currently expected to be on Thursday, July 9, 2026).

<<<PAGE 17>>>
17
PUBLIC FLOAT AND FREE FLOAT
Immediately following completion of the Global Offering, based on the Offer Price of HK$38.00 
per H Share, the expected market capitalization of the Company’s H Shares upon the Listing is 
HK$9,492 million and the minimum prescribed public float percentage applicable to the H Shares 
is 15.08%. Immediately following completion of the Global Offering, an aggregate of 169,153,580 
H Shares representing approximately 64.63% of the issued share capital of the Company will be 
held in the public hands, which is higher than the prescribed percentage of H Shares required to be 
held in public hands of 15.08% under Rule 19A.13A(1) of the Listing Rules, satisfying the public 
float requirement under Rule 19A.13A(1) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing shall not be 
counted towards the free float of the Shares of the Company at the time of Listing. Based on the 
Offer Price of HK$38.00 per H Share, the Company satisfies the free float requirement under Rule 
19A.13C(1)(b) of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering (before any 
exercise of the Over-allotment Option): (i) no placee will, individually, be placed more than 10% 
of the enlarged issued share capital of the Company immediately after the Global Offering; (ii) 
there will not be any new substantial Shareholder under the Listing Rules immediately after the 
Global Offering; (iii) the three largest public shareholders of the Company do not hold more than 
50% of the Shares in public hands at the time of the Listing in compliance with Rules 8.08(3) and 
8.24 of the Listing Rules; and (iv) there will be at least 300 Shareholders at the time of the Listing 
in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
Share certificates will only become valid evidence of title at 8:00 a.m. on Thursday, July 9, 2026 
(Hong Kong time), provided that the Global Offering has become unconditional and the right of 
termination described in the section headed “Underwriting – Underwriting Arrangements – Hong 
Kong Public Offering – Grounds for Termination” in the Prospectus has not been exercised. 
Investors who trade H Shares prior to the receipt of H Share certificates or the H Share certificates 
becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Thursday, July 
9, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange will 
commence at 9:00 a.m. on Thursday, July 9, 2026 (Hong Kong time). The H Shares will be traded 
in board lots of 100 H Shares each. The stock code of the H Shares will be 3752.
By order of the Board
Rokae (Shandong) Robotics Group Inc.
Mr. Tuo Hua
Chairman of the Board,
Executive Director and General Manager
Hong Kong, July 8, 2026
As at the date of this announcement, the Board comprises: (i) Mr. Tuo Hua, Mr. Tang Shengtian, 
Dr. Wang Hao, Mr. Song Bin and Mr. Zhang Lei as executive Directors; (ii) Mr. Yu Shihua as 
a non-executive Director; and (iii) Mr. Zhang Peilin, Ms. Zhang Rui and Ms. Chan Maria as 
independent non-executive Directors.
