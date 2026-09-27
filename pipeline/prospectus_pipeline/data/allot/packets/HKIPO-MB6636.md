# 配发结果公告抽取任务：6636.HK Shandong Extreme Vision Technology Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**27/03/2026 21:59**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0327/2026032703232.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6636.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
– 1 –
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock 
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for 
the contents of this announcement, make no representation as to its accuracy or completeness and expressly 
disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement.
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings 
as those defined in the prospectus dated March 20, 2026 (the “Prospectus”) of Shandong Extreme Vision 
Technology Co., Ltd.* (山東極視角科技股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, 
purchase or subscribe for securities. This announcement is not a prospectus. Potential investors should read 
the Prospectus for detailed information about the Global Offering described below before deciding whether 
or not to invest in the Offer Shares. Any investment decision in relation to the Offer Shares should be taken 
solely in reliance on the information provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of Columbia). 
This announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe 
for securities in the United States. The securities mentioned herein have not been, and will not be, registered 
under the United States Securities Act of 1933, as amended (the “U.S. Securities Act”). The securities may 
not be offered or sold in the United States except pursuant to an exemption from the registration requirements 
of the U.S. Securities Act and in compliance with any applicable state securities laws, or outside the United 
States unless in compliance with Regulation S under the U.S. Securities Act. There will be no public offer 
of securities in the United States. The Offer Shares are being offered and sold outside the United States in 
offshore transactions in reliance on Regulation S under the U.S. Securities Act.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to term and conditions set 
out in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong 
Kong and/or not resident in Hong Kong.
Potential investors of the Offer Shares should note that the Sole Sponsor and Overall Coordinator (for itself 
and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the 
Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out 
in the paragraph headed “Underwriting — Hong Kong Underwriting Arrangement — Hong Kong Public 
Offering — Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on 
the Listing Date (which is currently expected to be on Monday, March 30, 2026).

<<<PAGE 2>>>
– 2 –
Shandong Extreme Vision Technology Co., Ltd.*
山東極視角科技股份有限公司
(A joint stock company established in the People’s Republic of China with limited liability)
Global Offering
Number of Offer Shares under the 
Global Offering
:
12,480,000 H Shares
Number of Hong Kong Offer Shares
:
2,496,000 H Shares (as adjusted after 
reallocation)
Number of International Offer Shares
:
9,984,000 H Shares (as adjusted after 
reallocation)
Offer Price
:
HK$40.0 per H Share (payable in full in 
Hong Kong dollars on application plus 
brokerage of 1%, SFC transaction levy 
of 0.0027%, AFRC transaction levy 
of 0.00015% and the Stock Exchange 
trading fee of 0.00565% and subject to 
refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
6636
Sole Sponsor, Overall Coordinator, Sole Global Coordinator, Joint Bookrunner and 
Joint Lead Manager
Joint Bookrunners and Joint Lead Managers
*	
For identification purpose only

<<<PAGE 3>>>
– 3 –
Shandong Extreme Vision Technology Co., Ltd.*
山東極視角科技股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the 
same meanings as those defined in prospectus dated March 20, 2026 (the “Prospectus”) 
of Shandong Extreme Vision Technology Co., Ltd.* (山東極視角科技股份有限公司) (the 
“Company”).
Warning: In view of high concentration of shareholding in a small number of 
Shareholders, Shareholders and prospective investors should be aware that the price 
of the H Shares could move substantially even with a small number of H Shares traded 
and should exercise extreme caution when dealing in the H Shares.
SUMMARY
Company Information
Stock code
6636
Stock short name
EXTREME VISION
Dealings commencement date
March 30, 2026*
*	
see note at the end of the announcement
Price Information
Offer Price
HK$40.00
Offer Shares and Share Capital
Number of Offer Shares
12,480,000
Number of Offer Shares in Hong Kong Public Offering (after 
reallocation)
2,496,000
Number of Offer Shares in International Offering (after 
reallocation)
9,984,000
Number of issued Shares upon Listing
112,914,783
Proceeds
Gross proceeds (Note)
HK$499.2 million
Less: Estimated listing expenses payable based on Offer Price
HK$64.8 million
Net proceeds
HK$434.4 million
Note:	
Gross proceeds refers to the amount which the Company is entitled to receive. For details of the 
use of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the 
Prospectus.

<<<PAGE 4>>>
– 4 –
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING 
No. of valid applications
159,089
No. of successful applications
33,931
Subscription level
4,591.37 times
Claw-back triggered
Yes
No. of Offer Shares initially available under the Hong 
Kong Public Offering
624,000
No. of Offer Shares reallocated from the International 
Offering
1,872,000
Final no. of Offer Shares under the Hong Kong Public 
Offering
2,496,000
% of Offer Shares under the Hong Kong Public 
Offering to the Global Offering
20%
Note:	For details of the final allocation of Shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/iporesult to perform a search by identification number or www.hkeipo.hk/iporesult 
for the full list of allottees.

<<<PAGE 5>>>
– 5 –
INTERNATIONAL OFFERING
No. of placees
128
Subscription Level
3.41 times
No. of Offer Shares initially available under the 
International Offering
11,856,000
No. of Offer Shares reallocated to the Hong Kong 
Public Offering
1,872,000
Final no. of Offer Shares under the International 
Offering
9,984,000
% of Offer Shares under the International Offering to 
the Global Offering
80%
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of the Offer Shares 
subscribed by the placees and the public have been financed directly or indirectly by the Company, any of the 
Directors, chief executive of the Company, substantial shareholders, existing shareholders of the Company or 
any of its subsidiaries or their respective close associates; (ii) none of the placees and the public who have 
purchased the Offer Shares are accustomed to taking instructions from the Company, any of the Directors, 
chief executive of the Company, substantial shareholders, existing shareholders of the Company or any of 
its subsidiaries or their respective close associates in relation to the acquisition, disposal, voting or other 
disposition of Shares registered in his/her/its name or otherwise held by him/her/it; (iii) there is no side 
agreement or arrangement between the Company, any of the Directors, chief executive of the Company, 
substantial shareholders, existing shareholders of the Company or any of its subsidiaries or their respective 
close associates, on one hand, and the public subscribers or the placees who have subscribed for the Offer 
Shares, on the other hand; and (iv) no rebate has been, directly or indirectly, provided by the Company, any 
of the Directors, chief executive of the Company, substantial shareholders or existing shareholders of the 
Company, or any of their subsidiaries or their respective close associates, or syndicate members, or any 
other brokers involved in the Global Offering, to any public investors in the Hong Kong Public Offering or 
placees in the International Offering.

<<<PAGE 6>>>
– 6 –
The placees in the International Offering include the following:
Cornerstone Investors
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares
% of total 
issued H 
Shares after 
the Global 
Offering
% of total 
issued share 
capital after 
the Global 
Offering
Existing 
shareholders 
or their close 
associates
Zhengjin International (Note 1)
1,130,000
9.05%
1.01%
1.00%
Yes
GKI
50,000
0.40%
0.04%
0.04%
No
Note:
1.	
Zhengjin International is a close associate of the existing Shareholders. The Stock Exchange has 
granted a waiver from strict compliance with the requirements under Rules 9.09(b) and 10.04 of and 
consent under Paragraph 1C(2) of Appendix F1 to the Listing Rules and paragraph 18 of Chapter 
4.15 of the Guide for New Listing Applicants to permit H Shares in the International Offering to be 
placed to certain close associates of the existing Shareholders. For further details, see “Waivers and 
Exemption — Waiver from Strict Compliance With Rules 9.09(b) and 10.04 of the Listing Rules and 
Consent Under Paragraph 1C(2) of Appendix F1 to the Listing Rules in Respect of Subscriptions of 
Offer Shares by Close Associate of Existing Shareholders and Core Connected Persons as Cornerstone 
Investor” in the Prospectus and the section headed “Allotment Results Details — International Offering 
— Allotees with waiver/consents obtained” in this announcement.

<<<PAGE 7>>>
– 7 –
Allottees with waiver/consents obtained
Investor
No. of Offer 
Shares 
allocated
% of Offer 
Shares
% of total 
issued H 
Shares after 
the Global 
Offering
% of total 
issued share 
capital after 
the Global 
Offering
Relationship
Allotees with consent under paragraph 1C(1) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) in relation to allocations to connected clients
CITIC Securities International Capital Management 
Limited (“CSI”) (Note 1)
3,000
0.02%
0.003%
0.003%
Connected client as a 
placee
Dol-Fin Select Investment Fund SPC — Dol-Fin Select 
Investment Fund SP (“Dol-Fin Fund”) (Note 1)
1,125,000
9.01%
1.00%
1.00%
Connected client as a 
placee
Allotee with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the Placing Guidelines in relation to 
allocation to a close associate of existing Shareholders
Zhengjin International (Note 2)
1,130,000
9.05%
1.01%
1.00%
A cornerstone investor and 
a close associate of existing 
Shareholders
Notes:
1.	
For details of the consents under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the 
Guide for New Listing Applicant in relation to allocations to connected clients, please refer to the 
section headed “Additional Information” in this announcement. 
2.	
As disclosed in the Prospectus, Guotou Capital Management, Qingdao Qingtie, Qingdao Financial 
and Shandong Luhailiandong are existing Shareholders. Guotou Capital Management and Qingdao 
Qingtie are ultimately controlled by Qingdao City SASAC; Qingdao Financial is ultimately controlled 
by Qingdao Xihaian SASAC; and Shandong Luhailiandong is ultimately controlled by Shandong 
Province SASAC. Qingdao City SASAC, Qingdao Xihaian SASAC and Shandong Province SASAC 
are government bodies of the Shandong Province. Zhengjin International, a cornerstone investor, 
is wholly-owned by JSFIG. JSFIG is wholly-owned by Jinan Shizhong Government Project Fund 
Service Center* (濟南市市中區政府項目資金服務中心), a direct supervisory institution under 
Jinan Shizhong District Finance Bureau* (濟南市市中區財政局), which is a government body of 
the Shandong Province. As Jinan Shizhong District Finance Bureau, Qingdao City SASAC, Qingdao 
Xihaian SASAC and Shandong Province SASAC are government bodies of the Shandong Province, 
Zhengjin International is a close associate of the Company’s abovementioned existing Shareholders 
for the purpose of waiver from strict compliance with Rules 9.09(b) and 10.04 of the Listing Rules 
and consent under paragraph 1C(2) of the Placing Guidelines. On the other hand, given that (a) JSFIG 
is not under direct control or supervision of Qingdao City SASAC, Qingdao Xihaian SASAC and 
Shandong Province SASAC, no approval from Qingdao City SASAC, Qingdao Xihaian SASAC and 
Shandong Province SASAC is required for JSFIG’s investment decisions, and JSFIG and investee 
companies of these authorities are subject to entirely different regulatory reporting lines and approval 
mechanisms in terms of corporate governance and management; (b) JSFIG is under the supervision 
of the Jinan Shizhong District Finance Bureau and is not under the direct control or supervision of 
the Jinan Municipal People’s Government or the Shandong Provincial People’s Government, and is 
therefore independent from the People’s Government of Jinan Municipality, the People’s Government 
of Shandong Province, and the entities under their control; and (c) as advised by the PRC Legal 
Advisors of the Company, relevant laws and regulations do not require JSFIG to obtain any approval 
from the People’s Government of Shandong Province or any of Qingdao City SASAC, Qingdao 
Xihaian SASAC and Shandong Province SASAC in respect of its investment in the Company, Zhengjin 
International should not be treated as a close associate of the abovementioned existing Shareholders 
for the purpose of the qualification as an independent price setting investor.

<<<PAGE 8>>>
– 8 –
LOCK-UP UNDERTAKINGS
Key Persons (as defined under Rule 18C.14 of the Listing Rules)
Name
Number of H 
Shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued H 
Shares in the 
Company upon 
Listing
% of total 
issued 
Shares in the 
Company upon 
Listing
Last day subject 
to the lock-up 
undertakings (Note 1)
Mr. Chan Chan Kit (Note 2)
16,114,821
14.34%
14.27%
March 29, 2027
Ms. Luo Yun (Note 3)
4,405,085
3.92%
3.90%
March 29, 2027
Mr. Chen Shuo (Note 4)
—
—
—
March 29, 2027
Mr. Xu Lei (Note 5)
—
—
—
March 29, 2027
Ms. Liu Ruoshui (Note 6)
—
—
—
March 29, 2027
Hengqin Jili (Note 7)
9,452,122
8.41%
8.37%
March 29, 2027
Hengqin Jichuang (Note 8)
9,024,164
8.03%
7.99%
March 29, 2027
Subtotal
38,996,192
34.70%
34.53%
Notes:
1.	
Pursuant to the applicable PRC law, within the 12 months following the Listing Date, all existing 
Shareholders (including the Pre-IPO Investors) are prohibited from disposing of any of the Shares held 
by them. Pursuant to Rule 18C.14(1) of the Listing Rules, the required lock-up period commences 
on the date by reference to which disclosure of their shareholdings in the Company is made in the 
Prospectus and end on the date upon the expiry of 12 months from the Listing Date, being the same 
date on which the restriction against disposal of Shares under the applicable PRC laws ends.
2.	
Mr. Chan Chan Kit is a member of the Single Largest Group of Shareholders, the chairman of the 
Board, a founder and an executive Director and the general manager of the Company.
3.	
Ms. Luo Yun is a member of the Single Largest Group of Shareholders, a co-founder and an executive 
Director and the deputy general manager of the Company.
4.	
Mr. Chen Shuo is the executive Director and the deputy general manager of the Company.
5.	
Mr. Xu Lei is the chief financial officer, secretary of the Board and joint company secretary of the 
Company.
6.	
Ms. Liu Ruoshui is the deputy general manager and head of operation and marketing centre of the 
Company.
7.	
Hengqin Jili is a member of the Single Largest Group of Shareholders, a close associate of Mr. Chan 
Chan Kit and one of the Pre-IPO Employee Incentive Platforms.
8.	
Hengqin Jichuang is, a close associate of Mr. Xu Lei and one of the Pre-IPO Employee Incentive 
Platforms.

<<<PAGE 9>>>
– 9 –
Pathfinder SIIs
Name
Number of H 
Shares held in 
the Company 
subject to lock-up 
undertakings upon 
Listing
% of total issued 
H Shares in the 
Company upon 
Listing
% of total issued 
Shares in the 
Company upon 
Listing
Last day subject to the 
lock-up undertakings 
(Note 1)
Qingdao Financial
5,464,317
4.86%
4.84%
March 29, 2027
Qualcomm China
4,990,208
4.44%
4.42%
March 29, 2027
China Resources Innovation
4,819,420
4.29%
4.27%
March 29, 2027
Shandong Luhailiandong
4,353,621
3.87%
3.86%
March 29, 2027
Subtotal
19,627,566
17.46%
17.39%
Notes:
1.	
Pursuant to the applicable PRC law, within the 12 months following the Listing Date, all existing 
Shareholders (including the Pre-IPO Investors) are prohibited from disposing of any of the Shares held 
by them. Pursuant to Rule 18C.14(2) of the Listing Rules, the required lock-up period commences on 
the date by reference to which disclosure of their respective shareholdings in the Company is made in 
the Prospectus and ends on the date upon the expiry of six months from the Listing Date i.e. September 
29, 2026.
2.	
Each of the Shareholders listed in the above table is a Pathfinder SII of the Company as defined under 
Chapter 2.5 of the Guide for New Listing Applicants.

<<<PAGE 10>>>
– 10 –
Pre-IPO Investors (as defined in the Prospectus)
Name
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
% of total issued 
H Shares in the 
Company upon 
Listing
% of total issued 
Shares in the 
Company upon 
Listing
Last day subject to the 
lock-up undertakings 
(Note 1)
All Pre-IPO Investors (except for the 
Key Persons and Pathfinder SIIs as 
set out above)
41,811,025 
(including 
41,248,678 H Shares)
36.71%
37.03%
March 29, 2027
Subtotal
41,811,025 
(including 
41,248,678 H 
Shares)
36.71%
37.03%
Notes:
1.	
Please see “History, Development and Corporate Structure — Details of the Pre-IPO Investments” in 
the Prospectus for the identities of the Pre-IPO Investors other than the Key Persons and Pathfinder 
SIIs.
2.	
Pursuant to the applicable PRC law, within the 12 months following the Listing Date, all existing 
Shareholders (including the Pre-IPO Investors) are prohibited from disposing of any of the Shares held 
by them.
Cornerstone Investors
Name
Number of H Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing
% of total issued 
H Shares in the 
Company upon 
Listing
% of total issued 
Shares in the 
Company upon 
Listing
Last day subject to the 
lock-up undertakings 
(Note 1)
Zhengjin International
1,130,000
1.01%
1.00%
December 31, 2026
GKI
50,000
0.04%
0.04%
December 31, 2026
Note:
1.	
Each of the Cornerstone Investors has agreed that it will not, whether directly or indirectly, at any time 
during the period from the Listing Date to December 31, 2026 (both days inclusive) (the “Lock-up 
Period”), dispose of any of the Offer Shares they have subscribed for pursuant to the relevant 
Cornerstone Investment Agreement, save for in certain limited circumstances, such as transfers to 
any of its wholly-owned subsidiaries who will be bound by the same obligations of such Cornerstone 
Investor, including the Lock-up Period restriction.

<<<PAGE 11>>>
– 11 –
PLACEE CONCENTRATION ANALYSIS
Placees
Number of 
H Shares
allotted
Allotment as % of
International Offering
Allotment as % of 
total Offer Shares 
Number
of Shares
held upon
Listing
% of total issued 
share capital 
upon Listing
Top 1
2,150,000
21.53%
17.23%
2,150,000
1.90%
Top 5
6,517,500
65.28%
52.22%
6,517,500
5.77%
Top 10
8,342,500
83.56%
66.85%
8,342,500
7.39%
Top 25
9,602,250
96.18%
76.94%
9,602,250
8.50%
Note:
*	
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHARE SHAREHOLDER CONCENTRATION ANALYSIS
H Shareholders*
Number of 
H Shares 
allotted
Allotment as % of 
International Offering 
Allotment as % of 
total Offer Shares 
Number of 
H Shares 
held upon 
Listing
% of total issued 
H Share capital 
upon Listing 
Number of 
Shares 
held upon 
Listing
Top 1
0
0.00%
0.00%
29,972,028
26.68%
29,972,028
Top 5
1,130,000
11.32%
9.05%
68,477,308
60.95%
68,477,308
Top 10
1,130,000
11.32%
9.05%
90,121,129
80.21%
90,121,129
Top 25
7,267,500
72.79%
58.23%
106,456,898
94.75%
106,456,898
Note:
*	
Ranking of H Shareholders is based on the number of H Shares held by H Shareholders upon Listing.
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders
Number of 
H Shares 
allotted
Allotment as % of 
International Offering 
Allotment as % of 
total Offer Shares 
Number of 
H Shares 
held upon 
Listing
Number of 
Shares 
held upon 
Listing
% of total issued 
share capital 
upon Listing 
Top 1
0
0.00%
0.00%
29,972,028
29,972,028
26.54%
Top 5
1,130,000
11.32%
9.05%
68,477,308
68,477,308
60.65%
Top 10
1,130,000
11.32%
9.05%
90,121,129
90,121,129
79.81%
Top 25
7,267,500
72.79%
58.23%
105,982,844
106,545,191
94.36%
Note:
*	
Ranking of Shareholders is based on the number of Shares (of all classes) held by Shareholders upon 
Listing.

<<<PAGE 12>>>
– 12 –
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications 
made by the public will be conditionally allocated on the basis set out below:
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
allotted of the
total number 
of H Shares 
applied
for
50
51,855
5,186 out of 51,855 applicants to receive 50 H Shares
10.00%
100
9,057
1,039 out of 9,057 applicants to receive 50 H Shares
5.74%
150
20,926
2,600 out of 20,926 applicants to receive 50 H Shares
4.14%
200
5,751
757 out of 5,751 applicants to receive 50 H Shares
3.29%
250
3,679
506 out of 3,679 applicants to receive 50 H Shares
2.75%
300
1,676
239 out of 1,676 applicants to receive 50 H Shares
2.38%
350
1,049
155 out of 1,049 applicants to receive 50 H Shares
2.11%
400
993
150 out of 993 applicants to receive 50 H Shares
1.89%
450
646
100 out of 646 applicants to receive 50 H Shares
1.72%
500
4,500
709 out of 4,500 applicants to receive 50 H Shares
1.58%
600
1,017
167 out of 1,017 applicants to receive 50 H Shares
1.37%
700
921
156 out of 921 applicants to receive 50 H Shares
1.21%
800
905
157 out of 905 applicants to receive 50 H Shares
1.08%
900
742
132 out of 742 applicants to receive 50 H Shares
0.99%
1,000
10,122
1,829 out of 10,122 applicants to receive 50 H Shares
0.90%
1,500
2,092
410 out of 2,092 applicants to receive 50 H Shares
0.65%
2,000
2,995
621 out of 2,995 applicants to receive 50 H Shares
0.52%
2,500
1,976
428 out of 1,976 applicants to receive 50 H Shares
0.43%
3,000
1,262
284 out of 1,262 applicants to receive 50 H Shares
0.38%
3,500
929
215 out of 929 applicants to receive 50 H Shares
0.33%
4,000
800
191 out of 800 applicants to receive 50 H Shares
0.30%
4,500
546
133 out of 546 applicants to receive 50 H Shares
0.27%
5,000
1,891
470 out of 1,891 applicants to receive 50 H Shares
0.25%
6,000
792
204 out of 792 applicants to receive 50 H Shares
0.21%
7,000
805
214 out of 805 applicants to receive 50 H Shares
0.19%
8,000
745
203 out of 745 applicants to receive 50 H Shares
0.17%
9,000
627
175 out of 627 applicants to receive 50 H Shares
0.16%
10,000
4,898
1,395 out of 4,898 applicants to receive 50 H Shares
0.14%
20,000
3,624
1,183 out of 3,624 applicants to receive 50 H Shares
0.08%

<<<PAGE 13>>>
– 13 –
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
allotted of the
total number 
of H Shares 
applied
for
30,000
2,984
1,056 out of 2,984 applicants to receive 50 H Shares
0.06%
40,000
1,611
603 out of 1,611 applicants to receive 50 H Shares
0.05%
50,000
1,539
602 out of 1,539 applicants to receive 50 H Shares
0.04%
60,000
859
349 out of 859 applicants to receive 50 H Shares
0.03%
70,000
651
273 out of 651 applicants to receive 50 H Shares
0.03%
80,000
695
299 out of 695 applicants to receive 50 H Shares
0.03%
90,000
609
268 out of 609 applicants to receive 50 H Shares
0.02%
100,000
3,349
1,502 out of 3,349 applicants to receive 50 H Shares
0.02%
 
Total
150,118
Total number of Pool A successful applicants: 24,960
 
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
total number 
of H Shares 
applied
for
150,000
4,674
100 H Shares plus 1,870 out of 4,674 applicants to 
receive an additional 50 H Shares
0.08%
200,000
1,010
100 H Shares plus 804 out of 1,010 applicants to receive 
an additional 50 H Shares
0.07%
250,000
676
150 H Shares
0.06%
312,000
2,611
150 H Shares plus 1,057 out of 2,611 applicants to 
receive an additional 50 H Shares
0.05%
 
Total
8,971
Total number of Pool B successful applicants: 8,971
 
As of the date of this announcement, the relevant subscription monies previously deposited in the designated 
nominee accounts have been remitted back to the accounts of all HKSCC participants. Investors should 
contact their relevant brokers for any inquiries.

<<<PAGE 14>>>
– 14 –
ADDITIONAL INFORMATION
Placing to connected clients with consents under paragraph 1C(1) of the Placing 
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients of 
certain distributors pursuant to the Placing Guidelines. Details of the placement to connected 
clients are set out below.
Connected client
Connected 
distributor
Relationship
Whether the 
connected client 
will hold beneficial 
interests of Offer 
Shares on a non-
discretionary or 
discretionary basis 
for independent 
third parties
No. of Offer 
Shares 
allocated to 
the connected 
client
% of Offer 
Shares
% of total 
issued share 
capital after 
the Global 
Offering
CSI
CLSA Limited 
(“CLSA”)
See Note 1
Non-discretionary 
basis
3,000
0.02%
0.003%
Dol-Fin Fund
Monmonkey Group 
Securities Limited 
(“MGSL”)
See Note 2
Discretionary basis
1,125,000
9.01%
1.00%
Notes:
1.	
CSI will act as the single counterparty of a back-to-back total return swap transaction (the “CSI 
Back-to-back TRS”) to be entered into by CSI in connection with a total return swap order (the “CSI 
Client TRS”) placed and fully funded by the ultimate clients (the “CSI Ultimate Clients”), including 
Black Crystal Capital Management Co., Ltd.* (黑晶資本管理有限公司) and the investment managers, 
Hainan Evolution Asset Management Co., LTD (海南進化論私募基金管理有限公司) and Shanghai 
QuantPi Investment Limited (上海量派投資管理有限公司)) who act for and on behalf of the CSI 
Ultimate Clients, by which CSI will pass the full economic exposure of the Offer Shares placed to CSI 
to the CSI Ultimate Clients. CSI will hold the legal title and beneficial interest in the Offer Shares but 
will contractually agree to pass on the full economic exposure and return of the Offer Shares to the 
CSI Ultimate Clients, on a non-discretionary basis. The CSI Ultimate Clients may exercise their early 
termination rights to terminate the CSI Client TRS at any time from the trade date of the CSI Client 
TRS which should be on or after the date on which the Offer Shares are listed on the Stock Exchange. 
Upon the final maturity or termination of the CSI Client TRS by the CSI Ultimate Clients, CSI will 
dispose of the Offer Shares on the secondary market and the CSI Ultimate Clients will receive a final 
termination amount of the CSI Back-to-back TRS which will have taken into account all the economic 
returns or economic loss in relation to the Offer Shares and the fixed amount of transaction fees of the 
CSI Back-to-back TRS and the CSI Client TRS. Due to its internal policy, CSI will not exercise the 
voting right of the Offer Shares during the terms of the CSI Back-to-back TRS.

