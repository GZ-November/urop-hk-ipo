# 配发结果公告抽取任务：2632.HK Jiangsu New Vision Automotive Electronics Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**23/03/2026 22:27**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0323/2026032301630.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2632.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
  - 提示：最终基石股数 ÷ base offer（不含超额配售）。优先用公告基石表的 Total 行；若表内已给『假设超额配售权未行使』的百分比，可直接采用。

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
  - 提示：超额配售权实际行使并配发的股数；未行使填 0。另有 FULL EXERCISE OF THE OVER-ALLOTMENT OPTION 公告可交叉确认。
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
announcement does not, and is not intended to, constitute or form a part of any offer or solicitation to purchase or 
subscribe for securities in the United States or in any other jurisdiction. The Offer Shares have not been and will not 
be registered under the United States Securities Act of 1933, as amended from time to time (the “U.S. Securities 
Act”) or securities law of any state or other jurisdiction of the United States and may not be offered, sold, pledged or 
otherwise transferred within the United States, except in transactions exempt from, or not subject to, the registration 
requirements of the U.S. Securities Act and in compliance with any applicable state securities laws. There will be no 
public offer of the Offer Shares in the United States. The Offer Shares are being offered and sold solely outside the 
United States in offshore transactions in reliance on Regulation S under the U.S. Securities Act and applicable laws of 
each jurisdiction where those offers and sales occur.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. Potential investors should read the Prospectus for detailed information about the Company 
and the Global Offering described below before deciding whether or not to invest in the Offer Shares.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as 
those defined in the prospectus dated March 16, 2026 (the “Prospectus”) issued by Jiangsu New Vision Automotive 
Electronics Co., Ltd. (江蘇澤景汽車電子股份有限公司) (the “Company”).
Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the 
Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the 
section headed “Underwriting – Underwriting Arrangements and Expenses – The Hong Kong Public Offering – 
Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which 
is currently expected to be on March 24, 2026).

<<<PAGE 2>>>
2
Jiangsu New Vision Automotive Electronics Co., Ltd.
江蘇澤景汽車電子股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under the
Global Offering
:
16,226,500 H Shares
Number of Hong Kong Offer Shares
:
1,622,650 H Shares
Number of International Offer Shares
:
14,603,850 H Shares
Final Offer Price
:
HK$44.20 per H Share, plus brokerage of 
1.0%, SFC transaction levy of 0.0027%, 
AFRC transaction levy of 0.00015% and 
Stock Exchange trading fee of 0.00565%
Nominal value
:
RMB0.50 per H Share
Stock code
:
2632
Joint Sponsors, Overall Coordinators,
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
JIANGSU NEW VISION AUTOMOTIVE ELECTRONICS CO., LTD. 
江蘇澤景汽車電子股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND 
ALLOTMENT RESULTS
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
2632
Stock short name
NEW VISION CO
Dealings commencement date
March 24, 2026*
* see note at the end of the announcement
Price Information
Final Offer Price
HK$44.20
Offer Price Range
HK$42.00 – HK$48.00
Offer Shares and Share Capital
Number of Offer Shares
16,226,500
Number of Offer Shares in Hong Kong Public Offer
1,622,650
Number of offer shares in International Offering
14,603,850
Number of issued shares upon Listing
123,395,266
Proceeds
Gross proceeds (Note)
HK$717.21 million
Less: Estimated listing expenses payable based on  
Offer Price
HK$67.54 million
Net proceeds
HK$649.67 million
Note: Gross proceeds refers to the amount to which the Company is entitled receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” in the Prospectus.

