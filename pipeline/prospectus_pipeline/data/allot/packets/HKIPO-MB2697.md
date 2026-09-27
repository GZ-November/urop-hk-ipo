# 配发结果公告抽取任务：2697.HK Guangdong True Health Medical Technology Development Co., Ltd. - B - H Shares

- 公告：ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**29/06/2026 20:35**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0629/2026062901959.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"2697.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same meanings as 
those defined in the prospectus dated June 22, 2026 (the “Prospectus”) issued by Guangdong True Health Medical 
Technology Development Co., Ltd. (廣東真健康醫療科技開發股份有限公司) (the “Company”).
This announcement is for information purposes only and does not constitute an invitation or offer to acquire, purchase 
or subscribe for any securities of our Company. This announcement is not a prospectus. Potential investors should read 
the Prospectus for detailed information about our Company and the Global Offering described below before deciding 
whether or not to invest in the Offer Shares. Any investment decision in relation to the Offer Shares should be taken 
solely in reliance on the information provided in the Prospectus.
This announcement is not for release, publication, distribution, directly or indirectly, in or into the United States 
(including its territories and possessions, any state of the United States and the District of Columbia). This 
announcement does not constitute or form a part of any offer or solicitation to purchase or subscribe for securities 
in the United States or in any other jurisdiction. The Offer Shares have not been, and will not be, registered under 
the United States Securities Act of 1933, as amended from time to time (the “U.S. Securities Act”) or securities law 
of any state or other jurisdiction of the United States and may not be offered, sold, pledged or otherwise transferred 
within the United States, except in transactions exempt from, or not subject to, the registration requirements of the U.S. 
Securities Act. The Company has not intended and does not intend to make any public offer of securities in the United 
States. The Offer Shares are being offered and sold outside the United States in offshore transactions in reliance on 
Regulation S under the U.S. Securities Act.
In connection with the Global Offering, China International Capital Corporation Hong Kong Securities Limited, 
as stabilizing manager (the “Stabilizing Manager”), its affiliates or any person acting for it, on behalf of the 
Underwriters, may over-allocate or effect transactions with a view to stabilizing or maintaining the market price of 
the Offer Shares at a level higher than that which might otherwise prevail in the open market for a limited period after 
the Listing Date. However, as there has been no over-allocation in the International Offering, there will not be any 
stabilization activities to be undertaken by the Stabilizing Manager after the Listing in connection with the Global 
Offering.
Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall Coordinators (for 
themselves and on behalf of the Hong Kong Underwriters) shall, in their sole and absolute discretion, be entitled to 
terminate the Hong Kong Underwriting Agreement with immediate effect upon the occurrence of any of the events set 
out in the section headed “Underwriting – Underwriting Arrangements and Expenses – Hong Kong Public Offering – 
Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on the Listing Date (which 
is currently expected to be on Tuesday, June 30, 2026).

<<<PAGE 2>>>
2
Guangdong True Health Medical 
Technology Development Co., Ltd.
廣東真健康醫療科技開發股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under 
the Global Offering
:
3,564,700 H Shares
Number of Hong Kong Offer Shares
:
356,480 H Shares
Number of International Offer Shares
:
3,208,220 H Shares
Final Offer Price
:
HK$126.20 per Offer Share, plus brokerage 
 of 1.0%, SFC transaction levy of 
 0.0027%, Stock Exchange trading fee of 
 0.00565% and AFRC transaction levy of 
 0.00015%
Nominal Value
:
RMB1.00 per H Share
Stock code
:
2697
Joint Sponsors, Overall Coordinators, Joint Global Coordinators, 
Joint Bookrunners and Joint Lead Managers

