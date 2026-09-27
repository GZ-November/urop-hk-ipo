# 配发结果公告抽取任务：1511.HK UISEE Technologies (Beijing) Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**19/05/2026 21:52**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0519/2026051901257.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"1511.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as 
those defined in the prospectus dated May 12, 2026 (the “Prospectus”) issued by UISEE Technologies (Beijing) 
Co., Ltd. (馭勢科技（北京）股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an offer or an invitation to induce 
an offer by any person to acquire, purchase or subscribe for any securities of the Company. This announcement is 
not a prospectus. Potential investors should read the Prospectus for detailed information about the Company and 
the Global Offering described below before deciding whether or not to invest in the Offer Shares. Any investment 
decision in relation to the Offer Shares should be taken solely in reliance on the information provided in the 
Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not, and is not intended to, constitute or form a part of any offer to sell or solicitation to 
purchase or subscribe for any securities in the United States or in any other jurisdiction. The Offer Shares have 
not been, and will not be, registered under the United States Securities Act of 1933, as amended from time to 
time (the “U.S. Securities Act”) or securities law of any state or other jurisdiction of the United States and may 
not be offered, sold, pledged or otherwise transferred within the United States, except pursuant to an available 
exemption from, or in a transaction not subject to, the registration requirements of the U.S. Securities Act and 
in compliance with any applicable state securities laws. The Offer Shares are being offered and sold solely 
outside the United States in offshore transactions in reliance on Regulation S under the U.S. Securities Act and 
applicable laws of each jurisdiction where those offers and sales occur. There will be no public offer of the Offer 
Shares in the United States.
In connection with the Global Offering, CITIC Securities (Hong Kong) Limited acts as the Sole Sponsor, CLSA 
Limited acts as the Sponsor-Overall Coordinator and CLSA Limited, BOCOM International Securities Limited, 
DBS Asia Capital Limited and China Galaxy International Securities (Hong Kong) Co., Limited act as Overall 
Coordinators.
Potential investors of the Offer Shares should note that the Sole Sponsor and the Sponsor-Overall Coordinator 
(for itself and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under 
the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out 
in the section headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong Underwriting 
Agreement – Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the 
Listing Date (which is currently expected to be on Wednesday, May 20, 2026).

<<<PAGE 2>>>
– 2 –
UISEE Technologies (Beijing) Co., Ltd.
馭勢科技（北京）股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the
Global Offering
:
14,461,200 H Shares
Number of Hong Kong Offer Shares
:
2,892,250 H Shares (as adjusted after 
reallocation)
Number of International Offer Shares
:
11,568,950 H Shares (as adjusted after 
reallocation)
Offer Price
:
HK$60.30 per H Share, plus brokerage 
of 1.0%, SFC transaction levy of 
0.0027%, Stock Exchange trading fee 
of 0.00565% and AFRC transaction 
levy of 0.00015% (payable in full on 
application in Hong Kong Dollars and 
subject to refund)
Nominal value
: RMB0.10 per H Share
Stock code
:
1511
Sole Sponsor, Overall Coordinator, Joint Global Coordinator, 
Joint Bookrunner and Joint Lead Manager
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3 
 
UISEE Technologies (Beijing) Co., Ltd.   
馭勢科技（北京）股份有限公司 
ANNOUNCEMENT OF ALLOTMENT RESULTS 
 
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as 
those defined in the prospectus dated May 12, 2026 (the “Prospectus”) issued by UISEE Technologies (Beijing) 
Co., Ltd. (馭勢科技（北京）股份有限公司) (the “Company”).  
 
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares could move 
substantially even with a small number of H Shares traded and should exercise extreme caution when 
dealing in the H Shares. 
SUMMARY  
 
Company information 
Stock code  
1511 
Stock short name  
UISEE TECH 
Dealings commencement date  
May 20, 2026* 
*see note at the end of the announcement  
 
Price Information  
Offer Price  
HK$60.30 
 
 
Offer Shares and Share Capital 
Number of Offer Shares  
14,461,200 H Shares 
Number of Offer Shares in Hong Kong Public Offering (as 
adjusted after reallocation) 
2,892,250 H Shares 
Number of Offer Shares in International Offering (as 
adjusted after reallocation) 
11,568,950 H Shares 
Number of issued Shares upon Listing  
162,485,020 Shares 
 
Note: The Offer Size Adjustment Option is not exercised. 
 
Proceeds  
Gross proceeds (Note)  
HK$872.0 million 
Less: Estimated listing expenses payable based on the 
Offer Price  
HK$76.6 million 
Net proceeds  
HK$795.4 million 
 
Note: Gross proceeds refer to the amount to which the issuer is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.  
 
 
 
 
 
 

<<<PAGE 4>>>
4 
 
 
ALLOTMENT RESULTS DETAILS 
 
HONG KONG PUBLIC OFFERING 
 
No. of valid applications  
285,972 
No. of successful applications  
48,689 
Subscription level  
6,777.29 times 
Claw-back triggered 
Yes 
No. of Offer Shares initially available under the Hong Kong Public 
Offering  
723,100 
No. of Offer Shares reallocated from the International Offering 
(claw-back) 
2,169,150 
Final no. of Offer Shares under the Hong Kong Public Offering 
(after reallocation) 
2,892,250 
% of final no. of Offer Shares under the Hong Kong Public 
Offering to the Global Offering 
20% 
 
Note: For details of the final allocation of Shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/iporesult to perform a search by identification number or www.hkeipo.hk/iporesult for the 
full list of allottees. 
INTERNATIONAL OFFERING 
 
No. of placees  
87 
Subscription level  
5.66 times  
No. of Offer Shares initially available under the International 
Offering 
13,738,100 
No. of Offer Shares reallocated to the Hong Kong Public Offering 
(claw-back) 
2,169,150 
Final no. of Offer Shares under the International Offering (after 
reallocation) 
11,568,950 
% of final no. of Offer Shares under the International Offering to 
the Global Offering 
80% 
 
The Directors confirm that, to the best of their knowledge, information and belief, save for waivers from 
strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 1C of Appendix F1 to 
the Listing Rules (the “Placing Guidelines”) granted by the Stock Exchange to permit H Shares in the 
International Offering to be placed to certain Existing Minority  Shareholders and/or their close associates, 
(i) none of the Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive of the Company, Controlling Shareholders, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective close 
associates; (ii) none of the placees and the public who have purchased the Offer Shares are accustomed to 
taking instructions from the Company, any of the Directors, chief executive of the Company, Controlling 
Shareholders, substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries or 
their respective close associates in relation to the acquisition, disposal, voting or other disposition of Shares 
registered in his/her/its name or otherwise held by him/her/it; (iii) there is no side agreement or arrangement 
between the Company, any of the Directors, chief executive of the Company, the Controlling Shareholders, 
substantial shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective 

<<<PAGE 5>>>
5 
 
close associates, on one hand, and the public subscribers or the placees who have subscribed for the Offer 
Shares, on the other hand; and (iv) no rebate has been, directly or indirectly, provided by the Company, any 
of the Directors, chief executive of the Company, the Controlling Shareholders, substantial Shareholders, 
existing Shareholders of the Company or any of its subsidiaries or their respective close associates, or 
syndicate members, or any other brokers involved in the Global Offering, to any public investors in the Hong 
Kong Public Offering or placees in the International Offering. 
The placees in the International Offering include the following: 
Cornerstone Investors 
 
 
Investor Note 1 
No. of Offer 
Shares 
allocated 
% of 
Offer 
Shares 
 
% of total 
issued H 
Shares after 
the Global 
Offering 
% of total 
issued Shares 
after the 
Global 
Offering 
 
Existing 
shareholders or 
their close 
associates 
Xiongan Autonomous 
Driving Limited (雄安自
動駕駛有限公司) 
(“Xiongan Auto 
Driving”) 
3,710,000 H 
Shares 
25.65% 
2.93% 
2.28% 
No 
CYGG Holding Limited 
(“CYGG”) 
129,700 H 
Shares 
0.90% 
0.10% 
0.08% 
No 
Starwin International A 
LPF (“Starwin 
International”) 
492,500 H 
Shares 
3.41% 
0.39% 
0.30% 
No 
Total 
4,332,200 H 
Shares 
29.96% 
3.42% 
2.67% 
 
Notes: 
 
1. For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone 
Investors” in the Prospectus. 
 
Allottees with Waivers/Consents Obtained 
 
Investor 
No. of Offer 
Shares allocated 
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
Allotees with consents under paragraph 1C of the Placing Guidelines and Chapter 4.15 of the Guide for 
New Listing Applicants in relation to allocations to connected clients  
Starwin International 
Note 1 
492,500 H Shares 
3.41% 
0.39% 
0.30% 
Connected client 
and a cornerstone 
investor 

<<<PAGE 6>>>
6 
 
Investor 
No. of Offer 
Shares allocated 
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
New Harvest Wealth 
Securities Company 
Limited (“New 
Harvest”) Note 2 
829,150 H Shares 
5.73% 
0.65% 
0.51% 
Connected client 
and a placee 
Allotees with waivers from strict compliance with Rule 10.04 of the Listing Rules and Chapters 2.5 and 4.15 
of the Guide for New Listing Applicants and consents under paragraphs 1C(1) and 1C(2) of the Placing 
Guidelines in relation to allocations to connected clients and close associates of existing Shareholder 
CITIC Securities 
International Capital 
Management Limited 
(“CSI”) Note 2 
31,350 H Shares 
0.22% 
0.02% 
0.019% 
Connected client 
and a close 
associate of 
existing 
Shareholders as a 
placee 
CITIC Securities 
Asset Management 
(HK) Limited 
(“CITIC AM HK”) 
Note 2 
1,700 H Shares 
0.01% 
0.001% 
0.001% 
Connected client 
and a close 
associate of 
existing 
Shareholders as a 
placee 
CITIC Securities 
Asset Management 
Company Limited 
(“CITIC AM”) Note 2 
1,700 H Shares 
0.01% 
0.001% 
0.001% 
Connected client 
and a close 
associate of 
existing 
Shareholders as a 
placee 
Notes: 
  
1. See “Waivers from Strict Compliance with the Listing Rules — Consent in respect of Proposed 
Subscription of Shares by Certain Cornerstone Investor who is a Connected Client” of the Prospectus 
and the section headed “Others / Additional Information — Placing to Connected Clients (including 
those who are close associate of existing Shareholder) with Prior Consents under Paragraphs 1C(1) 
and 1C(2) of the Placing Guidelines and waivers from the strict compliance with Rule 10.04 of the 
Listing Rules (as applicable)” in this announcement for further details. 
 
2. See the section headed “Others / Additional Information — Placing to Connected Clients (including 
those who are close associate of existing Shareholder) with Prior Consents under Paragraphs 1C(1) 
and 1C(2) of the Placing Guidelines and waivers from the strict compliance with Rule 10.04 of the 
Listing Rules (as applicable)” in this announcement for further details. 
 
LOCK-UP UNDERTAKINGS 
Controlling Shareholders 
 

<<<PAGE 7>>>
7 
 
Name 
Number of Shares 
held in the 
Company subject to 
lock-up 
undertakings upon 
Listing 
% of total issued 
H Shares after 
the Global 
Offering subject 
to lock-up 
undertakings 
upon Listing 
% of shareholding 
in the Company 
subject to lock-up 
undertakings 
upon Listing 
Last day subject 
to the lock-up 
undertakings Note 1   
Wu Gansha (吳甘沙) 
(“Mr. Wu”) Note 2 
24,341,740 Shares 
(including 8,113,910 
H Shares) 
6.40% 
14.98% 
May 19, 2027 
Jiang Yan (姜岩) (“Mr. 
Jiang”) Note 2 
7,055,560 H Shares 
5.57% 
4.34% 
May 19, 2027 
Zhou Xin (周鑫) (“Mr. 
Zhou”) Note 2 
3,527,780 Shares 
(including 1,000,000 
H Shares) 
0.79% 
2.17% 
May 19, 2027 
Peng Jinzhan (彭進展) 
(“Mr. Peng”) Note 2 
3,527,780 Shares 
(including 1,000,000 
H Shares) 
0.79% 
2.17% 
May 19, 2027 
Beijing Simaju 
Technology Center 
(Limited Partnership) 
(北京司馬駒科技中心
（有限合夥）) 
(“Beijing Simaju”) Note 2 
14,111,120 H Shares 
11.14% 
8.68% 
May 19, 2027 
Subtotal 
52,563,980 Shares 
(including 
31,280,590 H Shares) 
24.68% 
32.35% 
 
Notes: 
 
1. Pursuant to the applicable PRC laws, all existing Shareholders (including the Controlling 
Shareholders) are not permitted to dispose of any of the Shares held by them within 12 months following 
the Listing Date. 
 
2. On December 17, 2019, Mr. Wu, Mr. Jiang, Mr. Zhou, Mr. Peng and Mr. Zhao Yong (趙勇) (“Mr. 
Zhao”) entered into an acting-in-concert agreement, pursuant to which each of Mr. Jiang, Mr. Zhou, 
Mr. Peng and Mr. Zhao agreed that, so long as he directly or indirectly holds any equity interest in the 
Company, he shall exercise his voting rights in a consistent manner with Mr. Wu. The agreement shall 
remain in effect until its termination upon mutual consent among the parties, save that for Mr. Zhao, 
his obligation ceased when Beijing Deep Glint Technology Co., Ltd. (北京格靈深瞳信息技術股份有
限公司) ("Deep Glint") submitted its application for listing on the STAR Market of the Shanghai Stock 
Exchange on June 22, 2021. The cessation of Mr. Zhao as a party to the agreement was taken into 
account that Deep Glint, the primary business interest of Mr. Zhao, was anticipated to be listed on the 
STAR Market soon, and Mr. Zhao, as a chairman and director of Deep Glint, considered that it would 
be in the best interest of Deep Glint that his voting interest in the Company became aligned with that 
of Deep Glint without the restrictions under the agreement. 
 
Beijing Simaju is the designated shareholding platform for the Pre-IPO Incentive Schemes, of which 
Mr. Wu (its general partner) holds 61.47% partnership interest and Mr. Zhou (its limited partner) 
holds 20% partnership interest for the benefit of the option grantees under the Pre-IPO Incentive 
Schemes. The remaining 18.53% partnership interest in Beijing Simaju is beneficially held by Mr. Wu. 
 

<<<PAGE 8>>>
8 
 
Therefore, Mr. Wu, Mr. Jiang, Mr. Zhou, Mr. Peng and Beijing Simaju constitute a group of 
Controlling Shareholders of the Company under the Listing Rules. 
 
 
Key Persons (as defined under Rule 18C.14 of the Listing Rules) 
 
Name 
 
 
 
 
 
 
Capacity 
Number of Shares 
held in the 
Company subject 
to lock-up 
undertakings 
upon Listing 
% of total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing 
% of shareholding 
in the Company 
subject to lock-up 
undertakings 
upon Listing 
 
Last day 
subject to the 
lock-up 
undertakings 
Note 1 
Mr. Zhao 
Co-founder of 
the Group 
2,116,680 H 
Shares 
1.67% 
1.30% 
May 19, 2027 
Chiang 
Tsung Che 
(江宗哲) 
(“Mr. 
Chiang”) Note 
2 
Executive 
Director, chief 
financial officer, 
Board secretary 
and joint 
company 
secretary of the 
Group 
– 
– 
– 
May 19, 2027 
Wu Jun (吳
軍) Note 2 
Non-executive 
Director and 
former 
consultant of the 
Group 
– 
– 
– 
May 19, 2027 
Liu Yang (劉
洋) Note 2 
Core R&D Team 
member 
– 
– 
– 
May 19, 2027 
Zhou 
Xiaocheng 
(周小成) Note 
2 
Core R&D Team 
member 
– 
– 
– 
May 19, 2027 
Zhang Dan 
(張丹) Note 2 
Core R&D Team 
member 
– 
– 
– 
May 19, 2027 
Subtotal 
 
2,116,680 H 
Shares 
1.67% 
1.30% 
 
Notes: 
 
1. Pursuant to the applicable PRC laws, all existing Shareholders are not permitted to dispose of any 
of the Shares held by them within 12 months following the Listing Date. In accordance with Rule 
18C.14(1) of the Listing Rules, the required lock-up period for key persons commences on the date 
by reference to which disclosure of its shareholding is made in the Prospectus and end on the date 
which is 12 months from the Listing Date, i.e. May 19, 2027, being the same date on which the 
restriction against disposal of Shares under the applicable PRC laws ends. 
 
2. Certain options to acquire Incentive Units (i.e. partnership interests held by Mr. Wu and Mr. Zhou in 
Beijing Simaju) have been granted to the following persons under the Pre-IPO Incentive Schemes, 
namely (i) Mr. Chiang and Mr. Wu Jun, our Directors; and (ii) Mr. Liu Yang, Dr. Zhou Xiaocheng 
and Dr. Zhang Dan, our Core R&D Team members, who are key persons as defined under Rule 

<<<PAGE 9>>>
9 
 
18C.14 of the Listing Rules. Therefore, they have undertaken that they will not dispose of their 
interests in the options granted to them as well as the partnership interests in Beijing Simaju to be 
transferred to them upon the exercise of their vested options under Rule 18C.14 of the Listing Rules 
within the lock-up period referred to in note 1 above. 
 
Pursuant to the partnership agreement of Beijing Simaju, any transfer of partnership interest by 
limited partners shall be approved by Mr. Wu, as the general partner and the majority holder of the 
partnership interest. Mr. Wu will ensure that the lock-up restriction will be effectively enforced in 
respect of the indirect interests held by the aforementioned persons as limited partners.  
 
See the sections headed “History, Development and Corporate Structure — Pre-IPO Incentive 
Schemes” and “Appendix VI — Statutory and General Information — D. Pre-IPO Incentive 
Schemes” for further details. 
 
 
 
Pathfinder SIIs 
 
Name Note 1 
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing 
% of total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing 
% of 
shareholding in 
the Company 
subject to lock-up 
undertakings 
upon Listing 
 
Last day subject to the 
lock-up undertakings 
Note 2 
Shaanxi Xike Angel 
Phase III Commercial 
Consultancy 
Partnership (Limited 
Partnership) (陝西西科
天使叁期商務信息諮
詢合夥企業（有限合
夥）) 
5,110,390 H Shares 
4.03% 
3.15% 
May 19, 2027 
Beijing Phase II CAS 
Star Hard Technology 
Venture Capital 
Partnership (Limited 
Partnership) (北京二期
中科創星硬科技創業
投資合夥企業(有限合
夥）) 
1,950,370 H Shares 
 
1.54% 
1.20% 
May 19, 2027 
Shaanxi Big Data 
Industry Investment 
Fund Partnership 
(Limited Partnership) 
(陝西大數據產業投資
基金合夥企業（有限合
夥）) 
1,729,310 Shares 
- 
1.06% 
May 19, 2027 
Shanghai State-owned 
Enterprise Reform and 
Development Equity 
Investment Fund 
Partnership (Limited 
3,249,840 Shares 
- 
2.00% 
May 19, 2027 

<<<PAGE 10>>>
10 
 
Name Note 1 
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing 
% of total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing 
% of 
shareholding in 
the Company 
subject to lock-up 
undertakings 
upon Listing 
 
Last day subject to the 
lock-up undertakings 
Note 2 
Partnership) (上海國企
改革發展股權投資基
金合夥企業（有限合
夥）) 
Taizhou Shengsheng 
Equity Investment 
Partnership (Limited 
Partnership) (台州盛升
股權投資合夥企業(有
限合夥）) 
2,015,460 Shares 
- 
1.24% 
May 19, 2027 
Shenzhen Capital 
Group Co., Ltd. (深圳
市創新投資集團有限
公司) 
1,950,380 Shares 
- 
1.20% 
May 19, 2027 
Tianjin Haihe Hongtu 
Investment Fund 
Partnership (Limited 
Partnership) (天津海河
紅土投資基金合夥企
業（有限合夥）) 
1,170,230 H Shares 
0.92% 
0.72% 
May 19, 2027 
Shanghai Jinshan 
Hongtu Venture 
Capital Investment 
Center (Limited 
Partnership) (上海金山
紅土創業投資中心
（有限合夥）) 
390,070 H Shares 
0.31% 
0.24% 
May 19, 2027 
Liyang Hongtu New 
Economy Venture 
Capital Fund 
Partnership (Limited 
Partnership) (溧陽紅土
新經濟創業投資基金
合夥企業（有限合
夥）) 
390,070 H Shares 
0.31% 
0.24% 
May 19, 2027 
Changzhou Hongtu 
Human Resources 
Investment Partnership 
(Limited Partnership) 
(常州紅土人才投資合
夥企業（有限合夥）) 
195,040 H Shares 
0.15% 
0.12% 
May 19, 2027 
Nanjing CICC Qihong 
Investment Fund 
Partnership (Limited 
Partnership) (南京中金
4,314,230 H Shares 
3.40% 
2.66% 
May 19, 2027 

<<<PAGE 11>>>
11 
 
Name Note 1 
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing 
% of total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing 
% of 
shareholding in 
the Company 
subject to lock-up 
undertakings 
upon Listing 
 
Last day subject to the 
lock-up undertakings 
Note 2 
啟泓投資基金合夥企
業（有限合夥）) 
Subtotal 
22,465,390 Shares 
(including 
13,520,400 H 
Shares) 
10.67% 
13.83% 
 
Notes: 
 
1. Each of the Shareholders listed in the above table is a Pathfinder SII of the Company as defined under 
Chapter 2.5 of the Guide for New Listing Applicants. 
 
2. In accordance with Rule 18C.14(2) of the Listing Rules, the required lock-up period commences on 
the date by reference to which disclosure of its shareholding is made in the Prospectus and ends on 
the date which is six months from the Listing Date, i.e. November 19, 2026. In addition to the lock-
up requirement under Rule 18C.14(2) of the Listing Rules, all existing Shareholders are not permitted 
to dispose of any of the Shares held by them within 12 months following the Listing Date, i.e. ending 
on May 19, 2027, as required under the applicable PRC laws.  
 
Pre-IPO Investors other than Pathfinder SIIs (as defined in the Prospectus)  
 
 
 
 
 
Name 
Number of Shares 
held in the 
Company subject 
to lock-up 
undertakings 
upon Listing 
% of total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing 
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing 
 
Last day subject to 
the lock-up 
undertakings Note 1  
Zhuhai GF Yunyi 
Smart Car Industry 
Fund (Limited 
Partnership) (珠海廣
發雲意智能汽車產業
基金（有限合夥）) 
2,305,740 H Shares 
1.82% 
1.42% 
May 19, 2027 
Zhuhai GF Xinde 
Environment 
Protection Industry 
Investment Fund 
Partnership (Limited 
Partnership) (珠海廣
發信德環保產業投資
基金合夥企業（有限
合夥）) 
1,083,700 H 
Shares 
0.86% 
0.67% 
May 19, 2027 

<<<PAGE 12>>>
12 
 
 
 
 
 
Name 
Number of Shares 
held in the 
Company subject 
to lock-up 
undertakings 
upon Listing 
% of total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing 
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing 
 
Last day subject to 
the lock-up 
undertakings Note 1  
CDBC Manufacturing 
Transformation and 
Upgrading Fund 
(Limited Partnership) 
(國開製造業轉型升
級基金（有限合
夥）) 
3,120,600 Shares 
- 
1.92% 
May 19, 2027 
Hubei High Quality 
Development Industry 
Investment Fund 
Partnership (Limited 
Partnership) (湖北高
質量發展產業投資基
金合夥企業（有限合
夥）) 
2,690,870 H 
Shares 
2.12% 
1.66% 
May 19, 2027 
Bosch (Shanghai) 
Venture Capital 
Investment Co., Ltd. 
(博世（上海）創業
投資有限公司) 
2,590,020 H 
Shares 
2.04% 
1.59% 
May 19, 2027 
Xinzhifeng (Wuhan) 
Equity Investment 
Fund Partnership 
(Limited Partnership) 
(信之風（武漢）股
權投資基金合夥企業
（有限合夥）) 
2,027,720 H 
Shares 
1.60% 
1.25% 
May 19, 2027 
CITIC Securities 
Investment Co., Ltd. 
(中信証券投資有限
公司) 
1,345,430 H 
Shares 
1.06% 
0.83% 
May 19, 2027 
Century Gateway 
Investment Limited 
5,742,770 H 
Shares 
4.53% 
3.53% 
May 19, 2027 
Ningbo Lanting 
Shiling Investment 
Partnership (Limited 
Partnership) (寧波瀾
亭視聆投資合夥企業
（有限合夥）) 
5,187,920 H 
Shares 
4.09% 
3.19% 
May 19, 2027 

<<<PAGE 13>>>
13 
 
 
 
 
 
Name 
Number of Shares 
held in the 
Company subject 
to lock-up 
undertakings 
upon Listing 
% of total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing 
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing 
 
Last day subject to 
the lock-up 
undertakings Note 1  
Sinovation Fund III, 
L.P. 
5,065,700 H 
Shares 
4.00% 
3.12% 
May 19, 2027 
Chongqing Science 
City Investment 
Holding Co., Ltd. (重
慶科學城投資控股有
限公司) 
4,055,450 H 
Shares 
3.20% 
2.50% 
May 19, 2027 
Gongqingcheng 
Xinding Huaqi No. 1 
Equity Investment 
Partnership (Limited 
Partnership) (共青城
新鼎華麒壹號股權投
資合夥企業（有限合
夥）) 
3,740,040 H 
Shares 
2.95% 
2.30% 
May 19, 2027 
Beijing Z-Park 
Longmen Fund 
Investment Center 
(Limited Partnership) 
(北京中關村龍門基
金投資中心（有限合
夥）) 
1,950,370 H 
Shares 
1.54% 
1.20% 
May 19, 2027 
Ningbo Meishan 
Bonded Logistics 
Park Tengyun 
Yuansheng Equity 
Investment 
Partnership (Limited 
Partnership) (寧波梅
山保稅港區騰雲源晟
股權投資合夥企業
（有限合夥）) 
1,950,370 H 
Shares 
1.54% 
1.20% 
May 19, 2027 
Beijing Smart Cloud 
City Investment Fund 
Center (Limited 
Partnership) (北京智
慧雲城投資基金中心
（有限合夥）) 
1,949,910 H 
Shares 
1.54% 
1.20% 
May 19, 2027 
CAS-Tech Fund I L.P. 
1,824,170 H 
Shares 
1.44% 
1.12% 
May 19, 2027 

<<<PAGE 14>>>
14 
 
 
 
 
 
Name 
Number of Shares 
held in the 
Company subject 
to lock-up 
undertakings 
upon Listing 
% of total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing 
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing 
 
Last day subject to 
the lock-up 
undertakings Note 1  
Jiaxing Jiayao 
Venture Capital 
Partnership (Limited 
Partnership) (嘉興嘉
耀創業投資合夥企業
（有限合夥）) 
1,820,200 H 
Shares 
1.44% 
1.12% 
May 19, 2027 
Zhen Partners IV 
(HK) Limited 
1,383,450 H 
Shares 
1.09% 
0.85% 
May 19, 2027 
Yusheng Future 
(Zhuhai) Equity 
Investment 
Partnership (Limited 
Partnership) (馭勝未
來（珠海）股權投資
合夥企業（有限合
夥）) 
1,345,430 H 
Shares 
1.06% 
0.83% 
May 19, 2027 
Xiangjiang Industrial 
Investment Co., Ltd. 
(湘江產業投資有限
責任公司) 
1,299,940 H 
Shares 
1.03% 
0.80% 
May 19, 2027 
Jiangsu Zhongde 
Services Trade 
Industry Investment 
Fund (Limited 
Partnership) (江蘇中
德服貿產業投資基金
（有限合夥）) 
1,170,230 Shares 
- 
0.72% 
May 19, 2027 
Beijing Yintai Jiahe 
Venture Capital 
Investment Co., Ltd. 
(北京銀泰嘉禾創業
投資有限公司) 
1,152,870 Shares 
- 
0.71% 
May 19, 2027 
Suzhou Hengtong 
Datai Big Data 
Industry Fund 
Partnership (Limited 
Partnership) (蘇州亨
通達泰大數據產業基
金合夥企業（有限合
夥）) 
897,170 H Shares 
0.71% 
0.55% 
May 19, 2027 

<<<PAGE 15>>>
15 
 
 
 
 
 
Name 
Number of Shares 
held in the 
Company subject 
to lock-up 
undertakings 
upon Listing 
% of total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing 
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing 
 
Last day subject to 
the lock-up 
undertakings Note 1  
Henan Keyuan 
Shenneng Clean 
Energy Equity 
Investment Fund 
Partnership (Limited 
Partnership) (河南科
源申能潔淨能源股權
投資基金合夥企業
（有限合夥）) 
780,150 H Shares 
0.62% 
0.48% 
May 19, 2027 
Xiamen Oak Forest 
Energy Saving and 
Environmental 
Protection Venture 
Capital Fund 
Partnership (Limited 
Partnership) (廈門橡
樹林節能環保創投基
金合夥企業（有限合
夥）) 
780,150 H Shares 
0.62% 
0.48% 
May 19, 2027 
Chongqing Liangjiang 
New Area Innovative 
Service Industry 
Equity Investment 
Fund Partnership 
(Limited Partnership) 
(重慶兩江新區戰新
服務業股權投資基金
合夥企業（有限合
夥）) 
780,150 H Shares 
0.62% 
0.48% 
May 19, 2027 
Xiamen Datai Core 
Stone Venture Capital 
Partnership (Limited 
Partnership) (廈門達
泰芯石創業投資合夥
企業（有限合夥）) 
390,080 H Shares 
0.31% 
0.24% 
May 19, 2027 
Beijing Qingshan 
Enterprise Angel 
Investment 
Partnership (北京青
山基業天使投資合夥
企業（有限合夥）) 
350,030 H Shares 
0.28% 
0.22% 
May 19, 2027 

<<<PAGE 16>>>
16 
 
 
 
 
 
Name 
Number of Shares 
held in the 
Company subject 
to lock-up 
undertakings 
upon Listing 
% of total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing 
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing 
 
Last day subject to 
the lock-up 
undertakings Note 1  
Wang Yanmin (王彥
敏) 
262,540 H Shares 
0.21% 
0.16% 
May 19, 2027 
Chen Xuetao (陳雪
濤) 
87,490 Shares 
- 
0.05% 
May 19, 2027 
Zhuhai Kangyuan 
Investment Enterprise 
(Limited Partnership) 
(珠海康遠投資企業
（有限合夥）) 
69,180 H Shares 
0.05% 
0.04% 
May 19, 2027 
Subtotal 
59,199,840 
Shares 
(including 
53,668,650 H 
Shares) 
42.35% 
36.43% 
 
Notes:  
  
1. Pursuant to the applicable PRC laws, all existing Shareholders (including the Pre-IPO Investors) are 
not permitted to dispose of any of the Shares held by them within 12 months following the Listing 
Date. 
 
Existing Shareholders (excluding the Controlling Shareholders, Key Persons and Pre-IPO Investors) 
 
 
 
 
 
 
 
 
 
Name 
 
 
 
Number of 
Shares held in 
the Company 
subject to lock-up 
undertakings 
upon Listing 
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing 
% of shareholding 
in the Company 
subject to lock-up 
undertakings 
upon Listing 
 
Last day subject to 
the lock-up 
undertakings Note 1   
Deep Glint 
11,677,930 H 
Shares 
9.22% 
7.19% 
May 19, 2027 
Total 
11,677,930 H 
Shares 
9.22% 
7.19% 
 
Notes:  
  
1. Pursuant to the applicable PRC laws, all existing Shareholders are not permitted to dispose of any of 
the Shares held by them within 12 months following the Listing Date. 

<<<PAGE 17>>>
17 
 
 
Cornerstone Investors 
 
Name 
Number of Shares 
held in the 
Company subject to 
lock-up 
undertakings upon 
listing 
% of total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing 
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing 
Last day subject to 
the lock-up 
undertakings Note 1   
Xiongan Auto Driving 3,710,000 H Shares 
2.93% 
2.28% 
November 19, 2026 
CYGG 
129,700 H Shares 
0.10% 
0.08% 
November 19, 2026 
Starwin International 
492,500 H Shares 
0.39% 
0.30% 
November 19, 2026 
Total 
4,332,200 Shares 
(including 
4,332,200 H 
Shares) 
3.42% 
2.67% 
 
Notes:  
  
1. In accordance with the relevant cornerstone investment agreements, the required lock-up ends on 
November 19, 2026. The Cornerstone Investors will cease to be prohibited from disposing of or 
transferring H Shares subscribed for pursuant to the relevant cornerstone investment agreements 
after the indicated date. 

<<<PAGE 18>>>
18 
 
PLACEE CONCENTRATION ANALYSIS 
 
Placees Note 1 
Number of H 
Shares allotted 
Allotment as % of 
International Offering   
Allotment as % of total 
Offer Shares 
Number of 
Shares held upon Listing 
% of total issued share 
capital upon Listing  
Top 1 
3,710,000 
32.07% 
25.65% 
3,710,000 
2.28% 
Top 5 
7,905,850 
68.34% 
54.67% 
7,905,850 
4.87% 
Top 10 
9,384,850 
81.12% 
64.90% 
9,384,850 
5.78% 
Top 25 
11,070,500 
95.69% 
76.55% 
11,070,500 
6.81% 
 
  
Notes: 
1. Ranking of placees is based on the number of H Shares allotted to the placees. 
 
H SHAREHOLDERS CONCENTRATION ANALYSIS 
  
H Shareholders 
Note 1 
Number of H 
Shares allotted 
Allotment as % of 
International Offering  
Allotment as % of 
total Offer Shares 
Number of H Shares 
held upon Listing 
% of total issued H 
Shares capital upon 
Listing 
Number of Shares 
held upon Listing 
 
 Top 1 
0 
0.00% 
0.00% 
31,280,590 
24.68% 
52,563,980 
 Top 5 
0 
0.00% 
0.00% 
63,066,650 
49.77% 
86,079,350 
 Top 10 
3,710,000 
32.07% 
25.65% 
84,732,220 
66.86% 
107,744,920 
 Top 25 
5,700,000 
49.27% 
39.42% 
114,434,950 
90.30% 
139,398,030 
 
Notes: 
1. Ranking of H Shareholders is based on the number of H Shares held by H Shareholders upon Listing. 
 
 
 
 

<<<PAGE 19>>>
19 
 
SHAREHOLDER CONCENTRATION ANALYSIS 
 
 
Shareholders 
Note 1 
Number of H 
Shares allotted 
Allotment as % of 
International 
Offering 
Allotment as % of 
total Offer Shares 
Number of H Shares 
held upon Listing 
Number of Shares 
held upon Listing 
% of total issued 
share capital upon 
Listing 
Top 1 
0 
0.00% 
0.00% 
31,280,590 
52,563,980 
32.35% 
Top 5 
0 
0.00% 
0.00% 
57,878,730 
86,156,730 
53.02% 
Top 10 
0 
0.00% 
0.00% 
79,427,590 
109,655,970 
67.49% 
Top 25 
5,700,000 
49.27% 
39.42% 
111,789,580 
145,138,560 
89.32% 
 
 Notes: 
1. Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon Listing. 
 

<<<PAGE 20>>>
20 
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING 
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by the public 
will be conditionally allocated on the basis set out below: 
 
NO. OF H 
SHARES 
APPLIED FOR 
NO. OF VALID 
APPLICATIONS 
BASIS OF ALLOTMENT / BALLOT 
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL 
NO. OF H 
SHARES 
APPLIED FOR 
POOL A 
50 
77,605 
3,881 out of 77,605 applicants to receive 50 H 
Shares 
5.00% 
100 
15,996 
957 out of 15,996 applicants to receive 50 H Shares 
2.99% 
150 
29,246 
1,942 out of 29,246 applicants to receive 50 H 
Shares 
2.21% 
200 
7,539 
539 out of 7,539 applicants to receive 50 H Shares 
1.79% 
250 
6,109 
463 out of 6,109 applicants to receive 50 H Shares 
1.52% 
300 
4,662 
370 out of 4,662 applicants to receive 50 H Shares 
1.32% 
350 
2,997 
248 out of 2,997 applicants to receive 50 H Shares 
1.18% 
400 
2,742 
235 out of 2,742 applicants to receive 50 H Shares 
1.07% 
450 
1,668 
147 out of 1,668 applicants to receive 50 H Shares 
0.98% 
500 
8,872 
804 out of 8,872 applicants to receive 50 H Shares 
0.91% 
600 
2,595 
247 out of 2,595 applicants to receive 50 H Shares 
0.79% 
700 
2,159 
214 out of 2,159 applicants to receive 50 H Shares 
0.71% 
800 
14,986 
1,532 out of 14,986 applicants to receive 50 H 
Shares 
0.64% 
900 
1,937 
205 out of 1,937 applicants to receive 50 H Shares 
0.59% 
1,000 
7,859 
851 out of 7,859 applicants to receive 50 H Shares 
0.54% 
1,500 
7,838 
942 out of 7,838 applicants to receive 50 H Shares 
0.40% 
2,000 
4,627 
599 out of 4,627 applicants to receive 50 H Shares 
0.32% 
2,500 
3,749 
514 out of 3,749 applicants to receive 50 H Shares 
0.27% 
3,000 
3,543 
510 out of 3,543 applicants to receive 50 H Shares 
0.24% 
3,500 
2,871 
430 out of 2,871 applicants to receive 50 H Shares 
0.21% 
4,000 
2,368 
367 out of 2,368 applicants to receive 50 H Shares 
0.19% 
4,500 
1,440 
230 out of 1,440 applicants to receive 50 H Shares 
0.18% 
5,000 
3,705 
608 out of 3,705 applicants to receive 50 H Shares 
0.16% 
6,000 
2,202 
379 out of 2,202 applicants to receive 50 H Shares 
0.14% 
7,000 
2,037 
365 out of 2,037 applicants to receive 50 H Shares 
0.13% 
8,000 
1,839 
341 out of 1,839 applicants to receive 50 H Shares 
0.12% 
9,000 
1,585 
303 out of 1,585 applicants to receive 50 H Shares 
0.11% 
10,000 
10,668 
2,091 out of 10,668 applicants to receive 50 H 
Shares 
0.10% 

<<<PAGE 21>>>
21 
 
20,000 
8,406 
1,970 out of 8,406 applicants to receive 50 H 
Shares 
0.06% 
30,000 
5,969 
1,553 out of 5,969 applicants to receive 50 H 
Shares 
0.04% 
40,000 
3,826 
1,072 out of 3,826 applicants to receive 50 H 
Shares 
0.04% 
50,000 
3,192 
948 out of 3,192 applicants to receive 50 H Shares 
0.03% 
60,000 
2,206 
687 out of 2,206 applicants to receive 50 H Shares 
0.03% 
70,000 
1,888 
612 out of 1,888 applicants to receive 50 H Shares 
0.02% 
80,000 
5,275 
1,767 out of 5,275 applicants to receive 50 H 
Shares 
0.02% 
Total 
266,206  
Total number of Pool A successful applicants: 
28,923 
 
 
 
 
 
 
POOL B 
 
90,000 
5,321 
50 H Shares plus 1,384 out of 5,321 applicants to 
receive an additional 50 H Shares 
0.07% 
100,000 
7,286 
50 H Shares plus 2,186 out of 7,286 applicants to 
receive an additional 50 H Shares 
0.07% 
200,000 
2,904 
50 H Shares plus 1,743 out of 2,904 applicants to 
receive an additional 50 H Shares 
0.04% 
300,000 
1,094 
50 H Shares plus 895 out of 1,094 applicants to 
receive an additional 50 H Shares 
0.03% 
361,550 
3,161 
50 H Shares plus 2,948 out of 3,161 applicants to 
receive an additional 50 H Shares 
0.03% 
Total 
19,766 
Total number of Pool B successful applicants: 
19,766 
 
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries. 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of which 
consent has been obtained, the Company has complied with the Listing Rules and guidance materials in 
relation to the placing, allotment and listing of the Company’s H Shares. 
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees or the public 
(as the case may be) directly or indirectly for each Offer Share subscribed for or purchased by them was the 
same as the Offer Price in addition to any brokerage, AFRC transaction levy, SFC transaction levy and Stock 
Exchange trading fee payable. 
The Directors and the Overall Coordinators confirm that at least 50% of the total number of the Offer Shares 
have been allocated to and taken up by independent price setting investors in compliance with Rule 18C.08 
of the Listing Rules. 
The Directors further confirm that at least 10% of the issued share capital of the Company will be held by 
sophisticated independent investors at the time of Listing in compliance with Chapter 2.5 of the Guide for 
New Listing Applicants. 

<<<PAGE 22>>>
22 
 
OTHERS / ADDITIONAL INFORMATION 
Reallocation 
As the Hong Kong Public Offering has been over-subscribed by more than 50 times of the total number of 
Offer Shares initially available under the Hong Kong Public Offering, the reallocation procedure as disclosed 
in the section headed “Structure of the Global Offering – The Hong Kong Public Offering – Reallocation and 
Clawback” in the Prospectus has been applied.  
The number of Offer Shares initially available under the Hong Kong Public Offering is 723,100 H Shares, 
representing approximately 5% of the total number of Offer Shares initially available under the Global 
Offering (before exercise of the Offer Size Adjustment Option). As a result of such reallocation, the final 
number of Offer Shares under the Hong Kong Public Offering is adjusted to 2,892,250 Offer Shares, 
representing approximately 20% of the total number of Offer Shares initially available under the Global 
Offering (before exercise of the Offer Size Adjustment Option). 
Placing to Connected Clients (including those who are close associate of existing Shareholder) with Prior 
Consents under Paragraphs 1C(1) and 1C(2) of the Placing Guidelines and waivers from the strict 
compliance with Rule 10.04 of the Listing Rules (as applicable) 
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, consents under 
paragraphs 1C(1) and/or 1C(2) of the Placing Guidelines to permit allocation to connected clients (including 
those who are close associates of existing Shareholders) listed below. The allocation of Offer Shares to such 
connected clients is in compliance with all the conditions under the consents granted by the Stock Exchange. 
Details of the placement to connected clients are set out below.  
 
Connected 
Distributor 
Placee/Connected 
Client 
Relationship 
Whether the 
Connected 
Client will hold 
the beneficial 
interests of the 
Offer Shares on 
a non-
discretionary 
basis or 
discretionary 
basis for 
independent 
third parties 
Number of 
Offer 
Shares to 
be 
allocated 
to the 
connected 
client 
Approximate 
percentage of 
Offer Shares 
allocated to 
the connected 
client 
Approximate 
percentage of 
total issued 
Shares after 
the Global 
Offering 
Hong Tai 
Securities 
Limited 
(“Hong Tai 
Securities”) 
Starwin 
International Note 1 
Starwin 
International’s 
general partner is 
Starwin Wealth 
Management 
Limited and its 
investment manager 
is Hong Tai 
Securities. As Hong 
Tai Securities is one 
of the Joint Global 
Coordinators, the 
Joint Bookrunners, 
the Joint Lead 
Managers and the 
Underwriters, 
Non-
discretionary 
basis 
492,500 
3.41% 
0.30% 

<<<PAGE 23>>>
23 
 
Starwin 
International is a 
connected client of 
Hong Tai Securities 
Wang On 
Securities 
Limited 
(“Wang On 
Securities”) 
New Harvest Note 2 
New Harvest is a 
company 
incorporated in 
Hong Kong and its 
discretionary sub-
manager is Wang 
On Asset 
Management 
Limited, which is a 
member of the same 
group of companies 
as Wang On 
Securities.  
Discretionary 
basis 
829,150 
5.73% 
0.51% 
CLSA 
Limited 
(“CLSA”) 
CITIC Securities 
International 
Capital 
Management 
Limited (“CSI”) 
Note 3 
CSI is a member of 
the same group of 
companies as CLSA 
Note 4 
Non-
discretionary 
basis 
31,350 
0.22% 
0.019% 
CLSA 
CITIC Securities 
Asset Management 
(HK) Limited 
(“CITIC AM 
HK”) 
CITIC AM HK is a 
member of the same 
group of companies 
as CLSA Note 4 
Discretionary 
basis 
1,700 
0.01% 
0.001% 
CLSA 
CITIC Securities 
Asset Management 
Company Limited 
(“CITIC AM”) 
CITIC AM is a 
member of the same 
group of companies 
as CLSA Note 4 
Discretionary 
basis 
1,700 
0.01% 
0.001% 
Notes: 
1. Starwin International is a limited partnership fund established in Hong Kong in December 2025, and 
is primarily engaged in investment. Its general partner is Starwin Wealth Management Limited, and 
its non-discretionary investment manager is Hong Tai Securities, both of which are ultimately 
controlled by Ms. Shen Yanjie (沈燕婕). Ms. Shen Yanjie is the general manager and executive director 
of Hong Tai Securities and is responsible for the overall management and supervision of securities 
business. Based on the information provided, Starwin International has nine limited partners, of which 
Ms. Zhu Jianhua (朱建華) holds approximately 53.33% partnership interest and none of the others 
holds 30% or more. To the best knowledge and information of the Company, all these above-mentioned 
entities and individuals are independent third parties of the Company. 
2. New Harvest intends to hold the Offer Shares on behalf of its ultimate clients (“New Harvest Ultimate 
Clients”) who are independent third parties. To the best knowledge of New Harvest after due enquiry, 
each of the New Harvest Ultimate Clients is an independent third party of the Company, its subsidiaries, 
New Harvest and Wang On Securities and the companies which are members of the same group of 
Wang On Securities. 
3. CSI will act as the single counterparty of a back-to-back total return swap transaction (the “CSI Back-
to-back TRS”) to be entered into by CSI in connection with a total return swap order (the “CSI Client 
TRS”) placed and fully funded by its ultimate clients (the “CSI Ultimate Client(s)”), by which CSI 
will pass the full economic exposure of the Offer Shares placed to CSI to the CSI Ultimate Clients. CSI 
will hold the beneficial interest of the Offer Shares on behalf of the CSI Ultimate Client on a non-
discretionary basis. The CSI Ultimate Client may exercise an early termination right to early terminate 
the CSI Client TRS at any time from the trade date of the CSI Client TRS which should be on or after 

<<<PAGE 24>>>
24 
 
the date on which the Offer Shares are listed on the Stock Exchange. Upon the final maturity or 
termination of the CSI Client TRS by the CSI Ultimate Client, CSI will dispose of the Offer Shares on 
the secondary market and the CSI Ultimate Client will receive a final termination amount of the CSI 
Back-to-back TRS which should have taken into account all the economic returns or economic loss in 
relation to the Offer Shares and the fixed amount of transaction fees of the CSI Back-to-back TRS and 
the CSI Client TRS. CSI will not exercise the voting right of the Offer Shares during the terms of the 
CSI Back-to-back TRS. 
4. As disclosed in the Prospectus, as of the Latest Practicable Date, approximately 0.91% of the total 
number of issued Shares was held by CITIC Securities Investment Co., Ltd. (中信証券投資有限公司) 
(“CITIC Securities Investment”), which is a wholly-owned subsidiary of CITIC Securities Company 
Limited (a company listed on the Shanghai Stock Exchange with stock code 600030 and on the Hong 
Kong Stock Exchange with stock code 6030) (“CITICS”); and (ii) approximately 1.17% of the total 
number of issued Shares was held by Shaanxi Big Data Industry Investment Fund Partnership (Limited 
Partnership) (陝西大數據產業投資基金合夥企業（有限合夥）) (“Shaanxi Big Data”), which is 
a limited partnership established in the PRC and is owned as to 67% by CITICS. Each of CSI, CITIC 
AM HK and CITIC AM are all members of the same group of companies of CLSA, which is an indirect 
subsidiary controlled by CITICS. As such, each of CSI, CITIC AM HK and CITIC AM is a close 
associate of CITIC Securities Investment and Shaanxi Big Data under the Listing Rules. 
 

<<<PAGE 25>>>
25 
 
DISCLAIMERS 
 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and Hong 
Kong Securities Clearing Company Limited take no responsibility for the contents of this announcement, 
make no representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the 
contents of this announcement. 
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of 
Columbia). This announcement does not, and is not intended to, constitute or form a part of any offer to 
sell or solicitation to purchase or subscribe for any securities in the United States. The Offer Shares have 
not been, and will not be, registered under the United States Securities Act of 1933, as amended (the “U.S. 
Securities Act”) or securities law of any state or other jurisdiction of the United States and may not be 
offered, sold, pledged or otherwise transferred within the United States, except pursuant to an available 
exemption from, or in a transaction not subject to, the registration requirements of the U.S. Securities Act. 
There will be no public offer of the Offer Shares in the United States.  
The Offer Shares are being offered and sold solely outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or offer to 
acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential investors 
should read the Prospectus dated May 12, 2026 issued by the Company for detailed information about 
the Global Offering described below before deciding whether or not to invest in the H Shares thereby 
being offered. 
* Potential investors of the Offer Shares should note that the Sole Sponsor and the Sponsor-Overall 
Coordinator (for itself and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of 
any of the events set out in the section headed “Underwriting – Underwriting Arrangements and Expenses 
– Hong Kong Underwriting Agreement – Grounds for Termination” in the Prospectus at any time prior 
to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Wednesday, May 
20, 2026). 
 
 

<<<PAGE 26>>>
– 26 –
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering (after taking into account the full 
exercise of the Offer Size Adjustment Option) and based on the Offer Price of HK$60.30 per 
H Share:
(1) 
95,444,860 H Shares representing approximately 58.74% of the issued share capital of 
the Company will be counted towards the public float for the purpose of Rule 19A.13A 
of the Listing Rules, which is higher than the prescribed percentage of H Shares required 
to be held in public hands of 15.3094% under Rule 19A.13A of the Listing Rules; and
(2) 
excluding the Offer Shares to be allocated to the Cornerstone Investors that are subject 
to a lock-up period of six months following the Listing Date and the H Shares to be 
converted from Unlisted Shares that are subjected to a lock-up period of 12 months 
following the Listing Date, the Company’s H Shares to be counted towards the free float 
upon Listing will be 10,129,000 H Shares. Based on the Offer Price of HK$60.30 per H 
Share, the free float of the Company represents approximately 6.23% of the total issued 
share capital of the Company at the time of Listing with a market value of approximately 
HK$610.78 million. Accordingly, the Company will satisfy the free float requirement 
under Rule 19A.13C(1) of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering: (i) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital 
of the Company immediately after the Global Offering; (ii) there will not be any new 
substantial Shareholder immediately after the Global Offering; (iii) the three largest public 
Shareholders do not hold more than 50% of the H Shares in public hands at the time of Listing 
in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 
300 Shareholders at the time of Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Wednesday, 
May 20, 2026 (Hong Kong time), provided that the Global Offering has become unconditional 
and the right of termination described in the section headed “Underwriting – Underwriting 
Arrangements and Expenses – Hong Kong Underwriting Agreement – Grounds for 
Termination” in the Prospectus has not been exercised. Investors who trade the H Shares on 
the basis of publicly available allocation details prior to the receipt of H Share certificates or 
prior to the H Share certificates becoming valid evidence of title do so entirely at their own 
risk.

<<<PAGE 27>>>
– 27 –
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on 
Wednesday, May 20, 2026 (Hong Kong time), it is expected that dealings in the H Shares on 
the Stock Exchange will commence at 9:00 a.m. on Wednesday, May 20, 2026 (Hong Kong 
time). The H Shares will be traded in board lots of 50 H Shares each, and the stock code of the 
H Shares will be 1511.
By order of the Board
UISEE Technologies (Beijing) Co., Ltd.
Mr. Wu Gansha
Chairman of the Board, Executive Director and
Chief Executive Officer
Hong Kong, May 19, 2026
As at the date of this announcement, the board of directors of the Company comprises: (i) Mr. 
Wu Gansha, Mr. Zhou Xin and Mr. Chiang Tsung Che as executive Directors; (ii) Mr. Wu 
Jun, Mr. Zhou Jun and Mr. Gao Xiaohu as non-executive Directors; and (iii) Mr. Chow Ming 
Sang, Ms. Bai Rui and Mr. Du Zide as independent non-executive Directors.
