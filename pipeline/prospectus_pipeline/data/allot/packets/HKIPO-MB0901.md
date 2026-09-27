# 配发结果公告抽取任务：0901.HK Shenzhen SDMC Technology Co., Ltd. - H Shares

- 公告：ANNOUNCEMENT OF ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**27/05/2026 06:07**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0527/2026052700001.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"0901.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
those defined in the prospectus dated May 18, 2026 (the “Prospectus”) issued by Shenzhen SDMC Technology 
Co., Ltd. (深圳市華曦達科技股份有限公司) (the “Company”).
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
In connection with the Global Offering, China Securities (International) Corporate Finance Company Limited 
acts as the Sole Sponsor, Sole Sponsor-Overall Coordinator, Sole Overall Coordinator and Sole Global 
Coordinator.
Potential investors of the Offer Shares should note that the Sole Sponsor and the Sole Sponsor-Overall 
Coordinator (for itself and on behalf of the Hong Kong Underwriters) shall be entitled to terminate their 
obligations under the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of 
the events set out in the section headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong 
Public Offering – Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) 
on the Listing Date (which is currently expected to be on Wednesday, May 27, 2026).

<<<PAGE 2>>>
– 2 –
Shenzhen SDMC Technology Co., Ltd.
深圳市華曦達科技股份有限公司
(a joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the
Global Offering
:
19,207,300 H Shares
Number of Hong Kong Offer Shares
:
1,920,800 H Shares
Number of International Offer Shares
:
17,286,500 H Shares
Offer Price
:
HK$32.80 per H Share, plus brokerage 
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
00901
Sole Sponsor, Sole Overall Coordinator, Sole Global Coordinator,
Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3 
 
SHENZHEN SDMC TECHNOLOGY CO., LTD. / 深圳市華曦達科技股份有限公司 
ANNOUNCEMENT OF ALLOTMENT RESULTS 
Unless otherwise defined herein, capitalised terms used in this announcement shall have the same meanings 
as those defined in the prospectus dated May 18, 2026 (the “Prospectus”) issued by Shenzhen SDMC 
Technology Co., Ltd. (the “Company”).  
SUMMARY  
 
Company information 
Stock code  
901 
Stock short name  
SDMC 
Dealings commencement date  
May 27, 2026* 
*see note at the end of the announcement  
Price Information  
Offer Price  
HK$32.80 
Offer Shares and Share Capital 
Number of Offer Shares  
19,207,300 H Shares 
Final Number of Offer Shares in Hong Kong Public Offering 1,920,800 H Shares 
Final Number of Offer Shares in International Offering 
(Note) 
17,286,500 H Shares 
Number of issued shares upon Listing  
209,540,070 H Shares 
Note: The Offer Size Adjustment Option is not exercised. 
 
Proceeds 
Gross proceeds (Note)  
HK$ 630.00 million 
Less: Estimated listing expenses payable based on Final 
Offer Price  
HK$ (60.00) million 
Net proceeds  
HK$ 570.00 million 
Note: Gross proceeds refers to the amount to which the issuer is entitled receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” in the Prospectus. 
 
 
ALLOTMENT RESULTS DETAILS 
HONG KONG PUBLIC OFFERING 
 
No. of valid applications  
177,196 
No. of successful applications  
17,058 
Subscription level  
1,971.99 times 
Claw-back triggered  
N/A  
No. of Offer Shares initially available under the Hong Kong Public 
Offering  
1,920,800 
No. of Offer Shares reallocated from the International Offering 
0 
Final no. of Offer Shares under the Hong Kong Public Offering  
1,920,800 
% of Offer Shares under the Hong Kong Public Offering to the 
Global Offering 
10.00% 
 

<<<PAGE 4>>>
4 
 
Note: For details of the final allocation of shares to the Hong Kong Public Offering, investors can refer to 
https://www.hkeipo.hk/IPOResult to perform a search by name or identification number or 
https://www.hkeipo.hk/IPOResult for the full list of allottees. 
INTERNATIONAL OFFERING 
 
No. of placees  
215 
Subscription Level  
2.23 times  
No. of Offer Shares initially available under the International 
Offering  
17,286,500 
Final no. of Offer Shares under the International Offering 
17,286,500 
% of Offer Shares under the International Offering to the Global 
Offering 
90.00% 
 
The Directors confirm that, to the best of their knowledge, information and belief, save for consents under 
paragraph 1C(1) and (2) of Appendix F1 to the Listing Rules (the “Placing Guidelines”) granted by the Stock 
Exchange to permit H Shares in the International Offering to be placed to certain existing shareholders and/or 
their close associates and certain connected clients as disclosed in this announcement, (i) none of the Offer 
Shares subscribed by the placees and the public have been financed directly or indirectly by the Company, any 
of the Directors, chief executive of the Company, controlling shareholders, substantial shareholders, existing 
shareholders of the Company or any of its subsidiaries or their respective close associates; and (ii) none of 
the placees and the public who have purchased the Offer Shares are accustomed to taking instructions from 
the Company, any of the Directors, chief executive of the Company, controlling shareholders, substantial 
shareholders, existing shareholders of the Company or any of its subsidiaries or their respective close 
associates in relation to the acquisition, disposal, voting or other disposition of Shares registered in his/her/its 
name or otherwise held by him/her/it.  
ALLOTEES WITH CONSENTS OBTAINED  
 
Name 
No. of  
Offer  
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
issued  
Shares after  
the Global  
Offering 
Relationship 
Allotee with consent under paragraphs 1C(1) of the Placing Guidelines in relation to allocations to 
connected clients (Note 1)  
Guotai Junan Financial 
Products Limited (the 
“Guotai Junan 
Financial Products”) 
 
579,100 
 
3.01% 
 0.28% 
 0.28% 
Connected client as a 
placee 
Allotees with consent under paragraph 1C(2) of the Placing Guidelines in relation to allocation to close 
associates of existing Shareholders (Note 2) 
Luxshare Precision 
Limited (立訊精密
有限公司) 
(“Luxshare 
Precision”)  
(Note 3) 
 1,731,800 
 
9.02% 
0.83% 
 0.83% 
A close associate of an 
existing Shareholder 

<<<PAGE 5>>>
5 
 
Name 
No. of  
Offer  
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
issued  
Shares after  
the Global  
Offering 
Relationship 
Shenzhen Longsys 
Electronics Co., 
Ltd. (深圳市江波
龍電子股份有限公
司) (“Longsys”) 
(Note 4) 
1,038,500 
 
5.41% 
0.50% 
 0.50% 
A close associate of an 
existing Shareholder 
Shenzhen Qianhai 
Huirui Investment 
Management Co., 
Ltd. (深圳市前海匯
睿投資管理有限公
司) (“Shenzhen 
Qianhai”) (Note 5) 
548,700 
2.86% 
0.26% 
0.26% 
A close associate of an 
existing 
Shareholder 
(as a GTHT Ultimate 
Client) (Note 1) 
 
Notes: 
 
1. For details of the consents under paragraphs 1C(1) and 1C(2) of the Placing Guidelines in relation 
to allocations to connected clients and close associates of existing Shareholder, please refer to the 
section headed “Others/Additional Information — Placing to Connected Clients (including those 
who are close associate of existing Shareholder) with Prior Consents under Paragraph 1C(1) of the 
Placing Guidelines” in this announcement. 
 
2. The Stock Exchange has given a consent under paragraph 1C(2) of the Placing Guidelines to permit 
Offer Shares to be placed to the above placees who are close associate of certain existing 
Shareholders. Please refer to the section headed “Others/Additional Information – Placing to close 
associates of existing Shareholders as placees with a prior consent under paragraph 1C(2) of the 
Placing Guidelines” in this announcement. 
 
3. Luxshare Precision is a direct wholly-owned subsidiary of Luxshare Precision Industry Co., Ltd. (立
訊精密工業股份有限公司) (“Luxshare”). Luxshare is a company established in the PRC on May 
24, 2004, the A Shares of which have been listed on the Shenzhen Stock Exchange (stock code: 
002475). The controlling shareholder of Luxshare is Luxshare Limited (立訊有限公司), who held 
as to approximately 37.49% of Luxshare, an existing Shareholder. 
 
4. Longsys is a company established in the PRC on April 27, 1999, the A Shares of which have been 
listed on the ChiNext of Shenzhen Stock Exchange (stock code: 301308). The controlling 
shareholder of Longsys is CAI Huabo (蔡華波), the spouse of XU Zhiyan (徐志燕), an existing 
Shareholder. 
 
5. Shenzhen Qianhai is held as to 30% by Wang Daqi (王大琦), an existing Shareholder. 
 

<<<PAGE 6>>>
6 
 
LOCK-UP UNDERTAKINGS  
Controlling Shareholders 
 
 
 Name 
Number of 
shares held 
in the 
Company 
subject to 
lock-up 
undertakin
gs upon 
listing 
Number of  
H Shares  
held in the 
Company 
subject to 
lock-up 
undertakings 
upon listing 
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing  
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon listing  
Last day 
subject to  
the lock-up 
undertakings 
Note 1 
Li Bo / 李波 
50,286,768 
50,286,768 
24.02% 
24.00% 
May 26, 2027 
Shenzhen Zhixin 
Weilai Investment 
Partnership (Limited 
Partnership) / 深圳市
智信未來投資合夥企
業（有限合夥） 
14,752,800 
14,752,800 
7.05% 
7.04% 
May 26, 2027 
Shenzhen Kaida 
Yunzhi Investment 
Partnership (Limited 
Partnership) / 深圳市
凱達雲智投資合夥企
業（有限合夥） 
1,000,000 
1,000,000 
0.48% 
0.48% 
May 26, 2027 
Shenzhen Huazhi 
Changlian Internet 
Technology Partnership 
(Limited Partnership) / 
深圳市華智暢聯互聯
網技術合夥企業 
（有限合夥） 
1,000,000 
1,000,000 
0.48% 
0.48% 
May 26, 2027 
Shenzhen Qihang No. 1 
Investment Partnership 
(Limited Partnership) / 
深圳市啟航一號投資 
合夥企業 
（有限合夥）
(“Qihang No. 1”) Note 2 
1,500,000 
1,500,000 
0.72% 
0.72% 
May 26, 2027 

<<<PAGE 7>>>
7 
 
 
 
 
 
Shenzhen Qihang No. 2 
Investment Partnership 
(Limited Partnership) / 
深圳市啟航二號投資 
合夥企業 
（有限合夥）
(“Qihang No. 2”) Note 2 
1,150,000 
1,150,000 
0.55% 
0.55% 
May 26, 2027 
Subtotal 
69,689,568 
69,689,568 
33.30% 
32.37% 
 
 
Notes: 
1. The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company 
Law. 
2. Each of Qihang No. 1 and Qihang No. 2 is also a Pre-IPO Investor. 
 

<<<PAGE 8>>>
8 
 
Pre-IPO Investors (as defined in the “History and Corporate Structure” section of the Prospectus) 
 Name 
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon listing 
Number of  
H Shares  
held in the 
Company 
subject to 
lock-up 
undertakings 
upon listing 
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing  
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon listing  
Last day 
subject  
the lock-up 
undertakings 
Note 1 
Panorama Capital 
Investment 
Management Co., 
Ltd.– Panorama 
Capital Green 
Technology 
Manufacturing 
Private Equity 
Investment Fund 
Partnership 
 (Limited 
Partnership) /上海
國策投資管理有限
公司－上海國策綠
色科技製造私募投
資基金合夥企業
（有限合夥） 
2,150,000 
2,150,000 
1.03% 
1.03% 
May 26, 2027 
Qihang No. 1 Note 2 
1,500,000 
1,500,000 
0.72% 
0.72% 
May 26, 2027 
Qihang No. 2 Note 2 
1,150,000 
1,150,000 
0.55% 
0.55% 
May 26, 2027 
Liu Minhua /  
劉敏華 
300,000 
300,000 
0.14% 
0.14% 
May 26, 2027 
Li Jingcheng /  
李景程 
270,000 
270,000 
0.13% 
0.13% 
May 26, 2027 
Wu Jun / 吳俊 
100,000 
100,000 
0.05% 
0.05% 
May 26, 2027 
Subtotal 
5,470,000 
5,470,000 
2.62% 
2.62% 
 
 
Notes:  
 
1. 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company 
Law. 
 
2. 
Each of Qihang No. 1 and Qihang No. 2 is also a Controlling Shareholder. 
 
 
 

<<<PAGE 9>>>
9 
 
Existing Shareholders (other than the Controlling Shareholders and the Pre-IPO Investors as defined in 
the “History and Corporate Structure” section of the Prospectus) 
 Name 
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon listing 
Number of  
H Shares  
held in the 
Company 
subject to 
lock-up 
undertakings 
upon listing 
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing  
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon listing  
Last day 
subject to the 
lock-up 
undertakings 
Note 1 
Shenzhen 
Jingboyuan 
Technology Co., 
Ltd. / 深圳市晶博
源科技有限公司 
2,697,740 
2,697,740 
1.29% 
1.29% 
May 26, 2027 
Wang Houyong / 
汪厚勇 
2,594,024 
2,594,024 
1.24% 
1.24% 
May 26, 2027 
Shenzhen 
Danguishun Asset 
Management Co., 
Ltd. - Danguishun 
No. 5 Private 
Securities 
Investment Fund / 
深圳市丹桂順資
產管理有限公司
－丹桂順之實事
求是伍號私募證
券投資基金 
2,400,000 
2,400,000 
1.15% 
1.15% 
May 26, 2027 
Zhang Guiqiang / 
張桂強 
2,178,000 
2,178,000 
1.04% 
1.04% 
May 26, 2027 
Wang Yi / 王逸 
2,000,000 
2,000,000 
0.96% 
0.95% 
May 26, 2027 
Sichuan Tianyi 
Comheart Telecom 
Co., Ltd. / 四川 
天邑康和通信 
股份有限公司 
2,000,000 
2,000,000 
0.96% 
0.95% 
May 26, 2027 
Zhang Lingjing / 
張靈晶 
1,800,000 
1,800,000 
0.86% 
0.86% 
May 26, 2027 
Li Han / 李晗 
1,098,640 
1,098,640 
0.52% 
0.52% 
May 26, 2027 
Jiang Yanjun /  
蔣豔君 
635,200 
635,200 
0.30% 
0.30% 
May 26, 2027 
Shenzhen 
Chuangzhan 
Internet 
Partnership 
18,004,000 
18,004,000 
8.60% 
8.59% 
May 26, 2027 

<<<PAGE 10>>>
10 
 
 Name 
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon listing 
Number of  
H Shares  
held in the 
Company 
subject to 
lock-up 
undertakings 
upon listing 
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing  
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon listing  
Last day 
subject to the 
lock-up 
undertakings 
Note 1 
(Limited 
Partnership) / 深
圳市創展互聯網 
合夥企業 
（有限合夥） 
Li Qingqing / 
李青青 
4,815,400 
4,815,400 
2.30% 
2.30% 
May 26, 2027 
Yang Jian / 楊健 
600,000 
600,000 
0.29% 
0.29% 
May 26, 2027 
Yan Zhikang /  
嚴志康 
4,544,800 
4,544,800 
2.17% 
2.17% 
May 26, 2027 
Yan Lupeng /  
晏侶鵬 
1,510,500 
1,510,500 
0.72% 
0.72% 
May 26, 2027 
Zhou Dongdong / 
周冬冬 
502,400 
502,400 
0.24% 
0.24% 
May 26, 2027 
Shenzhen 
Shuangyi 
Electronic Co., 
Ltd. / 深圳市雙翼
電子有限公司 
5,213,692 
5,213,692 
2.49% 
2.49% 
May 26, 2027 
Pang Zhengrong / 
龐崢嶸 
1,112,900 
1,112,900 
0.53% 
0.53% 
May 26, 2027 
Wei Jing / 魏晶 
6,675,000 
6,675,000 
3.19% 
3.19% 
May 26, 2027 
Shenzhen Tencent 
Venture Base 
Development Co., 
Ltd. / 深圳市騰訊
創業基地發展有
限公司 
6,000,000 
6,000,000 
2.87% 
2.86% 
May 26, 2027 
Luxshare Precision 
Industry Co. Ltd. / 
立訊精密工業股
份有限公司 
4,000,000 
4,000,000 
1.91% 
1.91% 
May 26, 2027 
Zhu Yupei /  
朱玉佩 
2,175,640 
2,175,640 
1.04% 
1.04% 
May 26, 2027 
AVIC Trust Co. 
Ltd. - AVIC Trust - 
CICC Wealth 
Family Trust No. 
960,000 
960,000 
0.46% 
0.46% 
May 26, 2027 

<<<PAGE 11>>>
11 
 
 Name 
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon listing 
Number of  
H Shares  
held in the 
Company 
subject to 
lock-up 
undertakings 
upon listing 
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing  
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon listing  
Last day 
subject to the 
lock-up 
undertakings 
Note 1 
[638] / 中航信託
股份有限公司－
中航信託·中金財
富【638】號家族
信託 
Shenzhen Kaiying 
No. 9 Venture 
Capital Partnership 
(Limited 
Partnership) / 深
圳凱盈九號創業
投資合夥企業
（有限合夥） 
3,000,000 
3,000,000 
1.43% 
1.43% 
May 26, 2027 
Shenzhen Kaiying 
Tiancheng 
Investment 
Management 
Partnership - 
Shenzhen Kaiying 
No. 10 Venture 
Capital Partnership 
/ 深圳凱盈天成投
資管理合夥企業
（有限合夥）－
深圳凱盈十號創
業投資合夥企業
（有限合夥） 
1,880,000 
1,880,000 
0.90% 
0.90% 
May 26, 2027 
Shenzhen Kaiying 
No. 8 Venture 
Capital Partnership 
(Limited 
Partnership) / 深
圳凱盈八號創業
投資合夥企業
（有限合夥） 
1,000,000 
1,000,000 
0.48% 
0.48% 
May 26, 2027 
Xie Liying /  
謝麗穎 
1,680,796 
1,680,796 
0.80% 
0.80% 
May 26, 2027 
Xie Lifeng /  
1,660,000 
1,660,000 
0.79% 
0.79% 
May 26, 2027 

<<<PAGE 12>>>
12 
 
 Name 
Number of 
shares held in 
the Company 
subject to 
lock-up 
undertakings 
upon listing 
Number of  
H Shares  
held in the 
Company 
subject to 
lock-up 
undertakings 
upon listing 
% of total 
issued H 
Shares after 
the Global 
Offering 
subject to 
lock-up 
undertakings 
upon listing  
% of 
shareholding 
in the 
Company 
subject to 
lock-up 
undertakings 
upon listing  
Last day 
subject to the 
lock-up 
undertakings 
Note 1 
謝立峰 
Century Securities 
Co., Ltd. / 世紀證
券有限責任公司 
3,000,000 
3,000,000 
1.43% 
1.43% 
May 26, 2027 
Other Shareholders 
as of the Latest 
Practicable Date / 
截至最後可行日
期的其他股東 
32,084,470 
31,937,962 
15.25% 
15.31% 
May 26, 2027 
Subtotal 
117,823,202 
117,676,694 
56.21% 
56.23% 
 
 
Note: 
 
1. 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company 
Law. 
 
 
 

<<<PAGE 13>>>
13 
 
PLACEE CONCENTRATION ANALYSIS  
Placees* 
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
1,731,800 
10.02% 
9.02% 
5,731,800 
2.74% 
Top 5 
6,767,100 
39.15% 
35.23% 
11,167,100 
5.33% 
Top 10 
10,205,900 
59.04% 
53.14% 
14,605,900 
6.97% 
Top 25 
16,507,900 
95.50% 
85.95% 
21,007,900 
10.03% 
 
Notes 
* Ranking of placees is based on the number of H Shares allotted to the placees. 
H SHAREHOLDERS CONCENTRATION ANALYSIS 
H 
Shareholders* 
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
69,689,568 
33.28% 
69,689,568 
 Top 5 
0 
0.00% 
0.00% 
112,110,560 
53.54% 
112,110,560 
 Top 10 
1,731,800 
10.02% 
9.02% 
134,743,596 
64.35% 
134,743,596 
 Top 25 
6,767,100 
39.15% 
35.23% 
164,049,160 
78.34% 
164,049,160 
 
Notes 
* Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.  
SHAREHOLDER CONCENTRATION ANALYSIS 
Shareholders* 
Number of H 
Shares allotted 
Allotment as % of 
International Offering 
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
69,689,568 
69,689,568 
33.26% 
Top 5 
0 
0.00% 
0.00% 
112,110,560 
112,110,560 
53.50% 
Top 10 
1,731,800 
10.02% 
9.02% 
134,743,596 
134,743,596 
64.30% 
Top 25 
6,767,100 
39.15% 
35.23% 
164,049,160 
164,049,160 
78.29% 
 
 
 

<<<PAGE 14>>>
14 
 
Notes 
* Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.  
 
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING  
Subject to the satisfaction of the conditions set out in the Prospectus, valid applications made by 
the public will be conditionally allocated on the basis set out below: 
 
NO. OF H SHARES 
APPLIED FOR 
NO. OF VALID 
APPLICATIONS 
BASIS OF ALLOTMENT/BALLOT 
APPROXIMATE 
PERCENTAGE ALLOTTED 
OF THE TOTAL NO. OF H 
SHARES APPLIED FOR  
100 
57,352 
0 H Shares 
2.00% 
100 
1,171 
100 H Shares 
200 
9,684 
0 H Shares 
1.30% 
200 
259 
100 H Shares 
300 
28,406 
0 H Shares 
1.01% 
300 
889 
100 H Shares 
400 
3,594 
0 H Shares 
0.85% 
400 
126 
100 H Shares 
500 
3,627 
0 H Shares 
0.74% 
500 
139 
100 H Shares 
600 
1,860 
0 H Shares 
0.66% 
600 
77 
100 H Shares 
700 
1,208 
0 H Shares 
0.60% 
700 
53 
100 H Shares 
800 
1,153 
0 H Shares 
0.56% 
800 
54 
100 H Shares 
900 
891 
0 H Shares 
0.51% 
900 
43 
100 H Shares 
1,000 
7,081 
0 H Shares 
0.48% 
1,000 
356 
100 H Shares 
1,500 
12,768 
0 H Shares 
0.37% 
1,500 
755 
100 H Shares 
2,000 
2,544 
0 H Shares 
0.31% 
2,000 
169 
100 H Shares 
2,500 
1,308 
0 H Shares 
0.27% 
2,500 
95 
100 H Shares 
3,000 
2,721 
0 H Shares 
0.24% 
3,000 
213 
100 H Shares 
3,500 
1,183 
0 H Shares 
0.22% 
3,500 
99 
100 H Shares 
4,000 
894 
0 H Shares 
0.20% 
4,000 
79 
100 H Shares 
4,500 
675 
0 H Shares 
0.19% 
4,500 
63 
100 H Shares 
5,000 
1,803 
0 H Shares 
0.18% 

<<<PAGE 15>>>
15 
 
NO. OF H SHARES 
APPLIED FOR 
NO. OF VALID 
APPLICATIONS 
BASIS OF ALLOTMENT/BALLOT 
APPROXIMATE 
PERCENTAGE ALLOTTED 
OF THE TOTAL NO. OF H 
SHARES APPLIED FOR  
5,000 
174 
100 H Shares 
6,000 
1,203 
0 H Shares 
0.16% 
6,000 
126 
100 H Shares 
7,000 
846 
0 H Shares 
0.14% 
7,000 
94 
100 H Shares 
8,000 
668 
0 H Shares 
0.13% 
8,000 
79 
100 H Shares 
9,000 
588 
0 H Shares 
0.12% 
9,000 
73 
100 H Shares 
10,000 
4,246 
0 H Shares 
0.11% 
10,000 
549 
100 H Shares 
20,000 
2,692 
0 H Shares 
0.07% 
20,000 
471 
100 H Shares 
30,000 
2,052 
0 H Shares 
0.06% 
30,000 
431 
100 H Shares 
40,000 
1,382 
0 H Shares 
0.05% 
40,000 
332 
100 H Shares 
50,000 
1,243 
0 H Shares 
0.04% 
50,000 
332 
100 H Shares 
60,000 
850 
0 H Shares 
0.04% 
60,000 
248 
100 H Shares 
70,000 
569 
0 H Shares 
0.03% 
70,000 
179 
100 H Shares 
80,000 
472 
0 H Shares 
0.03% 
80,000 
159 
100 H Shares 
90,000 
449 
0 H Shares 
0.03% 
90,000 
161 
100 H Shares 
100,000 
4,126 
0 H Shares 
0.03% 
100,000 
1,556 
100 H Shares 
200,000 
4,551 
100 H Shares 
0.05% 
300,000 
663 
100 H Shares 
0.04% 
300,000 
227 
200 H Shares 
400,000 
244 
100 H Shares 
0.04% 
400,000 
220 
200 H Shares 
500,000 
107 
100 H Shares 
0.03% 
500,000 
219 
200 H Shares 
600,000 
40 
100 H Shares 
0.03% 
600,000 
226 
200 H Shares 
700,000 
156 
200 H Shares 
0.03% 
800,000 
94 
200 H Shares 
0.03% 
800,000 
20 
300 H Shares 
960,400 
406 
200 H Shares 
0.03% 
960,400 
281 
300 H Shares 
Total 
177,196 
1,920,800 H Shares 
 

<<<PAGE 16>>>
16 
 
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries. 
  
COMPLIANCE WITH LISTING RULES AND GUIDANCE 
The Directors confirm that, except for the Listing Rules in respect of which consent has been obtained, 
the Company has complied with the Listing Rules and guidance materials in relation to the placing, 
allotment and listing of the Company’s H Shares.  
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees or the 
public (as the case may be) directly or indirectly for each Offer Share subscribed for or purchased by 
them was the same as the final Offer Price in additional to any brokerage, AFRC transaction levy, SFC 
transaction levy and trading fee payable. 
OTHERS / ADDITIONAL INFORMATION 
Placing to Connected Client (including those who are close associate of existing Shareholder) 
with Prior Consents under Paragraph 1C(1) of the Placing Guidelines  
The Company has applied to the Stock Exchange and the Stock Exchange has given a consent under 
Paragraph 1C(1) of the Placing Guidelines to permit the company to allocate certain Offer Shares 
under the International Offering to a connected client (the “Connected Client”) of a distributor, 
Guotai Junan Securities (Hong Kong) Limited (the “Guotai Junan Securities” or the “Connected 
Distributor”) on the following basis: 
(a) the Sole Overall Coordinator has confirmed that: 
(i) the shares to be allocated to the Connected Client (i) will be held by the Connected 
Client on a non-discretionary basis for Guotai Junan Investments, (ii) will be held by 
Guotai Junan Investments on a non-discretionary basis for GTHTS, and (iii) will 
ultimately be held by GTHTS on a non-discretionary basis for GTHT Ultimate Clients, 
and each of the GTHT Ultimate Clients is an independent third party of the Company;  
(ii) the full economic exposure will be passed to each of the GTHT Ultimate Clients;  
(iii) to the best knowledge and belief of the Sole Overall Coordinator, the Sole Overall 
Coordinator has no reason to believe that the Connected Client has received any 
preferential treatment in the allocation of securities in the IPO as a placee by virtue of 
its relationship with the Connected Distributor;  
(iv) no preferential treatment has been, nor will be, given to the relevant existing 
Shareholder or his close associates by virtue of their relationship with the Company in 
any allocation in the placing tranche;  
(v) details of the allocation will be disclosed in this announcement; and  
(vi) the Connected Client neither is a collective investment scheme which is not authorised 
by the SFC nor is holding the securities on behalf of such scheme;  
 
 
 

<<<PAGE 17>>>
17 
 
(b) the Company has confirmed that  
(i) no preferential treatment has been, nor will be given to the Connected Client by virtue 
of their relationship with the Connected Distributor and  
(ii) no preferential treatment has been, nor will be given to the relevant existing 
Shareholder or his close associates by virtue of their relationship with the Company in 
any allocation of the Offer Shares in the International Offering;  
 
(c) the Sole Sponsor has confirmed that:  
(i) the relevant existing Shareholder or his close associates has less than 5% voting rights 
in the Company before the offering;  
(ii) the relevant existing Shareholder or his close associates is not a core connected person 
or a close associate of the Company;  
(iii) the relevant existing Shareholder or his close associates does not have the power to 
appoint directors or any other special rights;  
(iv) allocation to the relevant existing Shareholder or his close associates will not affect 
the Company’s ability to satisfy the public float requirement;  
(v) to the best of the Sole Sponsor’s knowledge and belief, the Sole Sponsor has no reason 
to believe that the relevant existing Shareholder or his close associates received any 
preferential treatment in any allocation of the Offer Shares in the International 
Offering as a placee by virtue of their relationship with the Company, and  
(vi) details of the allocation will be disclosed in this announcement; 
 
(d) the Connected Distributor has confirmed that no preferential treatment has been, nor will be 
given to the Connected Client by virtue of their relationship with the Connected Distributor 
in any allocation of the Offer Shares in the International Offering;  
 
(e) the Connected Client has confirmed that:  
(i) to the best of its knowledge and belief, it has not received and will not receive 
preferential treatment in the International Offering allocation as a placee by virtue of 
their relationship with the Connected Distributor;  
(ii) it neither is a collective investment scheme which is not authorised by the SFC nor is 
holding the securities on behalf of such scheme. 
 
Such allocations of Offer Shares are in compliance with all the conditions under the consent granted 
by the Stock Exchange.  
 
 
 

<<<PAGE 18>>>
18 
 
Details of the placement to the Connected Client are set out below: 
Connected 
Distributor 
Connected 
Client 
Relationship 
The GTHT 
Ultimate 
Clients (as 
defined in 
Note 1) 
Whether the 
Connected 
Client will 
hold the 
beneficial 
interests of 
the Offer 
Shares on a 
non 
discretionary 
basis or 
discretionary 
basis for 
independent 
third parties 
Number 
of Offer 
Shares 
allocated 
to the 
connected 
client 
Approximate 
percentage 
of Offer 
Shares 
allocated to 
the 
connected 
client 
Approximate 
percentage 
of total 
issued 
Shares after 
the Global 
Offering 
Guotai 
Junan 
Securities  
Guotai 
Junan 
Financial 
Products  
Guotai Junan 
Financial 
Products is a 
member of the 
same group of 
the Guotai 
Junan 
Securities Νοτε 1 
Shenzhen 
Qianhai and 
Qingdao 
Roadshow 
Investment 
Management 
Co., Ltd. - 
Reindeer 
No.17 
(青島鹿秀投
資管理有限公
司鹿秀馴鹿17
號私募證券投
資基金) 
(“Reindeer 
No.17”) Note 2 
Non-
discretionary 
basis 
579,100 
 
3.01% 
0.28% 
 
(1) Guotai Junan Financial Products shall hold the Offer Shares on a non-discretionary basis for hedging 
purposes as the single underlying asset of a delta one back-to-back total return swap transaction (the “GTJA 
Back-to-back TRS1”) to be entered into between Guotai Junan Financial Products and Guotai Junan 
Investments, and Guotai Junan Investments shall for hedging purposes enter into a cross-border delta one 
back-to-back total return swap transaction (the “GTJA Back-to-back TRS2”) with GTHTS, in connection 
with a total return swap order (the “GTHT Client TRS”) to be entered into by GTHTS and the GTHT 
ultimate clients (the “GTHT Ultimate Clients”). Such GTHT Client TRS is to be fully funded by the GTHT 
Ultimate Clients. The full economic exposure of the Offer Shares will be passed from Guotai Junan 
Financial Products to Guotai Junan Investments under the GTJA Back-to-back TRS1, from Guotai Junan 
Investments to GTHT under the GTJA Back-to-back TRS2, and ultimately from GTHTS to the GTHT 
Ultimate Clients under the GTHT Client TRS.  
 
The GTHT Ultimate Clients may exercise an early termination right to early terminate the GTHT Client 
TRS at any time from the trade date of the GTHT Client TRS, which should be on or after the date on 
which the Offer Shares are listed on the Stock Exchange. Accordingly, (i) GTHTS may exercise an early 
termination right to early terminate the GTJA Back-to-back TRS2 at any time from the trade date of the 
GTJA Back-to-back TRS2, and (ii) Guotai Junan Investments may exercise an early termination right to 
early terminate the GTJA Back-to-back TRS1 at any time from the trade date of the GTJA Back-to-back 
TRS1, which, in each case, should be on or after the date on which the Offer Shares are listed on the 
Stock Exchange. Upon the final maturity or early termination of (i) the GTHT Client TRS by the GTHT 
Ultimate Clients, (ii) the GTJA Back-to-back TRS2 by GTHTS, and (iii) the GTJA Back-to-back TRS1 
by Guotai Junan Investments, Guotai Junan Financial Products will dispose the Offer Shares on the 

<<<PAGE 19>>>
19 
 
secondary market and the GTHT Ultimate Clients ultimately will receive a final termination amount of 
the GTHT Client TRS, which should have taken into account all the economic returns or economic loss 
in relation to the Offer Shares, the fixed amount in relation to the GTJA Back-to-back TRS1, the GTJA 
Back-to-back TRS2 and the GTHT Client TRS.  
 
Guotai Junan Financial Products will hold the legal title and the voting right of the Offer Shares by itself 
and pass through the economic exposure to Guotai Junan Investments, GTHTS and ultimately the GTHT 
Ultimate Clients. Due to its internal policy, Guotai Junan Financial Products will not exercise the voting 
right of the Offer Shares during the tenor of the GTJA Back-to-back TRS1 and the GTJA Back-to-back 
TRS2.  
 
The details of the GTHT Ultimate Clients are as follows: 
 
Name 
of 
GTHT 
Ultimate Clients 
Ultimate Beneficial Owner holding 30% or more interest 
in the GTHT Ultimate Clients 
Shenzhen Qianhai 
Shenzhen Qianhai is held as to 70% and 30% by Li Wei-hua (李
偉華) and Wang Daqi (王大琦), respectively. Wang Daqi is an 
existing Shareholder. 
Reindeer No.17 
Reindeer No.17 is a limited partnership established in the PRC, 
the general partner of which is He Xiaomin (何小敏), who 
owned 54.73% interests of Reindeer No.17. Save for He 
Xiaomin (何小敏), no other limited partners owned more than 
30% of Reindeer No. 17. 
 
Placing to close associates of existing Shareholders as placees with a prior consent under 
paragraph 1C(2) of the Placing Guidelines 
The Company has applied to the Stock Exchange and the Stock Exchange has given a consent under 
Paragraph 1C(2) of the Placing Guidelines to permit the Company to allocate certain Offer Shares 
under the International Offering to the close associates of certain existing Shareholders, subject to 
the fulfilment of the Existing Shareholders Conditions (as defined in paragraph 14 of Chapter 4.15 
of the Guide for New Listing Applicant). Such allocations of Offer Shares are in compliance with all 
the conditions under the consent given by the Stock Exchange.  
 
 

<<<PAGE 20>>>
20 
 
Details of the placement to the close associates of certain existing Shareholders are set out below: 
Name of the 
close 
associates 
Relationship 
with the 
existing 
Shareholders 
Ultimate 
Beneficial 
Owner 
holding 30% 
or more 
interest in 
the close 
associates 
Number of 
Offer 
Shares 
allocated 
to the 
close 
associates 
Approximate 
percentage of 
Offer Shares 
allocated to the 
close associates 
Number of 
Shares held 
by the 
existing 
Shareholders 
and/or its 
close 
associates 
after the 
Global 
Offering 
Approximate 
percentage of 
total issued 
Shares after 
the Global 
Offering 
Luxshare 
Precision 
Limited (立訊
精密有限公
司) 
(“Luxshare 
Precision”) 
Luxshare 
Precision is a 
direct wholly-
owned 
subsidiary of 
Luxshare, an 
existing 
Shareholder.  
 
Luxshare is a 
company 
established in 
the PRC on 
May 24, 
2004, the A 
Shares of 
which have 
been listed on 
the Shenzhen 
Stock 
Exchange 
(stock code: 
002475).  
To the best of 
the Directors’ 
knowledge, 
Luxshare 
Limited (立訊
有限公司) 
held as to 
approximately 
37.49% of 
Luxshare. a 
company 
owned as to 
50% by Wang 
Laisheng (王
來勝) and 
50% by Wang 
Laichun (王
來春) and 
save for 
Luxshare 
Limited, no 
other 
shareholders 
of Luxshare 
holds 30% or 
more of its 
shareholding 
interests. 
1,731,800 
 
9.02% 
5,731,800 
 
2.74% 

<<<PAGE 21>>>
21 
 
Name of the 
close 
associates 
Relationship 
with the 
existing 
Shareholders 
Ultimate 
Beneficial 
Owner 
holding 30% 
or more 
interest in 
the close 
associates 
Number of 
Offer 
Shares 
allocated 
to the 
close 
associates 
Approximate 
percentage of 
Offer Shares 
allocated to the 
close associates 
Number of 
Shares held 
by the 
existing 
Shareholders 
and/or its 
close 
associates 
after the 
Global 
Offering 
Approximate 
percentage of 
total issued 
Shares after 
the Global 
Offering 
Shenzhen 
Longsys 
Electronics 
Co., Ltd. (深
圳市江波龍
電子股份有
限公司) 
(“Longsys”) 
The 
controlling 
shareholder of 
Longsys, CAI 
Huabo (蔡華
波), is the 
spouse of XU 
Zhiyan (徐志
燕), an 
existing 
Shareholder.  
Longsys is a 
company 
established in 
the PRC on 
April 27, 
1999, the A 
Shares of 
which have 
been listed on 
the ChiNext 
of Shenzhen 
Stock 
Exchange 
(stock code: 
301308).  
To the best of 
the Directors’ 
knowledge, 
CAI Huabo 
held as to 
approximately 
38.67% of 
Longsys and 
save for CAI 
Huabo, no 
other 
shareholders 
of Longsys 
holds 30% or 
more of its 
shareholding 
interests. 
1,038,500 
 
5.41% 
1,438,500 
 
0.69% 
 
 

<<<PAGE 22>>>
22 
 
Reference is made to the section headed “Others/Additional Information — Placing to Connected 
Client (including those who are close associate of existing Shareholder) with Prior Consents under 
Paragraph 1C(1) of the Placing Guidelines” in this announcement. Shenzhen Qianhai, a GTHT 
Ultimate Client, is a close associate of an existing Shareholder. Details are set out below: 
Name of the 
GTHT 
Ultimate 
Client 
Relationship with 
the existing 
Shareholders 
Ultimate 
Beneficial 
Owner 
holding 30% 
or more 
interest in 
the GTHT 
Ultimate 
Client 
Number 
of Offer 
Shares 
allocated 
to the 
GTHT 
Ultimate 
Client 
Approximate 
percentage 
of Offer 
Shares 
allocated to 
the GTHT 
Ultimate 
Client 
Number of 
Shares held 
by the 
GTHT 
Ultimate 
Client 
and/or its 
close 
associates 
after the 
Global 
Offering 
Approximate 
percentage 
of total 
issued 
Shares after 
the Global 
Offering 
Shenzhen 
Qianhai Huirui 
Investment 
Management 
Co., Ltd. (深圳
市前海汇睿 
投资管理 
有限公司) 
(“Shenzhen 
Qianhai”) 
Shenzhen Qianhai is 
held as to 70% and 
30% by Li Wei-hua 
(李伟华) and Wang 
Daqi (王大琦) (an 
existing Shareholder), 
respectively. 
Shenzhen 
Qianhai is held 
as to 70% and 
30% by Li 
Wei-hua (李伟
华) and Wang 
Daqi (王大
琦), 
respectively. 
548,700 
 
2.86% 
648,700 
 
0.31% 
 
Others 
Under the International Offering, certain Offer Shares were placed to Ju Yuen (Hong Kong) 
International Limited (巨源(香港)國際有限公司), a wholly-owned subsidiary of Zhuhai Jinpin 
Chuangye Share Platform Technology Co., Ltd. (珠海市金品創業共享平台科技有限公司), a 
former Shareholder. 
 
 
 

<<<PAGE 23>>>
23 
 
DISCLAIMERS 
  
 
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited (the “Stock 
Exchange”) and Hong Kong Securities Clearing Company Limited (“HKSCC”) take no 
responsibility for the contents of this announcement, make no representation as to its accuracy or 
completeness and expressly disclaim any liability whatsoever for any loss howsoever arising from 
or in reliance upon the whole or any part of the contents of this announcement. 
This announcement is not for release, publication, distribution, directly or indirectly, in or into the 
United States (including its territories and possessions, any state of the United States and the District 
of Columbia). This announcement does not constitute or form a part of any offer or solicitation to 
purchase or subscribe for securities in the United States. The securities mentioned herein have not 
been, and will not be, registered under the United States Securities Act of 1933, as amended (the “U.S. 
Securities Act”). The securities may not be offered or sold in the United States except pursuant to an 
exemption from the registration requirements of the U.S. Securities Act and in compliance with any 
applicable state securities laws, or outside the United States unless in compliance with Regulation S 
under the U.S. Securities Act. There will be no public offer of securities in the United States. 
The Offer Shares are being offered and sold outside the United States in offshore transactions in reliance 
on Regulation S under the U.S. Securities Act. 
This announcement is for information purposes only and does not constitute an invitation or offer to 
acquire, purchase or subscribe for securities. This announcement is not a prospectus. Potential 
investors should read the Prospectus dated May 18, 2026 issued by Shenzhen SDMC Technology Co., 
Ltd. for detailed information about the Global Offering described below before deciding whether or 
not to invest in the Shares thereby being offered.  
*Potential investors of the Offer Shares should note that the Sole Overall Coordinator (for itself and 
on behalf of the Hong Kong Underwriters) shall be entitled to terminate their obligations under the 
Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events 
set out in the paragraph headed “Underwriting – Underwriting Arrangements and Expenses – Hong 
Kong Public Offering – Hong Kong Underwriting Agreement – Grounds for Termination” in the 
Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which is currently 
expected to be on May 27, 2026). 
 
 

