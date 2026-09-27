# 配发结果公告抽取任务：6132.HK HJ Science Co., Ltd. - B - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**22/06/2026 21:30**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0622/2026062201627.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"6132.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
defined in the prospectus dated June 12, 2026 (the “Prospectus”) issued by HJ Science Co., Ltd. (華健未來(成都)科
技股份有限公司) (the “Company”).
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
In connection with the Global Offering, CLSA Limited, as stabilizing manager (the “Stabilizing Manager”), or any 
person acting for it, on behalf of the Underwriter, may over-allocate or effect transactions with a view to stabilizing 
or supporting the market price of the H Shares at a level higher than that which might otherwise prevail for a limited 
period after the Listing Date. However, there is no obligation on the Stabilizing Manager (or any person acting for it) 
to conduct any such stabilizing action, which, if commenced, will be done at the sole and absolute discretion of the 
Stabilizing Manager (or any person acting for it) and may be discontinued at any time. Any such stabilizing action is 
required to be brought to an end on the 30th day after the last day for the lodging of applications under the Hong Kong 
Public Offering. Such stabilizing action, if taken, may be effected in all jurisdictions where it is permissible to do so, 
in each case in compliance with all applicable laws, rules and regulatory requirements, including the Securities and 
Futures (Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities 
and Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors of the Offer Shares should note that the Sole Overall Coordinator (acting in such capacity and as the 
Hong Kong Underwriter) shall be entitled to terminate its obligations under the Hong Kong Underwriting Agreement 
with immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting – 
Underwriting Arrangements and Expenses – Hong Kong Public Offering – Hong Kong Underwriting Agreement – 
Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which 
is currently expected to be on Tuesday, June 23, 2026).

<<<PAGE 2>>>
2
HJ Science Co., Ltd.
華健未來(成都)科技股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the Global 
Offering
:
13,600,000 H Shares (subject to the Over-
allotment Option)
Number of Hong Kong Offer Shares
:
1,360,000 H Shares
Number of International Offer Shares
:
12,240,000 H Shares (subject to the Over-
allotment Option)
Offer Price
:
HK$81.80 per Offer Share, plus brokerage 
of 1.0%, SFC transaction levy of 
0.0027%, Stock Exchange trading fee of 
0.00565%, and AFRC transaction levy of 
0.00015%
Nominal Value
:
RMB1.00 per Share
Stock Code
:
6132
Sole Sponsor, Sponsor-Overall Coordinator, Sole Overall Coordinator, Sole Global 
Coordinator, Sole Bookrunner and Sole Lead Manager

<<<PAGE 3>>>
3 
 
HJ SCIENCE CO., LTD. / 華健未來（成都）科技股份有限公司 
ANNOUNCEMENT OF ALLOTMENT RESULTS 
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings 
as those defined in the Prospectus issued by the Company.  
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares could move 
substantially even with a small number of H Shares traded and should exercise extreme caution when 
dealing in the H Shares. 
SUMMARY  
 
Company information 
Stock code  
6132 
Stock short name  
HJ SCIENCE-B 
Dealings commencement date  
June 23, 2026* 
*see note at the end of the announcement  
Price Information  
Offer Price  
HK$81.80  
 
Offer Shares and Share Capital 
Number of Offer Shares (before exercise of Over-allotment 
Option) 
13,600,000 H Shares 
Final Number of Offer Shares in Hong Kong Public 
Offering  
1,360,000 H Shares 
Final Number of Offer Shares in International Offering 
(before exercise of Over-allotment Option)  
12,240,000 H Shares 
Number of issued shares upon Listing (before exercise of 
Over-allotment Option) 
73,599,605 Shares 
 
Over-allocation 
Number of Offer Shares over-allocated 
2,040,000 H Shares 
 
Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases in the 
secondary market at prices that do not exceed the Offer Price or through deferred delivery or a combination of these 
means. In the event the Over-allotment Option is exercised, an announcement will be made on the Stock Exchange’s 
website. 
Proceeds  
Gross proceeds (Note)  
HK$1,112.5 million 
Less: Estimated listing expenses payable based on Offer 
Price  
HK$93.7 million 
Net proceeds  
HK$1,018.7 million 
Note: Gross proceeds refers to the amount to which the Company is entitled to receive. For details of the 
use of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. 
Any discrepancies in the table between the aggregate amount and the sums of individual amounts listed 
therein are due to rounding.  
 

<<<PAGE 4>>>
4 
 
ALLOTMENT RESULTS DETAILS 
HONG KONG PUBLIC OFFERING 
 
No. of valid applications  
173,284 
No. of successful applications  
13,418 
Subscription level  
2,007.60 times 
Reallocation 
N/A  
No. of Offer Shares initially available under the Hong Kong Public 
Offering 
1,360,000 
No. of Offer Shares reallocated from the International Offering 
N/A 
Final no. of Offer Shares under the Hong Kong Public Offering 
1,360,000 
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering (before exercise of Over-allotment Option) 
10.00% 
 
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
www.eipo.com.hk/eIPOAllotment 
to 
perform 
a 
search 
by 
identification 
number 
or 
www.eipo.com.hk/eIPOAllotment for the full list of allottees. 
INTERNATIONAL OFFERING  
 
