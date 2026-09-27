# 配发结果公告抽取任务：2335.HK Shaanxi Micot Pharmaceutical Technology Co., Ltd. - B - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**23/06/2026 19:30**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0623/2026062301227.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2335.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the 
contents of this announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the 
contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia) or any 
other jurisdiction where such distribution is prohibited by law. This announcement does not constitute or form a 
part of any offer to sell or solicitation of an offer to buy, to purchase or subscribe for securities nor shall there 
be any sale of Offer Shares in the United States or in any other jurisdictions in which such offer or solicitation 
would be unlawful. The securities mentioned herein have not been, and will not be, registered under the United 
States Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or any state securities 
law of the United States. The securities may not be offered, sold, pledged, or transferred within the United 
States or to, or for the account or benefit of U.S. persons (as defined in Regulation S under the U.S. Securities 
Act (“Regulation S”)) except pursuant to an exemption from, or in a transaction not subject to, the registration 
requirements of the U.S. Securities Act and in compliance with any applicable state securities laws. There will 
be no public offering of securities in the United States. The Offer Shares are being offered and sold outside the 
United States in offshore transactions in reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities of the Company. This announcement is not a prospectus. Potential 
investors should read the prospectus dated June 15, 2026 (the “Prospectus”) of Shaanxi Micot Pharmaceutical 
Technology Co., Ltd. (陝西麥科奧特醫藥科技股份有限公司) (the “Company”) carefully for detailed 
information about the Company and the Global Offering before deciding whether or not to invest in the Offer 
Shares. Any investment decision in relation to the Global Offering should be taken solely in reliance on the 
information in the Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as 
those defined in the Prospectus.
In connection with the Global Offering, CCB International Capital Limited, as the stabilizing manager (the 
“Stabilizing Manager”), its affiliates or any person acting for it, may, to the extent permitted by applicable 
laws of Hong Kong or elsewhere, over-allocate or effect transactions with a view to stabilizing or maintaining 
the market price of the Shares at a level higher than that which might otherwise prevail for a limited period 
after the Listing Date. However, there is no obligation on the Stabilizing Manager (its affiliates or any person 
acting for it) to conduct any such stabilizing action. Such stabilizing action, if taken, (a) will be conducted at 
the absolute discretion of the Stabilizing Manager (its affiliates or any person acting for it) and in what the 
Stabilizing Manager reasonably regards as the best interest of the Company, (b) may be discontinued at any 
time and (c) is required to be brought to an end within 30 days of the last day for lodging applications under the 
Hong Kong Public Offering. Such stabilization action, if commenced, may be effected in all jurisdictions where it 
is permissible to do so, in each case in compliance with all applicable laws, rules and regulatory requirements, 
including the Securities and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as 
amended, made under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that stabilizing action cannot be taken to support the price of the Shares for 
longer than the stabilization period will begin on the Listing Date, and is expected to expire on Saturday, July 
18, 2026, the 30th day after the last day for the lodging of applications under the Hong Kong Public Offering. 
After this date, no further stabilizing action may be taken, demand for the Shares, and therefore the price of the 
Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions 
set out in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong 
Kong and/or not resident in Hong Kong. Potential investors of the Offer Shares should note that the Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement upon the occurrence of any of the events set out in the 
paragraph headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering 
— Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing 
Date (which is currently expected to be Wednesday, June 24, 2026).

<<<PAGE 2>>>
– 2 –
Shaanxi Micot Pharmaceutical Technology Co., Ltd.
陝西麥科奧特醫藥科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the 
Global Offering
: 58,054,400 H Shares
Number of Hong Kong Offer Shares : 5,805,600 H Shares
Number of International Offer Shares : 52,248,800 H Shares
Final Offer Price : HK$18.20 per H Share, plus brokerage 
of 1.0%, SFC transaction levy of 
0.0027%, AFRC transaction levy of 
0.00015% and the Stock Exchange 
trading fee of 0.00565% (payable in full 
on application in Hong Kong Dollars, 
subject to refund)
Nominal value : RMB0.02 per H Share
Stock code : 2335
Joint Sponsors, Overall Coordinators, Sponsor-Overall Coordinators, 
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers
SOMERLEY CAPITAL LIMITED
Зࡋ⳪暲
@:9)

