# 配发结果公告抽取任务：2672.HK Baige Online Digital Technology Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**26/06/2026 21:13**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0626/2026062602363.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2672.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Hong Kong Stock 
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no responsibility for the contents 
of this announcement, make no representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the contents of this 
announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer to sell or solicitation to purchase or subscribe for 
securities in the United States or in any other jurisdictions in which such offer or solicitation would be unlawful. The 
securities mentioned herein have not been, and will not be, registered under the United States Securities Act of 1933 as 
amended from time to time (the “U.S. Securities Act”) or any state securities law of the United States. The securities 
may not be offered, sold, pledged or transferred within the United States or to, or for the account or benefit of U.S. 
persons (as defined in Regulation S under the U.S. Securities Act (“Regulation S”)), except in transactions exempt 
from, or not subject to, the registration requirements of the U.S. Securities Act. The Offer Shares may be offered, sold 
or delivered outside the United States to non-U.S. persons in offshore transactions in accordance with Regulation S.
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for securities. This announcement is not a prospectus. Potential investors should read the prospectus dated 
Thursday, June 18, 2026 (the “Prospectus”) issued by Baige Online Digital Technology Co., Ltd. (白鴿在線(廈門)數
字科技股份有限公司) (the “Company”) for detailed information about the Global Offering described below before 
deciding whether or not to invest in the H Shares thereby being offered. Any investment decision in relation to the 
Offer Shares should be taken solely in reliance on the information in the Prospectus. The Company has not been and 
will not be registered under the U.S. Investment Company Act of 1940, as amended.
Unless otherwise defined in this announcement, capitalized terms used herein shall have the same meanings as those 
defined in the Prospectus.
In connection with the Global Offering, CMBC Securities Company Limited, as stabilizing manager (the “Stabilizing 
Manager”) (or its affiliates or any person acting for it), on behalf of CMBC Securities Company Limited, BOCI Asia 
Limited, Huafu International Securities Limited, ICBC International Securities Limited, ABCI Securities Company 
Limited, CMB International Capital Limited, SPDB International Capital Limited, Futu Securities International (Hong 
Kong) Limited, Tiger Brokers (HK) Global Limited, Fortune (HK) Securities Limited, uSmart Securities Limited, 
Hua Liang Securities Limited, Harmonia Capital Limited, Guoyuan Securities Brokerage (Hong Kong) Limited and 
Zircon Securities (HK) Limited (collectively, the “Underwriters”), the extent permitted by the applicable laws and 
regulatory requirements of Hong Kong or elsewhere, may over-allocate or effect transactions with a view to stabilizing 
or supporting the market price of the H Shares at such price, in such amounts and in such manners as the Stabilizing 
Manager, its affiliates or any person acting for it may determine and at a level higher than that which might otherwise 
prevail for a limited period after the Listing Date. However, there is no obligation on the Stabilizing Manager (or its 
affiliates or any person acting for it) to conduct any such stabilizing action. Such stabilizing action, if taken, (a) will 
be conducted at the absolute discretion of the Stabilization Manager (or its affiliates or any person acting for it) and 
in what the Stabilizing Manager reasonably regards as the best interest of our Company, (b) may be discontinued at 
any time and (c) is required to be brought to an end within 30 days of the last day for lodging applications under the 
Hong Kong Public Offering (which is Friday, July 24, 2026). Such stabilizing action, if taken, may be effected in all 
jurisdictions where it is permissible to do so, in each case in compliance with all applicable laws, rules and regulatory 
requirements, including the Securities and Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong 
Kong), as amended, made under the Securities and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the H Shares for 
longer than the stabilization period, which will begin on the Listing Date, and is expected to expire on the 30th day 
after the last day for lodging applications under the Hong Kong Public Offering (which is Friday, July 24, 2026). After 
this date, when no further stabilizing action may be taken, demand for the H Shares, and therefore the price of the H 
Shares, could fall.
The Overall Coordinators confirm that there has been no over-allocation of the H Shares under the International 
Offering, therefore, there will not be any delayed delivery arrangement and the Over-allotment Option will not be 
exercised. In view of the fact that there has been no over-allocation of the H Shares under the International Offering, 
no stabilizing action as described in the Prospectus will be taken during the stabilization period.
Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the 
Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set out in the 
section headed “Underwriting – Underwriting Arrangements – Hong Kong Public Offering – Grounds for Termination” 
in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to 
be on Monday, June 29, 2026).

