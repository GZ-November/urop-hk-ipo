# 配发结果公告抽取任务：2493.HK Mabwell (Shanghai) Bioscience Co., Ltd. - B - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**27/04/2026 22:08**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0427/2026042703128.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2493.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
 
MABWELL (SHANGHAI) BIOSCIENCE CO., LTD. / 邁威（上海）生物科技股份有
限公司 
ANNOUNCEMENT OF FINAL OFFER PRICE AND  
ALLOTMENT RESULTS 
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings 
as those defined in the prospectus dated April 20, 2026 (the “Prospectus”) issued by Mabwell (Shanghai) 
Bioscience Co., Ltd. (the “Company”).  
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares could move 
substantially even with a small number of H Shares traded and should exercise extreme caution when 
dealing in the H Shares. 
 
SUMMARY  
 
Company information 
Stock code  
2493 
Stock short name  
MABWELL-B 
Dealings commencement date  
April 28, 2026* 
*see note at the end of the announcement  
Price Information  
Final Offer Price  
HK$27.64   
Offer Price Range 
HK$27.64 – HK$30.71 
Offer Shares and Share Capital 
Number of Offer Shares 
47,130,200 H Shares 
Final Number of Offer Shares in Hong Kong Public 
Offering 
4,713,200 H Shares 
Final Number of Offer Shares in International Offering 
42,417,000 H Shares 
Number of issued shares upon Listing 
446,730,200 Shares 
Proceeds 
Gross proceeds (Note)  
HK$ 1,302.7 million 
Less: Estimated listing expenses payable based on Final 
Offer Price  
HK$ (113.6) million 
Net proceeds  
HK$ 1,189.0 million 
Note: Gross proceeds refers to the amount to which the Company is entitled to receive. For details of the 
use of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.  
 
ALLOTMENT RESULTS DETAILS 
HONG KONG PUBLIC OFFERING 
 
No. of valid applications  
126,378 
No. of successful applications  
14,808 
Subscription level  
481.71 times 
Reallocation 
No  
No. of Offer Shares initially available under the Hong Kong Public 
Offering 
4,713,200 
No. of Offer Shares reallocated from the International Offering 
0 
Final no. of Offer Shares under the Hong Kong Public Offering 
4,713,200 

<<<PAGE 2>>>
 
 
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering 
10.00% 
 
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
www.hkeipo.hk/IPOResult to perform a search by name or identification number or www.hkeipo.hk/IPOResult 
for the full list of allottees. 
INTERNATIONAL OFFERING 
 
No. of placees  
82 
Subscription Level 
3.46 times  
No. of Offer Shares initially available under the International 
Offering 
42,417,000 
Final no. of Offer Shares under the International Offering  
42,417,000 
% of Offer Shares under the International Offering to the Global 
Offering 
90.00% 
 
The Directors confirm that, to the best of their knowledge, information and belief, save for (a) a waiver from 
strict compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 1C(2) of Appendix F1 
to the Listing Rules (the "Placing Guidelines") granted by the Stock Exchange to permit H Shares in the 
International Offering to be placed to certain existing minority Shareholders who (i) hold less than 5% of the 
voting rights in the Company prior to the completion of the Global Offering and (ii) are not and will not become 
(upon the completion of the Global Offering) core connected persons of the Company or the close associates 
of any such core connected person (the "Permitted Existing Shareholders"), and (b) a waiver from strict 
compliance with the requirements under Rules 9.09(b) and 10.03 of the Listing Rules, and a written consent 
under paragraph 1C(2) of Appendix F to the Listing Rules, granted by the Stock Exchange to allow Charm 
Harvest International Limited ("CHIL"), a wholly-owned limited liability company of the Controlling 
Shareholder and executive Director, Mr. Tang, being a close associate of Mr. Tang and a core connected 
person of the Company, to participate as a cornerstone investor in the Global Offering to subscribe for H 
Shares to be issued by the Company under the International Offering, (i) none of the Offer Shares subscribed 
by the placees and the public have been financed directly or indirectly by the Company, any of the Directors, 
chief executive of the Company, substantial Shareholders, existing Shareholders of the Company or any of its 
subsidiaries or their respective close associates; and (ii) none of the placees and the public who have 
purchased the Offer Shares are accustomed to taking instructions from the Company, any of the Directors, 
chief executive of the Company, substantial Shareholders, existing Shareholders of the Company or any of its 
subsidiaries or their respective close associates in relation to the acquisition, disposal, voting or other 
disposition of H Shares registered in his/her/its name or otherwise held by him/her/it. 
The placees in the International Offering include the following: 
Cornerstone Investors 
Investor 
No. of 
Offer 
Shares 
allocated 
% of total 
issued H Shares after 
the Global 
Offering Note 1 
% of total 
issued share 
capital after the 
Global Offering 
 
Existing 
shareholders or 
their close 
associates 
Junshi Hong Kong 
Limited ( 香港君實
有限公司) Note 2 
5,668,200  
12.03% 
1.27% 
No 

<<<PAGE 3>>>
 
Investor 
No. of 
Offer 
Shares 
allocated 
% of total 
issued H Shares after 
the Global 
Offering Note 1 
% of total 
issued share 
capital after the 
Global Offering 
 
Existing 
shareholders or 
their close 
associates 
Sanjin International 
Co., Ltd. Note 2  
4,251,200 
9.02% 
0.95% 
No 
Guohui 
(HK) 
Holdings 
Co., 
Limited (國惠(香港)
控股有限公司) Note 2 
1,983,800 
4.21% 
0.44% 
No 
CHIL Note 2 
1,983,800 
4.21% 
0.44% 
Yes 
WuXi 
Biologics 
HealthCare Venture 
Note 2 
850,200 
1.80% 
0.19% 
No 
Splendid 
Zhonghe 
(Tianjin) Investment 
Management 
Co., 
Ltd. (錦繡中和( 天
津)投資管理有限公
司) Note 2 
283,400 
0.60% 
0.06% 
No 
Total 
15,020,600 
31.87% 
3.36% 
 