<<<PAGE 15>>>
– 15 –
2.	
Monmonkey Group Asset Management Limited (“MGAML”) is wholly-owned by Apex Goal 
Worldwide Limited, which is in turn wholly-owned by HKE Holdings Limited, which is in turn 
owned by Flourish Nation Enterprises Limited as to 49.75%. Flourish Nation Enterprise Limited is 
wholly-owned by Mr. Lin Ho Man (“Mr. Lin”). MGSL, one of the distributors in the Global Offering, 
is wholly-owned by Monmonkey Group Holdings Limited, which is in turn owned by Mr. Lin as to 
94.0%. Accordingly, MGAML is a related company of MGSL. MGAML is the investment manager 
Dol-Fin Fund SP and is authorized to make investment decisions for its investors to make investment 
decisions on a discretionary basis.
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a 
consent under paragraphs 1C(1) of the Placing Guidelines to permit the Company to allocate 
such Offer Shares in the International Offering to the connected clients listed above. The 
allocation of Offer Shares to such connected clients is in compliance with all the conditions 
under the consent granted by the Stock Exchange.
Placing to an close associate of existing Shareholders with consent under paragraph 
1C(2) of the Placing Guidelines
For details of the allocation of Offer Shares to Zhengjin International, please refer to the 
section headed “Allotment Results Details — International Offering — Allottees with 
waiver/consents obtained” in this announcement. The Company has applied to the Stock 
Exchange, and the Stock Exchange has granted, a waiver from strict compliance with Rules 
9.09(b) and 10.04 of the Listing Rules and consent under paragraph 1C(2) of the Placing 
Guidelines to permit the Company to allocate such Offer Shares in the International Offering 
to Zhengjin International.