<<<PAGE 2>>>
2
Baige Online Digital Technology Co., Ltd.
白鴿在線(廈門)數字科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the Global 
Offering
:
33,344,400 H Shares
Number of Hong Kong Offer Shares
:
3,334,600 H Shares
Number of International Offer Shares
:
30,009,800 H Shares
Final Offer Price
:
HK$15.60 per H Share plus brokerage of 
1.0%, SFC transaction levy of 0.0027%, 
Stock Exchange trading fee of 0.00565% 
and AFRC transaction levy of 0.00015% 
(payable in full on application in Hong Kong 
dollars and subject to refund)
Nominal value
:
RMB0.25 per H Share
Stock Code
:
2672
Joint Sponsors, Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers
Joint Lead Manager

<<<PAGE 3>>>
Baige Online Digital Technology Co., Ltd. 
白鴿在線(廈門)數字科技股份有限公司 
ANNOUNCEMENT OF ALLOTMENT RESULTS 
 
Unless otherwise defined herein, capitalized terms used in this announcement shall have the 
same meanings as those defined in the prospectus dated June 18, 2026 (the “Prospectus”) 
issued by Baige Online Digital Technology Co., Ltd. (白鴿在線(廈門)數字科技股份有限公
司) (the “Company”).  
 
 
Warning: In view of high concentration of shareholding in a small number of 
Shareholders, Shareholders and prospective investors should be aware that the price 
of the H Shares could move substantially even with a small number of H Shares traded 
and should exercise extreme caution when dealing in the H Shares. 
SUMMARY 
 
Company Information 
Stock Code 
2672 
Stock Short Name 
BAIGE DIGITAL 
Dealings commencement date 
June 29, 2026* 
* see note at the end of the announcement 
 
Price Information 
Offer Price 
HK$15.60 
 
Offer Shares and Share Capital 
Number of Offer Shares  
33,344,400 
Final number of Offer Shares in Hong 
Kong Public Offering  
3,334,600 
Final number of Offer Shares in 
International Offering  
30,009,800 
Number of issued Shares upon Listing 
320,620,632 
 
Over-allocation 
No. of Offer Shares over-allocated 
N/A 
There has been no over-allocation of Offer Shares in the International Offering. Therefore, 
the Over-allotment Option will not be exercised and will lapse upon Listing. 
 
Proceeds 
Gross proceeds (Note) 
HK$520,172,640 
Less: Estimated 
listing 
expenses 
payable based on Final Offer 
Price 
HK$54,382,183 

<<<PAGE 4>>>
Net Proceeds 
HK$465,790,457 
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For 
details of the use of proceeds, please refer to the section headed “Future Plans and Use of 
Proceeds” of the Prospectus.  
 
ALLOTMENT RESULTS DETAILS 
 
HONG KONG PUBLIC OFFERING  
 
 
No. of valid applications 
44,599 
No. of successful applications 
8,936 
Subscription level 
242.05 times 
Claw-back triggered  
N/A 
No. of Offer Shares initially available under the Hong Kong 
Public Offering 
3,334,600 
Final no. of Offer Shares under the Hong Kong Public 
Offering 
3,334,600 
% of Offer Shares under the Hong Kong Public Offering to 
the Global Offering  
10.00% 
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, 
investors can refer to www.eipo.com.hk/eIPOAllotment to perform a search by identification 
number or www.eipo.com.hk/eIPOAllotment for the full list of allottees. 
 
INTERNATIONAL OFFERING  
 
 
No. of placees 
95 
Subscription level  
2.44 times 
No. of Offer Shares initially available under the International Offering 30,009,800 
Final no. of Offer Shares under the International Offering 
30,009,800 
% of Offer Shares under the International Offering to the Global 
Offering  
90.0% 
 
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of 
the Offer Shares subscribed by the placees and the public have been financed directly or 
indirectly by the Company, any of the Directors, chief executive of the Company, Controlling 
Shareholders, substantial Shareholders, existing Shareholders of the Company or any of its 
subsidiaries or their respective close associates; and (ii) none of the placees and the public 
who have purchased the Offer Shares are accustomed to taking instructions from the Company, 
any of the Directors, chief executive of the Company, Controlling Shareholders, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their 
respective close associates in relation to the acquisition, disposal, voting or other disposition 
of H Shares registered in his/her/its name or otherwise held by him/her/it. 