No. of placees  
91  
Subscription Level 
7.00 times  
No. of Offer Shares initially available under the International 
Offering 
12,240,000  
Final no. of Offer Shares under the International Offering (before 
exercise of Over-allotment Option) 
12,240,000 
% of Offer Shares under the International Offering to the Global 
Offering (before exercise of Over-allotment Option) 
90.00% 
 
The Directors confirm that, to the best of their knowledge, information and belief, save for consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules, (i) none of the Offer Shares subscribed by the placees 
and the public have been financed directly or indirectly by the Company, any of the Directors, Supervisors, 
chief executive of the Company, substantial Shareholders, existing Shareholders of the Company or any of its 
subsidiaries or their respective close associates; and (ii) none of the placees and the public who have 
purchased the Offer Shares are accustomed to taking instructions from the Company, any of the Directors, 
Supervisors, chief executive of the Company, substantial Shareholders, existing Shareholders of the Company 
or any of its subsidiaries or their respective close associates in relation to the acquisition, disposal, voting or 
other disposition of H Shares registered in his/her/its name or otherwise held by him/her/it. 
The placees in the International Offering include the following: 

<<<PAGE 5>>>
5 
 
Cornerstone Investors 
Investor Note 1 
No. of 
Offer 
Shares 
allocated 
% of Offer 
Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)  
% of total 
issued share 
capital after 
the 
Global 
Offering 
(assuming the 
Over-
allotment 
Option is not 
exercised) 
 
Existing 
shareholders 
or 
their close 
associates 
Foresight Global Superior Choice 
SPC — Global Superior Choice 
Fund 1 SP, Foresight Global 
Superior Choice SPC — Vision 
Fund 1 SP, Foresight Global 
Superior Choice SPC — Horizon 
Fund 1 SP, Foresight Global 
Superior Choice SPC — Horizon 
Next Fund SP and Foresight 
International Series — Foresight 
China Equity Fund (collectively, 
“Foresight Funds”)  
2,395,400  
17.61% 
3.25% 
No 
Key Broad Future Limited (凱博
未來有限公司) (“Key Broad”)  
             2,395,400  
17.61% 
3.25% 
No 
LBC HK Opportunity Fund 
Limited (“LBC HK”) 
                479,000  
3.52% 
0.65% 
No 
Sage Partners Master Fund 
(“Sage Partners”) 
                383,200  
2.82% 
0.52% 
No 
Panjing Harbourview Investment 
Fund (盤京港景投資基金) 
(“Panjing Fund”) 
                287,400  
2.11% 
0.39% 
No 
Taikang Life Insurance Co., Ltd. 
(泰康人壽保險有限責任公司)  
(“Taikang Life”) 
                287,400  
2.11% 
0.39% 
No 
Total 
6,227,800 
45.79% 
8.46% 
 
Notes: 
1. For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in 
the Prospectus. 
 
 

<<<PAGE 6>>>
6 
 
Allotees with Consents Obtained 
Investor 
No. of Offer 
Shares 
allocated 
% of Offer Shares 
(assuming the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
share capital after 
the Global 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) 
 
Relationship 
Allotees with consents under paragraph 1C(1) of Appendix F1 to the Listing Rules (the "Placing Guidelines") in 
relation to allocations to connected clients Note 1  
CITIC 
Securities 
International Capital  
Management 
Limited ("CSI") 
213,000  
1.57%  
0.29%  
Connected client as a 
placee 
Shanxi Securities 
International  
Asset Management 
Limited ("SSIAM")  
244,400 
1.80%  
0.33%  
Connected client as a 
placee 
Allottee with consent under paragraph 1C(2) of the Placing Guidelines in relation to allocation to a close associate 
of existing Shareholders  
Wealth Shine Asia 
Pacific Limited 
("Wealth Shine") 
Note 2 
96,800 
0.71%  
0.13%  
A close associate of 
existing 
Shareholders  
Notes:  
1. For details of the consents under paragraph 1C(1) of the Placing Guidelines in relation to allocations to 
connected clients, please refer to the section headed “Others / Additional Information – Placing to connected 
clients with prior consents under paragraph 1C(1) of the Placing Guidelines” in this announcement.  
 
