# 配发结果公告抽取任务：9903.HK Shanghai Iluvatar CoreX Semiconductor Co., Ltd. - H shares

- 公告：ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS
- 刊发时间（港交所元数据）：**07/01/2026 21:58**  ← `col_CR` 直接填这个值
- 公告 PDF：https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0107/2026010701802.pdf
- 来源索引：out/allotment_index.json

## 这份文件是什么

这是**配发结果公告**（ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS），
不是招股书。它给出**最终**的发售结果：最终发售股数、回拨情况、超额配售权是否行使、
公众认购倍数与申请数目、基石投资者最终获配、上市时公众持股与自由流通等。

**必须用公告里的最终值**，不要用招股书的初始发售规模或估计值。

## 唯一输出契约

只输出一个 JSON 对象，顶层**只能**有 `code` 和 `fields`：

```json
{"code":"9903.HK","fields":{"col_CK":{"value":0.6886,"page":3,"quote":"<=200字符原文","confidence":"high"}}}
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
Shanghai Iluvatar CoreX Semiconductor Co., Ltd.
上海天數智芯半導體股份有限公司
ANNOUNCEMENT OF ALLOTMENT RESULTS
Unless otherwise defined herein, capitalized terms used in this announcement shall have the
same meanings as those defined in the prospectus dated December 30, 2025 (the
“Prospectus”) issued by Shanghai Iluvatar CoreX Semiconductor Co., Ltd. (上海天數智
芯半導體股份有限公司) (the “Company”).
Warning: In view of high concentration of shareholding in a small number of Shareholders,
Shareholders and prospective investors should be aware that the price of the H Shares could
move substantially even with a small number of H Shares traded and should exercise
extreme caution when dealing in the H Shares.
SUMMARY
Company information
Stock code
9903
Stock short name
ILUVATAR COREX
Dealings commencement date
January 8, 2026*
*
see note at the end of the announcement
Price Information
Offer Price
HK$144.60
Offer Price Adjustment exercised
N/A
Offer Shares and Share Capital
Number of Offer Shares
25,431,800
Final Number of Offer Shares in Hong Kong Public
Offering
2,543,200
Final Number of Offer Shares in International
Offering
22,888,600
Number of issued shares upon Listing
254,317,736
Proceeds
Gross proceeds (Note)
HK$3,677.4 million
Less: Estimated listing expenses payable based on
Offer Price
HK$168.2 million
Net proceeds
HK$3,509.3 million
Note:
Gross proceeds refers to the amount which the Company is entitled to receive. For
details of the use of proceeds, see “Future Plans and Use of Proceeds” of the
Prospectus.
– 1 –

<<<PAGE 2>>>
ALLOTMENT RESULTS DETAILS
HONG KONG PUBLIC OFFERING
Number of valid applications
180,802
Number of successful applications
22,451
Subscription level
414.24 times
Number of Offer Shares initially available under the
Hong Kong Public Offering
2,543,200
Final number of Offer Shares under the Hong Kong
Public Offering
2,543,200
Claw-back triggered
N/A
Number of Offer Shares reallocated from
International Offering to Hong Kong Public Offering
0
% of final number of Offer Shares under the Hong
Kong Public Offering to the Global Offering
10.00%
Note:
For details of the final allocation of Shares to the Hong Kong Public Offering, investors can refer to
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
Weblink English Search Engine (The English website link to the
H Share Registrar’s search function for public offer allottees)
www.eipo.com.hk/eIPOAllotment
Weblink Chinese Search Engine (The Chinese website link to the
H Share Registrar’s search function for public offer allottees)
www.eipo.com.hk/eIPOAllotment
Weblink English Allottee List (The English website link to the full
list of allotted public offer subscribers on the H Share Registrar’s
website)
www.eipo.com.hk/eIPOAllotment
Weblink Chinese Allottee List (The Chinese website link to the
full list of allotted public offer subscribers on the H Share
Registrar’s website)
www.eipo.com.hk/eIPOAllotment
– 2 –

<<<PAGE 3>>>
INTERNATIONAL OFFERING
Number of placees
121
Subscription level
10.68 times
Number of Offer Shares initially available under the
International Offering
22,888,600
Final number of Offer Shares under the International
Offering
22,888,600
% of Offer Shares under the International Offering to
the Global Offering
90%
The Directors confirm that, to the best of their knowledge, information and belief, save for
allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules, consents
under paragraphs 1C(1) and 1C(2) of Appendix F1 to the Listing Rules (the “Placing
Guidelines”) and Chapter 4.15 of the Guide for New Listing Applicants granted by the
Stock Exchange to permit the Company to, among other things, place certain H Shares in
the International Offering to close associates of certain existing Shareholders, Cornerstone
Investors and connected clients, (i) none of the Offer Shares subscribed by the placees and
the public have been financed directly or indirectly by the Company, any of the Directors,
chief executive of the Company, substantial Shareholders, existing Shareholders of the
Company or any of its subsidiaries or their respective close associates; and (ii) none of the
placees and the public who have purchased the Offer Shares are accustomed to taking
instructions from the Company, any of the Directors, chief executive of the Company,
substantial Shareholders, existing Shareholders of the Company or any of its subsidiaries or
their respective close associates in relation to the acquisition, disposal, voting or other
disposition of Shares registered in his/her/its name or otherwise held by him/her/it.
– 3 –

<<<PAGE 4>>>
The placees in the International Offering include the following:
Cornerstone Investors
Investor(1)
Number of
Offer Shares
allocated(2)
% of
Offer Shares
% of total
issued H Shares
after the Global
Offering
% of the total
issued Shares
after the Global
Offering
Existing
Shareholders or
their close
associates
ZTE (H.K.) LIMITED(3)
151,000
0.59%
0.06%
0.06%
No
XN Mountain International
Limited
914,700
3.60%
0.37%
0.36%
Yes
Wind Sabre Fund SPC acting
on behalf and for the account
of Wind Sabre Opportunities
Fund SP
1,076,100
4.23%
0.44%
0.42%
No
UBS Asset Management
(Singapore) Ltd.(3)
538,000
2.12%
0.22%
0.21%
No
Teamsun Technology (HK)
Limited
228,200
0.90%
0.09%
0.09%
No
Qin Wan Investment Limited
762,600
3.00%
0.31%
0.30%
No
OCM Limited
532,700
2.09%
0.22%
0.21%
No
Ocean Fine Industrial Limited
537,100
2.11%
0.22%
0.21%
No
Huatai Capital Investment
Limited (in connection with
OTC swaps for Jiujiu Hengxin
(Xiamen) Private Fund
Management Co., Ltd.)
1,129,900
4.44%
0.46%
0.44%
No
Fourth Paradigm
International Limited
691,500
2.72%
0.28%
0.27%
No
Engine International
Technology Co., Limited
228,800
0.90%
0.09%
0.09%
No
Duckling Fund, L.P.
1,076,100
4.23%
0.44%
0.42%
No
DeepRoot Alpha Ltd
215,200
0.85%
0.09%
0.08%
No
China Universal Asset
Management (Hong Kong)
Company Limited
1,076,100
4.23%
0.44%
0.42%
No
China Orient International
Asset Management Limited —
China Orient Enhanced
Income Fund
376,600
1.48%
0.15%
0.15%
No
China Orient International
Asset Management Limited —
China Orient Multi-Strategy
Master Fund
161,400
0.63%
0.07%
0.06%
No
China Asset Management
(Hong Kong) Limited
322,800
1.27%
0.13%
0.13%
No
CFIG Holdings Limited(3)
114,400
0.45%
0.05%
0.04%
No
Alphahill Capital Limited
807,100
3.17%
0.33%
0.32%
No
Total
10,940,300
43.02%
4.46%
4.30%
– 4 –

<<<PAGE 5>>>
Notes:
(1)
For further details of the Cornerstone Investors, see “Cornerstone Investors” in the Prospectus.
(2)
The number of Offer Shares allocated to relevant investors listed in this subsection only represents the
number of Offer Shares allocated to the investors as Cornerstone Investors in the International Offering.
For allocations of Offer Shares to the relevant investors as placees (if any), see “Allotment Results
Details — International Offering — Allottees with Waivers/Consents Obtained” in this announcement.
(3)
In addition to the Offer Shares subscribed for as Cornerstone Investors, ZTE (H.K.) LIMITED, UBS
Asset Management (Singapore) Ltd. and CFIG Holdings Limited were allocated further Offer Shares
as placees in the International Offering. For details, see “Allotment Results Details — International
Offering — Allottees with Waivers/Consents Obtained” in this announcement. Only the Offer Shares
subscribed for as Cornerstone Investors are subject to lock-up as indicated in “Lock-up Undertakings —
Cornerstone Investors” in this announcement.
– 5 –

<<<PAGE 6>>>
Allottees with Waivers/Consents Obtained
Investor
Number of
Offer Shares
allocated
% of Offer
Shares
% of total
issued H Shares
after the Global
Offering
% of total
issued share
capital after the
Global Offering
Relationship
Allottees with waiver from strict compliance with Rule 10.04 of the Listing Rules and consent under paragraph 1C(2) of the
Placing Guidelines in relation to subscription for H Shares by existing minority Shareholders and/or their close associates
XN Mountain
International
Limited(1)
914,700
3.60%
0.37%
0.36%
A close associate of Nanjing
Xingna Heyuan Venture Capital
Partnership (Limited
Partnership), Nanjing
Xingnafeng Enterprise
Management Partnership
(Limited Partnership),
FOCUSTAR CAPITAL
INVESTMENT FUND L.P. and
XN Speed International Limited,
which are existing Shareholders,
and a Cornerstone Investor
Ms. Lin Naihui (林
乃慧)(2)
107,000
0.42%
0.04%
0.04%
A close associate of Shanghai
Yunzhixin Enterprise
Management Consulting
Partnership (Limited
Partnership), which is an existing
Shareholder
Guohui (HK)
Holdings Co.,
Limited(3)
26,000
0.10%
0.01%
0.01%
A close associate of Zhuhai
Yueteng Ruiwen Equity
Investment Partnership (Limited
Partnership), which is an existing
Shareholder
Allottees with consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of further H Shares
to Cornerstone Investors and close associates of existing Shareholders(4)
ZTE (H.K.)
LIMITED
225,000
0.88%
0.09%
0.09%
A Cornerstone Investor
UBS Asset
Management
(Singapore) Ltd.
269,000
1.06%
0.11%
0.11%
A Cornerstone Investor
CFIG Holdings
Limited
266,000
1.05%
0.11%
0.10%
A Cornerstone Investor
Shanghai Hua
Hong
International,
Inc.(5)(7)
269,000
1.06%
0.11%
0.11%
A close associate of Shanghai
Linke Zhixin Private Equity
Investment Fund Partnership
(Limited Partnership), Princeville
Global Processing IC
Investments (Hong Kong)
Limited, Shanghai Dalinghao
Bay Ceyuan No.2 Venture
Capital Partnership (Limited
Partnership) and Shanghai
Shengyong State-owned
Enterprise Reform New Potential
Private Equity Investment Fund
Partnership (Limited
Partnership), which are existing
Shareholders
– 6 –

<<<PAGE 7>>>
Investor
Number of
Offer Shares
allocated
% of Offer
Shares
% of total
issued H Shares
after the Global
Offering
% of total
issued share
capital after the
Global Offering
Relationship
Lingang Wings
Inc(6)(7)
107,000
0.42%
0.04%
0.04%
A close associate of Shanghai
Linke Zhixin Private Equity
Investment Fund Partnership
(Limited Partnership), Princeville
Global Processing IC
Investments (Hong Kong)
Limited, Shanghai Dalinghao
Bay Ceyuan No. 2 Venture
Capital Partnership (Limited
Partnership) and Shanghai
Shengyong State-owned
Enterprise Reform New Potential
Private Equity Investment Fund
Partnership (Limited
Partnership), which are existing
Shareholders
Allottees with consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the Guide for New Listing
Applicants in relation to allocations to connected clients(8)
Huatai Capital
Investment Limited
(in connection with
OTC swaps for
Jiujiu Hengxin
(Xiamen) Private
Fund Management
Co., Ltd.)(9)
1,129,900
4.44%
0.46%
0.44%
Connected client as a
Cornerstone Investor
Huatai Capital
Investment Limited
(for onshore
investors)
149,600
0.59%
0.06%
0.06%
Connected client as a placee
Bosera Asset
Management Co.,
Limited
53,000
0.21%
0.02%
0.02%
Connected client as a placee
Fullgoal Fund
Management Co.,
Ltd.
34,500
0.14%
0.01%
0.01%
Connected client as a placee
Fullgoal Asset
Management (HK)
Limited
18,500
0.07%
0.01%
0.01%
Connected client as a placee
Guotai Junan
Financial Products
Limited
764,000
3.00%
0.31%
0.30%
Connected client as a placee
– 7 –

<<<PAGE 8>>>
Notes:
(1)
XN Mountain International Limited is wholly owned by Focustar Capital. Focustar Capital manages
certain of the existing minority Shareholders, namely Nanjing Xingna Heyuan Venture Capital
Partnership (Limited Partnership) (南京星納赫源創業投資合夥企業（有限合夥）), Nanjing Xingnafeng
Enterprise Management Partnership (Limited Partnership) (南京星納峰企業管理合夥企業（有限合
夥）), FOCUSTAR CAPITAL INVESTMENT FUND L.P. and XN Speed International Limited
(collectively, “Focustar Entities”). XN Mountain International Limited is therefore a close associate of
Focustar Entities.
(2)
Shanghai Yunzhixin Enterprise Management Consulting Partnership (Limited Partnership) (上海沄知
芯企業管理諮詢合夥企業（有限合夥）) (“Shanghai Yunzhixin”) is an existing Shareholder of the
Company. The general partner of Shanghai Yunzhixin is Shanghai Yundi Private Equity Fund
Management Co., Ltd. (上海沄砥私募基金管理有限公司), which is held as to 99% by Ms. Lin Naihui
(林乃慧). Ms. Lin Naihui is therefore a close associate of Shanghai Yunzhixin.
(3)
Guohui (HK) Holdings Co., Limited is wholly owned by Shandong Development & Investment Holding
Group Co., Ltd. (山東發展投資控股集團有限公司), which is 97.88% owned by State-owned Assets
Supervision and Administration Commission of Shandong (山東省人民政府國有資產監督管理委員會).
The limited partner of Zhuhai Yueteng Ruiwen Equity Investment Partnership (Limited Partnership)
(珠海悅騰睿文股權投資合夥企業（有限合夥）)
(“Zhuhai
Yueteng”)
is
Qingdao
Yaoye
Medical
Technology Co., Ltd. (青島耀曄醫療科技有限公司) (“Qingdao Yaoye”), holding its 99.9% interest.
Qingdao Yaoye is ultimately wholly owned by Qingdao Licang District Government Investment Project
Performance Evaluation and State-owned Enterprise Service Center (青島市李滄區政府投資項目績效
評價和國有企業服務中心). Guohui (HK) Holdings Co., Limited is therefore a close associate of Zhuhai
Yueteng.
(4)
The number of Offer Shares allocated to the relevant investors listed in this subsection only represents
the number of Offer Shares allocated to the investors as placees in the International Offering. For
allocations of Offer Shares to the relevant investors as Cornerstone Investors, see “Allotment Results
Details — International Offering — Cornerstone Investors” in this announcement. For details of the
consent under Chapter 4.15 of the Guide for New Listing Applicants in relation to allocations of further
H Shares to the Cornerstone Investors, see “Others/Additional Information — Placing to Cornerstone
Investors and/or Their Close Associates with a Consent Under Chapter 4.15 of the Guide for New Listing
Applicants” in this announcement.
(5)
Shanghai Hua Hong International, Inc. is wholly owned by Shanghai Hua Hong (Group) Co., Ltd. (上
海華虹（集團）有限公司). The State-owned Assets Supervision and Administration Commission of
Shanghai (上海市國有資產監督管理委員會) (“Shanghai SASAC”) directly holds a 51.74% interest in
Shanghai Hua Hong (Group) Co., Ltd. and is its actual controller.
(6)
Lingang Wings Inc is wholly owned by Shanghai Lingang Overseas Development Co., Ltd. which is in
turn wholly owned by Shanghai Lingang Economic Development (Group) Co., Ltd (上海臨港經濟發展
集團有限公司), an entity ultimately controlled by Shanghai SASAC.
(7)
Shanghai Linke Zhixin Private Equity Investment Fund Partnership (Limited Partnership) (上海臨科
智芯私募投資基金合夥企業（有限合夥）) (“Linke Zhixin”) is a limited partnership established under
the partnership laws of the PRC. The general partner of Linke Zhixin is Shanghai Lingang Kechuang
Investment Management Co., Ltd. (上海臨港科創投資管理有限公司), which in turn is owned as to 30%
by Shanghai Linchuang Investment Management Co., Ltd. (上海臨創投資管理有限公司), which is
controlled by Shanghai SASAC. The limited partners of Linke Zhixin are majority controlled by
Shanghai SASAC or the State-owned Assets Supervision and Administration Commission of Minhang
District of Shanghai (上海市閔行區國有資產監督管理委員會) (“Minhang SASAC”).
Princeville Global Processing IC Investments (Hong Kong) Limited (“PVG”) is wholly owned by
Princeville Global Processing IC Investments Limited, which in turn is majority owned by Shanghai
Electric Hongkong Co. Limited (上海電氣香港有限公司) (“Shanghai Electric HK”). Shanghai
Electric HK is a wholly-owned subsidiary of Shanghai Electric Group Company Limited (上海電氣集
團股份有限公司), a company listed on the Stock Exchange (stock code: 2727) and the Shanghai Stock
Exchange (stock code: 601727), and which is ultimately controlled by Shanghai SASAC.
The general partner of Shanghai Dalinghao Bay Ceyuan No. 2 Venture Capital Partnership (Limited
Partnership)
(上海大零號灣策源二號創業投資合夥企業（有限合夥）)
(“Shanghai
Dalinghao
Bay
Ceyuan”) is Shanghai Dalinghao Bay Private Equity Fund Management Co., Ltd. (上海大零號灣私
募基金管理有限公司), which is ultimately wholly owned by Minhang SASAC.
– 8 –

<<<PAGE 9>>>
The manager and executive partner of Shanghai Shengyong State-owned Enterprise Reform New
Potential Private Equity Investment Fund Partnership (Limited Partnership) (上海盛雍國企改革新勢
能私募投資基金合夥企業（有限合夥）) (“Shanghai Shengyong”, together with Linke Zhixin, PVG and
Shanghai Dalinghao Bay Ceyuan, the “Shanghai Entities”) is Shanghai Guosheng Capital Management
Co., Ltd. (上海國盛資本管理有限公司) (“Shanghai Guosheng Capital”), which is owned as to 30% by
Shanghai Guosheng (Group) Co., Ltd. (上海國盛（集團）有限公司), which is in turn wholly owned by
Shanghai SASAC.
For illustration purposes only, the aggregate number of H Shares held by the Shanghai Entities upon
completion of the Global Offering amounts to 11,874,964, representing approximately 4.67% of the total
issued Shares of the Company.
Each of Shanghai Hua Hong International, Inc. and Lingang Wings Inc is therefore a close associate of
the Shanghai Entities.
(8)
For details of the consent under paragraph 1C(1) of the Placing Guidelines and Chapter 4.15 of the
Guide for New Listing Applicants in relation to allocations to connected clients, see “Others/Additional
Information — Placing to Connected Clients with a Consent Under Paragraph 1C(1) of the Placing
Guidelines” in this announcement.
(9)
For further details of the allocation of Offer Shares to Huatai Capital Investment Limited as a
Cornerstone Investor, see “Waivers — Consent Under Paragraph 1C(1) of the Placing Guidelines to be
Granted for Allocation of Securities to HTCI” and “Cornerstone Investors” in the Prospectus.
– 9 –

<<<PAGE 10>>>
LOCK-UP UNDERTAKINGS
Existing Shareholders and Pre-IPO Investors
Name
Number of
Shares held in
the Company
subject to lock-up
undertakings
upon listing
Number of H
Shares held in
the Company
subject to lock-up
undertakings
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
subject to lock-up
undertakings
upon Listing
Last day subject
to the lock-up
undertakings(1)
Shanghai Xishi Enterprise
Management Consulting
Partnership (Limited
Partnership)
13,718,171
13,718,171
5.60%
5.39%
January 7, 2027
Shanghai Yishi Enterprise
Management Consulting
Partnership (Limited
Partnership)
12,340,003
12,340,003
5.03%
4.85%
January 7, 2027
Shanghai Sushi Business
Consulting Partnership
(Limited Partnership)
7,118,886
7,118,886
2.90%
2.80%
January 7, 2027
Shanghai Qiongyu Business
Consulting Partnership
(Limited Partnership)
8,900,000
8,900,000
3.63%
3.50%
January 7, 2027
Shanghai Nashi Business
Consulting Partnership
(Limited Partnership)
3,615,000
3,615,000
1.47%
1.42%
January 7, 2027
Shanghai Yuanshi Enterprise
Management Consulting
Partnership (Limited
Partnership)
5,515,250
5,515,250
2.25%
2.17%
January 7, 2027
Shanghai Yueshi Enterprise
Management Consulting
Partnership (Limited
Partnership)
2,826,815
2,826,815
1.15%
1.11%
January 7, 2027
Nanjing Youxu Equity
Investment Partnership
(Limited Partnership)
16,503,313
16,503,313
6.73%
6.49%
January 7, 2027
Fujian Centurium Phase I
Investment Partnership
(Limited Partnership)
18,269,383
18,269,383
7.45%
7.18%
January 7, 2027
Masterwork Holdings Limited
11,726,485
11,726,485
4.78%
4.61%
January 7, 2027
Xiamen Zhengmei Enterprise
Management Partnership
(Limited Partnership)
5,953,762
5,953,762
2.43%
2.34%
January 7, 2027
Rizhao Tianxin Information
Technology Partnership
(Limited Partnership)
9,143,732
9,143,732
3.73%
3.60%
January 7, 2027
Rizhao Peiqin Information
Technology Partnership
(Limited Partnership)
8,050,359
8,050,359
3.28%
3.17%
January 7, 2027
– 10 –

<<<PAGE 11>>>
Name
Number of
Shares held in
the Company
subject to lock-up
undertakings
upon listing
Number of H
Shares held in
the Company
subject to lock-up
undertakings
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
subject to lock-up
undertakings
upon Listing
Last day subject
to the lock-up
undertakings(1)
Tianjin Haihe Yunbai
Industrial Investment Fund
Partnership (Limited
Partnership)
5,255,030
5,255,030
2.14%
2.07%
January 7, 2027
Wuhu Kuangyun Artificial
Intelligence Industry
Investment Fund (Limited
Partnership)
1,709,272
1,709,272
0.70%
0.67%
January 7, 2027
Shenzhen Digital Future
Private Equity Investment
Fund Partnership (Limited
Partnership)
1,628,679
1,628,679
0.66%
0.64%
January 7, 2027
Nanjing Xingna Heyuan
Venture Capital Partnership
(Limited Partnership)
2,931,621
2,931,621
1.20%
1.15%
January 7, 2027
Nanjing Xingnafeng Enterprise
Management Partnership
(Limited Partnership)
415,313
415,313
0.17%
0.16%
January 7, 2027
FOCUSTAR CAPITAL
INVESTMENT FUND L.P.
2,346,698
2,346,698
0.96%
0.92%
January 7, 2027
XN Speed International
Limited
1,771,757
1,771,757
0.72%
0.70%
January 7, 2027
Jupiter Technology Link
Investment Company Ltd
7,166,801
7,166,801
2.92%
2.82%
January 7, 2027
Yuyao Bijiang Shengxing
Management Consulting
Partnership (Limited
Partnership)
6,775,509
6,775,509
2.76%
2.66%
January 7, 2027
Beijing Zhongguancun Science
City Technology Growth
Investment Partnership
(Limited Partnership)
5,946,308
5,946,308
2.43%
2.34%
January 7, 2027
Shanghai Huiyue Business
Consulting Partnership
(Limited Partnership)
5,425,000
5,425,000
2.21%
2.13%
January 7, 2027
Beijing Ruifeng Equity
Investment Fund (Limited
Partnership)
5,008,306
2,504,153
1.02%
0.98%
January 7, 2027
Xicheng Zhiyuan Digital Power
Selection (Beijing) Investment
Center (Limited Partnership)
297,250
297,250
0.12%
0.12%
January 7, 2027
Shanghai Linke Zhixin Private
Equity Investment Fund
Partnership (Limited
Partnership)
5,139,423
3,083,654
1.26%
1.21%
January 7, 2027
– 11 –

<<<PAGE 12>>>
Name
Number of
Shares held in
the Company
subject to lock-up
undertakings
upon listing
Number of H
Shares held in
the Company
subject to lock-up
undertakings
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
subject to lock-up
undertakings
upon Listing
Last day subject
to the lock-up
undertakings(1)
Princeville Global Processing
IC Investments (Hong Kong)
Limited
5,073,488
5,073,488
2.07%
1.99%
January 7, 2027
Shenzhen Dongsheng Asset
Management Partnership
(Limited Partnership)
3,830,000
3,830,000
1.56%
1.51%
January 7, 2027
Zhuhai Yueteng Ruiwen Equity
Investment Partnership
(Limited Partnership)
3,418,543
—
—
—
January 7, 2027
Quzhou Intelligent
Manufacturing Anhe Equity
Investment Partnership
(Limited Partnership)
3,257,357
3,257,357
1.33%
1.28%
January 7, 2027
Shanghai Yunzhixin Enterprise
Management Consulting
Partnership (Limited
Partnership)
3,076,689
3,076,689
1.26%
1.21%
January 7, 2027
Xiamen Yaheng Venture
Capital Fund Partnership
(Limited Partnership)
2,938,548
2,938,548
1.20%
1.16%
January 7, 2027
Shanghai Shengyong
State-owned Enterprise Reform
New Potential Private Equity
Investment Fund Partnership
(Limited Partnership)
2,903,483
2,903,483
1.18%
1.14%
January 7, 2027
Ningbo Dingzhixin Equity
Investment Partnership
(Limited Partnership)
1,081,714
1,081,714
0.44%
0.43%
January 7, 2027
Ningbo Dingyinxin Equity
Investment Partnership
(Limited Partnership)
915,714
915,714
0.37%
0.36%
January 7, 2027
Ningbo Dingmaoxin Equity
Investment Partnership
(Limited Partnership)
685,256
685,256
0.28%
0.27%
January 7, 2027
Jiangsu Jiequan New
Engineering Bangsheng Venture
Capital Fund Partnership
(Limited Partnership)
1,299,000
1,299,000
0.53%
0.51%
January 7, 2027
Suzhou Bangsheng Yingxin
Venture Capital Enterprise
(Limited Partnership)
860,000
860,000
0.35%
0.34%
January 7, 2027
Suzhou Industrial Park Yuanhe
Dingsheng Equity Investment
Partnership (Limited
Partnership)
1,113,542
1,113,542
0.45%
0.44%
January 7, 2027
– 12 –

<<<PAGE 13>>>
Name
Number of
Shares held in
the Company
subject to lock-up
undertakings
upon listing
Number of H
Shares held in
the Company
subject to lock-up
undertakings
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
subject to lock-up
undertakings
upon Listing
Last day subject
to the lock-up
undertakings(1)
Chengdu Tianfu Yuanhe Jingu
Venture Capital Center
(Limited Partnership)
599,599
599,599
0.24%
0.24%
January 7, 2027
Hangzhou Yuanqiao Zhishu
Equity Investment Partnership
(Limited Partnership)
1,713,141
1,713,141
0.70%
0.67%
January 7, 2027
Hunan Xiangjiang New District
Guiding No. 5 Equity
Investment Partnership
(Limited Partnership)
1,627,484
1,627,484
0.66%
0.64%
January 7, 2027
Sichuan Regional Collaborative
Development Investment
Guidance Fund Partnership
(Limited Partnership)
488,604
—
—
—
January 7, 2027
Mianyang Gaochuang Equity
Investment Fund Partnership
(Limited Partnership)
732,905
—
—
—
January 7, 2027
Hainan Kunjun Investment
Partnership (Limited
Partnership)
1,191,716
1,191,716
0.49%
0.47%
January 7, 2027
Sichuan Dingxiang Equity
Investment Fund Co., Ltd.
1,116,724
1,116,724
0.46%
0.44%
January 7, 2027
Wuhan Jiangxia Xintuo Equity
Investment Fund Management
Partnership (Limited
Partnership)
446,690
446,690
0.18%
0.18%
January 7, 2027
Zaozhuang Xinsheng Equity
Investment Partnership
(Limited Partnership)
670,034
670,034
0.27%
0.26%
January 7, 2027
Nanjing Lianchuang Digital
Equity Investment Partnership
(Limited Partnership)
1,027,884
1,027,884
0.42%
0.40%
January 7, 2027
Guangzhou Tianmu Artificial
Intelligence Industry
Investment Fund Partnership
(Limited Partnership)
974,169
974,169
0.40%
0.38%
January 7, 2027
Shanghai Kuanqing
Management Consulting
Partnership (Limited
Partnership)
963,415
947,618
0.39%
0.37%
January 7, 2027
Yancheng Yingwan Kexin
Linghang Equity Investment
Partnership (Limited
Partnership)
947,556
947,556
0.39%
0.37%
January 7, 2027
– 13 –

<<<PAGE 14>>>
Name
Number of
Shares held in
the Company
subject to lock-up
undertakings
upon listing
Number of H
Shares held in
the Company
subject to lock-up
undertakings
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
subject to lock-up
undertakings
upon Listing
Last day subject
to the lock-up
undertakings(1)
Gongqingcheng Baochuang
Gongying Venture Capital
Fund Partnership (Limited
Partnership)
856,570
856,570
0.35%
0.34%
January 7, 2027
Hubei Lihe Jiacheng
Investment Co., Ltd.
814,339
814,339
0.33%
0.32%
January 7, 2027
Hainan Zhihua Investment
Partnership (Limited
Partnership)
814,339
814,339
0.33%
0.32%
January 7, 2027
Shanghai Dalinghao Bay
Ceyuan No.2 Venture Capital
Partnership (Limited
Partnership)
814,339
814,339
0.33%
0.32%
January 7, 2027
Xi’an Xigaotou Zhiyuan
Investment Fund Partnership
(Limited Partnership)
814,339
814,339
0.33%
0.32%
January 7, 2027
Nanjing Lanpu High Quality
Equity Investment Fund
(Limited Partnership)
781,766
781,766
0.32%
0.31%
January 7, 2027
Cuihu Tianshu (Zibo) Equity
Investment Partnership
(Limited Partnership)
745,216
745,216
0.30%
0.29%
January 7, 2027
Nanjing Railway Investment
Jushi Hub Economic Industry
Investment Fund Partnership
(Limited Partnership)
651,471
651,471
0.27%
0.26%
January 7, 2027
Hina Growth Opportunities
Fund, L.P.
611,052
611,052
0.25%
0.24%
January 7, 2027
Zhejiang Biyi Electric
Appliance Co., Ltd.
575,126
575,126
0.23%
0.23%
January 7, 2027
Beijing Paradigm Artificial
Intelligence Equity Investment
Fund (Limited Partnership)
513,942
513,942
0.21%
0.20%
January 7, 2027
Interplanetary Pte. Ltd.
492,807
492,807
0.20%
0.19%
January 7, 2027
China Insurance Investment
Trust Quality (Jiaxing) Equity
Investment Partnership
(Limited Partnership)
488,604
488,604
0.20%
0.19%
January 7, 2027
Ningbo Ruihe Yingfu Venture
Capital Partnership (Limited
Partnership)
244,302
244,302
0.10%
0.10%
January 7, 2027
Ningbo Yingshi Venture
Capital Partnership (Limited
Partnership)
244,302
244,302
0.10%
0.10%
January 7, 2027
– 14 –

<<<PAGE 15>>>
Name
Number of
Shares held in
the Company
subject to lock-up
undertakings
upon listing
Number of H
Shares held in
the Company
subject to lock-up
undertakings
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
subject to lock-up
undertakings
upon Listing
Last day subject
to the lock-up
undertakings(1)
Sichuan Culture Industry
Investment Fund Partnership
(Limited Partnership)
407,170
407,170
0.17%
0.16%
January 7, 2027
Hunan Bofu Selected Equity
Investment Partnership
(Limited Partnership)
394,140
394,140
0.16%
0.15%
January 7, 2027
Suqian Lingrui Business
Consulting Service Partnership
Enterprise (Limited
Partnership)
170,731
170,731
0.07%
0.07%
January 7, 2027
Total
228,885,936
219,670,165
89.62%
90.00%
Note:
(1)
The expiry date of the lock-up period shown in the table above is pursuant to the PRC Company Laws.
– 15 –

<<<PAGE 16>>>
Cornerstone Investors
Name
Number of
Shares held in
the Company
subject to lock-up
undertakings
upon Listing
Number of H
Shares held in
the Company
subject to lock-up
undertakings
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
subject to lock-up
undertakings
upon Listing
Last day subject
to the lock-up
undertakings
(1)
ZTE (H.K.) LIMITED
151,000
151,000
0.06%
0.06%
July 7, 2026
XN Mountain International
Limited
914,700
914,700
0.37%
0.36%
July 7, 2026
Wind Sabre Fund SPC acting
on behalf and for the account
of Wind Sabre Opportunities
Fund SP
1,076,100
1,076,100
0.44%
0.42%
July 7, 2026
UBS Asset Management
(Singapore) Ltd.
538,000
538,000
0.22%
0.21%
July 7, 2026
Teamsun Technology (HK)
Limited
228,200
228,200
0.09%
0.09%
July 7, 2026
Qin Wan Investment Limited
762,600
762,600
0.31%
0.30%
July 7, 2026
OCM Limited
532,700
532,700
0.22%
0.21%
July 7, 2026
Ocean Fine Industrial Limited
537,100
537,100
0.22%
0.21%
July 7, 2026
Huatai Capital Investment
Limited (in connection with
OTC swaps for Jiujiu Hengxin
(Xiamen) Private Fund
Management Co., Ltd.)
1,129,900
1,129,900
0.46%
0.44%
July 7, 2026
Fourth Paradigm International
Limited
691,500
691,500
0.28%
0.27%
July 7, 2026
Engine International
Technology Co., Limited
228,800
228,800
0.09%
0.09%
July 7, 2026
Duckling Fund, L.P.
1,076,100
1,076,100
0.44%
0.42%
July 7, 2026
DeepRoot Alpha Ltd
215,200
215,200
0.09%
0.08%
July 7, 2026
China Universal Asset
Management (Hong Kong)
Company Limited
1,076,100
1,076,100
0.44%
0.42%
July 7, 2026
China Orient International
Asset Management Limited —
China Orient Enhanced Income
Fund
376,600
376,600
0.15%
0.15%
July 7, 2026
China Orient International
Asset Management Limited —
China Orient Multi-Strategy
Master Fund
161,400
161,400
0.07%
0.06%
July 7, 2026
China Asset Management
(Hong Kong) Limited
322,800
322,800
0.13%
0.13%
July 7, 2026
CFIG Holdings Limited
114,400
114,400
0.05%
0.04%
July 7, 2026
Alphahill Capital Limited
807,100
807,100
0.33%
0.32%
July 7, 2026
Total
10,940,300
10,940,300
4.46%
4.30%
– 16 –

<<<PAGE 17>>>
Note:
(1)
In accordance with the relevant cornerstone investment agreements, the required lock-up ends on July 7,
2026, being six months following the Listing Date. The Cornerstone Investors will cease to be prohibited
from disposing of or transferring H Shares subscribed for pursuant to the relevant cornerstone
investment agreements after the indicated date.
– 17 –

<<<PAGE 18>>>
PLACEE CONCENTRATION ANALYSIS
Placees
Number of
H Shares
allotted
Allotment as %
of International
Offering
Allotment as %
of total Offer
Shares
Number of
Shares held
upon Listing
% of total issued
share capital
upon Listing
Top 1
1,302,000
5.69%
5.12%
1,302,000
0.51%
Top 5
5,873,700
25.66%
23.10%
21,237,670
8.35%
Top 10
10,298,600
44.99%
40.49%
33,127,959
13.03%
Top 25
18,254,900
79.76%
71.78%
41,084,259
16.15%
Note
*
Ranking of placees is based on the number of H Shares allotted to the placees.
H SHAREHOLDERS CONCENTRATION ANALYSIS
H Shareholders*
Number of
H Shares
allotted
Allotment as
% of
International
Offering
Allotment as
% of total
Offer Shares
Number of
H Shares held
upon Listing
% of total
issued
H Shares
capital upon
Listing
Number of
Shares held
upon Listing
Top 1
0
0.00%
0.00%
54,034,125
22.05%
54,034,125
Top 5
1,140,000
4.98%
4.48%
145,289,104
59.28%
147,344,873
Top 10
2,054,700
8.98%
8.08%
179,728,027
73.33%
181,783,796
Top 25
4,743,200
20.72%
18.65%
213,957,119
87.29%
218,517,041
Note
*
Ranking of H Shareholders is based on the number of H Shares held by the H Shareholders upon Listing.
– 18 –

<<<PAGE 19>>>
SHAREHOLDER CONCENTRATION ANALYSIS
Shareholders
Number of
H Shares
allotted
Allotment as
% of
International
Offering
Allotment as
% of total
Offer Shares
Number of
H Shares held
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
54,034,125
54,034,125
21.25%
Top 5
1,140,000
4.98%
4.48%
145,289,104
147,344,873
57.94%
Top 10
2,054,700
8.98%
8.08%
179,728,027
181,783,796
71.48%
Top 25
4,769,200
20.84%
18.75%
212,156,841
221,356,815
87.04%
Note
*
Ranking of Shareholders is based on the number of Shares (of all classes) held by the Shareholder upon
Listing.
– 19 –

<<<PAGE 20>>>
BASIS OF ALLOCATION UNDER THE HONG KONG PUBLIC OFFERING
Subject to the satisfaction of the conditions set out in the Prospectus, a total of 180,802
valid applications made by the public will be conditionally allocated on the basis set out
below:
NO. OF SHARES
APPLIED FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED OF
THE TOTAL
NO. OF SHARES
APPLIED FOR
POOL A
100
102,763
7,193 out of 102,763 to receive 100 Shares
7.00%
200
7,517
588 out of 7,517 to receive 100 Shares
3.91%
300
16,673
1,307 out of 16,673 to receive 100 Shares
2.61%
400
2,094
165 out of 2,094 to receive 100 Shares
1.97%
500
2,250
178 out of 2,250 to receive 100 Shares
1.58%
600
2,759
219 out of 2,759 to receive 100 Shares
1.32%
700
1,575
126 out of 1,575 to receive 100 Shares
1.14%
800
823
66 out of 823 to receive 100 Shares
1.00%
900
511
41 out of 511 to receive 100 Shares
0.89%
1,000
7,184
577 out of 7,184 to receive 100 Shares
0.80%
1,500
2,383
192 out of 2,383 to receive 100 Shares
0.54%
2,000
2,557
207 out of 2,557 to receive 100 Shares
0.40%
2,500
1,460
119 out of 1,460 to receive 100 Shares
0.33%
3,000
1,789
146 out of 1,789 to receive 100 Shares
0.27%
3,500
993
82 out of 993 to receive 100 Shares
0.24%
4,000
1,116
93 out of 1,116 to receive 100 Shares
0.21%
4,500
739
62 out of 739 to receive 100 Shares
0.19%
5,000
1,805
152 out of 1,805 to receive 100 Shares
0.17%
6,000
1,323
112 out of 1,323 to receive 100 Shares
0.14%
7,000
1,378
117 out of 1,378 to receive 100 Shares
0.12%
8,000
1,112
95 out of 1,112 to receive 100 Shares
0.11%
9,000
831
71 out of 831 to receive 100 Shares
0.09%
10,000
4,595
393 out of 4,595 to receive 100 Shares
0.09%
20,000
2,742
235 out of 2,742 to receive 100 Shares
0.04%
30,000
2,095
180 out of 2,095 to receive 100 Shares
0.03%
171,067
Total number of Pool A successful applicants: 12,716
– 20 –

<<<PAGE 21>>>
NO. OF SHARES
APPLIED FOR
NO. OF VALID
APPLICATIONS
BASIS OF ALLOTMENT/BALLOT
APPROXIMATE
PERCENTAGE
ALLOTTED OF
THE TOTAL
NO. OF SHARES
APPLIED FOR
POOL B
40,000
5,722
100 Shares plus 1,717 out of 5,722 to receive
additional 100 Shares
0.33%
50,000
924
100 Shares plus 278 out of 924 to receive additional
100 Shares
0.26%
60,000
555
100 Shares plus 168 out of 555 to receive additional
100 Shares
0.22%
70,000
477
100 Shares plus 145 out of 477 to receive additional
100 Shares
0.19%
80,000
357
100 Shares plus 109 out of 357 to receive additional
100 Shares
0.16%
90,000
214
100 Shares plus 66 out of 214 to receive additional
100 Shares
0.15%
100,000
764
100 Shares plus 236 out of 764 to receive additional
100 Shares
0.13%
200,000
327
100 Shares plus 102 out of 327 to receive additional
100 Shares
0.07%
300,000
116
100 Shares plus 37 out of 116 to receive additional
100 Shares
0.04%
400,000
61
100 Shares plus 20 out of 61 to receive additional 100
Shares
0.03%
500,000
38
100 Shares plus 13 out of 38 to receive additional 100
Shares
0.03%
600,000
32
100 Shares plus 11 out of 32 to receive additional 100
Shares
0.02%
700,000
27
100 Shares plus 10 out of 27 to receive additional 100
Shares
0.02%
800,000
14
100 Shares plus 6 out of 14 to receive additional 100
Shares
0.02%
900,000
11
100 Shares plus 5 out of 11 to receive additional 100
Shares
0.02%
1,000,000
7
100 Shares plus 4 out of 7 to receive additional 100
Shares
0.02%
1,100,000
5
100 Shares plus 3 out of 5 to receive additional 100
Shares
0.01%
1,271,600
84
100 Shares plus 51 out of 84 to receive additional 100
Shares
0.01%
9,735
Total number of Pool B successful applicants: 9,735
– 21 –

<<<PAGE 22>>>
As of the date of this announcement, the relevant subscription monies previously deposited
in the designated nominee accounts have been remitted back to the accounts of all HKSCC
participants. Investors should contact their relevant brokers for any inquiries.
COMPLIANCE WITH LISTING RULES AND GUIDANCE
The Directors confirm that, except for the Listing Rules that have been waived and/or in
respect of which consent has been obtained, the Company has complied with the Listing
Rules and guidance materials in relation to the placing, allotment and listing of the
Company’s H Shares.
The Directors confirm that, to the best of their knowledge, no rebate has been, directly or
indirectly, provided by the Company, its Directors or syndicate members to any placees
or the public (as the case may be) and the consideration payable by them for each Offer
Share of the Company subscribed for or purchased by them is the same as the final Offer
Price
determined
by
agreement
between
the
Company
and
the
Sponsor-Overall
Coordinator (for itself and on behalf of other Underwriters), in addition to any
brokerage, AFRC transaction levy, SFC transaction levy and trading fee payable.
OTHERS/ADDITIONAL INFORMATION
Placing to Close Associates of Existing Minority Shareholders with a Waiver Under Rule
10.04 and Consent Under Paragraph 1C(2) of the Placing Guidelines
The Company has applied to the Stock Exchange for, and the Stock Exchange has
granted to the Company, a waiver from strict compliance with the requirements under
Rule 10.04 and the consent under paragraph 1C(2) of the Placing Guidelines, to permit
the existing shareholders and/or its close associates to participate as either cornerstone
investors or placees in the Global Offering to subscribe for the Offer Shares to be issued
by the Company under the International Offering (together, the “Existing Minority
Shareholder Participants”). The Stock Exchange has agreed to grant the requested waiver
and consent subject to the conditions that:
(a) each of the Existing Minority Shareholder Participants, (1) together with their close
associates, holds less than 5% voting rights in the Company prior to the completion
of the Global Offering. (2) is not and will not become (upon the completion of the
Global Offering) a core connected person of the Company or the close associate of
any such core connected person; and (3) does not have the right to appoint a
Director and/or have any other special rights;
(b) the allocation to the Existing Minority Shareholder Participants will not affect the
Company’s ability to satisfy its public float requirement under Rule 19A.13A of the
Listing Rules;
(c)
each of the Company, the Sole Sponsor and the Overall Coordinators confirms that
no preferential treatment has been, nor will be directly or indirectly, given to the
Existing Minority Shareholder Participants as cornerstone investors or placees by
virtue of their relationship with the Company in any allocation in the Global
Offering, other than the preferential treatment of assured entitlement under the
cornerstone investment at the Offer Price and the terms are substantially the same as
other cornerstone investors; and
– 22 –

<<<PAGE 23>>>
(d) details of the allocation of the Offer Shares to the Existing Minority Shareholder
Participants as cornerstone investors or placees under the Global Offering have been
disclosed in the Prospectus or in this announcement.
For details of the allocations of Offer Shares to such Existing Minority Shareholder
Participants, see “Allotment Results Details — International Offering — Allottees with
Waivers/Consents Obtained” in this announcement, and “Waivers — Allocation of H
Shares
to
a
Close
Associate
of
Certain
Existing
Minority
Shareholders”
and
“Cornerstone Investors” in the Prospectus..
Placing to Cornerstone Investors and Close Associates of the Existing Shareholders with a
Consent Under Chapter 4.15 of the Guide for New Listing Applicants
The Company has applied to, and the Stock Exchange has granted, a consent under
Chapter 4.15 of the Guide for New Listing Applicants to permit the Company to allocate
further Offer Shares in the International Offering to certain Cornerstone Investors
and/or close associates of existing Shareholders as placees, subject to the following
conditions (“Allocation to Size-based Exemption Participants”):
(a) the final offering size of the Global Offering will be of a total value of at least HK$1
billion;
(b) the Offer Shares allocated to all existing Shareholders and their close associates
(whether as cornerstone investors and/or as placees) as permitted under the
Size-based Exemption (as defined in the Guide for New Listing Applicants) do not
exceed 30% of the total number of the H Shares offered under the Global Offering;
(c)
the Allocation to Size-based Exemption Participants will not affect the Company’s
ability to satisfy its public float requirement under Rule 19A.13A of the Listing
Rules;
(d) each Director and chief executive of the Company confirms that no securities have
been allocated to them or their respective close associates under the Size-based
Exemption; and
(e)
details of the allocation to Cornerstone Investors and close associates of the existing
Shareholders
under
the
Size-based
Exemption
have
been
disclosed
in
this
announcement.
Such allocations of Offer Shares are in compliance with all the conditions under the
consent granted by the Stock Exchange.
For details of further allocations of Offer Shares to Cornerstone Investors and close
associates of existing Shareholders, see “Allotment Results Details — International
Offering — Allottees with Waivers/Consents Obtained” in this announcement.
Placing to Connected Clients with a Consent Under Paragraph 1C(1) of the Placing
Guidelines
Under the International Offering, certain Offer Shares were placed to connected clients
of their connected distributors pursuant to the Placing Guidelines.
– 23 –

<<<PAGE 24>>>
The Company has applied to the Stock Exchange for, and the Stock Exchange has
granted, a consent under paragraph 1C(1) of the Placing Guidelines to permit the
Company to allocate such Offer Shares in the International Offering to the connected
clients. The allocation of Offer Shares to such connected clients is in compliance with all
the conditions under the consent granted by the Stock Exchange.
Details of the placement to connected clients are set out below:
No.
Connected Client
(7)
Connected Distributor
Relationship between the
Connected Client and the
Connected Distributor
Information
of the
Connected
Client
Whether the
Connected Client will
hold the beneficial
interest of the Offer
Shares on a
non-discretionary
basis or discretionary
basis for independent
third parties
Number of
Offer Shares to
be allocated
% of total
issued H Shares
after the Global
Offering
% of the total
issued Shares
after the Global
Offering
1.
Huatai Capital Investment
Limited (“HTCI”) (in
connection with OTC
swaps for Jiujiu Hengxin
(Xiamen) Private Fund
Management Co., Ltd.)
Huatai Financial
Holdings (Hong Kong)
Limited (“HTFH”)
HTCI is a member of the
same group of
companies as HTFH.
Note (1)
Non-discretionary
1,129,900
0.46%
0.44%
2.
HTCI (for onshore
investors)
HTFH
HTCI is a member of the
same group of
companies as HTFH.
Note (2)
Non-discretionary
149,600
0.06%
0.06%
3.
Bosera Asset Management
Co., Limited (“Bosera”)
CMB International
Capital Limited
(“CMBI”)
Bosera is a member of
the same group of
companies as CMBI.
Note (3)
Discretionary
53,000
0.02%
0.02%
4.
Fullgoal Fund Management
Co., Ltd.
Guotai Junan Securities
(Hong Kong) Limited
(“GTJA”) and Haitong
International Securities
Company Limited
(“HTI”)
Fullgoal Fund
Management Co., Ltd.
is a member of the
same group of
companies as GTJA
and HTI.
Note (4)
Discretionary
34,500
0.01%
0.01%
5.
Fullgoal Asset
Management (HK)
Limited
GTJA and HTI
Fullgoal Asset
Management (HK)
Limited is a member of
the same group of
companies as GTJA
and HTI.
Note (5)
Discretionary
18,500
0.01%
0.01%
6.
Guotai Junan Financial
Products Limited
(“GTJA FP”)
GTJA and HTI
GTJA FP is a member of
the same group of
companies as GTJA
and HTI.
Note (6)
Non-discretionary
764,000
0.31%
0.30%
Notes:
(1)
For further details of the allocation of Offer Shares to Huatai Capital Investment Limited as a
Cornerstone Investor, see “Waivers — Consent Under Paragraph 1C(1) of the Placing Guidelines to
be Granted for Allocation of Securities to HTCI” and “Cornerstone Investors” in the Prospectus.
(2)
PRC investors are currently not permitted under applicable PRC laws to participate directly in initial
public offerings (“IPOs”) in Hong Kong. However, PRC investors are permitted to invest in products
issued by appropriate domestic securities firms licensed to undertake cross-border derivatives trading
activities. In connection with such products, the licensed domestic securities firms, through their
Hong Kong affiliates, may participate in Hong Kong IPOs either as placees or cornerstone investors
(the “Cross-border Derivatives Trading Regime”).
– 24 –

<<<PAGE 25>>>
Huatai Securities Co., Ltd. (“HTSC”), the A shares of which are listed on the Shanghai Stock
Exchange (stock code: 601688), the H shares of which are listed on the Stock Exchange (stock code:
6886), and the global depositary receipts of which are listed on the London Stock Exchange (LON:
HTSC), is one of the domestic securities firms licensed to undertake cross-border derivatives trading
activities. HTSC entered into an ISDA agreement (the “ISDA Agreement”) with its indirectly
wholly-owned subsidiary, HTCI, to set out the principal terms of any future total return swap
between HTSC and HTCI.
HTFH is the Sponsor-Overall Coordinator, Joint Global Coordinator and Joint Bookrunner in
connection with the Global Offering. Pursuant to the ISDA Agreement, HTCI, which intends to
participate in the International Offering as a placee, will hold the beneficial interest of the Offer
Shares on a non-discretionary basis as the single underlying holder under a back-to-back total return
swap (the “HT Back-to-back TRS”) to be entered by HTCI in connection with Huatai TRS (as
defined below) placed by and fully funded (i.e. with no financing provided by HTCI) by the Huatai
Ultimate Clients (as defined below), by which, HTCI will, subject to customary fees and commissions,
pass the full economic exposure of the Offer Shares to the Huatai Ultimate Clients, which in effect,
HTCI will hold the beneficial interest of the Offer Shares on behalf of the Huatai Ultimate Clients.
HTFH, the Sponsor-Overall Coordinator, one of the Joint Global Coordinators and Joint
Bookrunners of the Global Offering, and HTCI are indirectly wholly-owned subsidiaries of HTSC.
Accordingly, HTCI is considered as a “connected client” of Huatai pursuant to paragraph 1B(7) of
the Placing Guidelines.
Pursuant to the Cross-border Derivatives Trading Regime, the onshore investors (the “Huatai
Ultimate Clients”) cannot directly subscribe for the Offer Shares but may invest in derivative products
issued by domestic securities firms licensed to undertake cross-border derivatives trading activities,
such as HTSC, with the Offer Shares as the underlying assets. Instead of directly subscribing for the
Offer Shares, the Huatai Ultimate Clients will, through its investment manager, place a total return
swap order (the “Huatai TRS”) with HTSC in connection with the Company’s IPO and HTSC will
place a HT Back-to-back TRS order to HTCI on the terms of the ISDA Agreement. In order to hedge
its exposure under the HT Back-to-back TRS, HTCI participates in the Company’s IPO and
subscribes for the Offer Shares through placing order with HTFH during the International Offering.
Huatai Ultimate Clients includes: (i) Roadshow Xunlu No. 91 Private Equity Investment Fund (鹿秀
馴鹿91號私募證券投資基金), whose manager is Qingdao Roadshow Investment Management Co.,
Ltd. (青島鹿秀投資管理有限公司) (“Qingdao Roadshow”). The ultimate beneficial owner of Qingdao
Roadshow is Yao Bo (么博). No ultimate beneficial owner holds 30% or more interest in this fund;
(ii) Greenwoods Jingtai Global Private Equity Fund (景林景泰全球私募證券投資基金), whose
manager
is
Shanghai
Greenwoods
Asset
Management
Co.
Ltd.
(上海景林資產管理有限公司)
(“Shanghai Greenwood”). The ultimate beneficial owner of Shanghai Greenwood is Jiang Jinzhi (蔣
錦志). No ultimate beneficial owner holds 30% or more interest in this fund; (iii) Greenwoods Global
Fund (景林全球基金), whose manager is Shanghai Greenwoods. No ultimate beneficial owner holds
30% or more interest in this fund; (iv) Greenwoods Zhiyuan Private Equity Fund (景林致遠私募基
金), whose manager is Shanghai Greenwoods. No ultimate beneficial owner holds 30% or more
interest in this fund; (v) Greenwoods Jingtai Harvest Private Equity Investment Fund (景林景泰豐收
私募證券投資基金), whose manager is Shanghai Greenwoods. No ultimate beneficial owner holds
30% or more interest in this fund; (vi) Greenwoods Harvest No. 3 Private Fund (景林豐收3號私募基
金), whose manager is Shanghai Greenwoods. No ultimate beneficial owner holds 30% or more
interest in this fund; (vii) Greenwoods Harvest No. 2 Fund (景林豐收2號基金), whose manager is
Shanghai Greenwoods. No ultimate beneficial owner holds 30% or more interest in this fund; (viii)
Greenwoods Harvest No. 6 Private Equity Investment Fund (景林豐收6號私募證券投資基金), whose
manager is Shanghai Greenwoods. No ultimate beneficial owner holds 30% or more interest in this
fund; (ix) Baoyin Long/Short Steady No. 1 Private Securities Investment Fund (保銀多空穩健1號私募
證券投資基金), whose manager is Pinpoint Investment Management Limited (上海保银私募基金管理
有限公司) (“Pinpoint Investment”). The ultimate beneficial owner of Pinpoint Investment is Li Mo (李
墨). Other than Wang Qiang (王強), no ultimate beneficial owner holds 30% or more interest in this
fund; (x) Baoyin Long/Short Steady No. 2 Private Securities Investment Fund (保銀多空穩健2號私募
證券投資基金), whose manager is Pinpoint Investment. Other than Wang Qiang (王強), no ultimate
– 25 –

<<<PAGE 26>>>
beneficial owner holds 30% or more interest in this fund; and (xi) Baoyin Aggressive No. 1 Private
Securities Investment Fund (保銀進取1號私募證券投資基金), whose manager is Pinpoint Investment.
No ultimate beneficial owner holds 30% or more interest in this fund.
To the best of knowledge of HTCI and after making all reasonable enquiries, the Huatai Ultimate
Clients are independent third parties of HTCI, and the companies which are members of the same
group of HTCI.
The purpose of HTCI to subscribe for the Offer Shares is for hedging the HT Back-to-back TRS in
connection with the Huatai TRS order placed by the Huatai Ultimate Clients. Pursuant to the terms
of the contracts of the HT Back-to-back TRS and the Huatai TRS, during the tenor of the HT
Back-to-back TRS and the Huatai TRS, subject to customary fees and commissions, all economic
returns of the Offer Shares will be passed to the Huatai Ultimate Clients through the HT
Back-to-back TRS and the Huatai TRS and all economic loss shall be borne by the Huatai Ultimate
Clients. HTCI will not take any economic return or bear any economic loss in relation to the Offer
Shares, save as customary fees and commissions.
Investment in the HT Back-to-back TRS and the Huatai TRS is similar to the investment in a
qualified domestic institutional investor fund (“QDII”) in the way that the Huatai Ultimate Clients
would reap all the economic benefits of the underlying Offer Shares, except that a QDII fund would
pass through the exchange rate exposure on both the notional value of the investment and the profit
and loss of the investment. In contrast, the profit and loss of the HT Back-to-back TRS and the
Huatai TRS factor into account the fluctuation in RMB exchange rate upon termination of the
Huatai TRS by converting the profit and loss using the current exchange rate at the time of
termination. As such, the Huatai Ultimate Clients would bear the exchange rate exposure of the profit
and loss on settlement date.
The Huatai Ultimate Clients may exercise an early termination right to terminate the Huatai TRS at
any time from the issue date of the Huatai TRS which should be on or after the date on which the
Offer Shares are listed on the Stock Exchange at their own discretions. Upon the termination upon
maturity or early termination of the Huatai TRS by the Huatai Ultimate Clients, HTCI will dispose
the Offer Shares on the secondary market and the Huatai Ultimate Clients will receive a final
settlement amount in cash in accordance with the terms and conditions of the HT Back-to-back TRS
and the Huatai TRS which should have taken into account all the economic returns or economic loss
in relation to the Offer Shares. If upon the maturity of the Huatai TRS, the Huatai Ultimate Clients
intend to extend the investment period, subject to further agreement between HTSC and the relevant
Huatai Ultimate Clients, the term of the Huatai TRS could be extended by way of a new issuance or a
tenor extension. Accordingly, HTSC will extend the term of the HT Back-to-back TRS by way of a
new issuance or a tenor extension.
It is proposed that HTCI will hold the legal title and the voting right of the Offer Shares by itself, and
pass through the economic exposure to the Huatai Ultimate Clients, being an onshore client who
places Huatai TRS orders with HTSC in connection with the IPO of the Company. HTCI will not
exercise the voting rights of the Offer Shares during the tenor of the HT Back-to-back TRS.
During the life of the Huatai TRS and HT Back-to-back TRS, HTCI may continue to hold the Offer
Shares in its custodian account, or to hold some or all of the Offer Shares in a prime brokerage
account for stock borrowing purposes, where HTCI will lend out its holding of underlying Offer
Shares in the form of stock borrowing loans consistent with market practice to lower its finance costs,
provided that HTCI has the ability to call back the Offer Shares on loan at any time in order to satisfy
its obligations under the HT Back-to-back TRS to ensure the economic interests are ultimately passed
to the Huatai Ultimate Clients.
(3)
Bosera will hold the Offer Shares in its capacity as discretionary fund manager managing assets on
behalf of its underlying clients. To the best of Bosera’s knowledge after due enquiry, each underlying
clients of Bosera AM is an independent third party of Bosera AM, CMBI and the companies which
are members of the same group of CMBI.
– 26 –

<<<PAGE 27>>>
(4)
Fullgoal Fund Management Co., Ltd. will hold the Offer Shares in its capacity as the discretionary
fund manager on behalf of its investors, each of which is an independent third party of the Company,
its subsidiaries, its substantial Shareholders, Fullgoal Fund Management Co., Ltd., GTJA, HTI and
the companies which are members of the same group of GTJA and HTI.
(5)
Fullgoal Asset Management (HK) Limited will hold the Offer Shares in its capacity as the
discretionary fund manager managing the funds on behalf of their underlying investors, each of which
is an independent third party of the Company, its subsidiaries, its substantial Shareholders, Fullgoal
Asset Management (HK) Limited, GTJA, HTI and the companies which are members of the same
group of GTJA and HTI.
(6)
GTJA FP shall hold the Offer Shares on a non-discretionary basis for hedging purposes as the single
underlying asset of a delta one back-to-back total return swap transaction (the “GTJA Back-to-back
TRS1”) to be entered into between GTJA FP and Guotai Junan Investments (Hong Kong) Limited
(“GTJA INV”), and GTJA INV shall for hedging purposes enter into a cross-border delta one
back-to-back total return swap transaction (the “GTJA Back-to-back TRS2”) with Guotai Haitong
Securities Co., Ltd. (“GTHTS”), in connection with a total return swap order (the “GTHT Client
TRS”) to be entered into by GTHTS and the GTHTS onshore client (the “GTHT Onshore Client”).
Such GTHT Client TRS is to be fully funded by the GTHT Onshore Client. The full economic
exposure of the Offer Shares will be passed from GTJA FP to GTJA INV under the GTJA
Back-to-back TRS1, from GTJA INV to GTHTS under the GTJA Back-to-back TRS2, and
ultimately from GTHTS to the GTHT Onshore Client under the GTHT Client TRS. The term of the
GTHT Client TRS is one year and the GTHT Onshore Client may exercise an early termination right
to early terminate the GTHT Client TRS at any time from the trade date of the GTHT Client TRS,
which should be on or after the date on which the Offer Shares are listed on the Stock Exchange.
Accordingly, (i) GTHTS may exercise an early termination right to early terminate the GTJA
Back-to-back TRS2 at any time from the trade date of the GTJA Back-to-back TRS2, and (ii) GTJA
INV may exercise an early termination right to early terminate the GTJA Back-to-back TRS1 at any
time from the trade date of the GTJA Back-to-back TRS1, which in each case should be on or after
the date on which the Offer Shares are listed on the Stock Exchange. Upon the final maturity or early
termination of (i) the GTHT Client TRS by the GTHT Onshore Client, (ii) the GTJA Back-to-back
TRS2 by GTHTS, and (iii) the GTJA Back-to-back TRS1 by GTJA INV, GTJA FP will dispose the
Offer Shares on the secondary market and the GTHT Onshore Client ultimately will receive a final
termination amount of the GTHT Client TRS, which should have taken into account all the economic
returns or economic loss in relation to the Offer Shares, the fixed amount in relation to the GTJA
Back-to-back TRS1, the GTJA Back-to-back TRS2 and the GTHT Client TRS. GTJA FP will hold
the legal title and the voting right of the Offer Shares by itself and pass through the economic
exposure to GTJA INV, GTHTS and ultimately the GTHT Onshore Client. The termination of the
GTJA Back-to-back TRS1 and GTJA Back-to-back TRS2 will not result GTJA FP holding the Offer
Shares in its proprietary account. Due to its internal policy, GTJA FP will not exercise the voting
right of the Offer Shares during the tenor of the GTJA Back-to-back TRS1 and GTJA Back-to-back
TRS2.
GTHT Onshore Client is Hongze Jiaxin No. 1 Private Securities Investment Fund (宏澤嘉信1號私募
證券投資基金), whose manager is Fuzhou High-tech Zone Hongze Private Equity Fund Management
Co., Ltd. (福州高新區宏澤私募基金管理有限公司) (“Fuzhou High-tech”). The ultimate beneficial
owner of Fuzhou High-tech is Yao Po (姚釙). Other than Xu Xing (許星), no ultimate beneficial
owner holds 30% or more interest in this fund.
To the best of GTJA FP’s knowledge having made all reasonable inquiries, the GTHT Onshore Client
is an independent third party of GTJA FP, GTJA, HTI and the companies which are members of the
same group of GTJA and HTI.
(7)
Each of the Connected Client is not a collective investment scheme which is not authorized by the
SFC, nor is it holding the Offer Shares on behalf of such schemes.
– 27 –

<<<PAGE 28>>>
DISCLAIMERS
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong
Limited (the “Hong Kong Stock Exchange”) and Hong Kong Securities Clearing
Company
Limited
(“HKSCC”)
take
no
responsibility
for
the
contents
of
this
announcement,
make
no
representation
as
to
its
accuracy
or
completeness
and
expressly disclaim any liability whatsoever for any loss howsoever arising from or in
reliance upon the whole or any part of the contents of this announcement.
This announcement is not for release, publication, distribution, directly or indirectly, in or
into the United States (including its territories and possessions, any state of the United
States and the District of Columbia). This announcement does not constitute or form a
part of any offer or solicitation to purchase or subscribe for securities in the United
States. The securities mentioned herein have not been, and will not be, registered under
the United States Securities Act of 1933, as amended (the “U.S. Securities Act”). The
securities may not be offered or sold in the United States except pursuant to an exemption
from the registration requirements of the U.S. Securities Act and in compliance with any
applicable state securities laws, or outside the United States unless in compliance with
Regulation S under the U.S. Securities Act. There will be no Hong Kong Public Offering
of securities in the United States.
The Offer Shares are being offered and sold outside the United States in offshore
transactions in reliance on Regulation S under the U.S. Securities Act.
This announcement is for information purposes only and does not constitute an invitation
or offer to acquire, purchase or subscribe for securities. This announcement is not a
prospectus. Potential investors should read the Prospectus dated December 30, 2025
issued by Shanghai Iluvatar CoreX Semiconductor Co., Ltd. for detailed information
about the Global Offering described below before deciding whether or not to invest in the
Shares thereby being offered.
*
Potential investors of the Offer Shares should note that the Sole Sponsor and the
Sponsor-Overall Coordinator (for itself and on behalf of the other Hong Kong
Underwriters) shall be entitled to terminate their obligations under the Hong Kong
Underwriting Agreement with immediate effect upon the occurrence of any of the
events set out in the paragraph headed “Underwriting — Underwriting Arrangements
— Hong Kong Public Offering — Grounds for Termination” in the Prospectus at any
time prior to 8: 00 a.m. (Hong Kong time) on the Listing Date (which is currently
expected to be on Thursday, January 8, 2026).
PUBLIC FLOAT AND FREE FLOAT
Immediately following the completion of the Global Offering, the total number of the H
Shares held by the public represents approximately 41.87% of the total issued share
capital of the Company, which is higher than the prescribed percentage of H Shares
required to be held in public hands of 12.24% under Rule 19A.13A(1) of the Listing
Rules calculated based on the Offer Price of HK$144.60 per H Share, thereby satisfying
the public float requirement under Rule 19A.13A(1) of the Listing Rules.
– 28 –

<<<PAGE 29>>>
Each of the Cornerstone Investors has agreed to a lock-up period of six months following
the Listing Date. As such, Shares held by the Cornerstone Investors upon the Listing
shall not be counted towards the free float of the Shares of the Company at the time of
Listing. Based on the final Offer Price of HK$144.60 per H Share, the Company satisfies
the free float requirement under Rule 19A.13C(1)(b) of the Listing Rules.
The Directors confirm that, immediately following the completion of the Global
Offering, (i) no placee will, individually, be placed more than 10% of the enlarged issued
share capital of the Company immediately after the Global Offering; (ii) there will not be
any new substantial Shareholder immediately after the Global Offering; (iii) the three
largest public Shareholders do not hold more than 50% of the H Shares held in the public
hands at the time of the Listing in compliance with Rules 8.08(3) and 8.24 of the Listing
Rules; and (iv) there will be at least 300 Shareholders at the time of the Listing in
compliance with Rule 8.08(2) of the Listing Rules.
COMMENCEMENT OF DEALINGS
The H Share certificates will only become valid evidence of title at 8: 00 a.m. on
Thursday, January 8, 2026 (Hong Kong time), provided that the Global Offering has
become unconditional and the right of termination described in the paragraph headed
“Underwriting — Underwriting Arrangements — Hong Kong Public Offering —
Grounds for Termination” in the Prospectus has not been exercised. Investors who
trade the H Shares on the basis of publicly available allocation details prior to the receipt
of H Share certificates or prior to the H Share certificates becoming valid evidence of title
do so entirely at their own risk.
Assuming that the Global Offering becomes unconditional at or before 8: 00 a.m. on
Thursday, January 8, 2026 (Hong Kong time), it is expected that dealings in the H Shares
on the Hong Kong Stock Exchange will commence at 9: 00 a.m. on Thursday, January 8,
2026 (Hong Kong time).
The H Shares will be traded in board lots of 100 H Shares each, and the stock code of the
H Shares will be 9903.
By order of the Board
Shanghai Iluvatar CoreX Semiconductor Co., Ltd.
上海天數智芯半導體股份有限公司
Mr. Gai Lujiang
Chairman of the Board
Hong Kong, January 7, 2026
As at the date of this announcement, the Board comprises Mr. Gai Lujiang, Mr. Sun Yile,
Mr. Liu Zheng and Mr. Yang Lei as executive Directors, Mr. Wang Chen and Ms. Kou
Xiaoxiao as non-executive Directors, and Dr. Teng Yong, Mr. Ren Jintao and Dr. Wang
Yan as independent non-executive Directors.
– 29 –