<<<PAGE 3>>>
3
Guangdong True Health Medical
Technology Development Co., Ltd.
廣東真健康醫療科技開發股份有限公司
ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the same 
meanings as those defined in the Prospectus issued by the Company.
Warning: In view of high concentration of shareholding in a small number of Shareholders, 
Shareholders and prospective investors should be aware that the price of the H Shares 
could move substantially even with a small number of H Shares traded and should exercise 
extreme caution when dealing in the H Shares.
SUMMARY
Company Information
Stock Code
2697
Stock Short Name
TH MEDICAL-B
Dealings commencement date
June 30, 2026*
* 
see note at the end of the announcement
Price Information
Final Offer Price
HK$126.20
Offer Shares and Share Capital
Number of Offer Shares
3,564,700 H Shares
Number of Offer Shares in Hong Kong Public Offering
356,480 H Shares
Number of Offer Shares in International Offering
3,208,220 H Shares
Number of issued Shares upon Listing
35,647,003 H Shares
Over-allocation
Number of Offer Shares over-allocated
0
Note: There has been no over-allocation of Offer Shares in the International Offering. Therefore, (i) the Over-
allotment Option will not be exercised and will lapse upon Listing; and (ii) there will not be any stabilization 
activities to be undertaken by the Stabilizing Manager after the Listing in connection with the Global 
Offering.

<<<PAGE 4>>>
4
Proceeds
Gross proceeds (Note)
HK$449.9 million
Less: Estimated listing expenses payable based on Final Offer Price
HK$65.9 million
Net Proceeds
HK$384.0 million
Note: Gross proceeds refers to the amount which the Company is entitled to receive. For details of the use of 
proceeds, please refer to the section headed “Future Plans and Use of Proceeds” of the Prospectus.
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
No. of valid applications
128,208
No. of successful applications
15,453
Subscription level
1,790.4 times
Reallocation
N/A
No. of Offer Shares initially available under the Hong Kong Public 
Offering
356,480
No. of Offer Shares allocated from the International Offering
0
Final no. of Offer Shares under the Hong Kong Public Offering
356,480
% of Offer Shares under the Hong Kong Public Offering to the Global 
Offering
10.00%
Note: For details of the final allocation of H Shares to the Hong Kong Public Offering, investors can refer to 
the “Allotment Results” page at the designated results of allocation at https://www.hkeipo.hk/iporesult or 
https://www.hkeipo.hk/IPOResult with a “search by ID” function.
INTERNATIONAL OFFERING
No. of placees
107
Subscription Level
2.2 times
No. of Offer Shares initially available under the International Offering
3,208,220
No. of Offer Shares reallocated to the Hong Kong Public Offering
0
Final no. of Offer Shares under the International Offering
3,208,220
% of Offer Shares under the International Offering to the Global 
Offering
90.00%

<<<PAGE 5>>>
5
The Directors confirm that, to the best of their knowledge, information and belief, (i) none of the 
Offer Shares subscribed by the placees and the public have been financed directly or indirectly 
by the Company, any of the Directors, chief executive of the Company, Controlling Shareholders, 
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries or 
their respective close associates; and (ii) none of the placees and the public who have purchased 
the Offer Shares are accustomed to taking instructions from the Company, any of the Directors, 
chief executive of the Company, Controlling Shareholders, substantial Shareholders, existing 
Shareholders of the Company or any of its subsidiaries or their respective close associates in 
relation to the acquisition, disposal, voting or other disposition of H Shares registered in his/her/its 
name or otherwise held by him/her/it.
LOCK-UP UNDERTAKINGS
Controlling Shareholders
Name Note 1
No. of 
H Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued 
H Shares 
after the 
Global 
Offering 
subject to 
lock-up 
undertakings 
upon 
Listing Note 2
% of total 
issued share 
capital of the 
Company 
subject to 
lock-up 
undertakings 
upon 
Listing Note 2
Last day 
subject to 
the lock-up 
undertakings Note 2
Guangdong Hengqin Renyang 
Biotechnology Center (Limited 
Partnership)* (廣東橫琴任陽生物科技中心
(有限合夥))
(“Renyang Biotechnology”) Note 3
3,360,000
9.43%
9.43%
June 29, 2027
Zhuhai Chengzhen Health Technology 
Partnership (Limited Partnership)* (珠海誠
真健康科技合夥企業(有限合夥))
(“Chengzhen Health”) Note 3
3,000,000
8.42%
8.42%
June 29, 2027
Zhuhai Jiarun Tongchuang Technology 
Development Partnership (Limited 
Partnership)* (珠海嘉潤同創科技發展合夥
企業(有限合夥))
(“Jiarun Tongchuang”) Note 3
2,400,000
6.73%
6.73%
June 29, 2027
Zhuhai Jiarun Hechuang Technology 
Development Partnership (Limited 
Partnership)* (珠海嘉潤合創科技發展合夥
企業(有限合夥))
(“Jiarun Hechuang”) Note 3
2,293,900
6.44%
6.44%
June 29, 2027