2. Ruiji Phase III Venture Capital Partnership (Limited Partnership) (安義瑞吉三期創業投資合夥企業(有限合
夥)) (“Ruiji Phase III”) and Anyi Ruiji Phase X Venture Capital Partnership Enterprise (Limited Partnership) 
(安義瑞吉十期創業投資合夥企業 (有限合夥) ("Ruiji Phase X") own approximately 1.72% and 1.11%, 
respectively, of the total number of issued Shares of the Company before the Global Offering. Such shareholding 
is expected to be approximately 2.44% immediately following the completion of the Global Offering (and before 
any exercise of the Over-allotment Option), after taking into account the Shares to be subscribed by Wealth Shine 
under the International Offering. For further details, please refer to the section headed " Others / Additional 
Information – Placing to a close associate of existing Shareholders as placee with a prior consent under 
paragraph 1C(2) of the Placing Guidelines" in this announcement.  
 
 
LOCK-UP UNDERTAKINGS  
Controlling Shareholders 
Name 
Number of Shares 
held in the Company 
subject to lock-up 
undertakings 
immediately upon 
Listing 
% of shareholding in 
the Company subject 
to lock-up 
undertakings upon 
Listing (assuming the 
Over-allotment 
Last day subject to the 
lock-up undertakings 
Note 2 

<<<PAGE 7>>>
7 
 
Option is not 
exercised) 
Dr. Ji Jianxin (姬建新) (“Dr. Ji”) 
Note 1 
12,424,624 
16.88% 
June 22, 2027 
Chengdu Wenshao Enterprise 
Management Center (Limited 
Partnership) (成都聞韶企業管理
中心(有限合夥)) (“Chengdu 
Wenshao”) Note 1 
19,971,379 
27.14% 
June 22, 2027 
Suzhou Jishitang Enterprise 
Management Center (Limited 
Partnership) (蘇州積石堂企業管
理中心(有限合夥)) (“Suzhou 
Jishitang”) Note 1 
2,097,440 
2.85% 
June 22, 2027 
Total  
34,493,443 
46.87% 
 
Notes:  
1. Dr. Ji, Chengdu Wenshao and Suzhou Jishitang will be regarded as a group of Controlling Shareholders upon 
Listing. For further details, please refer to “Relationship with our Controlling Shareholders” in the Prospectus. 
 
2. The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law. In 
accordance with the relevant Listing Rules/guidance materials, the required lock-up for existing Shareholders 
ends on June 22, 2027, being 12 months following the Listing Date. 
 
Cornerstone Investors 
Name 
Number of Shares 
held in the 
Company subject to 
lock-up 
undertakings upon 
Listing 
% of shareholding in 
the Company subject 
to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised) 
Last day subject to the 
lock-up undertakings Note 
2 
Foresight Funds 
2,395,400  
3.25% 
December 22, 2026 
Key Broad 
             2,395,400  
3.25% 
December 22, 2026 
LBC HK  
                479,000  
0.65% 
December 22, 2026 
Sage Partners  
                383,200  
0.52% 
December 22, 2026 
Panjing Fund  
                287,400  
0.39% 
December 22, 2026 
Taikang Life 
                287,400  
0.39% 
December 22, 2026 
Total  
6,227,800 
8.46%  

<<<PAGE 8>>>
8 
 
Name 
Number of Shares 
held in the 
Company subject to 
lock-up 
undertakings upon 
Listing 
% of shareholding in 
the Company subject 
to lock-up 
undertakings upon 
Listing (assuming 
the Over-allotment 
Option is not 
exercised) 
Last day subject to the 
lock-up undertakings Note 
2 
Notes:  
1. In accordance with the relevant cornerstone investment agreements, the required lock-up ends on December 
22, 2026. The Cornerstone Investors will cease to be prohibited from disposing of or transferring H Shares 
subscribed for pursuant to the relevant cornerstone investment agreements after the indicated date. 
 
Pre-IPO Investors (as defined in the "History, Development and Corporate Structure" section of the 
Prospectus)  
Name 
Number of shares held in 
the Company subject to 
lock-up undertakings 
upon listing 
% of shareholding in the 
Company subject to lock-up 
undertakings upon listing 
(assuming the Over-
allotment Option is not 
exercised) 
Last day subject to the lock-
up undertakings Note 1 
(SDIC) VC Fund (Shanghai) of 
Technology Transfer and 
Commercialization (Limited 
Partnership) (國投(上海)科技成
果轉化創業投資基金企業(有限
合夥)) 
           5,520,100 
7.50%
June 22, 2027
Suzhou Junlian Xinkang Venture 
Capital Partnership (Limited 
Partnership) (蘇州君聯欣康創
業投資合夥企業(有限合夥)) 
           4,246,253 
5.77%
June 22, 2027
Chongqing Jiangjin District 
Private Equity Investment Fund 
Partnership (Limited 
Partnership) (重慶市江津區私
募股權投資基金合夥企業(有限
合夥)) 
           2,222,218 
3.02%
June 22, 2027
Chongqing Chengyu Tuanjie 
Lake Strategic Emerging 
Industry Private Equity 
Investment Fund Partnership 
(Limited Partnership) (重慶市成
渝團結湖戰略性新興產業私募
1,777,751 
2.42%
June 22, 2027

<<<PAGE 9>>>
9 
 
Name 
Number of shares held in 
the Company subject to 
lock-up undertakings 
upon listing 
% of shareholding in the 
Company subject to lock-up 
undertakings upon listing 
(assuming the Over-
allotment Option is not 
exercised) 
Last day subject to the lock-
up undertakings Note 1 
股權投資基金合夥企業(有限合
夥)) 
Ningbo Huaige Ruixin Venture 
Capital Partnership Enterprise 
(Limited Partnership) (寧波懷格
銳信創業投資合夥企業(有限合
夥)) 
1,617,322 
2.20%
June 22, 2027
Shanghai Junshi Biosciences 
Co., Ltd. (上海君實生物醫藥科
技股份有限公司) 
1,261,749 
1.71%
June 22, 2027
Chengdu Peikun Jingrong 
Venture Capital Partnership 
(Limited Partnership) (成都沛坤
菁蓉創業投資合夥企業(有限合
夥)) 
1,204,357 
1.64%
June 22, 2027
Anyi Ruiji Phase III Venture 
Capital Partnership (Limited 
Partnership) (安義瑞吉三期創
業投資合夥企業(有限合夥)) 
1,032,356 
1.40%
June 22, 2027
Sichuan Science and Technology 
Achievement Transformation 
Equity Investment Fund 
Partnership (Limited 
Partnership) (四川省科技成果
轉化股權投資基金合夥企業(有
限合夥)) 
946,326 
1.29%
June 22, 2027
Xiamen Jianfa Emerging 
Industries Equity Investment 
Partnership No. 2 (Limited 
Partnership) (廈門建發新興產
業股權投資貳號合夥企業(有限
合夥)) 
876,544 
1.19%
June 22, 2027
Zhang Naiye (張乃燁) 
876,544 
1.19%
June 22, 2027
Hefei Xingtai Huike Venture 
Capital Partnership (Limited 
Partnership) (合肥興泰慧科創
業投資合夥企業(有限合夥)) 
666,671 
0.91%
June 22, 2027

