# 配发结果公告抽取任务：6727.HK Transwarp Technology (Shanghai) Co., Ltd - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**18/09/2026 19:42**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0918/2026091801414.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6727.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated September 11, 2026 (the “Prospectus”) issued by Transwarp Technology (Shanghai) 
Co., Ltd. (星環信息科技(上海)股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an offer or an invitation to induce an 
offer by any person to acquire, purchase or subscribe for any securities of the Company. This announcement is not a 
prospectus. Potential investors should read the Prospectus for detailed information about the Company and the Global 
Offering described below before deciding whether or not to invest in the Offer Shares. Any investment decision in 
relation to the Offer Shares should be taken solely in reliance on the information provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not, and is not intended to, constitute or form a part of any offer to sell or solicitation to purchase 
or subscribe for any securities in the United States or in any other jurisdiction. The Offer Shares have not been, 
and will not be, registered under the United States Securities Act of 1933, as amended from time to time (the “U.S. 
Securities Act”) or securities law of any state or other jurisdiction of the United States and may not be offered, 
sold, pledged or otherwise transferred within the United States, except pursuant to an available exemption from, 
or in a transaction not subject to, the registration requirements of the U.S. Securities Act and in compliance with 
any applicable state securities laws. The Offer Shares are being offered and sold solely outside the United States in 
offshore transactions in reliance on Regulation S under the U.S. Securities Act. There will be no public offer of the 
Offer Shares in the United States.
Potential investors of the Offer Shares should note that the Sponsor and the Sole Sponsor-Overall Coordinator (for 
itself and on behalf of the other Hong Kong Underwriters) shall be entitled to terminate their obligations under the 
Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the 
paragraph headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – Hong 
Kong Underwriting Agreement – Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong 
Kong time) on the Listing Date (which is currently expected to be on Monday, September 21, 2026).

<<<PAGE 2>>>
2
Transwarp Technology (Shanghai) Co., Ltd.
星環信息科技(上海)股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
14,010,800 H Shares
Number of Hong Kong Offer Shares
:
2,802,200 H Shares (as adjusted after  
reallocation)
Number of International Offer Shares
:
11,208,600 H Shares (as adjusted after  
reallocation)
Final Offer Price
:
HK$49.00 per H Share, plus  
brokerage of 1.0%, SFC transaction  
levy of 0.0027%, Stock Exchange  
trading fee of 0.00565% and AFRC  
transaction levy of 0.00015% (payable  
in full on application in Hong Kong  
Dollars and subject to refund)
Nominal Value
:
RMB1.00 per H Share
Stock Code
:
6727
Sole Sponsor, Sole Sponsor-Overall Coordinator, Overall Coordinator,
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Overall Coordinators, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers
Joint Lead Manager

<<<PAGE 3>>>
3
TRANSWARP TECHNOLOGY (SHANGHAI) CO., LTD./星環信息科技(上海)股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the Prospectus issued by the Company.
SUMMARY
Company information
Stock code
6727
Stock short name
TRANSWARP
Dealings commencement date
September 21, 2026*
* 
see note at the end of the announcement
Price Information
Offer Price
HK$49.00
Offer Shares and Share Capital
Number of Offer Shares
14,010,800 H Shares
Final Number of Offer Shares in Hong Kong Public Offering
2,802,200 H Shares
Final Number of Offer Shares in International Offering
11,208,600 H Shares
Number of issued Shares upon Listing
135,146,716 Shares
Proceeds
Gross proceeds (Note)
HK$686.53 million
Less: Estimated listing expenses payable based on Final Offer 
Price
HK$57.08 million
Net proceeds
HK$629.45 million
Note: Gross proceeds refers to the amount to which the issuer is entitled receive. For details of the use of proceeds, 
please refer to the section headed “Future Plans and Use of Proceeds” in the Prospectus.