<<<PAGE 6>>>
6
Name Note 1
No. of 
H Shares 
held in the 
Company 
subject to 
lock-up 
undertakings 
upon Listing
% of total 
issued 
H Shares 
after the 
Global 
Offering 
subject to 
lock-up 
undertakings 
upon 
Listing Note 2
% of total 
issued share 
capital of the 
Company 
subject to 
lock-up 
undertakings 
upon 
Listing Note 2
Last day 
subject to 
the lock-up 
undertakings Note 2
Zhuhai Meijirui Medical Technology 
Partnership (Limited Partnership)* (珠
海美吉睿醫療科技合夥企業(有限合夥)) 
(“Zhuhai Meijirui”) Note 3
2,071,682
5.81%
5.81%
June 29, 2027
Zhuhai Jiarun Xinchuang Technology 
Development Partnership (Limited 
Partnership)* (珠海嘉潤新創科技發展合夥
企業(有限合夥))
(“Jiarun Xinchuang”) Note 3
1,800,000
5.05%
5.05%
June 29, 2027
Xinhui Runkang (Zhuhai Hengqin) 
Investment Consulting Center (Limited 
Partnership)* (欣慧潤康(珠海橫琴) 
投資諮詢中心(有限合夥))  
(“Xinhui Runkang”) Note 3
33,650
0.09%
0.09%
June 29, 2027
Subtotal of Controlling Shareholders
14,959,232
41.96%
41.96%
* 
For identification purposes only
Notes:
1. 
For illustrative purposes only, this subsection lists only those members of the Controlling Shareholders who 
hold H Shares directly in the Company.
2. 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law. The 
required lock-up for existing Shareholders ends on June 29, 2027, being 12 months following the Listing 
Date. Pursuant to Rule 10.07 of the Listing Rules, each of the Controlling Shareholders has undertaken to the 
Stock Exchange and the Company that, she or it shall comply with the applicable lock-up requirements. For 
further details, please refer to the section headed “Underwriting – Underwriting Arrangements – Lock Up 
Arrangement – Undertakings to the Stock Exchange Pursuant to the Listing Rules – (B) Undertakings by the 
Controlling Shareholders” in the Prospectus.
3. 
Renxiang Biotechnology which is held as to 99.99% by Ms. Cheong Hou Iam (張昊任) (“Ms. Cheong”), is 
the sole general partner of, and is, pursuant to the relevant partnership agreements, entitled to exercise all 
voting rights in, each of Renyang Biotechnology, Chengzhen Health, Jiarun Tongchuang, Jiarun Hechuang, 
Zhuhai Meijirui, Jiarun Xinchuang and Xinhui Runkang.
Each of Renyang Biotechnology, Chengzhen Health and Jiarun Tongchuang is owned as to 99% by China 
True Health Medical Technology Co., Ltd. (中國真健康醫療科技有限公司) (“China True Health Medical”) 
as its sole limited partner and 1% by Renxiang Biotechnology as its general partner. Jiarun Hechuang is 
owned as to 99% by China Shui Mu Medical Technology Company Limited (中國水木醫療科技有限公
司) (“Shuimu Medical Technology”) as its sole limited partner and 1% by Renxiang Biotechnology as its 
general partner. Each of China True Health Medical and Shuimu Medical Technology is owned as to 96.67% 
by Ms. Cheong.
As such, (i) Ms. Cheong is the ultimate beneficial owner of each of Renyang Biotechnology, Chengzhen 
Health, Jiarun Tongchuang, Jiarun Hechuang, Zhuhai Meijirui, Jiarun Xinchuang and Xinhui Runkang; 
and (ii) Ms. Cheong, Renxiang Biotechnology, China True Health Medical, Shuimu Medical Technology, 
Renyang Biotechnology, Chengzhen Health, Jiarun Tongchuang, Jiarun Hechuang, Zhuhai Meijirui, Jiarun 
Xinchuang and Xinhui Runkang are a group of Controlling Shareholders. For details of the Controlling 
Shareholders, please refer to the section headed “Relationship with our Controlling Shareholders – Our 
Controlling Shareholders” in the Prospectus.

