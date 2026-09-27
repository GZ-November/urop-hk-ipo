# 配发结果公告抽取任务：9976.HK Shenzhen Longsys Electronics Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**07/09/2026 21:39**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0907/2026090701319.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"9976.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”, 
or the “Hong Kong Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no 
responsibility for the contents of this announcement, make no representation as to its accuracy or completeness and 
expressly disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated August 31, 2026 (the “Prospectus”) of Shenzhen Longsys Electronics Co., Ltd. (深圳
市江波龍電子股份有限公司) (the “Company”). This announcement is made by the order of the board (the “Board”) 
of directors (the “Directors”) of the Company. The Board collectively and individually accept responsibility for the 
accuracy of this announcement.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for any securities. This announcement is not a prospectus. Potential investors should read the Prospectus 
for detailed information about the Global Offering described below before deciding whether or not to invest in 
the Offer Shares. Any investment decision in relation to the Offer Shares should be taken solely in reliance on the 
information provided in the Prospectus.
This announcement is not for release, publication or distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia or any other 
jurisdiction where such distribution is prohibited by laws). This announcement does not constitute or form a part of 
any offer or solicitation to purchase or subscribe for securities in the United States or in any other jurisdictions. The 
securities mentioned herein have not been, and will not be, registered under the United States Securities Act of 1933 
as amended from time to time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the 
United States. The securities may not be offered, sold, pledged or otherwise transferred within the United States, 
except pursuant to an available exemption from, or in a transaction not subject to, the registration requirements of the 
U.S. Securities Act and in accordance with any applicable state securities laws in the United States. The Offer Shares 
may only be offered and sold (a) in the United States to QIBs in reliance on Rule 144A or another available exemption 
from registration requirements under the U.S. Securities Act, and (b) outside the United States in offshore transactions 
in reliance on Regulation S. There will be no public offer of securities in the United States.
In connection with the Global Offering, CLSA Limited as stabilizing manager (the “Stabilizing Manager”) (or its 
affiliates or any person acting for it), on behalf of the Underwriters, to the extent permitted by the applicable laws and 
regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect transactions with a view to stabilizing 
or supporting the market price of the H Shares at such price, in such amounts and in such manners as the Stabilizing 
Manager, its affiliates or any person acting for it may determine and at a level higher than that which might otherwise 
prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilizing Manager (or its 
affiliates or any person acting for it) to conduct any such stabilizing action. Such stabilizing action, if taken, (a) will 
be conducted at the absolute discretion of the Stabilizing Manager (or its affiliates or any person acting for it) and in 
what the Stabilizing Manager reasonably regards as the best interest of the Company, (b) may be discontinued at any 
time and (c) is required to be brought to an end within 30 days of the last day for lodging applications under the Hong 
Kong Public Offering (which is Saturday, October 3, 2026). Such Stabilizing action, if taken, may be effected in all 
jurisdictions where it is permissible to do so, in each case in compliance with all applicable laws, rules and regulatory 
requirements, including the Securities and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong 
Kong), as amended, made under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering (which is Saturday, October 3, 2026). 
After this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the price of 
the H Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to terms and conditions set out in 
the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not 
resident in Hong Kong. Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate the Hong 
Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the section 
headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. on the Listing Date.

<<<PAGE 2>>>
2
Shenzhen Longsys Electronics Co., Ltd.
深圳市江波龍電子股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the
Global Offering
:
29,989,450 H Shares (taking into account 
 the full exercise of the Offer Size 
 Adjustment Option and subject to the 
 Over-allotment Option)
Number of Hong Kong Offer Shares
:
2,607,800 H Shares
Number of International Offer Shares
:
27,381,650 H Shares (taking into account 
 the full exercise of the Offer Size 
 Adjustment Option and subject to 
 the Over-allotment Option)
Final Offer Price
:
HK$236.00 per H Share plus brokerage 
 of 1%, SFC transaction levy of 
 0.0027%, Stock Exchange trading fee 
 of 0.00565% and AFRC transaction 
 levy of 0.00015%