<<<PAGE 3>>>
– 3 –
Shaanxi Micot Pharmaceutical Technology Co., Ltd.
陝西麥科奧特醫藥科技股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Warning: In view of high concentration of shareholding in a small number of H 
Shareholders, Shareholders and prospective investors should be aware that the price 
of the H Shares could move substantially even with a small number of H Shares 
traded and should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
2335
Stock short name
MICOT PHARMA-B
Dealings commencement date
June 24, 2026 *
* see note at the end of the announcement
Price Information
Final Offer Price
HK$18.20
Offer Shares and Share Capital
Number of Offer Shares
58,054,400
Final number of Offer Shares in Hong Kong Public 
Offering
5,805,600
Final number of Offer Shares in International 
Offering
52,248,800
Number of issued Shares upon Listing
331,740,350
Over-allocation
No. of Offer Shares over-allocated
0
There has been no over-allocation of Offer Shares in the International Offering. 
Therefore, the Over-allotment Option will not be exercised and will lapse upon Listing.
Proceeds
Gross proceeds (Note)
HK$1,056.6 million
Less: Estimated listing expenses payable based on 
Final Offer Price
HK$67.3 million
Net proceeds
HK$989.3 million

<<<PAGE 4>>>
– 4 –
Note: Gross proceeds refer to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
153,832
No. of successful applications
22,665
Subscription level
1,181.46 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong 
Kong Public Offering
5,805,600
No. of Offer Shares reallocated from the International 
Offering
0
Final no. of Offer Shares under the Hong Kong Public 
Offering
5,805,600
% of Offer Shares under the Hong Kong Public Offering 
to the Global Offering
10%
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/IPOResult to perform a search by identification document number or www.hkeipo.hk/IPOResult 
for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
73
Subscription Level
2.52 times
No. of Offer Shares initially available under the 
International Offering
52,248,800
No. of Offer Shares reallocated to the Hong Kong 
Public Offering
0
Final no. of Offer Shares under the International 
Offering
52,248,800
% of Offer Shares under the International Offering to 
the Global Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for 
consent under paragraph 1C(2) of Appendix F1 to the Listing Rules granted by the Stock 
Exchange to permit Qiyuan Hong Kong, a close associates of Existing Shareholders, to 

<<<PAGE 5>>>
– 5 –
participate in the Global Offering as a cornerstone investor subject to certain conditions, 
(i) none of the Offer Shares subscribed by the placees and the public have been financed 
directly or indirectly by the Company, any of the Directors, chief executive of the Company, 
Controlling Shareholders, substantial Shareholders, existing Shareholders of the Company 
or any of its subsidiaries or their respective close associates; and (ii) none of the placees and 
the public who have purchased the Offer Shares are accustomed to taking instructions from 
the Company, any of the Directors, chief executive of the Company, Controlling Shareholders, 
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries 
or their respective close associates in relation to the acquisition, disposal, voting or other 
disposition of H Shares registered in his/her/its name or otherwise held by him/her/it.
The placees in the International Offering include the following:
Cornerstone Investors
Investor note 1
TNo. of Offer Shares 
allocated
% of Offer Shares 
after the Global 
Offering
% of total issued 
share capital in the 
Company after the 
Global Offering
Existing 
shareholders or 
their close 
associates
Qiyuan Hong Kong note 2
18,756,200
32.31%
5.65%
YES
Everest Medicine
5,494,400
9.46%
1.66%
No
Summit Capital
430,400
0.74%
0.13%
No
Total
24,681,000
42.51%
7.44%
Notes:
1. 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone 
Investors” in the Prospectus.
2. 
As disclosed in the Prospectus, as Qiyuan Hong Kong is ultimately controlled by government bodies 
of Shaanxi Province, it is a close associate of existing Shareholders of the Company. The Company 
has sought, and the Stock Exchange has given, a consent under paragraph 1C(2) of Appendix F1 to 
the Listing Rules to permit Qiyuan Hong Kong to participate in the Global Offering as a cornerstone 
investor subject to certain conditions. For further details of the abovementioned consent, please refer 
to the section headed “Waivers from Strict Compliance with the Listing Rules and Exemption from 
Strict Compliance with the Companies (Winding Up and Miscellaneous Provisions) Ordinance” in the 
Prospectus and “Others/Additional Information” in this announcement for details.

