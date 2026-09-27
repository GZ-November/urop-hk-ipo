# 配发结果公告抽取任务：0100.HK MiniMax Group Inc. - W - P

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**08/01/2026 22:40**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0108/2026010801342.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"0100.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as those 
defined in the prospectus dated Wednesday, December 31, 2025 (the “Prospectus”) of MiniMax Group Inc. (the 
“Company”).
This announcement is for information purposes only and does not constitute an offer or an invitation to induce an offer 
by any person to acquire, purchase or subscribe for any of the securities of the Company. This announcement is not a 
prospectus. Potential investors should read the Prospectus for detailed information about the Global Offering described 
below before deciding whether or not to invest in the Offer Shares. Any investment decision in relation to the Offer 
Shares should be taken solely in reliance on the information provided in the Prospectus.
This announcement does not constitute an offer to sell or the solicitation of an offer to buy nor shall there be any sale 
of Offer Shares in any jurisdiction in which such offer, solicitation or sales would be unlawful. This announcement is 
not for release, publication or distribution, directly or indirectly, in or into the United States or any other jurisdiction 
where such distribution is prohibited by law, nor is this announcement an offer for sale or solicitation to purchase or 
subscribe for securities in the United States or any other jurisdictions. The Offer Shares have not been and will not 
be registered under the U.S. Securities Act or any state securities laws in the United States and may not be offered, 
sold, pledged or transferred within the United States or to, or for the account or benefit of U.S. persons (as defined 
in Regulation S under the U.S. Securities Act), except in transactions exempt from, or not subject to, the registration 
requirements of the U.S. Securities Act. The Offer Shares are being offered and sold (1) solely to qualified institutional 
buyers as defined in Rule 144A in reliance on Rule 144A or another exemption from, or in a transaction not subject 
to, registration under the U.S. Securities Act and (2) outside the United States in offshore transactions in reliance on 
Regulation S under the U.S. Securities Act.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited, as 
the stabilizing manager (the “Stabilizing Manager”) (or any person acting for it), on behalf of the Underwriters, may 
over-allocate or effect transactions with a view to stabilizing or supporting the market price of the Class A Ordinary 
Shares at a level higher than that which might otherwise prevail for a limited period after the Listing Date. However, 
there is no obligation on the Stabilizing Manager (or any person acting for it) to conduct any such stabilizing action. 
Such stabilizing action, if taken, (a) will be conducted at the absolute discretion of the Stabilizing Manager (or any 
person acting for it) and in what the Stabilizing Manager (or any person acting for it) reasonably regards as the best 
interest of our Company, (b) may be discontinued at any time, and (c) is required to be brought to an end within 30 
days after the last day for lodging applications under the Hong Kong Public Offering (which is Thursday, February 5, 
2026). Such stabilization action, if taken, may be effected in all jurisdictions where it is permissible to do so, in each 
case in compliance with all applicable laws, rules and regulatory requirements, including the Securities and Futures 
(Price Stabilizing) Rules (Chapter 571W of the Laws of Hong Kong), as amended, made under the Securities and 
Futures Ordinance (Chapter 571 of the Laws of Hong Kong).
Potential investors should be aware that no stabilizing action can be taken to support the price of the Class A 
Ordinary Shares for longer than the stabilization period which begins on the Listing Date, and is expected to expire on 
Thursday, February 5, 2026, the 30th day after the last day for the lodging of applications under the Hong Kong Public 
Offering. After this date, when no further stabilizing action may be taken, demand for the Class A Ordinary Shares, 
and therefore the price of the Class A Ordinary Shares, could fall.
The Hong Kong Offer Shares will be offered to the public in Hong Kong subject to the terms and conditions set out 
in the Prospectus. The Hong Kong Offer Shares will not be offered to any person who is outside Hong Kong and/
or not resident in Hong Kong. Potential investors of the Offer Shares should note that the Joint Sponsors and the 
Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the 
events set out in the section headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public 
Offering – Hong Kong Underwriting Agreement – Grounds for Termination” in the Prospectus at any time prior to 8:00 
a.m. (Hong Kong time) on the Listing Date (which is currently expected to be on Friday, January 9, 2026).

<<<PAGE 2>>>
2
MiniMax Group Inc.
(A company controlled through weighted voting rights and incorporated in the Cayman Islands with limited liability)
GLOBAL OFFERING
Number of Offer Shares under
the Global Offering
:
29,197,600 Offer Shares (taking into 
 account the full exercise of the Offer Size 
 Adjustment Option and subject to the 
 Over-allotment Option)
Number of Hong Kong Offer Shares
:
5,077,860 Offer Shares (as adjusted after 
 reallocation)
Number of International Offer Shares
:
24,119,740 Offer Shares (taking into 
 account the full exercise of the Offer 
 Size Adjustment Option, as adjusted 
 after reallocation and subject to the 
 Over-allotment Option)
Final Offer Price
:
HK$165.00 per Offer Share, plus
 brokerage of 1%, SFC transaction levy
 of 0.0027%, Stock Exchange trading fee
 of 0.00565% and AFRC transaction levy
 of 0.00015% (payable in full on
 application in Hong Kong dollars and
 subject to refund)
Nominal value
:
US$0.0001 per Offer Share
Stock code
:
0100
Joint Sponsors, Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
(in alphabetical order)
Overall Coordinators, Joint Global Coordinators,
Joint Bookrunners and Joint Lead Managers
(in alphabetical order)
Joint Bookrunners and Joint Lead Managers
(in alphabetical order)

<<<PAGE 3>>>
 
 
3 
 
MiniMax Group Inc. 
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS 
 
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the Class A Ordinary Shares 
could move substantially even with a small number of the Class A Ordinary Shares traded and should 
exercise extreme caution when dealing in the Class A Ordinary Shares. 
SUMMARY 
 
Company information 
Stock code  
0100 
Stock short name  
MINIMAX - WP 
Dealings commencement date 
January 9, 2026* 
*see note at the end of the announcement 
 
Price Information  
Final Public Offer Price and International Offer Price (the 
“Offer Price”) 
HK$165.00 
Offer Price Range 
HK$151.00 - HK$165.00 
 
Offer Shares and Share Capital 
Number of Offer Shares (after full exercise of the Offer Size 
Adjustment Option) 
29,197,600 
Final Number of Offer Shares in Public Offer (after 
reallocation) 
5,077,860 
Final Number of Offer Shares in International Offer (after 
reallocation and the full exercise of the Offer Size 
Adjustment Option) 
24,119,740 
Number of issued Shares upon Listing (before exercise of the 
Over-allotment Option) 
309,255,668 
The number of Offer Shares above is determined after taking into account the additional Offer Shares issued 
under the following Offer Size Adjustment Option. 
 
Offer Size Adjustment Option (Upsize option) 
Number of additional shares issued under the option 
3,808,380 
- 
Public Offer 
0 
- 
International Offer 
3,808,380 
The Offer Size Adjustment Option has been exercised in full, pursuant to which the Company is issuing 
and allotting 3,808,380 additional Offer Shares, representing approximately 15% of the total number of 
Offer Shares initially available under the Global Offering, at the final Offer Price. 
 
Over-allocation 
No. of Offer Shares over-allocated 
4,379,640 
- 
International Offer 
4,379,640 
Such over-allocation may be covered by exercising the Over-allotment Option or by making purchases 
in the secondary market at prices that do not exceed the Offer Price or through deferred delivery or a 

<<<PAGE 4>>>
4 
 
combination of these means. In the event the Over-allotment Option is exercised, an announcement will 
be made on the Stock Exchange’s website.  
 
Proceeds   
Gross proceeds (Note)  
HK$4,817.6 million  
Less: Estimated listing expenses payable based on final 
Offer Price  
HK$(221.5) million 
Net proceeds  
HK$4,596.1 million  
 
Note: Gross proceeds refer to the amount which the Company is entitled to receive. For details of the use 
of proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus. The 
Company will adjust the allocation of the net proceeds from the exercise of the Offer Size Adjustment Option 
and the exercise of the Over-allotment Option (if any) for the purposes as set out in the section headed 
“Future Plans and Use of Proceeds” of the Prospectus on a pro rata basis. 
 
 
ALLOTMENT RESULTS DETAILS 
PUBLIC OFFER 
 
No. of valid applications  
417,646 
No. of successful applications  
104,901 
Subscription level  
1,837.17 times 
Claw-back triggered  
Yes 
No. of Offer Shares initially available under the Public Offer  
1,269,480 
No. of Offer Shares reallocated from the International Offer (claw-
back) 
3,808,380 
Final no. of Offer Shares under the Public Offer (after reallocation) 5,077,860 
% of Offer Shares under the Public Offer to the Global Offering 
(after the full exercise of the Offer Size Adjustment Option) 
17.4% 
 
Note: For details of the final allocation of Offer Shares to the Public Offer, investors can refer to 
www.hkeipo.hk/iporesult to perform a search by identification number or www.hkeipo.hk/iporesult for the full 
list of allottees. 
INTERNATIONAL OFFER 
 
No. of placees 
376 
Subscription level (before taking into account the Offer Size 
Adjustment Option) 
36.76 times 
No. of Offer Shares initially available under the International Offer  24,119,740 
No. of Offer Shares reallocated to the Public Offer (claw-back) 
3,808,380 
Final no. of Offer Shares under the International Offer (after 
reallocation and the full exercise of the Offer Size Adjustment 
Option) 
24,119,740 
% of Offer Shares under the International Offer to the Global 
Offering (after the full exercise of the Offer Size Adjustment 
Option) 
82.6% 
 

<<<PAGE 5>>>
5 
 
The Directors confirm that, to the best of their knowledge, information and belief, save for a waiver from strict 
compliance with Rule 10.04 of the Listing Rules and a consent under paragraph 1C(2) of Appendix F1 to the 
Listing Rules (the “Placing Guidelines”) granted by the Stock Exchange to permit Offer Shares in the 
International Offering to be placed to certain existing minority shareholders and/or their close associates, (i) 
none of the Offer Shares subscribed by the placees and the public have been financed directly or indirectly by 
the Company, any of the Directors, chief executive of the Company, Controlling Shareholders, substantial 
Shareholders, existing Shareholders of the Company or any of its subsidiaries or their respective close 
associates; and (ii) none of the placees and the public who have purchased the Offer Shares are accustomed 
to taking instructions from the Company, any of the Directors, chief executive of the Company, Controlling 
Shareholders, substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries or 
their respective close associates in relation to the acquisition, disposal, voting or other disposition of the Class 
A Ordinary Shares registered in his/her/its name or otherwise held by him/her/it.  
The placees in the International Offer include the following: 
Cornerstone Investors  
 