<<<PAGE 4>>>
4
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
31,183
No. of successful applications
14,843
Subscription level
68.89 times
Reallocation
No
No. of Offer Shares initially available under the Hong Kong 
Public Offering
1,622,650
No. of Offer Shares reallocated from the International 
Offering (reallocation)
0
Final no. of Offer Shares under the Hong Kong Public 
Offering (after reallocation)
1,622,650
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering
10%
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/IPOResult to perform a search by name or identification number or www.hkeipo.hk/IPOResult for 
the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
71
Subscription level
1.34 times
No. of Offer Shares initially available under the 
International Offering
14,603,850
Number of Offer Shares reallocated to the Hong Kong 
Public Offering
0
Final no. of Offer Shares under the International Offering
14,603,850
% of Offer Shares under the International Offering to the 
Global Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) 
waivers under Rule 10.04 of the Listing Rules and consents under paragraph 1C(2) of Appendix 
F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock Exchange to permit the 
Company to allocate certain Offer Shares in the International Offering to the close associates 
of certain existing minority Shareholders, and (b) consent under paragraph 1C(1) of the Placing 
Guidelines and Chapter 4.15 of the Guide to permit the Company to allocate certain Offer Shares 
in the International Offering to a connected client, (i) none of the Offer Shares subscribed by 
the placees and the public have been financed directly or indirectly by the Company, any of the 
Directors, Supervisors, chief executive of the Company, Controlling Shareholders, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective 
close associates; and (ii) none of the placees and the public who have purchased the Offer Shares 
are accustomed to taking instructions from the Company, any of the Directors, Supervisors, 
chief executive of the Company, Controlling Shareholders, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates in 
relation to the acquisition, disposal, voting or other disposition of Shares registered in his/her/its 
name or otherwise held by him/her/it.

<<<PAGE 5>>>
5
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of
Offer
Shares
allocated
% of Offer
Shares
% of total
issued share
capital after 
the
Global 
Offering
Existing
shareholders 
or
their close
associates
Yingke No. 1 (Hongkong) Limited (盈科壹
號(香港)有限公司) (“Yingke No. 1”)
1,244,300
7.67%
1.01%
Yes
Hongkong High Tech Industrial (Beijing) 
Development Investment Co., Limited (香
港高精尖產業(北京)發展投資有限公司) 
(“Hongkong High Tech”)
1,243,200
7.66%
1.01%
Yes
Total
2,487,500
15.33%
2.02%
Note: Each of Yingke No. 1 and Hongkong High Tech is a close associate of the existing Shareholders, being 
Shunyi Fund and Yingke Fund. The Stock Exchange has granted a waiver from strict compliance with the 
requirements under Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the Placing Guidelines to 
permit Yingke No. 1 and Hongkong High Tech to participate in the International Offering as cornerstone investors. 
Please refer to the section headed “Waivers from Strict Compliance with the Listing Rules and Exemptions from 
the Companies (Winding Up and Miscellaneous Provisions) Ordinance – Waiver from Strict Compliance with Rule 
10.04 of the Listing Rules and the Stock Exchange’s Consent under Paragraph 1C of Appendix F1 to the Listing 
Rules in respect of Subscriptions of Offer Shares by Close Associates of Existing Shareholders as Cornerstone 
Investors” of the Prospectus for details.
Allottees with Waivers/Consents Obtained
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares
% of total 
issued share 
capital after 
the Global 
Offering
Relationship
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under 
paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by close associates of 
existing Shareholders Note 1
Shenzhen Bridge Asset Management 
Co., Ltd. (深圳市架橋資產管理有限
公司) (“Shenzhen Bridge”) Note 2
325,000
2.00%
0.26%
A placee and a close
associate of an
existing minority
Shareholder
Yangtze Grace Investment (Hong 
Kong) Limited Note 3
1,017,300
6.27%
0.82%
A placee and a close
associate of existing 
minority Shareholders
Kaize Investment (HK) Limited Note 4
1,526,000
9.40%
1.24%
A placee and a close 
associate of existing 
minority Shareholders