<<<PAGE 10>>>
10 
 
Name 
Number of shares held in 
the Company subject to 
lock-up undertakings 
upon listing 
% of shareholding in the 
Company subject to lock-up 
undertakings upon listing 
(assuming the Over-
allotment Option is not 
exercised) 
Last day subject to the lock-
up undertakings Note 1 
Anyi Ruiji Phase X Venture 
Capital Partnership Enterprise 
(Limited Partnership) (安義瑞吉
十期創業投資合夥企業(有限合
夥)) 
666,662 
0.91%
June 22, 2027
Suzhou Yuanju Fanmao 
Investment Partnership 
Enterprise (Limited Partnership) 
(蘇州元聚帆茂投資合夥企業
(有限合夥)) 
606,591 
0.82%
June 22, 2027
Chengdu Chunlei Xingming 
Technology Venture Capital 
Partnership Enterprise (Limited 
Partnership) (成都春壘星溟科
技創業投資合夥企業(有限合
夥)) 
499,997 
0.68%
June 22, 2027
Wuxi Runyuan 
Biopharmaceutical Venture 
Capital Partnership (Limited 
Partnership) (無錫潤元生物醫
藥創業投資合夥企業(有限合
夥)) 
444,467 
0.60%
June 22, 2027
Fuzhou Huace Xinming 
Pharmaceutical Investment 
Partnership Enterprise (Limited 
Partnership) (福州華策新明醫
藥投資合夥企業(有限合夥)) 
444,442 
0.60%
June 22, 2027
Hefei Baohe District Linghang 
Venture Capital Fund 
Partnership Enterprise (Limited 
Partnership) (合肥市包河區領
航創業投資基金合夥企業(有限
合夥)) 
444,442 
0.60%
June 22, 2027
Ningbo Huaige Health 
Investment Management 
Partnership (Limited 
Partnership) (寧波懷格健康投
資管理合夥企業(有限合夥)) 
103,212 
0.14%
June 22, 2027

<<<PAGE 11>>>
11 
 
Name 
Number of shares held in 
the Company subject to 
lock-up undertakings 
upon listing 
% of shareholding in the 
Company subject to lock-up 
undertakings upon listing 
(assuming the Over-
allotment Option is not 
exercised) 
Last day subject to the lock-
up undertakings Note 1 
Chengdu Peikun Songfu 
Technology Partnership (Limited 
Partnership) (成都沛坤宋富科
技合夥企業(有限合夥)) 
48,158 
0.07%
June 22, 2027
Total 
25,506,162 
34.66%
Notes:  
1. The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law. 
 

<<<PAGE 12>>>
12 
 
PLACEE CONCENTRATION ANALYSIS 
 
Placees* Number of 
H Shares 
allotted 
Allotment as % 
of International 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) 
Allotment as % 
of International 
Offering 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares are 
issued) 
Allotment as % 
of total Offer 
Shares (assuming 
the Over-
allotment Option 
is not exercised) 
Allotment as % of 
total Offer Shares 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares are 
issued) 
Number of 
Shares held upon 
Listing  
% of total issued 
share capital 
upon Listing 
(assuming the 
Over-allotment 
Option is not 
exercised)  
% of total issued 
share capital 
upon Listing 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares 
are issued) 
Top 1 
2,395,400  
19.57% 
16.77% 
17.61% 
15.32% 
2,395,400  
3.25% 
3.17% 
Top 5 
7,576,000  
61.90% 
53.05% 
55.71% 
48.44% 
7,576,000  
10.29% 
10.02% 
Top 10 
10,449,000  85.37% 
73.17% 
76.83% 
66.81% 
10,449,000  
14.20% 
13.81% 
Top 25 
13,001,900  106.22% 
91.05% 
95.60% 
83.13% 
14,700,918  
19.97% 
19.44% 
 
Note 
* Ranking of placees is based on the number of H Shares allotted to the placees. 
 
H SHAREHOLDERS CONCENTRATION ANALYSIS 
 
H 
Shareholders* 
Number of H 
Shares 
allotted 
Allotment as 
% of 
International 
Offering 
(assuming the 
Over-
allotment 
Option is not 
exercised) 
Allotment as 
% of 
International 
Offering 
(assuming the 
Over-
allotment 
Option is 
exercised and 
new H Shares 
are issued) 
Allotment as 
% of total 
Offer Shares 
(assuming the 
Over-
allotment 
Option is not 
exercised)  
Allotment as 
% of total 
Offer Shares 
(assuming the 
Over-
allotment 
Option is 
exercised and 
new H Shares 
are issued) 
Number of H 
Shares held 
upon Listing  
% of total 
issued H 
Share capital 
upon Listing 
(assuming the 
Over-
allotment 
Option is not 
exercised) 
% of total 
issued H share 
capital upon 
Listing 
(assuming the 
Over-
allotment 
Option is 
exercised and 
new H Shares 
are issued) 
Number of 
Shares held 
upon Listing 
Top 1 
-    
0.00% 
0.00% 
0.00% 
0.00% 
34,493,443  
46.87% 
45.60% 
34,493,443  
Top 5 
2,395,400  
19.57% 
16.77% 
17.61% 
15.32% 
50,655,165  
68.83% 
66.97% 
50,655,165  
Top 10 
4,887,600  
39.93% 
34.23% 
35.94% 
31.25% 
59,525,648  
80.88% 
78.70% 
59,525,648  
Top 25 
10,545,800  
86.16% 
73.85% 
77.54% 
67.43% 
70,100,963  
95.25% 
92.68% 
70,100,963  
 
