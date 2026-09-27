# 配发结果公告抽取任务：2553.HK Beijing Shougang LanzaTech Technology Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**02/06/2026 21:18**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0602/2026060202644.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2553.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for the Offer 
Shares in the United States or in any other jurisdictions. The Offer Shares have not been and will not be registered 
under the United States Securities Act of 1933, as amended from time to time (the “U.S. Securities Act”) or 
securities law of any state or other jurisdiction of the United States and may not be offered, sold, pledged or otherwise 
transferred within the United States, except in transactions exempt from, or not subject to, the registration requirements 
of the U.S. Securities Act and in compliance with any applicable state securities laws. The Offer Shares are being 
offered and sold outside the United States in offshore transactions in accordance with Regulation S under the U.S. 
Securities Act and applicable laws of each jurisdiction where those offers and sales occur. There will be no public 
offer of securities in the United States.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated 
May 26, 2026 (the “Prospectus”) issued by Beijing Shougang LanzaTech Technology Co., Ltd. (北京首鋼朗澤科技
股份有限公司) (the “Company”) for detailed information about the Global Offering described below before deciding 
whether or not to invest in the H Shares thereby being offered. Any investment decision in relation to the Offer Shares 
should be taken solely in reliance on the information in the Prospectus.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
In connection with the Global Offering, Yue Xiu Securities Company Limited, as stabilizing manager (the “Stabilizing 
Manager”) (or its affiliates or any person acting for it), on behalf of the Underwriters, the extent permitted by the 
applicable laws and regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect transactions with 
a view to stabilizing or supporting the market price of the H Shares at such price, in such amounts and in such manners 
as the Stabilizing Manager, its affiliates or any person acting for it may determine and at a level higher than that which 
might otherwise prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilizing 
Manager (or its affiliates or any person acting for it) to conduct any such stabilizing action. Such stabilizing action, 
if taken, (a) will be conducted at the absolute discretion of the Stabilization Manager (or its affiliates or any person 
acting for it) and in what the Stabilizing Manager reasonably regards as the best interest of our Company, (b) may 
be discontinued at any time and (c) is required to be brought to an end within 30 days of the last day for lodging 
applications under the Hong Kong Public Offering (which is Sunday, June 28, 2026). Such stabilizing action, if taken, 
may be effected in all jurisdictions where it is permissible to do so, in each case in compliance with all applicable 
laws, rules and regulatory requirements, including the Securities and Futures (Price Stabilizing) Rules (Chapter 571 W 
of the Laws of Hong Kong), as amended, made under the Securities and Futures Ordinance (Chapter 571 of the Laws 
of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering (which is Sunday, June 28, 2026). 
After this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the price of 
the H Shares, could fall.
Potential investors of the Offer Shares should note that the Sole Sponsor and the Overall Coordinator (for itself 
and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong 
Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the section headed 
“Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for termination” 
in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to 
be on Wednesday, June 3, 2026.

<<<PAGE 2>>>
2
BEIJING SHOUGANG LANZATECH TECHNOLOGY CO., LTD.
北京首鋼朗澤科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under
the Global Offering
:
40,000,000 H Shares
Number of Hong Kong Offer Shares
:
6,000,000 H Shares
Number of International
Offer Shares
:
34,000,000 H Shares
Final Offer Price
:
HK$14.60 per H Share, plus brokerage of 
 1.0%, SFC transaction levy of 0.0027%, 
 Hong Kong Stock Exchange trading fee 
 of 0.00565% and AFRC transaction levy 
 of 0.00015% (payable in full on 
 application in Hong Kong dollars 
 and subject to refund)
Nominal value
:
RMB1.00 per H Share 
Stock code
:
2553
Sole Sponsor
Overall Coordinator, Joint Global Coordinator, 
Joint Bookrunner and Joint Lead Manager
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
BEIJING SHOUGANG LANZATECH TECHNOLOGY CO., LTD.
北京首鋼朗澤科技股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Warning: In view of high concentration of shareholding in a small number of H Shareholders, 
H Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the 
same meanings as those defined in the prospectus dated May 26, 2026 (the “Prospectus”) issued 
by Beijing Shougang LanzaTech Technology Co., Ltd. (北京首鋼朗澤科技股份有限公司) (the 
“Company”).
SUMMARY
Company information
Stock code
2553
Stock short name
SHOUGANG LANZA
Dealings commencement date
June 3, 2026*
* see note at the end of the announcement
Price Information
Final Offer Price
HK$14.60
Offer Shares and Share Capital
Number of Offer Shares
40,000,000 H Shares
Final Number of Offer Shares in Hong Kong Public Offering
6,000,000 H Shares
Final Number of Offer Shares in International Offering
34,000,000 H Shares
Number of issued Shares upon Listing
400,000,000 Shares
Over-allocation
Number of Offer Shares over-allocated
–
The Overall Coordinator confirmed that there has been no over-allocation of the Offer Shares 
in the International Offering. Therefore, it is expected that the Over-allotment Option will not 
be exercised.

<<<PAGE 4>>>
4
Proceeds
Gross proceeds (Note)
HK$584 million
Less: Estimated listing expenses payable based on final Offer 
Price
HK$97.54 million
Net proceeds
HK$486.46 million
Note: Gross proceeds refers to the amount to which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
109,125
No. of successful applications
21,872
Subscription level
1,421.54 times
Claw-back triggered
N/A
No. of Offer Shares initially available under the Hong Kong Public 
Offering
4,000,000 
H Shares
No. of Offer Shares reallocated from the International Offering 
(reallocation)
2,000,000 
H Shares
Final no. of Offer Shares under the Hong Kong Public Offering
6,000,000 
H Shares
% of Offer Shares under the Hong Kong Public Offering to the Global 
Offering
15%
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/IPOResult to perform a search by identification number or www.hkeipo.hk/IPOResult for the 
full list of allottees.

<<<PAGE 5>>>
5
INTERNATIONAL OFFERING
No. of placees
97
Subscription level
0.95 times
No. of Offer Shares initially available under the International Offering
36,000,000 
H Shares
No. of Offer Shares reallocated to the Hong Kong Public Offering
(reallocation)
2,000,000 
H Shares
Final no. of Offer Shares under the International Offering
34,000,000 
H Shares
% of Offer Shares under the International Offering to the Global 
Offering
85%
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive, supervisors of the Company, Controlling 
Shareholders, substantial Shareholders, existing Shareholders of the Company or any of its 
subsidiaries or their respective close associates; and (ii) none of the placees and the public who 
have purchased the Offer Shares are accustomed to taking instructions from the Company, any of 
the Directors, chief executive, supervisors of the Company, Controlling Shareholders, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective 
close associates in relation to the acquisition, disposal, voting or other disposition of H Shares 
registered in his/her/its name or otherwise held by him/her/it.
The Overall Coordinator and the Directors confirm that the allocation cap pursuant to paragraph 9 
of Chapter 4.14 of the Guide for New Listing Applicants has not been exceeded.

<<<PAGE 6>>>
6
LOCK-UP UNDERTAKINGS
Controlling Shareholders
NameNote 1
Number of 
Unlisted 
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
shareholding in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakingsNote 2
Shougang  
Group Notes 3, 4, 6
95,532,658
–
23.88%
June 2, 2027
NZ Tang MingNotes 3, 5
–
34,137,886
8.53%
June 2, 2027
Caofeidian  
Fund Notes 4, 6
–
12,748,081
3.19%
June 2, 2027
Total
95,532,658
46,885,967
35.60%
–
Notes:
1. 
For illustrative purposes only, this subsection lists only those members of the Controlling Shareholders who 
hold Shares directly in the Company.
2. 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law. The 
required lock-up for existing Shareholders ends on June 2, 2027, being 12 months following the Listing Date. 
Pursuant to Rule 10.07 of the Listing Rules, each of the Controlling Shareholders has undertaken to the Stock 
Exchange and the Company that, she or it shall comply with the applicable lock-up requirements. For further 
details, please refer to the section headed “Underwriting – Underwriting Arrangements and Expenses – Hong 
Kong Public Offering – Undertakings to the Stock Exchange Pursuant to the Listing Rules – Undertakings by 
the Controlling Shareholders” in the Prospectus.
3. 
Pursuant to the Concert Party Agreements, Shougang Group and NZ Tang Ming concurred that they shall act 
in concert with respect to, inter alia, the voting during general meeting, for the period since the date of the 
Concert Party Agreements and up until they cease to hold any shares of the Company or upon the termination 
of the Concert Party Agreements. Please refer to “History, Development and Corporate Structure – Concert 
Party Arrangement” in the Prospectus for further details. As such, each of Shougang Group and NZ Tang 
Ming is deemed to be interested in the Shares each other is interested in.
4. 
Shougang Group is wholly-owned by Beijing State-owned Capital Operation and Management Company 
Limited (北京國有資本運營管理有限公司), which is in turn wholly-owned by the State-owned Assets 
Supervision and Administration Commission of People’s Government of Beijing Municipality. As at the 
Latest Practicable Date, Shares in which Shougang Group is interested consist of (i) 95,532,658 Unlisted 
Shares held at its own capacity; (ii) 12,748,081 Unlisted Shares (among which 12,748,081 Unlisted Shares 
will be converted to H Shares upon Listing) held by Caofeidian Fund, a company majority-held by its 
wholly-owned subsidiary, in which Shougang Group is deemed to be interested under the SFO; and (iii) 
34,137,886 Unlisted Shares (among which 34,137,886 Unlisted Shares will be converted to H Shares upon 
Listing) in which Shougang Group is deemed to be interested as a result of being a party acting-in-concert 
with NZ Tang Ming.

<<<PAGE 7>>>
7
5. 
As at the Latest Practicable Date, NZ Tang Ming was owned as to 65.57% by Ms. Dong, 30.89% by 
CTID Xinyuan and 3.54% by Ms. Ye. As at the Latest Practicable Date, Shares in which NZ Tang Ming 
is interested consist of (i) 34,137,886 Unlisted Shares (among which 34,137,886 Unlisted Shares will be 
converted to H Shares upon Listing) held at its own capacity; and (ii) 95,532,658 Unlisted Shares in which is 
deemed to be interested as a result of being a party acting-in-concert with Shougang Group.
6. 
Caofeidian Fund is a limited partnership established in the PRC, and is a private equity investment fund 
owned as to 72.00% of its economic interest by Beijing Shougang Fund Co., Ltd. (北京首鋼基金有限公司), 
a wholly-owned subsidiary of Shougang Group, approximately 3.00% by Shoucheng Rongshi and 25.00% 
by Hebei Jicai Industry Guidance Equity Investment Fund Co., Ltd. (河北省冀財產業引導股權投資基金有
限公司), a limited liability company ultimately controlled by the Department of Finance of Hebei Province. 
Caofeidian Fund is managed by its general partner and executive partner Shoucheng Rongshi which is 
wholly-owned by Shoucheng Holdings Limited (首程控股有限公司) (“Shoucheng Holdings”), a company 
listed on the Stock Exchange (stock code: 0697). As of the Latest Practicable Date, Shougang Group (together 
with its associates) was interested in approximately 17.95% in Shoucheng Holdings and was its single largest 
shareholder. Therefore, Shougang Group is deemed to be interested in the Shares held by Caofeidian Fund.
Other Existing Shareholders (including the Pre-IPO Investors as defined in the “History, 
Development and Corporate Structure” section of the Prospectus)
Name
Number of 
Unlisted 
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
shareholding in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakingsNote 1
Shanghai Mingda 
Industry and 
Shanghai Dehui
35,650,662
36,000,000
17.91%
June 2, 2027
LanzaTech Hong 
Kong
–
33,520,231
8.38%
June 2, 2027
Ruihong Investment
–
26,162,800
6.54%
June 2, 2027
Mitsui & Co., Ltd.
–
16,590,175
4.15%
June 2, 2027
Guofu Yonglang
–
12,029,865
3.01%
June 2, 2027
Pingyang Puyi
–
10,526,132
2.63%
June 2, 2027
Guangzhou Fanmei
–
7,848,801
1.96%
June 2, 2027
Tang Ming Hong 
Kong
–
4,535,755
1.13%
June 2, 2027
Zhuhai Jinsheng
2,267,877
2,267,878
1.13%
June 2, 2027

<<<PAGE 8>>>
8
Name
Number of 
Unlisted 
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
shareholding in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakingsNote 1
Beijing 
JiayeyuanNote 2
–
3,553,015
0.89%
June 2, 2029
Qingdao Baiwei 
Zhihe
–
1,511,918
0.38%
June 2, 2027
Shanghai Guoping
–
7,451,235
1.86%
June 2, 2027
Jiaxing Guoxing
–
5,107,028
1.28%
June 2, 2027
Binhe SIC
–
4,186,001
1.05%
June 2, 2027
Jiaxing Tianchen
–
4,186,001
1.05%
June 2, 2027
Jinxin Kaiying
–
4,186,001
1.05%
June 2, 2027
Total
37,918,539
179,662,836
54.40%
–
Notes:
1. 
Unless otherwise stated, the expiry date of the lock-up period shown in the table above is pursuant to the 
PRC Company Law. The required lock-up for existing Shareholders ends on June 2, 2027, being 12 months 
following the Listing Date.
2. 
Beijing Jiayeyuan voluntarily undertook not to transfer the Shares held by it for a period of 36 months from 
the Listing Date. Therefore, the lock-up period for Beijing Jiayeyuan ends on June 2, 2029.

<<<PAGE 9>>>
9
PLACEE CONCENTRATION ANALYSIS
Placees
* Numbers
of H Shares
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
% of
total issued
share capital
upon Listing
Top 1
5,313,600
15.63%
13.28%
5,313,600
1.33%
Top 5
17,100,600
50.30%
42.75%
17,100,600
4.28%
Top 10
24,816,000
72.99%
62.04%
24,816,000
6.20%
Top 25
30,587,000
89.96%
76.47%
30,587,000
7.65%
Note:
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders
* Numbers
of H Shares
allotted
Allotment as
% of
International
Offering
Allotment as
% of
total Offer
Shares
Number of
H Shares
held upon
Listing
% of
total issued
H Shares
capital upon
Listing
Number
of Shares
held upon
Listing
Top 1
0
0.00%
0.00%
46,885,967
17.59%
46,885,967
Top 5
0
0.00%
0.00%
159,159,173
59.71%
194,809,835
Top 10
5,313,600
15.63%
13.28%
202,328,806
75.91%
237,979,468
Top 25
23,498,400
69.11%
58.75%
250,047,203
93.81%
287,965,742
Note:
* 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.

<<<PAGE 10>>>
10
SHAREHOLDERS CONCENTRATION ANALYSIS
All Shareholders
* Numbers
of H Shares
allotted
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
% of
total issued
share capital
upon Listing
Top 1
0
0.00%
0.00%
142,418,625
35.60%
Top 5
0
0.00%
0.00%
290,342,493
72.59%
Top 10
5,313,600
15.63%
13.28%
333,512,126
83.38%
Top 25
23,498,400
69.11%
58.75%
383,498,400
95.87%
Note:
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
NO. OF
SHARES
APPLIED FOR
NO. OF
VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED
OF THE TOTAL
NO. OF H SHARES
APPLIED FOR
POOL A
200
30,809
617 out of 30,809 applicants to receive 200 H Shares
2.00%
400
16,511
569 out of 16,511 applicants to receive 200 H Shares
1.72%
600
4,754
207 out of 4,754 applicants to receive 200 H Shares
1.45%
800
2,345
120 out of 2,345 applicants to receive 200 H Shares
1.28%
1,000
3,578
208 out of 3,578 applicants to receive 200 H Shares
1.16%
1,200
1,828
118 out of 1,828 applicants to receive 200 H Shares
1.08%
1,400
991
70 out of 991 applicants to receive 200 H Shares
1.01%
1,600
1,195
91 out of 1,195 applicants to receive 200 H Shares
0.95%
1,800
961
78 out of 961 applicants to receive 200 H Shares
0.90%
2,000
10,817
930 out of 10,817 applicants to receive 200 H Shares
0.86%
3,000
2,254
244 out of 2,254 applicants to receive 200 H Shares
0.72%
4,000
1,703
218 out of 1,703 applicants to receive 200 H Shares
0.64%
5,000
2,236
324 out of 2,236 applicants to receive 200 H Shares
0.58%
6,000
1,540
248 out of 1,540 applicants to receive 200 H Shares
0.54%

<<<PAGE 11>>>
11
NO. OF
SHARES
APPLIED FOR
NO. OF
VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED
OF THE TOTAL
NO. OF H SHARES
APPLIED FOR
POOL A
7,000
771
136 out of 771 applicants to receive 200 H Shares
0.50%
8,000
761
144 out of 761 applicants to receive 200 H Shares
0.47%
9,000
574
116 out of 574 applicants to receive 200 H Shares
0.45%
10,000
4,121
885 out of 4,121 applicants to receive 200 H Shares
0.43%
20,000
2,378
757 out of 2,378 applicants to receive 200 H Shares
0.32%
30,000
1,498
600 out of 1,498 applicants to receive 200 H Shares
0.27%
40,000
930
439 out of 930 applicants to receive 200 H Shares
0.24%
50,000
872
467 out of 872 applicants to receive 200 H Shares
0.21%
60,000
800
476 out of 800 applicants to receive 200 H Shares
0.20%
70,000
528
343 out of 528 applicants to receive 200 H Shares
0.19%
80,000
471
330 out of 471 applicants to receive 200 H Shares
0.18%
90,000
388
291 out of 388 applicants to receive 200 H Shares
0.17%
100,000
3,229
2,564 out of 3,229 applicants to receive 200 H Shares
0.16%
200,000
2,897
200 H Shares plus 513 out of 2,897 applicants to receive 
additional 200 H Shares
0.12%
101,740
Total number of Pool A successful applicants: 14,487
POOL B
300,000
3,335
200 H Shares plus 667 out of 3,335 applicants to receive 
additional 200 H Shares
0.08%
400,000
990
200 H Shares plus 521 out of 990 applicants to receive 
additional 200 H Shares
0.08%
500,000
608
200 H Shares plus 511 out of 608 applicants to receive 
additional 200 H Shares
0.07%
600,000
567
400 H Shares plus 81 out of 567 applicants to receive 
additional 200 H Shares
0.07%
700,000
248
400 H Shares plus 109 out of 248 applicants to receive 
additional 200 H Shares
0.07%
800,000
219
400 H Shares plus 159 out of 219 applicants to receive 
additional 200 H Shares
0.07%
900,000
193
600 H Shares plus 2 out of 193 applicants to receive 
additional 200 H Shares
0.07%
1,000,000
702
600 H Shares plus 199 out of 702 applicants to receive 
additional 200 H Shares
0.07%
2,000,000
523
1,000 H Shares plus 450 out of 523 applicants to receive 
additional 200 H Shares
0.06%
7,385
Total number of Pool B successful applicants: 7,385
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.

<<<PAGE 12>>>
12
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the Offer Price in addition to any brokerage, AFRC transaction 
levy, SFC transaction levy and Stock Exchange trading fee payable.
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the 
“Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no 
responsibility for the contents of this announcement, make no representation as to its accuracy 
or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising 
from or in reliance upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and 
the District of Columbia). This announcement does not constitute or form a part of any offer 
to sell or solicitation to purchase or subscribe for securities in the United States or in any other 
jurisdictions in which such offer or solicitation would be unlawful. The securities mentioned 
herein have not been, and will not be, registered under the United States Securities Act of 1933 
as amended from time to time (the “U.S. Securities Act”) or any state securities law of the 
United States. The securities may not be offered, sold, pledged or transferred within the United 
States, except in transactions exempt from, or not subject to, the registration requirements of the 
U.S. Securities Act and in compliance with any applicable state securities laws. There will be no 
public offer of the Offer Shares in the United States.
The Offer Shares are being offered and sold solely outside the United States in offshore 
transactions in reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated May 26, 2026 issued by Beijing Shougang 
LanzaTech Technology Co., Ltd. (北京首鋼朗澤科技股份有限公司) for detailed information 
about the Global Offering described below before deciding whether or not to invest in the H 
Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Sole Sponsor and the Overall 
Coordinator (for itself and on behalf of the Hong Kong Underwriters) shall be entitled to 
terminate their obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the paragraph headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for 
termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing 
Date (which is currently expected to be on June 3, 2026).

<<<PAGE 13>>>
13
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering, the expected market capitalization of 
the Company would be HK$5,840 million, calculated based on the final Offer Price of HK$14.60. 
Under Rule 19A.13A(1), the minimum public float of the Company shall be 25% based on the 
final Offer Price of HK$14.60. The total number of listed H Shares held by the public (being 
163,519,646 H Shares) represents approximately 40.88% of the total issued Shares of the Company 
upon Listing. For details of the Shares held by certain of our Shareholders which shall not be 
counted towards the public float, see “History, Development and Corporate Structure – Public 
Float” in the Prospectus. Therefore, the Company will be able to meet the minimum public float 
requirement under Rule 19A.13A of the Listing Rules.
Immediately following the completion of the Global Offering and based on the final Offer Price 
of HK$14.60 per Offer Share, the expected market value of the H Shares held by the public and 
not subject to disposal restrictions (whether under contract, the Listing Rules, applicable laws or 
otherwise) will be HK$584 million, representing 10% of the total issued Shares of the Company 
upon Listing. As such, the Company will be able to satisfy the free float requirement under Rule 
19A.13C(1)(a) of the Listing Rules.
The Directors confirm that immediately following the completion of the Global Offering, (i) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of 
the Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder immediately after the Global Offering; (iii) the three largest public shareholders of 
the Company do not hold more than 50% of the H Shares in public hands at the time of the Listing 
in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 
Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Wednesday, June 
3, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting – Underwriting Arrangements 
and Expenses – Hong Kong Public Offering – Grounds for termination” in the Prospectus has 
not been exercised. Investors who trade the H Shares on the basis of publicly available allocation 
details prior to the receipt of H Share certificates or prior to the H Share certificates becoming 
valid evidence of title do so entirely at their own risk.

<<<PAGE 14>>>
14
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Wednesday, 
June 3, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. on Wednesday, June 3, 2026 (Hong Kong time). The H Shares will be 
traded in board lots of 200 H Shares each, and the stock code of the H Shares will be 2553.
By order of the Board
Beijing Shougang LanzaTech Technology Co., Ltd.
Executive Director and General Manager
Ms. Dong Yan
Hong Kong, June 2, 2026
As at the date of this announcement, the Board comprises: (i) Ms. Dong Yan and Mr. Lin Siyu as 
executive Directors; (ii) Dr. Ma Lishen, Dr. Jennifer Holmgren, Dr. Wu Bin, Mr. Zhang Dan and 
Ms. Wang Yan as non-executive Directors; and (iii) Dr. Hu Shanying, Dr. Feng Yingang, Dr. Chen 
Xin and Mr. Hoong Cheong Thard as independent non-executive Directors.
