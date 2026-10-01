# 配发结果公告抽取任务：6731.HK Direct Drive Tech Limited - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**28/09/2026 22:32**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0928/2026092802011.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6731.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock Exchange”) and Hong 
Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents of this announcement, make no 
representation as to its accuracy or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising 
from or in reliance upon the whole or any part of the contents of this announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those defined in 
the prospectus dated September 21, 2026 (the “Prospectus”) of Direct Drive Tech Limited (本末動力（北京）科技股份有限公
司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase or 
subscribe for securities. This announcement is not a prospectus. Potential investors should read the Prospectus for detailed 
information about the Global Offering described below before deciding whether or not to invest in the Offer Shares. Any 
investment decision in relation to the Offer Shares should be taken solely in reliance on the information provided in the 
Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States (including its 
territories and possessions, any state of the United States and the District of Columbia) or any other jurisdiction where such 
distribution is prohibited by law. This announcement does not, and is not intended to, constitute or form a part of any offer to sell 
or solicitation of an offer to buy, to purchase or subscribe for securities nor shall there be any sale of Offer Shares in the United 
States or in any other jurisdictions in which such offer or solicitation would be unlawful. The Offer Shares have not been, and will 
not be, registered under the United States Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or any 
state securities law of the United States. The securities may not be offered, sold, pledged, or transferred within the United States 
or to, or for the account or benefit of U.S. persons (as defined in Regulation S under the U.S. Securities Act (“Regulation S”)) 
except pursuant to an exemption from, or in a transaction not subject to, the registration requirements of the U.S. Securities Act 
and in compliance with any applicable state securities laws. There will be no public offering of the Offer Shares in the United 
States. The Offer Shares are being offered and sold outside the United States in offshore transactions in reliance on Regulation S 
under the U.S. Securities Act.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to terms and conditions set out in the Prospectus. 
The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/or not resident in Hong Kong.
In connection with the Global Offering, CITIC Securities (Hong Kong) Limited acts as the Sole Sponsor; and CLSA Limited acts 
as the Overall Coordinator.
Potential investors of the Offer Shares should note that the Sole Sponsor and Overall Coordinator (for itself and on behalf of 
the Hong Kong Underwriters) shall be entitled to terminate their obligations under the Hong Kong Underwriting Agreement 
with immediate effect upon the occurrence of any of the events set out in the paragraph headed “Underwriting — Hong Kong 
Underwriting Arrangement — Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any time prior to 
8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Tuesday, September 29, 2026).

<<<PAGE 2>>>
2
Direct Drive Tech Limited
本末動力（北京）科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
50,000,000 H Shares
Number of Hong Kong Offer Shares
:
10,000,000 H Shares (as adjusted after 
  reallocation)
Number of International Offer Shares
:
40,000,000 H Shares (as adjusted after 
  reallocation)
Offer Price
:
HK$21.60 per H Share plus brokerage 
  of 1%, SFC transaction levy of 0.0027%, 
  AFRC transaction levy of 0.00015% and 
  the Stock Exchange trading fee of 
  0.00565%
Nominal value
:
RMB0.10 per H Share
Stock code
:
6731
Sole Sponsor, Overall Coordinator, Joint Global Coordinator, 
Joint Bookrunner and Joint Lead Manager