Investor 
No. 
of 
Offer 
Shares 
allocated 
% 
of 
Offer 
Shares 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
Class 
A 
Ordinary Shares 
(after 
taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
share 
capital 
after the Global 
Offering 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Existing 
shareholders 
or their close 
associates 
Abu Dhabi 
Investment 
Authority 
(“ADIA”) 
3,065,040 
10.50% 
1.34% 
0.99% 
No 
Alisoft China 
Holding Limited 
(“Alisoft China”) 
1,414,640 
4.85% 
0.62% 
0.46% 
Yes 
Aspex Master 
Fund  
1,650,400 
5.65% 
0.72% 
0.53% 
Yes 
Abstract Enigma 
Limited 
1,650,400 
5.65% 
0.72% 
0.53% 
Yes 
China Universal 
Asset 
Management 
(Hong Kong) 
Company Limited 
(“China 
Universal (HK)”) 
707,320 
2.42% 
0.31% 
0.23% 
No 

<<<PAGE 6>>>
6 
 
 
Investor 
No. 
of 
Offer 
Shares 
allocated 
% 
of 
Offer 
Shares 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
Class 
A 
Ordinary Shares 
(after 
taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
share 
capital 
after the Global 
Offering 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Existing 
shareholders 
or their close 
associates 
Eastspring 
Investments 
(Singapore) 
Limited 
(“Eastspring”) 
707,320 
2.42% 
0.31% 
0.23% 
No 
E Fund 
Management Co., 
Ltd. (“E Fund 
Management”) 
471,540 
1.61% 
0.21% 
0.15% 
No 
IDG Breyer 
Capital Fund L.P. 
(“IDG Breyer 
Fund”) 
707,320 
2.42% 
0.31% 
0.23% 
Yes 
Janchor Partners 
Pan-Asian Master 
Fund and Janchor 
Partners 
Opportunities 
Master Fund III 
(“Janchor 
Funds”) 
1,650,400 
5.65% 
0.72% 
0.53% 
Yes 
Martis Fund, L.P. 
707,320  
2.42% 
0.31% 
0.23% 
No 
Mirae Asset 
Securities Co., 
Ltd. (“Mirae 
Asset Securities”) 
943,080  
3.23% 
0.41% 
0.30% 
No 
MPC VII Pte. Ltd. 
(“MPC VII”) 
707,320  
2.42% 
0.31% 
0.23% 
Yes 
Perseverance 
Asset 
Management 
International 
(Singapore) Pte. 
Ltd. 
(“Perseverance 
1,178,860  
4.04% 
0.52% 
0.38% 
No 

<<<PAGE 7>>>
7 
 
 
Investor 
No. 
of 
Offer 
Shares 
allocated 
% 
of 
Offer 
Shares 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
Class 
A 
Ordinary Shares 
(after 
taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
share 
capital 
after the Global 
Offering 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Existing 
shareholders 
or their close 
associates 
Asset 
Management”) 
Taikang Life 
Insurance Co., Ltd 
(“Taikang Life”) 
943,080  
3.23% 
0.41% 
0.30% 
No 
Total 
16,504,040  56.53% 
7.23% 
5.34% 
 
 
 

<<<PAGE 8>>>
8 
 
 
Allotees with Waivers/Consents Obtained 
 
 
Investor 
No. 
of 
Offer 
Shares 
allocated 
% 
of 
Offer 
Shares 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
Class A 
Ordinary 
Shares (after 
taking into 
account the full 
exercise of the 
Offer Size 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
share 
capital 
after the Global 
Offering 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option 
is 
not 
exercised)  
Relationship 
Allotees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under 
paragraph 1C(2) of the Placing Guidelines in relation to subscription for Offer Shares by existing 
minority shareholders and/or its close associates as cornerstone investors and placees Note 1 
Cornerstone Investors 
Alisoft China 
1,414,640 
4.85% 
0.62% 
0.46% 
A 
cornerstone 
investor and an 
existing 
minority 
shareholder 
Aspex 
Master 
Fund 
1,650,400 
5.65% 
0.72% 
0.53% 
A 
cornerstone 
investor and a 
close 
associate 
of an existing 
minority 
shareholder 
Abstract Enigma 
Limited 
1,650,400 
5.65% 
0.72% 
0.53% 
A 
cornerstone 
investor and a 
close 
associate 
of an existing 
minority 
shareholder 
IDG Breyer Fund 707,320 
2.42% 
0.31% 
0.23% 
A 
cornerstone 
investor and a 
close 
associate 
of an existing 
minority 
shareholder 
Janchor Funds 
1,650,400 
5.65% 
0.72% 
0.53% 
A cornerstone 
investor and an 
existing 

<<<PAGE 9>>>
9 
 
 
Investor 
No. 
of 
Offer 
Shares 
allocated 
% 
of 
Offer 
Shares 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
Class A 
Ordinary 
Shares (after 
taking into 
account the full 
exercise of the 
Offer Size 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
share 
capital 
after the Global 
Offering 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option 
is 
not 
exercised)  
Relationship 
minority 
shareholder 
MPC VII 
707,320  
2.42% 
0.31% 
0.23% 
A 
cornerstone 
investor and an 
existing 
minority 
shareholder 
Placees  
Planetree Existing Shareholders and their close associate 
Planetree 
Partners III, L.P.  
120 
0.00% 
0.00% 
0.00% 
A placee and an 
existing 
minority 
shareholder 
Planetree 
Partners 
III-A, 
L.P.  
20 
0.00% 
0.00% 
0.00% 
A placee and an 
existing 
minority 
shareholder 
Farseer L.P. 
120 
0.00% 
0.00% 
0.00% 
A placee and a 
close 
associate 
of 
Planetree 
Partners 
III, 
L.P., 
Planetree 
Partners 
III-A, 
L.P. 
and 
Planetree 
PARTNERS 
HARVEST 
l, 
L.P. 
Subtotal 
260 
0.00% 
0.00% 
0.00% 
- 
China Orient and its close associate  
China 
Orient 
Enhanced 
Income 
Fund 
8,500 
0.03% 
0.00% 
0.00% 
A placee and an 
existing 

<<<PAGE 10>>>
10 
 
 
Investor 
No. 
of 
Offer 
Shares 
allocated 
% 
of 
Offer 
Shares 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
Class A 
Ordinary 
Shares (after 
taking into 
account the full 
exercise of the 
Offer Size 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
share 
capital 
after the Global 
Offering 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option 
is 
not 
exercised)  
Relationship 
(“China 
Orient”) 
minority 
shareholder 
China 
Orient 
Multi-Strategy 
Master Fund 
7,100 
0.02% 
0.00% 
0.00% 
A placee and a 
close 
associate 
of 
existing 
minority 
shareholders 
Subtotal 
15,600 
0.05% 
0.01% 
0.00% 
- 
Close associates of MNM Holdings Limited and XAM Holdings Limited 
Hillhouse 
Investment 
Management 
Limited  
238,160 
0.82% 
0.10% 
0.08% 
A placee and a 
close 
associate 
of 
existing 
minority 
shareholders 
HHLR Advisors, 
Ltd.  
238,140 
0.82% 
0.10% 
0.08% 
A placee and a 
close 
associate 
of 
existing 
minority 
shareholders 
Subtotal 
476,300 
1.63% 
0.21% 
0.15% 
- 
VitalFamily 
II 
Limited 
2,360 
0.01% 
0.00% 
0.00% 
A placee and a 
close 
associate 
of an existing 
minority 
shareholder 
HCEP 
Management 
Limited 
23,560 
0.08% 
0.01% 
0.01% 
A placee and a 
close 
associate 
of an existing 
minority 
shareholder 
CICC Financial 
Trading Limited 
in 
connection 
24,760 
0.08% 
0.01% 
0.01% 
A placee and a 
close 
associate 
of 
existing 

<<<PAGE 11>>>
11 
 
 
Investor 
No. 
of 
Offer 
Shares 
allocated 
% 
of 
Offer 
Shares 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
Class A 
Ordinary 
Shares (after 
taking into 
account the full 
exercise of the 
Offer Size 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
share 
capital 
after the Global 
Offering 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option 
is 
not 
exercised)  
Relationship 
with the CICCFT 
OTC Swaps (as 
defined below) 
minority 
shareholders 
Also 
a 
connected client 
Guotai 
Junan 
Investments 
(Hong 
Kong) 
Limited 
in 
connection with 
the 
GTJAI 
Subscription (as 
defined below) 
18,100 
0.06% 
0.01% 
0.01% 
A placee and a 
close 
associate 
of an existing 
minority 
shareholder 
Also 
a 
connected client 
Allotees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the 
Guide for New Listing Applicants in relation to allocations to connected clients Note 2  
CICC Financial 
Trading Limited 
24,760 
0.08% 
0.01% 
0.01% 
Connected client 
Also 
a 
close 
associate of an 
existing 
minority 
shareholder 
Guotai 
Junan 
Investments 
(Hong 
Kong) 
Limited 
18,100 
0.06% 
0.01% 
0.01% 
Connected client 
Also 
a 
close 
associate of an 
existing 
minority 
shareholder 
CITIC Securities 
International 
Capital 
Management 
Limited 
940 
0.00% 
0.00% 
0.00% 
Connected client 
 

<<<PAGE 12>>>
12 
 
 
Investor 
No. 
of 
Offer 
Shares 
allocated 
% 
of 
Offer 
Shares 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
Class A 
Ordinary 
Shares (after 
taking into 
account the full 
exercise of the 
Offer Size 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
share 
capital 
after the Global 
Offering 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option 
is 
not 
exercised)  
Relationship 
Huatai 
Capital 
Investment 
Limited 
10,040 
0.03% 
0.00% 
0.00% 
Connected client 
 
Bosera 
Asset 
Management 
(International) 
Co., Ltd 
9,400 
0.03% 
0.00% 
0.00% 
Connected client 
China 
Asset 
Management 
(Hong 
Kong) 
Limited  
23,560 
0.08% 
0.01% 
0.01% 
Connected client 
China 
Asset 
Management 
Co., Ltd.  
71,000 
0.24% 
0.03% 
0.02% 
Connected client 
CITIC Securities 
Asset 
Management 
Company 
Limited  
480 
0.00% 
0.00% 
0.00% 
Connected client 
ICBC UBS Asset 
Management 
(International) 
Company 
Limited 
1,400 
0.00% 
0.00% 
0.00% 
Connected client 
Notes: 
 
1. 
See “Waivers and Exemption – Waiver Under Rule 10.04 and Consent under Paragraph 1C(2) of Appendix 
F1 to the Listing Rules in respect of Subscriptions of Offer Shares by Existing Shareholders and/or its Close 
Associates as Cornerstone Investors” of the Prospectus and the section headed “Others / Additional 
Information – Placing to existing shareholders and/or its close associates with a prior waiver under Rule 
10.04 and consent under paragraph 1C(2) of the Placing Guidelines” in this announcement for further 
details. 
 
2. 
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide 
for New Listing Applicants in relation to allocations to connected clients, please refer to the section headed 
“Others / Additional Information – Placing to connected clients with a prior consent under paragraph 

<<<PAGE 13>>>
13 
 
 
Investor 
No. 
of 
Offer 
Shares 
allocated 
% 
of 
Offer 
Shares 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
Class A 
Ordinary 
Shares (after 
taking into 
account the full 
exercise of the 
Offer Size 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
share 
capital 
after the Global 
Offering 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option 
is 
not 
exercised)  
Relationship 
1C(1) of the Placing Guidelines” in this announcement. 
 
LOCK-UP UNDERTAKINGS  
Key Persons (as defined under Rule 18C.14 of the Listing Rules) 
Name 
Capacity  
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing  
% of total issued Shares 
after the Global Offering 
upon 
Listing 
(after 
taking into account the 
full exercise of the Offer 
Size Adjustment Option 
and assuming the Over-
allotment Option is not 
exercised) 
Last day subject 
to the lock-up 
undertakings 
Note 1 
Dr. Yan Junjie (“Dr. Yan”) Note 2 
Alpha EXP 
Limited 
(“Alpha 
EXP”) 
Dr. Yan’s close 
associates 
62,593,180 Class B 
Ordinary Shares 
20.24% 
January 8, 2028 
 
 
MiniMax 
Awakening 
Limited 
(“MiniMax 
Awakening”) 
Dr. Yan’s close 
associates 
11,509,339 Class B 
Ordinary Shares 
3.72% 
January 8, 2028 
 
MiniMax 
Matrix 
Limited 
(“MiniMax 
Matrix”) 
Dr. Yan’s close 
associates 
5,000,000 Class A 
Ordinary Shares 
1.62% 
January 8, 2028 
 
MiniMax 
Limited 
Dr. Yan’s close 
associates 
15 Class B Ordinary 
Shares 
0.000005%  
January 8, 2028 
 
Ms. Yun Yeyi (“Ms. Yun”) Note 2 
Floating Sky 
Limited 
(“Floating 
Sky”) 
Ms. Yun close 
associates 
7,000,000 Class B 
Ordinary Shares 
2.26% 
January 8, 2028 
 
Notes: 

<<<PAGE 14>>>
14 
 
Name 
Capacity  
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing  
% of total issued Shares 
after the Global Offering 
upon 
Listing 
(after 
taking into account the 
full exercise of the Offer 
Size Adjustment Option 
and assuming the Over-
allotment Option is not 
exercised) 
Last day subject 
to the lock-up 
undertakings 
Note 1 
 
1. The lock-up period commences on the date by reference to which disclosure of its shareholding is made in the 
Prospectus and ends on the date which is 24 months from the Listing Date, i.e. January 8, 2028. In the event 
that upon the notification by the Stock Exchange that the Company will no longer be regarded as a Pre-
Commercial Company after the Listing, the lock-up period will expire on the later of: (i) the date on which 
such lock-up periods would have ended if the Company had applied for listing as a Commercial Company; 
and (2) the date falling on the 30th day after the announcement on the removal of designation as a Pre-
Commercial Company as required under Rule 18C.24 of the Listing Rules. 
 
2. Dr. Yan and Ms. Yun are our founders, WVR beneficiaries, executive Directors and senior management and 
Dr. Yan is also our key personnel responsible for our technical operations and/or the research and 
development of our Specialist Technology Products, who are subject to lock-up requirements pursuant to Rule 
18C.14 of the Listing Rules.  
 
Pathfinder SIIs 
Name 
Capacity  
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing  
% of total issued 
Class A 
Ordinary Shares 
(after taking into 
account the full 
exercise of the 
Offer Size 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
Shares after the 
Global Offering 
upon Listing 
(after taking into 
account the full 
exercise of the 
Offer Size 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is not 
exercised) 
Last day 
subject to the 
lock-up 
undertakings 
Note 1 
Shanghai 
Mihoyo 
Argo 
Technology 
Co., Ltd 
(上海米哈
游阿爾戈
科技有限
公司) 
Pathfinder 
SII 
1,912,399 
Class 
A 
Ordinary Shares 
0.84% 
0.62% 
January 
8, 
2027 
 
 
miHoYo 
Limited 
Pathfinder 
SII 
16,015,779 Class A 
Ordinary Shares 
7.02% 
5.18% 
January 
8, 
2027 
 

<<<PAGE 15>>>
15 
 
Name 
Capacity  
Number of Shares 
held in the Company 
subject to lock-up 
undertakings upon 
Listing  
% of total issued 
Class A 
Ordinary Shares 
(after taking into 
account the full 
exercise of the 
Offer Size 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is not 
exercised) 
% of total issued 
Shares after the 
Global Offering 
upon Listing 
(after taking into 
account the full 
exercise of the 
Offer Size 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is not 
exercised) 
Last day 
subject to the 
lock-up 
undertakings 
Note 1 
Cosmic 
Station 
Limited 
Pathfinder 
SII 
7,301,687 
Class 
A 
Ordinary Shares 
3.20% 
2.36% 
January 
8, 
2027 
 
Seasonal 
Charm 
Limited 
Pathfinder 
SII 
535,263 
Class 
A 
Ordinary Shares 
0.23% 
0.17% 
January 
8, 
2027 
 
Note: 
 
1. In accordance with Rule 18C.14 of the Listing Rules, the required lock-up period commences on the date by 
reference to which disclosure of its shareholding is made in the Prospectus and ends on the date which is 12 
months from the Listing Date, i.e. January 8, 2027. In the event that upon the notification by the Stock 
Exchange that the Company will no longer be regarded as a Pre-Commercial Company after the Listing, the 
lock-up period will expire on the later of: (i) the date on which such lock-up periods would have ended if the 
Company had applied for listing as a Commercial Company; and (2) the date falling on the 30th day after the 
announcement on the removal of designation as a Pre-Commercial Company as required under Rule 18C.24 
of the Listing Rules. 
 
Controlling Shareholders 
Name 
Number of Shares held in 
the Company subject to lock-
up 
undertakings 
upon 
Listing  
% of total issued Shares after the 
Global Offering upon Listing 
(after taking into account the full 
exercise 
of 
the 
Offer 
Size 
Adjustment Option and assuming 
the Over-allotment Option is not 
exercised) 
Last day subject to the 
lock-up undertakings 
Note 1 
Alpha EXP 
62,593,180 Class B Ordinary 
Shares 
20.24% 
January 8, 2028 
 
 
MiniMax 
Awakening 
11,509,339 Class B Ordinary 
Shares 
3.72% 
January 8, 2028 
 
MiniMax 
Matrix 
5,000,000 Class A Ordinary 
Shares 
1.62% 
January 8, 2028 
 
MiniMax 
Limited 
15 Class B Ordinary Shares 
0.000005% 
January 8, 2028 
 
Note: 
 

<<<PAGE 16>>>
16 
 
Name 
Number of Shares held in 
the Company subject to lock-
up 
undertakings 
upon 
Listing  
% of total issued Shares after the 
Global Offering upon Listing 
(after taking into account the full 
exercise 
of 
the 
Offer 
Size 
Adjustment Option and assuming 
the Over-allotment Option is not 
exercised) 
Last day subject to the 
lock-up undertakings 
Note 1 
1. The lock-up period commences on the date by reference to which disclosure of its shareholding is made in the 
Prospectus and ends on the date which is 24 months from the Listing Date, i.e. January 8, 2028. In the event 
that upon the notification by the Stock Exchange that the Company will no longer be regarded as a Pre-
Commercial Company after the Listing, the lock-up period will expire on the later of: (i) the date on which 
such lock-up periods would have ended if the Company had applied for listing as a Commercial Company; 
and (2) the date falling on the 30th day after the announcement on the removal of designation as a Pre-
Commercial Company as required under Rule 18C.24 of the Listing Rules. 
 
 
Existing Shareholders 
Name 
Number of Shares 
held 
in 
the 
Company subject 
to 
lock-up 
undertakings 
upon Listing  
% of total issued Class 
A 
Ordinary 
Shares 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
% 
of 
total 
issued 
Shares after the Global 
Offering upon Listing 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Last 
day 
subject to the 
lock-up 
undertakings 
Note 1 
MiniMax Gene 
Limited Note 3 
20,890,736 Class 
A Ordinary Shares 
9.16% 
6.76% 
the earlier of 
(i) 
the 
twentieth 
(20th) trading 
day 
starting 
from the date 
on which the 
Class 
A 
Ordinary 
Shares 
are 
included as an 
eligible stocks 
of 
Stock 
Connect 
and 
can be traded 
via 
Stock 
Connect of the 
Stock 
Exchange, 
or 
(ii) October 8, 
2026Note 2 
miHoYo 
Limited Note 4 and 
13 
16,015,779 Class 
A Ordinary Shares 
7.02% 
5.18% 
Shanghai 
Mihoyo 
Argo 
Technology 
Co., Ltd Note 4 and 
13 
1,912,399 Class A 
Ordinary Shares 
0.84% 
0.62% 
MPC VII Pte. 
Ltd. Note 13 
7,772,332 Class A 
Ordinary Shares 
3.41% 
2.51% 
Bravo 
Ideas 
Investments 
Limited Note 13 
3,633,558 Class A 
Ordinary Shares 
1.59% 
1.17% 
GW Investment 
Group Ltd. 
1,651,111 Class A 
Ordinary Shares 
0.72% 
0.53% 
Sidsi 
Holding 
Limited 
396,266 Class A 
Ordinary Shares 
0.17% 
0.13% 
Nanshan Alauda 
Limited 
723,208 Class A 
Ordinary Shares 
0.32% 
0.23% 

<<<PAGE 17>>>
17 
 
Name 
Number of Shares 
held 
in 
the 
Company subject 
to 
lock-up 
undertakings 
upon Listing  
% of total issued Class 
A 
Ordinary 
Shares 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
% 
of 
total 
issued 
Shares after the Global 
Offering upon Listing 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Last 
day 
subject to the 
lock-up 
undertakings 
Note 1 
Elephant Vision 
Technologies 
Limited 
330,222 Class A 
Ordinary Shares 
0.14% 
0.11% 
AIH Global Pte. 
Ltd. 
330,222 Class A 
Ordinary Shares 
0.14% 
0.11% 
CloudAlpha 
Master Fund 
792,533 Class A 
Ordinary Shares 
0.35% 
0.26% 
Yang 
Family 
Investments 
Limited 
198,133 Class A 
Ordinary Shares 
0.09% 
0.06% 
Futron 
Capital 
Limited 
330,222 Class A 
Ordinary Shares 
0.14% 
0.11% 
Nexus 
Vector 
Limited 
1,981,333 Class A 
Ordinary Shares 
0.87% 
0.64% 
Cosmic Station 
Limited Note 4 and 
13 
7,301,687 Class A 
Ordinary Shares 
3.20% 
2.36% 
July 8, 2026 
Seasonal Charm 
Limited Note 4 and 
13 
535,263 Class A 
Ordinary Shares 
0.23% 
0.17% 
July 8, 2026 
Alisoft 
China 
Holding 
Limited Note 13 
38,247,987 Class 
A Ordinary Shares 
16.76% 
12.37% 
July 8, 2026 
Image 
Frame 
Investment 
(HK) 
Limited 
Note 13 
7,232,084 Class A 
Ordinary Shares 
3.17% 
2.34% 
July 8, 2026 
XAM Holdings 
Limited Note 13 
14,201,184 Class 
A Ordinary Shares 
6.22% 
4.59% 
July 8, 2026 
MNM Holdings 
Limited Note 13 
2,343,196 Class A 
Ordinary Shares 
1.03% 
0.76% 
July 8, 2026 
Miheng 
Holdings 
Limited Note 5 
3,442,472 Class A 
Ordinary Shares 
1.51% 
1.11% 
July 8, 2026 
Himalia 
Holding 
Limited Note 13 
1,656,805 Class A 
Ordinary Shares 
0.73% 
0.54% 
July 8, 2026 
HSG 
Growth 
VII Holdco E, 
Ltd. Note 13 
9,011,235 Class A 
Ordinary Shares 
3.95% 
2.91% 
July 8, 2026 

<<<PAGE 18>>>
18 
 
Name 
Number of Shares 
held 
in 
the 
Company subject 
to 
lock-up 
undertakings 
upon Listing  
% of total issued Class 
A 
Ordinary 
Shares 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
% 
of 
total 
issued 
Shares after the Global 
Offering upon Listing 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Last 
day 
subject to the 
lock-up 
undertakings 
Note 1 
Astrend 
Opportunity IV 
Beta Limited Note 
13 
2,260,471 Class A 
Ordinary Shares 
0.99% 
0.73% 
July 8, 2026 
Astrend X Fund, 
L.P. Note 13 
1,446,417 Class A 
Ordinary Shares 
0.63% 
0.47% 
July 8, 2026 
Astrend 
X-2 
Limited Note 13 
814,054 Class A 
Ordinary Shares 
0.36% 
0.26% 
July 8, 2026 
Golden Horizon 
Limited Note 13 
411,097 Class A 
Ordinary Shares 
0.18% 
0.13% 
July 8, 2026 
Future 
Capital 
Discovery Fund 
IV, L.P. Note 13 
2,519,330 Class A 
Ordinary Shares 
1.10% 
0.81% 
July 8, 2026 
Ideafication 
Holdings 
L.P. 
Note 13 
1,111,903 Class A 
Ordinary Shares 
0.49% 
0.36% 
July 8, 2026 
Lingham 
Beauty Limited 
Note 6 
4,817,351 Class A 
Ordinary Shares 
2.11% 
1.56% 
July 8, 2026 
Forever 
Gain 
Limited Note 6 
478,100 Class A 
Ordinary Shares 
0.21% 
0.15% 
July 8, 2026 
China 
Life 
(Shenzhen) 
Technology 
Innovation 
Private 
Equity 
Investment 
Fund 
Partnership 
(Limited 
Partnership)( 國
壽( 深圳) 科技
創新私募股權
投資基金合夥
企業( 有限合
夥)) Note 7 
2,825,791 Class A 
Ordinary Shares 
1.24% 
0.91% 
July 8, 2026 
Hefei 
China 
Life 
Carbon 
Peak 
and 
330,021 Class A 
Ordinary Shares 
0.14% 
0.11% 
July 8, 2026 

<<<PAGE 19>>>
19 
 
Name 
Number of Shares 
held 
in 
the 
Company subject 
to 
lock-up 
undertakings 
upon Listing  
% of total issued Class 
A 
Ordinary 
Shares 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
% 
of 
total 
issued 
Shares after the Global 
Offering upon Listing 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Last 
day 
subject to the 
lock-up 
undertakings 
Note 1 
Carbon 
Neutrality Phase 
I 
Equity 
Investment 
Fund 
Partnership 
(Limited 
Partnership)( 合
肥國壽碳峰碳
中一期股權投
資基金合夥企
業(有限合夥)) 
Note 7 
Planetree 
PARTNERS 
HARVEST 
I, 
L.P. Note 8 
478,100 Class A 
Ordinary Shares 
0.21% 
0.15% 
July 8, 2026 
Planetree 
Partners III, L.P. 
Note 8 
2,154,046 Class A 
Ordinary Shares 
0.94% 
0.70% 
July 8, 2026 
Planetree 
Partners III-A, 
L.P. Note 8 
253,416 Class A 
Ordinary Shares 
0.11% 
0.08% 
July 8, 2026 
Star 
Bairui 
Holdings 
Limited 
2,438,309 Class A 
Ordinary Shares 
1.07% 
0.79% 
July 8, 2026 
Vitalbridge 
Fund II, L.P. 
2,280,734 Class A 
Ordinary Shares 
1.00% 
0.74% 
July 8, 2026 
Beijing Shunjin 
Shunying 
Enterprise 
Management 
Partnership 
(Limited 
Partnership) (北
京順金順贏企
業管理合夥企
業(有限合夥)) 
2,260,471 Class A 
Ordinary Shares 
0.99% 
0.73% 
July 8, 2026 

<<<PAGE 20>>>
20 
 
Name 
Number of Shares 
held 
in 
the 
Company subject 
to 
lock-up 
undertakings 
upon Listing  
% of total issued Class 
A 
Ordinary 
Shares 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
% 
of 
total 
issued 
Shares after the Global 
Offering upon Listing 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Last 
day 
subject to the 
lock-up 
undertakings 
Note 1 
Xinnuo Yuheng 
Ltd. 
1,912,399 Class A 
Ordinary Shares 
0.84% 
0.62% 
July 8, 2026 
Trend 
Xpand 
Limited 
1,446,417 Class A 
Ordinary Shares 
0.63% 
0.47% 
July 8, 2026 
Shanghai 
Lianxin 
Technology 
Equity 
Investment 
Center (Limited 
Partnership) (上
海聯新科技股
權投資中心(有
限合夥)) 
1,434,300 Class A 
Ordinary Shares 
0.63% 
0.46% 
July 8, 2026 
Anhui 
Transportation 
Holding CICC 
Industrial 
Development 
Fund 
Partnership 
(Limited 
Partnership) (安
徽交控中金產
業發展基金合
夥企業(有限合
夥)) Note 9 
217,000 Class A 
Ordinary Shares 
0.10% 
0.07% 
July 8, 2026 
Suzhou 
CICC 
SAIC Emerging 
Industry Equity 
Investment 
Fund 
Partnership 
(Limited 
Partnership) (蘇
州中金上汽新
興產業股權投
資基金合夥企
814,052 Class A 
Ordinary Shares 
0.36% 
0.26% 
July 8, 2026 

<<<PAGE 21>>>
21 
 
Name 
Number of Shares 
held 
in 
the 
Company subject 
to 
lock-up 
undertakings 
upon Listing  
% of total issued Class 
A 
Ordinary 
Shares 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
% 
of 
total 
issued 
Shares after the Global 
Offering upon Listing 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Last 
day 
subject to the 
lock-up 
undertakings 
Note 1 
業(有限合夥)) 
Note 9 
Shanghai 
Fortera 
FOF 
Investment 
Fund 
(Limited 
Partnership) (上
海國孚領航投
資合夥企業(有
限合夥)) Note 10 
814,054 Class A 
Ordinary Shares 
0.36% 
0.26% 
July 8, 2026 
Shanghai 
Modou Venture 
Capital 
Partnership 
(Limited 
Partnership) (上
海魔豆創業投
資合夥企業(有
限合夥)) Note 10 
445,800 Class A 
Ordinary Shares 
0.20% 
0.14% 
July 8, 2026 
Shenzhen 
Pengyuan 
Cornerstone 
Private 
Equity 
Investment 
Fund 
Partnership 
(Limited 
Partnership) (深
圳市鵬遠基石
私募股權投資
基金合夥企業
(有限合夥)) Note 
11 
552,394 Class A 
Ordinary Shares 
0.24% 
0.18% 
July 8, 2026 
Nanjing Lingyi 
Cornerstone 
Equity 
Investment 
Partnership 
220,958 Class A 
Ordinary Shares 
0.10% 
0.07% 
July 8, 2026 

<<<PAGE 22>>>
22 
 
Name 
Number of Shares 
held 
in 
the 
Company subject 
to 
lock-up 
undertakings 
upon Listing  
% of total issued Class 
A 
Ordinary 
Shares 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
% 
of 
total 
issued 
Shares after the Global 
Offering upon Listing 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Last 
day 
subject to the 
lock-up 
undertakings 
Note 1 
(Limited 
Partnership) (南
京領益基石股
權投資合夥企
業(有限合夥)) 
Note 11 
JointForce Fund 
I LP 
407,027 Class A 
Ordinary Shares 
0.18% 
0.13% 
July 8, 2026 
Shanghai 
Guangqihuichan 
Phase I Private 
Equity 
Investment 
Fund 
Partnership 
(Limited 
Partnership) (上
海光啟匯產一
期私募投資基
金合夥企業(有
限合夥)) 
1,298,626 Class A 
Ordinary Shares 
0.57% 
0.42% 
July 8, 2026 
Shanghai 
Guofang Kapa 
Enterprise 
Management 
Partnership 
(Limited 
Partnership)( 上
海國方卡帕企
業管理合夥企
業(有限合夥)) 
384,392 Class A 
Ordinary Shares 
0.17% 
0.12% 
July 8, 2026 
Cloud Maximus 
Limited 
334,670 Class A 
Ordinary Shares 
0.15% 
0.11% 
July 8, 2026 
Shanghai SSCI 
Leading 
Artificial 
Intelligence 
Private 
Equity 
891,599 Class A 
Ordinary Shares 
0.39% 
0.29% 
July 8, 2026 

<<<PAGE 23>>>
23 
 
Name 
Number of Shares 
held 
in 
the 
Company subject 
to 
lock-up 
undertakings 
upon Listing  
% of total issued Class 
A 
Ordinary 
Shares 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
% 
of 
total 
issued 
Shares after the Global 
Offering upon Listing 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Last 
day 
subject to the 
lock-up 
undertakings 
Note 1 
Investment 
Fund 
Partnership 
(Limited 
Partnership) (上
海國投先導人
工智能私募投
資基金合夥企
業(有限合夥) ) 
CMG 
Media 
Convergence 
Industry 
Investment 
Fund 
(Limited 
Partnership) (央
視融媒體產業
投資基金(有限
合夥)) 
891,599 Class A 
Ordinary Shares 
0.39% 
0.29% 
July 8, 2026 
Mentor 
Group 
Limited 
924,622 Class A 
Ordinary Shares 
0.41% 
0.30% 
July 8, 2026 
XEP-1 Holdings 
Limited 
2,971,999 Class A 
Ordinary Shares 
1.30% 
0.96% 
July 8, 2026 
TAL 
China 
Focus 
Master 
Fund 
1,320,888 Class A 
Ordinary Shares 
0.58% 
0.43% 
July 8, 2026 
Janchor Partners 
Pan-Asian 
Master Fund Note 
12 
2,044,706 Class A 
Ordinary Shares 
0.90% 
0.66% 
July 8, 2026 
Janchor Partners 
Opportunities 
Master Fund III 
Note 12 
332,893 Class A 
Ordinary Shares 
0.15% 
0.11% 
July 8, 2026 
China 
Orient 
Enhanced 
Income Fund 
1,320,888 Class A 
Ordinary Shares 
0.58% 
0.43% 
July 8, 2026 
Alliance 
Winford 
Limited 
1,320,888 Class A 
Ordinary Shares 
0.58% 
0.43% 
July 8, 2026 

<<<PAGE 24>>>
24 
 
Name 
Number of Shares 
held 
in 
the 
Company subject 
to 
lock-up 
undertakings 
upon Listing  
% of total issued Class 
A 
Ordinary 
Shares 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
% 
of 
total 
issued 
Shares after the Global 
Offering upon Listing 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Last 
day 
subject to the 
lock-up 
undertakings 
Note 1 
Jupiter 
Global 
Master 
Fund 
Ltd. 
541,564 Class A 
Ordinary Shares 
0.24% 
0.18% 
July 8, 2026 
CoreView 
Master 
Fund 
Limited 
990,666 Class A 
Ordinary Shares 
0.43% 
0.32% 
July 8, 2026 
LI 
FAMILY 
HOLDINGS 
PTE. LTD 
330,222 Class A 
Ordinary Shares 
0.14% 
0.11% 
July 8, 2026 
Charoen 
Pokphand 
Robot Limited 
1,981,333 Class A 
Ordinary Shares 
0.87% 
0.64% 
July 8, 2026 
Notes: 
 
1. The expiry date of the lock–up period shown in the table above is pursuant to the relevant Lock-up 
Undertakings as set out in the Prospectus. 
 
2. The lock-up period commences from the date of their respective Lock-up Undertakings or the date of the 
Prospectus and ending on a date which is the earlier of (i) the twentieth (20th) trading day starting from the 
date on which the Class A Ordinary Shares are included as an eligible stocks of Stock Connect and can be 
traded via Stock Connect of the Stock Exchange, or (ii) nine months from the Listing Date, subject to 
customary exceptions. 
 
3. being the Company's Employee Shareholding Platform. 
 
4. being one of the Company’s Pathfinder SIIs. In accordance with Rule 18C.14 of the Listing Rules, it also 
subject to the required lock-up period commences on the date by reference to which disclosure of its 
shareholding is made in the Prospectus and ends on the date which is 12 months from the Listing Date, i.e. 
January 8, 2027. 
 
5. Miheng Holdings Limited is an exempted company with limited liability incorporated under the laws of 
Cayman Islands, which is wholly controlled by Beijing Miheng Enterprise Management Consulting 
Partnership (Limited Partnership) (北京觅恒企业管理咨询合伙企业（有限合伙）) (“Beijing Miheng
”). The general partner of Beijing Miheng is Wuxi Ningjun Enterprise Management Co., Ltd. (无锡宁袀
企业管理有限公司), which is controlled by Zhuhai Gao Ling Private Fund Management Co., Ltd. The 
limited partners of Beijing Miheng are five private equity funds that are record-filed with Asset 
Management Association of China. There is no individual who directly or indirectly holds an interest of 
30% or more in Beijing Miheng. 
 
6. These entities are under common control. 
 
7.  All the entities are ultimately controlled by China Life Insurance (Group) Company (中國人壽保險(集
團)公司). 

<<<PAGE 25>>>
25 
 
Name 
Number of Shares 
held 
in 
the 
Company subject 
to 
lock-up 
undertakings 
upon Listing  
% of total issued Class 
A 
Ordinary 
Shares 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
% 
of 
total 
issued 
Shares after the Global 
Offering upon Listing 
(after 
taking 
into 
account 
the 
full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Last 
day 
subject to the 
lock-up 
undertakings 
Note 1 
 
8. All the entities are under Planetree Partners. 
 
9. The executive partners of both entitles are subsidiaries of China International Capital Corporation Limited 
(中國國際金融股份有限公司). 
 
10. These entities are under common control. 
 
11. These entities are under common control. 
 
12. These entities are under common control. 
 
13. For details of the background of relevant Shareholders, please refer to the section headed “History, 
Reorganization and Corporate Structure – Pre-IPO Investments – 4. Information relating to our key Pre-
IPO Investor”. 
 
14. The above notes, where applicable, reflect the latest and current shareholding structure of relevant 
Shareholders as of the date of this announcement. 
 
 
Cornerstone Investors 
Name 
Number of Offer 
Shares held in 
the 
Company 
subject to lock-up 
undertakings 
upon Listing 
% of total issued 
Class A Ordinary 
Shares 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
% 
of 
total 
issued 
Shares 
after 
the 
Global Offering upon 
Listing (after taking 
into account the full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Last day subject to the 
lock-up undertakings 
Note 1 
ADIA 
3,065,040 
1.34% 
0.99% 
July 8, 2026 
Alisoft China 
1,414,640 
0.62% 
0.46% 
July 8, 2026 
Aspex Master 
Fund  
1,650,400 
0.72% 
0.53% 
July 8, 2026 
Abstract 
Enigma 
Limited 
1,650,400 
0.72% 
0.53% 
July 8, 2026 

<<<PAGE 26>>>
26 
 
Name 
Number of Offer 
Shares held in 
the 
Company 
subject to lock-up 
undertakings 
upon Listing 
% of total issued 
Class A Ordinary 
Shares 
(after 
taking 
into 
account the full 
exercise of the 
Offer 
Size 
Adjustment 
Option 
and 
assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
% 
of 
total 
issued 
Shares 
after 
the 
Global Offering upon 
Listing (after taking 
into account the full 
exercise of the Offer 
Size 
Adjustment 
Option and assuming 
the 
Over-allotment 
Option 
is 
not 
exercised) 
Last day subject to the 
lock-up undertakings 
Note 1 
China 
Universal 
(HK) 
707,320 
0.31% 
0.23% 
July 8, 2026 
Eastspring 
707,320 
0.31% 
0.23% 
July 8, 2026 
E Fund 
Management 
471,540 
0.21% 
0.15% 
July 8, 2026 
IDG Breyer 
Fund 
707,320 
0.31% 
0.23% 
July 8, 2026 
Janchor Funds 
1,650,400 
0.72% 
0.53% 
July 8, 2026 
Martis Fund, 
L.P. 
707,320  
0.31% 
0.23% 
July 8, 2026 
Mirae Asset 
Securities 
943,080  
0.41% 
0.30% 
July 8, 2026 
MPC VII 
707,320  
0.31% 
0.23% 
July 8, 2026 
Perseverance 
Asset 
Management 
1,178,860  
0.52% 
0.38% 
July 8, 2026 
Taikang Life 
943,080  
0.41% 
0.30% 
July 8, 2026 
Total 
16,504,040  
7.23% 
5.34% 
July 8, 2026 
Note: 
 
1. 
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on July 8, 2026. 
The Cornerstone Investors will cease to be prohibited from disposing of or transferring the Class A Ordinary 
Shares subscribed for pursuant to the relevant cornerstone investment agreements after the indicated date. 
 

<<<PAGE 27>>>
27 
 
PLACEE CONCENTRATION ANALYSIS** 
Placees* 
Number of 
Class A 
Ordinary 
Shares 
allotted 
Allotment 
as % of the 
International 
Offering 
(assuming no 
exercise of 
the Over-
allotment 
Option) 
Allotment 
as % of the 
International 
Offering 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised 
and new 
Class A 
Ordinary 
Shares are 
issued) 
Allotment 
as % of 
total 
Offer 
Shares 
(assuming 
no 
exercise 
of the 
Over- 
allotment 
Option) 
Allotment 
as % of 
total Offer 
Shares 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised 
and new 
Class A 
Ordinary 
Shares are 
issued) 
Number of 
Class A 
Ordinary 
Shares held 
upon Listing 
% of total 
issued 
Class A 
Ordinary 
Shares 
upon 
Listing 
(assuming 
no exercise 
of the 
Over-
allotment 
Option) 
% of total 
issued 
Class A 
Ordinary 
Shares 
upon 
Listing 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised 
and new 
Class A 
Ordinary 
Shares are 
issued) 
% of total 
issued 
share 
capital 
upon 
Listing 
(assuming 
no exercise 
of the 
Over-
allotment 
Option) 
% of total 
issued share 
capital upon 
Listing 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised 
and new 
Class A 
Ordinary 
Shares are 
issued) 
Top 1 
 3,543,516  
14.69% 
12.43% 
12.14% 
10.55% 
 3,543,516  
1.55% 
1.52% 
1.15% 
1.13% 
Top 5 
 10,521,056  
43.62% 
36.92% 
36.03% 
31.33% 
 17,851,987  
7.82% 
7.68% 
5.77% 
5.69% 
Top 10 
 15,708,036  
65.13% 
55.12% 
53.80% 
46.78% 
 69,059,286  
30.27% 
29.70% 
22.33% 
22.02% 
Top 25 
 24,178,736  
100.24% 
84.84% 
82.81% 
72.01% 
 99,369,817  
43.55% 
42.73% 
32.13% 
31.68% 
 
Notes: 
* Ranking of placees is based on the number of Offer Shares allotted to the placees. 
** Taking into account the full exercise of the Offer Size Adjustment Option. 
 
 

<<<PAGE 28>>>
 
28 
 
CLASS A SHAREHOLDER CONCENTRATION ANALYSIS** 
Class A 
Shareholder* 
Number 
of Class A 
Ordinary 
Shares 
allotted 
Allotment 
as % of the 
International 
Offering 
(assuming no 
exercise of the 
Over-
allotment 
Option) 
Allotment 
as % of the 
International 
Offering 
(assuming the 
Over-
allotment 
Option is fully 
exercised and 
new Class A 
Ordinary 
Shares are 
issued) 
Allotment 
as % of 
total Offer 
Shares 
(assuming 
no exercise 
of the 
Over- 
allotment 
Option) 
Allotment 
as % of 
total Offer 
Shares 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised 
and new 
Class A 
Ordinary 
Shares are 
issued) 
Number of 
Class A 
Ordinary 
Shares 
held upon 
Listing 
% of total 
issued 
Class A 
Ordinary 
Shares 
upon 
Listing 
(assuming 
no exercise 
of the 
Over-
allotment 
Option) 
% of total 
issued 
Class A 
Ordinary 
Shares 
upon 
Listing 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised 
and new 
Class A 
Ordinary 
Shares are 
issued) 
% of total 
issued 
share 
capital 
upon 
Listing 
(assuming 
no exercise 
of the 
Over-
allotment 
Option) 
% of total 
issued 
share 
capital 
upon 
Listing 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised 
and new 
Class A 
Ordinary 
Shares are 
issued) 
Top 1 
 1,414,640  