<<<PAGE 7>>>
7
Pre-IPO Investors (as defined in the “History and Corporate Structure” section of the 
Prospectus)
Name Note 1
No. of H Shares 
held in the 
Company subject 
to lock-up 
undertakings 
upon Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings 
upon Listing Note 2
% of total issued 
share capital of the 
Company subject 
to lock-up 
undertakings 
upon Listing Note 2
Last day 
subject to the 
lock-up 
undertakings Note 2
Sophisticated Investors
CICC Entities
Hengqin Guangdong Macao Deep 
Cooperation Zone Industrial Investment 
Fund (Limited Partnership)* (橫琴粵澳
深度合作區產業投資基金(有限合夥)) 
(“Hengqin Industrial”)
1,438,669
4.04%
4.04%
June 29, 2027
Huzhou CICC Qihe Equity Investment 
Partnership (Limited Partnership)* (湖州
中金啟合股權投資合夥企業(有限合夥)) 
(“CICC Qihe”)
431,601
1.21%
1.21%
June 29, 2027
Dongrong No. 1 (Zhuhai Hengqin) 
Equity Investment Partnership (Limited 
Partnership)* (東融壹號(珠海橫琴)股權投
資合夥企業(有限合夥))  
(“Dongrong No. 1”)
143,867
0.40%
0.40%
June 29, 2027
Subtotal
2,014,137
5.65%
5.65%
Beijing Jinke Huiyu Venture Capital 
Partnership (Limited Partnership)* (北京
金科匯鈺創業投資合夥企業(有限合夥)) 
(“Jinke Huiyu”)
1,955,547
5.49%
5.49%
June 29, 2027
Subtotal of Sophisticated Investors
3,969,684
11.14%
11.14%
Other Pre-IPO Investors
Hengqin Guangdong-Macao Development 
& Investment Co., Ltd.* (橫琴粵澳開發投
資有限公司)
(“Guangdong-Macao Investment”)
2,877,337
8.07%
8.07%
June 29, 2027
Zhuhai Taike Maidi Technology 
Development Center (Limited Partnership)* 
(珠海泰科麥迪科技發展中心(有限合夥)) 
(“Taike Maidi”)
1,440,000
4.04%
4.04%
June 29, 2027

<<<PAGE 8>>>
8
Name Note 1
No. of H Shares 
held in the 
Company subject 
to lock-up 
undertakings 
upon Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings 
upon Listing Note 2
% of total issued 
share capital of the 
Company subject 
to lock-up 
undertakings 
upon Listing Note 2
Last day 
subject to the 
lock-up 
undertakings Note 2
KIP Entities
JingDe (Guangzhou) Equity Investment 
Partnership (LP)* (景得(廣州)股權
投資合夥企業(有限合夥)) (“JingDe 
(Guangzhou)”)
673,090
1.89%
1.89%
June 29, 2027
KIP (ZhangJiaGang) Venture Capital LLP* 
(韓投(張家港)股權投資合夥企業(有限合
夥)) (“KIP (ZhangJiaGang)”)
673,090
1.89%
1.89%
June 29, 2027
Subtotal
1,346,180
3.78%
3.78%
Ligong Innovation Entities
Beijing New Energy Technology Innovation 
Fund (Limited Partnership)* (北京新動能
科技創新基金(有限合夥)) (“Beijing New 
Energy”)
795,470
2.23%
2.23%
June 29, 2027
Qingdao Rongyu Venture Capital Fund 
Partnership (Limited Partnership)* (青島
榮昱創業投資基金合夥企業(有限合夥)) 
(“Qingdao Rongyu”)
259,840
0.73%
0.73%
June 29, 2027
Subtotal
1,055,310
2.96%
2.96%
Beijing Shuimu Dongfang Medical Robotic 
Technology Innovation Center Co., Ltd.* 
(北京水木東方醫用機器人技術創新中心有
限公司) (“Shuimu Dongfang”)
1,038,060
2.91%
2.91%
June 29, 2027
Gaorong Ventures Entities
Beijing Gaorong Phase IV Kangteng 
Equity Investment Partnership (Limited 
Partnership)* (北京高榕四期康騰股權投
資合夥企業(有限合夥)) (“Gaorong Phase 
IV”)
696,510
1.95%
1.95%
June 29, 2027
Chengdu Tianfu New Area Gaorong Phase 
IV Kangyong Investment Partnership 
(Limited Partnership)* (成都市天府新區
高榕四期康永投資合夥企業(有限合夥)) 
(“Kangyong Investment”)
122,904
0.34%
0.34%
June 29, 2027
Subtotal
819,414
2.30%
2.30%