<<<PAGE 6>>>
– 6 –
Allottee with Waiver/Consent Obtained
Investor
No. of Offer 
Shares allocated
% of Offer Shares 
after the Global 
Offering Note 4
% of total issued 
share capital in the 
Company after the 
Global Offering Note 5
Relationship
Allottee with consent under paragraph 1C(2) of the Placing Guidelines under Chapters 2.3 and 4.15 of the 
Guide in relation to allocation of Offer Shares to a close associate of existing Shareholders Note 1
Qiyuan Hong Kong
18,756,200
32.31%
5.65%
A close associate 
of existing 
Shareholders
Notes:
1. 
The Stock Exchange has given a consent under paragraph 1C(2) of the Placing Guidelines and Chapters 2.3 and 4.15 of Guide to 
permit Offer Shares to be placed to the above placee who is a close associate of existing Shareholders. Please refer to the section 
headed “Others/Additional Information” in this announcement.

<<<PAGE 7>>>
– 7 –
LOCK-UP UNDERTAKINGS
Cornerstone Investors
Name
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing
% of total issued 
share capital in 
the Company 
subject to lock-up 
undertakings upon 
Listing
Last day subject 
to the lock-up 
undertakings Note 1
Qiyuan Hong Kong
18,756,200
6.70%
5.65%
December 23, 2026
Everest Medicine
5,494,400
1.96%
1.66%
December 23, 2026
Summit Capital
430,400
0.15%
0.13%
December 23, 2026
Total
24,681,000
8.81%
7.44%
Notes:
1. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on December 23, 2026. The 
Cornerstone Investors will cease to be prohibited from disposing of or transferring H Shares subscribed pursuant to the relevant 
cornerstone investment agreements after the indicated date.
Controlling Shareholders
Name Note 1
Number of Shares held 
in the Company subject 
to lock-up undertakings 
upon Listing
Number of H Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
% of total issued H 
Shares after the Global 
Offering subject to 
lock-up undertakings 
upon Listing
% of total issued share 
capital in the Company 
subject to lock-up 
undertakings upon 
Listing
Last day subject to 
the lock-up 
undertakings Note 2
Dr. Wang Bing
111,000,000 
66,600,000
23.78%
33.46%
June 23, 2027
Dr. Wang Mei
18,060,050 
18,060,050
6.45%
5.44%
June 23, 2027
Xi’an Zhongrui
15,000,000 
15,000,000
5.36%
4.52%
June 23, 2027
Total
144,060,050
99,660,050
35.58%
43.43%
Notes:
1. 
As of the date of this announcement, Dr. Wang Bing (王冰), Dr. Wang Mei (王梅) and Xi’an Zhongrui directly held 40.56%, 6.60% and 5.48% of the interest in our Company, respectively. 
Dr. Wang Bing and Dr. Wang Mei are spouses. Dr. Wang Mei and Dr. Wang Bing held 99.00% and 1.00% of the equity interest, respectively, in Zhongrui Zekang, which acts as the general 
partner of Xi’an Zhongrui. Xi’an Zhongrui directly held 5.48% of the equity interest in the Company, such that Dr. Wang Mei and Dr. Wang Bing are deemed to be the beneficial owners 
of the 5.48% equity interest in the Company held by Xi’an Zhongrui. Therefore, Dr. Wang Bing, Dr. Wang Mei, Xi’an Zhongrui and Zhongrui Zekang will be regarded as our Controlling 
Shareholders under the Listing Rules before the Listing. For further details, please refer to the section headed “Relationship with our Controlling Shareholders” in the Prospectus.
2. 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law. The required lock-up for the Controlling Shareholders ends on June 23, 2027, being 
twelve months following the Listing Date. Pursuant to Rule 10.07 of the Listing Rules, each of the Controlling Shareholders (namely Dr. Wang Bing, Dr. Wang Mei, Xi’an Zhongrui and 
Zhongrui Zekang) has undertaken to the Stock Exchange and the Company that, he, she or it shall comply with the applicable lockup requirements. For further details, please refer to the 
section headed “Underwriting — Undertakings to the Stock Exchange Pursuant to the Listing Rules — Undertakings by our Controlling Shareholders” in the Prospectus.