Notes: 
1. The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be 
issued under the Global Offering. 
2. For further details of the Cornerstone Investors, please refer to the section headed “Cornerstone Investors” in 
the Prospectus. 
 
 
Allottees with Waivers/Consents Obtained 
Investor 
No. of Offer 
Shares 
allocated 
% of total issued H 
Shares after the Global 
OfferingNote 4 
% of total issued 
share capital after 
the Global 
OfferingNote 5  
 
Relationship* 
Allotees with waiver from strict compliance with Rule 10.03 of the Listing Rules and consent under paragraph 
1C(2) of the Placing Guidelines in relation to subscription for H Shares by a core connected person of the Company 
as a cornerstone investorNote 1 
CHIL 
1,983,800 
4.21% 
0.44% 
CHIL is a core 
connected person 
of the Company 
and 
a 
close 
associate of an  
existing 
shareholder of the 
Company  
Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 
1C(2) of the Placing Guidelines in relation to subscription for H Shares by existing minority Shareholders 
immediately prior to the completion of the Global OfferingNote 2 
 E Fund Management 
Co., Ltd. (易方達基
金管理有限公司) 
1,769,400 
3.75%  
0.40%  
E 
Fund 
Management is an 
existing 
shareholder of the 
Company 

<<<PAGE 4>>>
 
Investor 
No. of Offer 
Shares 
allocated 
% of total issued H 
Shares after the Global 
OfferingNote 4 
% of total issued 
share capital after 
the Global 
OfferingNote 5  
 