<<<PAGE 16>>>
– 16 –
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/
or in respect of which consent has been obtained, the Company has complied with the 
Listing Rules and guidance materials in relation to the placing, allotment and listing of the 
Company’s shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by 
the placees or the public (as the case may be) directly or indirectly for each Offer Share 
subscribed for or purchased by them was the same as the final Offer Price in addition to any 
brokerage, AFRC transaction levy, SFC transaction levy and trading fee payable.
The Directors and the Overall Coordinator confirm that at least 50% of the total number of 
the Offer Shares have been allocated to and taken up by independent price setting investors 
in compliance with Rule 18C.08 of the Listing Rules.
The Directors further confirm that at least 20% of the issued share capital of the Company 
will be held by sophisticated independent investors at the time of Listing in compliance with 
Chapter 2.5 of the Guide for New Listing Applicants.

<<<PAGE 17>>>
– 17 –
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong 
Limited (the “Stock Exchange”) and Hong Kong Securities Clearing Company Limited 
(“HKSCC”) take no responsibility for the contents of this announcement, make no 
representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part 
of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in 
or into the United States (including its territories and possessions, any state of the United 
States and the District of Columbia). This announcement does not constitute or form 
a part of any offer or solicitation to purchase or subscribe for securities in the United 
States. The securities mentioned herein have not been, and will not be, registered under 
the United States Securities Act of 1933, as amended (the “U.S. Securities Act”). The 
securities may not be offered or sold in the United States except pursuant to an exemption 
from the registration requirements of the U.S. Securities Act and in compliance with any 
applicable state securities laws, or outside the United States unless in compliance with 
Regulation S under the U.S. Securities Act. There will be no public offer of securities in 
the United States.
The Offer Shares are being offered and sold outside the United States in offshore 
transactions in reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation 
or offer to acquire, purchase or subscribe for securities. This announcement is not a 
prospectus. Potential investors should read the Prospectus dated March 20, 2026 issued 
by Shandong Extreme Vision Technology Co., Ltd.* (山東極視角科技股份有限公司) for 
detailed information about the Global Offering described herein before deciding whether 
or not to invest in the Shares thereby being offered.
*	
Potential investors of the Offer Shares should note that the Sole Sponsor and Overall Coordinator 
(for itself and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the 
occurrence of any of the events set out in the paragraph headed “Underwriting — Hong Kong 
Underwriting Arrangement — Hong Kong Public Offering — Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently 
expected to be on Monday, March 30, 2026).