<<<PAGE 8>>>
– 8 –
Other Existing Shareholders
Name
Number of Shares held 
in the Company subject 
to lock-up undertakings 
upon Listing
Number of H Shares 
held in the Company 
subject to lock-up 
undertakings 
upon Listing
% of total issued H 
Shares after the Global 
Offering subject to 
lock-up undertakings 
upon Listing
% of total issued share 
capital in the Company 
subject to lock-up 
undertakings upon 
Listing
Last day subject to 
the lock-up 
undertakings Note 1
The People’s Government of Shaanxi Province
Junying Growth
3,982,350
3,982,350
1.42%
1.20%
June 23, 2027
Listing Reserve Fund
3,631,750
3,631,750
1.30%
1.09%
June 23, 2027
Junying Jiacheng
2,017,650
2,017,650
0.72%
0.61%
June 23, 2027
Xi’an Huiyu
907,950
907,950
0.32%
0.27%
June 23, 2027
Shaanxi Innovation Relay
4,153,850
–
–
1.25%
–
Shaanxi Jingang
3,115,400
–
–
0.94%
–
New Materials Fund
6,000,000
6,000,000
2.14%
1.81%
June 23, 2027
Other Shareholders
Suzhou Mainiv
27,333,350
27,333,350
9.76%
8.24%
June 23, 2027
Beta Achieve
17,733,350
17,733,350
6.33%
5.35%
June 23, 2027
Linhai Qize
14,382,650
14,382,650
5.14%
4.34%
June 23, 2027
Huaxin Pharmaceutical Venture 
Capital
7,776,650
7,776,650
2.78%
2.34%
June 23, 2027
Suzhou Rongsheng
6,833,350
6,833,350
2.44%
2.06%
June 23, 2027
Xi’an Tongshang
5,939,950
5,939,950
2.12%
1.79%
June 23, 2027
Fengchuan Hongbo
5,125,000
5,125,000
1.83%
1.54%
June 23, 2027
Jingcheng Daxing
5,075,100
5,075,100
1.81%
1.53%
June 23, 2027
Tangxing Technology
4,780,200
4,780,200
1.71%
1.44%
June 23, 2027
Shanjin Runji
3,947,750
3,947,750
1.41%
1.19%
June 23, 2027
Hainan Wanfeng
1,361,900
1,361,900
0.49%
0.41%
June 23, 2027
Yinyun Heman
907,950
907,950
0.32%
0.27%
June 23, 2027
Hangzhou Quandewang
907,950
907,950
0.32%
0.27%
June 23, 2027
Hainan Ruizheng
907,950
907,950
0.32%
0.27%
June 23, 2027

<<<PAGE 9>>>
– 9 –
Name
Number of Shares held 
in the Company subject 
to lock-up undertakings 
upon Listing
Number of H Shares 
held in the Company 
subject to lock-up 
undertakings 
upon Listing
% of total issued H 
Shares after the Global 
Offering subject to 
lock-up undertakings 
upon Listing
% of total issued share 
capital in the Company 
subject to lock-up 
undertakings upon 
Listing
Last day subject to 
the lock-up 
undertakings Note 1
Maicheng Century
1,557,700
1,557,700
0.56%
0.47%
June 23, 2027
Jinan Liuji
1,246,150
1,246,150
0.44%
0.38%
June 23, 2027
Total
129,625,900
122,356,650
43.69%
39.07%
 
Notes:
1. 
Under the applicable PRC laws, all existing Shareholders are subject to a lockup period of twelve months following the Listing Date.
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of 
H Shares 
allotted
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
% of total 
issued share 
capital upon 
Listing
Top 1
18,756,200
35.90%
32.31%
18,756,200
5.65%
Top 5
39,640,000
75.87%
68.28%
39,640,000
11.95%
Top 10
45,269,000
86.64%
77.98%
45,269,000
13.65%
Top 25
51,790,600
99.12%
89.21%
51,790,600
15.61%
Note:
* 
Ranking of placees is based on the number of H Shares allotted to the placees.

<<<PAGE 10>>>
– 10 –
H SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholders*
Number of 
H Shares 
allotted
Allotment as 
% of 
International 
Offering
Allotment 
as % of total 
Offer Shares
Number of 
H Shares held 
upon Listing
% of total
issued 
H share 
capital upon 
Listing
Number of 
Shares held 
upon Listing
Top 1
0
NA
NA
99,660,050
35.58%
144,060,050
Top 5
18,756,000
35.90%
32.31%
194,405,300
69.41%
246,074,550
Top 10
33,204,000
63.55%
57.20%
229,403,650
81.91%
281,072,900
Top 25
44,574,800
85.31%
76.78%
265,683,550
94.86%
317,352,800
Note:
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
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
Number of 
H Shares held 
upon Listing
Number of 
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing
Top 1
0
NA
NA
99,660,050
144,060,050
43.43%
Top 5
18,756,200
35.90%
32.31%
194,405,300
246,074,550
73.18%
Top 10
33,204,600
63.55%
57.20%
229,403,650
281,072,900
84.73%
Top 25
44,574,800
85.31%
76.78%
265,683,550
317,352,800
95.66%
Note:
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon 
Listing.