<<<PAGE 4>>>
4
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
20,485
No. of successful applications
6,342
Subscription level
73.86 times
Reallocation
Yes
No. of Offer Shares initially available under the Hong Kong Public 
Offering
700,600
No. of Offer Shares reallocated from the International Offering
2,101,600
Final no. of Offer Shares under the Hong Kong Public Offering
2,802,200
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering
20%
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors can refer 
to https://www.hkeipo.hk/IPOResult to perform a search by name or identification number or 
https://www.hkeipo.hk/IPOResult for the full list of allottees.
INTERNATIONAL OFFERING
No. of placees
50
Subscription level
1.42 times
No. of Offer Shares initially available under the International 
Offering
13,310,200
Final no. of Offer Shares under the International Offering
11,208,600
% of Offer Shares under the International Offering to the Global 
Offering
80%

<<<PAGE 5>>>
5
The Directors confirm that, to the best of their knowledge, information and belief, save for 
(a) a waiver from strict compliance with Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the 
Stock Exchange to permit H Shares in the International Offering to be placed to certain Permitted 
Existing Shareholders, and (b) a consent under paragraph 1C(1) of the Placing Guidelines granted 
by the Stock Exchange to permit H Shares in the International Offering to be placed to certain 
connected clients as disclosed in this announcement, (i) none of the Offer Shares subscribed by the 
placees and the public offer subscribers have been financed directly or indirectly by the Company, 
any of the Directors, chief executive of the Company, controlling shareholders, substantial 
shareholders, existing shareholders of the Company or any of its subsidiaries or their respective 
close associates; (ii) none of the placees and the public offer subscribers who have subscribed for 
or purchased the Offer Shares are accustomed to taking instructions from the Company, any of 
the Directors, chief executive of the Company, controlling shareholders, substantial shareholders, 
existing shareholders of the Company or any of its subsidiaries or their respective close associates 
in relation to the acquisition, disposal, voting or other disposition of Shares registered in his/her/
its name or otherwise held by him/her/it; (iii) there is no side agreement or arrangement between 
the Company, any of the Directors, chief executive of the Company, controlling shareholders, 
substantial shareholders, existing shareholders of the Company or any of its subsidiaries or their 
respective close associates, on one hand, and the public offer subscribers or the placees who have 
subscribed for or purchased the Offer Shares, on the other hand; (iv) there is no side agreement 
or arrangement between the Company, any of the Directors, chief executive of the Company, the 
controlling shareholders, substantial shareholders, existing shareholders of the Company or any 
of its subsidiaries or their respective close associates, on one hand, and any other parties, on the 
other hand, in connection with the subscription, purchase, disposal or valuation of the Shares; 
and (v) no rebate has been, directly or indirectly, provided by the Company, any of the Directors, 
chief executive of the Company, the controlling shareholders, substantial shareholders, existing 
shareholders of the Company or any of its subsidiaries or their respective close associates, or 
syndicate members, or any other brokers involved in the Global Offering, to any investors in the 
Hong Kong Public Offering or placees in the International Offering.
The placees in the International Offer include the following:
Cornerstone Investors (Note 1)
Name
No. of
Offer Shares
allocated
% of Offer
Shares
% of total
issued H
Shares after
the Global
Offering
% of total
issued
Shares after
the Global
Offering
Existing 
shareholders 
or their close 
associates
Electronic Channel 
Limited
714,200
5.10%
5.10%
0.53%
No
Luoyang Science 
Technology Innovate 
Group, Ltd. 
(“LUOYANG Sci-
Tech Inv.”)
792,300
5.65%
5.65%
0.59%
No
Note:
1. 
For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in 
the Prospectus.