<<<PAGE 6>>>
6
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares
% of total 
issued share 
capital after 
the Global 
Offering
Relationship
Allottee with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide in 
relation to allocation to a connected client Note 1
Guotai Junan Investments (Hong 
Kong) Limited Note 2
325,000
2.00%
0.26%
A connected client of
Haitong International
Securities Company
Limited
Notes:
(1) 
For details of (i) the waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under 
paragraph 1C(2) of the Placing Guidelines in relation to subscription for H Shares by close associates of 
existing Shareholders, and (ii) the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 
4.15 of the Guide in relation to allocation to a connected client, please refer to the section headed “Others/
Additional Information” in this announcement.
(2) 
Shenzhen Bridge is a close associate of Jiaqiao Capital, which is an existing Shareholder. Shenzhen Bridge 
subscribes for the H Shares in the International Offering through GTHT Client TRS (as defined below). For 
details, please refer to the section headed “Others/Additional Information” in this announcement.
(3) 
Yangtze Grace Investment (Hong Kong) Limited is a close associate of Changjiang Investment (being 
Guangde Changzheng, Xiangyang Changzheng and Chutian Changxing), which are existing Shareholders.
(4) 
Kaize Investment (HK) Limited is a close associate of Changjiang Investment (being Guangde Changzheng, 
Xiangyang Changzheng and Chutian Changxing), which are existing Shareholders.
LOCK-UP UNDERTAKINGS
Controlling Shareholders (as defined in the Prospectus)
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
H Shares as
% of total 
issued
H Shares 
after the
Global 
Offering 
subject
to lock-up 
undertakings
upon Listing
% of total 
issued share
capital in the 
Company
subject to 
lock-up
undertakings
upon Listing
Last day 
subject to 
the lock-up 
undertakings Note
Mr. Zhang Tao
6,356,908
4,449,836
4.08%
5.15%
March 23, 2027
Mr. Zhang Bo
8,898,908
6,229,236
5.71%
7.21%
March 23, 2027
Mr. Wang Zhenggang
3,655,498
2,558,849
2.35%
2.96%
March 23, 2027
Mr. Lyu Tao
1,658,522
1,160,965
1.06%
1.34%
March 23, 2027
Ms. Ye Jing
4,146,298
2,902,409
2.66%
3.36%
March 23, 2027
Ms. Guo Hui
4,146,298
2,902,409
2.66%
3.36%
March 23, 2027
Ms. Lyu Xianglian
1,658,520
1,160,964
1.06%
1.34%
March 23, 2027

<<<PAGE 7>>>
7
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
H Shares as
% of total 
issued
H Shares 
after the
Global 
Offering 
subject
to lock-up 
undertakings
upon Listing
% of total 
issued share
capital in the 
Company
subject to 
lock-up
undertakings
upon Listing
Last day 
subject to 
the lock-up 
undertakings Note
Yangzhou Zeying
7,568,406
5,297,884
4.86%
6.13%
March 23, 2027
Yangzhou Zewu
9,771,438
6,840,007
6.27%
7.92%
March 23, 2027
Subtotal
47,860,796
33,502,559
30.73%
38.79%
Note: All existing Shareholders (including the Controlling Shareholders) shall not dispose of any of the Shares held 
by them within the 12 months following the Listing Date as required under the applicable PRC laws.
Other Existing Shareholders (including the Pre-IPO Investors as defined in the “History, 
Development and Corporate Structure” section of the Prospectus)
Name Note 1
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
H Shares as 
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued share
capital in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
Last day 
subject to 
the lock-up 
undertakings Note 2
Golden Growth
7,583,672
7,583,672
6.96%
6.15%
March 23, 2027
Qianzhan Yuanzhi
7,541,160
7,541,160
6.92%
6.11%
March 23, 2027
Kenge Capital
5,775,372
5,775,372
5.30%
4.68%
March 23, 2027
Suzhou Sushang
3,918,036
3,918,036
3.59%
3.18%
March 23, 2027
Jiaxing Kailian
3,872,180
3,872,180
3.55%
3.14%
March 23, 2027
Wenzhou Kechuang
3,601,446
3,601,446
3.30%
2.92%
March 23, 2027
Jiaqiao Capital
3,361,660
3,361,660
3.08%
2.72%
March 23, 2027
FAW Investment
2,848,442
2,848,442
2.61%
2.31%
March 23, 2027
Changjiang Investment
2,780,702
2,780,702
2.55%
2.25%
March 23, 2027
Binfu Capital
2,505,530
2,505,530
2.30%
2.03%
March 23, 2027
Jiaxing Juntai
2,400,000
2,400,000
2.20%
1.94%
March 23, 2027
Shunyi State Investment
2,305,976
2,305,976
2.11%
1.87%
March 23, 2027
Huang Zhigang
2,232,714
2,232,714
2.05%
1.81%
March 23, 2027
Lianshan Investment
1,458,684
1,458,684
1.34%
1.18%
March 23, 2027
Gongqingcheng Yintai
1,452,068
1,452,068
1.33%
1.18%
March 23, 2027