Relationship* 
("E 
Fund 
Management") 
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations to connected clientsNote 3 
CITIC 
Securities 
International Capital 
Management Limited 
(“CSI”) 
485,200 
1.03%  
0.11%  
A connected client 
of CLSA Limited 
(“CLSA”) as a 
placee 
CITIC Securities  
Asset Management  
Company Limited  
(“CITIC Asset  
Management”) 
36,000 
0.08%  
0.01%  
A connected client 
of CLSA as a 
placee 
CITIC Securities  
Asset Management  
(HK) Limited  
(“CITIC Asset  
Management HK”) 
2,339,600  
4.96%  
0.52%  
A connected client 
of CLSA as a 
placee 
Guotai 
Junan 
Investments 
(Hong 
Kong) 
Limited 
(“GTJAI”) 
36,000 
0.08%  
0.01%  
A connected client 
of 
Haitong 
International 
Securities 
Company Limited 
(“HTI”) 
as 
a 
placee 
ABCI 
Asset 
Management Limited 
(“ABCI AM”) 
198,600 
0.42%  
0.04%  
A connected client 
of ABCI Capital 
Limited 
(“ABCI 
Capital”)and 
ABCI 
Securities 
Company Limited 
(ABCI Securities, 
together 
with 
ABCI 
Capital, 
“ABCI”) 
as 
a 
placee 
E Fund Management 
1,769,400 
3.75% 
0.40% 
A connected client 
of GF Securities 
(Hong 
Kong) 
Brokerage as a 
placee 
 
Notes:  
1. 
The Company has applied for, and the Stock Exchange has granted, a waiver from strict compliance with the requirements 
under Rule 10.03 of the Listing Rules and consent under Paragraph 1C(2) of the Placing Guidelines to allow CHIL , a 
core connected person of the Company and a close associate of an existing shareholder of the Company to participate as 
a cornerstone investor in the Global Offering to subscribe for the H Shares to be issued by the Company under the 
International Offering. 

<<<PAGE 5>>>
 
2. 
The Company has applied for, and the Stock Exchange has granted, a waiver from strict compliance with the requirements 
under Rule 10.04 of the Listing Rules and consent under Paragraph 1C(2) of the Placing Guidelines to permit H Shares 
in the International Offering to be placed to certain existing minority Shareholders and/or their close associates. Please 
refer to the section headed “Waivers and Exemptions — Allocation of H Shares to existing minority Shareholders and 
their Close Associates” of the Prospectus for details. The Stock Exchange granted the waiver on the condition that, among 
others, details of the allocation to the existing minority Shareholders of the Company immediately prior to the completion 
of the Global Offering will be disclosed in the Prospectus and/or allotment results announcement. 
3. 
For details of the consents under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New 
Listing Applicants in relation to allocations to connected clients, please refer to the section headed “Others/Additional 
Information — Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines” in 
this announcement. 
4. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued 
under the Global Offering.  
5. 
Only taking into account the H Shares allocated to the relevant investors under the Global Offering. 
 
 
LOCK-UP UNDERTAKINGS  
Controlling Shareholders 
Name 
Number of 
Shares held in 
the Company 
subject to lock-
up 
undertakings 
immediately 
upon Listing 
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing Note 3 
% of shareholding 
in the Company 
subject to lock-up 
undertakings 
upon Listing 
Last day subject to 
the lock-up 
undertakings Note 2 
Langrun Equity 
140,560,000 
— 
31.46% 
October 27, 2026 
(First Six Month 
Period) Note 1 
April 27, 2027 
(Second Six Month 
Period) Note 2 
Zhongjun 
Jianlong 
20,000,000 
— 
4.48% 
October 27, 2026 
(First Six Month 
Period) Note 1 
April 27, 2027 
(Second Six Month 
Period) Note 2 
Zhenzhu 
Investment 
6,800,000 
— 
1.52% 
October 27, 2026 
(First Six Month 
Period) Note 1 

<<<PAGE 6>>>
 
April 27, 2027 
(Second Six Month 
Period) Note 2 
Langrun 
Investment 
Consultancy 
2,000,000 
— 
0.45% 
October 27, 2026 
(First Six Month 
Period) Note 1 
April 27, 2027 
(Second Six Month 
Period) Note 2 
Notes:  
1. 
The Controlling Shareholders may dispose of or transfer Share after the indicated date subject to that the Controlling 
Shareholders will not cease to be a Controlling Shareholder. 
 
2. 
The Controlling Shareholders will cease to be prohibited from disposing or transferring Shares after the indicated date. 
 
3. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under 
the Global Offering. 
 
4. 
Langrun Equity is a limited partnership, owned as to approximately 79.92% by Mr. Tang (being an executive Director), 
19.98% by Ms. Chen, spouse of Mr. Tang, each as a limited partner, and 0.10% by Langrun Investment Consultancy, which 
is also its sole general partner. Langrun Investment Consultancy is in turn owned by Mr. Tang and Ms. Chen as to 88.30% 
and 11.70%, respectively. Each of Zhongjun Jianlong and Zhenzhu Investment is an Employee Incentive Platform and a 
limited partnership controlled by Mr. Tang by virtue of his position as their respective sole general partner. Therefore, Mr. 
Tang and Ms. Chen, through Langrun Equity, Zhongjun Jianlong, Zhenzhu Investment and Langrun Investment Consultancy, 
each being a Controlling Shareholder, controlled in aggregate approximately 42.38% of our total issued share capital and 
constituted a group of Controlling Shareholders for the purpose of the Listing Rules immediately prior to the Global Offering. 
 
 
Cornerstone Investors 
Name 
Number of H 
Shares held in 
the Company 
subject to lock-
up 
undertakings 
upon Listing 
% of total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing Note 1 
% of shareholding in 
the Company subject 
to lock-up 
undertakings upon 
Listing 
Last day subject to 
the lock-up 
undertakings Note 2 
Junshi Hong 
Kong Limited Note 
2 
5,668,200  
12.03% 
1.27% October 27, 2026 
Sanjin 
International Co., 
Ltd. Note 2 
4,251,200 
9.02% 
0.95% October 27, 2026 
Guohui (HK) 
Holdings Co., 
Limited Note 2 
1,983,800 
4.21% 
0.44% October 27, 2026 

<<<PAGE 7>>>
 
Name 
Number of H 
Shares held in 
the Company 
subject to lock-
up 
undertakings 
upon Listing 
% of total issued H 
Shares after the 
Global Offering 
subject to lock-up 
undertakings upon 
Listing Note 1 
% of shareholding in 
the Company subject 
to lock-up 
undertakings upon 
Listing 
Last day subject to 
the lock-up 
undertakings Note 2 
CHIL Note 2 
1,983,800 
4.21% 
0.44% October 27, 2026 
WuXi Biologics 
HealthCare 
Venture Note 2 
850,200 
1.80% 
0.19% October 27, 2026 
Splendid 
Zhonghe 
(Tianjin) 
Investment 
Management Co., 
Ltd. Note 2 
283,400 
0.60% 
0.06% October 27, 2026 
Notes:  
1. 
The number of H Shares immediately after the Global Offering is the same as the number of Offer Shares to be issued under 
the Global Offering. 
2. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on October 27, 2026. The 
Cornerstone Investors will cease to be prohibited from disposing of or transferring H Shares subscribed for pursuant to the 
relevant cornerstone investment agreements after the indicated date. 
 
 

<<<PAGE 8>>>
 
PLACEE CONCENTRATION ANALYSIS 
 
 
Placees 
Number of 
H Shares 
allotted 
 
Allotment as % of 
International Offering 
Allotment as % of 
total Offer Shares 
Number of Shares held 
upon Listing 
 
% of total issued share 
capital upon Listing  
Top 1 
5,668,200 
13.36% 
12.03% 
5,668,200 
1.27% 
Top 5 
17,314,800 
40.82% 
36.74% 
17,314,800 
3.88% 
Top 10 
26,020,000 
61.34% 
55.21% 
204,068,824 
45.68% 
Top 25 
37,184,800 
87.66% 
78.90% 
216,059,975 
48.36% 
 
Note 
* Ranking of placees is based on the number of H Shares allotted to the placees. 
 
H SHAREHOLDERS CONCENTRATION ANALYSIS 
 
H 
Shareholders* 
Number 
of 
H Shares 
allotted 
 
 
Allotment as % of 
 International 
Offering 
Allotment as % of total 
Offer Shares 
Number of H Shares held 
upon Listing 
 
% of total issued H Shares 
capital upon Listing 
Number 
of 
Shares 
held 
upon 
Listing 
Top 1 
5,668,200 
13.36% 
12.03% 
5,668,200 
12.03% 
5,668,200 
Top 5 
17,314,800 
40.82% 
36.74% 
17,314,800 
36.74% 
17,314,800 
Top 10 
26,020,000 
61.34% 
55.21% 
26,020,000 
55.21% 
204,068,824 
Top 25 
37,184,800 
87.66% 
78.90% 
37,184,800 
78.90% 
216,059,975 
 
Note 

<<<PAGE 9>>>
 
* Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing. 
 
SHAREHOLDER CONCENTRATION  ANALYSIS 
Shareholders 
Number of 
H Shares 
allotted 
Allotment as % of 
 International 
Offering 
Allotment as % of 
total Offer Shares 
Number of H Shares 
held upon Listing 
 Number of
Shares
held upon
Listing
% of total issued
share capital upon
Listing
Top 1 
1,983,800 
4.68% 
4.21% 
1,983,800 
171,343,800 
38.36% 
Top 5 
3,753,200 
8.85% 
7.96% 
3,753,200 
213,420,791 
47.77% 
Top 10 
13,672,600 
32.23% 
29.01% 
13,672,600 
238,569,538 
53.40% 
Top 25 
26,529,400 
62.54% 
56.29% 
26,529,400 
272,135,520 
60.92% 
 
Note 
* Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing. 
 
 

<<<PAGE 10>>>
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING 
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by the 
public will be conditionally allocated on the basis set out below:  
 
Approximate 
Pool A 
percentage 
allotted of the 
 Number   
 Number  
total number of 
 of H Shares  
 of valid  
H Shares 
applied 
 applied for  
 applications  
Basis of allocation/ballot 
for 
200 
71,153 
 
712 out of 71,153 applicants to receive 200 H Shares 
1.00% 
400 
7,340 
130 out of 7,340 applicants to receive 200 H Shares 
0.89% 
600 
4,151 
99 out of 4,151 applicants to receive 200 H Shares 
0.79% 
800 
2,234 
67 out of 2,234 applicants to receive 200 H Shares 
0.75% 
1,000 
3,187 
114 out of 3,187 applicants to receive 200 H Shares 
0.72% 
1,200 
973 
 
41 out of 973 applicants to receive 200 H Shares 
0.70% 
1,400 
821 
39 out of 821 applicants to receive 200 H Shares 
0.68% 
1,600 
3,475 
184 out of 3,475 applicants to receive 200 H Shares 
0.66% 
1,800 
623 
 
36 out of 623 applicants to receive 200 H Shares 
0.64% 
2,000 
5,903 
 
372 out of 5,903 applicants to receive 200 H Shares 
0.63% 
3,000 
3,287 
286 out of 3,287 applicants to receive 200 H Shares 
0.58% 
4,000 
1,902 
 
214 out of 1,902 applicants to receive 200 H Shares 
0.56% 
5,000 
1,243 
159 out of 1,243 applicants to receive 200 H Shares 
0.51% 
6,000 
1,206 
178 out of 1,206 applicants to receive 200 H Shares 
0.49% 
7,000 
869 
 
145 out of 869 applicants to receive 200 H Shares 
0.48% 
8,000 
732 
136 out of 732 applicants to receive 200 H Shares 
0.46% 
9,000 
515 
105 out of 515 applicants to receive 200 H Shares 
0.45% 
10,000 
2,957 
 
652 out of 2,957 applicants to receive 200 H Shares 
0.44% 
20,000 
2,206 
 
841 out of 2,206 applicants to receive 200 H Shares 
0.38% 
30,000 
1,518 
798 out of 1,518 applicants to receive 200 H Shares 
0.35% 
40,000 
1,170 
 
796 out of 1,170 applicants to receive 200 H Shares 
0.34% 
50,000 
886 
731 out of 886 applicants to receive 200 H Shares 
0.33% 
60,000 
799 
745 out of 799 applicants to receive 200 H Shares 
0.31% 
70,000 
574 
 
200 H Shares 
0.29% 
80,000 
483 
200 H Shares plus 66 out of 483 applicants to receive an 
additional 200 H Shares 
0.28% 
90,000 
255 
200 H Shares plus 60 out of 255 applicants to receive an 
additional 200 H Shares 
0.27% 
100,000 
2,094 
200 H Shares plus 671 out of 2,094 applicants to receive 
an additional 200 H Shares 
0.26% 
 Total   
           
122,556  
Total number of Pool A successful applicants: 10,986 
Pool B 
Approximate 
percentage 

<<<PAGE 11>>>
 
allotted of the 
 Number   
 Number  
total number of 
 of H Shares  
 of valid  
H Shares 
applied 
 applied for  
 applications  
Basis of allocation/ballot 
for 
200,000 
2,197 
 
400 H Shares 
0.20% 
300,000 
428 
400 H Shares plus 339 out of 428 applicants to receive 
an additional 200 H Shares 
0.19% 
400,000 
311 
600 H Shares 
0.15% 
500,000 
162 
 
600 H Shares plus 122 out of 162 applicants to receive 
an additional 200 H Shares 
0.15% 
600,000 
132 
800 H Shares 
0.13% 
700,000 
109 
800 H Shares plus 77 out of 109 applicants to receive an 
additional 200 H Shares 
0.13% 
800,000 
75 
 
1,000 H Shares 
0.13% 
900,000 
51 
1,000 H Shares plus 31 out of 51 applicants to receive 
an additional 200 H Shares 
0.12% 
1,000,000 
188 
1,200 H Shares 
0.12% 
2,000,000 
36 
 
2,000 H Shares 
0.10% 
2,356,600 
133 
2,200 H Shares 
0.09% 
 Total   
               
3,822  
Total number of Pool B successful applicants: 3,822 
 
As of the date of this announcement, the relevant subscription monies previously deposited in the designated 
nominee accounts have been remitted back to the accounts of all HKSCC participants. Investors should 
contact their relevant brokers  for any inquiries. 
 
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of which 
consent has been obtained, the Company has complied with the Listing Rules and guidance materials 
in relation to the placing, allotment and listing of the Company’s H Shares. 
 
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees or the 
public (as the case may be) directly or indirectly for each Offer Share subscribed for or purchased by 
them was the same as the final Offer Price in addition to any brokerage, AFRC transaction levy, SFC 
transaction levy and Stock Exchange trading fee payable. 
 
OTHERS / ADDITIONAL INFORMATION 
 
Allocation of H shares to existing minority shareholders and their close associates 
The Company has applied for, and the Stock Exchange has granted, a waiver from strict compliance 
with Rule 10.04 of, and a consent under paragraph 1C(2) of Appendix F1 to the Listing Rules to permit 
H Shares in the International Offering to be placed to Permitted Existing Shareholders, subject to the 
following conditions:  
 

<<<PAGE 12>>>
 
a) each Permitted Existing Shareholder to whom our Company may allocate the H Shares under 
the International Offering holds less than 5% of the voting rights in our Company prior to the 
completion of the Global Offering;  
b) each Permitted Existing Shareholder is not, and will not be, a core connected person of our 
Company or any close associate of any such core connected person immediately prior to or 
following the Global Offering;  
c) none of the Permitted Existing Shareholders has the power to appoint any Directors nor have 
any other special rights in our Company;  
d) allocation to the Permitted Existing Shareholders and their close associates will not affect our 
Company’s ability to satisfy the public float requirement as prescribed under the requirements 
of Rule 8.08(1)(b) of the Listing Rules;  
e) to the best knowledge and belief of our Company and the Joint Sponsors, and based on 
discussions between our Company and the Overall Coordinators and confirmations required to 
be submitted to the Stock Exchange by the Joint Sponsors, we will confirm to the Stock 
Exchange that: a. in case of participation as cornerstone investors, no preferential treatment has 
been, nor will be, given to the Permitted Existing Shareholders and/or their close associates by 
virtue of their relationship with our Company, other than the preferential treatment of assured 
entitlement under a cornerstone investment following the principles set out in Chapter 4.15 of 
the Guide for New Listing Applicants, and the Permitted Existing Shareholders’ cornerstone 
investment agreements do not contain any material terms which are more favorable to the 
Permitted Existing Shareholders than those in other cornerstone investment agreements; or b. 
in case of participation as placees, no preferential treatment will be given to the Permitted 
Existing Shareholders and/or their close associates in the allocation process by virtue of their 
relationship with our Company;  
f) in the case of participation as placees, the Overall Coordinators will confirm to the Stock 
Exchange that, to the best of their knowledge and belief, no preferential treatment has been, 
nor will be, given to any of the Permitted Existing Shareholders or their close associates by 
virtue of their relationship with our Company in any allocation in the International Offering; 
and  
g) the Joint Sponsors will confirm to the Stock Exchange that based on (i) their discussions with 
our Company and the Overall Coordinators; and (ii) the confirmations provided to the Stock 
Exchange by our Company and the Overall Coordinators, and to the best of their knowledge 
and belief, they have no reason to believe that the Permitted Existing Shareholders and/or their 
close associates received any preferential treatment in the allocation process either as 
cornerstone investors or as placees by virtue of their relationship with our Company, other than, 
in the case of participation as cornerstone investors, the preferential treatment of assured 
entitlement under a cornerstone investment following the principles set out in Chapter 4.15 of 
the Guide for New Listing Applicants, and details of allocation to the Permitted Existing 
Shareholders and/or their close associates will be disclosed in this Prospectus (for cornerstone 
investors) and allotment results announcement (for both cornerstone investors and placees) of 
our Company. 
 
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted 
by the Stock Exchange. 
 