<<<PAGE 6>>>
6
Allottees with waivers/consents obtained
Name
No. of
Offer Shares
allocated
% of Offer
Shares
% of total
issued H
Shares after
the Global
Offering
% of total
issued
Shares after
the Global
Offering
Relationship
Allottees with consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to connected clients (Note 
1)
Sheng Yuan Asset 
Management Limited 
(“Sheng Yuan AM”) 
(Note 2)
102,000
0.73%
0.73%
0.08%
Sheng Yuan AM is a 
member of the same group 
as Sheng Yuan Securities 
Limited (“Sheng Yuan 
Securities”) (a distributor 
of the Global Offering).
Long Trends Select LPF 
(“Long Trends LPF”) 
(Note 3)
346,900
2.48%
2.48%
0.26%
Long Trends LPF is 
a close associate of a 
substantial shareholder of 
Long Trends Securities 
Limited (“Long Trends 
Securities”) (a distributor 
of the Global Offering).
Notes:
1. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines in relation to allocations to connected 
clients, please refer to the section headed “Others/Additional Information – Placing to connected clients with 
prior consent under paragraph 1C(1) of the Placing Guidelines” in this announcement.
2. 
Sheng Yuan AM will hold the Offer Shares in its capacity as the discretionary fund manager managing assets on 
behalf of its underlying clients or mandates on a discretionary basis. To the best knowledge of Sheng Yuan AM, 
each of the underlying clients or mandates of Sheng Yuan AM and their respective ultimate beneficial owner(s) 
is an independent third party of Sheng Yuan AM, Sheng Yuan Securities and the companies which are members 
of the same group of companies as Sheng Yuan AM and Sheng Yuan Securities.
3. 
Long Trends LPF, a close associate of a substantial shareholder of Long Trends Securities and whose 
discretionary investment manager is Long Trends Securities, will hold the Offer Shares on behalf of its clients 
on a discretionary basis. To the best knowledge of Long Trends LPF, each of the clients of Long Trends LPF 
and their respective ultimate beneficial owner(s) is an independent third party of Long Trends LPF.

<<<PAGE 7>>>
7
LOCK-UP UNDERTAKINGS
Key Persons (as defined under Rule 18C.14 of the Listing Rules) and their close associates 
(Note 2)
Name
Capacity
Number of A Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
% of shareholding 
in the Company 
subject to lock-up 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings  
(Note 1)
Mr. SUN Yuanhao
Founder, executive Director, 
chairman of the Board, 
general manager and Core 
R&D Member
11,167,863
8.26%
September 20, 2027
Mr. LV Cheng
Executive Director, vice 
president and Core R&D 
Member
1,519,779
1.12%
September 20, 2027
Shanghai Zanxing 
(Note 3)
Close associate of Mr. SUN 
Yuanhao
7,537,589
5.58%
September 20, 2027
Ms. LI Yiduo 
(Note 4)
Executive Director, chief 
financial officer, secretary of 
the Board, and joint company 
secretary
9,856
0.01%
September 20, 2027
Notes:
1. 
In accordance with Rule 18C.14(1) of the Listing Rules, the required lock-up period for the Key Persons 
commences on the date by reference to which disclosure of its shareholding is made in the Prospectus and 
end on the date which is 12 months from the Listing Date, i.e. September 20, 2027.
2. 
Mr. LIU Wanggen is also entitled to outstanding share options representing 3,000 A Shares under the 2023 
Share Incentive Scheme, which are subject to a vesting period. Should these A Shares be vested within 12 
months from the Listing Date, such A Shares will be subject to a lock-up period ending on expiry of 12 
months from the Listing Date. See the section headed “Appendix VI – Statutory and General Information – D. 
2023 Share Incentive Scheme” in the Prospectus for details.
3. 
As of the Latest Practicable Date, (i) Mr. LV Cheng, Mr. ZHU Junchen (executive Director, vice president 
and Core R&D Member), Ms. WEN Ye (executive Director and deputy general manager), Mr. ZHANG 
Liming (executive Director and deputy general manager), Ms. LI Yiduo and Mr. LIU Wanggen (Core R&D 
Member and vice president) held their respective interests as limited partners in the Company’s employee 
shareholding platforms (including Jiaxing Xinghan, Jiaxing Xingzhi, Jiaxing Xinghuan and Jiaxing Xingye), 
which in turn are the limited partners of Shanghai Zanxing, and (ii) Mr. SUN Yuanhao held interests as 
general partner in Shanghai Zanxing as well as the Company’s other employee shareholding platforms 
(including Jiaxing Xingrong, Jiaxing Xinghan, Jiaxing Xingzhi, Jiaxing Xinghuan, Jiaxing Xingye and 
Shanghai Yexing) and Jiaxing Xingyuan, which in turn are the limited partners of Shanghai Zanxing. See 
the section headed “History, Development and Corporate Structure – Employee Incentive Schemes” in the 
Prospectus for details. Such (a) partnership interests held by the executive Directors, senior management and 
Core R&D Members in Shanghai Zanxing as well as in the limited partners of Shanghai Zanxing, and (b) 
partnership interests held by Jiaxing Xingrong, Jiaxing Xinghan, Jiaxing Xingzhi, Jiaxing Xinghuan, Jiaxing 
Xingye, Shanghai Yexing and Jiaxing Xingyuan in Shanghai Zanxing, will be subject to a lock-up period 
ending on the expiry of 12 months from the Listing Date.