<<<PAGE 8>>>
8
Name Note 1
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
H Shares as 
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued share
capital in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
Last day 
subject to 
the lock-up 
undertakings Note 2
Gold Investment
1,181,672
1,181,672
1.08%
0.96%
March 23, 2027
Anhui Jiaokong
1,181,672
1,181,672
1.08%
0.96%
March 23, 2027
Ningbo Youfu
1,138,878
1,138,878
1.04%
0.92%
March 23, 2027
Yangzhou Qizheng
1,027,650
1,027,650
0.94%
0.83%
March 23, 2027
Yuhu Investment
455,696
455,696
0.42%
0.37%
March 23, 2027
Zhao Huarong
290,412
290,412
0.27%
0.24%
March 23, 2027
Zheng Yanhua
201,198
201,198
0.18%
0.16%
March 23, 2027
Zhang Feng
193,150
193,150
0.18%
0.16%
March 23, 2027
Subtotal
59,307,970
59,307,970
54.39%
48.06%
Notes:
(1) 
Please refer to the Prospectus for further details.
(2) 
The expiry date of the lock-up period shown in the table above is pursuant to applicable PRC laws. The 
required lock-up for existing Shareholders ends on March 23, 2027, being 12 months following the Listing 
Date.
Cornerstone Investors
Name
Number of 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total
issued H
Shares after the
Global Offering
% of 
shareholding in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings
Yingke No. 1
1,244,300
1.14%
1.01%
September 23, 2026
Hongkong High Tech
1,243,200
1.14%
1.01%
September 23, 2026
Subtotal
2,487,500
2.28%
2.02%
Note: In accordance with the relevant cornerstone investment agreements, the required lock-up ends on September 
23, 2026, being six months following the Listing Date. The Cornerstone Investors will cease to be prohibited from 
disposing of or transferring H Shares subscribed for pursuant to the relevant cornerstone investment agreements 
after the indicated date.