For details of the allocations of Offer Shares to existing Shareholders and/or their close associates, 
please refer to the section headed “Allotment Results Details — International Offer — Allottees with 
Waivers/Consents Obtained” in this announcement. 

<<<PAGE 13>>>
 
 
Cornerstone subscription by a core connected person during the listing application process 
The Company has applied for a waiver from strict compliance with the requirements under Rules 
9.09(b) and Rule 10.03 of the Listing Rules, and a written consent under paragraph 1C(2) of Appendix 
F to the Listing Rules, to allow CHIL, a wholly-owned limited liability company of our Controlling 
Shareholder and executive Director, Mr. Tang, to participate as a cornerstone investor in the Global 
Offering to subscribe for the H Shares to be issued by the Company under the International Offering 
(the “Proposed Cornerstone Investment”). CHIL is a close associate of Mr. Tang and a core 
connected person of the Company. 
 
The Stock Exchange has granted the requested waiver and consent subject to the conditions that:  
a) we will comply with (i) the public float requirement under Rule 19A.13A(2) of the Listing Rules 
and (ii) the free float requirement under Rule 19A.13C(2) of the Listing Rules;  
b) the Offer Shares to be subscribed by and allocated to CHIL under the Global Offering will be at 
the same Offer Price and the terms of the Proposed Cornerstone Investment will be on 
substantially the same, or no more favourable, terms as other cornerstone investors;  
c) no preferential treatment has been, nor will be, given to CHIL by virtue of its relationship with 
Mr. Tang, a Controlling Shareholder and an executive Director of the Company, in any 
allocation in the placing tranche other than the preferential treatment of assured entitlement 
under the Proposed Cornerstone Investment which follows the principles set out in Chapters 2.3 
and 4.15 of the Guide for New Listing Applicant, that the cornerstone investment agreement of 
CHIL does not contain any material terms which are more favorable to them than those in other 
cornerstone investment agreements;  
d) the H Shares to be subscribed by CHIL will be subject to a lock-up period of six months 
following the Listing Date, to which the other cornerstone investors of the Company will also 
be subject to;  
e) Mr. Tang shall abstain from voting in relation to resolutions concerning pricing of the Offer 
Shares, and also concerning CHIL, including the approval of and proposed allocation of the 
Proposed Cornerstone Investment;  
f) CHIL will pay and settle the Proposed Cornerstone Investment in full before the Listing; and 
g) details of the subscription of the Offer Shares by CHIL as a cornerstone investor under the 
Global Offering is disclosed in this prospectus and the details of the allocation will be disclosed 
in the allotment results announcement of our Company.  
 
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing Guidelines 
 
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a consent under 
paragraph 1C(1) of the Placing Guidelines to permit GF Securities AM to participate in the Global Offering. 
For details of the allocations to GF Securities AM, please refer to the allocation to Splendid Zhonghe 
Investment under the section headed “Allotment Results Details — International Offer — Cornerstone 
Investors” in this announcement. 
 