<<<PAGE 8>>>
8
Name
Capacity
Number of A Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
% of shareholding 
in the Company 
subject to lock-up 
undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings  
(Note 1)
4. 
Ms. LI Yiduo is also entitled to outstanding share options representing 6,159 A Shares under the 2023 Share 
Incentive Scheme, which are subject to a vesting period. Should these A Shares be vested within 12 months 
from the Listing Date, such A Shares will be subject to a lock-up period ending on expiry of 12 months from 
the Listing Date. See the section headed “Appendix VI – Statutory and General Information – D. 2023 Share 
Incentive Scheme” in the Prospectus for details.
Cornerstone Investors
Name
Number of H 
Shares held in 
the Company 
subject to lock-
up undertakings 
upon Listing
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon Listing
% of 
shareholding in 
the Company 
subject to lock-
up undertakings 
upon Listing
Last day subject 
to the lock-up 
undertakings 
(Note 1)
Electronic Channel Limited
714,200
5.10%
0.53%
March 20, 2027
LUOYANG Sci-Tech Inv.
792,300
5.65%
0.59%
March 20, 2027
Total
1,506,500
10.75%
1.12%
Note:
1. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on March 
20, 2027. The Cornerstone Investors will cease to be prohibited from disposing of or transferring H Shares 
subscribed for pursuant to the relevant cornerstone investment agreements after the indicated date.

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
Allotment 
as % of total 
Offer Shares
Number of
Shares held 
upon Listing
% of total issued 
share capital 
upon Listing
Top 1
2,571,400
22.94%
18.35%
2,571,400
1.90%
Top 5
7,245,200
64.64%
51.71%
7,245,200
5.36%
Top 10
9,330,700
83.25%
66.60%
9,330,700
6.90%
Top 25
11,162,000
99.58%
79.67%
11,162,000
8.26%
Note
* 
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering
Allotment 
as % of total 
Offer Shares
Number of 
H Shares held 
upon Listing
% of total 
issued H 
Shares capital 
upon Listing
Number of 
Shares held 
upon Listing
Top 1
2,571,400
22.94%
18.35%
2,571,400
18.35%
2,571,400
Top 5
7,245,200
64.64%
51.71%
7,245,200
51.71%
7,245,200
Top 10
9,330,700
83.25%
66.60%
9,330,700
66.60%
9,330,700
Top 25
11,162,000
99.58%
79.67%
11,162,000
79.67%
11,162,000
Note
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
Allotment 
as % of total 
Offer Shares
Number of H 
Shares held 
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
0.00%
0.00%
0
27,163,372
20.10%
Top 5
4,983,600
44.46%
35.57%
4,983,600
45,307,575
33.52%
Top 10
4,983,600
44.46%
35.57%
4,983,600
55,063,016
40.74%
Top 25
8,208,400
73.23%
58.59%
8,208,400
65,365,032
48.37%
Note
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 10>>>
10
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
OF THE 
TOTAL NO. OF 
SHARES 
APPLIED FOR
POOL A
100
10,552
1,056 out of 10,552 applicants to receive 100 H Shares
10.01%
200
2,237
356 out of 2,237 applicants to receive 100 H Shares
7.96%
300
1,075
245 out of 1,075 applicants to receive 100 H Shares
7.60%
400
567
169 out of 567 applicants to receive 100 H Shares
7.45%
500
846
303 out of 846 applicants to receive 100 H Shares
7.16%
600
296
126 out of 296 applicants to receive 100 H Shares
7.09%
700
169
83 out of 169 applicants to receive 100 H Shares
7.02%
800
290
158 out of 290 applicants to receive 100 H Shares
6.81%
900
133
78 out of 133 applicants to receive 100 H Shares
6.52%
1,000
1,230
775 out of 1,230 applicants to receive 100 H Shares
6.30%
1,500
501
404 out of 501 applicants to receive 100 H Shares
5.38%
2,000
393
100 H Shares
5.00%
2,500
170
100 H Shares plus 34 out of 170 applicants to receive an additional 100 H Shares
4.80%
3,000
227
100 H Shares plus 94 out of 227 applicants to receive an additional 100 H Shares
4.71%
3,500
95
100 H Shares plus 58 out of 95 applicants to receive an additional 100 H Shares
4.60%
4,000
133
100 H Shares plus 107 out of 133 applicants to receive an additional 100 H Shares
4.51%
4,500
78
200 H Shares
4.44%
5,000
217
200 H Shares plus 42 out of 217 applicants to receive an additional 100 H Shares
4.39%
6,000
109
200 H Shares plus 65 out of 109 applicants to receive an additional 100 H Shares
4.33%
7,000
59
300 H Shares
4.29%
8,000
70
300 H Shares plus 23 out of 70 applicants to receive an additional 100 H Shares
4.16%
9,000
57
300 H Shares plus 41 out of 57 applicants to receive an additional 100 H Shares
4.13%
10,000
364
400 H Shares
4.00%
20,000
187
700 H Shares
3.50%
30,000
91
1,000 H Shares
3.33%
40,000
49
1,300 H Shares
3.25%
50,000
58
1,600 H Shares
3.20%
60,000
34
1,900 H Shares
3.17%
70,000
17
2,200 H Shares
3.14%
80,000
46
2,500 H Shares
3.13%
Total
20,350
Total number of Pool A successful applicants: 6,207

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
OF THE 
TOTAL NO. OF 
SHARES 
APPLIED FOR
POOL B
90,000
57
6,900 H Shares plus 25 out of 57 applicants to receive an additional 100 H Shares
7.72%
100,000
37
7,600 H Shares plus 30 out of 37 applicants to receive an additional 100 H Shares
7.68%
150,000
16
11,400 H Shares
7.60%
200,000
7
15,100 H Shares
7.55%
250,000
2
18,800 H Shares
7.52%
300,000
6
22,400 H Shares
7.47%
350,300
10
26,100 H Shares
7.45%
Total
135
Total number of Pool B successful applicants: 135
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules in respect of which consent has been 
obtained, the Company has complied with the Listing Rules and guidance materials in relation to 
the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in additional to any brokerage, AFRC 
transaction levy, SFC transaction levy and Stock Exchange trading fee payable.