<<<PAGE 11>>>
– 11 –
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 153,832 valid 
applications made by the public will be conditionally allocated on the basis set out below:
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
allotted 
of the total 
number of
H Shares 
applied for
200
44,060
1,322 out of 44,060 applicants to receive 200 H Shares
3.00%
400
24,701
976 out of 24,701 applicants to receive 200 H Shares
1.98%
600
4,048
188 out of 4,048 applicants to receive 200 H Shares
1.55%
800
2,703
141 out of 2,703 applicants to receive 200 H Shares
1.30%
1,000
3,083
175 out of 3,083 applicants to receive 200 H Shares
1.14%
1,200
1,918
118 out of 1,918 applicants to receive 200 H Shares
1.03%
1,400
1,344
88 out of 1,344 applicants to receive 200 H Shares
0.94%
1,600
1,425
98 out of 1,425 applicants to receive 200 H Shares
0.86%
1,800
1,500
108 out of 1,500 applicants to receive 200 H Shares
0.80%
2,000
12,982
970 out of 12,982 applicants to receive 200 H Shares
0.75%
3,000
3,436
302 out of 3,436 applicants to receive 200 H Shares
0.59%
4,000
4,863
479 out of 4,863 applicants to receive 200 H Shares
0.49%
5,000
1,990
214 out of 1,990 applicants to receive 200 H Shares
0.43%
6,000
1,481
171 out of 1,481 applicants to receive 200 H Shares
0.38%
7,000
1,130
139 out of 1,130 applicants to receive 200 H Shares
0.35%
8,000
1,070
139 out of 1,070 applicants to receive 200 H Shares
0.32%
9,000
1,558
212 out of 1,558 applicants to receive 200 H Shares
0.30%
10,000
6,201
877 out of 6,201 applicants to receive 200 H Shares
0.28%
20,000
5,421
1,009 out of 5,421 applicants to receive 200 H Shares
0.19%
30,000
3,691
807 out of 3,691 applicants to receive 200 H Shares
0.15%
40,000
2,469
605 out of 2,469 applicants to receive 200 H Shares
0.12%
50,000
1,567
420 out of 1,567 applicants to receive 200 H Shares
0.11%
60,000
1,352
389 out of 1,352 applicants to receive 200 H Shares
0.10%
70,000
1,071
328 out of 1,071 applicants to receive 200 H Shares
0.09%
80,000
750
242 out of 750 applicants to receive 200 H Shares
0.08%
90,000
647
219 out of 647 applicants to receive 200 H Shares
0.08%
100,000
4,429
1,559 out of 4,429 applicants to receive 200 H Shares
0.07%
200,000
4,791
2,219 out of 4,791 applicants to receive 200 H Shares
0.05%
 
Total
145,681
Total number of Pool A successful applicants: 14,514
 

<<<PAGE 12>>>
– 12 –
Pool B
Number of 
H Shares 
applied for
Number of 
valid 
applications
Basis of allocations/ballot
Approximate 
percentage 
allotted 
of the total 
number of 
H Shares 
applied for
300,000
4,433
200 H Shares plus 2,217 out of 4,433 applicants to 
receive an additional 200 H Shares
0.10%
400,000
912
200 H Shares plus 609 out of 912 applicants to 
receive an additional 200 H Shares
0.08%
500,000
725
200 H Shares plus 588 out of 725 applicants to 
receive an additional 200 H Shares
0.07%
600,000
348
200 H Shares plus 326 out of 348 applicants to 
receive an additional 200 H Shares
0.06%
700,000
339
400 H Shares
0.06%
800,000
204
400 H Shares plus 32 out of 204 applicants to 
receive an additional 200 H Shares
0.05%
900,000
123
400 H Shares plus 31 out of 123 applicants to 
receive an additional 200 H Shares
0.05%
1,000,000
618
400 H Shares plus 209 out of 618 applicants to 
receive an additional 200 H Shares
0.05%
2,000,000
126
600 H Shares
0.03%
2,902,800
323
600 H Shares plus 169 out of 323 applicants to 
receive an additional 200 H Shares
0.02%
 