Note 
* Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing. 

<<<PAGE 13>>>
13 
 
 
SHAREHOLDER CONCENTRATION ANALYSIS 
  
Shareholders* Number of H 
Shares allotted 
Allotment as 
% of 
International 
Offering 
(assuming the 
Over-allotment 
Option is not 
exercised) 
Allotment as 
% of 
International 
Offering 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares 
are issued) 
Allotment as 
% of total 
Offer Shares 
(assuming the 
Over-allotment 
Option is not 
exercised)  
Allotment as 
% of total 
Offer Shares 
(assuming the 
Over-allotment 
Option is 
exercised and 
new H Shares 
are issued) 
Number of H 
Shares held 
upon Listing  
Number of 
Shares held 
upon Listing 
% of total 
issued Share 
capital upon 
Listing 
(assuming the 
Over-allotment 
Option is not 
exercised) 
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
Top 1 
-    
0.00% 
0.00% 
0.00% 
0.00% 
34,493,443  
34,493,443  
46.87% 
45.60% 
Top 5 
2,395,400  
19.57% 
16.77% 
17.61% 
15.32% 
50,655,165  
50,655,165  
68.83% 
66.97% 
Top 10 
4,887,600  
39.93% 
34.23% 
35.94% 
31.25% 
59,525,648  
59,525,648  
80.88% 
78.70% 
Top 25 
10,545,800  
86.16% 
73.85% 
77.54% 
67.43% 
70,100,963  
70,100,963  
95.25% 
92.68% 
 
Note 
* Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing. 
 
 

<<<PAGE 14>>>
 
14 
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING 
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by the 
public will be conditionally allocated on the basis set out below:  
 
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF 
THE TOTAL NO. 
OF SHARES 
APPLIED FOR 
NO. OF SHARES 
APPLIED FOR 
NO. OF VALID 
APPLICATIONS BASIS OF ALLOTMENT / BALLOT 
POOL A 
100 
81,913 
 1,638 out of 81,913 to receive 100 Shares 
2.00% 
200 
8,450 
 215 out of 8,450 to receive 100 Shares 
1.27% 
300 
4,357 
 128 out of 4,357 to receive 100 Shares 
0.98% 
400 
2,851 
 93 out of 2,851 to receive 100 Shares 
0.82% 
500 
3,371 
 118 out of 3,371 to receive 100 Shares 
0.70% 
600 
12,470 
 467 out of 12,470 to receive 100 Shares 
0.62% 
700 
1,814 
 72 out of 1,814 to receive 100 Shares 
0.57% 
800 
1,076 
 45 out of 1,076 to receive 100 Shares 
0.52% 
900 
874 
 38 out of 874 to receive 100 Shares 
0.48% 
1,000 
8,505 
 381 out of 8,505 to receive 100 Shares 
0.45% 
1,500 
2,514 
 130 out of 2,514 to receive 100 Shares 
0.34% 
2,000 
2,125 
 121 out of 2,125 to receive 100 Shares 
0.28% 
2,500 
1,454 
 90 out of 1,454 to receive 100 Shares 
0.25% 
3,000 
1,418 
 93 out of 1,418 to receive 100 Shares 
0.22% 
3,500 
1,009 
 70 out of 1,009 to receive 100 Shares 
0.20% 
4,000 
1,259 
 92 out of 1,259 to receive 100 Shares 
0.18% 
4,500 
920 
 70 out of 920 to receive 100 Shares 
0.17% 
5,000 
1,991 
 157 out of 1,991 to receive 100 Shares 
0.16% 
6,000 
1,587 
 133 out of 1,587 to receive 100 Shares 
0.14% 
7,000 
1,367 
 121 out of 1,367 to receive 100 Shares 
0.13% 
8,000 
1,191 
 111 out of 1,191 to receive 100 Shares 
0.12% 
9,000 
942 
 91 out of 942 to receive 100 Shares 
0.11% 
10,000 
5,288 
 531 out of 5,288 to receive 100 Shares 
0.10% 

<<<PAGE 15>>>
 
15 
 
20,000 
3,418 
 438 out of 3,418 to receive 100 Shares 
0.06% 
30,000 
2,480 
 366 out of 2,480 to receive 100 Shares 
0.05% 
40,000 
1,710 
 279 out of 1,710 to receive 100 Shares 
0.04% 
50,000 
1,387 
 245 out of 1,387 to receive 100 Shares 
0.04% 
60,000 
2,484 
 467 out of 2,484 to receive 100 Shares 
