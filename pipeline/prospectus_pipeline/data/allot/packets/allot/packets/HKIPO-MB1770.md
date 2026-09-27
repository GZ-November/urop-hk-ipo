# 配发结果公告抽取任务：1770.HK DKE Holding Company Limited - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND
ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**08/07/2026 21:38**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0708/2026070801214.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"1770.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited 
(the “Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) 
take no responsibility for the contents of this announcement, make no representation as to 
its accuracy or completeness and expressly disclaim any liability whatsoever for any loss 
howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
Unless otherwise defined herein, capitalised terms used in this announcement shall have the 
same meanings as those defined in the prospectus dated June 29, 2026 (the “Prospectus”) 
issued by DKE Holding Company Limited (浙江東方科脈電子股份有限公司) (the 
“Company”).
This announcement is for information purposes only and does not constitute an offer or an 
invitation to induce an offer by any person to acquire, purchase or subscribe for securities. 
This announcement is not a prospectus. Potential investors should read the Prospectus for 
detailed information about the Global Offering described below before deciding whether or 
not to invest in the Offer Shares.
This announcement is not for release, publication, distribution, directly or indirectly, in or 
into the United States (including its territories and possessions, any state of the United States 
and the District of Columbia). This announcement does not constitute or form a part of any 
offer to sell or solicitation to purchase or subscribe for securities in the United States or in 
any other jurisdictions. The Offer Shares have not been, and will not be, registered under the 
United States Securities Act of 1933, as amended from time to time (the “U.S. Securities Act”) 
or any states securities laws of the United States. The securities may not be offered or sold in 
the United States except pursuant to an effective registration statement or in accordance with 
an available exemption from, or in a transaction not subject to, the registration requirements 
of the U.S. Securities Act. It is not currently intended for there to be any public offer of 
securities in the United States. The Offer Shares are being offered and sold outside the United 
States in offshore transactions in reliance on Regulation S under the U.S. Securities Act.
In connection with the Global Offering, CITIC Securities (Hong Kong) Limited acts as the 
Sole Sponsor, CLSA Limited acts as the Sponsor-Overall Coordinator and CLSA Limited and 
SPDB International Capital Limited act as Overall Coordinators.
Potential investors of the Offer Shares should note that the Sole Sponsor and the Sponsor-
Overall Coordinator (for itself and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate their obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the section headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for 
Termination” in the Prospectus at any time at or prior to 8:00 a.m. on the Listing Date.

<<<PAGE 2>>>
– 2 –
DKE Holding Company Limited
浙江東方科脈電子股份有限公司
(a joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the Global 
Offering
:
5,118,600 H Shares
Number of Hong Kong Offer Shares
:
511,900 H Shares
Number of International Placing Shares
:
4,606,700 H Shares
Final Offer Price
:
HK$78.64 per H Share, plus brokerage 
of 1.0%, SFC transaction levy of 
0.0027%, AFRC transaction levy 
of 0.00015% and Hong Kong Stock 
Exchange trading fee of 0.00565%
Nominal value
:
RMB1.00 per H Share
Stock code
:
1770
Sole Sponsor and Sponsor-Overall Coordinator
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Bookrunners and Joint Lead Managers
(in alphabetical order)

<<<PAGE 3>>>
– 3 –
DKE Holding Company Limited
浙江東方科脈電子股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND 
ALLOTMENT RESULTS
Unless otherwise defined herein, capitalised terms used in this announcement shall have the 
same meanings as those defined in the prospectus dated June 29, 2026 (the “Prospectus”) 
issued by DKE Holding Company Limited (the “Company”).
SUMMARY
Company Information
Stock code
1770
Stock short name
DKE
Dealings commencement date
July 9, 2026*
* see note at the end of the announcement
Price Information
Final Offer Price
HK$78.64
Offer Price Range
HK$78.64 – HK$101.11
Offer Shares and Share Capital
Number of Offer Shares
5,118,600
Number of Offer Shares in Hong Kong Public Offering
511,900
Number of offer shares in International Placing
4,606,700
Number of issued shares upon Listing
51,185,739
Over-allocation
No. of Offer Shares over-allocated
0
Note: There is no over-allocation, and therefore no stabilization action will be taken and the Over-allotment 
Option will not be exercised.

<<<PAGE 4>>>
– 4 –
Proceeds
Gross proceeds (Note)
HK$402.53 million
Less: Estimated listing expenses payable based 
on Final Offer Price
HK$47.17 million
Net proceeds
HK$355.36 million
Note: Gross proceeds refer to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
126,957
No. of successful applications
9,652
Subscription level
1,067.54 times
Reallocation
N/A
No. of Offer Shares initially available under the 
Hong Kong Public Offering
511,900
Final no. of Offer Shares under the Hong Kong 
Public Offering
511,900
% of Offer Shares under the Hong Kong Public 
Offering to the Global Offering (after reallocation)
10%
Note: For details of the final allocation of Offer Shares to the Hong Kong Public Offering, investors 
can refer to www.eipo.com.hk/eIPOAllotment to perform a search by identification number or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees.

<<<PAGE 5>>>
– 5 –
INTERNATIONAL PLACING
No. of placees
52
Subscription Level
3.69 times
No. of Offer Shares initially available under the 
International Placing
4,606,700
Final no. of Offer Shares under the International 
Placing
4,606,700
% of Offer Shares under the International Placing to 
the Global Offering (after reallocation)
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for 
consents under paragraphs 1C(1) and 1C(2) of Appendix F1 to the Listing Rules (the “Placing 
Guidelines”) and under Chapter 4.15 of the Guide for New Listing Applicants (the “Guide”) 
granted by the Stock Exchange to permit the Company to, among other things, allocate 
certain Offer Shares in the International Placing to close associate of existing Shareholder 
and certain connected clients, (i) none of the Offer Shares subscribed by the placees and 
the public have been financed directly or indirectly by the Company, any of the Directors, 
chief executive of the Company, Controlling Shareholders, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates; 
and (ii) none of the placees and the public who have purchased the Offer Shares are 
accustomed to taking instructions from the Company, any of the Directors, chief executive of 
the Company, Controlling Shareholders, substantial Shareholders, existing Shareholders of 
the Company or any of its subsidiaries or their respective close associates in relation to the 
acquisition, disposal, voting or other disposition of H Shares registered in his/her/its name or 
otherwise held by him/her/it.

<<<PAGE 6>>>
– 6 –
The placees in the International Placing include the following:
Allottees with consents obtained
Investor
No. of Offer
Shares allocated
% of Offer Shares
% of total issued 
share capital in the 
Company after the 
Global Offering
Relationship
Allottee with consent under paragraph 1C(2) of the Placing Guidelines under Chapter 4.15 of the Guide in relation 
to allocation of Offer Shares to close associate of existing Shareholder (Note 1)
Qu Shengjun
254,300
4.968%
0.4968%
Close associate 
of existing 
Shareholder
Allottees with consents under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide in relation 
to allocations to connected clients (Note 2)
CITIC Asset Management
1,300
0.025%
0.0025%
Connected client
JA Investment SPC
381,450
7.452%
0.7452%
Connected client
SSIF AM Portfolio
1,300 
0.025%
0.0025%
Connected client
Notes:
1. 
The Stock Exchange has given a consent under paragraph 1C(2) of the Placing Guidelines and Chapter 
4.15 of Guide permit Offer Shares be placed the above placee who is a close associate of existing 
Shareholder. Please refer to the section headed “Additional Information” in this announcement.
2. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide 
in relation to allocations to connected clients, please refer to the section headed “Additional Information” 
in this announcement.

<<<PAGE 7>>>
– 7 –
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name
Number of H shares held in 
the Company subject to lock-
up undertakings upon Listing
% of total issued share 
capital in the Company 
subject to lock-up 
undertakings upon Listing
Last day subject 
to the lock-up 
undertakings (Note 1)
Concert Party Group
Mr. Zhou (Note 2)
9,578,935
18.71%
July 8, 2027
Mr. Lv (Note 2)
3,172,978
6.20%
July 8, 2027
Incentive Platforms
Dalian Longgu (Note 2)
2,175,000
4.25%
July 8, 2027
Jiaxing Longxi (Note 2)
1,035,000
2.02%
July 8, 2027
Jiaxing Longguan (Note 2)
985,500
1.93%
July 8, 2027
Subtotal
16,947,413
33.11%
Notes:
1. 
According to the PRC Company Law, all the Shares held by existing Shareholders (including the Controlling Shareholders) prior 
to the Global Offering are subject to a lock-up period of one year from the Listing Date.
2. 
On April 16, 2018, in order to optimize the governance structure, consolidate the control of the Company and ensure the 
sustainable development of the Company, the Concert Party Group entered into the Acting in Concert Agreement, pursuant to 
which Mr. Lv acknowledges and confirms that he will consult with Mr. Zhou and reach a unanimous decision with Mr. Zhou 
before exercising his Shareholder’s right, especially on the rights to convene a Shareholders’ meeting, right to propose and right 
to vote. If no consensus can be reached after full discussions, Mr. Lv will act according to the decision of Mr. Zhou. The Acting in 
Concert Agreement is effective from the date of the Acting in Concert Agreement until any of the Concert Party Group ceases to 
be interested in any of the issued Shares.
Mr. Zhou acts as the general partner of each of the Incentive Platforms, and is therefore deemed to be interested in the Shares 
held by the Incentive Platforms in the Company. The Incentive Platforms are not parties to the Acting in Concert Agreement, and 
do not form part of the Concert Party Group.
Accordingly, the Concert Party Group and the Incentive Platforms collectively form the Controlling Shareholders.

<<<PAGE 8>>>
– 8 –
Other Existing Shareholders (including the Pre-IPO Investors (as defined in the section 
headed “History, Development and Corporate Structure – Pre-IPO Investments” in the 
Prospectus))
Name(Note 2)
Number of H shares held in 
the Company subject to lock-up 
undertakings upon Listing
% of total issued share capital in 
the Company subject to lock-up 
undertakings upon Listing
Last day subject to 
the lock-up 
undertakings (Note 1)
Redbanyan Venture Capital
6,975,000
13.63%
July 8, 2027
Huang Tao(Note 3)
5,068,972
9.90%
July 8, 2027
Fuzhou Zhuiyuan
3,303,855
6.45%
July 8, 2027
Mr. Zhao Jinggang
2,700,000
5.27%
July 8, 2027
Shenzhen Xinrui
2,020,223
3.95%
July 8, 2027
Pingyang Kunyi
1,695,538
3.31%
July 8, 2027
Chuanqi Optoelectronics
1,255,500
2.45%
July 8, 2027
Shanghai Chaoyue Moore
1,010,111
1.97%
July 8, 2027
Mr. Gao Yanfeng
887,449
1.73%
July 8, 2027
Dalian Peninsula
685,428
1.34%
July 8, 2027
Dalian Junhao
678,215
1.33%
July 8, 2027
Jiaxing Honghai
606,066
1.18%
July 8, 2027
Fuzhou Zijing
513,922
1.00%
July 8, 2027
Ningbo Gongshang Huifu
411,256
0.80%
July 8, 2027
Tianjin Junxian
404,043
0.79%
July 8, 2027
Lishui Shanrong Haina
202,022
0.39%
July 8, 2027
Zhuhai Hengzhen Tianxing
202,022
0.39%
July 8, 2027
Beijing Yitang Changhou
202,022
0.39%
July 8, 2027
Zhu Zhaofu
202,022
0.39%
July 8, 2027
Gu Jinzhou
90,000
0.18%
July 8, 2027
Hainan Chaoyue Moore
6,060
0.01%
July 8, 2027
Subtotal
29,119,726
56.89%
Notes:
(1) 
According to the PRC Company Law, all the Shares held by existing Shareholders (including the Pre-IPO Investors) prior to the 
Global Offering are subject to a lock-up period of one year from the Listing Date.
 (2) 
Please refer to the section headed “History, Development and Corporate Structure – Pre-IPO Investments” in the Prospectus for 
details.
(3) 
Huang Tao’s interest is held through Tibet Wanqing, Fuzhou Jinyuan and Tibet Yuankun, all of which are controlled by Huang 
Tao.

<<<PAGE 9>>>
– 9 –
PLACEE CONCENTRATION ANALYSIS
Placees (Note 1)
Number of 
H Shares 
allotted
Allotment as % 
of International 
Placing
Allotment as % 
of total 
Offer Shares
Number of 
Shares held 
upon Listing
% of total 
issued share 
capital upon 
Listing
Top 1
1,207,900
26.2%
23.6%
1,207,900
2.4%
Top 5
2,928,350
63.6%
57.2%
2,928,350
5.7%
Top 10
3,952,250
85.8%
77.2%
4,630,465
9.0%
Top 25
4,531,750
98.4%
88.5%
5,209,965
10.2%
Note:
1. 
Ranking of placees is based on the number of H Shares allotted to the placees
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders (Note 1)
Number of 
H Shares 
allotted
Allotment as % 
of International 
Placing
Allotment as % 
of total 
Offer Shares
Number of 
H Shares held 
upon Listing
% of total 
issued H Shares 
capital upon 
Listing
Top 1
–
–
–
16,947,413
33.1%
Top 5
–
–
–
34,995,240
68.4%
Top 10
1,207,900
26.2%
23.6%
42,190,572
82.4%
Top 25
3,725,550
80.9%
72.8%
49,298,645
96.3%
Note:
1. 
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders (Note 1)
Number of 
H Shares 
allotted
Allotment as % 
of International 
Placing
Allotment as % 
of total 
Offer Shares
Number of 
H Shares held 
upon Listing
% of total
issued share
capital upon
Listing
Top 1
–
–
–
16,947,413
33.1%
Top 5
–
–
–
34,995,240
68.4%
Top 10
1,207,900
26.2%
23.6%
42,190,572
82.4%
Top 25
3,725,550
80.9%
72.8%
49,298,645
96.3%
Note:
1. 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon 
Listing.

<<<PAGE 10>>>
– 10 –
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
NO. OF 
H SHARES
APPLIED FOR
NO. OF 
VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED
OF THE TOTAL 
NO. OF
H SHARES 
APPLIED FOR
POOL A
50
79,597
2,388 out of 79,597 to receive 50 H Shares
3.00%
100
6,989
266 out of 6,989 to receive 50 H Shares
1.90%
150
2,117
89 out of 2,117 to receive 50 H Shares
1.40%
200
1,557
75 out of 1,557 to receive 50 H Shares
1.20%
250
2,222
108 out of 2,222 to receive 50 H Shares
0.97%
300
892
45 out of 892 to receive 50 H Shares
0.84%
350
500
26 out of 500 to receive 50 H Shares
0.74%
400
631
34 out of 631 to receive 50 H Shares
0.67%
450
6,760
383 out of 6,760 to receive 50 H Shares
0.63%
500
6,438
373 out of 6,438 to receive 50 H Shares
0.58%
600
568
34 out of 568 to receive 50 H Shares
0.50%
700
375
23 out of 375 to receive 50 H Shares
0.44%
800
377
24 out of 377 to receive 50 H Shares
0.40%
900
1,227
80 out of 1,227 to receive 50 H Shares
0.36%
1,000
1,693
112 out of 1,693 to receive 50 H Shares
0.33%
1,500
912
63 out of 912 to receive 50 H Shares
0.23%
2,000
851
61 out of 851 to receive 50 H Shares
0.18%
2,500
634
48 out of 634 to receive 50 H Shares
0.15%
3,000
480
37 out of 480 to receive 50 H Shares
0.13%
3,500
266
22 out of 266 to receive 50 H Shares
0.12%
4,000
342
29 out of 342 to receive 50 H Shares
0.11%
4,500
275
24 out of 275 to receive 50 H Shares
0.10%
5,000
1,020
90 out of 1,020 to receive 50 H Shares
0.09%
6,000
403
38 out of 403 to receive 50 H Shares
0.08%
7,000
293
28 out of 293 to receive 50 H Shares
0.07%
8,000
283
28 out of 283 to receive 50 H Shares
0.06%
9,000
254
26 out of 254 to receive 50 H Shares
0.06%
10,000
1,699
177 out of 1,699 to receive 50 H Shares
0.05%
20,000
1,053
126 out of 1,053 to receive 50 H Shares
0.03%
30,000
626
113 out of 626 to receive 50 H Shares
0.03%
40,000
733
149 out of 733 to receive 50 H Shares
0.03%
 
122,067
Total number of Pool A successful applicants: 5,119
 

<<<PAGE 11>>>
– 11 –
NO. OF 
H SHARES
APPLIED FOR
NO. OF 
VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED
OF THE TOTAL 
NO. OF
H SHARES 
APPLIED FOR
POOL B
50,000
2,104
1,852 out of 2,104 to receive 50 H Shares
0.09%
60,000
760
686 out of 760 to receive 50 H Shares
0.08%
70,000
320
296 out of 320 to receive 50 H Shares
0.07%
80,000
332
327 out of 332 to receive 50 H Shares
0.06%
90,000
152
150 out of 152 to receive 50 H Shares
0.05%
100,000
497
50 H Shares
0.05%
150,000
206
50 H Shares plus 94 out of  206 to receive additional 50 
H Shares
0.05%
200,000
122
50 H Shares plus 95 out of  122 to receive additional 50 
H Shares
0.04%
255,950
397
100 H Shares
0.04%
 
4,890
Total number of Pool B successful applicants: 4,533
 
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in 
respect of which consent has been obtained, the Company has complied with the Listing Rules 
and guidance materials in relation to the placing, allotment and listing of the H shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by 
the placees or the public (as the case may be) directly or indirectly for each Offer Share 
subscribed for or purchased by them was the same as the final Offer Price in addition to any 
brokerage, SFC transaction levy, AFRC transaction levy and Stock Exchange trading fee 
payable.
ADDITIONAL INFORMATION
Placing to a close associate of existing Shareholder with prior consent under paragraph 
1C(2) of the Placing Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, 
a consent under paragraph 1C(2) of the Placing Guidelines to permit a close associate of 
existing Shareholder participate in the Global Offering. Qu Shengjun is the general partner of 
Dalian Junhao, which is an existing minority Shareholder who (i) holds less than 5% of the 
voting rights in our Company prior to the completion of the Global Offering and (ii) is not and 
will not become (upon the completion of the Global Offering) core connected person of the 
Company or the close associates of any such core connected person. The allocation of Offer 
Shares to such close associate of existing Shareholder is in compliance with all the conditions 
under the consent granted by the Stock Exchange.

<<<PAGE 12>>>
– 12 –
For details of the allocations of Offer Shares to such close associates of existing Shareholders 
and such connected clients, please refer to the section headed “Allotment Results Details – 
International Placing – Allottees with Consents Obtained” in this announcement.
Placing to connected clients with prior consent under paragraph 1C(1) of the Placing 
Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraph 1C(1) of the Placing Guidelines to permit the connected clients listed 
below to participate in the Global Offering. The allocation of Offer Shares to such connected 
clients is in compliance with all the conditions under the consent granted by the Stock 
Exchange. Details of the placing are set out below.
Connected 
client
Connected 
distributor
Relationship with 
the connected 
distributor
Number of 
Offer 
Shares
Ultimate beneficial owner 
of the Offer Shares allocated to 
the connected client
Percentage 
of the Offer 
Shares
Percentage of 
total issued 
Shares of the 
Company
 immediately 
upon 
completion of 
the Global 
Offering
CITIC Securities 
Asset Management 
Company Limited 
(“CITIC Asset 
Management”)
CLSA Limited 
(“CLSA”)
CITIC Asset Management is a 
member of the same group of 
companies as CLSA.
1,300
• 
CITIC Asset Management will 
hold the Offer Shares in its 
capacity as the discretionary fund 
manager managing the funds on 
behalf of their investors, each 
of which is an independent third 
party. 
• 
The funds are as follows:
1. 
CITIC SECURITIES 
COMPANY LIMITED-
XINHANG ZHIYUAN NO.1 
(中信證券信航致遠1號集
合資產管理計劃), of which 
no ultimate beneficial owner 
holds 30% or more interest; 
and
2. 
CITIC SECURITIES 
COMPANY LIMITED-
XINHANG ZHIYUAN NO.3 
(中信證券信航致遠3號集
合資產管理計劃), of which 
no ultimate beneficial owner 
holds 30% or more interest.
0.025%
0.0025%

<<<PAGE 13>>>
– 13 –
Connected 
client
Connected 
distributor
Relationship with 
the connected 
distributor
Number of 
Offer 
Shares
Ultimate beneficial owner 
of the Offer Shares allocated to 
the connected client
Percentage 
of the Offer 
Shares
Percentage of 
total issued 
Shares of the 
Company
 immediately 
upon 
completion of 
the Global 
Offering
JA INVESTMENT 
SPC-JA CHINA 
PLUS HIGH 
INCOME FUND SP 
(“JA Investment 
SPC”)
JA Securities 
Limited (“JA 
Securities”)
JA Investment SPC is managed 
by JD International Investment 
Management Limited, which is 
a member of the same group of 
companies as JA Securities.
381,450
• 
JA Investment SPC will hold the 
Offer Shares in its capacity as 
the discretionary fund manager 
managing the funds on behalf of 
their investors, each of which is 
an independent third party.
• 
Except for Ma Rizhao, no ultimate 
beneficial owner of JA Investment 
SPC holds 30% or more interest.
7.452%
0.7452%
SSIF Asset Management 
SPC-SSI & Affluence 
Capital IPO Strategy 
Opportunity 
Segregated Portfolio 
(“SSIF AM 
Portfolio”)
Shanxi Securities 
International 
Limited (“SSI”)
SSI is Non-syndicate CMI 
member who places securities 
of the Company in relation to 
the Global Offering; SSI and 
Shanxi Securities International 
Asset Management Limited 
(“SSIAM”) are both ultimately 
controlled by Shanxi Securities 
International Financial 
Holdings (“SSIFH”). The 
subscribing investor is SSIF 
AM Portfolio, a segregated 
portfolio managed by SSIF 
Asset Management SPC which 
is controlled by SSIAM.
1,300
• 
SSIF AM Portfolio will hold the 
Offer Shares on a discretionary 
basis, with SSIAM acting as its 
discretionary fund manager on 
behalf of numerous independent 
third-party investors of the 
portfolio.
• 
No ultimate beneficial owner 
holds 30% or more interest in the 
portfolio, and no natural person 
exercises sole control over the 
fund.
0.025%
0.0025%

<<<PAGE 14>>>
– 14 –
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited 
(the “Stock Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) 
take no responsibility for the contents of this announcement, make no representation as to 
its accuracy or completeness and expressly disclaim any liability whatsoever for any loss 
howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in 
or into the United States (including its territories and possessions, any state of the United 
States and the District of Columbia). This announcement does not constitute or form a part 
of any offer or solicitation to purchase or subscribe for securities in the United States. The 
securities mentioned herein have not been, and will not be, registered under the United 
States Securities Act of 1933, as amended (the “U.S. Securities Act”). The securities 
may not be offered or sold in the United States except pursuant to an exemption from the 
registration requirements of the U.S. Securities Act and in compliance with any applicable 
state securities laws, or outside the United States unless in compliance with Regulation S 
under the U.S. Securities Act. There will be no public offer of securities in the United States.
The Offer Shares are being offered and sold outside the United States in offshore 
transactions in reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation 
or offer to acquire, purchase or subscribe for securities. This announcement is not a 
prospectus. Potential investors should read the Prospectus dated June 29, 2026 issued 
by DKE Holding Company Limited for detailed information about the Global Offering 
described below before deciding whether or not to invest in the H Shares thereby being 
offered.
* Potential investors of the Offer Shares should note that the Sponsor-Overall Coordinator 
shall be entitled to terminate the Hong Kong Underwriting Agreement with immediate effect 
upon the occurrence of any of the events set out in the paragraph headed “Underwriting 
– Underwriting Arrangements and Expenses – Hong Kong Public Offering – Grounds for 
Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the 
Listing Date (which is currently expected to be on July 9, 2026).

<<<PAGE 15>>>
– 15 –
PUBLIC FLOAT AND FREE FLOAT
Immediately after completion of the Global Offering, 27,263,326 H Shares, representing 
approximately 53.26% of the issued Shares will be held in the public hands, satisfying the 
minimum percentage requirement under Rule 8.08 and Rule 19A.13A of the Listing Rules.
Immediately following the completion of the Global Offering, at least 10.0% of the total 
number of issued share capital (excluding treasury shares) will be held by the public 
and not be subject to lock-up, with an expected market capitalization of approximately 
HK$402,526,704 at the time of listing, thereby satisfying Rule 19A.13C(1)(a) of the Listing 
Rules at the time of Listing.
The Directors confirm that immediately after the completion of the Global Offering, (i) no 
placee will, individually, be placed more than 10% of the enlarged issued share capital of the 
Company; (ii) there will not be any new substantial shareholder (as defined in the Listing 
Rules) of the Company; (iii) the three largest public shareholders of the Company do not hold 
more than 50% of the H Shares in public hands at the time of the Listing in compliance with 
Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 Shareholders at 
the time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Thursday, 
July 9, 2026 (Hong Kong time), provided that the Global Offering has become unconditional 
and the right of termination described in the section headed “Underwriting – Underwriting 
Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus has not been exercised. Investors who trade the H Shares on the basis of publicly 
available allocation details prior to the receipt of H Share certificates or prior to the H Share 
certificates becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional in all respects at or before 8:00 a.m. 
on Thursday, July 9, 2026, it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. on Thursday, July 9, 2026. The H Shares will be traded in board 
lots of 50 H Shares each. The stock code of the H Shares is 1770.
By order of the Board
DKE Holding Company Limited
Zhou Aijun
Chairman of the Board, Executive Director and
General Manager
Hong Kong, July 8, 2026
As of the date of this announcement, the board of directors of the Company comprises: (i) 
Mr. ZHOU Aijun and Mr. WANG Wenliang as executive directors; (ii) Mr. WANG Xiao, Ms. 
WANG Yang, Mr. LIU Yu, and Mr. DI Chen as non-executive directors; and (iii) Prof. ZENG 
Aimin, Prof. ZHOU Guofu, and Mr. RUAN Tim as independent non-executive directors.