<<<PAGE 14>>>
 
In addition, under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines as placees. Please refer to the section headed 
“Allotment Results Details — International Offering — Allottees with Waivers/Consents Obtained” in this 
announcement for details. The Company has applied to the Stock Exchange for, and the Stock Exchange 
has granted, a consent under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate 
such Offer Shares in the International Offering to the connected clients as placees. The allocation of  
Offer Shares to such connected clients is in compliance with all the conditions under the consent granted 
by the Stock Exchange. Details of the placement to connected clients as placees are set out below. 

<<<PAGE 15>>>
No 
Connected 
Distributor 
Connected Client 
Relationship with the 
Connected 
Distributor 
Whether the 
Connected 
Client will hold 
the beneficial 
interests of the Offer 
Shares on a non-
discretionary 
basis or 
discretionary basis 
for 
independent 
third parties 
Whether the 
Connected 
Client is a 
collective 
investment 
scheme which is 
not authorised by 
the SFC or is 
expected to hold 
the Offer Shares 
on behalf of such 
scheme 
Maximum 
number of 
Offer Shares 
(rounded 
down to 
nearest 
whole board 
lot of 200 
Shares) to be 
allocated to 
the Connected 
Client 
Approximate 
percentage of 
total number 
of Offer Shares 
Approximate 
percentage of 
total Shares in 
issue 
immediately 
following the 
completion of 
Global 
Offering 
1. 
CLSA 
CSI Note (1) 
CSI is a 
member of the 
same group of 
companies as 
CLSA 
Non-discretionary 
N 
485,200 
1.03% 
0.11% 
2. 
CITIC Asset 
Management Note (2) 
CITIC Asset 
Management is a 
member of the same 
group of companies as 
CLSA 
Discretionary 
Y Note (2) 
36,000 
0.08% 
0.01% 
3. 
CITIC AM HK Note 
(3)
CITIC AM HK is a 
member of the same 
group of companies as 
CLSA 
Discretionary 
N 
2,339,600 
4.96% 
0.52% 
4. 
HTI 
GTJAI Note (4) 
GTJAI is a 
member of the 
Non-discretionary 
N 
36,000 
0.08% 
0.01% 

<<<PAGE 16>>>
 
 
same group of 
companies as HTI 
5.  
ABCI Capital, 
ABCI Securities 
ABCI AM Note (5) 
ABCI AM, ABCI 
Capital and ABCI 
Securities are group 
companies within the 
same group 
Discretionary 
Y Note (5) 
198,600 
0.42%  
0.04%  
6.  
GF Securities (Hong 
Kong) Brokerage 
E Fund 
Management Note (6) 
E Fund Management 
and GF Securities 
(Hong Kong) 
Brokerage are 
members of the same 
group of companies 
Discretionary 
 