<<<PAGE 12>>>
12
OTHERS/ADDITIONAL INFORMATION
Allocation of H Shares to existing minority Shareholders and their close associates
The Company has applied for, and the Stock Exchange has granted, a waiver from strict 
compliance with Rule 10.04 of, and a consent under paragraph 1C(2) of Appendix F1 to the 
Listing Rules to permit H Shares in the International Offering to be placed to certain existing 
minority Shareholders who (i) hold less than 5% of the voting rights in the Company prior to the 
completion of the Global Offering and (ii) are not and will not become (upon the completion of the 
Global Offering) core connected persons of the Company or the close associates of any such core 
connected person (together, the “Permitted Existing Shareholders”), on the following conditions:
(a) 
each Permitted Existing Shareholder to whom the Company may allocate the H Shares under 
the International Offering holds less than 5% of the total number of issued Shares prior to the 
completion of the Global Offering;
(b) 
each Permitted Existing Shareholder is not, and will not be, a core connected person of the 
Company or the close associate of any such core connected person immediately prior to or 
following the Global Offering;
(c) 
none of the Permitted Existing Shareholders has the power to appoint any Directors nor have 
any other special rights in the Company;
(d) 
allocation to the Permitted Existing Shareholders and their close associates will not affect 
the Company’s ability to satisfy the public float requirement as prescribed by the Stock 
Exchange under the waiver in respect of the strict compliance with the requirements of Rule 
19A.13A(2) of the Listing Rules;
(e) 
to the best knowledge and belief of the Company and the Sole Sponsor, and based on 
discussions between the Company and the Overall Coordinators and confirmations required 
to be submitted to the Stock Exchange by the Sole Sponsor, the Company will confirm to 
the Stock Exchange that in case of participation as placees, no preferential treatment will be 
given to the Permitted Existing Shareholders and/or their close associates in the allocation 
process by virtue of their relationship with the Company;
(f) 
in the case of participation as placees, the Overall Coordinators will confirm to the Stock 
Exchange that, to the best of their knowledge and belief, no preferential treatment has been, 
nor will be, given to any of the Permitted Existing Shareholders or their close associates by 
virtue of their relationship with our Company in any allocation in the International Offering; 
and
(g) 
the Sole Sponsor will confirm to the Stock Exchange that based on (i) its discussion with 
our Company and the Overall Coordinators; and (ii) the confirmations provided to the Stock 
Exchange by the Company and the Overall Coordinators, and to the best of their knowledge 
and belief, they have no reason to believe that the Permitted Existing Shareholders and/
or their close associates received any preferential treatment in the allocation process as 
placees by virtue of their relationship with the Company, and details of allocation to the 
Permitted Existing Shareholders holding more than 1% of the total number of issued Shares 
immediately prior to the completion of the Global Offering will be disclosed in the allotment 
results announcement of the Company.