<<<PAGE 5>>>
 
The placees in the International Offering include the following: 
 
Cornerstone Investors  
 
Investor 
No. of Offer 
Shares 
allocated Note 
1 
% of total 
issued H 
Shares upon 
Listing 
% of total issued 
share capital of 
the Company 
immediately after 
the Global 
Offering  
Existing 
shareholders or 
their close 
associates 
GLY New 
Mobility 
641,000 
0.42% 
0.20% 
No 
Mr. Ke 
641,000 
0.42% 
0.20% 
No 
Total 
1,282,000 
0.84% 
0.40% 
- 
 
Note: 
(1) The number of Offer Shares allocated to such investor only represents the number of Offer Shares allocated 
to the investors as cornerstone investors in the International Offering. 
 
 

<<<PAGE 6>>>
 
 
LOCK-UP UNDERTAKINGS  
 
Existing Shareholders (excluding Pre-IPO Investors)  
 
Name 
Number of 
shares held 
in the 
Company 
subject to 
lock-up 
undertaking 
Number of H 
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
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing  
Last day 
subject to the 
lock-up 
undertakings 
Note 1  
Controlling Shareholders Note 2 
Fujian 
Helihemei 
129,638,800 
N/A 
N/A 
40.43% 
June 28, 
2027 
Baige 
Tongchuang 
30,022,296 
10,507,800 
6.96% 
9.36% 
June 28, 
2027 
Other Existing Shareholder 
Gerui 
Xiamen 
26,638,000 
14,650,800 
9.70% 
8.31% 
June 28, 
2027 
Xiamen 
Fuguohao 
21,310,400 
14,917,200 
9.88% 
6.65% 
June 28, 
2027 
Yujin 
Tongxing 
7,575,704 
7,575,704 
5.02% 
2.36% 
June 28, 
2027 
Notes:  
1. The expiry date of the lock-up period is pursuant to the PRC Company Law, which is 
longer than the lock-up period required for controlling shareholders under Rule 
10.07 of the Listing Rules. 
2. Fujian Helihemei is owned as to approximately 58.90% by Mr. Tu, 20.55% by Xiamen 
Zhongjiaxiu (which is in turn owned as to 80% by Mr. Su Weida (蘇偉達) and 20% 
by Mr. Huang Jia’en (黃嘉恩)) and 20.55% by Mr. Zeng. Baige Tongchuang is held 
as to 99.9% by Fujian Helihemei and 0.1% by Mr. Tu with Mr. Tu as its executive 
partner. Mr. Tu, Xiamen Zhongjiaxiu, Mr. Su Weida, Mr. Huang Jia’en, Mr. Zeng, 
Baige Tongchuang and Fujian Helihemei have been acting in concert since 
November 9, 2023. Upon Listing, Mr. Tu, Mr. Zeng, Mr. Su, Mr. Huang, Xiamen 
Zhongjiaxiu, Fujian Helihemei and Baige Tongchuang will constitute a group of 
Controlling Shareholders. For further details, please refer to “Relationship with our 
Controlling Shareholders” in the Prospectus. This subsection illustrates their direct 
shareholding in the Company. 
 
Pre-IPO Investors 
 
Name 
Number of 
shares held 
in the 
Company 
subject to 
lock up 
Number of 
H Shares 
held in the 
Company 
subject to 
lock-up 
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
Last day 
subject to the 
lock-up 
undertakings 
Note 

<<<PAGE 7>>>
 
 
undertaking 
undertakings 
upon Listing 
lock-up 
undertakings 
upon Listing  
undertakings 
upon Listing  
Xiamen 
Huicheng 
10,652,800 
10,652,800 
7.06% 
3.32% 
June 28, 
2027 
New Hope 
39,854,000 
39,854,000 
26.40% 
12.43% 
June 28, 
2027 
Xiamen 
Meitong 
Luqi 
9,926,000 
9,926,000 
6.58% 
3.10% 
June 28, 
2027 
Mr. Lin 
Baojie (林
報捷) 
2,204,800 
2,204,800 
1.46% 
0.69% 
June 28, 
2027 
Jiaxing 
Mianmiao 
5,305,600 
5,305,600 
3.51% 
1.65% 
June 28, 
2027 
Prolight 
707,820 
707,820 
0.47% 
0.22% 
June 28, 
2027 
Fujian 
Yongchun 
2,123,464 
N/A 
N/A 
0.66% 
June 28, 
2027 
Minyin 
Sci-Tech 
1,316,548 
1,316,548 
0.87% 
0.41% 
June 28, 
2027 
Note: The expiry date of the lock-up period is pursuant to the PRC Company Law. 
 