<<<PAGE 9>>>
9
Name Note 1
No. of H Shares 
held in the 
Company subject 
to lock-up 
undertakings 
upon Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings 
upon Listing Note 2
% of total issued 
share capital of the 
Company subject 
to lock-up 
undertakings 
upon Listing Note 2
Last day 
subject to the 
lock-up 
undertakings Note 2
Zhuhai Gree Group Entities
Zhuhai Hengqin Golden Investment Venture 
Capital Fund Partnership (L.P.)* (珠海橫
琴金投創業投資基金合夥企業(有限合夥)) 
(“Hengqin Golden Investment”)
535,420
1.50%
1.50%
June 29, 2027
Zhuhai Ligao No. 2 Equity Investment Fund 
Partnership (Limited Partnership)* (珠海力
高貳號股權投資基金合夥企業(有限合夥)) 
(“Ligao No. 2”)
198,870
0.56%
0.56%
June 29, 2027
Subtotal
734,290
2.06%
2.06%
Taiping (Shenzhen) Medical and Health 
Industry Private Equity Investment Fund 
Partnership (Limited Partnership)* (太平
(深圳)醫療健康產業私募股權投資基金
合夥企業(有限合夥)) (“Taiping Medical 
Investment Fund”)
719,335
2.02%
2.02%
June 29, 2027
Beijing Zhongguancun Zhiyou Investment 
Partnership (L.P.) (北京中關村智友投資
合夥企業(有限合夥)) (“Zhongguancun 
Zhiyou”)
664,900
1.87%
1.87%
June 29, 2027
Beijing Jingantai Technology Development 
Co., Ltd.* (北京京安泰科技發展有限公司) 
(“Beijing Jingantai”)
615,030
1.73%
1.73%
June 29, 2027
Hengqin Shenhe Industrial Investment 
Co., Ltd.* (橫琴深合產業投資有限公司) 
(“Hengqin Shenhe Industrial
Investment”)
431,601
1.21%
1.21%
June 29, 2027
Beijing Shuimu Linghang Entrepreneurship 
Investment Center (Limited Partnership)* 
(北京水木領航創業投資中心(有限合夥)) 
(“Shuimu Linghang”)
249,340
0.70%
0.70%
June 29, 2027
Novel Robotics Limited (諾威機器人有限
公司) (“Novel Robotics”)
207,780
0.58%
0.58%
June 29, 2027
X Technology Fund, L.P. (“X 
Technology”)
207,780
0.58%
0.58%
June 29, 2027