<<<PAGE 18>>>
– 18 –
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering, (i) approximately 60.38% 
of the total number of issued Shares will be regarded as public float and the Company 
will satisfy the minimum percentage as prescribed under Rule 19A.13A(1) of the Listing 
Rules; (ii) the three largest public Shareholders do not hold more than 50% of the H Shares 
in public hands at the time of Listing in compliance with Rules 8.08(3) and 8.24 of the 
Listing Rules; (iii) there will not be any new substantial shareholder (as defined in the 
Listing Rules) of the Company immediately after the Global Offering; (iv) no placee will, 
individually, be placed more than 10% of the enlarged issued share capital of the Company 
immediately after the Global Offering; and (v) there will be at least 300 Shareholders at the 
time of Listing in compliance with Rule 8.08(2) of the Listing Rules.
In consideration that the total number of H Shares in issue upon Listing that are held by the 
public and not subject to any disposal restrictions is expected to be at least 10% of the total 
number of issued H Shares at the time of Listing, with an expected market value at the time 
of Listing of not less than HK$50,000,000, the Company is expected to satisfy the free float 
requirement under Rule 19A.13C of the Listing Rules at the time of the Listing.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. (Hong 
Kong time) on Monday, March 30, 2026, provided that the Global Offering has become 
unconditional and the right of termination described in the section headed “Underwriting 
— Hong Kong Underwriting Arrangement — Hong Kong Public Offering — Grounds for 
Termination” in the Prospectus has not been exercised. Investors who trade H Shares prior 
to the receipt of H Share certificates or the H Share certificates becoming valid evidence of 
title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. (Hong 
Kong time) on Monday, March 30, 2026, it is expected that dealings in the H Shares on the 
Stock Exchange will commence at 9:00 a.m. on Monday, March 30, 2026. The H Shares 
will be traded in board lots of 50 H Shares each. The stock code of the Shares is 6636.
By order of the Board
Shandong Extreme Vision Technology Co., Ltd.*
Mr. Chan Chan Kit
Chairman and Executive Director
Hong Kong, March 27, 2026
As at the date of this announcement, the Board comprises (i) Mr. CHAN Chan Kit, Ms. LUO Yun and Mr. 
CHEN Shuo as executive Directors; and (ii) Dr. NIU Baozhuang, Dr. LIU Shijie and Mr. LI Changzhen and 
Mr. CHEUNG Che Kit Richard as independent non-executive Directors.