N 
 
1,769,400 
3.75% 
0.40% 
 

<<<PAGE 17>>>
 
 
Notes: 
 
(1) CSI 
CSI will hold the Offer Shares as a placee under the International Offering on behalf of its ultimate 
clients (the “CSI Ultimate Clients”), on a non-discretionary basis, pursuant to which: (i) CSI will act 
as the single counterparty of the CSI Back-to-back TRS (the “CSI Back-to-back TRS”) to be entered 
into by it in connection with a total return swap order (the “CSI Client TRS”) placed and fully funded 
by the CSI Ultimate Clients, by which CSI will pass the full economic exposure of the Offer Shares 
placed to CSI to the CSI Ultimate Clients; (ii) as confirmed by CSI and CLSA, CSI will hold the legal 
title and beneficial interest in the Offer Shares, but will contractually agree to pass on the full economic 
exposure and return of the Offer Shares to the CSI Ultimate Clients, on a non-discretionary basis. The 
CSI Ultimate Clients may exercise their early termination rights to terminate the CSI Client TRS at any 
time from the trade date of the CSI Client TRS which should be on or after the date on which the Offer 
Shares are listed on the Stock Exchange; (iii) upon the final maturity or termination of the CSI Client 
TRS by the CSI Ultimate Clients, CSI will dispose of the Offer Shares on the secondary market and the 
CSI Ultimate Clients will receive a final termination amount of the CSI Back-to-back TRS which will 
have taken into account all the economic returns or economic loss in relation to the Offer Shares and 
the fixed amount of transaction fees of the CSI Back-to-back TRS and the CSI Client TRS. Due to its 
internal policy, CSI will not exercise the voting right of the Offer Shares during the terms of the CSI 
Back-to-back TRS; and (iv) CSI is not a collective investment scheme which is not authorized by the 
SFC, nor is expected to hold the Offer Shares on behalf of such scheme.   
 
The details of the CSI Ultimate Clients are as follows: 
 
Name of the CSI 
Ultimate Clients 
Fund Manager 
UBO(s) holding 30% 
or more interest in 
Fund Manager (if 
applicable) 
UBO(s) holding 30% 
or more interest in the 
CSI Ultimate Clients 
(if applicable) 
Panjing 
Tiandao 
Phase 3 Private 
Equity Investment 
Fund* (盘京天道
3 期私募证券投资
基金) 
Shanghai 
Panjing 
Investment Management 
Center 
(Limited 
Partnership)* (上海盘京
投资管理中心（有限合
伙）) 
Zhuang Tao (庄涛) 
Zhuang Tao (庄涛) 
Panjing 
Jiaxuan 
Phase 2 Private 
Equity Investment 
Fund* (盘京嘉选
2 期私募证券投资
基金) 
Shanghai 
Panjing 
Investment Management 
Center 
(Limited 
Partnership)* (上海盘京
投资管理中心（有限合
伙）) 
Zhuang Tao (庄涛) 
N/A 
Panjing 
Tiandao 
Phase 8 Private 
Equity Investment 
Fund* (盘京天道
8 期私募证券投资
基金) 
Shanghai 
Panjing 
Investment Management 
Center 
(Limited 
Partnership)* (上海盘京
投资管理中心（有限合
伙）) 
Zhuang Tao (庄涛) 
N/A 
Panjing 
Jiaxuan 
Phase 5 Private 
Equity Investment 
Fund* (盘京嘉选
5 期私募证券投资
基金) 
Shanghai 
Panjing 
Investment Management 
Center 
(Limited 
Partnership)* (上海盘京
投资管理中心（有限合
伙）) 
Zhuang Tao (庄涛) 
N/A 

<<<PAGE 18>>>
 
 
Hengde 
Yuanzheng Tianli 
No. 
3 
Private 
Equity Investment 
Fund* (恒德远征
添利3 号私募证
券投资基金) 
Beijing Hengde Times 
Private 
Equity 
Fund 
Management Co., Ltd.* 
(北京恒德时代私募基金
管理有限公司) 
N/A 
N/A 
CITIC 
Capital 
China 
Value 
Return 
No. 
1 
Private 
Equity 
Investment Fund* 
(中信资本中国价
值回报1 号私募
证券投资基金) 
Yuanxin (Zhuhai) Private 
Equity Fund Management 
Co., Ltd.* ( 远信（珠
海）私募基金管理有限
公司) 
Liu Yan (刘岩) 
N/A 
Yuanxin 
Medical 
Industry 
Private 
Equity Investment 
Fund* (远信医疗
产业私募证券投
资基金) 
Yuanxin (Zhuhai) Private 
Equity Fund Management 
Co., Ltd.* ( 远信（珠
海）私募基金管理有限
公司) 
Liu Yan (刘岩) 
N/A 
*For identification purposes only 
 
To the best of knowledge of CSI and having made all reasonable inquiries, each of the CSI Ultimate 
Clients and its UBOs is an independent third party of the Company, its subsidiaries, its substantial 
shareholders, CSI, CLSA and the companies which are members of the same group of companies as 
CLSA.  
 
 
(2) CITIC Asset Management 
CITIC Asset Management will hold the Offer Shares in its capacity as the discretionary fund manager 
managing the funds on behalf of their investors (the “CITIC Asset Management Ultimate Clients”), 
each of which is, to the best knowledge of CITIC Asset Management, (i) an independent third party of 
the Company, its subsidiaries, its substantial shareholders, CITIC Asset Management, CLSA and the 
companies which are members of the same group of companies as CLSA; and (ii) a collective investment 
scheme which is not authorized by the SFC. No ultimate beneficial owner holds 30% or more interest 
in the funds.  
 
The details of the CITIC Asset Management Ultimate Clients are as follows: 
 