<<<PAGE 10>>>
10
Name Note 1
No. of H Shares 
held in the 
Company subject 
to lock-up 
undertakings 
upon Listing
% of total issued 
H Shares after the 
Global Offering 
subject to lock-up 
undertakings 
upon Listing Note 2
% of total issued 
share capital of the 
Company subject 
to lock-up 
undertakings 
upon Listing Note 2
Last day 
subject to the 
lock-up 
undertakings Note 2
Zhuhai Huajin Lingyue Intelligent 
Manufacturing Industry Investment Fund 
(Limited Partnership)* (珠海華金領越智能
製造產業投資基金(有限合夥)) (“Huajin 
Lingyue”)
198,870
0.56%
0.56%
June 29, 2027
Zhuhai Hengqin Xinti Investment 
Partnership (Limited Partnership)* (珠
海橫琴辛醍投資合夥企業(有限合夥)) 
(“Hengqin Xinti”)
198,870
0.56%
0.56%
June 29, 2027
Beijing Dongsheng Bozhan Science & 
Technology Development Co., Ltd.* (北京
東升博展科技發展有限公司) (“Dongsheng 
Bozhan”)
178,980
0.50%
0.50%
June 29, 2027
Beijing Lide Gongchuang Intelligent 
Robotic Technology Co., Ltd.* (北京立
德共創智能機器人科技有限公司) (“Lide 
Gongchuang”)
83,110
0.23%
0.23%
June 29, 2027
Beijing Deruida Wealth Technology 
Management Center (Limited Partnership)* 
(北京德睿達財富科技管理中心(有限合
夥)) (“Deruida Wealth”)
67,310
0.19%
0.19%
June 29, 2027
Shenzhen Ruisheng Equity Investment Fund 
Partnership (Limited Partnership)* (深圳
瑞昇股權投資基金合夥企業(有限合夥)) 
(“Shenzhen Ruisheng”)
19,890
0.06%
0.06%
June 29, 2027
Subtotal of other Pre-IPO Investors
13,153,387
36.90%
36.90%
Subtotal of all Pre-IPO Investors
17,123,071
48.04%
48.04%
* 
For identification purposes only
Notes:
1. 
Please refer to the section headed “History and Corporate Structure — Pre-IPO Investments – Information 
about the Pre-IPO Investors” in the Prospectus for details of the Pre IPO Investors.
2. 
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Law.

<<<PAGE 11>>>
11
PLACEE CONCENTRATION ANALYSIS
Placees*
Number of 
H Shares 
allotted
Allotment 
as % of 
International 
Offering
Allotment 
as % of 
total Offer 
Shares
Number of 
H Shares 
held upon 
Listing
% of total 
issued share 
capital upon 
Listing
Top 1
198,000
6.17%
5.55%
198,000
0.56%
Top 5
735,040
22.91%
20.62%
735,040
2.06%
Top 10
1,210,280
37.72%
33.95%
1,210,280
3.40%
Top 25
2,005,360
62.51%
56.26%
2,005,360
5.63%
Note:
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
as % of 
total Offer 
Shares
Number of 
H Shares 
held upon 
Listing
% of total 
issued share 
capital upon 
Listing
Top 1
0
N/A
N/A
14,959,232
41.96%
Top 5
0
N/A
N/A
23,246,253
65.21%
Top 10
0
N/A
N/A
28,239,507
79.22%
Top 25
735,040
22.91%
20.62%
32,647,033
91.58%
Note:
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
as % of 
total Offer 
Shares
Number of 
H Shares 
held upon 
Listing
% of total 
issued share 
capital upon 
Listing
Top 1
0
N/A
N/A
14,959,232
41.96%
Top 5
0
N/A
N/A
23,246,253
65.21%
Top 10
0
N/A
N/A
28,239,507
79.22%
Top 25
735,040
22.91%
20.62%
32,647,033
91.58%
Note:
* 
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon Listing.