<<<PAGE 24>>>
– 24 –
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering, the total number of the H 
Shares held by the public represents approximately 52.37% of the total issued share capital of 
the Company. Under Rule 19A.13A(1) of the Listing Rules, in the event the expected market 
value of the Company’s H Shares upon Listing does not exceed HK$6 billion, at least 25% 
of the total issued H Shares must be held by the public upon Listing, and the Company’s 
expected public float of 52.37% will satisfy the minimum requirement of 25%. Should the 
expected market value exceeds HK$6.00 billion but not exceeding HK$30.00 billion, the 
minimum public float requirement is the higher of (i) 15% of the total issued H Shares and (ii) 
such percentage of the total issued H Shares as would result in the expected market value of 
the H Shares held by the public being at least HK$1.50 billion upon Listing; in this scenario, 
the Company’s expected public float of 52.37% exceeds the 15% threshold, and the market 
value of such H Shares held by the public would also exceed the HK$1.50 billion requirement 
(e.g., approximately HK$3.60 billion based on the Offer Price of HK$32.8 per Offer Share). 
Therefore, the Company will be able to meet the minimum public float requirement Rule 
8.08 (as amended and replaced by Rule 19A.13A) of the Listing Rules upon Listing in either 
scenario.
Based on an Offer Price of HK$32.80 per H Share, the Company will satisfy the free float 
requirement under Rule 19A.13C of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering, (i) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of 
the Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder immediately after the Global Offering; (iii) the three largest public shareholders 
of the Company do not hold more than 50% of the shares in public hands at the time of the 
Listing in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will 
be at least 300 Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the 
Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Wednesday, 
May 27, 2026 (Hong Kong time), provided that the Global Offering has become unconditional 
and the right of termination described in the section headed “Underwriting – Underwriting 
Arrangements and Expenses – Hong Kong Public Offering – Grounds for Termination” in the 
Prospectus has not been exercised. Investors who trade the H Shares on the basis of publicly 
available allocation details prior to the receipt of H Share certificates or prior to the H Share 
certificates becoming valid evidence of title do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on 
Wednesday, May 27, 2026 (Hong Kong time), it is expected that dealings in the H Shares on 
the Stock Exchange will commence at 9:00 a.m. on Wednesday, May 27, 2026 (Hong Kong 
time). The H Shares will be traded in board lots of 100 H Shares each, and the stock code of 
the H Shares will be 00901.
By order of the Board
Shenzhen SDMC Technology Co., Ltd.
深圳市華曦達科技股份有限公司
Mr. Li Bo
Chairman and Executive Director
Hong Kong, May 26, 2026
As at the date of this announcement, the Board comprises: (i) Mr. Li Bo, Mr. Yan Zhikang, Mr. 
Li Jun and Ms. Dang Hui as executive directors; and (ii) Ms. Luk Pui Yin, Mr. Yin Renyong 
and Dr. Zheng Qian as independent non-executive directors.