<<<PAGE 13>>>
13
Please refer to the section headed “Waivers and Exemptions – Waiver in respect of Allocation 
of H Shares to Existing Minority Shareholders and their Close Associates” in the Prospectus for 
further details of the waiver and consent. The allocations of Offer Shares to the Permitted Existing 
Shareholders are in compliance with all the conditions under the waiver and consent granted by the 
Stock Exchange.
Waiver in respect of allocation to price setting investors
The Company has applied, and the Stock Exchange has granted, a waiver from strict compliance 
with the requirements under Rule 18C.08 of and Paragraph 11A of Appendix F1 to the Listing 
Rules in connection with the minimum allocation to independent price setting investors under the 
following conditions:
(a) 
the Offer Price of the H Shares will be determined with reference to the prevailing market 
price of the A Shares;
(b) 
the Company will comply with paragraph 3.2 of the Practice Note 18 of the Listing Rules, 
in particular, no more than 40% of the total number of Offer Shares will be allocated to 
cornerstone investors as described in the section headed “Cornerstone Investors” in the 
Prospectus;
(c) 
the Prospectus will disclose:
(i) 
the time for the determination of the Offer Price and the form of its publication;
(ii) the historical prices of the A Shares and trading volume on the STAR Market during the 
Track Record Period and up to the Latest Practicable Date;
(iii) the closing price of the A Shares on the Latest Practicable Date;
(iv) the discount of the high-end and low-end of the indicative Offer Price range to the 
closing price of the A Shares in (iii) above; and
(v) 
the source for investors to access the latest market price of the A Shares; and
(d) 
the Company will include in the allotment results announcement a description of the placees 
and the distribution of the International Offer Shares.
Please refer to the section headed “Waivers and Exemptions – Waiver in respect of Allocation to 
Price Setting Investors” in the Prospectus for further details of the waiver. All the conditions under 
the waiver granted by the Stock Exchange have been complied with.