Total
8,151
Total number of Pool B successful applicants: 8,151
 
As of the date of this announcement, the relevant subscription monies previously deposited 
in the designated nominee accounts have been remitted back to the accounts of all HKSCC 
participants. Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in 
respect of which consent has been obtained, the Company has complied with the Listing Rules 
and guidance materials in relation to the placing, allotment and listing of the Company’s H 
Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by 
the placees or the public (as the case may be) directly or indirectly for each Offer Share 
subscribed for or purchased by them was the same as the final Offer Price in addition to any 
brokerage, AFRC transaction levy, SFC transaction levy and Stock Exchange trading fee 
payable.

<<<PAGE 13>>>
– 13 –
OTHERS/ADDITIONAL INFORMATION
Allocation of Offer Shares to a Close Associate of the Existing Shareholders
The Company has sought, and the Stock Exchange has given, a consent under the paragraph 
1C(2) of Appendix F1 to the Listing Rules to permit Qiyuan Hong Kong to participate in the 
Global Offering as a cornerstone investor subject to the conditions that:
(a) 
our Company will comply with the public float requirements of Rule 19A.13A and 
the free float requirement under Rule 19A.13C of the Listing Rules. For details of the 
calculation of public float and free float of the Company, please refer to the section 
headed “History, Development and Corporate Structure” in this prospectus;
(b) 
the Offer Shares to be subscribed by and allocated to Qiyuan Hong Kong as a 
Cornerstone Investor under the Global Offering will be at the same Offer Price and on 
substantially the same terms as the other Cornerstone Investors (including being subject 
to a lock-up period of six months from the Listing Date, and Qiyuan Hong Kong shall 
pay and settle in full the consideration for the Offer Shares before the dealing commence 
on the Listing Date);
(c) 
no preference in allocation has been, nor will be, given to Qiyuan Hong Kong other than 
the preferential treatment of assured entitlement at the Offer Price under a cornerstone 
investment and the terms of the cornerstone investment agreement of the Qiyuan 
Hong Kong are substantially the same as the other cornerstone investment agreements 
following the principles set out in Chapters 2.3 and 4.15 of the Guide and each of the 
Company, the Joint Sponsors and the Overall Coordinators has provided the Stock 
Exchange with written confirmations in accordance with Chapters 2.3 and 4.15 of the 
Guide for New Listing Applicants; and
(d) 
details of the allocation of the Offer Shares to Qiyuan Hong Kong in the Global Offering 
as a cornerstone investor are disclosed in this prospectus, and details of the allocation 
will be disclosed in the allotment results announcement of our Company.
Such allocations of Offer Shares to Qiyuan Hong Kong, as the close associate of the Existing 
Shareholders is in compliance with all the conditions under the consent given by the Stock 
Exchange.
For details of the allocations of Offer Shares to Qiyuan Hong Kong, please refer to the section 
headed “Allotment Results Details — International Offering — Cornerstone Investors” in this 
announcement.

<<<PAGE 14>>>
– 14 –
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited 
and Hong Kong Securities Clearing Company Limited take no responsibility for the 
contents of this announcement, make no representation as to its accuracy or completeness 
and expressly disclaim any liability whatsoever for any loss howsoever arising from or in 
reliance upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in 
or into the United States (including its territories and possessions, any state of the United 
States and the District of Columbia) or any other jurisdiction where such distribution is 
prohibited by law. This announcement does not constitute or form a part of any offer to sell 
or solicitation of an offer to buy, to purchase or subscribe for securities nor shall there be 
any sale of Offer Shares in the United States or in any other jurisdictions in which such 
offer or solicitation would be unlawful. The securities mentioned herein have not been, 
and will not be, registered under the United States Securities Act or any state securities 
law of the United States. The securities may not be offered, sold, pledged, or transferred 
within the United States or to, or for the account or benefit of U.S. persons (as defined in 
Regulation S) except pursuant to an exemption from, or in a transaction not subject to, the 
registration requirements of the U.S. Securities Act and in compliance with any applicable 
state securities laws. The Offer Shares are being offered and sold outside the United States 
in offshore transactions in reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities of the Company. This announcement is 
not a prospectus. Potential investors should read the Prospectus dated June 15, 2026 issued 
by Shaanxi Micot Pharmaceutical Technology Co., Ltd. (陝西麥科奧特醫藥科技股份有限
公司) for detailed information about the Global Offering described below before deciding 
whether or not to invest in the Offer Shares.
* Potential investors of the Offer Shares should note that the Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate 
their obligations under the Hong Kong Underwriting Agreement upon the occurrence of any 
of the events set out in the paragraph headed “Underwriting — Underwriting Arrangements 
and Expenses — Hong Kong Public Offering — Grounds for Termination” in the Prospectus 
at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently 
expected to be Friday, June 24, 2026).
PUBLIC FLOAT AND FREE FLOAT
Rule 19A.13A of the Listing Rules requires that where the expected market value of the Shares 
at the time of Listing is over HK$6,000,000,000 but not exceeding HK$30,000,000,000, the 
minimum prescribed percentage of the Shares which must be H Shares held by the public is 
determined at the higher of: (i) the percentage that would result in the expected market value 
of the H Shares held by the public to be HK$1,500,000,000 at the time of Listing; and (ii) 
15%.