Name of the CITIC 
Asset Management 
Ultimate Clients 
Fund Manager 
UBO 
of 
Fund 
Manager 
(if 
applicable) 
UBO holding 30% or 
more interest in the 
CITIC 
Asset 
Management Ultimate 
Client (if applicable) 
CITIC SECURITIES 
COMPANY 
LIMITED-
XINHANG 
ZHIYUAN 
NO.1* 
(中信证券信航致远
1 号集合资产管理
计划) 
CITIC 
Asset 
Management 
CITIC 
Securities 
Company Limited 
N/A 

<<<PAGE 19>>>
 
 
CITIC SECURITIES 
COMPANY 
LIMITED-
XINHANG 
ZHIYUAN 
NO.3* 
(中信证券信航致远
3 号集合资产管理
计划 ) 
CITIC 
Asset 
Management 
CITIC 
Securities 
Company Limited 
N/A 
 
To the best of knowledge of CITIC Asset Management and after making all reasonable enquiries, (i) 
CITIC Asset Management Ultimate Clients, together with each of their ultimate beneficial owners, is 
an independent third party of the Company, its subsidiaries, its substantial shareholders, CITIC Asset 
Management, CLSA and the companies which are members of the same group of companies as CLSA, 
and (ii) none of CLSA and any companies which are members of the same group of companies as CLSA 
that hold any beneficial interest in any of CITIC Asset Management Ultimate Clients. 
 
(3) CITIC AM HK  
CITIC AM HK will hold the Offer Shares in its capacity as the discretionary fund manager managing 
the fund on behalf of its underlying clients, namely (a) Zhengling Xinyin No.2 Private Investment Fund, 
of which the ultimate beneficial owner holding 30% interest or more is Zhuhai Municipal State-owned 
Assets Supervision and Administration Commission (珠海市国资委); and (b) RICH DEVELOPMENT 
LIMITED, of which the ultimate beneficial owners holding 30% or more interest therein are Lu Hui 
and Wang Heping, and of which are, to the best knowledge of CITIC AM HK, independent third parties 
of the Company, its subsidiaries, its substantial shareholders, CITIC AM HK, CLSA and the companies 
which are members of the same group companies as CLSA.  
 
The ultimate beneficial owner of CITIC AM HK is CITIC Securities Company Limited (中信證券股份
有限公司, 6030.HK). 
 
(4) GTJAI 
It is proposed that GTJAI participates as placee to subscribe for the Offer Shares under the 
International Offering (the “GTJAI Subscription”). GTJAI is a member of the same group of 
companies as HTI and is considered as a connected client of HTI pursuant to paragraph 1B(7) of the 
Placing Guidelines. 
 
In relation to the GTJAI Subscription, GTJAI shall hold the Offer Shares for hedging purpose as the 
single underlying asset of several sets of back-to-back total return swap transaction (the “GTHT Back-
to-back TRS”) to be entered into between GTJAI and Guotai Haitong Securities Co., Ltd. (the “GTHT 
Onshore Parent”) in connection with several total return swap orders (the “GTHT Client TRS”) to 
be entered into by GTHT Onshore Parent and an ultimate client (the “GTHT Onshore Ultimate 
Client”), respectively. Such GTHT Client TRS is to be fully funded by the GTHT Onshore Ultimate 
Client. GTJAI will hold the Offer Shares on a non-discretionary basis for the purpose of hedging the 
economic exposure under the GTHT Back-to-back TRS and GTHT Client TRS only, During the tenor 
of the GTHT Client TRS, all economic returns of the Offer Shares will be passed to the GTHT Onshore 
Ultimate Client and all economic losses shall be borne by the GTHT Onshore Ultimate Client, subject 
to the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS, and GTJAI will not 
take part in any economic return or bear any economic loss in relation to the price of the Offer Shares. 
The GTHT Onshore Ultimate Client may request to redeem the Offer Shares at their own discretion, 
upon which GTJAI shall dispose of the Offer Shares and settle the GTHT Back-to-back TRS and GTHT 

<<<PAGE 20>>>
 
 
Client TRS in cash in accordance with the terms and conditions of the GTHT Back-to-back TRS and 
GTHT Client TRS documents. Due to its internal policy, GTJAI will not exercise the voting right 
attaching to the Offer Shares during the tenor of the GTHT Back-to-back TRS and GTHT Client TRS. 
 
To the best knowledge, information and belief of GTJA Investments after due enquiry, the GTJA 
Onshore Ultimate Client is Tianchong Changyang No. 8 Private Securities Investment Fund (天虫长
阳8 号私募证券投资基金), of which the ultimate beneficial owner holding 30% or more interest is Ye 
Lan (叶兰).  
 
To the best knowledge of GTJAI and after making all reasonable enquiries, (i) GTJA Investments has 
confirmed that, to the best of their knowledge, the GTJA Onshore Ultimate Client and the ultimate 
beneficial owner holding 30% or more interest of the GTJA Onshore Ultimate Client listed above is an 
independent third party of GTJA Investments, HTI and the companies which are members of the same 
group of companies as HTI, and (ii) GTJAI is not a collective investment scheme which is not authorised 
by the SFC nor is expected to hold the Offer Shares on behalf of such scheme. 
 
(5) ABCI AM 
ABCI AM is a member of the same group of companies as ABCI Capital and ABCI Securities, and ABCI 
AM is therefore a connected client of ABCI Capital and ABCI Securities. 
 
ABCI AM intends to hold the Offer Shares in its capacity as manager managing investment portfolios 
on behalf of underlying investors (the “ABCI AM Ultimate Clients”) who are independent third parties 
on a discretionary basis. The details of the ABCI Ultimate Clients are as follows: 
 
Name of the ABCI 
Ultimate Clients 
Fund Manager 
UBO of Fund Manager 
UBO(s) holding 30% 
or more interest in 
the ABCI Ultimate 
Client (if applicable) 
ABCI 
Global 
Opportunities SPC - 
ABCI China Rising 6 
SP 
ABCI AM 
AGRICULTURAL BANK 
OF CHINA LIMITED 
Wei 
Dezhi, 
Chen 
Dong 
ABCI 
CHINA 
OPPORTUNITIES 
SPC - ABCI CHINA 
NEW GROWTH SP 
ABCI AM 
AGRICULTURAL BANK 
OF CHINA LIMITED 
He Dian (贺电) 
 