Cornerstone Investors  
 
Name 
Number of H Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing 
% of shareholding 
in the Company 
subject to lock-up 
undertakings upon 
Listing  
Last day subject to the 
lock-up undertakings 
Note 
GLY New 
Mobility 
641,000 
0.20% 
June 28, 2027 
Mr. Ke 
641,000 
0.20% 
June 28, 2027 
Note: In accordance with the relevant cornerstone investment agreements, the required lock-
up ends on 12 months after the Listing Date, i.e. June 28, 2027. The Cornerstone Investors 
will cease to be prohibited from disposing of or transferring H Shares subscribed for 
pursuant to the relevant cornerstone investment agreements after the indicated date. 
 
 
PLACEE CONCENTRATION ANALYSIS  
 
Placees* 
Number of H 
Shares allotted 
Allotment as % 
of International 
Offering 
Allotment 
as % of 
total Offer 
Shares  
Number of H 
Shares held 
upon Listing 
% of total 
issued share 
capital upon 
Listing  
Top 1 
4,025,600 
13.41% 
12.07% 
4,025,600 
1.26% 
Top 5 
11,384,000 
37.93% 
34.14% 
11,384,000 
3.55% 
Top 10 
16,383,600 
54.59% 
49.13% 
16,383,600 
5.11% 
Top 25 
26,895,600 
89.62% 
80.66% 
26,895,600 
8.39% 
 

<<<PAGE 8>>>
 
 
Note 
* Ranking of placees is based on the number of H Shares allotted to the placees. 
 
H SHAREHOLDERS CONCENTRATION ANALYSIS  
 
H 
Shareholders* 
Number of 
H Shares 
allotted 
Allotment 
as % of 
International 
Offering  
Allotment 
as % of 
total 
Offer 
Shares  
Number of 
H Shares 
held upon 
Listing 
% of 
total 
issued H 
Shares 
upon 
Listing  
Number of 
Shares held 
upon Listing 
% of total 
issued 
share 
capital 
upon 
Listing 
Top 1 
- 
- 
- 
39,854,000 
26.40% 
39,854,000 
12.43% 
Top 5 
- 
- 
- 
90,582,600 
60.00% 
258,116,296 
80.51% 
Top 10 
7,858,800 
26.19% 
23.57% 
121,248,704 
80.32% 
288,782,400 
90.07% 
Top 25 
20,357,600 
67.84% 
61.05% 
137,268,852 
90.93% 
304,802,548 
95.07% 
 
Note 
* Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders 
upon Listing. 
 
SHAREHOLDER CONCENTRATION ANALYSIS  
 
Shareholders* 
Number of 
H Shares 
allotted 
Allotment 
as % of 
Internation
al Offering  
Allotment 
as % of 
total Offer 
Shares  
Number of H 
Shares held 
upon Listing 
% of 
total 
issued 
share 
capital 
upon 
Listing  
Number of 
Shares held 
upon Listing 
% of 
total 
issued 
share 
capital 
upon 
Listing 
Top 1 
- 
- 
- 
10,507,800 
3.28% 
159,661,096 
49.80% 
Top 5 
- 
- 
- 
90,582,600 
28.25% 
258,116,296 
80.51% 
Top 10 
7,858,800 
26.19% 
23.57% 
121,248,704 
37.82% 
288,782,400 
90.07% 
Top 25 
19,588,400 
65.27% 
58.75% 
136,499,652 
42.57% 
306,156,812 
95.49% 
 
Note 
* Ranking of Shareholders is based on the number of Shares (of all classes) held by the 
Shareholder upon Listing. 
 

<<<PAGE 9>>>
 
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING  
 
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 44,599 valid 
applications made by the public will be conditionally allocated on the basis set out below: 
 