5.87% 
4.96% 
4.85% 
4.21% 
39,662,627  
17.38% 
17.06% 
12.83% 
12.65% 
Top 5 
 1,914,500  
7.94% 
6.72% 
6.56% 
5.70% 106,193,821  
46.54% 
45.67% 
34.34% 
33.86% 
Top 10 
 3,329,140  
13.80% 
11.68% 
11.40% 
9.91% 140,745,278  
61.69% 
60.53% 
45.51% 
44.88% 
Top 25 
 13,852,816  
57.43% 
48.61% 
47.45% 
41.26% 189,241,408  
82.94% 
81.38% 
61.19% 
60.34% 
 
Notes: 
* Ranking of Class A Shareholders is based on the number of Class A Ordinary Shares held by the Class A Shareholders upon Listing. 
** Taking into account the full exercise of the Offer Size Adjustment Option. 
 
 
 

<<<PAGE 29>>>
 
29 
 
SHAREHOLDER CONCENTRATION ANALYSIS** 
Shareholder* 
Number of 
Class A 
Ordinary 
Shares 
allotted 
Allotment as % 
of the 
International 
Offering 
(assuming no 
exercise of the 
Over-allotment 
Option) 
Allotment as % 
of the 
International 
Offering 
(assuming the 
Over-allotment 
Option is fully 
exercised and 
new Class A 
Ordinary 
Shares are 
issued) 
Allotment 
as % of 
total Offer 
Shares 
(assuming 
no exercise 
of the Over- 
allotment 
Option) 
Allotment 
as % of 
total Offer 
Shares 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised 
and new 
Class A 
Ordinary 
Shares are 
issued) 
Number of 
Class A 
Ordinary 
Shares held 
upon 
Listing 
Number of 
total Shares 
held upon 
Listing 
% of total 
issued share 
capital 
upon 
Listing 
(assuming 
no exercise 
of the Over-
allotment 
Option) 
% of total 
issued 
share 
capital 
upon 
Listing 
(assuming 
the Over-
allotment 
Option is 
fully 
exercised 
and new 
Class A 
Ordinary 
Shares are 
issued) 
Top 1 
 -   