0.03% 
160,225 
Total number of Pool A successful applicants: 
6,800 
POOL B 
70,000 
4,235 
1,503 out of 4,235 to receive 100 Shares 
0.05% 
80,000 
1,293 
 493 out of 1,293 to receive 100 Shares 
0.05% 
90,000 
748 
 304 out of 748 to receive 100 Shares 
0.05% 
100,000 
2,337 
 1,007 out of 2,337 to receive 100 Shares 
0.04% 
150,000 
1,188 
 638 out of 1,188 to receive 100 Shares 
0.04% 
200,000 
836 
 526 out of 836 to receive 100 Shares 
0.03% 
250,000 
511 
 363 out of 511 to receive 100 Shares 
0.03% 
300,000 
360 
 282 out of 360 to receive 100 Shares 
0.03% 
350,000 
203 
 173 out of 203 to receive 100 Shares 
0.02% 
400,000 
206 
 189 out of 206 to receive 100 Shares 
0.02% 
450,000 
109 
 107 out of 109 to receive 100 Shares 
0.02% 
500,000 
204 
 
100 Shares plus 7 out of 204 to receive additional 
100 Shares 
0.02% 
600,000 
137 
 
100 Shares plus 20 out of 137 to receive 
additional 100 Shares 
0.02% 
680,000 
692 
 
100 Shares plus 155 out of 692 to receive 
additional 100 Shares 
0.02% 
13,059 
Total number of Pool B successful 
applicants: 6,618 
  
As of the date of this announcement, the relevant subscription monies previously deposited in the designated 
nominee accounts have been remitted back to the accounts of all HKSCC participants. Investors should 
contact their relevant brokers for any inquiries. 
 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
The Directors confirm that, except for the Listing Rules in respect of which consents have been 

<<<PAGE 16>>>
 
16 
 
obtained, the Company has complied with the Listing Rules and guidance materials in relation to 
the placing, allotment and listing of the Company’s H Shares. 
 
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees or the 
public (as the case may be) directly or indirectly for each Offer Share subscribed for or purchased by 
them was the same as the Offer Price in addition to any brokerage, AFRC transaction levy, SFC 
transaction levy and Stock Exchange trading fee payable. 
 
OTHERS / ADDITIONAL INFORMATION 
 
Placing to connected clients with prior consents under paragraph 1C(1) of the Placing Guidelines  
 
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, consents 
under paragraph 1C(1) of the Placing Guidelines to permit certain Offer Shares to be placed to 
connected clients of connected distributors under the International Offering pursuant to the Placing 
Guidelines. Details of the placement to connected clients are set out below. The allocation of Offer 
Shares to such connected clients is in compliance with all the conditions under the consents granted 
by the Stock Exchange. Please also refer to the section headed “Allotees with Consents Obtained” in 
this announcement for details.  
 
Connected Clients holding the beneficial interest of the Offer Shares on behalf of independent third 
parties  
 
Connected 
Distributor 
Connected 
Client 
Relationship 
with 
the 
Connected 
Distributor 
Whether the 
connected 
client 
will  
hold 
beneficial 
interests 
of 
Offer Shares 
on 
a-non 
discretionary 
or 
discretionary 
basis 
for 
independent 
third parties 
Number of 
Offer 
Shares to be 
allocated to 
the 
connected 
client 
Appropriate 
percentage 
of 
total 
number 
of 
Offer 
Shares 
(assuming 
the 
Over-
allotment 
Option 
is 
not 
exercised) 
Approximate 
percentage 
of 
total 
issued share 
capital in the 
Company 
upon Listing 
(assuming 
the 
Over-
allotment 
Option is not 
exercised) 
CLSA 
Limited 
(“CLSA”) 
CSI 
CSI 
is 
a 
member 
of 
the 
same 
group 
of 
companies as 
CLSA 
Non-
discretionary 
basis  
213,000 
1.57% 
0.29% 
Shanxi 
Securities 
International 
Limited 
("SSI") Note 2 
SSIAM 
Both SSI and 
SSIAM 
are 
ultimately 
controlled by 
Shanxi 
Discretionary 
basis  
244,400 
1.80% 
0.33% 

<<<PAGE 17>>>
 
17 
 
Connected 
Distributor 
Connected 
Client 
Relationship 
with 
the 
Connected 
Distributor 
Whether the 
connected 
client 
will  
hold 
beneficial 
interests 
of 
Offer Shares 
on 
a-non 
discretionary 
or 
discretionary 
basis 
for 
independent 
third parties 
Number of 
Offer 
Shares to be 
allocated to 
the 
connected 
client 
Appropriate 
percentage 
of 
total 
number 
of 
Offer 
Shares 
(assuming 
the 
Over-
allotment 
Option 
is 
not 
exercised) 
Approximate 
percentage 
of 
total 
issued share 
capital in the 
Company 
upon Listing 
(assuming 
the 
Over-
allotment 
Option is not 
exercised) 
Securities 
International 
Financial 
Holdings 
("SSIFH").  
 
Notes:  
 