<<<PAGE 9>>>
9
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of 
H Shares 
allotted
Allotment as % 
of International 
Offering
Allotment as % 
of total Offer 
Shares
Number of
Shares held
upon Listing
% of total issued 
share capital 
upon Listing
Top 1
7,563,100
51.79%
46.61%
7,563,100
6.13%
Top 5
13,293,900
91.03%
81.93%
18,380,578
14.90%
Top 10
14,472,900
99.10%
89.19%
22,921,238
18.58%
Top 25
14,601,600
99.98%
89.99%
23,049,938
18.68%
Note:
* Ranking of placees is based on the number of Offer Shares allotted to the placees.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
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
Number of H 
Shares held 
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
0.00%
0.00%
33,502,559
30.73%
47,860,796
Top 5
7,563,100
51.79%
46.61%
61,965,863
56.83%
76,324,100
Top 10
12,918,900
88.46%
79.62%
83,560,217
76.63%
97,918,454
Top 25
13,967,900
95.65%
86.08%
106,093,669
97.30%
120,451,906
Note:
* Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders*
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
Number of H 
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
33,502,559
47,860,796
38.79%
Top 5
7,563,100
51.79%
46.61%
61,965,863
76,324,100
61.85%
Top 10
12,918,900
88.46%
79.62%
83,560,217
97,918,454
79.35%
Top 25
13,967,900
95.65%
86.08%
106,093,669
120,451,906
97.61%
Note:
* Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 10>>>
10
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:
Pool A
Number of 
H Shares 
applied for
Number. 
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
11,349
3,405 out of 11,349 applicants to receive 50 H Shares
30.00%
100
2,708
1,000 out of 2,708 applicants to receive 50 H Shares
18.46%
150
5,296
2,208 out of 5,296 applicants to receive 50 H Shares
13.90%
200
3,555
1,616 out of 3,555 applicants to receive 50 H Shares
11.36%
250
429
209 out of 429 applicants to receive 50 H Shares
9.74%
300
264
136 out of 264 applicants to receive 50 H Shares
8.59%
350
188
102 out of 188 applicants to receive 50 H Shares
7.75%
400
192
108 out of 192 applicants to receive 50 H Shares
7.03%
450
121
71 out of 121 applicants to receive 50 H Shares
6.52%
500
818
490 out of 818 applicants to receive 50 H Shares
5.99%
600
185
117 out of 185 applicants to receive 50 H Shares
5.27%
700
162
108 out of 162 applicants to receive 50 H Shares
4.76%
800
138
95 out of 138 applicants to receive 50 H Shares
4.30%
900
216
155 out of 216 applicants to receive 50 H Shares
3.99%
1,000
1,279
942 out of 1,279 applicants to receive 50 H Shares
3.68%
1,500
563
468 out of 563 applicants to receive 50 H Shares
2.77%
2,000
1,038
940 out of 1,038 applicants to receive 50 H Shares
2.26%
2,500
307
298 out of 307 applicants to receive 50 H Shares
1.94%
3,000
240
50 H Shares
1.67%
3,500
166
50 H Shares plus 12 out of 166 applicants to receive an additional 50 H Shares
1.53%
4,000
110
50 H Shares plus 13 out of 110 applicants to receive an additional 50 H Shares
1.40%
4,500
56
50 H Shares plus 9 out of 56 applicants to receive an additional 50 H Shares
1.29%
5,000
169
50 H Shares plus 33 out of 169 applicants to receive an additional 50 H Shares
1.20%
6,000
79
50 H Shares plus 21 out of 79 applicants to receive an additional 50 H Shares
1.05%
7,000
57
50 H Shares plus 19 out of 57 applicants to receive an additional 50 H Shares
0.95%
8,000
62
50 H Shares plus 24 out of 62 applicants to receive an additional 50 H Shares
0.87%
9,000
47
50 H Shares plus 20 out of 47 applicants to receive an additional 50 H Shares
0.79%
10,000
304
50 H Shares plus 142 out of 304 applicants to receive an additional 50 H Shares
0.73%
20,000
227
50 H Shares plus 183 out of 227 applicants to receive an additional 50 H Shares
0.45%

<<<PAGE 11>>>
11
Number of 
H Shares 
applied for
Number. 
of valid 
applications
Basis of allocation/ballot
Approximate 
percentage 
allotted of the 
total number 
of H Shares 
applied for
30,000
149
100 H Shares
0.33%
40,000
94
100 H Shares plus 21 out of 94 applicants to receive an additional 50 H Shares
0.28%
50,000
111
100 H Shares plus 42 out of 111 applicants to receive an additional 50 H Shares
0.24%
60,000
52
100 H Shares plus 26 out of 52 applicants to receive an additional 50 H Shares
0.21%
70,000
28
100 H Shares plus 15 out of 28 applicants to receive an additional 50 H Shares
0.18%
80,000
24
100 H Shares plus 18 out of 24 applicants to receive an additional 50 H Shares
0.17%
90,000
20
100 H Shares plus 16 out of 20 applicants to receive an additional 50 H Shares
0.16%
100,000
224
150 H Shares
0.15%
Total
31,027
Total number of Pool A successful applicants: 14,687
Pool B
Number of 
H Shares 
applied for
Number. 
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
92
3,600 H Shares plus 4 out of 92 applicants to receive an additional 50 H Shares
1.80%
300,000
27
5,300 H Shares
1.77%
400,000
17
7,000 H Shares
1.75%
500,000
9
8,700 H Shares
1.74%
600,000
2
10,350 H Shares
1.73%
700,000
3
12,000 H Shares
1.71%
811,300
6
13,800 H Shares
1.70%
Total
156 
Total number of Pool B successful applicants: 156
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.