0.00% 
0.00% 
0.00% 
0.00% 
5,000,000  
 79,102,534  
25.58% 
25.22% 
Top 5 
 1,890,940  
7.84% 
6.64% 
6.48% 
5.63% 
100,025,921   174,128,455 
56.31% 
55.52% 
Top 10 
 2,621,820  
10.87% 
9.20% 
8.98% 
7.81% 
134,266,207   215,368,741  
69.64% 
68.67% 
Top 25 
 13,852,816  
57.43% 
48.61% 
47.45% 
41.26% 
186,783,775   267,886,309 
86.62% 
85.41% 
 
Notes: 
* Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholders upon Listing. 
** Taking into account the full exercise of the Offer Size Adjustment Option. 
 

<<<PAGE 30>>>
30 
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING 
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below:  
 
NO. 
OF 
OFFER 
SHARES 
APPLIED 
FOR 
NO. OF VALID 
APPLICATIONS 
BASIS OF ALLOTMENT / 
BALLOT 
APPROXIMATE 
PERCENTAGE 
ALLOTTED OF THE 
TOTAL 
NO. 
OF 
OFFER 
SHARES 
APPLIED FOR 
POOL A 
20 
139,314 
3,911 out of 139,314 applicants to 
receive 20 shares 
2.81% 
40 
39,265 
1,582 out of 39,265 applicants to 
receive 20 shares 
2.01% 
60 
23,720 
1,135 out of 23,720 applicants to 
receive 20 shares 
1.59% 
80 
7,002 
412 out of 7,002 applicants to 
receive 20 shares 
1.47% 
100 
10,391 
716 out of 10,391 applicants to 
receive 20 shares 
1.38% 
120 
7,508 
589 out of 7,508 applicants to 
receive 20 shares 
1.31% 
140 
4,698 
411 out of 4,698 applicants to 
receive 20 shares 
1.25% 
160 
4,622 
445 out of 4,622 applicants to 
receive 20 shares 
1.20% 
180 
5,194 
544 out of 5,194 applicants to 
receive 20 shares 
1.16% 
200 
32,223 
3,634 out of 32,223 applicants to 
receive 20 shares 
1.13% 
300 
15,651 
2,357 out of 15,651 applicants to 
receive 20 shares 
1.00% 
400 
7,267 
1,343 out of 7,267 applicants to 
receive 20 shares 
0.92% 
500 
4,760 
1,032 out of 4,760 applicants to 
receive 20 shares 
0.87% 
600 
7,570 
1,868 out of 7,570 applicants to 
receive 20 shares 
0.82% 
700 
3,843 
1,058 out of 3,843 applicants to 
receive 20 shares 
0.79% 
800 
3,291 
997 out of 3,291 applicants to 
receive 20 shares 
0.76% 
900 
2,495 
822 out of 2,495 applicants to 
receive 20 shares 
0.73% 
1,000 
16,195 
5,748 out of 16,195 applicants to 
receive 20 shares 
0.71% 
2,000 
11,308 
6,576 out of 11,308 applicants to 
receive 20 shares 
0.58% 
3,000 
7,187 
5,579 out of 7,187 applicants to 
receive 20 shares 
0.52% 
4,000 
5,704 
20 shares 
0.50% 