(1) CSI will act as the single counterparty of a back-to-back total return swap transaction (the “CSI Back 
to-back TRS”) to be entered into by CSI in connection with a total return swap order (the “CSI Client 
TRS”) placed and fully funded by its ultimate clients (the “CSI Ultimate Client(s)”), by which CSI will 
pass the full economic exposure of the Offer Shares placed to CSI to the CSI Ultimate Clients. CSI will 
hold the beneficial interest of the Offer Shares on behalf of the CSI Ultimate Client on a non-
discretionary basis. The CSI Ultimate Client may exercise an early termination right to early terminate 
the CSI Client TRS at any time from the trade date of the CSI Client TRS which should be on or after 
the date on which the Offer Shares are listed on the Stock Exchange. Upon the final maturity or 
termination of the CSI Client TRS by the CSI Ultimate Client, CSI will dispose of the Offer Shares on 
the secondary market and the CSI Ultimate Client will receive a final termination amount of the CSI 
Back-to-back TRS which should have taken into account all the economic returns or economic loss in 
relation to the Offer Shares and the fixed amount of transaction fees of the CSI Back-to-back TRS and 
the CSI Client TRS. CSI will not exercise the voting right of the Offer Shares during the terms of the 
CSI Back-to-back TRS. CSI is not a collective investment scheme which is not authorized by the SFC, 
or is expected to hold the Offer Shares on behalf of such scheme.  
 
The details of the CSI Ultimate Clients are as follows:  
 
Name of CSI Ultimate 
Client 
Limited Partner/ 
Shareholding 
holding 30% or 
more in the CSI 
Ultimate Clients 
Fund Manager/ 
General Partner 
Ultimate beneficial 
owners of Fund 
Manager / General 
Partner 
Liangpai Exclusive Fund 
No. 43 Private Securities 
Investment Fund (量派
專享四十三號私募證券
投資基金) 
Sun Lin (孫林) 
Shanghai QuantPi 
Investment Limited 
(上海量派投資管理有限
公司) 
Sun Lin (孫林) and Yu 
Hang (余航) 
Canaan China Flagship 
Fund 
Liang Hao 
N/A 
N/A 
Hover4pi Fund I OFC 
N/A 
Hover4pi Capital 
He Hui  

<<<PAGE 18>>>
 
18 
 
Name of CSI Ultimate 
Client 
Limited Partner/ 
Shareholding 
holding 30% or 
more in the CSI 
Ultimate Clients 
Fund Manager/ 
General Partner 
Ultimate beneficial 
owners of Fund 
Manager / General 
Partner 
Management 
Tongyi Taoli No. 1 
Private Securities 
Investment Fund (通怡
桃李1號私募證券投資
基金) 
Wang Jing (王靜) 
Shanghai Tongyi 
Investment Management  
Co., Ltd. (上海通怡投資
管理有限公司) 
Chu Yibo (儲貽波) 
Tongyi Taoli No. 10 
Private Securities 
Investment Fund (通怡
桃李10號私募證券投資
基金) 
N/A 
Shanghai Tongyi 
Investment Management  
Co., Ltd. (上海通怡投資
管理有限公司) 
Chu Yibo (儲貽波) 
Heyi Xuehu No. 1 
Private Securities 
Investment Fund (合易
雪湖1號私募證券投資
基金) 
N/A 
Beijing Heyi Yingtong 
Asset Management Co., 
Ltd (北京合易盈通資產
管理有限公司) 
Liu Zhe (劉喆) and Liu 
Yang (劉洋) 
Evolution Darwin 
Shangshan No. 3 Private 
Securities Investment 
Fund (進化論達爾文上
善三號私募證券投資基
金) 
N/A 
Hainan Evolution Asset 
Management Co., LTD (海
南進化論私募基金管理
有限公司) 
Wang Yiping (王一平) 
Heijing Capital 
Management Co., Ltd. 
(黑晶資本管理有限公
司) 
Li Chuxin (李出新) 
and Shao Yukai (邵
宇開) 
N/A 
N/A 
 
To the best knowledge of CSI and after making all reasonable enquiries, each of the CSI Ultimate 
Clients is an independent third party of the Company, its subsidiaries and substantial shareholders, 
CSI, CLSA and the companies which are members of the same group of CLSA. 
 
(2) SSI is a non-syndicate distributor in relation to the Global Offering. In relation to the subscription, 
SSIAM shall hold the Offer Shares in its capacity as the discretionary fund manager on behalf of its 
investor holding over 30% interest (the "SSIAM Ultimate Client"). SSIAM is not a collective 
investment scheme which is not authorised by the SFC or is expected to hold the Offer Shares on 
behalf of such scheme. The SSIAM Ultimate Client is Zeng Jinjing (曾金晶). To the best knowledge 
of SSIAM, the SSIAM Ultimate Client is an independent third party of the Company, its subsidiaries, 
its substantial shareholders, SSIFH and the companies which are members of the same group of 
companies as SSIFH.  
 
Placing to a close associate of existing Shareholders as placee with a prior consent under 
paragraph 1C(2) of the Placing Guidelines 
 
The Company has applied to the Stock Exchange, and the Stock Exchange has granted, a consent under 
paragraph 1C(2) of the Placing Guidelines to permit the Company to allocate such Offer Shares in the 
International Offering to Wealth Shine, a close associate of Ruiji Phase III and Ruiji Phase X (the 
"Existing Shareholders"), each an existing Shareholder, on the following grounds which are 
consistent with the conditions as set out in Paragraph 18 of Chapter 2.3 and Chapter 4.15 of the Guide 

<<<PAGE 19>>>
 
19 
 
for New Listing Applicant: 
 
(1) the Company will comply with the public float requirement under Rule 19A.13A of the Listing 
Rules and the free float requirement under Rule 19A.13C of the Listing Rules;  
 