<<<PAGE 12>>>
12
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Placing to close associates of existing Shareholders with a waiver under Rule 10.04 of the 
Listing Rules and a prior consent under paragraph 1C(2) of the Placing Guidelines
The Company has applied to the Stock Exchange, and the Stock Exchange has granted, a waiver 
from strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 
1C(2) of the Placing Guidelines to permit the Company to allocate certain Offer Shares in the 
International Offering to close associates of existing Shareholders as placees. The allocation 
of Offer Shares to such close associates of existing Shareholders is in compliance with all the 
conditions under the waiver/consent granted by the Stock Exchange.
For details of the allocations of Offer Shares to the close associates of existing Shareholders, 
please refer to the section headed “Allotment Results Details – International Offering – Allottees 
with Waivers/Consents Obtained” in this announcement.
Placing to a connected client with prior consent under paragraph 1C(1) of the Placing 
Guidelines and Chapter 4.15 of the Guide
The Company has applied to the Stock Exchange, and the Stock Exchange has granted, a consent 
under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide to permit the 
Company to allocate certain Offer Shares in the International Offering to a connected client as 
a placee. The allocation of Offer Shares to such connected client is in compliance with all the 
conditions under the consent granted by the Stock Exchange.

<<<PAGE 13>>>
13
Details of the placement to the connected client are set out below.
No.
Connected 
distributor
Connected client
Relationship
Whether the 
connected client will 
hold the beneficial 
interests of the 
Offer Shares on a 
non-discretionary 
basis or discretionary 
basis for independent 
third parties
Number 
of Offer 
Shares to be 
allocated to 
the connected 
client
Approximate 
percentage of 
Offer Shares 
allocated to 
the connected 
client
Approximate 
percentage 
of total 
issued share 
capital after 
the Global 
Offering
1.
Haitong International 
Securities Company 
Limited (“HTI 
Securities”)
Guotai Junan 
Investments (Hong 
Kong) Limited 
(“GTJAI”) Note 1
GTJAI is a member 
of the same group 
of HTI Securities
Non-discretionary 
basis
325,000
2.00%
0.26%
Note:
(1) 
GTJAI proposes to subscribe for and hold the Offer Shares as a placee under the International Offering on 
behalf of its ultimate client on a non-discretionary basis.
GTJAI shall hold the Offer Shares for hedging purpose as the single underlying asset of a back-to-back total 
return swap transaction (the “GTHT Back-to-back TRS”) to be entered into between GTJAI and Guotai 
Haitong Securities Co., Ltd. (國泰海通證券股份有限公司) (the “GTHT Onshore Parent”) in connection 
with a total return swap order (the “GTHT Client TRS”) to be entered into by GTHT Onshore Parent and an 
ultimate client (the “GTHT Onshore Ultimate Client”). Such GTHT Client TRS is to be fully funded by the 
GTHT Onshore Ultimate Client. GTJAI will hold the Offer Shares on a non-discretionary basis for the purpose 
of hedging the economic exposure under the GTHT Back-to-back TRS and GTHT Client TRS only. During the 
tenor of the GTHT Client TRS, all economic returns of the Offer Shares will be passed to the GTHT Onshore 
Ultimate Client and all economic losses shall be borne by the GTHT Onshore Ultimate Client, subject to the 
terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS, and GTJAI will not take part in 
any economic return or bear any economic loss in relation to the price of the Offer Shares. The GTHT Onshore 
Ultimate Client may request to redeem the Offer Shares at their own discretion, upon which GTJAI shall dispose 
of the Offer Shares and settle the GTHT Back-to-back TRS and GTHT Client TRS in cash in accordance with 
the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS documents. Due to its internal 
policy, GTJAI will not exercise the voting right attaching to the Offer Shares during the tenor of the GTHT 
Back-to-back TRS and GTHT Client TRS.
The GTHT Onshore Ultimate Client is Shenzhen Bridge Asset Management Co., Ltd., which is indirectly owned 
as to approximately 86.57% by Mr. Xu Bo (徐波). To the best knowledge of GTJAI after making all reasonable 
enquiries, each of the GTHT Onshore Ultimate Client and its beneficial owners is an independent third party of 
GTJAI, HTI Securities and the companies which are members of the same group of HTI Securities.
GTJAI is not a collective investment scheme which is not authorized by the SFC nor is expected to hold the 
Offer Shares on behalf of such scheme.