<<<PAGE 12>>>
12
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 128,208 valid 
applications made by the public will be conditionally allocated on the basis set out below:
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
total number of 
H Shares 
applied for
20
41,427
829 out of 41,427 applicants to receive 20 H Shares
2.00%
40
7,588
209 out of 7,588 applicants to receive 20 H Shares
1.38%
60
27,564
912 out of 27,564 applicants to receive 20 H Shares
1.10%
80
2,610
99 out of 2,610 applicants to receive 20 H Shares
0.95%
100
2,326
98 out of 2,326 applicants to receive 20 H Shares
0.84%
120
1,081
50 out of 1,081 applicants to receive 20 H Shares
0.77%
140
894
44 out of 894 applicants to receive 20 H Shares
0.70%
160
789
41 out of 789 applicants to receive 20 H Shares
0.65%
180
666
37 out of 666 applicants to receive 20 H Shares
0.62%
200
5,197
298 out of 5,197 applicants to receive 20 H Shares
0.57%
300
5,819
402 out of 5,819 applicants to receive 20 H Shares
0.46%
400
2,139
169 out of 2,139 applicants to receive 20 H Shares
0.40%
500
1,281
112 out of 1,281 applicants to receive 20 H Shares
0.35%
600
966
92 out of 966 applicants to receive 20 H Shares
0.32%
700
1,574
160 out of 1,574 applicants to receive 20 H Shares
0.29%
800
737
80 out of 737 applicants to receive 20 H Shares
0.27%
900
448
52 out of 448 applicants to receive 20 H Shares
0.26%
1,000
2,980
357 out of 2,980 applicants to receive 20 H Shares
0.24%
2,000
2,421
398 out of 2,421 applicants to receive 20 H Shares
0.16%
3,000
1,755
347 out of 1,755 applicants to receive 20 H Shares
0.13%
4,000
1,468
332 out of 1,468 applicants to receive 20 H Shares
0.11%
5,000
1,032
258 out of 1,032 applicants to receive 20 H Shares
0.10%
6,000
774
211 out of 774 applicants to receive 20 H Shares
0.09%
7,000
581
170 out of 581 applicants to receive 20 H Shares
0.08%
8,000
794
246 out of 794 applicants to receive 20 H Shares
0.08%
9,000
455
149 out of 455 applicants to receive 20 H Shares
0.07%
10,000
2,874
986 out of 2,874 applicants to receive 20 H Shares
0.07%
20,000
1,760
829 out of 1,760 applicants to receive 20 H Shares
0.05%
30,000
1,667
945 out of 1,667 applicants to receive 20 H Shares
0.04%
Total
121,667
Total number of Pool A successful applicants: 8,912

<<<PAGE 13>>>
13
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
total number of
H Shares 
applied for
40,000
2,994
20 H Shares
0.05%
50,000
744
20 H Shares plus 106 out of 744 applicants to receive an 
 additional 20 H Shares
0.05%
60,000
524
20 H Shares plus 144 out of 524 applicants to receive an 
 additional 20 H Shares
0.04%
70,000
341
20 H Shares plus 135 out of 341 applicants to receive an 
 additional 20 H Shares
0.04%
80,000
314
20 H Shares plus 161 out of 314 applicants to receive an 
 additional 20 H Shares
0.04%
90,000
171
20 H Shares plus 107 out of 171 applicants to receive an 
 additional 20 H Shares
0.04%
100,000
281
20 H Shares plus 204 out of 281 applicants to receive an 
 additional 20 H Shares
0.03%
120,000
199
20 H Shares plus 184 out of 199 applicants to receive an 
 additional 20 H Shares
0.03%
140,000
145
40 H Shares plus 16 out of 145 applicants to receive an 
 additional 20 H Shares
0.03%
160,000
127
40 H Shares plus 36 out of 127 applicants to receive an 
 additional 20 H Shares
0.03%
178,240
701
40 H Shares plus 305 out of 701 applicants to receive an 
 additional 20 H Shares
0.03%
Total
6,541
Total number of Pool B successful applicants: 6,541
As of the date of this announcement, the relevant subscription monies previously deposited in the 
designated nominee accounts have been remitted back to the accounts of all HKSCC participants. 
Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in respect of 
which consent has been obtained, the Company has complied with the Listing Rules and guidance 
materials in relation to the placing, allotment and listing of the Company’s H Shares.
The Directors confirm that, to the best of their knowledge, the consideration paid by the placees 
or the public (as the case may be) directly or indirectly for each Offer Share subscribed for or 
purchased by them was the same as the final Offer Price in addition to any brokerage, AFRC 
transaction levy, SFC transaction levy and trading fee payable.