(2) no preference in allocation has been, nor will be, given to Wealth Shine as a placee by virtue 
of being a close associate of the Existing Shareholders in any allocation in the placing tranche 
of the Global Offering;  
 
(3) each of the Company, the Sole Sponsor and the Sole Overall Coordinator has provided the 
Stock Exchange with written confirmations in accordance with Chapters 2.3 and 4.15 of the 
Guide; and  
 
(4) the relevant information in respect of the allocation to Wealth Shine as a placee has been 
disclosed in this allotment results announcement.  
 
Such allocation of Offer Shares is in compliance with all the conditions under the consent granted by 
the Stock Exchange. 
 
 

<<<PAGE 20>>>
 
20 
 
DISCLAIMERS 
 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and Hong 
Kong Securities Clearing Company Limited take no responsibility  for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement. 
This announcement is not for release, publication, distribution, directly or indirectly, in or into the 
United States (including its territories and possessions, any state of the United States and the District 
of Columbia). This announcement does not constitute or form a part of any offer or solicitation to 
purchase or subscribe for securities in the United States. The securities mentioned herein have not 
been, and will not be, registered under the United States Securities Act of 1933, as amended (the 
“U.S. Securities Act”). The securities may not be offered or sold in the United States except pursuant 
to an exemption from the registration requirements of the U.S. Securities Act and in compliance with 
any applicable state securities laws, or outside the United States unless in compliance with 
Regulation S under the U.S. Securities Act. There will be no public offer of securities in the United 
States. 
The Offer Shares are being offered and sold outside the United States in offshore transactions in 
reliance on Regulation S under the U.S. Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or offer to 
acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated June 12, 2026 issued by HJ Science Co., Ltd. for detailed 
information about the Global Offering described below before deciding whether or not to invest in 
the H Shares thereby being offered. 
*Potential investors of the Offer Shares should note that the Sole Sponsor and the Sole Overall 
Coordinator (acting in such capacity and as the Underwriter and the Capital Market Intermediary) 
shall be entitled to terminate their obligations under the Hong Kong Underwriting Agreement with 
immediate effect upon the occurrence of any of the events set out in the section headed 
“Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — 
Hong Kong Underwriting Agreement — Grounds for Termination” in the Prospectus at any time 
prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on June 
23, 2026). 

<<<PAGE 21>>>
21
PUBLIC FLOAT AND FREE FLOAT
Immediately after the completion of the Global Offering (before any exercise of the Over-allotment 
Option), an aggregate of 39,106,162 H Shares, representing 53.13% of the total issued Shares upon 
the Listing which is higher than the prescribed percentage of H Shares required to be held in public 
hands of 25% under Rule 19A.13A(1) of the Listing Rules, will be counted towards the public 
float. Hence, the Company will be able to comply with Rule 19A.13A(1) of the Listing Rules.
Pursuant to the applicable PRC law, within the 12 months following the Listing Date, all existing 
Shareholders (including the Pre-IPO Investors) cannot dispose of any of the Shares held by them. 
Pursuant to the relevant cornerstone investment agreements, each Cornerstone Investor has agreed 
to a lock-up period of six months following the Listing Date. As such, the H Shares held by the 
existing Shareholders and the Cornerstone Investors upon the Listing shall not be counted towards 
the free float of the H Shares of the Company at the time of Listing. Based on the Offer Price of 
HK$81.80 per Offer Share, the expected market value of the H Shares held by the public and not 
subject to disposal restrictions exceeds HK$600,000,000. Therefore, the Company will comply 
with the free float requirement under Rule 19A.13C(1)(b) of the Listing Rules.
The Directors confirm that, immediately following completion of the Global Offering (assuming 
the Over-allotment Option is not exercised): (i) no placee will, individually, be placed more than 
10% of the enlarged issued share capital of the Company immediately after the Global Offering; 
(ii) there will not be any new substantial Shareholder under the Listing Rules immediately after the
Global Offering; (iii) the three largest public shareholders of the Company do not hold more than
50% of the H shares in public hands at the time of the Listing in compliance with Rules 8.08(3)
and 8.24 of the Listing Rules; and (iv) there will be at least 300 Shareholders at the time of the
Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, June 
23, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting – Underwriting Arrangements 
and Expenses – Hong Kong Public Offering – Hong Kong Underwriting Agreement – Grounds for 
Termination” in the Prospectus has not been exercised. Investors who trade the H Shares on the 
basis of publicly available allocation details prior to the receipt of H Share certificates or prior to 
the H Share certificates becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Tuesday, June 
23, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. on Tuesday, June 23, 2026 (Hong Kong time). The H Shares will be 
traded in board lots of 100 H Shares each, and the stock code of the H Shares will be 6132.
By order of the Board
HJ Science Co., Ltd.
Dr. Ji Jianxin
Executive Director, chairman of the Board, 
chief executive officer and general manager
Hong Kong, June 22, 2026
As at the date of this announcement, the executive Directors are Dr. Ji Jianxin, Mr. Yang Xiangyu, 
Mr. Wu Zhen and Ms. Zhang Yao; the non-executive Directors are Ms. Geng Xueli, Mr. Du 
Jiangbo, Mr. Wang Junfeng and Mr. Zhang Zhiyong; and the independent non-executive Directors 
are Mr. Wong Jovi Chi Wing, Mr. Jiang He, Ms. Lin Fangzhu and Mr. Liu Zhe.