<<<PAGE 14>>>
14
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
offer of securities in the United States. The Offer Shares are being offered and sold solely 
outside the United States in offshore transactions in reliance on Regulation S under the U.S. 
Securities Act and applicable laws of each jurisdiction where those offers and sales occur.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated March 16, 2026 issued by the Company for 
detailed information about the Global Offering described below before deciding whether or not 
to invest in the H Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the 
Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the 
paragraph headed “Underwriting – Underwriting Arrangements and Expenses – The Hong Kong Public Offering – 
Hong Kong Underwriting Agreement – Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. 
(Hong Kong time) on the Listing Date (which is currently expected to be on March 24, 2026).

<<<PAGE 15>>>
15
PUBLIC FLOAT AND FREE FLOAT
Taking into consideration of the H Shares to be issued pursuant to the Global Offering, the public 
float of our Company will be approximately 61.21% upon the Listing, which is higher than the 
prescribed percentage of H Shares required to be held in public hands of 25% under Rule 8.08(1) 
(as amended and replaced by Rule 19A.13A(1)) of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering, (i) the 
three largest public Shareholders do not hold more than 50% of the H Shares in public hands at 
the time of Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; (ii) there will 
not be any new substantial Shareholder (as defined in the Listing Rules) of the Company; (iii) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of our 
Company immediately after the Global Offering; and (iv) there will be at least 300 Shareholders at 
the time of Listing in compliance with Rule 8.08(2) of the Listing Rules.
The Cornerstone Investors have agreed to a lock-up period of six months following the Listing 
Date and pursuant to the applicable PRC laws, each of the existing Shareholders of the Company 
(including the Pre-IPO Investors) are not permitted to dispose of any of the Shares held by them 
within the 12 months immediately following the Listing Date. As such, the H Shares held by the 
Cornerstone Investors and existing Shareholders of the Company upon the Listing shall not be 
counted towards the free float of the H Shares of the Company at the time of Listing. Based on an 
Offer Price of HK$44.20 per H Share, the Company satisfies the free float requirement under Rule 
19A.13C of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, March 
24, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting – Underwriting Arrangements 
and Expenses – The Hong Kong Public Offering – Grounds for Termination” in the Prospectus has 
not been exercised. Investors who trade the H Shares on the basis of publicly available allocation 
details prior to the receipt of H Share certificates or prior to the H Share certificates becoming 
valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Tuesday, 
March 24, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Tuesday, March 24, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 50 H Shares each, and the stock code of the H Shares will be 
2632.
By order of the Board
Jiangsu New Vision Automotive Electronics Co., Ltd.
Mr. Zhang Tao
Chairperson of the Board and Executive Director
Hong Kong, March 23, 2026
As at the date of this announcement, the Board comprises: (i) Mr. Zhang Tao, Mr. Zhang Bo and 
Mr. Fan Xin as executive directors; (ii) Mr. Hu Bin, Mr. You Tianyu and Ms. Zheng Shiying 
as non-executive directors; and (iii) Ms. Young Meng Ying, Ms. Sun Hui and Prof. Bai Jian as 
independent non-executive directors.