To the best knowledge of ABCI AM, each of the ABCI AM Ultimate Clients is an independent third 
party of the Company, its subsidiaries, its substantial shareholders, ABCI Capital, ABCI Securities and 
the companies which are members of the same group of companies as ABCI Capital and ABCI 
Securities. ABCI AM also confirms that it will not hold any Offer Shares placed to it on a proprietary 
basis for itself or for any group member of ABCI, and the Offer Shares will be held by it on behalf of 
independent third parties. 
 
(6) E Fund Management 
E Fund Management will hold the Offer Shares for and on behalf of their underlying clients (the “E 
Fund Management Ultimate Clients”) on a discretionary basis. To the best knowledge of E Fund 
Management and after making all reasonable enquiries, each of the E Fund Management Ultimate 
Clients is independent from the Company, its subsidiaries, its substantial shareholders, GF 
Securities (Hong Kong) Brokerage, E Fund Management and the companies which are members of 

<<<PAGE 21>>>
 
 
the same group of companies as GF Securities (Hong Kong) Brokerage. 
 
 
 

<<<PAGE 22>>>
 
 
DISCLAIMERS 
 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and Hong 
Kong Securities Clearing Company Limited take no responsibility for the contents of this announcement, 
make no representation as to its accuracy or completeness and expressly disclaim any liability 
whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the contents 
of this announcement. 
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United 
States (including its territories and possessions, any state of the United States and the District of 
Columbia). This announcement does not constitute or form a part of any offer or solicitation to purchase 
or subscribe for securities in the United States. The securities mentioned herein have not been, and will 
not be, registered under the United States Securities Act of 1933, as amended (the “U.S. Securities Act”). 
The securities may not be offered or sold in the United States except pursuant to an exemption from the 
registration requirements of the U.S. Securities Act and in compliance with any applicable state securities 
laws, or outside the United States unless in compliance with Regulation S under the U.S. Securities Act. 
There will be no public offer of securities in the United States. 
The Offer Shares are being offered and sold outside the United States in offshore transactions in reliance 
on Regulation S under the U.S. Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or offer to 
acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential investors 
should read the Prospectus dated April 20, 2026 issued by Mabwell (Shanghai) Bioscience Co., Ltd. for 
detailed information about the Global Offering described below before deciding whether or not to invest 
in the H Shares thereby being offered. 
*Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall Coordinators 
(for themselves and on behalf of the Hong Kong Underwriters and the Capital Market Intermediaries) 
shall be entitled to terminate their obligations under the Hong Kong Underwriting Agreement with 
immediate effect upon the occurrence of any of the events set out in the section headed “Underwriting — 
Underwriting Agreements — Hong Kong Underwriting Agreement — Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently 
expected to be on April 28, 2026). 

<<<PAGE 23>>>
 
 
PUBLIC FLOAT AND FREE FLOAT 
Immediately after the completion of the Global Offering, the total number of H Shares to be 
held by the public is 45,146,400 H Shares, calculated on the basis that save for the 1,983,800 
H Shares to be subscribed by CHIL, a wholly-owned limited liability company of our 
Controlling Shareholder and executive Director, Mr. Tang, as a cornerstone investor, none of 
the other H Shareholders is expected to be a core connected person of our Company, and no H 
Shares will be allocated under the Global Offering to any core connected person of our 
Company (other than CHIL) or person which is not regarded as a member of the public under 
Rule 8.24 of the Listing Rules.  
The total number of H Shares to be held by the public upon the Listing represents approximately 
10.11% of the total issued share capital of our Company (being the total number of issued 
shares in the class to which H Shares belong, excluding treasury shares), which is higher than 
the minimum prescribed percentage of 10% under Rule 19A.13A(2)(a) of the Listing Rules, 
thereby satisfying Rule 19A.13A of the Listing Rules.   
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date.  As such, H Shares held by the Cornerstone Investors (including CHIL) upon the 
Listing shall not be counted towards the free float of the H Shares of the Company at the time 
of Listing. Based on the final Offer Price of HK$ 27.64 per H Share, the market capitalization 
of the H Shares listed on the Stock Exchange that are held by the public and are not subject to 
any disposal restrictions at the time of the Listing is expected to be approximately HK$ 887.51 
million, which is higher than the prescribed expected market capitalization of not less than 
HK$600,000,000 under Rule 19A.13C(2)(b) of the Listing Rules.  The Company confirms the 
free float requirement under Rule 19A.13C of the Listing Rules is satisfied. 
The Directors confirm that, immediately following completion of the Global Offering: (i) no 
placee will, individually, be placed more than 10% of the enlarged issued share capital of the 
Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder under the Listing Rules immediately after the Global Offering; (iii) the three largest 
public shareholders of the Company do not hold more than 50% of the H shares in public hands 
at the time of the Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and 
(iv) there will be at least 300 Shareholders at the time of the Listing in compliance with Rule 
8.08(2) of the Listing Rules. 
COMMENCEMENT OF DEALINGS 
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, April 
28, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and 
the right of termination described in the section headed “Underwriting — Underwriting 
Agreements — Hong Kong Underwriting Agreement — Grounds for Termination” in the 
Prospectus has not been exercised. Investors who trade the H Shares on the basis of publicly 
available allocation details prior to the receipt of H Share certificates or prior to the H Share 
certificates becoming valid evidence of title do so entirely at their own risk. 
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Tuesday, 
April 28, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock 
Exchange will commence at 9:00 a.m. on Tuesday, April 28, 2026 (Hong Kong time). The H 
Shares will be traded in board lots of 200 H Shares each, and the stock code of the H Shares 
will be 2493. 

<<<PAGE 24>>>
 
 
 
By order of the Board 
Mabwell (Shanghai) Bioscience Co., Ltd. 
Mr. Hu Huiguo 
    Executive Director 
 
 
Hong Kong, April 27, 2026 
 
As at the date of this announcement, the Board comprises: (i) Mr. Tang Chunshan, Dr. Liu 
Datao (Chairman of the Board), Dr. Wu Hai, Mr. Hu Huiguo, Dr. Gui Xun as executive 
Directors; (ii) Mr. Wu Yufeng as non-executive Director; and (iii) Mr. Qin Zhengyu, Dr. Xu 
Qing, Dr. Zhao Qian as independent non-executive Directors and Ms. Wang Fang as 
proposed independent non-executive Director, effective upon Listing. 
 