NO. OF SHARES 
APPLIED FOR 
NO. OF VALID 
APPLICATIONS 
BASIS OF 
ALLOTMENT / 
BALLOT 
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL NO. 
OF H SHARES 
APPLIED FOR 
POOL A 
200 
21,031 
2,103 out of 21,031 to 
receive 200 Shares 
10.00% 
400 
12,534 
1,680 out of 12,534 to 
receive 200 Shares 
6.70% 
600 
730 
119 out of 730 to 
receive 200 Shares 
5.43% 
800 
354 
65 out of 354 to receive 
200 Shares 
4.59% 
1,000 
658 
132 out of 658 to 
receive 200 Shares 
4.01% 
1,200 
190 
41 out of 190 to receive 
200 Shares 
3.60% 
1,400 
217 
51 out of 217 to receive 
200 Shares 
3.36% 
1,600 
146 
36 out of 146 to receive 
200 Shares 
3.08% 
1,800 
118 
31 out of 118 to receive 
200 Shares 
2.92% 
2,000 
3,483 
947 out of 3,483 to 
receive 200 Shares 
2.72% 
3,000 
319 
103 out of 319 to 
receive 200 Shares 
2.15% 
4,000 
770 
283 out of 770 to 
receive 200 Shares 
1.84% 
5,000 
261 
106 out of 261 to 
receive 200 Shares 
1.62% 
6,000 
126 
55 out of 126 to receive 
200 Shares 
1.46% 
7,000 
66 
31 out of 66 to receive 
200 Shares 
1.34% 
8,000 
123 
61 out of 123 to receive 
200 Shares 
1.24% 
9,000 
83 
43 out of 83 to receive 
200 Shares 
1.15% 
10,000 
485 
265 out of 485 to 
receive 200 Shares 
1.09% 
20,000 
377 
278 out of 377 to 
receive 200 Shares 
0.74% 
30,000 
183 
161 out of 183 to 
receive 200 Shares 
0.59% 
40,000 
144 
200 Shares 
0.50% 
50,000 
148 
200 Shares plus 15 out 
of 148 to receive 
0.44% 

<<<PAGE 10>>>
 
 
additional 200 Shares 
60,000 
98 
200 Shares plus 19 out 
of 98 to receive 
additional 200 Shares 
0.40% 
70,000 
57 
200 Shares plus 16 out 
of 57 to receive 
additional 200 Shares 
0.37% 
80,000 
43 
200 Shares plus 15 out 
of 43 to receive 
additional 200 Shares 
0.34% 
90,000 
61 
200 Shares plus 26 out 
of 61 to receive 
additional 200 Shares 
0.32% 
100,000 
335 
200 Shares plus 163 out 
of 335 to receive 
additional 200 Shares 
0.30% 
200,000 
303 
400 Shares 
0.20% 
 
43,443 
Total number of 
Pool A successful 
applicants: 7,780 
 
POOL B 
300,000 
532 
800 Shares plus 382 out 
of 532 to receive 
additional 200 Shares 
0.31% 
400,000 
183 
1,200 Shares 
0.30% 
500,000 
133 
1,400 Shares 
0.28% 
600,000 
35 
1,600 Shares 
0.27% 
700,000 
35 
1,800 Shares 
0.26% 
800,000 
37 
2,000 Shares 
0.25% 
900,000 
15 
2,200 Shares 
0.24% 
1,000,000 
46 
2,400 Shares 
0.24% 
1,100,000 
20 
2,600 Shares 
0.24% 
1,200,000 
16 
2,800 Shares 
0.23% 
1,300,000 
33 
3,000 Shares 
0.23% 
1,667,200 
71 
3,200 Shares 
0.19% 
 
1,156 
Total number of 
Pool B successful 
applicants: 1,156 
 
 
As of the date of this announcement, the relevant subscription monies previously deposited in 
the designated nominee accounts have been remitted back to the accounts of all HKSCC 
participants. Investors should contact their relevant brokers for any inquiries. 
 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
 
The Directors confirm that, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.  
 
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and trading fee payable. 
 

<<<PAGE 11>>>
 
 
DISCLAIMERS 
 
 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited 