<<<PAGE 31>>>
31 
 
5,000 
5,035 
20 shares plus 589 out of 5,035 
applicants to receive an additional 
20 shares 
0.45% 
6,000 
4,273 
20 shares plus 1,162 out of 4,273 
applicants to receive an additional 
20 shares 
0.42% 
7,000 
2,845 
20 shares plus 1,194 out of 2,845 
applicants to receive an additional 
20 shares 
0.41% 
8,000 
2,524 
20 shares plus 1,417 out of 2,524 
applicants to receive an additional 
20 shares 
0.39% 
9,000 
1,855 
20 shares plus 1,295 out of 1,855 
applicants to receive an additional 
20 shares 
0.38% 
10,000 
10,634 
20 shares plus 8,827 out of 10,634 
applicants to receive an additional 
20 shares 
0.37% 
20,000 
6,429 
40 shares plus 6,419 out of 6,429 
applicants to receive an additional 
20 shares 
0.30% 
30,000 
4,886 
80 shares plus 13 out of 4,886 
applicants to receive an additional 
20 shares 
0.27% 
Total 
397,689 
Total number of Pool A 
successful applicants: 84,944 
POOL B 
40,000 
9,721 
100 shares 
0.25% 
50,000 
2,163 
100 shares plus 1,099 out of 2,163 
applicants to receive an additional 
20 shares 
0.22% 
60,000 
1,555 
100 shares plus 1,494 out of 1,555 
applicants to receive an additional 
20 shares 
0.20% 
70,000 
1,027 
120 shares plus 383 out of 1,027 
applicants to receive an additional 
20 shares 
0.18% 
80,000 
759 
120 shares plus 571 out of 759 
applicants to receive an additional 
20 shares 
0.17% 
90,000 
548 
140 shares plus 58 out of 548 
applicants to receive an additional 
20 shares 
0.16% 
100,000 
2,167 
140 shares plus 949 out of 2,167 
applicants to receive an additional 
20 shares 
0.15% 
200,000 
864 
200 shares plus 38 out of 864 
applicants to receive an additional 
20 shares 
0.10% 
300,000 
344 
220 shares plus 335 out of 344 
applicants to receive an additional 
20 shares 
0.08% 

<<<PAGE 32>>>
32 
 
400,000 
172 
260 shares plus 97 out of 172 
applicants to receive an additional 
20 shares 
0.07% 
500,000 
128 
280 shares plus 121 out of 128 
applicants to receive an additional 
20 shares 
0.06% 
634,740 
509 
320 shares plus 289 out of 509 
applicants to receive an additional 
20 shares 
0.05% 
Total 
19,957 
Total 
number 
of 
Pool 
B 
successful applicants: 19,957 
 
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries. 
  
COMPLIANCE WITH LISTING RULES AND GUIDANCE  
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Class A Ordinary Shares.  
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees or the 
public (as the case may be) directly or indirectly for each Offer Share subscribed for or purchased by 
them is the same as the final Offer Price in addition to any brokerage, AFRC transaction levy, SFC 
transaction levy and trading fee payable. 
The Directors and the Overall Coordinators confirm that at least 50% of the total number of the Offer 
Shares have been allocated to and taken up by independent price setting investors in compliance with 
Rule 18C.08 of the Listing Rules.  
The Directors further confirm that at least 20% of the issued share capital of the Company will be held 
by sophisticated independent investors at the time of Listing in compliance with Chapter 2.5 of the 
Guide for New Listing Applicants. 
OTHERS / ADDITIONAL INFORMATION 
 
Offer Size Adjustment Option 
 
The Offer Size Adjustment Option has been exercised in full, pursuant to which the Company is issuing 
and allotting 3,808,380 additional Offer Shares, representing approximately 15% of the total number 
of Offer Shares initially available under the Global Offering, at the final Offer Price to increase the 
number of Offer Shares available under the International Offering.  
 