<<<PAGE 3>>>
3
Direct Drive Tech Limited
本末動力（北京）科技股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the prospectus dated September 21, 2026 (the “Prospectus”) of Direct 
Drive Tech Limited (本末動力（北京）科技股份有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares could 
move substantially even with a small number of H Shares traded and should exercise extreme 
caution when dealing in the H Shares.
SUMMARY
Company Information
Stock code
6731
Stock short name
DIRECT DRIVE
Dealings commencement date
September 29, 2026*
*	
see note at the end of the announcement
Price Information
Offer Price
HK$21.60
Offer Shares and Share Capital
Number of Offer Shares
50,000,000
Number of Offer Shares in Hong Kong Public Offering 
  (after reallocation)
10,000,000
Number of Offer Shares in International Offering 
  (after reallocation)
40,000,000
Number of issued Shares upon Listing
369,588,080
Over-allocation
Number of Offer Shares over-allocated
0
Note: There is no over-allocation, and therefore the Over-allotment Option will not be exercised.

<<<PAGE 4>>>
4
Proceeds
Gross proceeds (Note)
HK$1,080.0 million
Less: Estimated listing expenses payable based on Offer Price
HK$97.5 million
Net proceeds
HK$982.5 million
Note:	Gross proceeds refers to the amount which the Company is entitled to receive. For details of 
the use of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” 
of the Prospectus.
ALLOTMENT RESULTS DETAILS
Hong Kong Public Offering
No. of valid applications
43,933
No. of successful applications
36,052
Subscription level
208.56 times
Claw-back triggered
Yes
No. of Offer Shares initially available under the Hong Kong 
  Public Offering
2,500,000
No. of Offer Shares reallocated from the International Offering
7,500,000
Final no. of Offer Shares under the Hong Kong Public Offering
10,000,000
% of Offer Shares under the Hong Kong Public Offering to 
  the Global Offering
20%
Note:	For details of the final allocation of shares to the Hong Kong Public Offering, investors can 
refer to www.eipo.com.hk/eIPOAllotment to perform a search by identification number or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees.

<<<PAGE 5>>>
5
International Offering
No. of placees
84
Subscription Level
2.72 times
No. of Offer Shares initially available under the 
  International Offering
47,500,000
No. of Offer Shares reallocated to the Hong Kong Public Offering
7,500,000
Final no. of Offer Shares under the International Offering
40,000,000
% of Offer Shares under the International Offering to 
  the Global Offering
80%
The Directors confirm that, to the best of their knowledge, information and belief, save for a 
waiver from strict compliance with Rules 9.09(b) and 10.04 of the Listing Rules and a consent 
under paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted 
by the Stock Exchange to permit the Company to allocate certain Offer Shares in the International 
Offering to close associates of existing Shareholders; (i) none of the Offer Shares subscribed by the 
placees and the public offer subscribers have been financed directly or indirectly by the Company, 
any of the Directors, chief executive of the Company, Controlling Shareholders, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective 
close associates; (ii) none of the placees and the public offer subscribers who have subscribed for 
or purchased the Offer Shares are accustomed to taking instructions from the Company, any of the 
Directors, chief executive of the Company, Controlling Shareholders, substantial Shareholders, 
existing Shareholders of the Company or any of its subsidiaries or their respective close associates 
in relation to the acquisition, disposal, voting or other disposition of Shares registered in his/her/
its name or otherwise held by him/her/it; (iii) there is no side agreement or arrangement between 
the Company, any of the Directors, chief executive of the Company, the Controlling Shareholders, 
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries or their 
respective close associates, on one hand, and the public offer subscribers or the placees who have 
subscribed for or purchased the Offer Shares, on the other hand; (iv) there is no side agreement 
or arrangement between the Company, any of the Directors, chief executive of the Company, the 
Controlling Shareholders, substantial Shareholders, existing Shareholders of the Company or 
any of its subsidiaries or their respective close associates, on one hand, and any other parties, on 
the other hand, in connection with the subscription, purchase, disposal, turnover or valuation of 
the Shares (which, for the avoidance of doubt, does not include agreements entered into with the 
Stabilizing Manager); and (v) no rebate has been, directly or indirectly, provided by the Company, 
any of the Directors, chief executive of the Company, the Controlling Shareholders, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective 
close associates, or syndicate members, or any other brokers involved in the Global Offering, to any 
investors in the Hong Kong Public Offering or placees in the International Offering.

<<<PAGE 6>>>
6
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of 
Offer 
Shares 
allocated
% of 
Offer 
Shares
% of total 
issued share 
capital after 
the Global 
Offering
Existing 
shareholders 
or their 
close 
associates
HK Technology Innovation
13,842,500
27.69%
3.75%
No
JSC International (for and 
  on behalf of Shenghai SP)
(Note)
7,929,400
15.86%
2.15%
Yes
Total
21,771,900
43.54%
5.89%
Note:
JSC International (for and on behalf of Shenghai SP) is a close associate of the existing 
Shareholders. The Stock Exchange has granted a waiver from strict compliance with the 
requirements under Rules 9.09(b) and 10.04 of and consent under Paragraph 1C(2) of Appendix 
F1 to the Listing Rules to permit H Shares in the International Offering to be placed to JSC 
International (for and on behalf of Shenghai SP), being a close associate of the existing 
Shareholders. For further details, see the sections headed “Waivers — Subscription of Offer Shares 
by Close Associate of Existing Shareholders and Core Connected Persons as Cornerstone Investor” 
and “Cornerstone Investors” in the Prospectus and the section headed “Allotment Results Details — 
International Offering — Allottee with waivers/consents obtained” in this announcement.

<<<PAGE 7>>>
7
Allottees with waivers/consents obtained
Investor
No. of 
Offer 
Shares 
allocated
% of 
Offer 
Shares
% of total 
issued share 
capital after 
the Global 
Offering
Relationship
Allottee with consent under paragraph 1C(1) of the Placing Guidelines in relation to 
allocations to connected client
(1)
Orient Asset Management 
  (Hong Kong) Limited 
  (“Orient AM”)
6,990,700
13.98%
1.89%
Connected client
Allottee with a waiver from strict compliance with Rules 9.09(b) and 10.04 of the Listing Rules 
and consent under paragraph 1C(2) of the Placing Guidelines in relation to allocations to close 
associate of existing Shareholders
JSC International (for and 
  on behalf of 
  Shenghai SP)
(2)
7,929,400
15.86%
2.15%
A 
cornerstone 
investor 
and 
a 
close 
associate 
o f 
e x i s t i n g 
Shareholder
Allottee with a waiver from strict compliance with Rule 10.04 of the Listing Rules and consent 
under paragraph 1C(2) of the Placing Guidelines in relation to allocation to a close associate 
of an existing Shareholder
Rockets Capital Advisor
(3)
231,400
0.46%
0.06%
A close associate 
o f 
e x i s t i n g 
Shareholder
Notes:
1.	 For details of the consents under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of 
the Guide for New Listing Applicants in relation to allocations to connected clients, please refer 
to the section headed “Additional Information” in this announcement.
2.	 For details of the waiver from strict compliance with Rules 9.09(b) and 10.04 of the Listing 
Rules and consent under paragraph 1C(2) of the Placing Guidelines and Chapter 2.5 of the 
Guide for New Listing Applicants in relation to allocation of Offer Shares to a close associate 
of existing Shareholders, please refer to the section headed “Additional Information” in this 
announcement.
3.	 For details of the waiver from strict compliance with Rule 10.04 of the Listing Rules and 
consent under paragraph 1C(2) of the Placing Guidelines and Chapter 2.5 of the Guide for New 
Listing Applicants in relation to allocation of Offer Shares to a close associate of an existing 
Shareholder, please refer to the section headed “Additional Information” in this announcement.

<<<PAGE 8>>>
8
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number 
of Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued 
Shares in the 
Company 
upon Listing
Last day subject to 
the lock-up 
undertakings
(1)
Mr. Zhang
(2)
131,991,840
35.71%
September 28, 2027
Notes:
1.	 Pursuant to the applicable PRC law, within the 12 months following the Listing Date, all 
existing Shareholders (including the Pre-IPO Investors) are prohibited from disposing of any of 
the Shares held by them.
2.	 Upon Listing, the Company will be held as to (i) approximately 18.99% by Worang Zhonghe, 
which was controlled by Mr. Zhang, (ii) approximately 13.77% by Worang Zhongchuang, 
which was controlled by its general partner Juwuxian, a company wholly owned by Mr. Zhang, 
and (iii) approximately 2.96% by Guyuan Investment, which was controlled by Juwuxian as 
its general partner and ultimately controlled by Mr. Zhang. The general partner of each of 
Zhongchuang No. 1, Zhongchuang No. 2 and Zhongchuang No. 3, which are limited partners 
of Worang Zhongchuang, is also Juwuxian. Therefore, Mr. Zhang was entitled to exercise a 
total of approximately 35.71% of the voting power at general meetings of the Company upon 
Listing. Each of Mr. Zhang, Worang Zhonghe, Worang Zhongchuang, Guyuan Investment, 
Zhongchuang No. 1, Zhongchuang No. 2 and Zhongchuang No. 3 and Juwuxian shall be subject 
to disposal restrictions pursuant to Rules 10.07 and 18C.13 of the Listing Rules.

<<<PAGE 9>>>
9
Key Persons
(1) (as defined under Rule 18C.14 of the Listing Rules) and their close associate(s)
Name
Capacity
Number 
of Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued 
Shares in the 
Company 
upon Listing
Last day 
subject to 
the lock-up 
undertakings 
(4)
Mr. Zhang
(2)
Founder, executive 
Director, chairman 
of the Board and 
chief executive 
officer
131,991,840
35.71%
September 28, 
2027
Worang Zhonghe
Mr. Zhang’s 
associate
70,191,810
18.99%
September 28, 
2027
Worang Zhongchuang
(3)
Mr. Zhang’s 
associate
50,876,570
13.77%
September 28, 
2027
Guyuan Investment
(3)
Mr. Zhang’s 
associate
10,923,460
2.96%
September 28, 
2027
Notes:
1.	 (i) Mr. Zhang, the founder, executive Director, chairman of the Board and chief executive 
officer; (ii) Mr. Zhang Hongbo, an executive Director, chief financial officer, secretary of the 
Board and joint company secretary of the Company; (iii) Dr. Liu Xuyang, an executive Director 
and president of the Company; (iv) Mr. Zhu Zhilong, vice president of the Company; (v) Dr. 
Yu Yanan, director of motor technology of the Company; (vi) Dr. Huang Yongcan, director of 
embodied joint module product line of the Company; and (vii) Mr. Liao Xuanhong, director 
of robotic technology of the Company are the executive Directors and key persons responsible 
for the technical operations and/or the research and development of the Specialist Technology 
Products and are subject to lock-up requirements pursuant to Rule 18C.14 of the Listing Rules. 
Mr. Zhang, Dr. Liu Xuyang, Mr. Zhang Hongbo, Dr. Huang Yongcan and Mr. Liao Xuanhong 
were granted options and/or restricted shares corresponding to certain underlying Shares. The 
Shares underlying the Employee Stock Ownership Scheme will be subject to a 12-month lock-
up period pursuant to the relevant PRC laws and regulations. For further details, please refer to 
the section headed “Appendix VI — Statutory and General Information — D. Employee Stock 
Ownership Scheme” in the Prospectus.

<<<PAGE 10>>>
10
2.	 Upon Listing, the Company will be held as to (i) approximately 18.99% by Worang Zhonghe, 
which was controlled by Mr. Zhang, (ii) approximately 13.77% by Worang Zhongchuang, 
which was controlled by its general partner Juwuxian, a company wholly owned by Mr. Zhang, 
and (iii) approximately 2.96% by Guyuan Investment, which was controlled by Juwuxian as 
its general partner and ultimately controlled by Mr. Zhang. The general partner of each of 
Zhongchuang No. 1, Zhongchuang No. 2 and Zhongchuang No. 3, which are limited partners 
of Worang Zhongchuang, is also Juwuxian. Therefore, Mr. Zhang was entitled to exercise a 
total of approximately 35.71% of the voting power at general meetings of the Company upon 
Listing.
3.	 Worang Zhongchuang and Guyuan Investment are employee stock ownership platforms of the 
Company. The Company had granted options and/or restricted shares corresponding to certain 
underlying Shares to certain selected participants.
4.	 Pursuant to the applicable PRC law, within the 12 months following the Listing Date, all 
existing Shareholders (including the Pre-IPO Investors) are prohibited from disposing of any of 
the Shares held by them.

<<<PAGE 11>>>
11
Pathfinder SIIs
Name
Capacity
Number 
of Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued 
Shares in the 
Company 
upon Listing
Last day 
subject to 
the lock-up 
undertakings 
(Note)
Shunxi Fund
Pathfinder SII
25,763,720
6.97%
September 28, 
2027
Lenovo Venture Capital
Pathfinder SII
12,234,660
3.31%
September 28, 
2027
Greenpine Chuangzhi
Pathfinder SII
7,468,150
2.02%
September 28, 
2027
Note:
In accordance with Rule 18C.14(2) of the Listing Rules, the required lock-up period commences on 
the date by reference to which disclosure of its shareholding is made in the Prospectus and ends on 
the date which is six months from the Listing Date, i.e. 28 March 2027. In addition to the lockup 
requirement under Rule 18C.14(2) of the Listing Rules, all existing Shareholders are not permitted 
to dispose of any of the Shares held by them within 12 months following the Listing Date, i.e. 
ending on 28 September 2027, as required under the applicable PRC laws.

<<<PAGE 12>>>
12
Pre-IPO Investors (as defined in the Prospectus)
Name
Number 
of Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued 
Shares in the 
Company 
upon Listing
Last day subject 
to the lock-up 
undertakings
(2)
All Pre-IPO Investors (except 
  for the Controlling Shareholders, 
  Key Persons and Pathfinder SIIs 
  as set out above)
(1)
142,129,710
38.46%
September 28, 2027
Notes:
1.	 Please see “History, Development and Corporate Structure — Details of the Pre-IPO 
Investments” in the Prospectus for the identities of the Pre-IPO Investors other than the Key 
Persons and Pathfinder SIIs.
2.	 Pursuant to the applicable PRC law, within the 12 months following the Listing Date, all 
existing Shareholders (including the Pre-IPO Investors) are prohibited from disposing of any of 
the Shares held by them.
Cornerstone Investors
Name
Number 
of Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued 
Shares in the 
Company 
upon Listing
Last day subject 
to the lock-up 
undertakings 
(Note)
HK Technology Innovation
13,842,500
3.75%
March 28, 2027
JSC International (for and on behalf 
  of Shenghai SP) 
7,929,400
2.15%
March 28, 2027
Note:
In accordance with the relevant cornerstone investment agreements, the required lock-up periods 
will end on March 28, 2027. The Cornerstone Investors will cease to be prohibited from disposing 
of or transferring the H Shares subscribed for pursuant to the relevant cornerstone investment 
agreements after the indicated date.

<<<PAGE 13>>>
13
PLACEE CONCENTRATION ANALYSIS
Placees
Number of
H Shares
allotted
Allotment as % 
of International 
Offering
Allotment as % 
of total
Offer Shares 
Number of
Shares
held upon
Listing
% of total 
issued share
capital upon 
Listing
Top 1
13,842,500
34.61%
27.69%
13,842,500
3.75%
Top 5
35,452,300
88.63%
70.90%
102,756,920
27.80%
Top 10
39,271,500
98.18%
78.54%
106,576,120
28.84%
Top 25
39,894,700
99.74%
79.79%
110,842,170
29.99%
Note:
*	
Ranking of placees is based on the number of H Shares allotted to the placees. 
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
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
H Shares
held upon
Listing
% of total issued 
H Shares capital
upon Listing
Number of
Shares
held upon
Listing
Top 1
0
0.00%
0.00%
131,991,840
35.71%
131,991,840
Top 5
21,771,900
54.43%
43.54%
264,982,580
71.70%
264,982,580
Top 10
21,771,900
54.43%
43.54%
306,567,130
82.95%
306,567,130
Top 25
38,692,800
96.73%
77.39%
358,280,880
96.94%
358,280,880
Note:
*	
Ranking of H Shareholders is based on the number of H Shares held by H Shareholders upon 
Listing. 

<<<PAGE 14>>>
14
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders
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
H Shares
held upon
Listing
Number of
Shares
held upon
Listing
% of total
issued share
capital upon
Listing
Top 1
0
0.00%
0.00%
131,991,840
131,991,840
35.71%
Top 5
21,771,900
54.43%
43.54%
264,982,580
264,982,580
71.70%
Top 10
21,771,900
54.43%
43.54%
306,567,130
306,567,130
82.95%
Top 25
38,692,800
96.73%
77.39%
358,280,880
358,280,880
96.94%
Note:
*	
Ranking of Shareholders is based on the number of Shares (of all classes) held by Shareholders 
upon Listing.

<<<PAGE 15>>>
15
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC 
OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by the 
public will be conditionally allocated on the basis set out below:
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
allotted of 
the total 
number of 
H Shares 
applied for
100
15,376
9,226 out of 15,376 to receive 100 Shares
60.00%
200
3,377
2,702 out of 3,377 to receive 100 Shares
40.01%
300
5,864
4,926 out of 5,864 to receive 100 Shares
28.00%
400
1,628
1,563 out of 1,628 to receive 100 Shares
24.00%
500
2,134
2,081 out of 2,134 to receive 100 Shares
19.50%
600
608
100 Shares
16.67%
700
436
100 Shares plus 31 out of 436 to receive additional 100 Shares
15.30%
800
391
100 Shares plus 63 out of 391 to receive additional 100 Shares
14.51%
900
390
100 Shares plus 66 out of 390 to receive additional 100 Shares
12.99%
1,000
2,898
100 Shares plus 725 out of 2,898 to receive additional 100 Shares
12.50%
1,500
866
100 Shares plus 433 out of 866 to receive additional 100 Shares
10.00%
2,000
1,565
100 Shares plus 783 out of 1,565 to receive additional 100 Shares
7.50%
2,500
548
100 Shares plus 343 out of 548 to receive additional 100 Shares
6.50%
3,000
525
100 Shares plus 341 out of 525 to receive additional 100 Shares
5.50%
3,500
201
100 Shares plus 151 out of 201 to receive additional 100 Shares
5.00%
4,000
311
100 Shares plus 236 out of 311 to receive additional 100 Shares
4.40%
4,500
494
100 Shares plus 395 out of 494 to receive additional 100 Shares
4.00%
5,000
694
100 Shares plus 590 out of 694 to receive additional 100 Shares
3.70%
6,000
233
100 Shares plus 214 out of 233 to receive additional 100 Shares
3.20%
7,000
194
100 Shares plus 186 out of 194 to receive additional 100 Shares
2.80%
8,000
185
200 Shares
2.50%
9,000
175
200 Shares plus 12 out of 175 to receive additional 100 Shares
2.30%
10,000
1,223
200 Shares plus 122 out of 1,223 to receive additional 100 Shares
2.10%
20,000
706
200 Shares plus 635 out of 706 to receive additional 100 Shares
1.45%
30,000
326
300 Shares
1.00%
40,000
221
300 Shares plus 9 out of 221 to receive additional 100 Shares
0.76%
50,000
335
300 Shares plus 17 out of 335 to receive additional 100 Shares
0.61%
60,000
129
300 Shares plus 62 out of 129 to receive additional 100 Shares
0.58%
70,000
119
400 Shares
0.57%
80,000
106
400 Shares plus 8 out of 106 to receive additional 100 Shares
0.51%
90,000
63
400 Shares plus 9 out of 63 to receive additional 100 Shares
0.46%
100,000
632
400 Shares plus 126 out of 632 to receive additional 100 Shares
0.42%
200,000
460
500 Shares
0.25%
 
Total
43,413
Total number of Pool A successful applicants: 35,532
 

<<<PAGE 16>>>
16
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
allotted of 
the total 
number of 
H Shares
applied for
300,000
338
7,500 Shares
2.50%
400,000
37
8,900 Shares
2.23%
500,000
40
9,700 Shares
1.94%
600,000
15
11,600 Shares
1.93%
700,000
7
13,200 Shares
1.89%
800,000
10
13,900 Shares
1.74%
900,000
11
15,200 Shares
1.69%
1,000,000
5
16,500 Shares
1.65%
1,100,000
5
17,800 Shares
1.62%
1,250,000
52
19,300 Shares
1.54%
 
Total
520
Total number of Pool B successful applicants: 520
 
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.

<<<PAGE 17>>>
17
ADDITIONAL INFORMATION
Placing to connected client with consent under paragraph 1C(1) of the Placing Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraphs 1C(1) of the Placing Guidelines to permit the Company to allocate such 
Offer Shares in the International Offering to Orient Asset Management (Hong Kong) Limited 
(“Orient AM”). The allocation of Offer Shares to Orient AM is in compliance with all the 
conditions under the consent granted by the Stock Exchange. Details of the placement to Orient AM 
are set out below.
No. 
Connected
client
Connected
distributor
Relationship
with the connected 
distributor
Basis of
holding securities
Number
of Offer
Shares
Whether 
connected client 
is a collective 
investment
scheme which is 
not authorised
by the SFC
or is expected
to hold the
Offer Shares
on behalf
of such scheme
Percentage
of the
Offer Shares
Percentage of 
total issued Shares 
of the Company 
immediately upon 
completion of the 
Global Offering 
1.
Orient Asset 
  Management 
  (Hong Kong) 
  Limited
(1)
Orient Securities 
  (Hong Kong) Limited 
  (“Orient Securities”)
Orient AM is 
  a member of 
  the same group 
  of companies as
  Orient Securities
Discretionary 
  on behalf of
  independent third 
  parties
6,990,700 Yes
13.98%
1.89%
Note:
(1)	
Orient AM will hold the Offer Shares in its capacity as the discretionary fund manager managing, OSR AM (HK) LTD 
CLIENT ACCOUNT — CHEN LIBO and OSR AM (HK) LTD CLIENT ACCOUNT — SUNGROW INTERNATIONAL 
LIMITED, which are collective investment schemes not authorized by the SFC, on behalf of their underlying clients, each 
of which is an independent third party of the Company, its subsidiaries, its substantial shareholders, Orient AM, Orient 
Securities and the companies which are members of the same group of Orient Securities. Details of the clients are as 
follows:
Client name
Types and values 
of assets under 
management
Whether 
the scheme 
is publicly 
marketed
Identities of the general 
partners and the 20 largest 
limited partners of the 
scheme where applicable
Identity of the scheme 
administrator
OSR AM (HK) LTD 
  CLIENT ACCOUNT 
— SUNGROW 
INTERNATIONAL LIMITED
Discretionary account
HK$120 million
No
General partner: not 
applicable as it is not a 
partnership structure 
Investor: Wan Shihao: 
100%
Agriculture Bank of 
China, Hong Kong 
Branch
OSR AM (HK) LTD 
  CLIENT ACCOUNT  
— CHEN LIBO
Discretionary account
US$110 million
No
General partner: not 
applicable as it is not a 
partnership structure 
Investor: Chen Libo: 100%
Agriculture Bank of 
China, Hong Kong 
Branch

<<<PAGE 18>>>
18
Placing to close associates of existing Shareholders with waivers from strict compliance with 
Rules 9.09(b) and 10.04 of the Listing Rules and consents under paragraph 1C(2) of the Placing 
Guidelines
For details of the allocation of Offer Shares to JSC International (for and on behalf of Shenghai 
SP) and Rockets Capital Advisor, please refer to the section headed “Allotment Results Details 
— International Offering — Allottees with waiver/consents obtained” in this announcement. The 
Company has applied to the Stock Exchange, and the Stock Exchange has granted, a waiver from 
strict compliance with Rules 9.09(b) and 10.04 of the Listing Rules and consent under paragraph 
1C(2) of the Placing Guidelines to permit the Company to allocate such Offer Shares in the 
International Offering to JSC International (for and on behalf of Shenghai SP). The Company 
has applied to the Stock Exchange, and the Stock Exchange has granted, a waiver from strict 
compliance with Rule 10.04 and consent under paragraph 1C(2) of the Placing Guidelines to permit 
the Company to allocate such Offer Shares in the International Offering to Rockets Capital Advisor.
Reallocation
As the International Offer Shares are oversubscribed and the Hong Kong Public Offering has been 
over-subscribed by more than 208.56 times of the total number of Offer Shares initially available 
under the Hong Kong Public Offering, the reallocation procedure as disclosed in the section 
headed “Structure of the Global Offering — The Hong Kong Public Offering — Reallocation and 
Clawback” in the Prospectus has been applied. The number of Offer Shares initially available 
under the Hong Kong Public Offering is 2,500,000 H Shares, representing approximately 5% of 
the total number of Offer Shares initially available under the Global Offering. As a result of such 
reallocation, the final number of Offer Shares under the Hong Kong Public Offering is adjusted to 
10,000,000 H Shares, representing approximately 20% of the total number of Offer Shares initially 
available under the Global Offering.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and the Stock Exchange trading fee payable.
The Directors and the Overall Coordinator confirm that at least 50% of the total number of the Offer 
Shares have been allocated to and taken up by independent price setting investors in compliance 
with Rule 18C.08 of the Listing Rules.
The Directors further confirm that at least 20% of the issued share capital of the Company will be 
held by sophisticated independent investors at the time of Listing in compliance with Chapter 2.5 of 
the Guide for New Listing Applicants.

<<<PAGE 19>>>
19
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the 
“Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no 
responsibility for the contents of this announcement, make no representation as to its accuracy or 
completeness and expressly disclaim any liability whatsoever for any loss howsoever arising from 
or in reliance upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and 
the District of Columbia). This announcement does not constitute or form a part of any offer or 
solicitation to purchase or subscribe for securities in the United States. The securities mentioned 
herein have not been, and will not be, registered under the United States Securities Act of 1933, 
as amended (the “U.S. Securities Act”). The securities may not be offered or sold in the United 
States except pursuant to an exemption from the registration requirements of the U.S. Securities 
Act and in compliance with any applicable state securities laws, or outside the United States 
unless in compliance with Regulation S under the U.S. Securities Act. There will be no public 
offer of securities in the United States.
The Offer Shares are being offered and sold outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated September 21, 2026 issued by Direct Drive 
Tech Limited (本末動力（北京）科技股份有限公司) for detailed information about the Global 
Offering described herein before deciding whether or not to invest in the Shares thereby being 
offered.
*	
Potential investors of the Offer Shares should note that the Sole Sponsor and Overall 
Coordinator (for itself and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate their obligations under the Hong Kong Underwriting Agreement with 
immediate effect upon the occurrence of any of the events set out in the paragraph headed 
“Underwriting — Hong Kong Underwriting Arrangement — Hong Kong Public Offering — 
Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) 
on the Listing Date (which is currently expected to be on Tuesday, September 29, 2026).