<<<PAGE 14>>>
14
Placing to connected clients with prior consent under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines. Please refer to the section headed 
“Allotment Results Details – International Offering – Allottees with waivers/consents obtained” in 
this announcement for details. The Company has applied to the Stock Exchange for, and the Stock 
Exchange has granted, a consent under paragraph 1C(1) of the Placing Guidelines to permit the 
Company to allocate such Offer Shares in the International Offering to the connected clients. The 
allocation of Offer Shares to such connected clients is in compliance with all the conditions under 
the consent granted by the Stock Exchange.
For details of the placing to connected clients, please see “Allottees with waivers/consents 
obtained – Allottees with consent under paragraph 1C(1) of the Placing Guidelines in relation to 
allocations to connected clients” in this announcement.
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
offer of securities in the United States.
The Offer Shares are being offered and sold outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act.

<<<PAGE 15>>>
15
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated September 11, 2026 issued by Transwarp 
Technology (Shanghai) Co., Ltd. for detailed information about the Global Offering described 
below before deciding whether or not to invest in the Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Sponsor and the Sole Sponsor-
Overall Coordinator (for itself and on behalf of the other Hong Kong Underwriters) shall be 
entitled to terminate their obligations under the Hong Kong Underwriting Agreement with 
immediate effect upon the occurrence of any of the events set out in the paragraph headed 
“Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – 
Hong Kong Underwriting Agreement – Grounds for Termination” in the Prospectus at any time 
prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on 
Monday, September 21, 2026).
PUBLIC FLOAT AND FREE FLOAT
Under Rule 19A.13A(2) of the Listing Rules, the portion of H Shares held by the public, at 
the time of Listing, must (a) represent at least 10% of the Company’s total number of issued 
Shares (excluding treasury shares); or (b) have an expected market value of not less than 
HK$3,000,000,000. Immediately following the completion of the Global Offering, the total number 
of the H Shares issued pursuant to the Global Offering represents 10.37% of the total issued 
share capital of our Company (excluding treasury shares), which satisfy the minimum public float 
requirement under Rule 19A.13A(2)(a) of the Listing Rules.
Based on an Offer Price of HK$49.00 per H Share, the Company will satisfy the free float 
requirement under Rule 19A.13C(2) of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering, (i) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of 
the Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder immediately after the Global Offering; (iii) the three largest public shareholders of 
the Company do not hold more than 50% of the shares in public hands at the time of the Listing 
in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 
Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Monday, 
September 21, 2026 (Hong Kong time), provided that the Global Offering has become 
unconditional and the right of termination described in the section headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for 
Termination” in the Prospectus has not been exercised. Investors who trade the H Shares on the 
basis of publicly available allocation details prior to the receipt of H Share certificates or prior to 
the H Share certificates becoming valid evidence of title do so entirely at their own risk.

<<<PAGE 16>>>
16
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Monday, 
September 21, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Monday, September 21, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 100 H Shares each, and the stock code of the H Shares will 
be 6727.
By order of the Board
Transwarp Technology (Shanghai) Co., Ltd.
Mr. SUN Yuanhao
Chairman and Executive Director
Hong Kong, September 18, 2026
As at the date of this announcement, the Board comprises: (i) Mr. Sun Yuanhao, Mr. Lv Cheng, 
Mr. Zhu Junchen, Ms. Wen Ye, Mr. Zhang Liming and Ms. Li Yiduo as executive Directors; (ii) 
Mr. Huang Yihua, Mr. Ma Dongming and Mr. Liu Dong as independent non-executive Directors; 
and (iii) Ms. Liu Jin as proposed independent non-executive Director.