Accordingly, the total number of Offer Shares available under the Global Offering (after taking into 
account the full exercise of the Offer Size Adjustment Option and before any exercise of the Over-
allotment Option) that would be allotted and issued by the Company is 29,197,600 Offer Shares and 
the total issued share capital of the Company upon Listing (after taking into account the full exercise 
of the Offer Size Adjustment Option and before any exercise of the Over-allotment Option) will be 
309,255,668 Shares.  
 

<<<PAGE 33>>>
33 
 
Reallocation 
 
As the Hong Kong Public Offering has been over-subscribed by more than 1,800 times of the total 
number of Offer Shares initially available under the Hong Kong Public Offering, the reallocation 
procedure as disclosed in the section headed “Structure of the Global Offering – The Hong Kong 
Public Offering – Reallocation” in the Prospectus has been applied.  
 
The number of Offer Shares initially available under the Hong Kong Public Offering is 1,269,480 
Offer Shares, representing approximately 5% of the total number of Offer Shares initially available 
under the Global Offering (assuming the Offer Size Adjustment Option and the Over-allotment Option 
are not exercised). As a result of such reallocation, the final number of Offer Shares under the Hong 
Kong Public Offering is adjusted to 5,077,860 Offer Shares, representing approximately 20% of the 
total number of Offer Shares initially available under the Global Offering (assuming the Offer Size 
Adjustment Option and the Over-allotment Option are not exercised). 
 
Placing to existing shareholders and/or its close associates with a prior waiver under Rule 10.04 
and consent under paragraph 1C(2) of the Placing Guidelines 
 
The Company has applied for a waiver under Rule 10.04 of the Listing Rules and a consent under 
paragraph 1C(2) of Appendix F1 to the Listing Rules, to permit the existing shareholders and/or its 
close associates to participate as either cornerstone investors or placees in the Global Offering to 
subscribe for the Offer Shares to be issued by the Company under the International Offering (together, 
the “Existing Shareholder Participants”). The Stock Exchange has agreed to grant the requested 
waiver and consent subject to the conditions that:  
 
(a) the allocation to the Existing Shareholder Participants will not affect the Company’s ability to 
satisfy relevant requirements under Rules 8.08(1), 18C.08 and 8.08A of the Listing Rules, 
respectively;  
 
(b) the Company and the Joint Sponsors confirm that no preferential treatment has been, nor will be 
directly or indirectly, given to the Existing Shareholder Participants as cornerstone investors or 
placees by virtue of their relationship with the Company in any allocation in the Global Offering, 
other than the preferential treatment of assured entitlement under the cornerstone investment at the 
Offer Price and the terms are substantially the same as other cornerstone investors; and  
 
(c) details of the subscription of the Offer Shares by the Existing Shareholder Participants as 
cornerstone investors or placees under the Global Offering have been disclosed in the Prospectus, 
and details of the allocation are disclosed in this allotment results announcement of the Company. 
 
For details of the allocations of Offer Shares to such Existing Shareholder Participants, please refer to 
the section headed “Allotment Results Details – International Offering – Allotees with 
Waivers/Consents Obtained” in this announcement. 
 
Placing to connected clients with a prior consent under paragraph 1C(1) of the Placing 
Guidelines 
 
Under the International Offering, certain Offer Shares were placed to connected clients of their 
connected distributors pursuant to the Placing Guidelines.  
 

<<<PAGE 34>>>
34 
 
The Company has applied to the Stock Exchange for, and the Stock Exchange has granted, a consent 
under paragraph 1C(1) of the Placing Guidelines to permit the Company to allocate such Offer Shares 
in the International Offering to the connected clients. The allocation of Offer Shares to such connected 
clients is in compliance with all the conditions under the consent granted by the Stock Exchange. 
Details of the placement to connected clients are set out below: 

<<<PAGE 35>>>
35 
 
No. 
Connected 
Distributor 
Connecte
d Client 
Relationship 
Identities of the 
ultimate 
beneficial 
owners of the 
Offer Shares or, 
where 
applicable, 
details of the 
structured 
products under 
which the 
subscription by 
the Connected 
Client was 
made (e.g. OTC 
total return 
swaps) 
Whether the 
Connected 
Client is a 
collective 
investment 
scheme which 
is not 
authorised by 
the SFC or is 
expected to 
hold the Offer 
Shares on 
behalf of such 
scheme 
Amount of 
Offer Shares 
to be 
allocated to 
the 
Connected 
Client 
Approximate 
percentage of 
total number of 
Offer Shares 
under the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming no 
exercise of the 
Over-allotment 
Option) 
Approximate 
percentage of 
total issued 
Class A 
Ordinary 
Shares under 
the Global 
Offering (after 
taking into 
account the full 
exercise of the 
Offer Size 
Adjustment 
Option and 
assuming no 
exercise of the 
Over-allotment 
Option) 
Approximate 
percentage of 
total issued 
share capital 
immediately 
following the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is not 
exercised) 
Part A - Connected Client holding the beneficial interest of the Offer Shares on a non-discretionary basis on behalf of independent third parties 
1. 
China 
International 
Capital 
Corporation 
Hong Kong 
Securities 
Limited 
(CICCHKS) 
CICC 
Financial 
Trading 
Limited 
(CICC 
FT) (Note 
1) 
CICCFT is a 
member of 
the same 
group as 
CICCHKS. 
Please refer to 
Note (1). 
N 
24,760 
0.08% 
0.01% 
0.01% 
2. 
Guotai Junan 
Securities 
(Hong Kong) 
Limited 
(GTJA HK)  
Guotai 
Junan 
Investme
nts (Hong 
Kong) 
Limited 
(GTJA 
Investme
GTJA 
Investment is 
a member of 
the same 
group as 
GTJA HK. 
Please refer to 
Note (2). 
N 
18,100 
0.06% 
0.01% 
0.01% 

<<<PAGE 36>>>
36 
 
No. 
Connected 
Distributor 
Connecte
d Client 
Relationship 
Identities of the 
ultimate 
beneficial 
owners of the 
Offer Shares or, 
where 
applicable, 
details of the 
structured 
products under 
which the 
subscription by 
the Connected 
Client was 
made (e.g. OTC 
total return 
swaps) 
Whether the 
Connected 
Client is a 
collective 
investment 
scheme which 
is not 
authorised by 
the SFC or is 
expected to 
hold the Offer 
Shares on 
behalf of such 
scheme 
Amount of 
Offer Shares 
to be 
allocated to 
the 
Connected 
Client 
Approximate 
percentage of 
total number of 
Offer Shares 
under the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming no 
exercise of the 
Over-allotment 
Option) 
Approximate 
percentage of 
total issued 
Class A 
Ordinary 
Shares under 
the Global 
Offering (after 
taking into 
account the full 
exercise of the 
Offer Size 
Adjustment 
Option and 
assuming no 
exercise of the 
Over-allotment 
Option) 
Approximate 
percentage of 
total issued 
share capital 
immediately 
following the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is not 
exercised) 
nts) (Note 
2)  
3. 
CITIC 
Securities 
Brokerage 
(HK) Limited 
(CSB) 
CITIC 
Securities 
Internatio
nal 
Capital 
Managem
ent 
Limited 
(CSI) 
(Note 3) 
CSI is a 
member of 
the same 
group of 
companies as 
CSB. 
Please refer to 
Note (3). 
N 
940 
0.00% 
0.00% 
0.00% 
4. 
Huatai 
Financial 
Holdings 
(Hong Kong) 
Huatai 
Capital 
Investme
nt 
Limited 
HTCI is a 
member of 
the same 
group of 
HTFH. 
Please refer to 
Note (4). 
N 
10,040 
0.03% 
0.00% 
0.00% 

<<<PAGE 37>>>
37 
 
No. 
Connected 
Distributor 
Connecte
d Client 
Relationship 
Identities of the 
ultimate 
beneficial 
owners of the 
Offer Shares or, 
where 
applicable, 
details of the 
structured 
products under 
which the 
subscription by 
the Connected 
Client was 
made (e.g. OTC 
total return 
swaps) 
Whether the 
Connected 
Client is a 
collective 
investment 
scheme which 
is not 
authorised by 
the SFC or is 
expected to 
hold the Offer 
Shares on 
behalf of such 
scheme 
Amount of 
Offer Shares 
to be 
allocated to 
the 
Connected 
Client 
Approximate 
percentage of 
total number of 
Offer Shares 
under the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming no 
exercise of the 
Over-allotment 
Option) 
Approximate 
percentage of 
total issued 
Class A 
Ordinary 
Shares under 
the Global 
Offering (after 
taking into 
account the full 
exercise of the 
Offer Size 
Adjustment 
Option and 
assuming no 
exercise of the 
Over-allotment 
Option) 
Approximate 
percentage of 
total issued 
share capital 
immediately 
following the 
Global Offering 
(after taking 
into account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming the 
Over-allotment 
Option is not 
exercised) 
Limited 
(HTFH) 
(HTCI) 
(Note 4) 
 

<<<PAGE 38>>>
38 
 
No. Connected 
Distributor 
Connected 
Client 
Relationship 
Whether the 
Connected Client is a 
collective investment 
scheme which is not 
authorised by the 
SFC or is expected to 
hold the Offer Shares 
on behalf of such 
scheme 
Amount of 
Offer Shares 
to be 
allocated to 
the 
Connected 
Client 
Approximate 
percentage of 
total number 
of Offer 
Shares under 
the Global 
Offering (after 
taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming no 
exercise of the 
Over-
allotment 
Option) 
Approximate 
percentage of 
total issued 
Class A 
Ordinary 
Shares under 
the Global 
Offering (after 
taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming no 
exercise of the 
Over-
allotment 
Option) 
Approximate 
percentage of 
total issued 
share capital 
immediately 
following the 
Global 
Offering (after 
taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming the 
Over-
allotment 
Option is not 
exercised) 
Part B - Connected Clients holding the beneficial interest of the Offer Shares on a discretionary basis on behalf of independent third parties 
1. 
CMB 
International 
Securities 
Limited and 
CMB 
International 
Global 
Markets 
Limited 
(collectively, 
CMBI) and 
China 
Merchants 
Securities 
Bosera Asset 
Management 
(International) 
Co., Ltd 
(Bosera AM) 
(Note 5) 
Bosera AM is a 
member of the 
same group of 
CMBI and CMS 
HK. 
N 
9,400 
0.03% 
0.00% 
0.00% 

<<<PAGE 39>>>
39 
 
No. Connected 
Distributor 
Connected 
Client 
Relationship 
Whether the 
Connected Client is a 
collective investment 
scheme which is not 
authorised by the 
SFC or is expected to 
hold the Offer Shares 
on behalf of such 
scheme 
Amount of 
Offer Shares 
to be 
allocated to 
the 
Connected 
Client 
Approximate 
percentage of 
total number 
of Offer 
Shares under 
the Global 
Offering (after 
taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming no 
exercise of the 
Over-
allotment 
Option) 
Approximate 
percentage of 
total issued 
Class A 
Ordinary 
Shares under 
the Global 
Offering (after 
taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming no 
exercise of the 
Over-
allotment 
Option) 
Approximate 
percentage of 
total issued 
share capital 
immediately 
following the 
Global 
Offering (after 
taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming the 
Over-
allotment 
Option is not 
exercised) 
(HK) Co., 
Ltd (CMS 
HK) 
2. 
CSB 
China Asset 
Management 
(Hong Kong) 
Limited (China 
AMC HK) 
(Note 6) 
CSB, China 
AMC HK and 
China AMC are 
members of the 
same group. 
N 
23,560 
0.08% 
0.01% 
0.01% 
3. 
China Asset 
Management 
Co., Ltd. 
(China AMC) 
(Note 7) 
N 
71,000 
0.24% 
0.03% 
0.02% 

<<<PAGE 40>>>
40 
 