<<<PAGE 20>>>
20
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering, approximately 43.93% of the total 
number of issued Shares will be regarded as public float and based on the Offer Price of HK$21.60, 
the expected market capitalization of the Company upon Listing would exceed HK$6 billion but 
would not exceed HK$30 billion. Accordingly, the minimum prescribed public float percentage 
applicable to the H Shares under Rule 19A.13A(1) is approximately 18.79%, being the percentages 
that would result in the expected market value of H Shares held by the public at the time of Listing 
being HK$1.5 billion. Therefore, the Company will be able to meet the minimum public float 
requirement under Rule 19A.13A(1) of the Listing Rules.
Furthermore, immediately following the completion of the Global Offering, (i) the three largest 
public Shareholders do not hold more than 50% of the H Shares in public hands at the time of 
Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; (ii) there will not be any 
new substantial shareholder (as defined in the Listing Rules) of the Company immediately after the 
Global Offering; (iii) no placee will, individually, be placed more than 10% of the enlarged issued 
share capital of the Company immediately after the Global Offering; and (iv) there will be at least 
300 Shareholders at the time of Listing in compliance with Rule 8.08(2) of the Listing Rules.
It is expected that the market capitalization of the H Shares in issue upon Listing that are held 
by the public and not subject to any disposal restrictions at the time of the Listing would exceed 
HK$600,000,000. As such, the Company is expected to satisfy the free float requirement under Rule 
19A.13C of the Listing Rules at the time of the Listing.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. (Hong Kong time) 
on Tuesday, September 29, 2026, provided that the Global Offering has become unconditional and 
the right of termination described in the section headed “Underwriting — Hong Kong Underwriting 
Arrangement — Hong Kong Public Offering — Grounds for Termination” in the Prospectus has not 
been exercised. Investors who trade H Shares prior to the receipt of H Share certificates or the H 
Share certificates becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. (Hong Kong time) 
on Tuesday, September 29, 2026, it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. on Tuesday, September 29, 2026. The H Shares will be traded in board 
lots of 100 H Shares each. The stock code of the Shares is 6731.
By order of the Board
Direct Drive Tech Limited
Mr. ZHANG Di
Chairman of the Board, Executive Director and 
Chief Executive Officer
Hong Kong, September 28, 2026
As at the date of this announcement, the Board comprises (i) Mr. ZHANG Di, Dr. LIU Xuyang and Mr. ZHANG Hongbo 
as executive Directors; (ii) Mr. CHEN Can, Mr. ZHAO Yun and Mr. JI Haiquan as non-executive Directors; and (iii) 
Mr. LAM Kwok Sun, Dr. WANG Yuqian and Mr. HUANG Min as independent non-executive Directors.