and Hong Kong Securities Clearing Company Limited take no responsibility for the contents 
of this announcement, make no representation as to its accuracy or completeness and 
expressly disclaim any liability whatsoever for any loss howsoever arising from or in reliance 
upon the whole or any part of the contents of this announcement. 
This announcement is not for release, publication, distribution, directly or indirectly, in or 
into the United States (including its territories and possessions, any state of the United States 
and the District of Columbia). This announcement does not constitute or form a part of any 
offer to sell or solicitation to purchase or subscribe for securities in the United States or in 
any other jurisdictions in which such offer or solicitation would be unlawful. The securities 
mentioned herein have not been, and will not be, registered under the United States 
Securities Act of 1933 as amended from time to time (the “U.S. Securities Act”) or any state 
securities law of the United States. The securities may not be offered, sold, pledged or 
transferred within the United States or to, or for the account or benefit of U.S. persons (as 
defined in Regulation S under the U.S. Securities Act (“Regulation S”)), except in 
transactions exempt from, or not subject to, the registration requirements of the U.S. 
Securities Act. The Offer Shares may be offered, sold or delivered outside the United States 
to non-U.S. persons in offshore transactions in accordance with Regulation S. 
The Offer Shares are being offered and sold outside the United States in offshore transactions 
in reliance on Regulation S under the U.S. Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated June 18, 2026 issued by Baige Online 
Digital Technology Co., Ltd. for detailed information about the Global Offering described 
below before deciding whether or not to invest in the H Shares thereby being offered. 
*Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled 
to terminate their obligations under the Hong Kong Underwriting Agreement with immediate 
effect upon the occurrence of any of the events set out in the section headed “Underwriting 
– Underwriting Arrangements – Hong Kong Public Offering – Hong Kong Underwriting 
Agreement – Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. 
(Hong Kong time) on the Listing Date (which is currently expected to be on June 29, 2026). 
 
 
 

<<<PAGE 12>>>
 
 
PUBLIC FLOAT AND FREE FLOAT 
 
Immediately after the completion of the Global Offering , the total number of H Shares held in 
public hands represents approximately 25.69% of the total issued share capital of the Company, 
which is higher than the prescribed percentage of H Shares required to be held in public hands 
of 25% under Rule 19A.13A(1) of the Listing Rules calculated based on the final Offer Price 
of HK$15.60 per H Share, thereby satisfying Rule 19A.13A(1) of the Listing Rules. 
 
Each of the Cornerstone Investors has agreed to a lock-up period of 12 months following the 
Listing Date. As such, H Shares held by the Cornerstone Investors (excluding the Offer Shares 
subscribed for by them as placees) upon the Listing shall not be counted towards the free float 
of the H Shares of the Company at the time of Listing. Based on the final Offer Price of 
HK$15.60 per H Share, the Company satisfies the free float requirement under Rule 19A.13C(1) 
of the Listing Rules. 
 
The Directors confirm that, immediately following the completion of the Global Offering, (i) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of 
the Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder immediately after the Global Offering; (iii) the three largest public shareholders 
of the Company do not hold more than 50% of the H shares in public hands at the time of the 
Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be 
at least 300 Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the 
Listing Rules.  
 
COMMENCEMENT OF DEALINGS 
 
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Monday, June 
29, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and 
the right of termination described in the section headed “Underwriting – Underwriting 
Arrangements – Hong Kong Public Offering – Grounds for Termination” in the Prospectus has 
not been exercised. Investors who trade the H Shares on the basis of publicly available 
allocation details prior to the receipt of H Share certificates or prior to the H Share certificates 
becoming valid evidence of title do so entirely at their own risk. 
 
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Monday, 
June 29, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Monday, June 29, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 200 H Shares each, and the stock code of the H Shares 
will be 2672.  
 
By order of the Board  
Baige Online Digital Technology Co., Ltd.  
Tu Jinbo  
Executive Director, Chairman of the Board and 
Chief Executive Officer 
 
Hong Kong, June 26, 2026 
 
As at the date of this announcement, the board of directors of the Company (the 
“Director(s)”) comprises: (i) Mr. Tu Jinbo and Mr. Shi Wenzheng as executive 

<<<PAGE 13>>>
 
 
Directors; (ii) Mr. Zeng Jianhua, Mr. Zheng Yu and Mr. Wang Qianwei as non-executive 
Directors; and (iii) Dr. Zhao Zhengtang, Ms. Wong Gianne and Dr. Jiang Min as the 
proposed independent non-executive Directors.  