No. Connected 
Distributor 
Connected 
Client 
Relationship 
Whether the 
Connected Client is a 
collective investment 
scheme which is not 
authorised by the 
SFC or is expected to 
hold the Offer Shares 
on behalf of such 
scheme 
Amount of 
Offer Shares 
to be 
allocated to 
the 
Connected 
Client 
Approximate 
percentage of 
total number 
of Offer 
Shares under 
the Global 
Offering (after 
taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming no 
exercise of the 
Over-
allotment 
Option) 
Approximate 
percentage of 
total issued 
Class A 
Ordinary 
Shares under 
the Global 
Offering (after 
taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming no 
exercise of the 
Over-
allotment 
Option) 
Approximate 
percentage of 
total issued 
share capital 
immediately 
following the 
Global 
Offering (after 
taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming the 
Over-
allotment 
Option is not 
exercised) 
4. 
CITIC 
Securities Asset 
Management 
Company 
Limited 
(CITICS AM) 
(Note 8) 
N 
480 
0.00% 
0.00% 
0.00% 
5. 
UBS AG 
Hong Kong 
Branch 
(UBS AG) 
ICBC UBS 
Asset 
Management 
(International) 
Company 
Limited (ICBC 
UBS 
ICBC UBS 
(International) is 
a member of the 
same group of 
companies as 
UBS AG. 
N 
1,400 
0.00% 
0.00% 
0.00% 

<<<PAGE 41>>>
41 
 
No. Connected 
Distributor 
Connected 
Client 
Relationship 
Whether the 
Connected Client is a 
collective investment 
scheme which is not 
authorised by the 
SFC or is expected to 
hold the Offer Shares 
on behalf of such 
scheme 
Amount of 
Offer Shares 
to be 
allocated to 
the 
Connected 
Client 
Approximate 
percentage of 
total number 
of Offer 
Shares under 
the Global 
Offering (after 
taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming no 
exercise of the 
Over-
allotment 
Option) 
Approximate 
percentage of 
total issued 
Class A 
Ordinary 
Shares under 
the Global 
Offering (after 
taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming no 
exercise of the 
Over-
allotment 
Option) 
Approximate 
percentage of 
total issued 
share capital 
immediately 
following the 
Global 
Offering (after 
taking into 
account the 
full exercise of 
the Offer Size 
Adjustment 
Option and 
assuming the 
Over-
allotment 
Option is not 
exercised) 
(International))  
(Note 9) 
 
Notes: 
 
1) 
CICC FT and CICC will enter into a series of cross border delta-one OTC equity swap transactions (collectively, the CICCFT OTC Swaps) with each 
other and the ultimate clients (the CICC FT Ultimate Clients), pursuant to which CICC FT will hold the Offer Shares on a non-discretionary basis to 
hedge the CICCFT OTC Swaps  while the economic risks and returns of the underlying Offer Shares are passed to the CICC FT Ultimate Client, subject 
to customary fees and commissions. The CICCFT OTC Swaps will be fully funded by the CICC FT Ultimate Clients. During the term (which is one 
year although the CICC FT Ultimate Clients can terminate anytime) of the CICCFT OTC Swaps , all economic returns of the Offer Shares subscribed 
by CICC FT as Connected Client will be passed to the CICC FT Ultimate Clients and all economic losses shall be borne by the CICC FT Ultimate 
Clients through the CICCFT OTC Swaps , and CICC FT will not take part in any economic return or bear any economic loss in relation to the Offer 
Shares. The termination of the CICCFT OTC Swaps will not result CICC FT holding the Offer Shares in its proprietary account. Despite that CICC FT 
will hold the legal title of the Offer Shares by itself, it will not exercise the voting rights attaching to the relevant Offer Shares during the terms of the 

<<<PAGE 42>>>
42 
 
CICCFT OTC Swaps according to its internal policy. Consequently, CICC FT Ultimate Client is not entitled to any voting rights of the relevant Offer 
Shares.  
The CICCFT OTC Swaps  are linked to performance of the Offer Shares and the CICC FT Ultimate Clients may, after expiration of the lock-up period 
beginning from the date of the cornerstone agreement entered into between CICC FT and the Company and ending on the date which is six months 
from the Listing Date, request to early terminate the CICCFT OTC Swaps  at their own discretions, upon which CICC FT may dispose of the Offer 
Shares and settle the CICCFT OTC Swaps  in cash in accordance with the terms and conditions of the CICCFT OTC Swaps. Despite that CICC FT will 
hold the legal title of the Offer Shares by itself, it will not exercise the voting rights attaching to the relevant Offer Shares during the terms of the 
CICCFT OTC Swaps according to its internal policy. Consequently, the CICC FT Ultimate Clients is not entitled to any voting rights of the relevant 
Offer Shares.  
Details of the CICC FT Ultimate Clients are set out as below:  
Name of the CICC FT Ultimate Client 
Ultimate beneficial owner(s) 
holding 30% or more interest (if 
any) 
Evolution Darwin Shangshan No.3 Private Securities Investment Fund (進化論達爾文上善三號私募證券投
資基金) 
NA 
Qinchen Senyu No.1 Private Securities Investment Fund (勤辰森裕1 號私募證券投資基金) 
NA 
Qinchen Senyu No.2 Private Securities Investment Fund (勤辰森裕2 號私募證券投資基金) 
NA 
Qinchen Senyu No.3 Private Securities Investment Fund (勤辰森裕3 號私募證券投資基金) 
NA 
Qinchen Jinxuan Senyu No.1 Private Securities Investment Fund (勤辰金選森裕1 號私募證券投資基金) 
NA 
Qinchen Jiaxuan Senyu No.1 Private Securities Investment Fund (勤辰嘉選森裕1 號私募證券投資基金) 
NA 
Baoyin Jinqu No.1 Private Securities Investment Fund (保銀進取1 號私募證券投資基金) 
NA 
Baoyin Long-Short Stable No.1 Private Securities Investment Fund (保銀多空穩健1 號私募證券投資基金) WANG Qiang(王强) 
Baoyin Long-Short Stable No.2 Private Securities Investment Fund (保銀多空穩健2 號私募證券投資基金) WANG Qiang(王强) 
 
To the best of CICC FT’s knowledge having made all reasonable inquiries, each of the CICC FT Ultimate Clients and their respective ultimate beneficial 
owner holding 30% or more interest is an independent third party of CICC FT, CICCHKS and the companies which are members of the same group of 
CICCHKS. 
2) 
GTJA HK is a distributor in connection with the Global Offering.  
It is proposed that GTJA Investments participates as placee to subscribe for the Offer Shares under the International Offering (the GTJAI Subscription). 
In relation to the GTJAI Subscription, GTJA Investments shall hold the Offer Shares for hedging purpose as the single underlying asset of several sets 

<<<PAGE 43>>>
43 
 
of back-to-back total return swap transaction (the GTHT Back-to-back TRS) to be entered into between GTJA Investments and Guotai Haitong 
Securities Co., Ltd. (the GTHT On-shore Parent) in connection with several total return swap orders (the GTHT Client TRS) to be entered into by 
GTHT Onshore Parent and several ultimate clients (the GTHT Onshore Ultimate Clients), respectively. Such GTHT Client TRS is to be fully funded 
by the GTHT Onshore Ultimate Clients. GTJA Investments will hold the Offer Shares on a non-discretionary basis for the purpose of hedging the 
economic exposure under the GTHT Back-to-back TRS and GTHT Client TRS only, During the tenor of the GTHT Client TRS, all economic returns 
of the Offer Shares will be passed to the GTHT Onshore Ultimate Clients and all economic losses shall be borne by the GTHT Onshore Ultimate Client, 
subject to the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS, and GTJA Investments will not take part in any economic 
return or bear any economic loss in relation to the price of the Offer Shares. The GTHT Onshore Ultimate Client may request to redeem the Offer 
Shares at their own discretion, upon which GTJA Investments shall dispose of the Offer Shares and settle the GTHT Back-to-back TRS and GTHT 
Client TRS in cash in accordance with the terms and conditions of the GTHT Back-to-back TRS and GTHT Client TRS documents.  
Due to its internal policy, GTJA Investments will not exercise the voting right attaching to the Offer Shares during the tenor of the GTHT Back-to-back 
TRS and GTHT Client TRS.  
The GTHT Onshore Ultimate Clients for purpose of this placee subscription are set out as below:  
No. 
Name of the GTHT Onshore Ultimate Client 
Ultimate beneficial owner(s) holding 30% or 
more interest (if any) 
1.  
上海孚騰私募基金管理有限公司 (Shanghai Futeng Private Equity Fund Management 
Co., Ltd.) 
Fei Fei (費飛) 
2.  
通怡安鑫2 號私募證券投資基金 (Tongyi Anxin No.2 Private Equity Securities Investment 
Fund) and 通怡裕鑫2 號私募證券投資基金 (Tongyi Yuxin No.2 Private Equity Securities 
Investment Fund) 
Huang Shilin (黃世霖) 
3.  
通怡桃李1 號私募證券投資基金 (Tongyi Taoli No.1 Private Equity Securities Investment 
Fund) and 通怡全球價值1 號私募證券投資基金 (Tongyi Quanqiu Jiazhi No.1 Private 
Equity Securities Investment Fund) 
Wang Jing (王靜) 
4.  
通怡低波組合1 號私募證券投資基金 (Tongyi Low Volatility Strategy Fund No. 1, a 
private securities investment fund) 
Sun Yuan (孫遠) 
5.  
廣州凱得資本運營有限公司 (Guangzhou Get Capital Operation Co., Ltd.) 
Yu Bo (餘波) 
6.  
廣州開發區美芯科技發展有限公司 (Guangzhou Development District Meixin 
Technology Development Co., Ltd.) 
He Xuegang (何學剛) 
7.  
錦繡中和（天津）投資管理有限公司-中和資本耕耘810 號私募證券投資基金 
(Splendid Zhonghe (tianjin) Investment management Co. Ltd - Zhonghe Capital Cultivation 
810 Private Securities Investment Fund) 
Wang Diansuo (王殿鎖) 

<<<PAGE 44>>>
44 
 
No. 
Name of the GTHT Onshore Ultimate Client 
Ultimate beneficial owner(s) holding 30% or 
more interest (if any) 
8.  
上海衛寧私募基金管理有限公司-衛甯啟航2 號私募證券投資基金 (Shanghai Weining 
Investment Mangement Co , Ltd-Weining Qihang No. 2 Private Securities Investment 
Fund) 
ZHANG YUN (張韞) 
 
GTJA Investments has confirmed that, to the best of their knowledge and after making all reasonable enquiries, each of the GTHT Onshore Ultimate 
Clients and its ultimate beneficial owner is an independent third party of GTJA Investments, GTJA HK and the companies which are members of the 
same group of companies as GTJA HK. 
 
3) 
CSI proposes to subscribe for and hold the Offer Shares as a placee under the International Offering on behalf of Global Multi Alpha Fund SP (the CSI 
Ultimate Client), which is an independent third party, on a non-discretionary basis, pursuant to which:  
(i) 
CSI will act as the single counterparty of a back-to-back total return swap transaction (the CSI Back-to-back TRS) to be entered into by it in 
connection with a total return swap order (the CSI Client TRS) placed and fully funded by the CSI Ultimate Client, by which CSI will pass the 
full economic exposure of the Offer Shares placed to CSI to the CSI Ultimate Client.  
(ii) 
As confirmed by CSI and CLSA, CSI will hold the legal title and beneficial interest in the Offer Shares, but will contractually agree to pass on 
the full economic exposure and return of the Offer Shares to the CSI Ultimate Client, on a non-discretionary basis. The CSI Ultimate Client 
may exercise their early termination rights to terminate the CSI Client TRS at any time from the trade date of the CSI Client TRS which should 
be on or after the date on which the Offer Shares are listed on the Stock Exchange. 
(iii) 
Upon the final maturity or termination of the CSI Client TRS by the CSI Ultimate Client, CSI will dispose of the Offer Shares on the secondary 
market and the CSI Ultimate Client will receive a final termination amount of the CSI Back-to-back TRS which will have taken into account 
all the economic returns or economic loss in relation to the Offer Shares and the fixed amount of transaction fees of the CSI Back- to-back TRS 
and the CSI Client TRS. Due to its internal policy, CSI will not exercise the voting right of the Offer Shares during the terms of the CSI Back-
to-back TRS. 
The ultimate beneficial owner(s) holding 30% or more interest of the CSI Ultimate Client is Zeng Shuzhen. 
CSI has confirmed that, to the best of their knowledge and after making all reasonable enquiries, the CSI Ultimate Client and its ultimate beneficial 
owner is an independent third party of CSI, CSB and the companies which are members of the same group of companies as CSB. 
4) 
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial public offerings (IPOs) in Hong Kong. However, 
PRC investors are permitted to invest in products issued by appropriate domestic securities firms licensed to undertake cross-border derivatives trading 
activities. In connection with such products, the licensed domestic securities firms, through their Hong Kong affiliates, may participate in Hong Kong 
IPOs either as placees or cornerstone investors (the Cross-border Derivatives Trading Regime). 

<<<PAGE 45>>>
45 
 