<<<PAGE 15>>>
– 15 –
Immediately after the completion of the Global Offering, an aggregate of 145,115,150 H 
Shares, representing approximately 43.74% of the total issued share capital of the Company 
upon the completion of the Global Offering will be counted towards the public float. Based 
on the Offer Price of HK$18.20 per Offer Share, the expected market capitalization of the 
Company’s H Shares would exceed HK$6,000,000,000 and the percentage that would result in 
the expected market value of H shares held by the public to be HK$1,500,000,000 at the time 
of Listing would be 24.84%. Therefore, the Company will be able to meet the public float 
requirement under Rule 19A.13A of the Listing Rules.
Rule 19A.13C(1) of the Listing Rules provides that, where a new applicant is a PRC issuer 
with no other listed shares at the time of listing, the portion of H shares for which listing is 
sought that are held by the public and not subject to any disposal restrictions at the time listing 
must normally (i) represent at least 10% of the total number of issued shares in the class to 
which H shares belong at the time of listing (excluding treasury shares), with an expected 
market value at the time of listing of not less than HK$50,000,000; or (ii) have an expected 
market value at the time of listing of not less than HK$600,000,000.
Immediately after the completion of the Global Offering, based on the Offer Price of 
HK$18.20, except for (i) 273,685,950 Shares held by all existing Shareholders that are 
subject to a lock-up period of twelve months following the Listing Date under applicable PRC 
law; and (ii) 24,681,000 Shares held by Cornerstone Investors that are subject to a lock-up 
period of six months from and including the Listing Date, all remaining 33,373,400 Shares, 
representing 10.06% of the total Shares, will be counted toward the free float. Therefore, our 
Company will be able to satisfy the free float requirement under Rule 19A.13C(1)(a) of the 
Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Wednesday, 
June 24, 2026 (Hong Kong time), provided that the Global Offering has become unconditional 
and the right of termination described in the section headed “Underwriting — Underwriting 
Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination” 
in the Prospectus has not been exercised. Investors who trade the H Shares on the basis of 
publicly available allocation details prior to the receipt of H Share certificates or prior to the 
H Share certificates becoming valid evidence of title do so entirely at their own risk.

<<<PAGE 16>>>
– 16 –
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on 
Wednesday, June 24, 2026 (Hong Kong time), it is expected that dealings in the H Shares on 
the Stock Exchange will commence at 9:00 a.m. on Wednesday, June 24, 2026 (Hong Kong 
time). The H Shares will be traded in board lots of 200 H Shares each, and the stock code of 
the H Shares will be 2335.
By order of the Board
Shaanxi Micot Pharmaceutical Technology Co., Ltd.
Dr. Wang Bing
Chairman, Chief Executive Officer and Executive Director
Hong Kong, June 23, 2026
As of the date of this announcement, the Board comprises (i) Dr. Wang Bing and Dr. Yu 
Weiping as executive Directors; (ii) Dr. Wang Mei, Mr. You Xiangdong, Dr. Song Gaoguang 
and Dr. Wang Nayi as non-executive Directors; and (iii) Dr. Xiangli Liuxu, Mr. Zhang 
Wenqiang and Mr. Wang Kaifeng as proposed independent non-executive Directors.