Nominal value
:
RMB1.00 per H Share
Stock code
:
09976
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators,
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
SHENZHEN LONGSYS ELECTRONICS CO., LTD.
深圳市江波龍電子股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated August 31, 2026 (the “Prospectus”) issued by 
Shenzhen Longsys Electronics Co., Ltd. (深圳市江波龍電子股份有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of H 
Shareholders, H Shareholders and prospective investors should be aware that the price of 
the H Shares could move substantially even with a small number of H Shares traded and 
should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
09976
Stock short name
LONGSYS
Dealings commencement date
September 8, 2026*
* 
see note at the end of the announcement
Price Information
Final Offer Price
HK$236.00
Maximum Offer Price
HK$240.60
Offer Shares and Share Capital
Number of Offer Shares (taking into account the full exercise 
of the Offer Size Adjustment Option and before exercise of 
the Over-allotment Option)
29,989,450
Number of Offer Shares in Hong Kong Public Offering
2,607,800
Number of Offer Shares in International Offering (taking into 
account the full exercise of the Offer Size Adjustment Option 
and before exercise of the Over-allotment Option)
27,381,650
Number of issued Shares upon Listing (taking into account the 
full exercise of the Offer Size Adjustment Option and before 
exercise of the Over-allotment Option)
459,657,599

<<<PAGE 4>>>
4
Offer Size Adjustment Option (Upsize option)
Number of additional shares issued under the option
3,911,650
– Hong Kong Public Offering
–
– International Offering
3,911,650
The Offer Size Adjustment Option was exercised in full, pursuant to which the Company is issuing and allotting 
3,911,650 additional Offer Shares, representing approximately 15.0% of the Offer Shares initially being offered 
under the Global Offering, at the Offer Price.
The additional Offer Shares issued pursuant to the Offer Size Adjustment Option will be allocated to the 
International Offering.
Over-allocation
Number of Offer Shares over-allocated
4,498,400
International Offering 
4,498,400
Such over-allocation may be covered by exercising the Over-allotment Option or by making 
purchases in the secondary market at prices that do not exceed the Offer Price or through 
deferred delivery or a combination of these means. In the event the Over-allotment Option is 
exercised, an announcement will be made on the Stock Exchange’s website.
Proceeds
Gross proceeds
HK$7,077.5 million
Less: Estimated listing expenses payable based on Final 
Offer Price
HK$274.3 million
Net proceeds
HK$6,803.2 million
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The Company 
will adjust the allocation of the net proceeds from the exercise of the Over-allotment Option (if any) for the 
purposes as set out in the section headed “Future Plans and Use of Proceeds” of the Prospectus on a pro rata basis.

<<<PAGE 5>>>
5
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
Number of valid applications
36,285
Number of successful applications
10,568
Subscription level
40.32 times
Claw-back triggered
N/A
Number of Offer Shares initially available under the Hong Kong 
Public Offering
2,607,800
Number of Offer Shares reallocated from the International Offering 
0
Final number of Offer Shares under the Hong Kong Public Offering
2,607,800
% of final number of Offer Shares under the Hong Kong Public Offering 
to the Global Offering (after taking into account the full exercise of the 
Offer Size Adjustment Option)
8.70%
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can refer to 
www.eipo.com.hk/eIPOAllotment to perform a search by identification number or www.eipo.com.hk/eIPOAllotment 
for the full list of allottees. 

<<<PAGE 6>>>
6
INTERNATIONAL OFFERING
Number of placees
227
Subscription level (before taking into account the Offer Size Adjustment 
Option)
3.88 times
Number of Offer Shares initially available under the International 
Offering
23,470,000
Number of Offer Shares reallocated to the Hong Kong Public Offering 
0
Final number of Offer Shares under the International Offering (after 
taking into account the full exercise of the Offer Size Adjustment Option)
27,381,650
% of final number of Offer Shares under the International Offering 
to the Global Offering (after taking into account the full exercise of the 
Offer Size Adjustment Option)
91.30%
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a 
waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 
1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock 
Exchange to permit the Company to allocate certain Offer Shares in the International Offering to 
certain Existing Minority A Shareholders and/or their close associates, and (b) a consent under 
paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants to permit the Company 
to, among other things, allocate further H Shares in the International Offering to certain existing 
Shareholders and/or their close associates and Cornerstone Investors and/or their close associates, 
(i) none of the Offer Shares subscribed by the placees and the public have been financed directly 
or indirectly by the Company, any of its Directors, chief executive, Controlling Shareholders, 
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries or 
their respective close associates; and (ii) none of the placees and the public who have purchased 
the Offer Shares are accustomed to taking instructions from the Company, any of its Directors, 
chief executive, substantial Shareholders, Controlling Shareholders, existing Shareholders of the 
Company or any of its subsidiaries or their respective close associates in relation to the acquisition, 
disposal, voting or other disposition of H Shares registered in his/her/its name or otherwise held by 
him/her/it.

<<<PAGE 7>>>
7
The placees in the International Offering include the following: 
Cornerstone Investors
Investor
No. of Offer 
Shares 
allocated
Approximate % 
of total issued H 
Shares after the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (1) (2)
Approximate % 
of total issued 
share capital 
after the Global 
Offering (after 
taking into account 
the full exercise 
of the Offer 
Size Adjustment 
Option) (2)
Existing 
Shareholders 
(including 
2025 A Share 
Placees) or 
their close 
associates
Transsion International Limited
830,800
2.77%
0.18%
No
YuFeng Financial Group Limited (“YuFeng”)
– YuFeng(3)
332,300
1.11%
0.07%
No
– YuFeng Project 1 Limited Partnership 
 Fund (“YuFeng LPF”)(3)
332,300
1.11%
0.07%
No
Subtotal
664,600
2.22%
0.14%
CITIC Securities Asset Management 
(HK) Limited (中信證券資產管理(香
港)有限公司) (“CITIC AM HK”)(3)
635,550
2.12%
0.14%
Yes（4）
Admiralty Harbour Growth 
Opportunities SPC SP1 (“AHGO 
SPC”)(3)
423,700
1.41%
0.09%
No
Lenovo Group Limited (聯想集團有限
公司) (“Lenovo”)(3)
332,300
1.11%
0.07%
No
Lens Technology (HK) Co., Limited 
(藍思科技(香港)有限公司) (“Lens 
Technology HK”)(3)
332,300
1.11%
0.07%
No
Ingenic Semiconductor (Hong Kong) 
Group Limited (北京君正集成電
路(香港)集團有限公司) (“Ingenic 
Semiconductor HK”)
332,300
1.11%
0.07%
No
Ju Yuen (Hong Kong) International 
Limited (巨源(香港)國際有限公司) 
(“Ju Yuen International”)(3)
332,300
1.11%
0.07%
No
Colorful Technology Company Limited 
(七彩虹科技有限公司) (“Colorful 
Technology”)(3)
317,750
1.06%
0.07%
No

<<<PAGE 8>>>
8
Investor
No. of Offer 
Shares 
allocated
Approximate % 
of total issued H 
Shares after the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (1) (2)
Approximate % 
of total issued 
share capital 
after the Global 
Offering (after 
taking into account 
the full exercise 
of the Offer 
Size Adjustment 
Option) (2)
Existing 
Shareholders 
(including 
2025 A Share 
Placees) or 
their close 
associates
HOSIN Global (HK) Electronics Co., 
Limited (宏芯宇電子有限公司)
237,250
0.79%
0.05%
No
Huadeng Tech Bright Investment  
Ltd (“Huadeng”)(3)
166,150
0.55%
0.04%
No
Wind Sabre Fund SPC(3)
166,150
0.55%
0.04%
No
CQTech Limited (香港常青科技有限公
司)
166,150
0.55%
0.04%
No
SDMC Technology (Hong Kong) 
Limited (華曦達科技(香港)有限公司)
84,700
0.28%
0.02%
No
Notes:
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.
(2) 
Assuming the Over-allotment Option is not exercised.
(3) 
In addition to the Offer Shares subscribed for as Cornerstone Investors, YuFeng, YuFeng LPF, CITIC AM 
HK, AHGO SPC, Lenovo, Lens Technology HK, Ju Yuen International, Colorful Technology, Huadeng and 
Wind Sabre Fund SPC and/or their close associates, were allocated further Offer Shares as placees in the 
International Offering. Please refer to the section headed “Allotment Results Details — International Offering 
— Allottees with Waivers/Consents Obtained” in this announcement for details. Only the Offer Shares 
subscribed for as Cornerstone Investors are subject to lock-up as indicated below. For details, please refer to 
the section headed “Lock-up Undertakings — Cornerstone Investors” in this announcement.
(4) 
For details of the waiver from strict compliance with Rule 10.04 of the Listing Rules and prior consent 
under paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by existing minority 
Shareholders and/or close associates of existing Shareholders, please refer to the section headed “Others/
Additional Information — Allocation of H Shares to Existing Minority Shareholders and/or their close 
associates” in this announcement.

<<<PAGE 9>>>
9
Allottees with waivers/consents obtained
Investor
No. of Offer 
Shares allocated
Approximate % 
of total issued H 
Shares after the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (1) (2)
Approximate % 
of total issued 
share capital 
after the Global 
Offering (after 
taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (2)
Relationship
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 
1C(2) of the Placing Guidelines in relation to subscription for H Shares by Existing Minority Shareholders holding 
1% or more of the issued share capital of the Company immediately prior to the completion of the Global Offering 
and/or their close associates(3)
Nil
Nil
Nil
Nil
Nil
Allottees with consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to 
allocations of further H Shares to existing Shareholders and Cornerstone Investors and/or their close associates(4)
CITIC AM HK
435,100
1.45%
0.09%
Same entity as the 
Cornerstone Investor 
and a close associate 
of existing Shareholder
Admiralty Harbour 
 Capital Limited
381,350 
1.27%
0.08%
A close associate of a
Cornerstone Investor
YuFeng LPF
332,300
1.11%
0.07%
Same entity as the 
Cornerstone Investor
YuFeng
332,300
1.11%
0.07%
Same entity as the 
Cornerstone Investor
Lenovo
332,300
1.11%
0.07%
Same entity as the 
Cornerstone Investor
Lens Technology HK
332,300
1.11%
0.07%
Same entity as the 
Cornerstone Investor
Colorful Technology
317,750
1.06%
0.07%
Same entity as the 
Cornerstone Investor
Huadeng
166,150
0.55%
0.04%
Same entity as the 
Cornerstone Investor
WIND SABRE 
 CAPITAL 
 LIMITED
166,150
0.55%
0.04%
A close associate of a 
Cornerstone Investor

<<<PAGE 10>>>
10
Investor
No. of Offer 
Shares allocated
Approximate % 
of total issued H 
Shares after the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (1) (2)
Approximate % 
of total issued 
share capital 
after the Global 
Offering (after 
taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (2)
Relationship
Ju Yuen International
118,600
0.40%
0.03%
Same entity as the 
Cornerstone Investor
CITIC Securities Asset 
 Management Company 
 Limited (“CITIC AM”)
14,400
0.05%
0.003%
A close associate of a 
Cornerstone Investor 
and an existing Shareholder
Allottees who are 2025 A Share Placees and/or their close associates (5)
Cornerstone Investor
CITIC AM HK(6)
635,550
2.12%
0.14%
A close associate of a 2025 
A Share Placee
Placees
CITIC AM HK(6)
435,100
1.45%
0.09%
A close associate of a 2025 
A Share Placee
CITIC Securities
International Capital
Management Limited 
(“CSI”)(7)
830,800
2.77%
0.18%
A close associate of a 2025 
A Share Placee
CITIC AM(8)
14,400
0.05%
0.003%
A close associate of a 2025 
A Share Placee
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations to connected clients(9)

<<<PAGE 11>>>
11
Investor
No. of Offer 
Shares allocated
Approximate % 
of total issued H 
Shares after the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (1) (2)
Approximate % 
of total issued 
share capital 
after the Global 
Offering (after 
taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (2)
Relationship
CITIC AM HK
635,550
2.12%
0.14%
Connected client as a 
Cornerstone Investor
435,100
1.45%
0.09%
Connected client as a placee
CSI
830,800
2.77%
0.18%
Connected client as a placee
CITIC AM
14,400
0.05%
0.003%
Connected client as a placee
Bosera Asset Management 
(International) Co., Limited 
(“Bosera International”)
598,200
1.99%
0.13%
Connected client as a placee
SDIC Securities Asset 
Management (Hong Kong) 
Limited (“SDICSAMHK”)
33,200
0.11%
0.01%
Connected client as a placee

<<<PAGE 12>>>
12
Notes:
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.
(2) 
Assuming the Over-allotment Option is not exercised.
(3) 
Among the Cornerstone Investors, CITIC AM HK is a close associate of an existing minority Shareholder. 
The Stock Exchange has granted a waiver from strict compliance with the requirements under Rule 10.04 
and consent under Paragraph 1C(2) of Appendix F1 to the Listing Rules and paragraph 17 of Chapter 4.15 of 
the Guide for New Listing Applicants to permit H Shares in the International Offering to be placed to certain 
existing minority Shareholders and/or their close associates. Please refer to the section headed “Waivers and 
Exemption — Allocation of Our H Shares to Existing Minority Shareholders and Their Close Associates 
under Rule 10.04 and Paragraph 1C(2) of Appendix F1 to the Listing Rules”of the Prospectus for details.
The Stock Exchange has granted the waiver on the condition that, among others, details of the allocation to 
the Existing Minority Shareholders and/or their close associates holding more than 1% of the issued share 
capital of the Company (including the treasury Shares) immediately prior to the completion of the Global 
Offering will be disclosed in the Prospectus and/or allotment results announcement.
(4) 
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents the 
number of Offer Shares allocated to the investors as placees in the International Offering. For allocations of 
Offer Shares to the relevant investors as Cornerstone Investors, please refer to the section headed “Allotment 
Results Details — International Offering — Cornerstone Investors” in this announcement. For details of 
the consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing Applicants in relation to 
allocations of further H Shares to the Cornerstone Investors, please refer to the section headed “Others/
Additional Information — Allocations of Offer Shares to the existing Shareholders and Cornerstone Investors 
and/or their close associates with a consent under paragraph 18 of Chapter 4.15 of the Guide for New Listing 
Applicants” in this announcement.
(5) 
Each of investors listed in this subsection has confirmed that (i) its decision to participate in the Global 
Offering is independent of any participation by any of its close associates in the 2025 A Shares Issuance; and 
(ii) no side agreement, bundling arrangement or other understanding exists linking any participation by any of 
its close associates in the 2025 A Shares Issuance with its participation in the Global Offering. The Overall 
Coordinators and the distributors through which such investors placed their orders have also confirmed that 
their allocation of H Shares under the Global Offering has been, and will be, conducted entirely separately 
and independently of the 2025 A Shares Issuance, and that no bundling arrangement, side agreement or other 
understanding linking participation in the 2025 A Shares Issuance with any allocation of H Shares under the 
Global Offering exists. To the best knowledge of the Company, none of the Cornerstone Investor, placee and/
or its respective ultimate beneficial owner is a 2025 A Share Placee, its close associate or ultimate beneficial 
owner, save for the relationship of close associate as disclosed in table above.
(6) 
CITIC AM HK, as a discretionary investment manager for certain managed accounts and funds, is a close 
associate of China Asset Management Co., Ltd. (“CAMC”), one of the 2025 A Share Placees. For further 
details of its managed accounts and funds, please refer to “Cornerstone Investors” in the Prospectus and Note 
3 to the table under the section headed “— Placing to connected clients with a consent under paragraph 1C(1) 
of the Placing Guidelines” in this announcement.
(7) 
CSI is a close associate of CAMC and will hold the Offer Shares on behalf of its ultimate clients, on a non-
discretionary basis. For details of its ultimate clients, please refer to Note 4 to the table under the section 
headed “— Placing to connected clients with a consent under paragraph 1C(1) of the Placing Guidelines” in 
this announcement.

<<<PAGE 13>>>
13
(8) 
CITIC AM, as a discretionary investment manager for certain managed funds, is a close associate of CAMC. 
For details of its managed funds, please refer to Note 5 to the table under the section headed “— Placing to 
connected clients with a consent under paragraph 1C(1) of the Placing Guidelines” in this announcement.
(9) 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations to connected clients, please refer to the sections headed 
“Others/Additional Information － Placing to connected clients with a consent under paragraph 1C(1) of 
the Placing Guidelines” and “Others/Additional Information － Allocations of Offer Shares to the existing 
Shareholders and Cornerstone Investors and/or their close associates with a consent under paragraph 18 of 
Chapter 4.15 of the Guide for New Listing Applicants” in this announcement.

<<<PAGE 14>>>
14
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name(6)
Number of 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-
up undertakings 
upon Listing 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (1)(2)
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon Listing 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (2)
Last day subject to the 
lock-up undertakings (3)
Mr. Cai Huabo 
 (蔡華波先生)
162,071,900
–
35.26%
March 7, 2027 (First 
Six-Month Period)(4)
September 7, 2027 
(Second Six-Month 
Period)(5)
Ms. Cai Lijiang 
 (蔡麗江女士)
14,700,000
–
3.20%
March 7, 2027 (First 
Six-Month Period)(4) 
September 7, 2027 
(Second Six-Month 
Period)(5)
Notes:
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.
(2) 
Assuming the Over-allotment Option is not exercised.
(3) 
In accordance with the applicable Listing Rules, the required lock-up for the first six-month period will end 
on March 7, 2027 and for the second six-month period will end on September 7, 2027.
(4) 
Each member of the Controlling Shareholders may dispose of or transfer Shares after the indicated date 
subject to that the any member of Controlling Shareholders will not cease to be a controlling shareholder (as 
defined in the Listing Rules).
(5) 
The Controlling Shareholders will cease to be prohibited from disposing of or transferring Shares after the 
indicated date.
(6) 
For illustrative purposes only, this subsection lists only those members of the Controlling Shareholders who 
hold Shares directly in the Company. Pursuant to Rule 10.07 of the Listing Rules, each of the Controlling 
Shareholders (namely, Mr. Cai Huabo and Ms. Cai Lijiang) has undertaken to the Company and the Stock 
Exchange that, except in connection with the Global Offering (including the Over-allotment Option), he/
she shall, and shall procure that the relevant registered holders of the Shares in which he/she is beneficially 
interested shall, comply with the applicable lock-up requirements. For further details, please refer to the 
section headed “Underwriting — Underwriting Arrangements and Expenses — Undertakings to the Hong 
Kong Stock Exchange pursuant to the Listing Rules” in the Prospectus.

<<<PAGE 15>>>
15
2025 A Share Placees
Name
Number of A 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon Listing 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (1)
Last day subject 
to the lock-up 
undertakings (2)
Zhao Qixiang (趙啟祥)
562,500
0.12%
February 16, 2027
Jin Changjiang (金長江)
714,285
0.16%
February 16, 2027
He Wei (賀偉)
535,714
0.12%
February 16, 2027
Wang Weimin (王偉民)
267,857
0.06%
February 16, 2027
Zhong Ge (鍾革)
267,857
0.06%
February 16, 2027
Yang Xiaobin (楊曉斌)
178,571
0.04%
February 16, 2027
Huang Haihua (黃海華)
178,571
0.04%
February 16, 2027
Zhang Xu (張旭)
178,571
0.04%
February 16, 2027
Xu Limin (許利民)
36,971
0.01%
February 16, 2027
E Fund Management Co., Ltd. (易方達基金
管理有限公司)
947,321
0.21%
February 16, 2027
Caitong Fund Management Co., Ltd. (財通
基金管理有限公司)
442,321
0.10%
February 16, 2027
Nord Fund Management Co., Ltd. (諾德基
金管理有限公司)
395,357
0.09%
February 16, 2027
China Southern Asset Management Co., 
Ltd. (南方基金管理股份有限公司)
358,392
0.08%
February 16, 2027
Oriental Alpha Fund Management Co., Ltd. 
(東方阿爾法基金管理有限公司)
267,857
0.06%
February 16, 2027
China Asset Management Co., Ltd. (華夏基
金管理有限公司)
203,571
0.04%
February 16, 2027
Guotai Asset Management Co., Ltd. (國泰
基金管理有限公司)
178,571
0.04%
February 16, 2027

<<<PAGE 16>>>
16
Name
Number of A 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon Listing 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option) (1)
Last day subject 
to the lock-up 
undertakings (2)
Morgan Stanley & Co. International plc (摩
根士丹利國際股份有限公司)
178,571
0.04%
February 16, 2027
Guotai Haitong Securities Co., Ltd. (國泰海
通證券股份有限公司)
178,571
0.04%
February 16, 2027
SigmaStar Technology Ltd. (星宸科技股份
有限公司)
178,571
0.04%
February 16, 2027
Sungrow Power Supply (Sanya) Co., Ltd. 
(陽光電源(三亞)有限公司)
178,571
0.04%
February 16, 2027
Fujian Yinfeng Venture Capital Co., Ltd. 
(福建銀豐創業投資有限責任公司)
178,571
0.04%
February 16, 2027
Notes:
(1) 
Assuming the Over-allotment Option is not exercised.
(2) 
In accordance with the respective subscription agreements, the required lock-up periods will end on February 
16, 2027. The 2025 A Share Placees will cease to be prohibited from disposing of or transferring the Shares 
subscribed for pursuant to their respective subscription agreements after the indicated date.

<<<PAGE 17>>>
17
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
(after taking 
into account 
the full 
exercise of 
the Offer Size 
Adjustment 
Option) (1)(2)
% of 
shareholding in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing 
(after taking 
into account 
the full 
exercise of 
the Offer Size 
Adjustment 
Option) (2)
Last day subject 
to the lock-up 
undertakings (3)
Transsion International 
Limited
830,800
2.77%
0.18%
March 7, 2027
YuFeng
332,300
1.11%
0.07%
March 7, 2027
YuFeng LPF
332,300
1.11%
0.07%
March 7, 2027
CITIC AM HK
635,550
2.12%
0.14%
March 7, 2027
AHGO SPC
423,700
1.41%
0.09%
March 7, 2027
Lenovo
332,300
1.11%
0.07%
March 7, 2027
Lens Technology HK
332,300
1.11%
0.07%
March 7, 2027
Ingenic Semiconductor HK
332,300
1.11%
0.07%
March 7, 2027
Ju Yuen International
332,300
1.11%
0.07%
March 7, 2027
Colorful Technology
317,750
1.06%
0.07%
March 7, 2027
HOSIN Global (HK) 
Electronics Co., 
Limited
237,250
0.79%
0.05%
March 7, 2027
Huadeng
166,150
0.55%
0.04%
March 7, 2027
Wind Sabre Fund SPC
166,150
0.55%
0.04%
March 7, 2027
CQTech Limited
166,150
0.55%
0.04%
March 7, 2027
SDMC Technology 
(Hong Kong) Limited
84,700
0.28%
0.02%
March 7, 2027
Notes:
(1) 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to 
be issued under the Global Offering.
(2) 
Assuming the Over-allotment Option is not exercised.
(3) 
In accordance with the respective cornerstone investment agreements, the required lock-up periods will end 
on March 7, 2027. The Cornerstone Investors will cease to be prohibited from disposing of or transferring the 
Shares subscribed for pursuant to their respective cornerstone investment agreements after the indicated date.

<<<PAGE 18>>>
18
PLACEE CONCENTRATION ANALYSIS
Placees(1)
Number of H 
Shares allotted
Allotment as % 
of International 
Offering (assuming 
no exercise of the 
Over-allotment 
Option)(2)
Allotment as % 
of International 
Offering (assuming 
the Over-allotment 
Option is exercised 
and new H Shares 
are issued)(2)
Allotment as % 
of total Offer 
Shares (assuming 
no exercise of the 
Over-allotment 
Option)(2)
Allotment as % of 
total Offer Shares 
(assuming the 
Over-allotment 
Option is exercised 
and new H Shares 
are issued)(2)
Number of H 
Shares held upon 
Listing
Top 1
1,595,150
5.83%
5.00%
5.32%
4.63%
1,595,150
Top 5
5,870,450
21.44%
18.41%
19.58%
17.02%
5,870,450
Top 10
9,982,050
36.46%
31.31%
33.29%
28.94%
9,982,050
Top 25
18,131,900
66.22%
56.88%
60.46%
52.57%
18,131,900
Notes:
(1) 
Ranking of placees is based on the number of H Shares allotted to the placees.
(2) 
After taking into account the full exercise of the Offer Size Adjustment Option.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H 
Shareholders(1)
Number of
H Shares
allotted
Allotment
as % of
International
Offering
(assuming
no exercise
of the
Over-
allotment
Option)(2)
Allotment
as % of
International
Offering
(assuming 
the
Over-
allotment
Option is
exercised
and new
H Shares
are
issued)(2)
Allotment
as % of
total Offer
Shares
(assuming
no exercise
of the
Over-
allotment
Option)(2)
Allotment
as % of
total Offer
Shares
(assuming 
the
Over-
allotment
Option is
exercised
and new
H Shares
are
issued)(2)
Number of
H Shares
held upon
Listing
% of total
issued 
share
capital 
upon
Listing
(assuming 
no
exercise of 
the
Over-
allotment
Option)(2)
% of total
issued 
share
capital 
upon
Listing
(assuming 
the
Over-
allotment
Option is
exercised 
and
new H 
Shares
are
issued)(2)
Number of
Shares 
held
upon 
Listing
% of total
issued 
share
capital 
upon
Listing
(assuming
no exercise
of the
Over-
allotment
Option)(2)
% of
total issued
share 
capital
upon 
Listing
(assuming 
the
Over-
allotment
Option is
exercised
and new
H Shares
are
issued)(2)
Top 1
1,595,150
5.83%
5.00%
5.32%
4.63%
1,595,150
0.35%
0.34%
1,595,150
0.35%
0.34%
Top 5
5,870,450
21.44%
18.41%
19.58%
17.02%
5,870,450
1.28%
1.26%
7,432,175
1.62%
1.60%
Top 10
9,982,050
36.46%
31.31%
33.29%
28.94%
9,982,050
2.17%
2.15%
11,543,775
2.51%
2.49%
Top 25
18,131,900
66.22%
56.88%
60.46%
52.57%
18,131,900
3.94%
3.91%
19,877,704
4.32%
4.28%
Notes:
(1) 
Ranking of H Shareholders is based on the number of H Shares held by the Shareholder upon Listing.
(2) 
After taking into account the full exercise of the Offer Size Adjustment Option.

<<<PAGE 19>>>
19
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders
(1)
Number 
of
H Shares
allotted
Allotment
as % of
International
Offering
(assuming
no exercise
of the
Over-
allotment
Option)
(2)
Allotment
as % of
International
Offering
(assuming the
Over-
allotment
Option is
exercised
and new
H Shares
are issued)
(2)
Allotment
as % of
total Offer
Shares
(assuming
no exercise
of the
Over-
allotment
Option)
(2)
Allotment
as % of
total Offer
Shares
(assuming the 
Over-
allotment
Option is
exercised
and new
H Shares
are issued)
(2)
Number of
H Shares
held upon
Listing
Number of 
Shares held 
upon Listing
% of total issued 
share capital 
upon Listing 
(assuming no 
exercise of the 
Over-allotment 
Option)
(2)
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
(2)
Top 1
–
0.00%
0.00%
0.00%
0.00%
–
176,771,900
38.46%
38.08%
Top 5
–
0.00%
0.00%
0.00%
0.00%
–
223,693,650
48.67%
48.19%
Top 10
–
0.00%
0.00%
0.00%
0.00%
–
250,877,456
54.58%
54.05%
Top 25
4,009,400
14.64%
12.58%
13.37%
11.63%
4,009,400
274,577,518
59.74%
59.16%
Notes:
(1) 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.
(2) 
After taking into account the full exercise of the Offer Size Adjustment Option.

<<<PAGE 20>>>
20
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, 36,285 valid applications 
made by the public will be conditionally allocated on the basis set out below:
Pool A
Number of 
H Shares 
applied for
Number of 
valid
applications
Basis of allocation/ballot
Approximate
percentage
allotted of the
total number of
H Shares 
applied for
50
13,704
391 out of 13,704 to receive 50 Shares
2.85%
100
3,585
204 out of 3,585 to receive 50 Shares
2.85%
150
1,494
127 out of 1,494 to receive 50 Shares
2.83%
200
2,070
234 out of 2,070 to receive 50 Shares
2.83%
250
1,080
153 out of 1,080 to receive 50 Shares
2.83%
300
661
112 out of 661 to receive 50 Shares
2.82%
350
422
82 out of 422 to receive 50 Shares
2.78%
400
647
144 out of 647 to receive 50 Shares
2.78%
450
398
99 out of 398 to receive 50 Shares
2.76%
500
1,826
503 out of 1,826 to receive 50 Shares
2.75%
600
492
162 out of 492 to receive 50 Shares
2.74%
700
355
135 out of 355 to receive 50 Shares
2.72%
800
408
177 out of 408 to receive 50 Shares
2.71%
900
298
145 out of 298 to receive 50 Shares
2.70%
1,000
2,013
1,068 out of 2,013 to receive 50 Shares
2.65%
2,000
1,285
50 Shares plus 72 out of 1,285 to receive additional 50 Shares
2.64%
3,000
735
50 Shares plus 429 out of 735 to receive additional 50 Shares
2.64%
4,000
597
100 Shares plus 66 out of 597 to receive additional 50 Shares
2.64%
5,000
578
100 Shares plus 369 out of 578 to receive additional 50 Shares
2.64%
6,000
263
150 Shares plus 44 out of 263 to receive additional 50 Shares
2.64%
7,000
181
150 Shares plus 125 out of 181 to receive additional 50 Shares
2.64%
8,000
706
200 Shares plus 158 out of 706 to receive additional 50 Shares
2.64%
9,000
145
200 Shares plus 109 out of 145 to receive additional 50 Shares
2.64%
10,000
949
250 Shares plus 266 out of 949 to receive additional 50 Shares
2.64%
20,000
649
500 Shares plus 363 out of 649 to receive additional 50 Shares
2.64%
35,541
Total number of Pool A successful applicants: 9,824

<<<PAGE 21>>>
21
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
total number of
H Shares 
applied for
30,000
340
650 Shares plus 328 out of 340 to receive additional 50 Shares
2.33%
40,000
106
900 Shares plus 65 out of 106 to receive additional 50 Shares
2.33%
50,000
72
1,150 Shares plus 19 out of 72 to receive additional 50 Shares
2.33%
60,000
42
1,350 Shares plus 39 out of 42 to receive additional 50 Shares
2.33%
70,000
24
1,600 Shares plus 14 out of 24 to receive additional 50 Shares
2.33%
80,000
18
1,850 Shares plus 4 out of 18 to receive additional 50 Shares
2.33%
90,000
11
2,050 Shares plus 10 out of 11 to receive additional 50 Shares
2.33%
100,000
69
2,300 Shares plus 37 out of 69 to receive additional 50 Shares
2.33%
200,000
32
4,650 Shares plus 2 out of 32 to receive additional 50 Shares
2.33%
300,000
7
6,950 Shares plus 4 out of 7 to receive additional 50 Shares
2.33%
400,000
5
9,300 Shares plus 1 out of 5 to receive additional 50 Shares
2.33%
500,000
10
11,600 Shares plus 7 out of 10 to receive additional 50 Shares
2.33%
750,000
1
17,450 Shares
2.33%
1,000,000
3
23,250 Shares plus 1 out of 3 to receive additional 50 Shares
2.33%
1,303,900
4
30,300 Shares plus 3 out of 4 to receive additional 50 Shares
2.33%
744
Total number of Pool B successful applicants: 744
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.

<<<PAGE 22>>>
22
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Offer Size Adjustment Option
The Offer Size Adjustment Option has been exercised in full, pursuant to which the Company 
is issuing and allotting 3,911,650 additional Offer Shares, representing approximately 15.0% of 
the Offer Shares initially being offered under the Global Offering, at the Offer Price. All of the 
additional Offer Shares that would be allotted and issued by the Company pursuant to the Offer 
Size Adjustment Option will be allocated to the International Offering. Accordingly, the total 
number of Offer Shares finally available under the Global Offering (taking into account the full 
exercise of the Offer Size Adjustment Option and before any exercise of the Over-allotment 
Option) will be 29,989,450 Shares and the total issued share capital of the Company upon Listing 
(after taking into account the full exercise of the Offer Size Adjustment Option and before any 
exercise of the Over-allotment Option) will be 459,657,599 Shares.
Allocation of H Shares to Existing Minority Shareholders and/or their close associates
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted to the 
Company, a waiver from strict compliance with the requirements under Rule 10.04 and consent 
under Paragraph 1C(2) of Appendix F1 to the Listing Rules to permit H Shares in the International 
Offering to be placed to certain existing minority Shareholders who (i) hold less than 5% of the 
total voting rights in the Company prior to the completion of the Global Offering and (ii) are 
not and will not become (upon the completion of the Global Offering) core connected persons of 
the Company or the close associates of any such core connected person (together, the “Existing 
Minority A Shareholders”) and/or their close associates, subject to the conditions as follows:
(a) 
the Joint Sponsors confirm that each Existing Minority A Shareholder (in case of the 2025 
A Share Placees, including their respective close associates) to whom the Company may 
allocate the H Shares under the International Offering holds less than 5% voting rights in the 
Company immediately before completion of the Global Offering;
(b) 
the Joint Sponsors confirm that each Existing Minority A Shareholder (in case of the 2025 
A Share Placees, including their respective close associates) is not, and will not be, a core 
connected person of the Company or any close associate of any such core connected person 
immediately prior to or following the Global Offering;
(c) 
the Joint Sponsors confirm that none of the Existing Minority A Shareholders (in case of the 
2025 A Share Placees, including their respective close associates) has the right to appoint a 
Director and/or has any other special rights;
(d) 
the Joint Sponsors confirm that allocation to the Existing Minority A Shareholders (including 
the 2025 A Share Placees) or their close associates will not affect the Company’s ability to 
satisfy the public float requirement as prescribed by the Hong Kong Stock Exchange under 
Rule 8.08 (as amended and replaced by Rule 19A.13A(2)) of the Listing Rules;

<<<PAGE 23>>>
23
(e) 
the Joint Sponsors confirm to the Hong Kong Stock Exchange in writing that based on (i) 
their discussions with the Company and the Overall Coordinators; and (ii) the confirmations 
provided to the Hong Kong Stock Exchange by the Company and the Overall Coordinators 
(as mentioned in the confirmations (f) and (g) below), and to the best of their knowledge 
and belief, they have no reason to believe that any of the Existing Minority A Shareholders 
(including the 2025 A Share Placees) or their close associates received any preferential 
treatment, or is in a position to exert influence on the Company to obtain actual or perceived 
preferential treatment in the allocation either as a cornerstone investor or as a placee by 
virtue of their relationship with the Company, other than the preferential treatment of assured 
entitlement under a cornerstone investment following the principles set out in Chapter 4.15 
of the Guide for New Listing Applicants, and the details of the allocation to (i) the Existing 
Minority A Shareholders holding more than 1% of the issued share capital of the Company 
immediately prior to the completion of the Global Offering and (ii) the 2025 A Share 
Placees and/or their respective close associates will be disclosed in the Prospectus and/or the 
allotment results announcement, as the case may be;
(f) 
to the best knowledge and belief of the Company, and based on discussions between the 
Company and the Overall Coordinators and confirmations required to be submitted to the 
Hong Kong Stock Exchange by the Joint Sponsors, the Company will confirm to the Hong 
Kong Stock Exchange in writing that:
(i) 
in the case of participation as cornerstone investors, no preferential treatment has been, 
nor will be, given to the Existing Minority A Shareholders (including the 2025 A Share 
Placees) or their close associates by virtue of their relationship with the Company, other 
than the preferential treatment of assured entitlement under a cornerstone investment 
following the principles set out in Chapter 4.15 of the Guide for New Listing 
Applicants, nor is the Existing Minority A Shareholder in a position to exert influence 
on the Company to obtain actual or perceived preferential treatment, and the Existing 
Minority A Shareholders (including the 2025 A Share Placees) or their close associates’ 
cornerstone investment agreements do not contain any material terms which are more 
favorable to the Existing Minority A Shareholders (including the 2025 A Share Placees) 
or their close associates than those in other cornerstone investment agreements; or
(ii) in the case of participation as placees, no preferential treatment has been, nor will be, 
given to the Existing Minority A Shareholders (including the 2025 A Share Placees) or 
their close associates, nor is the Existing Minority A Shareholder (including the 2025 A 
Share Placees) or their close associates in a position to exert influence on the Company 
to obtain actual or perceived preferential treatment, by virtue of their relationship with 
the Company in any allocation in the placing tranche;
(g) 
in the case of participation as placees, the Overall Coordinators will confirm to the Stock 
Exchange that, to the best of their knowledge and belief, no preferential treatment has been, 
nor will be, given to the Existing Minority A Shareholders (including the 2025 A Share 
Placees) or their close associates by virtue of their relationship with the Company in any 
allocation in the placing tranche.

<<<PAGE 24>>>
24
Please refer to the section headed “Waivers and Exemption — Allocation of Our H Shares to 
Existing Minority Shareholders and Their Close Associates under Rule 10.04 and Paragraph 
1C(2) of Appendix F1 to the Listing Rules” in the Prospectus for further details of the waiver and 
consent.
Each of the Joint Sponsors and the Company has provided the required confirmations as 
elaborated in the Prospectus. In particular, as the Company’s A Shares are listed on the Shenzhen 
Stock Exchange since September 2018, the Company has a highly extensive base of existing 
Shareholders and disclosure of details of allocations to all Existing Minority A Shareholders and/
or their respective close associates will not be meaningful to investors, the proposed disclosure 
threshold, i.e. condition (e) of the waiver and consent which provides that details of the allocation 
to (i) the Existing Minority A Shareholders holding more than 1% of the issued share capital of 
the Company immediately prior to the completion of the Global Offering and (ii) the 2025 A 
Share Placees and/or their respective close associates will be disclosed in this announcement, is 
appropriate.
All allocations of Offer Shares to the Existing Minority A Shareholders are in compliance with all 
the conditions under the waiver and consent granted by the Stock Exchange.
Allocations of Offer Shares to the existing Shareholders and Cornerstone Investors and/or 
their close associates with a consent under paragraph 18 of Chapter 4.15 of the Guide for 
New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under paragraph 
18 of Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to allocate 
further Offer Shares in the International Offering to certain existing Shareholders and Cornerstone 
Investors and/or their close associates as placees (the “Size-based Exemption Participants”), 
subject to the following conditions (“Allocation to Size-based Exemption Participants”):
(a) 
the final offering size of the Global Offering, excluding any over-allocation, will be of a total 
value of at least HK$1 billion;

<<<PAGE 25>>>
25
(b) 
the Offer Shares allocated to all existing Shareholders (whether as cornerstone investors and 
as placees) as permitted under this exemption do not exceed 30% of the total number of the 
H Shares offered under the Global Offering;
(c) 
the Allocation to Size-based Exemption Participants will not affect the Company’s ability 
to satisfy its public float requirement as prescribed by the Stock Exchange under the waiver 
from strict compliance with the requirements of Rule 19A.13A(2) of the Listing Rules;
(d) 
each of the Directors, chief executive of the Company and the Controlling Shareholders 
confirms that no securities have been allocated to them or their respective close associates 
under this exemption; and
(e) 
details of the allocation to Size-based Exemption Participants under this exemption have been 
disclosed in this announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the consent 
granted by the Stock Exchange.
For details of further allocations of Offer Shares to Size-based Exemption Participants, please 
refer to the section headed “Allotment Results Details — International Offering — Allottees with 
Waivers/Consents Obtained” in this announcement.
Placing to connected clients with a consent under paragraph 1C(1) of the Placing Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, consent 
under paragraph 1C(1) of the Placing Guidelines to permit CITIC AM HK to participate in the 
Global Offering as a connected client and participate in the Global Offering as a Cornerstone 
Investor. For details of the consent granted, please refer to the section headed “Allotment 
Results Details — International Offering — Allottees With Waivers/Consents Obtained” in this 
announcement.
In addition, under the International Offering, certain Offer Shares were placed to connected clients 
of their connected distributors pursuant to the Placing Guidelines as placees. Please refer to the 
section headed “Allotment Results Details — International Offering — Allottees with Waivers/
Consents Obtained” in this announcement for details. The Company has applied to the Stock 
Exchange for, and the Stock Exchange has granted, a consent under paragraph 1C(1) of the Placing 
Guidelines to permit the Company to allocate such Offer Shares in the International Offering to 
the connected clients as placees. The allocation of Offer Shares to such connected clients is in 
compliance with all the conditions under the consent granted by the Stock Exchange. Details of the 
placement to connected clients as placees are set out below.

<<<PAGE 26>>>
26
No.
Connected 
Client (8)
Connected 
Distributor(s)
Relationship between the 
Connected Client and the 
Connected Distributor(s)
Discretionary or non- 
discretionary
Number of H 
Shares to be 
allocated
Approximate 
percentage of 
Offer Shares 
in the Global 
Offering(1)
Approximate 
percentage of 
the total issued 
share capital 
immediately 
following 
completion 
of the Global 
Offering(1)
Approximate 
percentage of 
Offer Shares 
in the Global 
Offering(2)
Approximate 
percentage of 
the total issued 
share capital 
immediately 
following 
completion 
of the Global 
Offering(2)
1.
CITIC AM HK(3)
CLSA Limited 
(“CLSA”) and 
China 
CITIC Bank 
International 
Limited (“China 
CITIC”)
Members of the same group of 
companies
Discretionary
435,100
1.45%
0.09%
1.26%
0.09%
2.
CSI(4)
CLSA and China 
CITIC
Members of the same group of 
companies
Non-discretionary
830,800
2.77%
0.18%
2.41%
0.18%

<<<PAGE 27>>>
27
No.
Connected 
Client (8)
Connected 
Distributor(s)
Relationship between the 
Connected Client and the 
Connected Distributor(s)
Discretionary or non- 
discretionary
Number of H 
Shares to be 
allocated
Approximate 
percentage of 
Offer Shares 
in the Global 
Offering(1)
Approximate 
percentage of 
the total issued 
share capital 
immediately 
following 
completion 
of the Global 
Offering(1)
Approximate 
percentage of 
Offer Shares 
in the Global 
Offering(2)
Approximate 
percentage of 
the total issued 
share capital 
immediately 
following 
completion 
of the Global 
Offering(2)
3.
CITIC AM(5)
CLSA and China 
CITIC
Members of the same 
group of companies
Discretionary
14,400
0.05%
0.003%
0.04%
0.003%
4.
Bosera 
 International(6)
CMB International 
Securities Limited 
(“CMBI”) and 
China Merchants 
Securities (HK) 
Co., Limited 
(“CMS HK”)
Members of the same group of 
companies
Discretionary
598,200
1.99%
0.13%
1.73%
0.13%
5.
SDICSAMHK(7)
SDIC Securities 
(Hong Kong) 
Limited 
(“SDICSHK”)
Members of the same group of 
companies
Discretionary
33,200
0.11%
0.01%
0.10%
0.01%

<<<PAGE 28>>>
28
Notes:
(1) 
Assuming the Over-allotment Option is not exercised.
(2) 
Assuming the Over-allotment Option is fully exercised.
(3) 
CITIC AM HK will hold the Offer Shares in its capacity as the discretionary investment manager of the below managed accounts: (i) CLSA CT Limited Sub Account 13, where save for the State-owned Assets Supervision and Administration Commission of 
Zhenjiang Municipality (鎮江市國有資產監督管理委員會), there is no other ultimate beneficial owner holding 30% or more interest; and (ii) CITIC Securities Asset Management (HK) Limited Client 12, where save for natural person Chen Shi (陳實), there 
is no other ultimate beneficial owner holding 30% or more interest; and (iii) CLSA CT Limited Sub Account 48, where save for natural person Gao Bin (高斌), there is no other ultimate beneficial owner holding 30% or more interest. The aforementioned 
managed accounts are, to the best knowledge of CITIC AM HK, independent third parties of the Company, its subsidiaries, its substantial shareholders, CITIC AM HK, CLSA, China CITIC and the companies which are members of the same group of 
companies as CLSA and China CITIC. The ultimate beneficial owner of CITIC AM HK is CITIC Securities Company Limited (6030.HK).
(4) 
CSI will hold the Offer Shares as a placee under the International Offering on behalf of its ultimate client (the “CSI Ultimate Client”), on a non-discretionary basis, pursuant to which: (i) CSI will act as the single counterparty of the CSI Back-to-back TRS (the 
“CSI Back-to-back TRS”) to be entered into by it in connection with a total return swap order (the “CSI Client TRS”) placed and fully funded by the CSI Ultimate Client, by which CSI will pass the full economic exposure of the Offer Shares placed to CSI 
to the CSI Ultimate Client; (ii) as confirmed by CSI and CLSA, CSI will hold the legal title and beneficial interest in the Offer Shares, but will contractually agree to pass on the full economic exposure and return of the Offer Shares to the CSI Ultimate Client, 
on a non-discretionary basis. The CSI Ultimate Client may exercise their early termination rights to terminate the CSI Client TRS at any time from the trade date of the CSI Client TRS which should be on or after the date on which the Offer Shares are listed 
on the Stock Exchange; (iii) upon the final maturity or termination of the CSI Client TRS by the CSI Ultimate Client, CSI will dispose of the Offer Shares on the secondary market and the CSI Ultimate Client will receive a final termination amount of the CSI 
Back-to-back TRS which will have taken into account all the economic returns or economic loss in relation to the Offer Shares and the fixed amount of transaction fees of the CSI Back-to-back TRS and the CSI Client TRS. Due to its internal policy, CSI will 
not exercise the voting right of the Offer Shares during the terms of the CSI Back-to-back TRS; and (iv) CSI is not a collective investment scheme which is not authorized by the SFC, nor is expected to hold the Offer Shares on behalf of such scheme.
The details of the CSI Ultimate Client are as follows:
Name (CSI Ultimate Client)
Asset Manager
UBO of Asset Manager
UBO of CSI Ultimate Client
Beevest Capital Management Limited – Global Multi Alpha Fund
Beevest Capital Management Limited
KANG Lan (康瀾)
NIE Fanqi
To the best knowledge of CSI and having made all reasonable inquiries, each of the CSI Ultimate Client and its UBOs is an independent third party of the Company, its subsidiaries, its substantial shareholders, CSI, CLSA, China CITIC and the companies 
which are members of the same group of companies as CLSA and China CITIC.

<<<PAGE 29>>>
29
(5) 
CITIC AM will hold the Offer Shares in its capacity as the discretionary fund manager managing two funds (i.e. CITIC SECURITIES COMPANY LIMITED-XINHANG ZHIYUAN NO. 1 (中信證券信航致遠1號集合資產管理計劃) and CITIC SECURITIES 
COMPANY LIMITED-XINHANG ZHIYUAN NO. 3 (中信證券信航致遠3號集合資產管理計劃)) on behalf of their underlying clients, none of which has an ultimate beneficial owner holding 30% or more interest therein and each of which is, to the best 
knowledge of CITIC AM, an independent third party of the Company, its subsidiaries, its substantial shareholders, CITIC AM, CLSA, China CITIC and the companies which are members of the same group of CLSA and China CITIC.
(6) 
Bosera International will hold the Offer Shares in its capacity as the discretionary fund manager on behalf of its sub-funds, which are all independent third parties. To the best knowledge of Bosera International after due enquiry, each of the sub-funds and their 
respective ultimate beneficial owner holding 30% or more interest is an independent third party of the Company, its subsidiaries, its substantial shareholders, Bosera International, CMBI and CMS HK, and the companies which are members of the same group 
of CMBI and CMS HK. Details of the sub-funds are set out as below:
Name of the sub-funds 
Ultimate beneficial owner(s) holding 30% or more interest (if any)
Bosera Hong Kong Equity Plus Fund (SFC Authorised Fund) 
N/A
Bosera China New Opportunities Fund SP 
N/A
Bosera Growth Premium Global Equity Strategy Fund SP 
Guo Feng (郭峰)
KB CHINA MAINLAND FD BOSERA 
N/A
Bosera Growth Premium Global Equity Strategy Fund SP2 
Guangdong Dongfang Precision Science & Technology Co.,Ltd (廣東東方精工科技股份有限公司) (002611.SZ) (“Dongfang Precision”)
Bosera Greater China Enhanced Return Bond Fund (SFC Authorised Fund) 
N/A
Bosera Growth Premium Global Equity Strategy Fund SP3 
HUANG Liya (黃麗亞)
Bosera Growth Premium Global Equity Strategy Fund SP4 
Dongfang Precision
(7) 
SDICSAMHK will hold the Offer Shares as a placee under the International Offering on behalf of its ultimate client (the “SDICSAMHK Ultimate Client”), namely HUANG Junhao (黃俊豪), on a discretionary basis. To the best knowledge of SDICSAMHK 
and having made all reasonable inquiries, the SDICSAMHK Ultimate Client is an independent third party of the Company, its subsidiaries, its substantial shareholders, SDICSAMHK, SDICSHK and the companies which are members of the same group of 
companies as SDICSHK.
(8) 
Each of the connected clients is not a collective investment scheme which is not authorized by the SFC, nor is it holding the Offer Shares on behalf of such schemes.

<<<PAGE 30>>>
30
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
herein have not been, and will not be, registered under the U.S. Securities Act. The securities 
may not be offered or sold in the United States except pursuant to an available exemption from, 
or in a transaction not subject to, the registration requirements of the U.S. Securities Act and in 
accordance with any applicable state securities laws in the United States. The Offer Shares may 
only be offered and sold (a) in the United States to QIBs in reliance on Rule 144A or another 
available exemption from registration requirements under the U.S. Securities Act, and (b) outside 
the United States in offshore transactions in reliance on Regulation S. There will be no public 
offer of securities in the United States.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated August 31, 2026 issued by the Company for 
detailed information about the Global Offering described above before deciding whether or not 
to invest in the Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate their obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the paragraph headed “Underwriting 
— Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing 
Date (which is currently expected to be on September 8, 2026).

<<<PAGE 31>>>
31
Public Float and Free Float
Immediately after the completion of the Global Offering (taking into account the full exercise 
of the Offer Size Adjustment Option and before any exercise of the Over-allotment Option), 
the total market value of the H Shares to be held by the public is expected to be approximately 
HK$7,077.5 million, calculated based on the final Offer Price of HK$236.00, which is higher than 
the prescribed expected market value of H Shares required to be held in public hands of not less 
than HK$3,000 million under Rule 19A.13A(2)(b) of the Listing Rules, thereby satisfying Rule 
19A.13A(2) of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following and 
including the Listing Date. As such, H Shares held by the Cornerstone Investors upon the Listing 
shall not be counted towards the free float of the H Shares of the Company at the time of Listing. 
Based on the Offer Price of HK$236.00 per H Share, the Company confirmed that it complies with 
the free float requirement under Rule 19A.13C(2)(b) of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering (before any 
exercise of the Over-allotment Option): (i) the Shares will be held by at least 300 Shareholders 
at the time of Listing, in compliance with Rule 8.08(2) of the Listing Rules; (ii) the three largest 
public Shareholders will not hold more than 50% of the H Shares held in public hands at the 
time of Listing, in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; (iii) no placee 
will, individually, be placed more than 10% of the enlarged issued share capital of the Company 
immediately after the Global Offering; and (iv) there will not be any new substantial Shareholder 
(as defined in the Listing Rules) immediately after the Global Offering.

<<<PAGE 32>>>
32
Commencement of Dealings
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, 
September 8, 2026 (Hong Kong time), provided that the Global Offering has become unconditional 
and the right of termination described in the section headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” in the 
Prospectus has not been exercised. Investors who trade the H Shares on the basis of publicly 
available allocation details prior to the receipt of H Share certificates or prior to the H Share 
certificates becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Tuesday, 
September 8, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Tuesday, September 8, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 50 H Shares each, and the stock code of the H Shares will be 
09976.
By order of the Board
Shenzhen Longsys Electronics Co., Ltd.
Mr. Cai Huabo
Chairman of the Board
Hong Kong, September 7, 2026
As of the date of this announcement, the Board comprises: (i) Mr. Cai Huabo, Mr. Li Zhixiong 
and Mr. Wang Jingyang as executive Directors; (ii) Mr. Cai Jing and Mr. Hu Yingping as non-
executive Directors; and (iii) Mr. Tang Zhongcheng, Mr. Chen Weiyue, Mr. Huang Zhiqiang and 
Ms. Tang Mei Shan as independent non-executive Directors.