Huatai Securities Co., Ltd. (Huatai Securities), the shares of which are listed on both the Shanghai Stock Exchange (stock code: 601688) and the Stock 
Exchange (stock code: 6886), is one of the domestic securities firms licensed to undertake cross-border derivatives trading activities. Huatai Securities 
entered into an ISDA agreement (the ISDA Agreement) with its indirectly wholly-owned subsidiary, HTCI, to set out the principal terms of any future 
total return swap between Huatai Securities and HTCI.  
HTFH is a distributor in connection with the Global Offering. HTCI is a member of the same group of HTFH. Pursuant to the ISDA Agreement, HTCI, 
which intends to participate in the Global Offering as a placee, will hold the beneficial interest of the Offer Shares on a non-discretionary basis as the 
single underlying holder under a back-to-back total return swap (the Back-to-back TRS) to be entered by HTCI in connection with a Client TRS (as 
defined below) placed by and fully funded (i.e. with no financing provided by HTCI) by the Huatai Ultimate Clients (as defined below), by which, 
HTCI will, subject to customary fees and commissions, pass the full economic exposure of the Offer Shares ultimately to the Huatai Ultimate Clients, 
which in effect, HTCI will hold the beneficial interest of the Offer Shares on behalf of the Huatai Ultimate Clients. HTFH and HTCI are indirectly 
wholly owned subsidiaries of Huatai Securities. Accordingly, HTCI is considered as a “connected client” of HTFH pursuant to paragraph 1B of the 
Placing Guidelines.  
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (the Huatai Ultimate Clients) cannot directly subscribe for the Offer 
Shares but may invest in derivative products issued by domestic securities firms licenced to undertake cross-border derivatives trading activities, such 
as Huatai Securities, with the Offer Shares as the underlying assets. Instead of directly subscribing for the Offer Shares, the Huatai Ultimate Clients, 
through their respective investment manager, will place a total return swap order (the Client TRS) with Huatai Securities in connection with the 
Company’s IPO and Huatai Securities will place a Back-to-back TRS order to HTCI on the terms of the ISDA Agreement. In order to hedge its exposure 
under the Back-to-back TRS, HTCI participates in the Company’s initial public offering and subscribes the Offer Shares through placing order with 
HTFH during the International Placing.  
To the best of our knowledge and after making all reasonable enquiries, each of the Huatai Ultimate Clients and their respective ultimate beneficial 
owner holding 30% or more interest is an independent third party of (i) the Company, the connected person or the associates thereof, and (ii) HTCI, 
HTFH and the companies which are members of the same group of HTCI. 
The purpose of HTCI to subscribe for the Offer Shares is for hedging the Back-to-back TRS in connection with the Client TRS order placed by the 
Huatai Ultimate Clients. Pursuant to the terms of the contracts of the Back-to-back TRS and the Client TRS, during the tenor of the Back-to-back TRS 
and the Client TRS, subject to customary fees and commissions, all economic returns of the Offer Shares will be ultimately passed to the Huatai Ultimate 
Clients through the Back-to-back TRS and the Client TRS and all economic loss shall be ultimately borne by the Huatai Ultimate Clients. HTCI will 
not take any economic return or bear any economic loss in relation to the Offer Shares.  
Investment in the Back-to-back TRS and the Client TRS is similar to the investment in a qualified domestic institutional investor fund (“QDII”) in the 
way that the Huatai Ultimate Clients would reap all the economic benefits of the underlying Offer Shares, except that a QDII fund would pass through 
the exchange rate exposure on both the notional value of the investment and the profit and loss of the investment. In contrast, the profit and loss of the 
Back-to-back TRS and the Client TRS factor into account the fluctuation in RMB exchange rate upon termination of the Client TRS by converting the 
profit and loss using the current exchange rate at the time of termination. As such, the Huatai Ultimate Clients would bear the exchange rate exposure 
of the profit and loss on settlement date.  

<<<PAGE 46>>>
46 
 
The Huatai Ultimate Clients may exercise an early termination right to terminate the Client TRS at any time from the issue date of the Client TRS 
which should be on or after the date on which the Offer Shares are listed on the Stock Exchange at their own discretion. Upon the termination upon 
maturity or early termination of the Client TRS by the Huatai Ultimate Clients, HTCI will dispose the Offer Shares on the secondary market and the 
Huatai Ultimate Clients will receive a final settlement amount in cash in accordance with the terms and conditions of the Back-to-back TRS and the 
Client TRS which should have taken into account all the economic returns or economic loss in relation to the Offer Shares. If upon the maturity of the 
Client TRS, the Huatai Ultimate Clients intend to extend the investment period, subject to further agreement between Huatai Securities and the relevant 
Huatai Ultimate Clients, the term of the Client TRS could be extended by way of a new issuance or a tenor extension. Accordingly, Huatai Securities 
will extend the term of the Back-to-back TRS by way of a new issuance or a tenor extension. 
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and pass through the economic exposure to the Huatai 
Ultimate Clients, each being an onshore client who places a Client TRS order with Huatai Securities in connection with the IPO of the Company. HTCI 
will not exercise the voting right of the Offer Shares during the tenor of the Back-to-back TRS.  
During the life of the Client TRS and Back-to-back TRS, HTCI may continue to hold the Offer Shares in its custodian account, or to hold some or all 
of the Offer Shares in a prime brokerage account for stock borrowing purposes, where HTCI will lend out its holding of underlying Offer Shares in the 
form of stock borrowing loans consistent with market practice to lower its finance costs, provided that HTCI has the ability to call back the Offer Shares 
on loan at any time in order to satisfy its obligations under the Back-to-back TRS to ensure the economic interests are ultimately passed to the Huatai 
Ultimate Clients. 
Details of the Huatai Ultimate Clients are set out as below:  
Name of the Huatai Ultimate Clients 
Ultimate beneficial owner(s) holding 30% or more interest 
(if any) 
源峰穩健私募證券投資基金 (Yuanfeng Wenjian Private Equity Fund) 
N/A 
艾方金科3 號私募證券投資基金 (Aifang Jinke No.3 Private Equity Fund) 
Leng Ling (冷玲) 
道合承光私募證券投資基金 (Daohe Chengguang Private Equity Fund) 
ZHONG SHANSHAN 
 
5) 
Each of CMBI and CMS HK is distributor of the Global Offering. Bosera AM intends to subscribe and hold the Offer Shares in its capacity as the 
discretionary fund manager on behalf of its sub-funds, which are all independent third parties. To the best knowledge of Bosera AM after due enquiry, 
each of the sub-funds and their respective ultimate beneficial owner holding 30% or more interest is an independent third party of Bosera AM and each 
of CMBI and CMS HK, and the companies which are members of the same group of companies as each of CMBI and CMS HK.  
6) 
CSB is a distributor of the Global Offering. China AMC HK will hold the Offer Shares in its capacity as the discretionary fund manager managing 
assets on behalf of its underlying clients or mandates, which are independent third parties. To the best knowledge of China AMC HK after due enquiry, 
each of the underlying clients or mandates of China AMC HK and their respective ultimate beneficial owner holding 30% or more interest is an 
independent third party of China AMC HK and CSB, and the companies which are members of the same group of companies as CSB.  

<<<PAGE 47>>>
47 
 
7) 
CSB is a distributor of the Global Offering. China AMC will hold the Offer Shares in its capacity on behalf of its underlying client, which is an 
independent third party. There is no ultimate beneficial owner holding 30% interest or more in such underlying client. To the best knowledge of China 
AMC after due enquiry, the underlying client of China AMC is an independent third party of China AMC and CSB, and the companies which are 
members of the same group of companies as CSB.  
8) 
CSB is a distributor of the Global Offering. CITICS AM will hold the Offer Shares in its capacity as the discretionary fund manager on behalf of its 
underlying client, which is an independent third party. There is no ultimate beneficial owner holding 30% interest or more in such underlying client. 
To the best knowledge of CITICS AM after due enquiry, the underlying client of CITICS AM is an independent third party of CITICS AM and CSB, 
and the companies which are members of the same group of companies as CSB.  
9) 
UBS AG is an underwriter of the Global Offering. ICBC UBS (International) will hold the Offer Shares in its capacity as the discretionary fund manager 
on behalf of its underlying client, who, and its ultimate beneficial owner holding 30% interest or more, is an independent third party of the Company, 
its subsidiaries, its substantial shareholders, ICBC UBS (International), UBS AG and the companies which are members of the same group of UBS AG. 
 

<<<PAGE 48>>>
48 
 
DISCLAIMERS 
 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and Hong 
Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any 
part of the contents of this announcement. 
This announcement is not for release, publication, distribution, directly or indirectly, in or into the  
United States (including its territories and possessions, any state of the United States and the District 
of Columbia). This announcement does not constitute or form a part of any offer or solicitation to 
purchase or subscribe for securities in the United States. The Offer Shares have not been and will not 
be registered under the United States Securities Act of 1933, as amended (the “U.S. Securities Act”)or 
any state securities laws in the United States and may not be offered, sold, pledged or transferred 
within the United States or to, or for the account or benefit of U.S. persons (as defined in Regulation 
S under the U.S. Securities Act), except in transactions exempt from, or not subject to, the registration 
requirements of the U.S. Securities Act. The Offer Shares are being offered and sold (1) solely to 
qualified institutional buyers as defined in Rule 144A in reliance on Rule 144A or another exemption 
from, or in a transaction not subject to, registration under the U.S. Securities Act and (2) outside the 
United States in offshore transactions in reliance on Regulation S under the U.S. Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or offer to 
acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated December 31, 2025 issued by MiniMax Group Inc. for 
detailed information about the Global Offering described below before deciding whether or not to 
invest in the Offer Shares thereby being offered. 
*Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall be entitled to 
terminate their obligations under the Hong Kong Underwriting Agreement with immediate effect upon 
the occurrence of any of the events set out in the section headed “Underwriting – Underwriting 
Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on  the Listing Date (which is currently 
expected to be on January 9, 2026). 
 
 

<<<PAGE 49>>>
49
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering (after taking into account the full 
exercise of the Offer Size Adjustment Option and before any exercise of the Over-allotment 
Option), the total number of the Class A Ordinary Shares held by the public represents 
approximately 80.4% of the total number of issued Class A Ordinary Shares of the Company, 
which is higher than the prescribed percentage of Class A Ordinary Shares required to be held in 
public hands of 12.2% under Rule 8.08(1) of the Listing Rules calculated based on the final Offer 
Price of HK$165.00 per Share, thereby satisfying the public float requirement under Rule 8.08(1) 
of the Listing Rules.
Each of the Cornerstone Investors has agreed to a lock-up period of six months following the 
Listing Date. As such, Class A Ordinary Shares held by the Cornerstone Investors upon the Listing 
shall not be counted towards the free float of the Class A Ordinary Shares of the Company at the 
time of Listing. Based on the final Offer Price of HK$165.00 per Share, the Company satisfies the 
free float requirement under Rule 8.08A of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering (after 
taking into account the full exercise of the Offer Size Adjustment Option and before any exercise 
of the Over-allotment Option), (i) no placee will, individually, be placed more than 10% of the 
enlarged issued share capital of the Company immediately after the Global Offering; (ii) there 
will not be any new substantial Shareholder immediately after the Global Offering; (iii) the three 
largest public shareholders of the Company do not hold more than 50% of the shares in public 
hands at the time of the Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; 
and (iv) there will be at least 300 Shareholders at the time of the Listing in compliance with Rule 
8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The Share certificates will only become valid evidence of title at 8:00 a.m. on Friday, January 
9, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting – Underwriting Arrangements 
and Expenses – Hong Kong Public Offering – Grounds for Termination” in the Prospectus has 
not been exercised. Investors who trade the Class A Ordinary Shares on the basis of publicly 
available allocation details prior to the receipt of Share certificates or prior to the Share certificates 
becoming valid evidence of title do so entirely at their own risk.

<<<PAGE 50>>>
50
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Friday, 
January 9, 2026 (Hong Kong time), it is expected that dealings in the Class A Ordinary Shares on 
the Stock Exchange will commence at 9:00 a.m. on Friday, January 9, 2026 (Hong Kong time). 
The Class A Ordinary Shares will be traded in board lots of 20 Class A Ordinary Shares each, and 
the stock code of the Shares will be 0100.
By order of the Board
MiniMax Group Inc.
Dr. Yan Junjie
Chairman of the Board and Executive Director
Hong Kong, January 8, 2026
As of the date of this announcement, the Board comprises: (i) Dr. Yan Junjie, Ms. Yun Yeyi, Mr. 
Zhao Pengyu and Mr. Zhou Yucong as executive Directors; (ii) Mr. Chen Yingjie and Mr. Liu 
Wei as non-executive Directors; and (iii) Mr. Huang Guobin, Dr. Wang Pengcheng and Dr. Zhu 
Huaxing as proposed independent non-executive Directors.