<<<PAGE 14>>>
14
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and 
Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this 
announcement, make no representation as to its accuracy or completeness and expressly disclaim 
any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or 
any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or into 
the United States (including its territories and possessions, any state of the United States and 
the District of Columbia). This announcement does not constitute or form a part of any offer or 
solicitation to purchase or subscribe for securities in the United States. The securities mentioned 
herein have not been, and will not be, registered under the United States Securities Act of 1933, 
as amended (the “U.S. Securities Act”). The securities may not be offered or sold in the United 
States except pursuant to an exemption from the registration requirements of the U.S. Securities 
Act and in compliance with any applicable state securities laws, or outside the United States 
unless in compliance with Regulation S under the U.S. Securities Act. There will be no public 
offer of securities in the United States. The Offer Shares are being offered and sold outside the 
United States in offshore transactions in reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation or 
offer to acquire, purchase or subscribe for securities. This announcement is not a prospectus. 
Potential investors should read the Prospectus dated June 22, 2026 issued by Guangdong True 
Health Medical Technology Development Co., Ltd. (廣東真健康醫療科技開發股份有限公司) 
for detailed information about the Global Offering described below before deciding whether or 
not to invest in the H Shares thereby being offered.
* Potential investors of the Offer Shares should note that the Joint Sponsors and the Overall 
Coordinators (for themselves and on behalf of the Hong Kong Underwriters) shall, in their 
sole and absolute discretion, be entitled to terminate the Hong Kong Underwriting Agreement 
with immediate effect upon the occurrence of any of the events set out in the section headed 
“Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — 
Grounds for Termination” in the Prospectus at any time prior to 8:00 a.m. (Hong Kong time) on 
the Listing Date (which is currently expected to be on Tuesday, June 30, 2026).

<<<PAGE 15>>>
15
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering, an aggregate of 15,205,874 H Shares 
or approximately 42.66% of the total issued share capital of the Company will be held in the public 
hands. For details of the Shareholders that are not counted towards the public float, please refer to 
the section headed “History and Corporate Structure – Public Float” in the Prospectus. Therefore, 
the number of Shares in the public hands represents no less than 25% of the total issued share 
capital of the Company, satisfying the minimum percentage requirement in compliance with Rule 
19A.13A of the Listing Rules.
Pursuant to the applicable PRC law, within the 12 months following the Listing Date, all existing 
Shareholders (including the Pre-IPO Investors) cannot dispose of any of the Shares held by them. 
As such, the H Shares held by the existing Shareholders (including the Pre-IPO Investors) upon the 
Listing shall not be counted towards the free float of the H Shares of the Company at the time of 
Listing. Based on an Offer Price of HK$126.20 per Offer Share, the Company will satisfy with the 
free float requirement under Rule 19A.13C(1)(a) of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global Offering, (i) 
no placee will, individually, be placed more than 10% of the enlarged issued share capital of 
the Company immediately after the Global Offering; (ii) there will not be any new substantial 
Shareholder immediately after the Global Offering; (iii) the three largest public shareholders of 
the Company do not hold more than 50% of the H shares in public hands at the time of the Listing 
in compliance with Rules 8.08(3) and 8.24 of the Listing Rules; and (iv) there will be at least 300 
Shareholders at the time of the Listing in compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8:00 a.m. on Tuesday, June 
30, 2026 (Hong Kong time), provided that the Global Offering has become unconditional and the 
right of termination described in the section headed “Underwriting – Underwriting Arrangements – 
Hong Kong Public Offering – Grounds for Termination” in the Prospectus has not been exercised. 
Investors who trade the H Shares on the basis of publicly available allocation details prior to the 
receipt of H Share certificates or prior to the H Share certificates becoming valid evidence of title 
do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8:00 a.m. on Tuesday, June 
30, 2026 (Hong Kong time), it is expected that dealings in the H Shares on the Stock Exchange 
will commence at 9:00 a.m. on Tuesday, June 30, 2026 (Hong Kong time). The H Shares will be 
traded in board lots of 20 H Shares each, and the stock code of the H Shares will be 2697.
By order of the Board
Guangdong True Health Medical Technology Development Co., Ltd.
Ms. Cheong Hou Iam
Chairperson, Executive Director and General Manager
Hong Kong, June 29, 2026
As of the date of this announcement, the Board comprises: (i) Ms. Cheong Hou Iam, Ms. Chen 
Miaoping and Ms. Guo Jian as executive Directors; (ii) Ms. Mo Jinling as non-executive Director; 
and (iii) Dr. Liu Lianggang, Mr. Ng Kun Seng Chris and Mr. Ma Jianming as independent 
non-executive Directors.
