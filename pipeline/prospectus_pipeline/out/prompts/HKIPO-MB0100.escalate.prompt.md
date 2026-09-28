你是 HK IPO 数据库的数据员，负责公司 0100.HK MiniMax Group Inc. - W - P 的字段质量。

## 公司
- 公司：0100.HK MiniMax Group Inc. - W - P


<<< 抽取包开始（权威字段契约与种子切片） >>>

# 招股书抽取任务包：0100.HK MiniMax Group Inc. - W - P

- 来源：https://www1.hkexnews.hk/listedco/listconews/sehk/2025/1231/2025123100025.pdf
- 港交所文件：Listing Documents - [Offer for Subscription] / GLOBAL OFFERING（31/12/2025 06:10）
- 招股书日期：2025-12-31 ｜ 上市日期：2026-01-09
- 本包只包含招股书来源字段；字段名、类型、缺失值和期间契约见字段清单。

## 唯一输出契约（必须严格遵守）

只输出一个 JSON 对象，且**顶层必须是**：
`{"code":"0100.HK","fields":{"col_X":{"value":...,"page":...,"quote":"...","confidence":"high|medium|low"}}}`。
不要输出 Markdown 围栏、解释文字、notes 顶层键或额外字段。每个字段 key 必须出现且只能出现一次。
`page` 必须是本包中的正整数页码；缺失时为 `null`。`quote` 必须是本包原文的短摘录（最多 200 字符）；缺失时为空字符串。

## 手册硬规则

1. 只依据本包原文，不使用常识、外部网页或估算；不确定就使用字段契约指定的 `NaN`/`NA`。
2. 金额换算为基本货币单位；百分比填小数；确认零填数字 0。
3. year-1/2/3 必须对应同一套历史期间；year-1 销售/利润若为非全年，按手册年化。AU/AW/AX 为期间流量，AV/BE 为期末余额；这些扩展字段不年化。
4. 经营现金流是 net cash from operating activities；现金及等价物不自动包含受限现金。
5. `AX` 只填资本化开发成本的**当期新增**，不是无形资产期末余额；`AY` 是 year-1 前五大客户收入占比。表格明确为 `–`/nil 时填数字 0。
6. 承销佣金：按全球发售披露时 AO/AP 同率；只按香港公开发售披露时 AP=0；不能把总上市费用当佣金。绿鞋 AQ 只能按招股书披露，不能默认 15%。
7. `CJ` 基石名单必须来自真正的 Cornerstone Investors/Cornerstone Placing 协议和名单表；不要使用目录、豁免段或普通提及。
8. listing route 必须按招股书披露的 basis of listing/适用章节填写，不能按行业猜测；中文名填简体中文。
9. `BA` 只表示上市前是否有 VC/PE 支持；基石投资者身份本身不能证明 BA。`BC`/`BD` 分别是控制人上市时经济权益/投票权，不是基石最终获配。
10. 每一项都要保留准确页码、原文短摘录和置信度；不得为了配平而修改原文数字。

---


## 股份结构（L–S）

- `col_L` = Total (without option) (type=integer unit=shares missing=NaN)
- `col_M` = Global Offering (without option) (type=integer unit=shares missing=NaN)
- `col_N` = Number of offer shares under the capitalization Issue (type=integer unit=shares missing=NaN)
- `col_O` = Number of offer shares under Capitalization Rest (type=integer unit=shares missing=NaN)
- `col_P` = Sale Shares (type=integer unit=shares missing=NaN)
- `col_Q` = New shares  (type=integer unit=shares missing=NaN)
- `col_R` = Placing Shares (type=integer unit=shares missing=NaN)
- `col_S` = Public Offer shares (type=integer unit=shares missing=NaN)
- `col_BI` = Share class (type=text unit=text missing=NA)
- `col_CE` = H shares after IPO (base; no options) (type=integer unit=shares missing=NaN)

### 原文切片：股份结构（L–S）


<<<PAGE 401>>>
AUTHORIZED AND ISSUED SHARE CAPITAL
The following is a description of the authorized and issued share capital of our Company
in issue and to be issued as fully paid or credited as fully paid upon Listing, assuming the
Presumptions.
Share capital as of the date of this Prospectus
(i)
Authorized share capital
Number
Description of Shares
Aggregate
Nominal Value
221,311,196
Class A Ordinary Shares with a nominal
value of US$0.0001 each in issue
US$22,131.1196
106,650,075
Class B Ordinary Shares with a nominal
value of US$0.0001 each in issue
US$10,665.0075
172,038,729
Preferred Shares with a nominal
value of US$0.0001 each in issue
US$17,203.8729
500,000,000
Total
US$50,000
(ii)
Issued and to be issued, fully paid or credited to be fully paid
Number
Description of Shares
Aggregate
Nominal Value
22,890,736(1)
Class A Ordinary Shares with a nominal
value of US$0.0001 each in issue
US$2,289.0736
85,759,339(2)
Class B Ordinary Shares with a nominal
value of US$0.0001 each in issue
US$8,575.9339
171,407,993
Preferred Shares with a nominal value of
US$0.0001 each in issue
US$17,140.7993
280,058,068
Total
US$28,005.8068
Notes:
(1)
representing 343,195 Class A Ordinary Shares, 20,890,736 Class A Ordinary Shares and 1,656,805 Class
A Ordinary Shares held by Alpha EXP, MiniMax Gene and Himalia Holding Limited, respectively, as
of the date of this Prospectus.
(2)
representing 15 Class B Ordinary Shares, 5,000,000 Class B Ordinary Shares, 11,509,339 Class B
Ordinary Shares, 62,249,985 Class B Ordinary Shares and 7,000,000 Class B Ordinary Shares held by
MiniMax Limited, MiniMax Matrix, MiniMax Awakening, Alpha EXP and Floating Sky, respectively,
as of the date of this Prospectus.
SHARE CAPITAL
– 391 –

<<<PAGE 402>>>
Share capital immediately following the completion of the Global Offering
(i)
Authorized share capital
Number
Description of Shares
Aggregate
Nominal Value
393,349,925
Class A Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$39,334.9925
106,650,075
Class B Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$10,665.0075
500,000,000
Total
US$50,000
(ii)
Issued and to be issued, fully paid or credited to be fully paid (assuming the Offer Size
Adjustment Option and the Over-allotment Option are not exercised)
Number
Description of Shares
Aggregate
Nominal Value
22,547,541(1)
Class A Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$2,254.7541
80,759,339(2)
Class B Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$8,075.9339
343,195(3)
Class A Ordinary Shares to be converted into
Class B Ordinary Shares
US$34.3195
5,000,000(4)
Class B Ordinary Shares to be converted into
Class A Ordinary Shares
US$500
171,407,993
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued on conversion of
Preferred Shares
US$17,140.7993
25,389,220
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued pursuant to the
Global Offering
US$2,538.9220
305,447,288
Total
US$30,544.7288
SHARE CAPITAL
– 392 –

<<<PAGE 403>>>
Notes:
(1)
representing 20,890,736 Class A Ordinary Shares and 1,656,805 Class A Ordinary Shares held by
MiniMax Gene and Himalia Holding Limited, respectively, upon Listing.
(2)
representing 15 Class B Ordinary Shares, 11,509,339 Class B Ordinary Shares, 62,249,985 Class B
Ordinary Shares and 7,000,000 Class B Ordinary Shares held by MiniMax Limited, MiniMax
Awakening, Alpha EXP and Floating Sky, respectively, upon Listing.
(3)
representing 343,195 Class A Ordinary Shares held by Alpha EXP to be converted into Class B Ordinary
Shares upon Listing.
(4)
representing 5,000,000 Class B Ordinary Shares held by MiniMax Matrix to be converted into Class A
Ordinary Shares upon Listing.
(iii) Issued and to be issued, fully paid or credited to be fully paid (assuming the Offer Size
Adjustment Option is fully exercised and the Over-allotment Option is not exercised)
Number
Description of Shares
Aggregate
Nominal Value
22,547,541(1)
Class A Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$2,254.7541
80,759,339(2)
Class B Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$8,075.9339
343,195(3)
Class A Ordinary Shares to be converted into
Class B Ordinary Shares
US$34.3195
5,000,000(4)
Class B Ordinary Shares to be converted into
Class A Ordinary Shares
US$500
171,407,993
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued on conversion of
Preferred Shares
US$17,140.7993
25,389,220
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued pursuant to the
Global Offering
US$2,538.9220
3,808,380
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued pursuant to the
Offer Size Adjustment Option
US$380.8380
309,255,668
Total
US$30,925.5668
Note:
please refer to the section headed “— (ii) Issued and to be issued, fully paid or credited to be fully paid
(assuming the Offer Size Adjustment Option and the Over-allotment Option are not exercised)” above.
SHARE CAPITAL
– 393 –

<<<PAGE 404>>>
(iv)
Issued and to be issued, fully paid or credited to be fully paid (assuming the Offer Size
Adjustment Option is not exercised and the Over-allotment Option is fully exercised)
Number
Description of Shares
Aggregate
Nominal Value
22,547,541(1)
Class A Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$2,254.7541
80,759,339(2)
Class B Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$8,075.9339
343,195(3)
Class A Ordinary Shares to be converted into
Class B Ordinary Shares
US$34.3195
5,000,000(4)
Class B Ordinary Shares to be converted into
Class A Ordinary Shares
US$500
171,407,993
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued on conversion of
Preferred Shares
US$17,140.7993
25,389,220
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued pursuant to the
Global Offering
US$2,538.9220
3,808,380
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued pursuant to the
Over-allotment Option
US$380.8380
309,255,668
Total
US$30,925.5668
Note:
please refer to the section headed “— (ii) Issued and to be issued, fully paid or credited to be fully paid
(assuming the Offer Size Adjustment Option and the Over-allotment Option are not exercised)” above.
SHARE CAPITAL
– 394 –

<<<PAGE 405>>>
(v)
Issued and to be issued, fully paid or credited to be fully paid (assuming the Offer Size
Adjustment Option and the Over-allotment Option are fully exercised)
Number
Description of Shares
Aggregate
Nominal Value
22,547,541(1)
Class A Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$2,254.7541
80,759,339(2)
Class B Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$8,075.9339
343,195(3)
Class A Ordinary Shares to be converted into
Class B Ordinary Shares
US$34.3195
5,000,000(4)
Class B Ordinary Shares to be converted into
Class A Ordinary Shares
US$500
171,407,993
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued on conversion of
Preferred Shares
US$17,140.7993
25,389,220
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued pursuant to the
Global Offering
US$2,538.9220
3,808,380
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued pursuant to the
Offer Size Adjustment Option
US$380.8380
4,379,640
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued pursuant to the
Over-allotment Option
US$437.9640
313,635,308
Total
US$31,363.5308
Note:
please refer to the section headed “— (ii) Issued and to be issued, fully paid or credited to be fully paid
(assuming the Offer Size Adjustment Option and the Over-allotment Option are not exercised)” above.
SHARE CAPITAL
– 395 –

<<<PAGE 406>>>
WEIGHTED VOTING RIGHTS STRUCTURE
The Company has a weighted voting rights structure. Under our weighted voting rights
structure, our share capital comprises Class A Ordinary Shares and Class B Ordinary Shares.
Each Class B Ordinary Share entitles the holder to exercise ten votes, and each Class A
Ordinary Share entitles the holder to exercise one vote, respectively, on any matters subject to
the vote at general meetings of the Company, subject to Rule 8A.24 of the Listing Rules that
requires the Reserved Matters to be voted on a one vote per share basis.
The Reserved Matters are:
(i)
any amendment to the Memorandum and Articles;
(ii)
the variation of the rights attached to any class of Shares;
(iii) the appointment, election or removal of any independent non-executive Director;
(iv) the appointment or removal of the Company’s auditors; and
(v)
the voluntary liquidation or winding-up of the Company.
See “Summary of the Constitution of our Company and Cayman Islands Company Law
— 2 Articles of Association” in Appendix III to this Prospectus for further details.
Class B Ordinary Shares may be converted into Class A Ordinary Shares on a one to one
basis. Upon the conversion of all the issued and outstanding Class B Ordinary Shares into Class
A Ordinary Shares, the Company will issue 81,102,534 Class A Ordinary Shares, representing
approximately 26.55% of the total number of issued Class A Ordinary Shares immediately
following the Listing (assuming the Offer Size Adjustment Option and the Over-allotment
Option are not exercised).
The weighted voting rights attached to our Class B Ordinary Shares will cease when the
WVR Beneficiaries cease to have beneficial ownership of any of our Class B Ordinary Shares,
in accordance with Rule 8A.22 of the Listing Rules. This may occur:
(i)
upon the occurrence of any of the circumstances set out in Rule 8A.17 of the Listing
Rules, in particular where the WVR Beneficiaries are: (1) deceased; (2) no longer
a member of our Board; (3) deemed by the Stock Exchange to be incapacitated for
the purpose of performing his duties as a director; or (4) deemed by the Stock
Exchange to no longer meet the requirements of a director set out in the Listing
Rules;
(ii)
when the holders of Class B Ordinary Shares have transferred to another person the
beneficial ownership of, or economic interest in, the Class B Ordinary Shares or the
control over the voting rights attached to them, other than in the circumstances
permitted by Rule 8A.18 of the Listing Rule;
SHARE CAPITAL
– 396 –

<<<PAGE 407>>>
(iii) where a vehicle holding Class B Ordinary Shares on behalf of a WVR Beneficiary
no longer complies with Rule 8A.18(2) of the Listing Rule; or
(iv) when all of the Class B Ordinary Shares have been converted to Class A Ordinary
Shares.
Shareholding Structure of the WVR Beneficiaries
The table below sets out the beneficial interests entitled to and voting rights to be held
by the WVR Beneficiaries upon the completion of the Global Offering (assuming the Offer
Size Adjustment Option and the Over-allotment Option are not exercised):
Number of
Class B
Ordinary Shares
held
Number of Class
A Ordinary
Shares interested
in(3)
Approximate
percentage of
beneficial
interests
in the issued
share capital
Approximate
percentage of
voting rights
controlled(1)
Dr. Yan(2)   
74,102,534
3,355,030
25.36%
72.05%
Ms. Yun(2)   
7,000,000
1,644,970
2.83%
6.76%
Notes:
(1)
On the basis that each Class A Ordinary Share entitles the Shareholder to one vote per Share and each
Class B Ordinary Share entitles the Shareholder to ten votes per Share.
(2)
For details of the shareholding structure of our WVR Beneficiaries, please refer to the section headed
“History, Reorganization and Corporate Structure.”
(3)
Dr. Yan and Ms. Yun are interested in MiniMax Matrix as to 67.1% and 32.9%.
The Company confirms that the holding arrangement through which the WVR
Beneficiaries hold the Class B Ordinary Shares as described above meets the requirements in
Rule 8A.18 of the Listing Rules and the holding arrangement is permitted under the
“Consultation Conclusions — a listing regime for companies from emerging and innovative
sectors” issued by the Stock Exchange in April 2018, namely: (a) a partnership of which the
WVR Beneficiary is a partner and the terms of which must expressly specify that the voting
rights attached to any and all of the Class B Ordinary Shares held by such partnership are solely
dictated by the WVR Beneficiary; (b) a trust of which the WVR Beneficiary is a beneficiary
and that meets the following conditions: (i) the WVR Beneficiary must in substance retain an
element of control of the trust and any immediate holding companies of, or, if not permitted
in the relevant tax jurisdiction, retain a beneficial interest in any and all of the Class B Ordinary
Shares held by such trust; and (ii) the purpose of the trust must be for estate planning and/or
tax planning purposes; or (c) a private company or other vehicle wholly owned and wholly
controlled by the WVR Beneficiary or by a trust referred to in paragraph (b) above.
SHARE CAPITAL
– 397 –

<<<PAGE 408>>>
To ensure that there will not be any circumvention of Rule 8A.18(1), each of the
Company, Dr. Yan and Ms. Yun undertakes that so long there is any weighted voting rights
attached to the Shares held by Alpha EXP, MiniMax Gene, Floating Sky, MiniMax Awakening,
MiniMax Limited (the “WVR Management Shareholders”), respectively, Dr. Yan and Ms.
Yun will not transfer any beneficial ownership of or economic interest in the WVR
Management Shareholders or the control over the voting rights attached to the Shares held by
WVR Management Shareholders to another person. In the event that there is any change in the
beneficial ownership of or economic interest in the Shares held by the WVR Management
Shareholders or the control over the voting rights attached to the Shares held by the WVR
Management Shareholders to another person, the Company, Dr. Yan and Ms. Yun will notify
the Stock Exchange pursuant to Rule 8A.19 of the Listing Rules and comply with the relevant
statutory obligations including obligations of disclosure of interests under the SFO, and the
weighted voting rights attached to the Class B Ordinary Shares held by WVR Management
Shareholders shall cease upon such transfer accordingly. The Company will also comply with
Rule 8A.30 of the Listing Rules to confirm, on an annual basis, that the WVR Beneficiary has
complied with Rule 8A.18 of the Listing Rules.
Contribution of the WVR Beneficiaries
Dr. Yan and Ms. Yun, being the WVR beneficiaries, have been materially responsible for
the growth of the Company’s business during the Track Record Period by way of their
respective skills, knowledge and/or insights to the industry. As the core of the Group’s
leadership team and leveraging their professional experience in the industry, each of Dr. Yan
and Ms. Yun is pivotal to the success of the Group and has made significant contributions to
the Group from strategic, technological and operational perspectives.
We set forth below the academic background, work experience and contribution of the
proposed WVR beneficiaries to the success of the Company:
Dr. Yan
Dr. Yan is the founder, the chairman of the board of directors, chief executive officer and
chief technology officer of the Company. As the chief executive officer and chief technology
officer of the Company, Dr. Yan has been integral to the success of the Company and has been
materially responsible for the founding and growth of the Company during the Track Record
Period. Dr. Yan, with profound technical insight and deep understanding and knowledge of AI
technology, laid the foundation for the Company and was critical in shaping the Group’s
mission, vision and values, and devising long-term strategies for the R&D and operations of
the Group over the years. During the Track Record Period, Dr. Yan had spearheaded the team
in developing a trimodal large model that integrates text, audio, and visual capabilities and
have led our Group to achieve its key milestones. For example, he led the launch of our first
text model abab1 in 2022, our text model abab5.5 and speech model MiniMax-Speech-01 in
2023, our MoE text model abab6, visual generation platform Hailuo AI and video-generation
model Hailuo-01 and music model Music-01 in 2024 as well as our open-source text model
MiniMax-Text-01, MiniMax-M1 and MiniMax-M2 in 2025. In addition, leveraging the
SHARE CAPITAL
– 398 –

<<<PAGE 546>>>
CONSOLIDATED STATEMENTS OF CHANGES IN DEFICITS
Attributable to owners of the parent
Share
capital
Share
option
reserve*
Exchange
fluctuation
reserve*
Accumulated
losses*
Total
USD’000
USD’000
USD’000
USD’000
USD’000
At 31 December 2021
(unaudited)            
–
–
–
(3,814)
(3,814)
Loss for the year          
–
–
–
(73,728)
(73,728)
Other comprehensive income
for the year:
Exchange differences on
translation of foreign
operations             
–
–
99
–
99
Total comprehensive loss for
the year               
–
–
99
(73,728)
(73,629)
Recognition of share-based
payment expenses       
–
1,069
–
–
1,069
At 31 December 2022      
–
1,069
99
(77,542)
(76,374)
Attributable to owners of the parent
Share
capital
Share
option
reserve*
Exchange
fluctuation
reserve*
Accumulated
losses*
Total
USD’000
USD’000
USD’000
USD’000
USD’000
At 31 December 2022      
–
1,069
99
(77,542)
(76,374)
Loss for the year          
–
–
–
(269,246)
(269,246)
Other comprehensive income
for the year:
Exchange differences on
translation of foreign
operations             
–
–
360
–
360
Total comprehensive loss for
the year               
–
–
360
(269,246)
(268,886)
Recognition of share-based
payment expenses       
–
3,346
–
–
3,346
At 31 December 2023      
–
4,415
459
(346,788)
(341,914)
APPENDIX I
ACCOUNTANT’S REPORT
– I-9 –

<<<PAGE 547>>>
Attributable to owners of the parent
Share
capital
Share
option
reserve*
Fair value
reserve of
financial
assets at
fair value
through other
comprehensive
income*
Exchange
fluctuation
reserve*
Accumulated
losses*
Total
USD’000
USD’000
USD’000
USD’000
USD’000
USD’000
At 31 December 2023  
–
4,415
–
459
(346,788)
(341,914)
Loss for the year     
–
–
–
–
(465,238)
(465,238)
Other comprehensive
income for the year:
Change in fair value of
equity investments at
fair value through
other comprehensive,
net of tax        
–
–
662
–
–
662
Exchange differences on
translation of foreign
operations        
–
–
–
347
–
347
Total comprehensive
loss for the year    
–
–
662
347
(465,238)
(464,229)
Recognition of
share-based payment
expenses         
–
6,823
–
–
–
6,823
At 31 December 2024  
–
11,238
662
806
(812,026)
(799,320)
APPENDIX I
ACCOUNTANT’S REPORT
– I-10 –

<<<PAGE 548>>>
Attributable to owners of the parent
Share
capital
Share
option
reserve
Fair value
reserve of
financial
assets at
fair value
through other
comprehensive
income
Exchange
fluctuation
reserve
Accumulated
losses
Total
USD’000
USD’000
USD’000
USD’000
USD’000
USD’000
At 31 December 2023

–
4,415
–
459
(346,788)
(341,914)
Loss for the period
(unaudited)       
–
–
–
–
(304,342)
(304,342)
Other comprehensive
income for the period:
Change in fair value of
equity investments at
fair value through
other comprehensive,
net of tax (unaudited)
–
–
(839)
–
–
(839)
Exchange differences on
translation of foreign
operations
(unaudited)       
–
–
–
(86)
–
(86)
Total comprehensive
loss for the period
(unaudited)       
–
–
(839)
(86)
(304,342)
(305,267)
Recognition of share-
based payment
expenses (unaudited) 
–
6,100
–
–
–
6,100
At 30 September 2024
(unaudited)       
–
10,515
(839)
373
(651,130)
(641,081)
APPENDIX I
ACCOUNTANT’S REPORT
– I-11 –

<<<PAGE 549>>>
Attributable to owners of the parent
Share
capital
Share
option
reserve*
Fair value
reserve of
financial
assets at
fair value
through other
comprehensive
income*
Exchange
fluctuation
reserve*
Accumulated
losses*
Total
USD’000
USD’000
USD’000
USD’000
USD’000
USD’000
At 31 December 2024  
–
11,238
662
806
(812,026)
(799,320)
Loss for the period    
–
–
–
–
(512,013)
(512,013)
Other comprehensive
income for the period:
Change in fair value of
equity investments at
fair value through
other comprehensive,
net of tax        
–
–
1,604
–
–
1,604
Exchange differences on
translation of foreign
operations        
–
–
–
(1,255)
–
(1,255)
Total comprehensive
loss for the period   
–
–
1,604
(1,255)
(512,013)
(511,664)
Recognition of share-
based payment
expenses         
–
8,581
–
–
–
8,581
Deemed distribution   
–
–
–
–
(1,096)
(1,096)
At 30 September 2025 
–
19,819
2,266
(449)
(1,325,135) (1,303,499)
*
These
deficits
accounts
comprise
the
consolidated
deficits
of
USD76,374,000,
USD341,914,000,
USD799,320,000 and USD1,303,499,000 in the consolidated statements of financial position as at 31
December 2022, 2023 and 2024 and 30 September 2025, respectively.
APPENDIX I
ACCOUNTANT’S REPORT
– I-12 –

<<<PAGE 550>>>
CONSOLIDATED STATEMENTS OF CASH FLOWS
Year ended 31 December
Nine months ended
30 September
Notes
2022
2023
2024
2024
2025
USD’000
USD’000
USD’000
USD’000
USD’000
(unaudited)
CASH FLOWS FROM
OPERATING ACTIVITIES
Loss before tax            
(73,728)
(269,246)
(465,238)
(304,342)
(512,013)
Adjustments for:
Finance costs            
6
14
61
509
316
511
Interest income          
5
(39)
(7,785)
(20,448)
(17,199)
(7,876)
Fair value gain on financial
assets at fair value through
profit or loss          
5
(941)
(788)
(15,710)
(6,682)
(20,414)
Fair value loss on financial
liabilities             
7
60,509
176,826
214,172
128,063
313,477
(Gains)/losses on disposal of
right-of-use assets       
–
(70)
1
–
(175)
Depreciation of property, plant
and equipment         
13
25
180
451
325
582
Depreciation of right-of-use
assets               
14
182
631
1,450
1,072
1,478
Share-based payment expense 
26
1,069
3,346
6,823
6,100
8,581
Provision for impairment on
financial assets         
15
–
3
88
68
22
(12,909)
(96,842)
(277,902)
(192,279)
(215,827)
Increase in trade receivables    
–
(1,341)
(5,732)
(4,230)
(1,103)
(Increase)/decrease in
prepayments, other receivables
and other assets          
(513)
(4,190)
(9,272)
(11,925)
1,846
Increase in trade and bills
payables               
2,394
14,848
33,970
37,949
19,007
Increase/(decrease) in other
payables, accruals and other
liabilities              
2,191
12,624
21,048
4,557
(22,865)
Increase in other non-current
liabilities              
–
1,218
–
–
267
Increase in contract liabilities   
–
559
994
481
3,104
(Increase)/decrease in restricted
cash                 
(2,221)
2,182
(27,292)
(35,347)
2,193
Cash flows used in operating
activities              
(11,058)
(70,942)
(264,186)
(200,794)
(213,378)
Interest received           
39
6,487
5,703
5,198
3,982
Net cash flows used in operating
activities              
(11,019)
(64,455)
(258,483)
(195,596)
(209,396)
APPENDIX I
ACCOUNTANT’S REPORT
– I-13 –

<<<PAGE 551>>>
Year ended 31 December
Nine months ended
30 September
Notes
2022
2023
2024
2024
2025
USD’000
USD’000
USD’000
USD’000
USD’000
(unaudited)
CASH FLOWS FROM
INVESTING ACTIVITIES
Purchases of items of property,
plant and equipment       
(256)
(697)
(759)
(496)
(479)
Placement of time deposits     
–
(90,400)
(199,100)
(195,200)
–
Maturity of time deposits      
–
–
271,201
267,036
26,513
Proceeds from disposal of
financial assets at amortised
cost                 
–
–
982,359
862,084
2,531,476
Purchase of financial assets at
amortised cost           
–
–
(1,121,788)
(1,033,743)
(2,380,324)
Purchases of financial assets at
fair value through other
comprehensive income      
–
–
(4,174)
(4,174)
–
Proceeds from disposal of
financial assets at fair value
through profit or loss       
11,050
136,076
1,851,346
1,056,303
1,519,366
Purchases of financial assets at
fair value through profit or
loss                  
(45,950)
(85,299)
(2,210,385)
(1,582,273)
(1,822,783)
Net cash flows used in investing
activities              
(35,156)
(40,320)
(431,300)
(630,463)
(126,231)
CASH FLOWS FROM
FINANCING ACTIVITIES
Proceeds from issuance of
convertible bonds         
–
–
13,910
13,910
–
Proceeds from issuance of
convertible redeemable
preferred shares          
50,000
307,000
739,588
686,372
426,262
New bank and other borrowings 
–
–
19,455
19,455
44,565
Repayment of bank and
other borrowings         
–
–
–
–
(44,918)
Repayment of convertible bonds 
–
–
–
–
(14,668)
Interest paid for bank borrowings 
–
–
(355)
(199)
(404)
Principal portion of lease
payments              
14(b)
(200)
(696)
(1,352)
(1,097)
(1,364)
Interest paid for leases       
14(b)
(14)
(61)
(154)
(117)
(107)
Payment of Listing expenses    
–
–
–
–
(357)
Others                 
–
–
–
503
(1,096)
Net cash flows from financing
activities              
49,786
306,243
771,092
718,827
407,913
APPENDIX I
ACCOUNTANT’S REPORT
– I-14 –

<<<PAGE 552>>>
Year ended 31 December
Nine months ended
30 September
Notes
2022
2023
2024
2024
2025
USD’000
USD’000
USD’000
USD’000
USD’000
(unaudited)
NET INCREASE/(DECREASE)
IN CASH AND CASH
EQUIVALENTS         
3,611
201,468
81,309
(107,232)
72,286
Cash and cash equivalents at
beginning of year/period     
994
4,691
206,295
206,295
288,912
Effect of foreign exchange rate
changes, net            
86
136
1,308
500
1,449
CASH AND CASH
EQUIVALENTS AT END OF
YEAR/PERIOD          
18
4,691
206,295
288,912
99,563
362,647
APPENDIX I
ACCOUNTANT’S REPORT
– I-15 –

<<<PAGE 553>>>
STATEMENTS OF FINANCIAL POSITION OF THE COMPANY
As at 31 December
As at
30 September
Notes
2022
2023
2024
2025
USD’000
USD’000
USD’000
USD’000
NON-CURRENT ASSETS
Investments in subsidiaries     
17
1,069
4,415
11,238
19,819
Financial assets at fair value
through profit or loss       
17
–
–
95,331
70,228
Total non-current assets      
1,069
4,415
106,569
90,047
CURRENT ASSETS
Prepayments, other receivables
and other assets           
16
14,100
103,895
360,091
663,642
Financial assets at amortised
cost                    
17
–
–
147,444
–
Financial assets at fair value
through profit or loss       
17
65,791
10,152
295,220
639,899
Restricted cash              
18
–
–
11,802
–
Time deposits               
18
–
91,598
26,327
–
Cash and cash equivalents     
18
1,784
191,634
235,209
250,712
Total current assets         
81,675
397,279
1,076,093
1,554,253
CURRENT LIABILITIES
Convertible redeemable
preferred shares           
24
145,175
629,001
1,581,949
2,321,193
Other payables, accruals and
other liabilities            
–
330
71
1,319
Total current liabilities       
145,175
629,331
1,582,020
2,322,512
NET CURRENT
LIABILITIES            
(63,500)
(232,052)
(505,927)
(768,259)
TOTAL ASSETS LESS
CURRENT LIABILITIES  
(62,431)
(227,637)
(399,358)
(678,212)
NON-CURRENT
LIABILITIES
Total non-current liabilities   
–
–
–
–
Net liabilities              
(62,431)
(227,637)
(399,358)
(678,212)
DEFICITS
Share capital               
–
–
–
–
Deficits                   
25
(62,431)
(227,637)
(399,358)
(678,212)
Total deficits               
(62,431)
(227,637)
(399,358)
(678,212)
APPENDIX I
ACCOUNTANT’S REPORT
– I-16 –

<<<PAGE 39>>>
GLOBAL OFFERING STATISTICS
All statistics in the following table are based on the assumption that the Offer Size
Adjustment Option and the Over-allotment Option are not exercised.
Based on an
Offer Price of
HK$151.00
per Share
Based on an
Offer Price of
HK$165.00
per Share
Market capitalization of our Shares(1)          
HK$46,122.54
million
HK$50,398.80
million
Unaudited pro forma adjusted consolidated net
tangible assets per Share(2)                
HK$37.96
HK$39.08
(1)
The calculation of the market capitalization of our Shares is based on the assumption that 305,447,288
Shares will be in issue and outstanding immediately following the completion of the Global Offering.
(2)
The unaudited pro forma adjusted consolidated net tangible assets per Share is calculated after making
the adjustments referred to in “Appendix II — Unaudited Pro Forma Financial Information” and on the
basis that 305,447,288 shares were in issue assuming that the Global Offering and reclassification of
financial liabilities arising from the convertible redeemable preferred shares and ordinary shares into
equity had been completed on September 30, 2025, without taking account of the exercise of the Offer
Size Adjustment Option and the Over-allotment Option. The unaudited pro forma adjusted consolidated
net tangible assets per Share amounts in USD are converted into Hong Kong dollars at USD1.00 =
HKD7.7805 prevailing on the Latest Practicable Date.
Listing Expenses
Our
listing
expenses
mainly
include
(i)
underwriting-related
expenses,
such
as
underwriting fees and commissions, and (ii) non-underwriting-related expenses, comprising
professional fees paid to our legal advisors and reporting accountants for their services
rendered in relation to the Listing and the Global Offering, and other fees and expenses.
Assuming full payment of the discretionary incentive fee, the estimated total listing expenses
(based on the mid-point of the Offer Price range and assuming that the Offer Size Adjustment
Option and the Over-allotment Option are not exercised) for the Global Offering are
approximately HK$193.2 million, accounting for approximately 4.8% of our gross proceeds.
Among such estimated total listing expenses, we expect to pay underwriting-related expenses
of HK$133.0 million, professional fees for our legal advisors and reporting accountants of
HK$40.3 million and other fees and expenses of HK$19.9 million. During the Track Record
Period, the listing expenses charged to our consolidated statements of profit or loss were
US$3.7 million (HK$28.6 million) and the issuance costs which were recognized as
prepayments and are expected to be deducted from equity upon the Listing, were US$0.4
million (HK$3.3 million). After the Track Record Period approximately HK$26.7 million is
expected to be charged to our consolidated statements of profit or loss, and approximately
HK$134.7 million is expected to be accounted for as a deduction from equity upon the Listing.
SUMMARY
– 29 –

<<<PAGE 40>>>
Future Plans and Use of Proceeds
We estimate that we will receive net proceeds from the Global Offering of approximately
HK$3,818.3 million, after deducting underwriting commissions, fees and estimated expenses
payable by us in connection with the Global Offering, assuming the Offer Size Adjustment
Option or Over-allotment Option is not exercised and an Offer Price of HK$158.00 per Offer
Share, being the midpoint of the indicative Offer Price range stated in this Prospectus.
We intend to use the net proceeds of the Global Offering for the following purposes:
•
Approximately 90%, or HK$3,436.4 million of the net proceeds will be used for our
research and development over the next five years including the development of our
foundation models and our AI-native products. Specifically, (i) approximately
70.0%, or HK$2,672.8 million, of the net proceeds over the next five years to the
research and development of our foundation models; and (ii) approximately 20.0%,
or HK$763.7 million, of the net proceeds over the next five years to the
development, refinement and global scaling of our AI-native products.
•
Approximately 10.0%, or HK$381.8 million, of the net proceeds will be allocated to
working capital and general corporate purposes.
See “Future Plans” and “Use of Proceeds” for details.
DIVIDEND AND DIVIDEND POLICY
No dividend was paid or declared by us or any of our subsidiaries since our incorporation.
After the Track Record Period and up to the date of this Prospectus, we did not declare any
dividends to our Shareholders. As of the Latest Practicable Date, we did not have a formal
dividend policy or a fixed dividend distribution ratio. Any declaration and payment as well as
the amount of dividends will be subject to our Articles and the Cayman Companies Act. We
currently do not have any dividend policy to guide our dividends declaration or payments. Our
board of directors has the discretion to pay interim dividends and to recommend to
Shareholders to pay final dividends, and will depend on a number of factors, including our
earnings, capital requirements, overall financial condition and contractual restrictions. See
“Financial Information — Dividends.”
IMPACT OF THE COVID-19 PANDEMIC DURING THE TRACK RECORD PERIOD
COVID-19 did not have any material impact on the Group’s business, operation or
financial condition during the Track Record Period because the Group’s core business activities
are performed by distributed engineering teams and are inherently remote-compatible, its
products are provided online through cloud infrastructure rather than offline channels, and it
has limited reliance on physical supply chains or on-site deployment and did not experience
any material project delays, customer cancellations, revenue shortfalls or credit losses
attributable to the pandemic.
SUMMARY
– 30 –

<<<PAGE 41>>>
RECENT DEVELOPMENTS
As of the Latest Practicable Date, we had not experienced any material impact from
tariffs, export controls, or other trade-related measures imposed by governmental authorities in
the jurisdictions in which we operate. Although certain countries, including the United States,
have in recent periods introduced or adjusted tariffs and related policies on goods and
technologies, such measures have not had a material adverse effect on our operations, financial
condition or prospects to date. We continue to monitor relevant developments and assess their
potential implications for our business.
Our Directors confirm that, up to the date of this Prospectus, there has been no material
adverse change in our financial or trading position or prospects since September 30, 2025,
being the end date of the periods reported in the Accountant’s Report set out in Appendix I, and
there is no event since September 30, 2025 that would materially affect the information shown
in the Accountant’s Report set out in Appendix I.
We anticipate a significant increase in net loss for the year ended December 31, 2025,
primarily due to the expected R&D expenses as we continue to elevate the intelligence level
of our foundation models and fair value loss on financial liabilities, as the valuation of our
company is expected to increase in 2025.
RECENT REGULATORY DEVELOPMENT
Outbound Investment Rules
Effective on January 2, 2025, the final rule issued Treasury to implement the executive
order of August 9, 2023 (the “Final Rule”) imposes investment prohibition and notification
requirements on U.S. Persons for a wide range of investments in entities associated with China
(including Hong Kong and Macau) that are engaged in activities relating to three sectors: (i)
semiconductors and microelectronics, (ii) quantum information technologies, and (iii) AI
systems. U.S. persons subject to the Final Rule are prohibited from making, or required to
report, certain investments in covered foreign persons, which are defined as “covered
transactions,” and include acquisitions of equity interests (including contingent equity
interests), certain debt financing, joint ventures, and certain investments as a limited partner
in a non-U.S. person pooled investment fund. Since our principal place of business is in China
and we engage in the development of certain AI models, we are likely to be deemed as a
“covered foreign person” as described in the Final Rule. Based on information we provided to
our international sanctions advisor, it appears likely that some U.S. persons that purchase our
Shares in the Global Offering or are the parents of non-U.S. person subsidiaries that purchase
our Shares in the Global Offering would be required to file notifications regarding their or their
subsidiaries’ purchases with Treasury no later than 30 days after such purchases of the Shares.
See “Risk Factors — Risks Related to Our Business and Industry — We are subject to the risks
associated with international trade policies, geopolitics and trade protection measures. Changes
in international relationships, trade and investment policies, trade protection and investment
restriction measures may adversely impact our business, financial condition and results of
operations.”
SUMMARY
– 31 –

<<<PAGE 42>>>
Export Control Regulations
In recent years, the United States has expanded export controls restrictions on China
through the Export Administration Regulations (the “EAR”), administered by the Bureau of
Industry and Security of the United States Department of Commerce (the “BIS”). The United
States in recent years has placed an increasing number of entities, including a number of
entities in China, on the Entity List and other restricted or prohibited parties lists. In addition
to naming additional persons to these lists, BIS has imposed complex and restrictive rules
applicable to doing business with persons on them. For example, on September 29, 2025, the
BIS issued an immediately effective interim final rule that extended Entity List and Military
End-User List restrictions to entities that are 50% or more owned, directly or indirectly, by
shareholders on those lists. The U.S. Government has indicated that implementation of the
Affiliate Rule will be delayed for at least one year (i.e., until October 2026). These recent
measures together with the U.S. export control regime regulate the export, reexport and
transfer of U.S. products, software, and technology, including certain items manufactured
outside the United States that contain greater than de minimis controlled U.S. content or are
the foreign direct product of certain U.S. software or technology.
Tariff Regulations
We are also closely monitoring potential changes in tariff policy and assessing the
potential impact of such policy changes on our business operations and financial performance.
For example, recently, the United States proposed to impose multiple rounds of tariffs on a
wide range of goods imported from multiple countries, including China, and China responded
with retaliatory tariffs. As advised by our international legal advisor, U.S. import tariffs only
apply of export of physical goods to the United States. On such basis, it is of the view of our
Directors that, given that we do not export physical goods to the United States, U.S. tariffs are
unlikely to have a material adverse impact on our business operations and financial
performance. As relevant policies are rapidly evolving, it may be difficult to evaluate these
tariff measures’ potential future impacts. See “Risk Factors — Risks Related to Our Business
and Industry — We are subject to the risks associated with international trade policies,
geopolitics and trade protection measures. Changes in international relationships, trade and
investment policies, trade protection and investment restriction measures may adversely impact
our business, financial condition and results of operations.”
AI Chatbot Regulations
Several U.S. states, including California, New York, Maine, and Utah, have recently
enacted laws that specifically regulate AI-powered chatbots. These laws impose new
operational requirements, such as clear and recurring user disclosures, and mandate the
implementation of safety protocols to prevent harmful content, particularly related to
self-harm. For example, California’s law, effective January 2026, includes specific protections
for minors and establishes a private right of action allowing for statutory damages.
SUMMARY
– 32 –

<<<PAGE 43>>>
We are in the process of reviewing these regulations to ensure the continued compliance
of our Talkie application. Based on (i) an assessment of the current features and functionalities
of Talkie and (ii) research conducted on existing state legislation and regulations governing
chatbots, as advised by our U.S. data legal advisor, (a) the current features and design of Talkie
are already in material compliance with the chatbot laws currently in force in Utah, New York
and Maine; and (b) Talkie is not subject to the chatbot laws currently enacted in other U.S.
states, as such laws regulate functions that Talkie does not offer, such as the provision of
medical services.
Guided by legal advice from our U.S. data legal advisor, we are currently implementing
the updates necessary for compliance with the upcoming chatbot law in California. These
updates primarily involve reviewing our user interface, supplementing certain mandatory
disclosures and incorporating required safety features. Such updates are consistent with our
ordinary product-development cycle for Talkie and are expected to be completed within a
reasonable timeframe and at a reasonable cost. We are currently designing and implementing
these updates and expect to complete the process by the end of 2025, ahead of the California
chatbot law’s anticipated effective date in January 2026. Based on our planned timetable and
the progress made to date, as advised by our U.S. data legal advisor, Talkie is expected to be
in compliance with the requirements under the California chatbot law, once it is enacted in
January 2026.
In light of the abovementioned view of our U.S. data legal advisor, although compliance
with these state-level regulations may result in certain incremental operational costs, we do not
expect such regulations to have any material adverse effect on our business, results of
operations or financial condition. For further details regarding our AI safety and alignment
measures, safeguards against inappropriate or harmful outputs and user misuse, and our
ongoing efforts to ensure responsible AI development, please refer to the section headed
“Business — Research and Development.”
SUMMARY
– 33 –

<<<PAGE 44>>>
In this Prospectus, unless the context otherwise requires, the following terms shall
have the meanings set out below. Certain other terms are explained in the section headed
“Glossary of Technical Terms” in this Prospectus.
“Accountant’s Report”
the accountant’s report of our Company, the text of which
is set out in Appendix I to this Prospectus
“affiliate(s)”
with respect to any specified person, any other person,
directly or indirectly, controlling or controlled by or
under direct or indirect common control with such
specified person
“AFRC”
Accounting and Financial Reporting Council (會計及財
務匯報局)
“Alpha EXP”
Alpha EXP Limited, a business company incorporated in
the BVI on November 23, 2021, and one of our
Controlling Shareholders
“Articles” or “Articles of
Association”
the amended and restated articles of association of our
Company with effect upon the Listing Date (as amended
from time to time), a summary of which is set out in
Appendix III to this Prospectus
“associate(s)”
has the meaning ascribed thereto under the Listing Rules
“Audit Committee”
the audit committee of the Board
“Beijing Jizhi”
Beijing Xiyu Jizhi Technology Co., Ltd. (北京稀宇極智
科技有限公司) (formerly known as Mingri Zhimeng
(Beijing) Technology Co., Ltd. (名日之夢(北京)科技有限
公司)), a limited liability company established in the
PRC
on
November
18,
2021
and
a
wholly-owned
subsidiary of the Company
“Board”, “Board of Directors”
or “our Board”
the board of Directors of the Company
“Business Day”
a day on which banks in Hong Kong are generally open
for normal business to the public and which is not a
Saturday, Sunday or public holiday in Hong Kong
“BVI”
the British Virgin Islands
DEFINITIONS
– 34 –

<<<PAGE 136 起已省略：超出 share_structure 字符上限；请人工复核覆盖范围>>>



## 价格区间（T–U）

- `col_T` = Maximum Offer Price (type=number unit=HKD_per_share missing=NaN)
- `col_U` = Minimum Offer Price (type=number unit=HKD_per_share missing=NaN)

### 原文切片：价格区间（T–U）


<<<PAGE 1>>>
Stock Code : 0100
(A company controlled through weighted voting rights and 
incorporated in the Cayman Islands with limited liability)
MiniMax Group Inc.
GLOBAL 
OFFERING
Joint Sponsors, Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
(in alphabetical order)
(in alphabetical order)

<<<PAGE 2>>>
IMPORTANT: If you are in any doubt about any of the contents of this Prospectus, you should seek independent professional advice.
MiniMax Group Inc.
(A company controlled through weighted voting rights and incorporated in the Cayman Islands with limited liability)
GLOBAL OFFERING
Number of Offer Shares under
the Global Offering
:
25,389,220 Offer Shares (subject to the
Offer Size Adjustment Option and the
Over-allotment Option)
Number of Hong Kong Offer Shares
:
1,269,480 Offer Shares (subject to
reallocation)
Number of International Offer Shares
:
24,119,740 Offer Shares (subject to
reallocation, the Offer Size Adjustment
Option and the Over-allotment Option)
Maximum Offer Price
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this Prospectus, make no
representation as to its accuracy or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the contents of this Prospectus.
A copy of this Prospectus, having attached thereto the documents specified in the section headed “Appendix V — Documents Delivered to the Registrar of Companies in Hong Kong and Available on Display”, has been
registered by the Registrar of Companies in Hong Kong as required by section 342C of the Companies (Winding Up and Miscellaneous Provisions) Ordinance (Chapter 32 of the Laws of Hong Kong). The Securities
and Futures Commission and the Registrar of Companies in Hong Kong take no responsibility for the contents of this Prospectus or any other document referred to above.
The final Offer Price is expected to be fixed by agreement between the Overall Coordinators (for themselves and on behalf of the Underwriters) and the Company on the Price Determination Date, which is expected
to be on or around Wednesday, January 7, 2026. The Offer Price will be not more than HK$165.00 per Offer Share and is currently expected to be not less than HK$151.00 per Offer Share unless otherwise announced.
If, for any reason, the final Offer Price is not agreed by 12:00 noon on Wednesday, January 7, 2026 between the Overall Coordinators (for themselves and on behalf of the Underwriters) and the Company, the Global
Offering will not proceed and will lapse.
The Offer Shares have not been and will not be registered under the U.S. Securities Act or any state securities laws of the United States and may not be offered, sold, pledged, or transferred within the United States,
except that Offer Shares may be offered, sold or delivered (a) in the United States solely to QIBs in reliance on Rule 144A or another exemption from, or in a transaction not subject to, the registration requirements
of the U.S. Securities Act; or (b) outside the United States in offshore transactions in reliance on Regulation S.
Applicants for Hong Kong Offer Shares may be required to pay, on application (subject to application channels), the Offer Price of HK$165.00 for each Hong Kong Offer Share together with a brokerage fee of 1%, a
SFC transaction levy of 0.0027%, Stock Exchange trading fee of 0.00565% and AFRC transaction levy of 0.00015%.
Prior to making an investment decision, prospective investors should consider carefully all of the information set out in this Prospectus, including the risk factors set out in the section headed “Risk Factors”.
The obligations of the Hong Kong Underwriters under the Hong Kong Underwriting Agreement are subject to termination by the Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) if
certain grounds arise prior to 8:00 a.m. on the Listing Date. See “Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination”.
Our Company is a Specialist Technology Company (as defined in Chapter 18C of the Listing Rules). The securities of Specialist Technology Companies carry high investment risks including risks of share price volatility
and inflated valuation due to the difficulty in valuing such companies. Investors should fully understand the investment risks of a Specialist Technology Company and the risks disclosed by our Company before making
their investment decisions. In addition, our Company is a Pre-Commercial Company (as defined in Chapter 18C of the Listing Rules). Pre-Commercial Companies are Specialist Technology Companies that cannot meet
the revenue requirement as set out in Rule 18C.03(4) of the Listing Rules, and so are subject to a higher risk of corporate failure if they are unable to secure sufficient external funding and/or cannot generate sufficient
revenue to sustain their operations after listing.
Our Company will be controlled through weighted voting rights upon Listing. Prospective investors should be aware of the potential risks of investing in a company with a WVR structure, in particular that the WVR
Beneficiary, whose interests may not necessarily be aligned with those of our Shareholders as a whole, will be in a position to exert significant influence over the outcome of our Shareholders’ resolutions, irrespective
of how other Shareholders vote. For further information about the risks associated with the WVR structure, see “Risk Factors — Risks Related to the WVR Structure”. Prospective investors should make the decision
to in our Company only after due and careful consideration.
ATTENTION
We have adopted a fully electronic application process for the Hong Kong Public Offering. We will not provide printed copies of this prospectus to the public in relation to the Hong Kong Public Offering.
This prospectus is available at the website of the Stock Exchange at www.hkexnews.hk and our website at https://www.minimaxi.com. If you require a printed copy of this prospectus, you may download
and print from the website addresses above.
IMPORTANT
December 31, 2025

<<<PAGE 3>>>
IMPORTANT NOTICE TO INVESTORS OF HONG KONG OFFER SHARES
FULLY ELECTRONIC APPLICATION PROCESS
The Company has adopted a fully electronic application process for the Hong Kong
Public Offering.
This prospectus is available at the website of the Stock Exchange at www.hkexnews.hk
under the “HKEXnews > New Listings > New Listing Information” section, and our website at
https://www.minimaxi.com.
The Company will not provide any physical channels to accept any application for the
Hong Kong Offer Shares by the public. The contents of the electronic version of this prospectus
are identical to the prospectus as registered with the Registrar of Companies in Hong Kong
pursuant to section 342C of the Companies (Winding Up and Miscellaneous Provisions)
Ordinance.
To apply for the Hong Kong Offer Shares, you may:
(1)
apply online through the HK eIPO White Form service at www.hkeipo.hk; or
(2)
apply electronically through the HKSCC EIPO channel and cause HKSCC
Nominees to apply on your behalf by instructing your broker or custodian who is a
HKSCC Participant to give electronic application instructions via HKSCC’s FINI
system to apply for the Hong Kong Offer Shares on your behalf.
If you are an intermediary, broker or agent, please remind your customers, clients or
principals, as applicable, that this prospectus is available online at the website addresses stated
above. Please refer to the section headed “How to Apply for Hong Kong Offer Shares” in this
prospectus for further details of the procedures through which you can apply for the Hong
Kong Offer Shares.
Your application through the HK eIPO White Form service or the HKSCC EIPO
channel must be for a minimum of 20 Hong Kong Offer Shares and in one of the numbers set
out in the table.
If you are applying through the HK eIPO White Form service, you may refer to the table
below for the amount payable for the number of Hong Kong Offer Shares you have selected.
You must pay the respective maximum amount payable on application in full upon application
for Hong Kong Offer Shares.
IMPORTANT
– ii –

<<<PAGE 4>>>
If you are applying through the HKSCC EIPO channel, you are required to pre-fund your
application based on the amount specified by your broker or custodian, as determined based on
the applicable laws and regulations in Hong Kong.
No. of
Hong Kong
Offer Shares
applied for
Maximum
Amount
payable(2) on
application/
successful
allotment
No. of
Hong Kong
Offer Shares
applied for
Maximum
Amount
payable(2) on
application/
successful
allotment
No. of
Hong Kong
Offer Shares
applied for
Maximum
Amount
payable(2) on
application/
successful
allotment
No. of
Hong Kong
Offer Shares
applied for
Maximum
Amount
payable(2) on
application/
successful
allotment
HK$
HK$
HK$
HK$
20
3,333.28
400
66,665.61
6,000
999,984.16
80,000
13,333,122.00
40
6,666.56
500
83,332.01
7,000
1,166,648.18
90,000
14,999,762.26
60
9,999.84
600
99,998.41
8,000
1,333,312.20
100,000
16,666,402.50
80
13,333.13
700
116,664.82
9,000
1,499,976.23
200,000
33,332,805.00
100
16,666.40
800
133,331.22
10,000
1,666,640.26
300,000
49,999,207.50
120
19,999.68
900
149,997.62
20,000
3,333,280.50
400,000
66,665,610.00
140
23,332.96
1,000
166,664.03
30,000
4,999,920.76
500,000
83,332,012.50
160
26,666.24
2,000
333,328.06
40,000
6,666,561.00
634,740(1)
105,788,323.23
180
29,999.52
3,000
499,992.08
50,000
8,333,201.26
200
33,332.80
4,000
666,656.10
60,000
9,999,841.50
300
49,999.21
5,000
833,320.13
70,000
11,666,481.76
(1)
Maximum number of Hong Kong Offer Shares you may apply for and this is 50% of the Hong Kong Offer
Shares initially offered.
(2)
The amount payable is inclusive of brokerage, SFC transaction levy, the Stock Exchange trading fee and AFRC
transaction levy. If your application is successful, brokerage will be paid to the Exchange Participants (as
defined in the Listing Rules) or to the HK eIPO White Form Service Provider (for applications made through
the application channel of the HK eIPO White Form service) while the SFC transaction levy, the Stock
Exchange trading fee and the AFRC transaction levy will be paid to the SFC, the Stock Exchange and the
AFRC, respectively.
IMPORTANT
– iii –

<<<PAGE 5>>>
If there is any change in the following expected timetable, we will issue an
announcement
to
be
published
on
the
websites
of
the
Company
at
https://www.minimaxi.com and the Stock Exchange at www.hkexnews.hk.
Date(1)
Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on
Wednesday, December 31, 2025
Latest time for completing electronic applications under
HK eIPO White Form service through the designated website
at www.hkeipo.hk(2)
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .11:30 a.m. on
Tuesday, January 6, 2026
Application lists open(3)
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .11:45 a.m. on
Tuesday, January 6, 2026
Latest time for (a) completing payment for
HK eIPO White Form applications by effecting
internet banking transfer(s) or PPS payment
transfer(s) and (b) giving electronic application
instructions to HKSCC(4) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .12:00 noon on
Tuesday, January 6, 2026
If you are instructing your broker or custodian who is a HKSCC Participant to submit
an EIPO application on your behalf through HKSCC’s FINI system in accordance with your
instruction to apply for the Hong Kong Offer Shares, you are advised to contact your broker
or custodian for the earliest and latest time for giving such instructions, as this may vary by
broker or custodian.
Application lists close(3) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .12:00 noon on
Tuesday, January 6, 2026
Expected Price Determination Date(5) . . . . . . . . . . . . . . . . . . . . . . on or before 12:00 noon,
Wednesday, January 7, 2026
(1)
Announcement of the Offer Price, the level of
indication of interest in the International Offering,
the level of applications in the Hong Kong
Public Offering and the basis of allocation of the
Hong Kong Offer Shares under the Hong Kong
Public Offering to be published of the website
of Hong Kong Stock Exchange at www.hkexnews.hk
and the Company’s website at
https://www.minimaxi.com(6) on or before(10)
. . . . . . . . . . . . . . . . . . . .11:00 p.m. on
Thursday, January 8, 2026
EXPECTED TIMETABLE(1)
– iv –

<<<PAGE 6>>>
(2)
Results of allocations in the Hong Kong
Public Offering (with successful applicants’
identification document or business registration
numbers, where appropriate) to be available
through a variety of channels, including:
•
in the announcement to be published on
the website of the Hong Kong Stock Exchange
at www.hkexnews.hk and on the Company’s
website at https://www.minimaxi.com, at or before . . . . . . . . . . . .11:00 p.m. on
Thursday, January 8, 2026
•
from the “Allotment Results” page in the
designated results of allocations website
at www.hkeipo.hk/IPOResult
(or www.tricor.com.hk/ipo/result) from . . . . . . . . . . . . . . . . . . . . .11:00 p.m. on
Thursday, January 8, 2026
to 12:00 midnight on
Wednesday, January 14, 2026
•
from the allocation results telephone
enquiry line by calling +852 3691 8488
between 9:00 a.m. and 6:00 p.m. from . . . . . . . . . . . . . . .Friday, January 9, 2026
to Wednesday, January 14, 2026
(except Saturday, Sunday
and public holiday
in Hong Kong)
Share certificates in respect of wholly or
partially successful applications to be dispatched
or deposited into CCASS on or before(7) . . . . . . . . . . . . . . . . . Thursday, January 8, 2026
HK eIPO White Form e-Auto Refund payment
instructions/refund checks in respect of (i) wholly or
partially successful applications if the final Offer
Price is less than the price payable on application
(if applicable) and (ii) wholly or partially
unsuccessful applications under the Hong Kong
Public Offering to be dispatched on or before(8)(9)
. . . . . . . . . . . Friday, January 9, 2026
Dealings in the Class A Ordinary Shares on the Hong Kong Stock
Exchange expected to commence at 9:00 a.m. on . . . . . . . . . . . . .Friday, January 9, 2026
EXPECTED TIMETABLE(1)
– v –

<<<PAGE 517>>>
Underwriters may be asked to demonstrate compliance with their obligations under the Code,
and may request other CMIs (including private banks) to provide evidence showing compliance
with the obligations above (in particular, that the necessary consents have been obtained). In
such event, other CMIs (including private banks) are required to provide the relevant
Underwriter with such evidence within the timeline requested.
Important Notice to Prospective Investors
Prospective investors should be aware that certain intermediaries in the context of this
offering of the Offer Shares, including certain Underwriters, are CMIs subject to Paragraph 21
of the Code. This notice to prospective investors is a summary of certain obligations the Code
imposes on such CMIs, which require the attention and cooperation of prospective investors.
Certain CMIs may also be acting as the Overall Coordinators for this offering and is subject
to additional requirements under the Code.
Prospective investors who are the directors, employees or major shareholders of the
Company, a CMI or its group companies would be considered under the Code as having an
Association with the Company, the CMI or the relevant group company (as the case may be).
Prospective investors associated with the Company or any CMI (including its group
companies) should specifically disclose this when placing an order for the Offer Shares and
should disclose, at the same time, if such orders may negatively impact the price discovery
process in relation to this offering. Prospective investors who do not disclose their Associations
are hereby deemed not to be so associated. Where prospective investors disclose their
Associations but do not disclose that such order may negatively impact the price discovery
process in relation to this offering, such order is hereby deemed not to negatively impact the
price discovery process in relation to this offering.
Prospective investors to whom the allocation of Offer Shares will be subject to
restrictions or require prior consent from the Stock Exchange under the Stock Exchange
Requirements (e.g. a connected person of a listed issuer) would be considered as “Restricted
Investors”. Offer Shares may only be allocated to Restricted Investors in accordance with
applicable Stock Exchange Requirements. Prospective investors who are Restricted Investors
should specifically disclose whether they are Restricted Investors when placing an order for the
Offer Shares. Prospective investors who do not disclose they are Restricted Investors are
hereby deemed not to be Restricted Investors.
Prospective investors should ensure, and by placing an order prospective investors are
deemed to confirm, that orders placed are bona fide, are not inflated and do not constitute
duplicated orders (i.e. two or more corresponding or identical orders placed via two or more
CMIs). If a prospective investor is an asset management arm affiliated with any Underwriter,
such prospective investor should indicate when placing an order if it is for a fund or portfolio
where the Underwriter or its group company has more than 50% interest, in which case it will
be classified as a “proprietary order” and subject to appropriate handling by CMIs in
accordance with the Code and should disclose, at the same time, if such “proprietary order”
may negatively impact the price discovery process in relation to this offering. Prospective
STRUCTURE OF THE GLOBAL OFFERING
– 507 –

<<<PAGE 518>>>
investors who do not indicate this information when placing an order are hereby deemed to
confirm that their order is not such a “proprietary order”. If a prospective investor is otherwise
affiliated with any Underwriter, such that its order may be considered to be a “proprietary
order” (pursuant to the Code), such prospective investor should indicate to the relevant
Underwriter when placing such order and such orders will be subject to applicable
requirements in accordance with the Code. Prospective investors who do not indicate this
information when placing an order are hereby deemed to confirm that their order is not such
a “proprietary order”. Where prospective investors disclose such information but do not
disclose that such “proprietary order” may negatively impact the price discovery process in
relation to this offering, such “proprietary order” is hereby deemed not to negatively impact the
price discovery process in relation to this offering.
Prospective investors should be aware that certain information may be disclosed by CMIs
(including private banks) which is personal and/or confidential in nature to the prospective
investor. By placing an order, prospective investors are deemed to have understood and
consented to the collection, disclosure, use and transfer of such information by the
Underwriters and/or any other third parties as may be required by the Code, including to the
Company, the Overall Coordinators, relevant regulators and/or any other third parties as may
be required by the Code, it being understood and agreed that such information shall only be
used for the purpose of complying with the Code, during the book-building process for this
offering. Failure to provide such information may result in that order being rejected.
STRUCTURE OF THE GLOBAL OFFERING
– 508 –

<<<PAGE 519>>>
IMPORTANT NOTICE TO INVESTORS
OF HONG KONG OFFER SHARES
FULLY ELECTRONIC APPLICATION PROCESS
The Company has adopted a fully electronic application process for the Hong
Kong Public Offering and below are the procedures for application.
This prospectus is available at the website of the Stock Exchange at
www.hkexnews.hk under the “HKEXnews > New Listings > New Listing Information”
section, and the Company’s website at https://www.minimaxi.com.
The contents of this prospectus are identical to the prospectus as registered with the
Registrar of Companies in Hong Kong pursuant to Section 342C of the Companies
(Winding Up and Miscellaneous Provisions) Ordinance.
A.
APPLICATION FOR HONG KONG OFFER SHARES
1.
Who Can Apply
You can apply for Hong Kong Offer Shares if you or the person(s) for whose benefit you
are applying for:
•
are 18 years of age or older; and
•
have a Hong Kong address (for the HK eIPO White Form service only); and
•
are outside the United States (within the meaning of Regulation S) or are a person
described in paragraph (h)(3) of Rule 902 of Regulation S.
Unless permitted by the Listing Rules or a waiver and/or consent has been granted by the
Stock Exchange to the Company, you cannot apply for any Hong Kong Offer Shares if you or
the person(s) for whose benefit you are applying for:
•
are an existing Shareholder;
•
are a Director or chief executive of the Company and/or a director or chief executive
of any of its subsidiaries;
•
are a close associate (as defined in the Listing Rules) of any of the above persons;
•
are a connected person (as defined in the Listing Rules) of the Company or will
become a connected person of the Company immediately upon the completion of the
Global Offering; or
•
have been allocated or have applied for or indicated an interest in any International
Offer Shares or otherwise participate in the International Offering.
HOW TO APPLY FOR HONG KONG OFFER SHARES
– 509 –

<<<PAGE 520>>>
2.
Application Channels
The Hong Kong Public Offering period will begin at 9:00 a.m. on Wednesday, December
31, 2025 and end at 12:00 noon on Tuesday, January 6, 2026 (Hong Kong time).
To apply for Hong Kong Offer Shares, you may use one of the following application
channels:
Application
Channel
Platform
Target Investors
Application Time
HK eIPO White
Form service 
www.hkeipo.hk
Applicants who would like
to
receive
a
physical
Share certificate. Hong
Kong
Offer
Shares
successfully applied for
will
be
allotted
and
issued in your own name.
From
9:00
a.m.
on
Wednesday,
December
31, 2025 until 11:30 a.m.
on Tuesday, January 6,
2026, Hong Kong time.
The
latest
time
for
completing full payment
of
application
monies
in
respect
of
such
applications
will
be
12:00 noon on Tuesday,
January 6, 2026, Hong
Kong time.
HKSCC EIPO
channel    
Your broker or custodian who is a
HKSCC Participant will submit an
EIPO application on your behalf
through HKSCC’s FINI system in
accordance with your instruction
Applicants who would not
like to receive a physical
Share certificate. Hong
Kong
Offer
Shares
successfully applied for
will
be
allotted
and
issued in the name of
HKSCC
Nominees,
deposited directly into
CCASS and credited to
your designated HKSCC
Participant’s
stock
account.
Contact
your
broker
or
custodian for the earliest
and latest time for giving
such instructions, as this
may vary by broker or
custodian.
The HK eIPO White Form service and the HKSCC EIPO channel are facilities subject
to capacity limitations and potential service interruptions and you are advised not to wait until
the last day of the application period to apply for Hong Kong Offer Shares.
HOW TO APPLY FOR HONG KONG OFFER SHARES
– 510 –

<<<PAGE 521 起已省略：超出 price 字符上限；请人工复核覆盖范围>>>



## 上市前三年财务（V–AN）

- `col_V` = currency in financial information (type=text unit=currency_code missing=NA)
- `col_W` = total assets in year-3 (3 years before IPO) (type=number unit=basic_currency_units missing=NaN period=year-3 annualize=False)
- `col_X` = total assets in year-2 (type=number unit=basic_currency_units missing=NaN period=year-2 annualize=False)
- `col_Y` = total assets in year-1 (type=number unit=basic_currency_units missing=NaN period=year-1 annualize=sales_profit_only_if_partial)
- `col_Z` = total equity in year-3 (type=number unit=basic_currency_units missing=NaN period=year-3 annualize=False)
- `col_AA` = total equity in year-2 (type=number unit=basic_currency_units missing=NaN period=year-2 annualize=False)
- `col_AB` = total equity in year-1 (type=number unit=basic_currency_units missing=NaN period=year-1 annualize=sales_profit_only_if_partial)
- `col_AC` = total liability in year-3 (type=number unit=basic_currency_units missing=NaN period=year-3 annualize=False)
- `col_AD` = total liability in year-2 (type=number unit=basic_currency_units missing=NaN period=year-2 annualize=False)
- `col_AE` = total liability in year-1 (type=number unit=basic_currency_units missing=NaN period=year-1 annualize=sales_profit_only_if_partial)
- `col_AF` = Net sales in year-3 (type=number unit=basic_currency_units missing=NaN period=year-3 annualize=False)
- `col_AG` = Net sales in year-2 (type=number unit=basic_currency_units missing=NaN period=year-2 annualize=False)
- `col_AH` = Net sales in year-1 (type=number unit=basic_currency_units missing=NaN period=year-1 annualize=sales_profit_only_if_partial)
- `col_AI` = Profit before tax in year-3 (type=number unit=basic_currency_units missing=NaN period=year-3 annualize=False)
- `col_AJ` = Profit before tax in year-2 (type=number unit=basic_currency_units missing=NaN period=year-2 annualize=False)
- `col_AK` = Profit before tax in year-1 (type=number unit=basic_currency_units missing=NaN period=year-1 annualize=sales_profit_only_if_partial)
- `col_AL` = Profit for the year in year-3 (type=number unit=basic_currency_units missing=NaN period=year-3 annualize=False)
- `col_AM` = Profit for the year in year-2 (type=number unit=basic_currency_units missing=NaN period=year-2 annualize=False)
- `col_AN` = Profit for the year in year-1 (type=number unit=basic_currency_units missing=NaN period=year-1 annualize=sales_profit_only_if_partial)
- `col_BE` = Interest-bearing debt at year-1 end (type=number unit=HKD missing=NaN)
- `col_BT` = Accounting standard (type=text unit=text missing=NA)
- `col_CF` = Gross profit in year-1 (type=number unit=money missing=NaN)
- `col_CG` = Capital expenditure in year-1 (type=number unit=money missing=NaN)
- `col_CH` = Audit opinion (year-1) (type=text unit=text missing=NA)

### 原文切片：上市前三年财务（V–AN）


<<<PAGE 28>>>
OUR CONTROLLING SHAREHOLDERS
Immediately following the completion of the Global Offering (assuming the Offer Size
Adjustment Option and the Over-allotment Option are not exercised), an aggregate of
5,000,000 Class A Ordinary Shares and 74,102,534 Class B Ordinary Shares, representing
approximately (i) 72.05% of the voting rights in our issued share capital in general meetings
(except for resolutions with respect to the Reserved Matters), and (ii) 25.90% of the voting
rights in our issued share capital in general meetings for resolutions with respect to the
Reserved Matters, will be held by MiniMax Awakening, MiniMax Limited and Alpha EXP as
well as MiniMax Matrix. MiniMax Awakening and MiniMax Limited are wholly owned by Dr.
Yan through Local Linearity. MiniMax Matrix is also a controlled entity of Dr. Yan through
Local Linearity. Alpha EXP is held by Scaling EXP Limited as to 99% and Local Linearity as
to 1%. Scaling EXP Limited is wholly-owned by Trident Trust Company (Hong Kong) Limited,
which acts as the trustee of Alpha EXP Trust. Alpha EXP Trust is a trust established by Dr. Yan
(as settlor) for the benefit of himself. Accordingly, Dr. Yan, Local Linearity Inc., MiniMax
Awakening, MiniMax Limited, Alpha EXP, Scaling EXP Limited, and MiniMax Matrix
together will constitute as a group of Controlling Shareholders of our Company after the
Listing.
PRE-IPO INVESTMENTS
We have undertaken several rounds of Pre-IPO Investments. For details of the background
of our key Pre-IPO Investors and the principal terms of the Pre-IPO Investments, see “History,
Reorganization and Corporate Structure — Pre-IPO Investments.”
LOCK-UP REQUIREMENTS UNDER RULE 18C.14 OF THE LISTING RULES
Dr. Yan, Ms. Yun and their close associates as well as our Pathfinder SIIs will be subject
to lock-up requirements pursuant to Rule 18C.14 of the Listing Rules. For details, see the
section headed “History, Reorganization and Corporate Structure — Lock-up Periods”. Upon
the Company’s application and the notification by the Stock Exchange that our Company will
no longer be regarded as a Pre-Commercial Company after the Listing, the lock-up period will
expire on the later of: (i) the date on which such lock-up periods would have ended if the
Company had applied for listing as a Commercial Company; and (2) the date falling on the 30th
day after the announcement on the removal of designation as a Pre-Commercial Company as
required under Rule 18C.24 of the Listing Rules.
SUMMARY OF HISTORICAL FINANCIAL INFORMATION
The following tables set forth summary financial data from our consolidated financial
information for the Track Record Period, extracted from the Accountants’ Report set out in
Appendix I. You should read this summary in conjunction with our consolidated financial
information included in the Accountants’ Report set out in Appendix I, including the
accompanying notes, and the information set forth in “Financial Information.”
SUMMARY
– 18 –

<<<PAGE 29>>>
Summary of Consolidated Statements of Profit or Loss
The following table sets forth a summary of our consolidated statements of profit or loss,
in absolute amounts and as a percentage of our total revenue, for the periods indicated. See
“Financial Information” for details.
For the year ended December 31,
For the nine months ended
September 30,
2022
2023
2024
2024
2025
US$
%
US$
%
US$
%
US$
%
US$
%
(unaudited)
(in thousands, except for percentages)
Revenue          
–
–
3,460
100.0
30,523
100.0
19,454
100.0
53,437
100.0
Cost of sales
      
–
–
(4,314)
(124.7)
(26,785)
(87.8)
(18,944)
(97.4)
(40,961)
(76.7)
Gross (loss)/profit
   
–
–
(854)
(24.7)
3,738
12.2
510
2.6
12,476
23.3
Other income and gains,
net
          
1,155
–
8,942
258.4
36,151
118.4
25,278
129.9
31,232
58.4
Selling and distribution
expenses
       
(587)
–
(22,827)
(659.7)
(86,995)
(285.0)
(53,389)
(274.4)
(39,325)
(73.6)
Administrative expenses  
(3,213)
–
(7,615)
(220.1)
(14,384)
(47.1)
(9,610)
(49.4)
(22,074)
(41.3)
Research and development
expenses
       
(10,560)
–
(70,002) (2,023.2) (188,979)
(619.1) (138,684)
(712.9) (180,312)
(337.4)
Fair value loss on financial
liabilities        
(60,509)
–
(176,826)
(5,110.6) (214,172)
(701.7) (128,063)
(658.3) (313,477)
(586.6)
Finance costs       
(14)
–
(61)
(1.8)
(509)
(1.7)
(316)
(1.6)
(511)
(1.0)
Impairment losses on
financial assets, net   
–
–
(3)
(0.1)
(88)
(0.3)
(68)
(0.3)
(22)
(0.0)
Loss before tax      
(73,728)
–
(269,246) (7,781.7) (465,238) (1,524.2) (304,342) (1,564.4) (512,013)
(958.2)
Income tax expense    
–
–
–
–
–
–
–
–
–
–
Loss for the year/period 
(73,728)
–
(269,246) (7,781.7) (465,238) (1,524.2) (304,342) (1,564.4) (512,013)
(958.2)
Attributable to:
Owners of the parent
  
(73,728)
–
(269,246) (7,781.7) (465,238) (1,524.2) (304,342) (1,564.4) (512,013)
(958.2)
Non-controlling interests

–
–
–
–
–
–
–
–
–
–
Loss and total
comprehensive income
for the year
     
(73,728)
–
(269,246) (7,781.7) (465,238) (1,524.2) (304,342) (1,564.4) (512,013)
(958.2)
Loss per share
attributable to ordinary
equity holders of the
parent
Basic and diluted
–For loss for the
year/period (US$)    
(0.74)
(2.56)
(4.28)
(2.80)
(4.71)
SUMMARY
– 19 –

<<<PAGE 30>>>
Non-IFRS Financial Measure
We use adjusted net loss (non-IFRS measure), which is a non-IFRS financial measure, in
evaluating our operating results and for financial and operational decision-making purposes.
We believe that adjusted net loss (non-IFRS measure) helps identify underlying trends in our
business that could otherwise be distorted by the effect of certain expenses that we include in
our net loss. We believe that adjusted net loss (non-IFRS measure) provides useful information
about our results of operations, enhances the overall understanding of our past performance and
future prospects and allows for greater visibility with respect to key metrics used by our
management in its financial and operational decision-making.
Adjusted net loss (non-IFRS measure) should not be considered in isolation or construed
as an alternative to net loss or any other measure of performance or as an indicator of our
operating performance. Investors are encouraged to review adjusted net loss (non-IFRS
measure) and the reconciliation to its most directly comparable IFRS measure. Adjusted net
loss (non-IFRS measure) presented here may not be comparable to similarly titled measures
presented by other companies. Other companies may calculate similarly titled measures
differently, limiting their usefulness as comparative measures to our data. We encourage
investors and others to review our financial information in its entirety and not rely on a single
financial measure.
We define our adjusted net loss (non-IFRS measure) as net loss adjusted by adding back
(i) share-based payment expenses that are included in cost of sales, general administrative,
research and development, and sales and marketing expenses, relates to the share-based awards
that we grant to participants of our share incentive schemes and is a non-cash expense, (ii) fair
value losses on financial liabilities, comprising fair value changes of convertible redeemable
preferred shares which will be re-designated from liabilities to equity as a result of the
automatic conversion into ordinary shares upon Listing, and convertible bonds, which have
subsequently been repaid in full as of the Latest Practicable Date, and (iii) listing expenses.
The following table presents our non-IFRS financial measure for the years ended
December 31, 2022, 2023, 2024 and the nine months ended September 30, 2024 and 2025. See
“Financial Information — Non-IFRS Financial Measure” for details.
For the year ended
December 31,
For the nine months
ended September 30,
2022
2023
2024
2024
2025
US$
US$
US$
US$
US$
(unaudited)
(in thousands)
Net loss for the year/period          
(73,728)
(269,246)
(465,238)
(304,342)
(512,013)
Add:
Share-based payment expenses         
1,069
3,346
6,823
6,100
8,581
Fair value loss on financial liabilities     
60,509
176,826
214,172
128,063
313,477
Listing expenses                 
–
–
–
–
3,675
Adjusted net loss for the year/period (non-
IFRS measure)                
(12,150)
(89,074)
(244,243)
(170,179)
(186,280)
SUMMARY
– 20 –

<<<PAGE 31>>>
We recorded US$73.7 million, US$269.2 million, US$465.2 million, US$304.3 million
and US$512.0 million in loss for the year/period in 2022, 2023, 2024 and for the nine months
ended September 30, 2024 and 2025, respectively, due to significant initial investment in
foundation model R&D and AI infrastructure and fair value loss on financial liabilities.
Summary of Consolidated Statements of Financial Position
The table below sets forth selected information from our consolidated statements of
financial position as of the dates indicated, which has been extracted from our consolidated
financial statements included in Appendix I to this Prospectus.
As of December 31,
As of
September 30,
2022
2023
2024
2025
(US$ in thousands)
NON-CURRENT ASSETS
Property, plant and
equipment            
231
709
1,093
1,134
Right-of-use assets       
458
3,313
3,077
2,746
Prepayments, other
receivables and other
assets                
–
435
561
731
Financial assets at fair value
through profit or loss    
–
–
95,331
70,228
Financial assets at fair value
through other
comprehensive income   
–
–
4,836
6,440
Restricted cash          
–
39
38
41
Total non-current assets  
689
4,496
104,936
81,320
CURRENT ASSETS
Trade receivables        
–
1,338
6,982
8,063
Prepayments, other
receivables and other
assets                
569
4,378
13,470
11,811
Financial assets at amortised
costs                
–
–
147,444
–
Financial assets at fair value
through profit or loss    
65,791
15,802
295,220
644,154
Time deposits           
–
91,698
26,327
–
Restricted cash          
2,221
–
27,293
25,097
Cash and cash equivalents  
4,691
206,295
288,912
362,647
SUMMARY
– 21 –

<<<PAGE 32>>>
As of December 31,
As of
September 30,
2022
2023
2024
2025
(US$ in thousands)
Total current assets      
73,272
319,511
805,648
1,051,772
CURRENT LIABILITIES
Interest-bearing bank
borrowings           
–
–
19,455
19,102
Trade and bills payables   
2,394
17,242
51,212
70,219
Other payables, accruals and
other liabilities        
2,326
14,741
51,512
17,322
Contract liabilities        
–
559
1,553
4,657
Lease liabilities          
349
1,248
1,964
1,694
Convertible redeemable
preferred shares        
145,175
629,001
1,581,949
2,321,193
Total current liabilities   
150,244
662,791
1,707,645
2,434,187
NET CURRENT
LIABILITIES        
(76,972)
(343,280)
(901,997)
(1,382,415)
TOTAL ASSETS LESS
CURRENT
LIABILITIES        
(76,283)
(338,784)
(797,061)
(1,301,095)
NON-CURRENT
LIABILITIES
Lease liabilities          
91
1,912
1,059
937
Other non-current liabilities
–
1,218
1,200
1,467
Total non-current
liabilities             
91
3,130
2,259
2,404
Net liabilities           
(76,374)
(341,914)
(799,320)
(1,303,499)
Our net current liabilities increased from US$77.0 million as of December 31, 2022 to
US$343.3 million as of December 31, 2023, primarily due to (i) an increase in convertible
redeemable preferred shares from US$145.2 million as of December 31, 2022 to US$629.0
million as of December 31, 2023, (ii) a decrease in financial assets at fair value through profit
or loss from US$65.8 million as of December 31, 2022 to US$15.8 million as of December 31,
2023, (iii) an increase in trade and bills payables from US$2.4 million as of December 31, 2022
to US$17.2 million as of December 31, 2023, and (iv) an increase in other payables, accruals
and other liabilities from US$2.3 million as of December 31, 2022 to US$14.7 million as of
December 31, 2023, partially offset by (i) an increase in cash and cash equivalents from
US$4.7 million as of December 31, 2022 to US$206.3 million as of December 31, 2023, and
(ii) the recognition of time deposits of US$91.7 million.
SUMMARY
– 22 –

<<<PAGE 33>>>
Our net current liabilities increased from US$343.3 million as of December 31, 2023 to
US$902.0 million as of December 31, 2024, primarily due to (i) an increase in convertible
redeemable preferred shares from US$629.0 million as of December 31, 2023 to US$1,581.9
million as of December 31, 2024, (ii) an increase in trade and bills payables from US$17.2
million as of December 31, 2023 to US$51.2 million as of December 31, 2024, and (iii) an
increase in other payables, accruals and other liabilities from US$14.7 million as of December
31, 2023 to US$51.5 million as of December 31, 2024. This was partially offset by (i) an
increase in financial assets at fair value through profit or loss from US$15.8 million as of
December 31, 2023 to US$295.2 million as of December 31, 2024, and (ii) an increase in
financial assets at amortized costs from nil as of December 31, 2023 to US$147.4 million as
of December 31, 2024.
Our net current liabilities increased from US$902.0 million as of December 31, 2024 to
US$1,382.4 million as of September 30, 2025, primarily due to (i) an increase in convertible
redeemable preferred shares from US$1,581.9 million as December 31, 2024 to US$2,321.2
million as of September 30, 2025, and (ii) a decrease in financial assets at amortized cost from
US$147.4 million as of December 31, 2024 to nil as of September 30, 2025, and (iii) an
increase in trade and bills payables from US$51.2 million as of December 31, 2024 to US$70.2
million as of September 30, 2025. This was partially offset by (i) an increase in financial assets
at fair value through profit or loss from US$295.2 million as of December 31, 2024 to
US$644.2 million as of September 30, 2025, and (ii) a decrease in other payables, accruals and
other liabilities from US$51.5 million as of December 31, 2024 to US$17.3 million as of
September 30, 2025.
We had net liabilities of US$76.4 million, US$341.9 million, US$799.3 million and
US$1,303.5 million as of December 31, 2022, 2023, 2024 and September 30, 2025,
respectively.
As of September 30, 2025, we had net liabilities of US$1,303.5 million primarily because
of convertible redeemable preferred shares totaling US$2,321.2 million. Nevertheless, as these
convertible redeemable preferred shares will be re-designated from financial liabilities to
equity as a result of the automatic conversion into ordinary shares upon Listing, our net
liabilities position will turn into a net assets position.
Our net liabilities increased from US$76.4 million as of December 31, 2022 to US$341.9
million as of December 31, 2023, primarily due to an increase of US$269.2 million in the
accumulated losses for the period, partially offset by (i) an increase of US$3.3 million in the
recognition of share-based payment expenses, and (ii) an increase of US$0.4 million in the
exchange differences on translation of foreign operations.
Our net liabilities increased from US$341.9 million as of December 31, 2023 to US$799.3
million as of December 31, 2024, primarily due to an increase of US$465.2 million in the
accumulated losses for the period, partially offset by (i) an increase of US$6.8 million in the
SUMMARY
– 23 –

<<<PAGE 34>>>
recognition of share-based payment expenses, (ii) an increase of US$0.4 million in the
exchange differences on translation of foreign operations, and (iii) an increase of US$0.7
million of change in fair value of equity investments at fair value through other comprehensive,
net of tax.
Our net liabilities increased from US$799.3 million as of December 31, 2024 to
US$1,303.5 million as of September 30, 2025, primarily due to an increase of US$512.0
million in the accumulated losses for the period, partially offset by (i) an increase of US$8.6
million in the recognition of share-based payment expenses, and (ii) an increase of US$1.6
million of change in fair value of equity investments at fair value through other comprehensive,
net of tax.
Summary of Consolidated Statements of Cash Flows
The following table sets forth our cash flows for the periods indicated.
For the year ended December 31,
For the nine months
ended September 30,
2022
2023
2024
2024
2025
(unaudited)
(US$ in thousands)
Net cash flows used in
operating activities     
(11,019)
(64,455)
(258,483)
(195,596)
(209,396)
Net cash flows used in
investing activities      
(35,156)
(40,320)
(431,300)
(630,463)
(126,231)
Net cash flows generated
from financing activities  
49,786
306,243
771,092
718,827
407,913
Net increase/ (decrease) in
cash and cash
equivalents          
3,611
201,468
81,309
(107,232)
72,286
Cash and cash equivalents at
the beginning of the
year/period           
994
4,691
206,295
206,295
288,912
Effect of foreign exchange
differences, net        
86
136
1,308
500
1,449
Cash and cash equivalents
at the end of the
year/period          
4,691
206,295
288,912
99,563
362,647
During the Track Record Period, we recorded net cash flows used in operating activities,
primarily reflecting our position as an R&D-intensive Specialist Technology Company in the
early stages of commercialization. In particular, our operating cash outflows were mainly
attributable to (i) significant research and development expenses, including staff costs for our
SUMMARY
– 24 –

<<<PAGE 35>>>
R&D and AI infrastructure teams and substantial third-party cloud services and other
computing-related costs incurred for training and operating our foundation models, (ii) our
early stage of commercialisation, during which our AI-native products and Open Platform only
began to generate revenue in the course of 2023 and 2024, resulting in a relatively small
revenue base as compared with our operating cost structure, and (iii) other operating cash
outflows, including cash operating costs relating to workforce employment, marketing and
promotion to acquire and engage users, and general and administrative expenses. These factors
collectively resulted in net operating cash outflows throughout the Track Record Period.
Our cash burn refers to the aggregate amount of (i) net cash used in operating activities,
(ii) capital expenditures, and (iii) lease payment. Our historical cash burn was US$11.5 million,
US$65.9 million, US$260.7 million and US$211.3 million in 2022, 2023, 2024 and nine
months ended September 30, 2025, respectively. Our cash burn increased throughout the Track
Record Period primarily due to increases in net cash used in operating activities as we scale
up R&D activities. In the future, we aim to continue to enhance our profitability and improve
our net operating cash outflows position through the following focus areas: (i) leveraging the
rapid growth of the foundation model industry, (ii) continuing to enhance foundation model
intelligence levels, (iii) enhancing the affordability of our AI technologies, (iv) broadening
monetization of our AI-native product suite, and (v) optimizing organizational efficiency and
scalability. Please refer to “Business — Path to the Commercialization of our Specialist
Technology Products” for our detailed strategies.
For the year ended December 31, 2025, our monthly cash burn is expected to be US$28.1
million. As of September 30, 2025, our cash balance was US$1,046.2 million, including cash
and cash equivalents US$362.6 million, current portion of financial assets at fair value through
profit or loss US$644.2 million and unutilised banking facilities US$39.4 million, as they
represent available liquidity to fund our operations. Assuming the expected average monthly
cash burn of US$28.1 million going forward at approximately 1.3 times of the average monthly
cash burn of the twelve months ended December 31, 2024, we estimate that our cash balance
is sufficient for us to operate for approximately 37 months without IPO proceeds, lasting
approximately until October 2028. With the estimated net IPO proceeds of US$468.7 million
(assuming 25,389,220 Offer Shares to be issued at the Offer Price of HK$151.0 per Share,
being the low-end of the Offer Price range, and the Offer Size Adjustment Option and the
over-allotment option are not exercised, and deducting the estimated IPO expense), our cash
is sufficient for us to operate for approximately 54 months with IPO proceeds, lasting
approximately until March 2030.
See “Financial Information — Cash Burn” for details.
SUMMARY
– 25 –

<<<PAGE 544>>>
CONSOLIDATED STATEMENTS OF FINANCIAL POSITION
As at 31 December
As at
30 September
Notes
2022
2023
2024
2025
USD’000
USD’000
USD’000
USD’000
NON-CURRENT ASSETS
Property, plant and equipment  
13
231
709
1,093
1,134
Right-of-use assets           
14(a)
458
3,313
3,077
2,746
Prepayments, other receivables
and other assets           
16
–
435
561
731
Financial assets at fair value
through profit or loss       
17
–
–
95,331
70,228
Financial assets at fair value
through other comprehensive
income                  
17
–
–
4,836
6,440
Restricted cash              
18
–
39
38
41
Total non-current assets      
689
4,496
104,936
81,320
CURRENT ASSETS
Trade receivables            
15
–
1,338
6,982
8,063
Prepayments, other receivables
and other assets           
16
569
4,378
13,470
11,811
Financial assets at amortised
cost                    
17
–
–
147,444
–
Financial assets at fair value
through profit or loss       
17
65,791
15,802
295,220
644,154
Restricted cash              
18
2,221
–
27,293
25,097
Time deposits               
18
–
91,698
26,327
–
Cash and cash equivalents     
18
4,691
206,295
288,912
362,647
Total current assets         
73,272
319,511
805,648
1,051,772
CURRENT LIABILITIES
Interest-bearing bank
borrowings               
19
–
–
19,455
19,102
Trade and bills payables       
20
2,394
17,242
51,212
70,219
Other payables, accruals and
other liabilities            
21
2,326
14,741
51,512
17,322
Contract liabilities           
22
–
559
1,553
4,657
Lease liabilities             
14(b)
349
1,248
1,964
1,694
Convertible redeemable
preferred shares           
24
145,175
629,001
1,581,949
2,321,193
Total current liabilities       
150,244
662,791
1,707,645
2,434,187
APPENDIX I
ACCOUNTANT’S REPORT
– I-7 –

<<<PAGE 545>>>
As at 31 December
As at
30 September
Notes
2022
2023
2024
2025
USD’000
USD’000
USD’000
USD’000
NET CURRENT
LIABILITIES            
(76,972)
(343,280)
(901,997)
(1,382,415)
TOTAL ASSETS LESS
CURRENT LIABILITIES  
(76,283)
(338,784)
(797,061)
(1,301,095)
NON-CURRENT
LIABILITIES
Lease liabilities             
14(b)
91
1,912
1,059
937
Other non-current liabilities    
23
–
1,218
1,200
1,467
Total non-current liabilities    
91
3,130
2,259
2,404
Net liabilities               
(76,374)
(341,914)
(799,320)
(1,303,499)
DEFICITS
Share capital               
25
–
–
–
–
Deficits                   
25
(76,374)
(341,914)
(799,320)
(1,303,499)
Total deficits               
(76,374)
(341,914)
(799,320)
(1,303,499)
APPENDIX I
ACCOUNTANT’S REPORT
– I-8 –

<<<PAGE 546>>>
CONSOLIDATED STATEMENTS OF CHANGES IN DEFICITS
Attributable to owners of the parent
Share
capital
Share
option
reserve*
Exchange
fluctuation
reserve*
Accumulated
losses*
Total
USD’000
USD’000
USD’000
USD’000
USD’000
At 31 December 2021
(unaudited)            
–
–
–
(3,814)
(3,814)
Loss for the year          
–
–
–
(73,728)
(73,728)
Other comprehensive income
for the year:
Exchange differences on
translation of foreign
operations             
–
–
99
–
99
Total comprehensive loss for
the year               
–
–
99
(73,728)
(73,629)
Recognition of share-based
payment expenses       
–
1,069
–
–
1,069
At 31 December 2022      
–
1,069
99
(77,542)
(76,374)
Attributable to owners of the parent
Share
capital
Share
option
reserve*
Exchange
fluctuation
reserve*
Accumulated
losses*
Total
USD’000
USD’000
USD’000
USD’000
USD’000
At 31 December 2022      
–
1,069
99
(77,542)
(76,374)
Loss for the year          
–
–
–
(269,246)
(269,246)
Other comprehensive income
for the year:
Exchange differences on
translation of foreign
operations             
–
–
360
–
360
Total comprehensive loss for
the year               
–
–
360
(269,246)
(268,886)
Recognition of share-based
payment expenses       
–
3,346
–
–
3,346
At 31 December 2023      
–
4,415
459
(346,788)
(341,914)
APPENDIX I
ACCOUNTANT’S REPORT
– I-9 –

<<<PAGE 547>>>
Attributable to owners of the parent
Share
capital
Share
option
reserve*
Fair value
reserve of
financial
assets at
fair value
through other
comprehensive
income*
Exchange
fluctuation
reserve*
Accumulated
losses*
Total
USD’000
USD’000
USD’000
USD’000
USD’000
USD’000
At 31 December 2023  
–
4,415
–
459
(346,788)
(341,914)
Loss for the year     
–
–
–
–
(465,238)
(465,238)
Other comprehensive
income for the year:
Change in fair value of
equity investments at
fair value through
other comprehensive,
net of tax        
–
–
662
–
–
662
Exchange differences on
translation of foreign
operations        
–
–
–
347
–
347
Total comprehensive
loss for the year    
–
–
662
347
(465,238)
(464,229)
Recognition of
share-based payment
expenses         
–
6,823
–
–
–
6,823
At 31 December 2024  
–
11,238
662
806
(812,026)
(799,320)
APPENDIX I
ACCOUNTANT’S REPORT
– I-10 –

<<<PAGE 548>>>
Attributable to owners of the parent
Share
capital
Share
option
reserve
Fair value
reserve of
financial
assets at
fair value
through other
comprehensive
income
Exchange
fluctuation
reserve
Accumulated
losses
Total
USD’000
USD’000
USD’000
USD’000
USD’000
USD’000
At 31 December 2023

–
4,415
–
459
(346,788)
(341,914)
Loss for the period
(unaudited)       
–
–
–
–
(304,342)
(304,342)
Other comprehensive
income for the period:
Change in fair value of
equity investments at
fair value through
other comprehensive,
net of tax (unaudited)
–
–
(839)
–
–
(839)
Exchange differences on
translation of foreign
operations
(unaudited)       
–
–
–
(86)
–
(86)
Total comprehensive
loss for the period
(unaudited)       
–
–
(839)
(86)
(304,342)
(305,267)
Recognition of share-
based payment
expenses (unaudited) 
–
6,100
–
–
–
6,100
At 30 September 2024
(unaudited)       
–
10,515
(839)
373
(651,130)
(641,081)
APPENDIX I
ACCOUNTANT’S REPORT
– I-11 –

<<<PAGE 549>>>
Attributable to owners of the parent
Share
capital
Share
option
reserve*
Fair value
reserve of
financial
assets at
fair value
through other
comprehensive
income*
Exchange
fluctuation
reserve*
Accumulated
losses*
Total
USD’000
USD’000
USD’000
USD’000
USD’000
USD’000
At 31 December 2024  
–
11,238
662
806
(812,026)
(799,320)
Loss for the period    
–
–
–
–
(512,013)
(512,013)
Other comprehensive
income for the period:
Change in fair value of
equity investments at
fair value through
other comprehensive,
net of tax        
–
–
1,604
–
–
1,604
Exchange differences on
translation of foreign
operations        
–
–
–
(1,255)
–
(1,255)
Total comprehensive
loss for the period   
–
–
1,604
(1,255)
(512,013)
(511,664)
Recognition of share-
based payment
expenses         
–
8,581
–
–
–
8,581
Deemed distribution   
–
–
–
–
(1,096)
(1,096)
At 30 September 2025 
–
19,819
2,266
(449)
(1,325,135) (1,303,499)
*
These
deficits
accounts
comprise
the
consolidated
deficits
of
USD76,374,000,
USD341,914,000,
USD799,320,000 and USD1,303,499,000 in the consolidated statements of financial position as at 31
December 2022, 2023 and 2024 and 30 September 2025, respectively.
APPENDIX I
ACCOUNTANT’S REPORT
– I-12 –

<<<PAGE 422>>>
CONSOLIDATED STATEMENTS OF PROFIT OR LOSS
The following table sets forth a summary of our consolidated statements of profit or loss,
in absolute amounts and as a percentage of our total revenue, for the periods indicated.
For the year ended December 31,
For the nine months ended
September 30,
2022
2023
2024
2024
2025
US$
%
US$
%
US$
%
US$
%
US$
%
(unaudited)
(in thousands, except for percentages)
Revenue          
–
–
3,460
100.0
30,523
100.0
19,454
100.0
53,437
100.0
Cost of sales
      
–
–
(4,314)
(124.7)
(26,785)
(87.8)
(18,944)
(97.4)
(40,961)
(76.7)
Gross (loss)/profit
   
–
–
(854)
(24.7)
3,738
12.2
510
2.6
12,476
23.3
Other income and gains,
net
          
1,155
–
8,942
258.4
36,151
118.4
25,278
129.9
31,232
58.4
Selling and distribution
expenses
       
(587)
–
(22,827)
(659.7)
(86,995)
(285.0)
(53,389)
(274.4)
(39,325)
(73.6)
Administrative expenses  
(3,213)
–
(7,615)
(220.1)
(14,384)
(47.1)
(9,610)
(49.4)
(22,074)
(41.3)
Research and development
expenses
       
(10,560)
–
(70,002) (2,023.2) (188,979)
(619.1) (138,684)
(712.9) (180,312)
(337.4)
Fair value loss on financial
liabilities        
(60,509)
–
(176,826)
(5,110.6) (214,172)
(701.7) (128,063)
(658.3) (313,477)
(586.6)
Finance costs       
(14)
–
(61)
(1.8)
(509)
(1.7)
(316)
(1.6)
(511)
(1.0)
Impairment losses on
financial assets, net   
–
–
(3)
(0.1)
(88)
(0.3)
(68)
(0.3)
(22)
–
Loss before tax      
(73,728)
–
(269,246) (7,781.7) (465,238) (1,524.2) (304,342) (1,564.4) (512,013)
(958.2)
Income tax expense    
–
–
–
–
–
–
–
–
–
–
Loss for the year/period 
(73,728)
–
(269,246) (7,781.7) (465,238) (1,524.2) (304,342) (1,564.4) (512,013)
(958.2)
Attributable to:
Owners of the parent
  
(73,728)
–
(269,246) (7,781.7) (465,238) (1,524.2) (304,342) (1,564.4) (512,013)
(958.2)
Non-controlling interests

–
–
–
–
–
–
–
–
–
–
Loss and total
comprehensive income
for the year
     
(73,728)
–
(269,246) (7,781.7) (465,238) (1,524.2) (304,342) (1,564.4) (512,013)
(958.2)
Loss per share
attributable to ordinary
equity holders of the
parent
Basic and diluted
–For loss for the
year/period (US$)    
(0.74)
(2.56)
(4.28)
(2.80)
(4.71)
FINANCIAL INFORMATION
– 412 –

<<<PAGE 423>>>
NON-IFRS FINANCIAL MEASURE
We use adjusted net loss (non-IFRS measure), which is a non-IFRS financial measure, in
evaluating our operating results and for financial and operational decision-making purposes.
We believe that adjusted net loss (non-IFRS measure) helps identify underlying trends in our
business that could otherwise be distorted by the effect of certain expenses that we include in
our net loss. We believe that adjusted net loss (non-IFRS measure) provides useful information
about our results of operations, enhances the overall understanding of our past performance and
future prospects and allows for greater visibility with respect to key metrics used by our
management in its financial and operational decision-making.
Adjusted net loss (non-IFRS measure) should not be considered in isolation or construed
as an alternative to net loss or any other measure of performance or as an indicator of our
operating performance. Investors are encouraged to review adjusted net loss (non-IFRS
measure) and the reconciliation to its most directly comparable IFRS measure. Adjusted net
loss (non-IFRS measure) presented here may not be comparable to similarly titled measures
presented by other companies. Other companies may calculate similarly titled measures
differently, limiting their usefulness as comparative measures to our data. We encourage
investors and others to review our financial information in its entirety and not rely on a single
financial measure.
We define our adjusted net loss (non-IFRS measure) as net loss adjusted by adding back
(i) share-based payment expenses that are included in cost of sales, general administrative,
research and development, and sales and marketing expenses, relates to the share-based awards
that we grant to participants of our share incentive schemes and is a non-cash expense, (ii) fair
value losses on financial liabilities, comprising fair value changes of convertible redeemable
preferred shares which will be re-designated from liabilities to equity as a result of the
automatic conversion into ordinary shares upon Listing, and convertible bonds, which have
subsequently been repaid in full as of the Latest Practicable Date, and (iii) listing expenses.
FINANCIAL INFORMATION
– 413 –

<<<PAGE 424>>>
The following table presents our non-IFRS financial measure for the years ended
December 31, 2022, 2023, 2024 and the nine months ended September 30, 2024 and 2025.
For the year ended December 31,
For the nine months ended
September 30,
2022
2023
2024
2024
2025
US$
US$
US$
US$
US$
(unaudited)
(in thousands)
Loss for the
year/period      
(73,728)
(269,246)
(465,238)
(304,342)
(512,013)
Add:
Share-based payment
expenses        
1,069
3,346
6,823
6,100
8,581
Fair value loss
on financial
liabilities
      
60,509
176,826
214,172
128,063
313,477
Listing expenses    
–
–
–
–
3,675
Adjusted net loss for
the year/period
(non-IFRS
measure)        
(12,150)
(89,074)
(244,243)
(170,179)
(186,280)
DESCRIPTION OF MAJOR COMPONENTS OF OUR RESULTS OF OPERATIONS
Revenue
Our revenue is derived from two primary sources — (i) AI-native products and (ii) Open
Platform and other AI-based enterprise services, mainly consists of API usage as well as
arrangements customized to enterprise requirements and licensed deliverables. For customised
arrangements, we work with enterprise customers to set up dedicated inference resource pools
tailored to their needs, helping ensure stable and predictable model inference performance. For
licensed deliverables, we license our foundation models to enable customers to deploy and
operate such models in their own systems. Each revenue stream reflects a distinct monetization
pathway aligned with our product and platform strategies. The following table sets forth the
breakdown of our revenue by nature, in absolute amounts and as a percentage of our total
revenue, for the periods indicated.
FINANCIAL INFORMATION
– 414 –

<<<PAGE 425>>>
For the year ended December 31,
For the nine months ended
September 30,
2022
2023
2024
2024
2025
US$
%
US$
%
US$
%
US$
%
US$
%
(unaudited)
(in thousands, except for percentages)
AI-native products     
–
–
758
21.9
21,805
71.4
13,529
69.5
38,020
71.1
Open Platform and other
AI-based enterprise
services         
–
–
2,702
78.1
8,718
28.6
5,925
30.5
15,417
28.9
Total revenue       
–
–
3,460
100.0
30,523
100.0
19,454
100.0
53,437
100.0
AI-native products. We generate revenue from individual users through subscription-
based access to our monetized AI-native consumer applications, such as MiniMax, Hailuo AI,
MiniMax Audio, and Talkie/Xingye. Subscriptions provide users with premium functionality
across multi-modal generation, intelligent interaction, and personalized experiences. Revenue
is recognised ratably over the subscription period, as we fulfill a stand-ready performance
obligation to provide continuous access to content and services throughout the term. Users
have option to pre-purchase additional credits to recharge their accounts and buy these virtual
items. For consumable virtual items, revenue is recognised when the virtual items are
consumed. For non-consumable virtual items, revenue is recognised over the estimated average
acting period of the paying users. In addition, we generate online marketing service revenue
by providing marketing services to mediation platform on certain of our AI-native applications.
Revenue is recognised at a point in time, when a user views or clicks on an advertisement,
thereby fulfilling our performance obligation. These services enable mediation platform to
engage with end users in a contextually relevant and measurable manner. As our user base and
engagement levels expand, this revenue stream is expected to continue contributing to our
overall monetization.
Open Platform and other AI-based enterprise services. We provide enterprise customers
with access to our usage-based Open Platform and other AI-based enterprise services. Revenue
from API usage is recognised at a point in time when the customers call APIs with tokens,
which are billed under certain agreed fee schedule or usage-based structure. Revenue from
other AI-based enterprise services, mainly consists of arrangements customized to enterprise
requirements and licensed deliverables, is typically recognised at a point in time, when control
is transferred or acceptance is confirmed. Specifically, for customised arrangements, we work
with enterprise customers to set up dedicated inference resource pools tailored to their needs,
helping ensure stable and predictable model inference performance. For licensed deliverables,
we license our foundation models to enable customers to deploy and operate such models in
their own systems. These services support enterprise use cases across sectors such as smart
devices, healthcare, tourism, and finance.
FINANCIAL INFORMATION
– 415 –

<<<PAGE 426>>>
The tables below set forth breakdowns of revenue by product and further by monetization
method:
For the year ended December 31,
For the nine months ended
September 30,
2022
2023
2024
2024
2025
US$
%
US$
%
US$
%
US$
%
US$
%
(unaudited)
(in thousands, except for percentages)
AI-native products
MiniMax          
–
–
–
–
–
–
–
–
756
1.4
Hailuo AI         
–
–
–
–
2,347
7.7
–
–
17,464
32.6
MiniMax Audio      
–
–
–
–
–
–
–
–
1,050
2.0
Talkie/Xingye       
–
–
758
21.9
19,458
63.7
13,529
69.5
18,750
35.1
Open Platform and other
AI-based enterprise
services         
–
–
2,702
78.1
8,718
28.6
5,925
30.5
15,417
28.9
Total revenue       
–
–
3,460
100.0
30,523
100.0
19,454
100.0
53,437
100.0
For the year ended December 31,
For the nine months ended
September 30,
2022
2023
2024
2024
2025
US$
%
US$
%
US$
%
US$
%
US$
%
(unaudited)
(in thousands, except for percentages)
AI-native products
MiniMax     In-app top-up
–
–
–
–
–
–
–
–
204.0
0.4
Subscriptions
–
–
–
–
–
–
–
–
552.0
1.0
Hailuo AI     In-app top-up
–
–
–
–
527
1.7
–
–
3,317
6.2
Subscriptions
–
–
–
–
1,820
6.0
–
–
14,147
26.4
MiniMax Audio  In-app top-up
–
–
–
–
–
–
–
–
196
0.4
Subscriptions
–
–
–
–
–
–
–
–
854
1.6
Talkie/Xingye   In-app top-up
–
–
164
4.8
897
3.0
712
3.7
958
1.8
Subscriptions
–
–
594
17.1
3,960
12.9
2,917
14.9
6,604
12.4
Online
marketing
service
–
–
–
–
14,601
47.8
9,900
50.9
11,188
20.9
Open Platform and other
AI-based enterprise services  
–
–
2,702
78.1
8,718
28.6
5,925
30.5
15,417
28.9
Total revenue          
–
–
3,460
100.0
30,523
100.0
19,454
100.0
53,437
100.0
FINANCIAL INFORMATION
– 416 –

<<<PAGE 542>>>
CONSOLIDATED STATEMENTS OF PROFIT OR LOSS
Year ended 31 December
Nine months ended
30 September
Notes
2022
2023
2024
2024
2025
USD’000
USD’000
USD’000
USD’000
USD’000
(unaudited)
REVENUE          
5
–
3,460
30,523
19,454
53,437
Cost of sales         
–
(4,314)
(26,785)
(18,944)
(40,961)
Gross (loss)/profit     
–
(854)
3,738
510
12,476
Other income and gains,
net               
5
1,155
8,942
36,151
25,278
31,232
Selling and distribution
expenses           
(587)
(22,827)
(86,995)
(53,389)
(39,325)
Administrative expenses 
(3,213)
(7,615)
(14,384)
(9,610)
(22,074)
Research and
development expenses
(10,560)
(70,002)
(188,979)
(138,684)
(180,312)
Fair value loss on
financial liabilities   
(60,509)
(176,826)
(214,172)
(128,063)
(313,477)
Finance costs         
6
(14)
(61)
(509)
(316)
(511)
Impairment losses on
financial assets, net  
–
(3)
(88)
(68)
(22)
LOSS BEFORE TAX  
7
(73,728)
(269,246)
(465,238)
(304,342)
(512,013)
Income tax expense    
10
–
–
–
–
–
LOSS FOR THE
YEAR/PERIOD     
(73,728)
(269,246)
(465,238)
(304,342)
(512,013)
Attributable to:
Owners of the parent 
(73,728)
(269,246)
(465,238)
(304,342)
(512,013)
Non-controlling
interests         
–
–
–
–
–
(73,728)
(269,246)
(465,238)
(304,342)
(512,013)
LOSS PER SHARE
ATTRIBUTABLE TO
ORDINARY EQUITY
HOLDERS OF THE
PARENT
Basic and diluted —
For loss for the
year/period (USD)   
12
(0.74)
(2.56)
(4.28)
(2.80)
(4.71)
APPENDIX I
ACCOUNTANT’S REPORT
– I-5 –

<<<PAGE 543>>>
CONSOLIDATED STATEMENTS OF COMPREHENSIVE INCOME
Year ended 31 December
Nine months ended
30 September
2022
2023
2024
2024
2025
USD’000
USD’000
USD’000
USD’000
USD’000
(unaudited)
LOSS FOR THE YEAR/
PERIOD               
(73,728)
(269,246)
(465,238)
(304,342)
(512,013)
OTHER COMPREHENSIVE
INCOME/(LOSS)
Other comprehensive
income/(loss) to be
reclassified to profit or loss
in subsequent periods:
Exchange differences on
translation of foreign
operations              
99
360
347
(86)
(1,255)
Net other comprehensive
income/(loss) to be
reclassified to profit or loss
in subsequent periods      
99
360
347
(86)
(1,255)
Other comprehensive income
not to be reclassified to
profit or loss in subsequent
periods:
Changes in fair value of equity
investments designated at
fair value through other
comprehensive income     
–
–
662
(839)
1,604
Net other comprehensive
income not to be reclassified
to profit or loss in
subsequent periods        
–
–
662
(839)
1,604
TOTAL COMPREHENSIVE
LOSS FOR THE YEAR/
PERIOD               
(73,629)
(268,886)
(464,229)
(305,267)
(511,664)
Attributable to:
Owners of the parent      
(73,629)
(268,886)
(464,229)
(305,267)
(511,664)
Non-controlling interests   
–
–
–
–
–
(73,629)
(268,886)
(464,229)
(305,267)
(511,664)
APPENDIX I
ACCOUNTANT’S REPORT
– I-6 –

<<<PAGE 349>>>
recovery of our own attorneys’ fees under the same discretionary framework.
Accordingly,
while
attorneys’ fees
are
a
component
of
risk,
they
do
not
fundamentally change the overall exposure profile described above.
As the case is still at an early stage and a reliable estimate of the amount of the obligation
cannot be made with certainty, the Directors, having given due consideration to the legal advice
and the relevant facts and circumstances, are of the opinion that the above matters give rise to
contingencies for the Group and hence no provision should be recognized as at September 30,
2025. See Note 28 to the Accountant’s report in Appendix I to the prospectus. The Reporting
Accountants conducted their work in accordance with Hong Kong Standard on Investment
Circular Reporting Engagements 200 Accountants’ Reports on Historical Financial Information
in Investment Circulars issued by the Hong Kong Institute of Certified Public Accountants.
This standard requires that the Reporting Accountants plan and perform their work to obtain
reasonable assurance about whether the Historical Financial Information as a whole is free
from any material misstatement. The Reporting Accountant’s opinion on the Historical
Financial Information of the Group for the Track Record Period as a whole is set out on page
I-1 to I-3 of Appendix I to the prospectus.
Based on the independent due diligence steps performed by the Joint Sponsors, including,
among other things, (a) discussing with the Company’s U.S. litigation advisor regarding the
potential worst-case scenario, the possibility of granting the injunctive relief and their legal
analysis in this regard, (b) reviewing of the Group’s financial information, and (c) examination
of the MAU data of Hailuo AI from June to November 2025 and the system-check results of
Hailuo AI’s outputs, the Joint Sponsors concur with the Directors’ view above.
We intend to defend ourselves vigorously against the allegations and will respond to the
complaint in accordance with U.S. civil procedure. However, as this case is still at an early
stage, we cannot predict with certainty its timing, outcome, potential damages, or expenses that
may be incurred, and there can be no assurance that we will prevail. Additionally, the potential
damages scenario mentioned above is inherently speculative given the early stage of the case,
the absence of discovery, and the unresolved questions regarding the Plaintiffs’ claims,
including the number of works that may ultimately be found to have been infringed, if any, and
the appropriate per-work amount of statutory damages. Any adverse outcome of this case could
result in payments of monetary damages and divert our management’s attention from
day-to-day operations, and thus have an adverse effect on our business, results of operations,
financial condition and reputation. For the potential impact of legal proceedings on us, see
“Risk Factors — Risks Related to Our Business and Industry — We, our directors,
management, employees and shareholders and their affiliates may be subject to lawsuits,
contract disputes, employment-related controversies, and other legal and administrative
proceedings or fines, which could have a material adverse effect on our business, results of
operations, financial condition and reputation.”
BUSINESS
– 339 –

<<<PAGE 350>>>
Additional Measures Adopted by the Group
Despite our view that the Plaintiffs’ claims in the Lawsuit are without merit in all material
respects, we have proactively implemented measures as part of our ongoing compliance and
risk-management framework. In order to prevent any improper or illegal inputs by users and
minimize our risk exposure and avoid being involved in similar claims and disputes, we
explicitly inform users in our terms of service that they must not input illegal, non-compliant
or inappropriate content, and must not use our products to engage in illegal or non-compliant
activities or for unlawful purposes. Our terms further specify the consequences of violations,
including our right to delete or block prohibited content, suspend user accounts, or take other
enforcement measures.
We have also established complaint and reporting mechanisms. As stated in the terms of
service, users may submit complaints if they discover illegal, infringing or otherwise
non-compliant content or activity. Upon receiving such reports, we will promptly verify and
handle the issue, including by removing or blocking content that is unlawful, infringing others’
intellectual property rights or otherwise noncompliant, or applying keyword blocks where
appropriate, according to the terms of service.
We monitor and regulate unlawful or non-compliant content at both the input and output
stages. We have developed content review standards and moderation rules based on applicable
laws, regulations and operational experience (for example, categories prohibited under the PRC
Administrative Measures on Internet Information Services and the Interim Measures for the
Administration of Generative Artificial Intelligence Services). Our automated and manual
review mechanisms may filter, block or otherwise address harmful content, including illegal
content, content that endangers public safety, or pornographic, violent or otherwise prohibited
material.
To support the implementation of our content-governance framework at scale, we apply
automated and manual review and moderation controls at both the input and output stages
across our products, and we track the effectiveness of such controls using an internal indicator
referred to as the “filter effectiveness rate”, which is defined as the ratio of (1) the total number
of reviewed items that are successfully filtered, over (2) the total number of reviewed items
that should be filtered. This indicator is measured primarily through a sampling-based
methodology, under which we deploy a test dataset comprising content that should be filtered
and assess the proportion that is successfully filtered by our systems, which we consider more
reliable than relying solely on detected misses in live user traffic, as undetected misses may
exist. As a reference point, in the month ended November 30, 2025, the filter effectiveness rate
across
our AI-native
products,
including
MiniMax,
Hailuo AI,
MiniMax Audio
and
Talkie/Xingye, was approximately 96.8%.
In addition to the above KPI testing, potential “misses” in live operations are identified
through multiple channels, including (i) user complaints, (ii) routine inspections and testings
by our safety team, and (iii) feedback from regulators, where applicable. For any miss that is
identified, we (a) promptly implement blocking measures to prevent recurrence (including
BUSINESS
– 340 –

<<<PAGE 351>>>
taking down, blocking or restricting the relevant content/output, as appropriate), and (b)
continuously improve our moderation controls based on root-cause analysis, including refining
our review models and expanding our keyword libraries for filtering, with a view to further
enhancing the effectiveness of filtering on an ongoing basis.
Our legal department manages infringement. In daily operations, when intellectual
property disputes are identified, the responsible business department promptly reports them to
the legal department. The responsible department and the legal department jointly investigate
the matter, determine a response strategy, and take appropriate actions. In cases involving
litigation or arbitration, the legal department also adheres to our internal regulations regarding
litigation and arbitration cases. Additionally, the legal department conducts searches through
public channels to identify potential infringement issues. For any confirmed infringement
incidents, the legal department follows up and manages their resolution and keep the follow up
records.
The Directors view these measures as adequate and effective and consistent with industry
practice. Based on the Joint Sponsors’ independent due diligence steps, including the
discussions with CIC on whether the Group’s business practices are comparable to those of its
industry peers, the discussion with the internal control consultant and the review of the internal
control report issued, nothing has come to the attention which would cause them to disagree
with the Directors’ view above.
General Legal Compliance
With respect to Singapore where we maintain a material subsidiary, as advised by our
Singapore legal advisor, the Group’s business operations have been conducted in compliance
with all material aspects of applicable laws and regulations throughout the Track Record Period
and up to the Latest Practicable Date.
While we do not possess any subsidiaries in the United States, given the volume of users
of our AI-native products and the associated revenue generated from the U.S. market, we have
engaged U.S. legal counsels to conduct legal due diligence, with a particular focus on U.S.
sanctions and export control issues and data protection compliance issues.
Sanctions and Export Controls
Based on the relevant diligence findings, as advised by our international sanctions legal
advisor, from a U.S. legal perspective, (a) our Group is not engaged in activities in violation
of U.S. export controls and (b) our Group is not currently engaged in primary sanctioned
activity or secondary sanctionable activity; and (c) our Group is not subject to U.S. tariff rules
and regulations in any material aspects, since U.S. import tariffs only apply of export of
physical goods to the United States and we do not export physical goods to the United States.
As advised by our international sanctions legal advisor, during the Track Record Period and up
to the Latest Practicable Date, our Group has not been subject to sanctions, and we have not
engaged in any material activities in comprehensively sanction countries, or entered into
BUSINESS
– 341 –

<<<PAGE 352>>>
material service contract or engaged in any material activities with any customers that are
targets of U.S. sanctions. Therefore, as advised by our international sanctions legal advisor, we
have been in compliance with rule and laws in US export control and sanctions in all material
aspects, and U.S. sanctions are not likely to have any material adverse impact on us. Based on,
among other things, the review of (a) the legal memorandum issued by the international
sanctions legal advisor, (b) the Group’s financial information during the Track Record Period
and (c) the results of background check conducted against the Group, and third party due
diligence sessions conducted by the Joint Sponsors, the Joint Sponsors have reasonable
grounds to believe that the view expressed fairly represents the views of the sanction expert.
Based on our Directors’ knowledge, we have conducted our business operations in
compliance with applicable laws and regulations in all material respects in all jurisdictions in
which we operate.
Outbound Investment Rules
Effective on January 2, 2025, the final rule issued Treasury to implement the executive
order of August 9, 2023 (the “Final Rule”) imposes investment prohibition and notification
requirements on U.S. Persons for a wide range of investments in entities associated with China
(including Hong Kong and Macau) that are engaged in activities relating to three sectors: (i)
semiconductors and microelectronics, (ii) quantum information technologies, and (iii) AI
systems. U.S. persons subject to the Final Rule are prohibited from making, or required to
report, certain investments in covered foreign persons, which are defined as “covered
transactions,” and include acquisitions of equity interests (including contingent equity
interests), certain debt financing, joint ventures, and certain investments as a limited partner
in a non-U.S. person pooled investment fund. The Final Rule excludes some investments from
the scope of covered transactions, including certain ones in publicly traded securities. The
Final Rule is aimed at exerting greater U.S. government oversight over U.S. direct and indirect
investments involving China, and may introduce new hurdles and uncertainties for cross-border
collaborations, investments, and funding opportunities of China-based issuers including us.
Since our principal place of business is in China and we engage in the development of certain
AI models, we are likely to be deemed as a “covered foreign person” as described in the Final
Rule.
Pursuant to the Final Rule, U.S. persons’ purchases of certain publicly traded securities
are neither prohibited nor subject to notification to Treasury under an exception in the Final
Rule that applies to U.S. persons’ purchase of “any publicly traded security, with ‘security’ as
defined in the U.S. Exchange Act, denominated in any currency, and that trades on a securities
exchange in any jurisdiction” (the “Publicly Traded Securities Exception”), provided that such
U.S. persons or their non-U.S. person subsidiaries are not afforded rights beyond standard
minority shareholder protections with respect to the Company. But it appears likely, based on
information we provided to our international sanctions advisor, that certain purchases of our
Shares by U.S. persons or their non-U.S. person subsidiaries in the Global Offering would be
in eligible for the Publicly Traded Securities Exception. Accordingly, it appears likely that
some U.S. persons that purchase our Shares in the Global Offering or are the parents of
BUSINESS
– 342 –

<<<PAGE 353>>>
non-U.S. person subsidiaries that purchase our Shares in the Global Offering would be required
to file notifications regarding their or their subsidiaries’ purchases with Treasury no later than
30 days after such purchases of the Shares.
As advised by our international sanctions legal advisor, our Directors are of the view that
the Final Rule will not have a material effect on our business, results of operations or financial
condition, in part because: (i) in light of the totality of the circumstances of the Global
Offering, including that it is expected to be marketed to, and capable of being supported by,
a broad investor base (including non-U.S. investors), the Final Rule is not expected to
materially constrain investor participation in the Global Offering; (ii) based on information we
provided to our international sanctions advisor, following completion of the Global Offering,
it appears likely that the Publicly Traded Securities Exception would generally be available to
U.S. persons (or their non-U.S. person subsidiaries) seeking to purchase our Class A Shares
after they become listed and traded on the Stock Exchange, provided that such U.S. persons or
non-U.S. person subsidiaries are not afforded rights beyond standard minority shareholder
protections with respect to the Company; and (iii) although some U.S. person investors (or
their non-U.S. person subsidiaries) may be unable to rely on the Publicly Traded Securities
Exception in connection with the purchase of our Shares in the Global Offering, any resulting
impact would be expected to relate primarily to the composition of our shareholder base, rather
than our ability to continue operating our business in the ordinary course.
Compliance with Applicable PRC AI Laws and Regulations
The regulations concerning generative artificial intelligence (AI) services in the PRC
mainly include the Interim Measures for the Administration of Generative Artificial
Intelligent Services (《生成式人工智能服務管理暫行辦法》) (the “AIGC Administration
Measures”), The Administrative Provisions on Algorithm Recommendation of Network
Information
Services
(《互聯網信息服務算法推薦管理規定》),
and
the
Administrative
Provisions for Deep Synthesis as an Internet Information Service. (《互聯網信息服務深度合成
管理規定》). These regulations set forth specific compliance requirements regarding the
record-filing of generative AI services, algorithm filing, security assessments, training data
processing activities, data labeling, service transparency, generation content identification, and
content compliance. See “Regulatory Overview — Laws and Regulations in the PRC —
Government Policies on Artificial Intelligence” for details.
As of the Latest Practicable Date, we have completed the record-filing procedures for the
large models and algorithms related to generative AI services in accordance with the
aforementioned regulations. We have filed the requisite model registration for our proprietary
models, including the “Abab” model series, the “Abab multi-modal” model series, and the
“MiniMax” model series, with the Shanghai Municipal Cyberspace Administration in
accordance with PRC regulations on generative artificial intelligence. As advised by our PRC
data legal advisor, our Directors are of the view that the Group had complied in all material
respects with the Measures and all applicable AI-related laws and regulations in the PRC
during the Track Record Period and up to the Latest Practicable Date. Based on the view of our
PRC legal advisor and the Joint Sponsors’ discussion with their PRC legal advisor, the Joint
BUSINESS
– 343 –

<<<PAGE 354>>>
Sponsors concur with the Directors’ view above. We attach great importance to the protection
of minors and have adopted a “Minor Protection Policy” to safeguard content safety for
underage users. As providers of generative artificial intelligence services, We respect
intellectual property rights and business ethics, keep trade secrets, and respect the legitimate
rights and interests of others. We have service agreements with users of generative artificial
intelligence services who have registered for our services to clarify the rights and obligations
of both parties. We have also conducted the required security assessments for the relevant
services as per the regulations. In addition, we have implemented compliance measures in areas
such as training data processing, data labeling, service transparency, generation content
identification, and content compliance, in line with the regulatory requirements set forth in the
relevant Chinese regulations on generative AI services. On March 7, 2025, the CAC and three
other departments jointly issued the Measures for the Identification of AI-Generated and
Synthesized Content (《人工智能生成合成內容標識辦法》) (the “Identification Measures”),
which came into effect on September 1, 2025. In accordance with the Identification Measures,
we add explicit identification to AI-generated and synthesized content such as text, audio,
images, video. We also add implicit identification to the file metadata containing AI-Generated
and Synthesized content. As advised by our PRC legal advisor, we had fully complied with the
Chinese government’s policies, laws and regulations on artificial intelligence in all major
aspects during the Track Record Period and up to the Latest Practicable Date. For more details,
see the section headed “Data Security and Privacy”.
Compliance with Applicable PRC Cybersecurity Laws and Regulations
The
Measures
for
Cybersecurity
Review
(《網絡安全審查辦法》)
prescribes
the
following conditions under which a cybersecurity review must be conducted. A company is
required to undergo such a review if any of the following circumstances apply:
•
Critical information infrastructures operators that purchase network products and
services shall anticipate the potential national security risk of products and services
after they enter operation, and they influence or could influence national security;
•
Online platform operators engage in data processing activities that may have an
impact on, or potentially affect, national security;
•
Online platform operators holding the personal information of more than one million
users and listing abroad; or
•
Regulatory authorities have initiated a review based on their official prerogative.
See “Regulatory Overview — Laws and Regulations in the PRC — Regulations Relating
to Cybersecurity and Data Protection” for details.
BUSINESS
– 344 –

<<<PAGE 467>>>
INDEBTEDNESS
The following table sets forth our indebtedness as of the dates indicated.
As of December 31,
As of
September 30,
As of
November 30,
2022
2023
2024
2025
2025
USD’000
USD’000
USD’000
USD’000
USD’000
(unaudited)
Current
Interest-bearing
bank borrowings 
–
–
19,455
19,102
14,130
Lease liabilities   
349
1,248
1,964
1,694
1,688
Convertible bonds
included in other
payables, accruals
and other
liabilities       
–
–
14,722
–
–
Convertible
redeemable
preferred shares 
145,175
629,001
1,581,949
2,321,193
3,091,653
Non-Current
Lease liabilities   
91
1,912
1,059
937
738
Total           
145,615
632,161
1,619,149
2,342,926
3,108,209
For details of our interest-bearing bank and other borrowings and lease liabilities during
the Track Record Period, see “— Discussion of Certain Key Items from Our Consolidated
Statements of Financial Position”. As of November 30, 2025, our committed unutilized bank
facilities amounted to US$44.9 million. During the Track Record Period and up to the date of
this Prospectus, we did not have any contingent liabilities.
Our Directors confirm that as of the Latest Practicable Date, the agreements under our
borrowings did not contain any covenants that would have a material and adverse effect on our
ability to obtain additional borrowings or issue debt or equity securities in the future. Our
Directors further confirm that we had no defaults in bank and other borrowings, nor did we
breach any covenants (that were not waived) during the Track Record Period and up to the
Latest Practicable Date. Additionally, our Directors confirm that, during the Track Record
Period and up to the Latest Practicable Date, we did not experience any difficulties in obtaining
credit facilities, nor any withdrawal of facilities or requests for early repayment.
Except as otherwise disclosed under the sections titled “— Indebtedness” and “—
Contractual Obligations,” as of November 30, 2025, the latest practicable date for determining
our indebtedness, we did not have any material bank overdrafts, loans, or other similar
indebtedness, liabilities under acceptances or acceptance credits, debentures, mortgages,
charges, other recognised lease liabilities, guarantees, or other material contingent liabilities.
Our Directors confirm that there have been no material changes in our indebtedness since
November 30, 2025 and up to the date of this Prospectus.
FINANCIAL INFORMATION
– 457 –

<<<PAGE 468>>>
RESEARCH AND
DEVELOPMENT
EXPENDITURE AND
TOTAL OPERATING
EXPENDITURE
During the Track Record Period, we did not capitalize internal development costs as
intangible assets. The following table sets forth our annual and total research and development
expenditure for the periods indicated
For the year ended December 31,
For the nine months ended
September 30,
2022
2023
2024
2024
2025
(unaudited)
(US$ in thousands)
Research and
development
expenses        
10,560
70,002
188,979
138,684
180,312
Adjustments:
Add: intangible assets
acquired from third
parties and
capitalized(1).     
–
–
–
–
–
Less: amortization
expense of
capitalized
intangible assets
included in
research and
development
expenditure(1).    
–
–
–
–
–
Annual research and
development
expenditure      
10,560
70,002
188,979
138,684
180,312
Total research and
development
expenditure for
the three financial
years prior to the
Global Offering  
269,541
FINANCIAL INFORMATION
– 458 –

<<<PAGE 469>>>
The following table sets forth our annual and total operating expenditure for the periods
indicated:
For the year ended December 31,
For the nine months ended
September 30,
2022
2023
2024
2024
2025
(unaudited)
(US$ in thousands)
Research and development
expenses             
10,560
70,002
188,979
138,684
180,312
Selling and distribution
expenses             
587
22,827
86,995
53,389
39,325
Administrative expenses    
3,213
7,615
14,384
9,610
22,074
Adjustments:
Add: intangible assets
acquired from third parties
and capitalized         
–
–
–
–
–
Less: amortization expense of
capitalized intangible assets
included in research and
development expenditure  
–
–
–
–
–
Total operating expenditure
for the three financial
years prior to the Global
Offering             
405,162
FINANCIAL INFORMATION
– 459 –

<<<PAGE 470>>>
The following table sets forth our annual research and development expenditure ratio and
total research and development expenditure ratio for the periods indicated:
For the year ended December 31,
For the nine months ended
September 30,
2022
2023
2024
2024
2025
(unaudited)
(US$ in thousands)
Annual research
and development
expenditure
ratio(1)          
73.5%
69.7%
65.1%
68.8%
74.6%
Total research
and development
expenditure
ratio(2)          
66.5%
(1)
Calculated by dividing annual research and development expenditure by annual total operating
expenditure.
(2)
Calculated by dividing total research and development expenditure for the three financial years prior to
the Global Offering by total operating expenditure for the three financial years prior to the Global
Offering.
CAPITAL EXPENDITURES
Our historical capital expenditures primarily consist of expenditures for plant and
equipment, specifically leasehold improvements and office equipment. The following table sets
forth our capital expenditures for the periods indicated.
For the year ended December 31,
For the nine months ended
September 30,
2022
2023
2024
2024
2025
(unaudited)
(US$ in thousands)
Property, Plant and
Equipment       
256
697
759
496
479
Total             
256
697
759
496
479
We will continue to make capital expenditures to support the expected growth of our
business and our expansion plans. We intend to fund these future capital expenditures with
financial resources available to us, including our existing cash and bank balances, cash flows
generated from our financing activities and net proceeds from the Global Offering.
FINANCIAL INFORMATION
– 460 –




## 承销佣金与超额配售（AO–AQ）

- `col_AO` = Underwriting Commission (% of fund raised HK (a) (type=number unit=decimal missing=NaN)
- `col_AP` = Underwriting Commission (% of fund raised Int.(b) (type=number unit=decimal missing=NaN)
- `col_AQ` = Over-allotment Option (%) (type=number unit=decimal missing=NaN)
- `col_CI` = Listing expenses (HK$) (type=number unit=HKD missing=NaN)

### 原文切片：承销佣金与超额配售（AO–AQ）


<<<PAGE 49>>>
“Hong Kong” or “HK”
the Hong Kong Special Administrative Region of the
PRC
“Hong Kong Offer Shares”
the 1,269,480 Class A Ordinary Shares (subject to
reallocation as described in the section headed “Structure
of the Global Offering”) initially offered by our Company
for subscription at the Offer Price pursuant to the Hong
Kong Public Offering
“Hong Kong Public Offering”
the
offering
of
the
Hong
Kong
Offer
Shares
for
subscription by the public in Hong Kong (plus brokerage
of 1.0%, SFC transaction levy of 0.0027%, AFRC
transaction
levy
of
0.00015%
and
Stock
Exchange
trading fee of 0.00565%), on and subject to the terms and
conditions described in “Structure of the Global Offering
— The Hong Kong Public Offering”
“Hong Kong Share Registrar”
Tricor Investor Services Limited
“Hong Kong Stock Exchange”
or “Stock Exchange”
The Stock Exchange of Hong Kong Limited, a wholly-
owned subsidiary of Hong Kong Exchanges and Clearing
Limited
“Hong Kong Takeovers Code”
or “Takeovers Code”
the Codes on Takeovers and Mergers and Share Buy-
backs issued by the SFC, as amended, supplemented or
otherwise modified from time to time
“Hong Kong Underwriters”
the underwriters of the Hong Kong Public Offering listed
in the section headed “Underwriting — Hong Kong
Underwriters”
“Hong Kong Underwriting
Agreement”
the underwriting agreement dated December 30, 2025,
relating to the Hong Kong Public Offering entered into
by,
among
others,
our
Company,
the
Controlling
Shareholders and the Overall Coordinators, as further
described
in
the
section
headed
“Underwriting
—
Underwriting Arrangements and Expenses — Hong Kong
Public Offering — Hong Kong Underwriting Agreement”
DEFINITIONS
– 39 –

<<<PAGE 50>>>
“ICP License(s)”
the value-added telecommunications business operation
licence (增值電信業務經營許可證) issued by MIIT with a
service
scope
of
Internet
information
service,
a
subcategory of value-added telecommunication service
under the Classification Catalogue Telecommunications
Services (《電信業務分類目錄》)
“IFRSs”
the IFRS Accounting Standards, which include standards,
amendments
and
interpretations
promulgated
by
International Accounting Standards Board
“IIT Law”
the Individual Income Tax Law of the PRC (《中華人民
共和國個人所得稅法》)
“Independent Third Party(ies)”
any person(s) or entity(ies) who is not a connected person
of the Company within the meaning of the Listing Rules
“International Offer Shares”
the 24,119,740 Class A Ordinary Shares offered by our
Company pursuant to the International Offering (subject
to
reallocation
as
described
in
the
section
headed
“Structure of the Global Offering”) together with any
additional Class A Ordinary Shares which may be allotted
and issued by our Company pursuant to the exercise of
the Offer Size Adjustment Option and the Over-allotment
Option
“International Offering”
the conditional placing of the International Offer Shares
by the International Underwriters at the Offer Price
outside the United States in offshore transactions in
reliance on Regulation S, and in the United States only to
QIBs in reliance on Rule 144A or any other available
exemption from registration under the US Securities Act,
in each case on and subject to the terms and conditions of
the International Underwriting Agreement, as further
described
in
the
section
headed
“Underwriting
—
International Offering”
“International Sanctions Legal
Advisor”
Hogan Lovells International LLP, our legal advisor on
international sanctions laws
“International Underwriters”
the group of international underwriters who are expected
to enter into the International Underwriting Agreement to
underwrite the International Offering
DEFINITIONS
– 40 –

<<<PAGE 51>>>
“International Underwriting
Agreement”
the underwriting agreement relating to the International
Offering expected to be entered into on or about
January 7, 2026 by our Company and the International
Underwriters, as further described in the section headed
“Underwriting — International Offering”
“Joint Bookrunners”
the joint bookrunners as named in the section headed
“Directors and Parties Involved in the Global Offering”
“Joint Global Coordinators”
the joint global coordinators as named in the section
headed “Directors and Parties Involved in the Global
Offering”
“Joint Lead Managers”
the joint lead managers as named in the section headed
“Directors and Parties Involved in the Global Offering”
“Joint Sponsors”
the Joint Sponsors as named in the section headed
“Directors and Parties Involved in the Global Offering”
“Latest Practicable Date”
December 21, 2025, being the latest practicable date for
the purpose of ascertaining certain information contained
in this Prospectus prior to its publication
“Local Linearity”
Local Linearity Inc., a company with limited liability
incorporated in the BVI on August 28, 2023 and one of
our Controlling Shareholders
“Listing”
the listing of our Shares on the Main Board
“Listing Committee”
the listing committee of the Hong Kong Stock Exchange
“Listing Date”
the date, expected to be on or about January 9, 2026, on
which our Shares are to be listed and on which dealings
in our Shares are to be first permitted to take place on the
Stock Exchange
“Listing Rules”
the Rules Governing the Listing of Securities on The
Stock Exchange of Hong Kong Limited (as amended,
supplemented or otherwise modified from time to time)
“M&A Rules”
the Regulations on Mergers and Acquisitions of Domestic
Enterprises by Foreign Investors (《關於外國投資者併購
境內企業的規定》)
DEFINITIONS
– 41 –

<<<PAGE 52>>>
“Main Board”
the
stock
exchange
(excluding
the
option
market)
operated by the Stock Exchange which is independent
from and operated in parallel with the GEM of the Hong
Kong Stock Exchange
“Memorandum” or
“Memorandum of Association”
the amended and restated memorandum of association of
our Company, conditionally adopted on December 29,
2025, with effect from the Listing Date, as amended from
time to time, a summary of which is set out in Appendix
III to this Prospectus
“MiniMax Awakening”
MiniMax Awakening Limited (formerly MiniMax LMM
Holding Limited), a company with limited liability
incorporated in the BVI on November 23, 2021, and one
of our Controlling Shareholders
“MiniMax Gene”
MiniMax Gene Limited, a company with limited liability
incorporated in the BVI on November 23, 2021
“MiniMax HongKong”
MiniMax Hongkong Tech Limited, a limited company
incorporated in Hong Kong on April 10, 2025, and a
wholly-owned subsidiary of our Company
“MiniMax Matrix”
MiniMax
Matrix
Limited,
a
company
with
limited
liability incorporated in the BVI on June 29, 2021, and
one of our Controlling Shareholders
“MOFCOM” or “Ministry of
Commerce”
the Ministry of Commerce of the PRC (中華人民共和國
商務部) (formerly known as the Ministry of Foreign
Trade and Economic Cooperation of the PRC (中華人民
共和國對外經濟貿易部))
“Ms. Yun”
Ms. Yun Yeyi (貟燁禕), one of our executive Directors
and our chief operating officer
“NDRC”
the National Development and Reform Commission (中
華人民共和國國家發展和改革委員會)
“Nomination Committee”
the nomination committee of the Board
“NPC”
the National People’s Congress of the PRC (中華人民共
和國全國人民代表大會)
DEFINITIONS
– 42 –

<<<PAGE 53>>>
“Offer Price”
the final offer price per Offer Share (exclusive of
brokerage of 1%, SFC transaction levy of 0.0027%, Hong
Kong Stock Exchange trading fee of 0.00565% and
AFRC transaction levy of 0.00015%), expressed in Hong
Kong dollars, at which Hong Kong Offer Shares are to be
subscribed
for
pursuant
to
the
Hong
Kong
Public
Offering and International Offer Shares are to be offered
pursuant to the International Offering, to be determined
as described in “Structure of the Global Offering —
Pricing and Allocation”
“Offer Share(s)”
the Hong Kong Offer Shares and the International Offer
Shares, together, where relevant, with any additional
Shares to be issued by our Company pursuant to the
exercise of the Offer Size Adjustment Option and the
Over-allotment Option
“Offer Size Adjustment Option”
the option expected to be granted by us under the
International
Underwriting
Agreement
to
the
International Underwriters, exercisable by the Overall
Coordinators (for themselves and on behalf of the
International
Underwriters),
pursuant
to
which
our
Company may allot and issue up to an aggregate of
3,808,380 additional Shares (representing in aggregate
approximately 15.0% of the Offer Shares initially being
offered under the Global Offering assuming the Over-
allotment Option is not exercised) at the Offer Price, to
cover any excess market demand in the International
Offering (without being subject to any reallocation
mechanism), as described in “Structure of the Global
Offering — Offer Size Adjustment Option”
“Overall Coordinators”
the overall coordinators as named in the section headed
“Directors and Parties involved in the Global Offering”
“Over-allotment Option”
the option expected to be granted by our Company to the
International Underwriters, exercisable by the Overall
Coordinators (for themselves and on behalf of the
International Underwriters), to require our Company to
allot and issue additional Shares to the International
Underwriters
to,
among
other
things,
cover
over-
allocations in the International Offering, if any, details of
which are described in “Structure of the Global Offering
— Over-allotment Option”
DEFINITIONS
– 43 –

<<<PAGE 54>>>
“Overseas Listing Trial
Measures”
The
Trial
Administrative
Measures
of
Overseas
Securities Offering and Listing by Domestic Companies
and five supporting guidelines (《境內企業境外發行證券
和上市管理試行辦法》及五項配套指引) promulgated by
the CSRC on February 17, 2023 and became effective on
March 31, 2023
“Post-IPO Share Incentive Plan”
the
post-IPO
share
incentive
plan
adopted
by
the
Company on December 29, 2025, with effect upon the
Listing, the principal terms of which are set out in the
section headed “Statutory and General Information — D.
Share Incentive Plans — 2. Post-IPO Share Incentive
Plan” in Appendix IV of this Prospectus
“PRC Company Law”
the Company Law of the People’s Republic of China (中
華人民共和國公司法),
as
amended,
supplemented
or
otherwise modified from time to time
“PRC Legal Advisor”
Jingtian & Gongcheng, our legal advisor on PRC laws in
connection with the Global Offering
“Pre-IPO Investment(s)”
the investment(s) in our Company undertaken by the
Pre-IPO Investors prior to this initial public offering,
details of which are set out in “History, Reorganization
and Corporate Structure”
“Pre-IPO Investor(s)”
Holder(s) of Shares pursuant to the Pre-IPO Investments,
details of which are set out in the section headed
“History, Reorganization and Corporate Structure”
“Pre-IPO Share Incentive Plan”
refers to the pre-IPO share incentive plan adopted by the
Company, as amended from time to time, the principal
terms of which are set out in the section headed
“Statutory and General Information — D. Share Incentive
Plans — 1. Pre-IPO Share Incentive Plan” in Appendix
IV of this Prospectus
“Preferred Share(s)”
preferred shares(s) in the share capital of the Company,
including the Series Angel Preferred Shares, the Series
Pre-A Preferred Shares, the Series A Preferred Shares, the
Series A+ Preferred Shares, the Series Pre-B Preferred
Shares, the Series Pre-B+ Preferred Shares and the Series
Pre-B++ Preferred Shares
DEFINITIONS
– 44 –

<<<PAGE 55>>>
“Price Determination Agreement”
the agreement to be entered into between our Company
and the Overall Coordinators (for themselves and on
behalf of the Underwriters) on the Price Determination
Date to record the Offer Price
“Price Determination Date”
the date, expected to be on or about January 7, 2026 on
which the Offer Price is determined, or such later time as
the Overall Coordinators (for themselves and on behalf of
the Underwriters) and our Company may agree, but in
any event no later than 12:00 noon on January 7, 2026
“Prospectus”
this prospectus being issued in connection with the Hong
Kong Public Offering
“QIB(s)”
qualified institutional buyer(s) within the meaning of
Rule 144A
“Regulation S”
Regulation S under the U.S. Securities Act
“Remuneration Committee”
the remuneration committee of the Board
“Renminbi” or “RMB”
the lawful currency of the PRC
“Reorganization”
the reorganization conducted by the Group described in
the
section
headed
“History,
Reorganization
and
Corporate Structure — Corporate Reorganization” in this
Prospectus
“Reserved Matters”
those matters resolutions with respect to which each
Share is entitled to one vote at general meetings of the
Company pursuant to Rule 8A.24 of the Hong Kong
Listing
Rules,
being:
(i)
any
amendment
to
the
Memorandum and Articles, (ii) the variation of the rights
attached to any class of Shares, (iii) the appointment or
removal of an independent non-executive Director, (iv)
the appointment or removal of the Company’s auditors,
and (v) the voluntary liquidation or winding-up of the
Company
“RSUs”
restricted share units
“Rule 144A”
Rule 144A under the U.S. Securities Act
“SAFE”
the State Administration of Foreign Exchange of the PRC
(中華人民共和國國家外匯管理局)
DEFINITIONS
– 45 –

<<<PAGE 56>>>
“SAMR”
the State Administration for Market Regulation of the
PRC (中華人民共和國國家市場監督管理總局)
“Sanctioned Target”
any person or entity (i) designated on any list of targeted
persons or entities issued under the sanctions-related law
or regulation of a Relevant Jurisdiction; (ii) that is, or is
owned or controlled by, a government of a sanctioned
country; or (iii) that is the target of sanctions under the
law or regulation of a Relevant Jurisdiction because of a
relationship of ownership, control, or agency with a
person or entity described in (i) or (ii)
“SAT”
the State Taxation Administration of the PRC (中華人民
共和國國家稅務總局)
“SFC”
the Securities and Futures Commission of Hong Kong
“SFO” or “Securities and
Futures Ordinance”
the Securities and Futures Ordinance, Chapter 571 of the
Laws of Hong Kong, as amended, supplemented or
otherwise modified from time to time
“Shanghai Jizhi Wujie”
Shanghai Jizhi Wujie Technology Co., Ltd. (上海極智無
界科技有限公司),
a
limited
liability
company
incorporated in the PRC on April 18, 2025, and is
controlled by Dr. Yan, hence a connected person of the
Company
“Shanghai Jizhi Zongheng”
Shanghai Jizhi Zongheng Technology Co., Ltd. (上海極
智縱橫科技有限公司),
a
limited
liability
company
incorporated in the PRC on April 23, 2025, and is
wholly-owned by Jizhi Wujie, which was ultimately
controlled by Dr. Yan, hence a connected person of the
Company
“Shanghai MiniMax”
Shanghai Xiyu Technology Co., Ltd. (上海稀宇科技有限
公司), a limited liability company established in China on
January 28, 2023, a wholly owned subsidiary of the
Company
“Shanghai Jizhi”
Shanghai Xiyu Jizhi Technology Co., Ltd. (上海稀宇極智
科技有限公司), a limited liability company established in
the
PRC
on
November
3,
2021,
a
wholly
owned
subsidiary of the Company
DEFINITIONS
– 46 –

<<<PAGE 57>>>
“Share(s)”
ordinary and/or preferred shares in the share capital of
our Company of US$0.0001 each
“Shareholder(s)”
holder(s) of our Share(s)
“Stabilizing Manager”
China International Capital Corporation Hong Kong
Securities Limited
“State Council”
the State Council of the PRC (中華人民共和國國務院)
“subsidiary(ies)”
has the meaning ascribed thereto under the Listing Rules
“substantial shareholder(s)”
has the meaning ascribed thereto under the Listing Rules
“Track Record Period”
the
period
comprising
three
financial
years
ended
December 31, 2022, 2023 and 2024 and the nine months
ended September 30, 2025
“treasury shares”
has the meaning ascribed thereto under the Listing Rules
“U.S. persons”
U.S. persons as defined in Regulation S
“U.S. Securities Act”
United States Securities Act of 1933, as amended,
supplemented or otherwise modified from time to time
“Underwriters”
the Hong Kong Underwriters and the International
Underwriters
“Underwriting Agreements”
the Hong Kong Underwriting Agreement and/or the
International Underwriting Agreement, as the context
may require
“United States”, “USA” or
“U.S.”
the
United
States
of
America,
its
territories
and
possessions, any State of the United States, and the
District of Columbia
“USD”, “US$” or “U.S. dollars”
United States dollar, the lawful currency of the United
States
“VAT”
value-added tax
DEFINITIONS
– 47 –

<<<PAGE 58>>>
“WVR Beneficiary(ies)”
has the meaning ascribed to it under the Hong Kong
Listing Rules and unless the context otherwise requires,
refers to each of Dr. Yan and Ms. Yun, being the holder
of the Class B Ordinary Shares upon Listing
“WVR structure”
has the meaning ascribed to it under the Hong Kong
Listing Rules
“%”
per cent
DEFINITIONS
– 48 –

<<<PAGE 59>>>
This glossary of technical terms contains explanations of certain technical terms
used in this Prospectus. As such, these terms and their meanings may not correspond to
standard industry meanings or usage of these terms.
“AI”
artificial intelligence, a branch of computer science that
develops
systems
capable
of
performing
tasks
that
typically require human intelligence, such as perception,
learning, reasoning, and decision-making
“AIGC”
Artificial Intelligence Generated Content, content such as
text, visual, and audio created automatically by artificial
intelligence technologies without direct human creation
“AI agent”
an
intelligent
system
capable
of
autonomously
performing specific tasks on behalf of a user to achieve a
proposed goal
“AI Infrastructure”
the integrated set of hardware, software, data systems, or
cloud resources necessary for training and inferencing AI
models
“AI music synthesis model”
an artificial intelligence system designed to generate or
compose
music
by
learning
patterns
from
existing
musical data, enabling creation of original melodies,
harmonies, and rhythms
“AI-native”
refers to products, services, or systems that are built from
the ground up with artificial intelligence as a core
component, rather than integrating AI as an add-on.
AI-native
solutions
are
designed
to
leverage
AI
technologies
in
their
fundamental
architecture
and
functionality
“AI-powered Multi-modal
Entertainment Platform”
a platform that uses artificial intelligence to enable
agents to process and respond to multiple types of inputs,
allowing more natural and versatile interactions
“API”
a set of rules and tools that allows different software
systems to communicate and interact with each other
“API Platform”
a system that provides standardized interfaces allowing
developers to access and integrate a company’s services
or data into their own applications
GLOSSARY OF TECHNICAL TERMS
– 49 –

<<<PAGE 60>>>
“app” or “application”
application software designed to run on smartphones and
other mobile devices
“Asia-Pacific”
A geographic region comprising countries in East Asia,
South Asia, Southeast Asia, and Oceania, often including
Australia and New Zealand
“attention”
the sophisticated mechanism that enables the foundation
model to weigh the importance of different parts of its
input data when processing information
“Audio Generation Tool”
software that uses AI to create synthetic audio content,
including speech, music, or sound effects, based on user
input or predefined parameters
“auto-regressive model”
a type of statistical model that uses past values of a time
series to predict future values of that same time series
“B2B” or “2B” or “ToB”
“business-to-business”, refers to commercial transactions
or relationships between businesses rather than between a
business and individual consumers
“B2C” or “2C” or “ToC”
“business-to-consumer”,
refers
to
commercial
transactions or relationships between a business and
individual consumers
“benchmark”
standardized evaluation frameworks used to measure and
compare the performance of language models
“CAGR”
compound annual growth rate
“Chat Completions API”
an
application
programming
interface
that
allows
developers to build interactive chat experiences by
generating
AI-driven
responses
in
a
conversational
format, typically based on large language models
“chain-of-thought” or “CoT”
a
reasoning
technique
where
the
model
generates
intermediate reasoning steps or explanations to solve
complex problems
“Diffusion Model”
a type of generative model in machine learning that
excels at creating high-quality data, particularly images
and text, by gradually adding noise to a data point and
then learning to reverse this process
GLOSSARY OF TECHNICAL TERMS
– 50 –

<<<PAGE 61>>>
“DiT”
diffusion models with transformers, a type of diffusion
model that utilizes the transformer architecture as its
backbone for image generation
“ELO”
a rating system used to assess the relative skill levels of
players in competitive games or activities, where a higher
score indicates stronger performance
“ESG”
environmental, social and governance
“fine-tuning”
the process of adapting a pre-trained foundation model to
perform a specific task or specialize in a particular
domain with higher accuracy and relevance
“Flow-VAE”
a hybrid AI model combining Variational Autoencoders
and normalizing flows to improve the quality and
flexibility of generated data by capturing complex data
distributions more effectively
“foundation model”
a large-scale, pre-trained model developed on broad and
diverse datasets designed to serve as a general-purpose
model that can be used for solving a wide variety of tasks
“fps”
frames per second, a measure of how many individual
frames (images) are displayed or generated each second
in a video or animation. Higher fps results in smoother
motion
“freemium”
a business model that offers basic services or products
free of charge while charging for premium features,
advanced functionality, or enhanced experiences.
“GDP”
gross domestic product, the total monetary value of all
goods and services produced within a country’s borders
during a specific period, commonly used to measure the
size and health of a country’s economy
“generative AI”
a type of artificial intelligence that creates new content
by learning patterns from existing data and generating
original outputs
“GPU”
Graphics Processing Unit, a processor that handles many
tasks at once, widely used in AI to speed up model
training and data processing
GLOSSARY OF TECHNICAL TERMS
– 51 –

<<<PAGE 62>>>
“High and New Technology
Enterprise”
refers to an enterprise established in the PRC that is
recognized by the competent government authorities as
meeting
the
prescribed
criteria
in
terms
of
core
independent intellectual property rights, research and
development
capability,
technology
and
product
offerings, and revenue composition from high and new
technology-related businesses. Enterprises with such
designation are entitled to a preferential PRC corporate
income tax rate of 15%, subject to fulfilment of the
relevant requirements
“HTML”
HyperText Markup Language, the standard language used
to create and structure content on the web, defining
elements such as text, images, links, and layout in web
pages
“IDC”
International Data Corporation (IDC), a global market
intelligence, data, and events provider for the information
technology,
telecommunications,
and
consumer
technology markets
“Image Generation & Music
Generation API”
an
application
programming
interface
that
enables
developers to create images and music programmatically
using AI models, allowing automated generation of visual
and audio content based on user inputs
“image-to-video” or “I2V”
a technology or model that generates video sequences
from a single image or a series of images, creating motion
and transitions to produce dynamic video content
“inference activities”
the computational processes through which a trained
foundation model is deployed to generate outputs or
responses based on new user inputs or data. Inference
takes place after the model has been trained and involves
applying the model’s learned parameters to perform
reasoning, prediction or content generation in real time.
For example, when a user inputs a prompt or message in
our MiniMax app and receives a generated text produced
by
the
underlying
foundation
model,
such
model
computation constitutes an inference activity
“inference cost”
the cost of computational resources needed to use a
trained AI model to process inputs and generate outputs
GLOSSARY OF TECHNICAL TERMS
– 52 –

<<<PAGE 63>>>
“inference latency”
the time delay between providing inputs to an AI model
and receiving outputs from the model
“Intelligent Agent Application”
a software application powered by AI that can understand
and respond to user inputs in natural language, enabling
interactive and human-like conversations for customer
service, information retrieval, or other purposes
“large model”, “large language
model” or “LLM”
advanced AI models trained on massive amounts of text
data to understand, generate, and interact using human
language. They are capable of performing a wide range of
natural
language
processing
tasks,
such
as
text
generation,
translation,
summarization,
and
question
answering
“large-scale hybrid-attention
reasoning model”
an AI technique that combines two different attention
mechanisms: one is the computationally expensive but
high-precision traditional attention (Softmax Attention),
and the other is the fast, less resource-intensive linear
attention (Lightning Attention). The model uses the fast
linear attention for most of the text processing and only
activates the high-precision traditional attention for
critical parts. This design allows the AI to efficiently
process extremely long texts at a lower computational
cost, achieving a balance between performance and
efficiency
“linear attention” or “linear
attention mechanism”
an
efficient
attention
mechanism
that
reduces
the
computational complexity of traditional attention from
quadratic to linear, enabling faster processing of long
input sequences while preserving key information
“long context processing
capacity”
the ability of an AI model to understand, retain, and make
use of extremely long sequences of input data, such as
lengthy texts, conversations, or documents, allowing it to
maintain
context
and
coherence
over
extended
interactions with users
GLOSSARY OF TECHNICAL TERMS
– 53 –

<<<PAGE 40>>>
Future Plans and Use of Proceeds
We estimate that we will receive net proceeds from the Global Offering of approximately
HK$3,818.3 million, after deducting underwriting commissions, fees and estimated expenses
payable by us in connection with the Global Offering, assuming the Offer Size Adjustment
Option or Over-allotment Option is not exercised and an Offer Price of HK$158.00 per Offer
Share, being the midpoint of the indicative Offer Price range stated in this Prospectus.
We intend to use the net proceeds of the Global Offering for the following purposes:
•
Approximately 90%, or HK$3,436.4 million of the net proceeds will be used for our
research and development over the next five years including the development of our
foundation models and our AI-native products. Specifically, (i) approximately
70.0%, or HK$2,672.8 million, of the net proceeds over the next five years to the
research and development of our foundation models; and (ii) approximately 20.0%,
or HK$763.7 million, of the net proceeds over the next five years to the
development, refinement and global scaling of our AI-native products.
•
Approximately 10.0%, or HK$381.8 million, of the net proceeds will be allocated to
working capital and general corporate purposes.
See “Future Plans” and “Use of Proceeds” for details.
DIVIDEND AND DIVIDEND POLICY
No dividend was paid or declared by us or any of our subsidiaries since our incorporation.
After the Track Record Period and up to the date of this Prospectus, we did not declare any
dividends to our Shareholders. As of the Latest Practicable Date, we did not have a formal
dividend policy or a fixed dividend distribution ratio. Any declaration and payment as well as
the amount of dividends will be subject to our Articles and the Cayman Companies Act. We
currently do not have any dividend policy to guide our dividends declaration or payments. Our
board of directors has the discretion to pay interim dividends and to recommend to
Shareholders to pay final dividends, and will depend on a number of factors, including our
earnings, capital requirements, overall financial condition and contractual restrictions. See
“Financial Information — Dividends.”
IMPACT OF THE COVID-19 PANDEMIC DURING THE TRACK RECORD PERIOD
COVID-19 did not have any material impact on the Group’s business, operation or
financial condition during the Track Record Period because the Group’s core business activities
are performed by distributed engineering teams and are inherently remote-compatible, its
products are provided online through cloud infrastructure rather than offline channels, and it
has limited reliance on physical supply chains or on-site deployment and did not experience
any material project delays, customer cancellations, revenue shortfalls or credit losses
attributable to the pandemic.
SUMMARY
– 30 –

<<<PAGE 41>>>
RECENT DEVELOPMENTS
As of the Latest Practicable Date, we had not experienced any material impact from
tariffs, export controls, or other trade-related measures imposed by governmental authorities in
the jurisdictions in which we operate. Although certain countries, including the United States,
have in recent periods introduced or adjusted tariffs and related policies on goods and
technologies, such measures have not had a material adverse effect on our operations, financial
condition or prospects to date. We continue to monitor relevant developments and assess their
potential implications for our business.
Our Directors confirm that, up to the date of this Prospectus, there has been no material
adverse change in our financial or trading position or prospects since September 30, 2025,
being the end date of the periods reported in the Accountant’s Report set out in Appendix I, and
there is no event since September 30, 2025 that would materially affect the information shown
in the Accountant’s Report set out in Appendix I.
We anticipate a significant increase in net loss for the year ended December 31, 2025,
primarily due to the expected R&D expenses as we continue to elevate the intelligence level
of our foundation models and fair value loss on financial liabilities, as the valuation of our
company is expected to increase in 2025.
RECENT REGULATORY DEVELOPMENT
Outbound Investment Rules
Effective on January 2, 2025, the final rule issued Treasury to implement the executive
order of August 9, 2023 (the “Final Rule”) imposes investment prohibition and notification
requirements on U.S. Persons for a wide range of investments in entities associated with China
(including Hong Kong and Macau) that are engaged in activities relating to three sectors: (i)
semiconductors and microelectronics, (ii) quantum information technologies, and (iii) AI
systems. U.S. persons subject to the Final Rule are prohibited from making, or required to
report, certain investments in covered foreign persons, which are defined as “covered
transactions,” and include acquisitions of equity interests (including contingent equity
interests), certain debt financing, joint ventures, and certain investments as a limited partner
in a non-U.S. person pooled investment fund. Since our principal place of business is in China
and we engage in the development of certain AI models, we are likely to be deemed as a
“covered foreign person” as described in the Final Rule. Based on information we provided to
our international sanctions advisor, it appears likely that some U.S. persons that purchase our
Shares in the Global Offering or are the parents of non-U.S. person subsidiaries that purchase
our Shares in the Global Offering would be required to file notifications regarding their or their
subsidiaries’ purchases with Treasury no later than 30 days after such purchases of the Shares.
See “Risk Factors — Risks Related to Our Business and Industry — We are subject to the risks
associated with international trade policies, geopolitics and trade protection measures. Changes
in international relationships, trade and investment policies, trade protection and investment
restriction measures may adversely impact our business, financial condition and results of
operations.”
SUMMARY
– 31 –

<<<PAGE 42>>>
Export Control Regulations
In recent years, the United States has expanded export controls restrictions on China
through the Export Administration Regulations (the “EAR”), administered by the Bureau of
Industry and Security of the United States Department of Commerce (the “BIS”). The United
States in recent years has placed an increasing number of entities, including a number of
entities in China, on the Entity List and other restricted or prohibited parties lists. In addition
to naming additional persons to these lists, BIS has imposed complex and restrictive rules
applicable to doing business with persons on them. For example, on September 29, 2025, the
BIS issued an immediately effective interim final rule that extended Entity List and Military
End-User List restrictions to entities that are 50% or more owned, directly or indirectly, by
shareholders on those lists. The U.S. Government has indicated that implementation of the
Affiliate Rule will be delayed for at least one year (i.e., until October 2026). These recent
measures together with the U.S. export control regime regulate the export, reexport and
transfer of U.S. products, software, and technology, including certain items manufactured
outside the United States that contain greater than de minimis controlled U.S. content or are
the foreign direct product of certain U.S. software or technology.
Tariff Regulations
We are also closely monitoring potential changes in tariff policy and assessing the
potential impact of such policy changes on our business operations and financial performance.
For example, recently, the United States proposed to impose multiple rounds of tariffs on a
wide range of goods imported from multiple countries, including China, and China responded
with retaliatory tariffs. As advised by our international legal advisor, U.S. import tariffs only
apply of export of physical goods to the United States. On such basis, it is of the view of our
Directors that, given that we do not export physical goods to the United States, U.S. tariffs are
unlikely to have a material adverse impact on our business operations and financial
performance. As relevant policies are rapidly evolving, it may be difficult to evaluate these
tariff measures’ potential future impacts. See “Risk Factors — Risks Related to Our Business
and Industry — We are subject to the risks associated with international trade policies,
geopolitics and trade protection measures. Changes in international relationships, trade and
investment policies, trade protection and investment restriction measures may adversely impact
our business, financial condition and results of operations.”
AI Chatbot Regulations
Several U.S. states, including California, New York, Maine, and Utah, have recently
enacted laws that specifically regulate AI-powered chatbots. These laws impose new
operational requirements, such as clear and recurring user disclosures, and mandate the
implementation of safety protocols to prevent harmful content, particularly related to
self-harm. For example, California’s law, effective January 2026, includes specific protections
for minors and establishes a private right of action allowing for statutory damages.
SUMMARY
– 32 –

<<<PAGE 43>>>
We are in the process of reviewing these regulations to ensure the continued compliance
of our Talkie application. Based on (i) an assessment of the current features and functionalities
of Talkie and (ii) research conducted on existing state legislation and regulations governing
chatbots, as advised by our U.S. data legal advisor, (a) the current features and design of Talkie
are already in material compliance with the chatbot laws currently in force in Utah, New York
and Maine; and (b) Talkie is not subject to the chatbot laws currently enacted in other U.S.
states, as such laws regulate functions that Talkie does not offer, such as the provision of
medical services.
Guided by legal advice from our U.S. data legal advisor, we are currently implementing
the updates necessary for compliance with the upcoming chatbot law in California. These
updates primarily involve reviewing our user interface, supplementing certain mandatory
disclosures and incorporating required safety features. Such updates are consistent with our
ordinary product-development cycle for Talkie and are expected to be completed within a
reasonable timeframe and at a reasonable cost. We are currently designing and implementing
these updates and expect to complete the process by the end of 2025, ahead of the California
chatbot law’s anticipated effective date in January 2026. Based on our planned timetable and
the progress made to date, as advised by our U.S. data legal advisor, Talkie is expected to be
in compliance with the requirements under the California chatbot law, once it is enacted in
January 2026.
In light of the abovementioned view of our U.S. data legal advisor, although compliance
with these state-level regulations may result in certain incremental operational costs, we do not
expect such regulations to have any material adverse effect on our business, results of
operations or financial condition. For further details regarding our AI safety and alignment
measures, safeguards against inappropriate or harmful outputs and user misuse, and our
ongoing efforts to ensure responsible AI development, please refer to the section headed
“Business — Research and Development.”
SUMMARY
– 33 –

<<<PAGE 44>>>
In this Prospectus, unless the context otherwise requires, the following terms shall
have the meanings set out below. Certain other terms are explained in the section headed
“Glossary of Technical Terms” in this Prospectus.
“Accountant’s Report”
the accountant’s report of our Company, the text of which
is set out in Appendix I to this Prospectus
“affiliate(s)”
with respect to any specified person, any other person,
directly or indirectly, controlling or controlled by or
under direct or indirect common control with such
specified person
“AFRC”
Accounting and Financial Reporting Council (會計及財
務匯報局)
“Alpha EXP”
Alpha EXP Limited, a business company incorporated in
the BVI on November 23, 2021, and one of our
Controlling Shareholders
“Articles” or “Articles of
Association”
the amended and restated articles of association of our
Company with effect upon the Listing Date (as amended
from time to time), a summary of which is set out in
Appendix III to this Prospectus
“associate(s)”
has the meaning ascribed thereto under the Listing Rules
“Audit Committee”
the audit committee of the Board
“Beijing Jizhi”
Beijing Xiyu Jizhi Technology Co., Ltd. (北京稀宇極智
科技有限公司) (formerly known as Mingri Zhimeng
(Beijing) Technology Co., Ltd. (名日之夢(北京)科技有限
公司)), a limited liability company established in the
PRC
on
November
18,
2021
and
a
wholly-owned
subsidiary of the Company
“Board”, “Board of Directors”
or “our Board”
the board of Directors of the Company
“Business Day”
a day on which banks in Hong Kong are generally open
for normal business to the public and which is not a
Saturday, Sunday or public holiday in Hong Kong
“BVI”
the British Virgin Islands
DEFINITIONS
– 34 –

<<<PAGE 45>>>
“Capital Market Intermediaries”
or “capital market
intermediary(ies)” or “CMI(s)”
the capital market intermediaries participating in the
Global Offering and has the meaning ascribed thereto
under the Listing Rules
“CCASS”
the Central Clearing and Settlement System established
and operated by HKSCC
“China” or “the PRC”
the People’s Republic of China, unless the context
requires otherwise, excluding, for the purposes of this
Prospectus only, the regions of Hong Kong, Macau and
Taiwan of the People’s Republic of China
“CIC”
China Insights Industry Consultancy Limited (灼識行業
諮詢有限公司),
an
independent
professional
market
research and consulting company
“Circular 37”
the Notice of the SAFE on Issues Concerning Foreign
Exchange Administration of the Overseas Investment and
Financing and the Round-Tripping Investment Made by
Domestic Residents through Special-Purpose Companies
(《國家外匯管理局關於境內居民通過特殊目的公司境外
投融資及返程投資外匯管理有關問題的通知》)
“Class A Ordinary Shares”
Class A ordinary shares in the share capital of the
Company with a par value of US$0.0001 each, conferring
a holder of a Class A ordinary share one vote per share on
all matters subject to the vote at general meetings of the
Company
“Class B Ordinary Shares”
Class B ordinary shares in the share capital of the
Company with a par value of US$0.0001 each, conferring
weighted voting rights in the Company such that a holder
of a Class B ordinary share is entitled to ten votes per
share on all matters subject to the vote at general
meetings of the Company, subject to the requirements
under Rule 8A.24 of the Hong Kong Listing Rules that
the Reserved Matters shall be voted on a one vote per
share basis
“close associate(s)”
has the meaning ascribed thereto under the Listing Rules
DEFINITIONS
– 35 –

<<<PAGE 484>>>
HONG KONG UNDERWRITERS
China International Capital Corporation Hong Kong Securities Limited
UBS AG Hong Kong Branch
Goldman Sachs (Asia) L.L.C.
Morgan Stanley Asia Limited
Futu Securities International (Hong Kong) Limited
Tiger Brokers (HK) Global Limited
UNDERWRITING
This prospectus is published solely in connection with the Hong Kong Public Offering.
The Hong Kong Public Offering is fully underwritten by the Hong Kong Underwriters on a
conditional basis. The Company expects the International Offering to be fully underwritten by
the International Underwriters. If, for any reason, the Offer Price is not agreed between the
Overall Coordinators (for themselves and on behalf of the Underwriters) and the Company, the
Global Offering will not proceed and will lapse.
The Global Offering comprises the Hong Kong Public Offering of initially 1,269,480
Hong Kong Offer Shares (subject to reallocation on the basis as set out in “Structure of the
Global Offering” in this prospectus) and the International Offering of initially 24,119,740
International Offer Shares (subject to reallocation on the basis as described in “Structure of the
Global Offering” in this prospectus as well as to the Offer Size Adjustment Option and the
Over-allotment Option).
As the Company is likely to be deemed as a “covered foreign person” as described in the
Final Rule, certain Underwriters have informed the Company that they may consider making
notifications with the U.S. Department of the Treasury. None of the Underwriters has any
obligation to inform the Company or any investor if they later decide that they will not file such
notifications.
UNDERWRITING ARRANGEMENTS AND EXPENSES
Hong Kong Public Offering
Hong Kong Underwriting Agreement
The Hong Kong Underwriting Agreement was entered into on December 30, 2025.
Pursuant to the Hong Kong Underwriting Agreement, the Company is offering the Hong Kong
Offer Shares for subscription on the terms and conditions set out in this prospectus, and the
Hong Kong Underwriting Agreement at the Offer Price.
UNDERWRITING
– 474 –

<<<PAGE 485 起已省略：超出 underwriting 字符上限；请人工复核覆盖范围>>>



## 主营业务与上市途径（AR–AS）

- `col_AR` = Principal business / industry (type=text unit=text missing=NA)
- `col_AS` = Listing route / applicable chapter (type=text unit=text missing=NA)
- `col_BF` = Technology commercialization stage (type=text unit=text missing=NA)
- `col_BG` = Debt repayment (% of planned net IPO proceeds) (type=number unit=decimal missing=NaN)

### 原文切片：主营业务与上市途径（AR–AS）


<<<PAGE 83>>>
•
more limited protection for intellectual property rights in some countries.
Our failure to manage any of these risks successfully could harm our international
operations, and adversely affect our business, operating results and financial condition.
AI technologies carry certain inherent safety risks, which may adversely affect our
business and reputation.
AI technologies carry certain inherent risks and challenges that may adversely affect
public perception of our business. Any inappropriate, abusive or premature usage of AI
technologies, whether actual or perceived, whether intended or inadvertent, and whether by us
or by third parties, may dissuade prospective users from adopting AI-native products, may
impair the general acceptance of AI-native products by the society, attract negative publicity
and adversely impact our reputation. Specific risks relating to AI technologies may include,
among others: (i) fraudulent activity, such as the creation of convincing fake images, videos,
and text that can be used to create deepfakes, impersonations, and forged documents for
fraudulent purposes; (ii) misinformation and disinformation, such as the generation of realistic
and
convincing
synthetic
media
that
could
be
used
to
spread
misinformation
and
disinformation; (iii) privacy concerns, such as the creation of synthetic identities or
manipulation of personal data, which may raise privacy concerns; (iv) cybersecurity threats,
such as the creation of sophisticated phishing attacks or bypass of security measures, which
may increase the risk of cyberattacks and data breaches; and (v) safety and alignment
challenges, particularly as AI systems become more advanced and capable.
Adverse user behaviours and misuse of AI-native products may also cause, or be alleged
to cause, harm to users or third parties, including by promoting or facilitating self-harm,
suicide or other violent conduct, or by creating undue emotional dependence, particularly
among minors or other vulnerable persons. In this regard, certain AI companies have been sued
in connection with allegations that their chatbot products contributed to users’ self-harm or
suicide.
In addition, adverse user behaviours may result in heightened scrutiny by platform
operators and other regulators, and could lead to enforcement actions such as takedowns,
suspensions, distribution restrictions, age-gating requirements or other remedial measures that
may materially reduce user acquisition, engagement and monetisation. For the temporary
removal of the Talkie app from Apple’s App Store, please refer to “Risk Factors – Any
restriction on access to major distribution channels, such as the iOS App Store, Google Play
or the Internet, or any failure to maintain stable relationships with such channels, could
materially and adversely affect our user growth and business performance”.
If similar incidents were to occur in relation to our products or services, we could be
subject to significant legal and regulatory exposure (including civil claims alleging negligence,
wrongful death, product liability, failure-to-warn or consumer-protection violations), as well as
other enforcement actions, product changes or usage restrictions. Even if such claims are
ultimately unsuccessful, defending against them could be costly and time-consuming, could
RISK FACTORS
– 73 –

<<<PAGE 84>>>
divert management attention, could require increased spending on safety, compliance and
customer support, and could cause reputational harm, any of which could materially and
adversely affect our business, operations and financial performance.
We may face significant challenges in ensuring that our AI-native products behave in a
manner that is safe, reliable, and aligned with human values. As AI models grow more
complex, there is an inherent risk that they may exhibit unintended behaviors, pursue goals
misaligned with user or societal interests, or fail to perform as expected in high-stakes or novel
situations. For example, advanced AI systems could develop emergent capabilities, such as
strategic planning or deception, that were not anticipated during their development.
Additionally, the rapid pace of AI progress may exacerbate safety risks, as competitive
pressures or the deployment of untrustworthy AI systems by third parties could lead to harmful
outcomes. If we are unable to address these safety challenges effectively, any real or perceived
failures in the safety or alignment of our AI systems could result in reputational damage,
regulatory scrutiny and a loss of user trust, all of which could materially and adversely affect
our business, operations, and financial performance.
In addition to these safety-related concerns, we are subject to a complex and evolving
regulatory landscape governing internet content. Applicable government and regulatory
authorities have adopted regulations governing content contained within videos, audios,
images and other information over the internet. Under these regulations, internet content
providers are prohibited from posting or displaying content that, among other things, violates
applicable laws and regulations, impairs the national dignity of certain countries or the public
interest, or is obscene, superstitious, fraudulent, violent or defamatory on the internet. Internet
content providers are also prohibited from displaying content that may be deemed by relevant
government authorities as illegal or inappropriate.
We allow our users to produce content using our AI-native products and generate outputs
via our foundation models. These outputs may include various forms of media such as text,
video, audio, and image, some of which may feature our proprietary watermarks. We
implement measures to identify and restrict content that may be prohibited under applicable
government regulations. However, we cannot guarantee that all generated content will be
identified or restricted in a timely manner, or that it will fully comply with all relevant laws
and regulations.
If we are unable to protect or promote our brand and reputation, our business may be
materially adversely affected. Negative publicity or rumors about us, our products, our
management, directors, employees, shareholders, users, business partners or their
affiliates or our industry in general may adversely affect our reputation and business.
We must maintain and enhance our brand identity while increasing market awareness of
the reputation of our business and products. The successful promotion of our brand depends on
our ability to achieve widespread acceptance of our products, attract and retain users, maintain
our current market share, and successfully differentiate our products from those of our
competitors.
RISK FACTORS
– 74 –

<<<PAGE 85>>>
Achieving these goals require substantial expenditures, and we anticipate expenses to
increase as we expand into new markets. In addition to marketing and advertising costs, we
may need to invest in customer support, public relations, community engagement, and
compliance mechanisms to reinforce positive brand perception. However, there is no assurance
that these investments will result in increased revenue, or that any revenue growth will be
sufficient to offset the associated expenses.
Moreover, even isolated incidents, such as unintended outputs generated by our
foundation models, miscommunication by company representatives, or negative feedback from
influential users or media, can quickly escalate online and undermine years of brand-building
efforts. Damage to our brand or reputation could lead to user attrition, reduced pricing power,
increased customer acquisition costs, or reluctance from potential partners and investors to
engage with us. Any of these factors could materially and adversely affect our business,
financial condition, results of operations and growth prospects.
The technology infrastructure we relied on and our products may experience system
failures, interruptions, security breaches, cyberattacks, or other technical inadequacies.
Our brand, reputation, business, financial conditions or results of operations may be
materially and adversely affected if we fail to effectively identify and rectify these
problems in a timely manner.
The technology infrastructure we relied on and products may encounter disruptions or
other outages caused by problems or defects in our own technologies and systems, such as
malfunctions in software or network overload. The technology infrastructure we relied on may
also be vulnerable to damage or interruption caused by security breaches, cyberattacks, human
error or other technical inadequacies. The occurrence of unanticipated problems that affect the
technology infrastructure we relied on could result in interruptions in the availability of our
products. It may be difficult for us to respond to such interruptions in a timely manner, or at
all. Such interruptions may affect the ability of users to use our products, which would damage
our reputation, reduce our future revenues, harm our future profits, subject us to regulatory
scrutiny and lead our users to seek alternative products.
It is possible that our security controls and other security practices we follow may not
prevent the improper access to or disclosure of personal data or proprietary information. We
also rely on systems provided by third parties, which may also suffer security breaches or
unauthorized access to or disclosure of personal data or proprietary information. Additionally,
our business involves the processing, storage, transmission and processing of confidential and
user data, including user data, and the deployment of our IT resources in a safe and secure
manner that does not expose our network systems to security breaches or the loss of data. Any
data security incidents, including internal malfeasance by our employees, unauthorized access
or usage, virus or similar breach or disruption of us or our service providers could result in loss
of confidential or proprietary information or personal data, damage to our reputation, loss of
users, litigation, regulatory investigations, fines, penalties and other liabilities. Accordingly, if
our cybersecurity measures or those of our users fail to protect against unauthorized access,
attacks (which may include sophisticated cyber-attacks), the compromise or mishandling of
RISK FACTORS
– 75 –

<<<PAGE 86>>>
data, or other misconduct or malfeasance, including by computer hackers, employees,
contractors, vendors, users and business partners, as well as software bugs, human error or
technical malfunctions, then our reputation, business, operating results and financial condition
could be adversely affected.
Furthermore, the technology infrastructure we relied on is also vulnerable to damages
from fires, floods, earthquakes and other natural disasters, power loss and telecommunications
failures. Any network interruption or inadequacy that causes interruptions to our operations, or
failure to maintain the network and server or solve such problems in a timely manner, could
reduce our user satisfaction, which in turn could adversely affect our reputation, business and
financial condition.
Flaws in our foundation model products, including programming errors or defects in our
models, whether real or perceived, could adversely affect our user experience and market
acceptance of our products, which may materially and adversely affect our reputation,
business and results of operations.
The technology underlying our AI-native products is inherently complex and may contain
material defects or errors, particularly when new products are first introduced, when new
features or capabilities are released or when integrated with new or updated third-party
hardware or software. Our foundation model products are subject to frequent updates, and may
contain bugs or flaws that can only become apparent when the updates are accessed by a
number of users, especially when we launch updates under a tight schedule. We have from time
to time received user feedback pertaining to programming errors. We cannot assure you that we
will be able to detect and resolve all these programming errors effectively and in a timely
manner. Any real or perceived programming errors or defects may adversely affect user
experience, cause users to refrain from subscribing for our products, or cause our enterprise
customers to reduce their use of our products, result in negative publicity and performance
issues, any of which could materially and adversely affect our business and results of
operations. Correcting such defects or errors may be costly and time consuming. Moreover, the
harm to our reputation and legal liability related to such real or perceived defects or errors may
be substantial and would harm our business.
We make certain of our models and products available on an open-source basis and may
use open-source technology, which may pose particular risks to our business.
We strongly believe in open-source collaboration and we make certain of our models and
products available on an open-source basis. By opening our technologies, we allow third
parties, including competitors, to access, use, modify, or redistribute them, which could limit
our ability to commercialize those technologies or differentiate ourselves in the marketplace.
Specifically, our competitors may develop their own products using our open-source
technology to compete with us, potentially reducing the demand for our products.
RISK FACTORS
– 76 –

<<<PAGE 87>>>
In addition, we may from time to time, use open-source technology in certain of our
operations and expect to continue using certain open-source technology in the future. There
remains a risk that third parties may assert claims of ownership or seek to enforce the terms
of open-source licenses. Such claims may include demands for the release of open-source
components, derivative works, or even our proprietary source code developed using open-
source technology. These claims could lead to litigation and divert management attention and
resources. Moreover, the terms of many open-source licenses have not been interpreted by
courts, creating a risk that these licenses could be construed in a way that could impose
unanticipated conditions or restrict our ability to commercialize our products. In such an event,
we may be required to seek licenses from third parties to continue commercially offering our
products, to make our proprietary code generally available in source code form, to re-engineer
our products or to discontinue the sale of our products if re-engineering could not be
accomplished on a timely basis, any of which could adversely affect our business, financial
condition and results of operations.
Any restriction on access to major distribution channels, such as the iOS App Store,
Google Play or the Internet, or any failure to maintain stable relationships with such
channels,
could
materially
and
adversely
affect
our
user
growth
and
business
performance.
Users of some of our products need to access the Internet and major app distribution
channels such as Apple’s App Store, Google Play, and other well-known app stores, to
download certain of our AI-native products. Any disruption, restriction, suspension, or removal
of our mobile apps from these third-party distribution channels, or any changes to their terms,
review policies, or technical requirements, could materially impact our ability to acquire users
and deliver our products. For example, in December 2024, a prior version of our Talkie app was
temporarily removed from Apple’s App Store in certain jurisdictions for a period of
approximately two months. To the best of our knowledge, such temporary removal of the Talkie
app from Apple’s App Store was not due to any product default or illegality, and Apple did not
specify the reasons for such removal. As a result, from mid-December 2024 to the
mid-February 2025, such prior version of Talkie app could not be downloaded from the Apple’s
App Store in certain jurisdictions, and the average daily downloads of Talkie app decreased by
approximately 16.8 thousand compared with its average level prior to such removal. During
such period, we made certain adjustments to the product features of our Talkie app to enhance
its risk management and user experience. Since mid-February 2025, the updated Talkie app has
been made available for download on Apple’s App Store. If any of our current or future mobile
apps are restricted, removed or otherwise disrupted in their access to these distribution
channels — whether due to technical issues, platform concerns, evolving content standards,
geopolitical sensitivities, or other factors — we may face reputational harm, reduced user
growth, and our financial condition and results of operations may be materially and adversely
affected.
Moreover, laws and regulations or government authorities may block or limit the access
to the Internet generally or these distribution channels for reasons of security, confidentiality,
data privacy or other concerns, and there is no assurance that we will be able to maintain stable
RISK FACTORS
– 77 –

<<<PAGE 88>>>
relationships with these distribution channels. Any restriction on access to the Internet in
general or these distribution channels or the failure to maintain relationship with these
distribution channels could result in the loss of existing users, slower user growth, or increased
distribution and customer acquisition costs. In case an important distribution channel is
inaccessible, we will resort to other distribution channels available to us. That said, our
business, results of operations and prospects may be materially and adversely affected by
limited access to distribution channels.
Our success depends on the continued contributions of our senior management and key
employees. Failure to attract, recruit, retain, and motivate such qualified personnel could
materially and adversely affect our business and growth prospects.
The business of the Company is highly dependent on certain individuals whose
leadership, vision, and technical expertise are not readily replaceable. The market for
high-caliber workers and leaders in our industry is extremely competitive. To execute our
business strategies successfully, we must attract, retain and motivate our senior management
and key employees. In particular, hiring qualified executives, scientists, engineers, technical
staff and research and development personnel is costly and critical to our business.
Competition for personnel results in increased costs in the form of cash and stock-based
compensation. Nonetheless, we must recruit and develop diverse qualified personnel to remain
competitive in our industry. If one or more of our key employees, including senior executives
or core technical personnel, were to depart unexpectedly, such departures could disrupt our
operations, delay product development or strategic initiatives, and result in the loss of valuable
institutional knowledge. Effective succession planning is also important to our long-term
success. Failure to ensure effective transfer of knowledge and smooth transitions involving key
employees could hinder our strategic planning and execution. If we are less successful in our
recruiting efforts, or if we cannot retain key employees or their knowledge, our ability to
develop and deliver successful products may be adversely affected. Such events may also lead
to reputational harm, decreased employee morale, and potential reluctance from customers or
partners to continue existing or prospective engagements.
The interpretation and application of employment-related laws to our workforce practices
may result in increased operating costs and less flexibility in how we meet our workforce
needs. Changes in immigration and work permit laws and regulations or the administration or
interpretation of such laws or regulations could impair our ability to attract and retain highly
qualified employees. If we do not continue to anticipate and address the needs of our
employees sufficiently and/or in a timely manner, their productivity could be impacted, or we
could fail to retain them, which could have a material adverse impact on our future business
operations, results of operations and financial condition.
RISK FACTORS
– 78 –

<<<PAGE 89>>>
We face risks related to changes in global and regional macroeconomic conditions,
geopolitical tensions, regional conflicts, terrorist activities, natural disasters, health
epidemics and other outbreaks of contagious diseases, and other force majeure events, any
of which could materially and adversely affect our business operations, financial
condition, results of operations and prospects.
Uncertainties about global economic conditions, regulatory changes, geopolitical tensions
and other factors, including fluctuation of interest rates, inflation level, unemployment, labor
and healthcare costs, access to credit, consumer confidence and other macroeconomic factors
may pose risks and materially and adversely affect demand for our products. A deteriorating
global economic outlook could result in a slowdown in business investment, tighter budget
allocations for technology spending, and greater pricing sensitivity among customers, which
may in turn reduce the market adoption of our products and services.
The escalated Palestinian-Israeli conflict, the conflict in Ukraine and the imposition of
broad economic sanctions on Russia have disrupted global supply chains and triggered
uncertainty across financial markets. Unrest, terrorist threats and the potential for war in the
Middle East and elsewhere may increase volatility and risk aversion in global capital markets.
In addition, the evolving trade relationships between China and other countries — particularly
regarding tariffs, treaties, and government regulations — may have profound implications on
cross-border business activities, cost structures, and our ability to access certain markets. Such
developments
may
affect
the
macroeconomic
environment,
both
domestically
and
internationally, and could have a direct or indirect impact on the markets in which we operate.
Geopolitical, economic and market conditions, including factors such as the liquidity of
the global financial markets, the level and volatility of debt and equity prices, interest rates,
currency and commodities prices, investor sentiment, inflation and the availability and cost of
capital and credit have been affecting, and will continue to affect the countries where we
operate. There is considerable uncertainty over the long-term effects of the expansionary
monetary and fiscal policies adopted by the central banks and financial authorities of some of
the world’s leading economies.
There have been concerns over unrest and terrorist threats in the Middle East, Europe and
Africa and over the conflicts involving Ukraine and Syria. The slow economic recoveries
around the world and the high inflation, high interest environment have contributed to higher
global volatility. These developments may adversely impact global liquidity, heighten market
volatility and increase U.S. dollar funding costs resulting in tightened global financial
conditions and fears of a recession. It is unclear whether these challenges and uncertainties will
be contained or resolved, and what effects they may have on the global political and economic
conditions in the long term. It remains unclear whether these challenges and uncertainties will
be resolved in the near future, and their potential long-term effects on the global political and
economic landscape remain difficult to predict. Any severe or prolonged slowdown in the
global or PRC economy may materially and adversely affect our business, results of operations
and financial condition.
RISK FACTORS
– 79 –

<<<PAGE 90>>>
In addition, natural disasters such as floods, earthquakes, sandstorms, snowstorms, fire or
drought, the outbreak of a widespread health epidemic or any severe epidemic disease such as
SARS, Ebola, Zika or the COVID-19, acts of war, terrorism or other force majeure events
beyond
our
control
may
disrupt
our
research
and
development,
manufacturing
and
commercialization activities and business operations, all of which could adversely affect our
business, results of operations, financial condition and prospects.
We are subject to the risks associated with international trade policies, geopolitics and
trade protection measures. Changes in international relationships, trade and investment
policies, trade protection and investment restriction measures may adversely impact our
business, financial condition and results of operations.
Our operations may be negatively affected by trade policies, geopolitics and other trade
protection measures administered by the government authorities in the countries in and with
which we operate, including, but not limited to, regulation of economic and labor conditions,
increased duties, taxes and other costs. Margins on sales of our products in certain countries
could be materially and adversely affected by international trade regulations, including duties,
tariffs and antidumping penalties. In addition to trade policy measures, the United States and
certain other governments have imposed and may adopt additional sanctions, export controls
and other regulatory measures that directly or indirectly affect technology companies based in
certain jurisdictions. Due to the global presence of our business, we are potentially impacted
by changes in international trade and investment policies, escalations of tensions in
international relations, and increased scrutiny from regulatory authorities, particularly given
recent trade negotiations between the United States and China, which has resulted in and may
continue to cause changes in international trade policies and additional barriers to trade. Such
regulatory measures are complex and subject to frequent changes, and the interpretation and
enforcement of the relevant regulations may change from time to time, which may be driven
by political and/or other factors that are not within our control or that are heightened by
national security and foreign policy concerns.
For instance, in recent years, the United States has expanded sanctions and export control
restrictions on China through the EAR, administered by BIS. These regulations are designed,
in part, to restrict the access by Chinese companies to sensitive U.S. technologies, particularly
in industries like telecommunications, artificial intelligence, and semiconductors. In recent
years, the United States has expanded sanctions and export controls restrictions on China
through the Export Administration Regulations (the “EAR”), administered by the Bureau of
Industry and Security of the United States Department of Commerce (the “BIS”). For instance,
in October 2022, BIS issued an interim final rule (the “BIS October 2022 IFR”) requiring
license for exports, re-exports, or transfers of any item subject to the EAR when there is
“knowledge” that the item is destined for end use in the development or production of ICs at
a fab in China that fabricates ICs meeting certain criteria. On December 2, 2024, BIS issued
an interim final rule (the “BIS December 2024 IFR”) and a final rule (the “BIS December 2024
FR”), which expanded controls in the EAR on advanced computing and semiconductor
manufacturing items. Separately, BIS issued the so-called “Affiliate Rule” that expanded the
scope of the Entity List and Military End-User List to include entities owned 50 percent or
RISK FACTORS
– 80 –

<<<PAGE 91>>>
more directly or indirectly, individually or in the aggregate, by one or more listed parties. The
U.S. Government has indicated that implementation of the Affiliate Rule will be delayed for
at least one year (i.e., until November 2026). These recent measures together with the U.S.
export control regime regulate the export, reexport and transfer of U.S. products, software, and
technology, including certain items manufactured outside the United States that contain greater
than de minimis controlled U.S. content or are the foreign direct product of certain U.S.
software or technology. Export licenses may be required depending on the nature of the items,
destination, end-use, end-user and other parties to the relevant transactions.
Our AI products were developed by us without direct using material U.S. software or
technology, or incorporating material components procured from U.S. suppliers. We engage
certain U.S. service providers in our ordinary course of business to support the operations of
our international business. The services provided by such U.S. service providers could
generally be replaced by suppliers in other jurisdictions around the world, at comparable
quality and price, and we therefore believe that our R&D activities and operations are not
reliant on technology or raw materials of U.S.-origin to any material extent. However, if any
uncertainties in U.S.-China relationship or any resulted disruption to our supply chains will
make it necessary for us to make such transition, such transition may take time to complete,
and cause certain delays or disruptions to our ordinary course of business, and may therefore
adversely affect our business, results of operations and financial conditions.
In addition to disrupting our supply chain in the U.S., export controls could also adversely
impact the ability of our technology vendors in China to procure certain hardware or related
services for their provision of services to us, which may have a material adverse impact on our
operations. In the future, as similar or more expansive restrictions may be imposed by different
jurisdictions, we will need to maintain heightened internal control and risk management
policies to ensure sound compliance with such restrictions, which requires significant
resources and efforts. Furthermore, such potential restrictions may materially and adversely
affect our and our technology partners’ abilities to acquire technologies, systems, devices or
components that may be critical to business operations. Any of these developments could affect
us, our users and/or suppliers or economic conditions generally, any of which could adversely
affect our business and financial condition.
As advised by our international sanctions legal advisor, during the Track Record Period
and up to the Latest Practicable Date, our Group has not been subject to sanctions, and we have
not engaged in any material activities in comprehensively sanction countries, or entered into
material service contract with any customers that are targets of U.S. sanctions. Therefore, as
advised by our international sanctions legal advisor, we have been in compliance with rule and
laws in US export control and sanctions in all material aspects, and U.S. sanctions are not
likely to have any material adverse impact on us.
Our business operations is impacted not only by rules and laws related to export control,
but also by changes in regulations governing cross-border investment policies. Changes in
international investment policies, particularly with regard to China, could materially and
adversely impact our business and operating results. In particular, in January 2025, a U.S. rule
RISK FACTORS
– 81 –

<<<PAGE 92>>>
went into effect that prohibits or requires the submission of notifications in connection with
U.S. outbound investment in Chinese-affiliated companies engaged in certain activities
involving
specified
sensitive
technologies
sectors
(artificial
intelligence
(“AI”),
semiconductors and microelectronics, and quantum information technologies) and issued a
broadly worded “America First Trade Policy” and an “America First Investment Policy” that
seek to further restrict U.S. investments involving China (including possibly expanding
technologies subject to the U.S. outbound investment regime and narrowing related exceptions
(including those related to publicly traded securities)). In addition, effective on January 2,
2025, the final rule issued by the U.S. Department of the Treasury to implement the executive
order of August 9, 2023 (the “Final Rule”) imposes investment prohibition and notification
requirements on U.S. Persons for a wide range of investments in entities associated with China
(including Hong Kong and Macau) that are engaged in activities relating to three sectors: (i)
semiconductors and microelectronics, (ii) quantum information technologies, and (iii) AI
systems. The Final Rule could limit our ability to raise capital or contingent equity capital from
U.S. investors after this Global Offering given that relevant laws, regulations, and policies
continue to evolve. See “— We are subject to the risks associated with sanctions and export
controls laws and regulations, and developing domestic and foreign laws and regulations on AI
and related technologies, and our business, financial condition and results of operations could
be materially and adversely affected.”
We are closely monitoring potential changes in tariff policy and assessing the potential
impact of such policy changes on our business operations and financial performance. For
example, recently, the United States proposed to impose multiple rounds of tariffs on a wide
range of goods imported from multiple countries, including China, and China responded with
retaliatory tariffs. Since February 2025, both countries raised reciprocal tariffs on each other’s
imported goods to 125%. However, on May 12, 2025, both the U.S. and China modified these
tariff measures: the U.S. removed the 125% tariff and temporarily reduced tariffs on Chinese
goods to 10% by suspending a 24% duty for 90 days. The PRC government announced the same
tariff adjustments, removing the 125% retaliatory tariff and cutting tariffs on U.S. goods from
34% to 10% for the same period. These policies have adversely affected the global economy
and financial markets. On August 12, 2025, both the U.S. and China announced the extension
of these tariff measures for another 90 days. On October 30, 2025, the United States announced
it would further reduce tariffs by 10% but otherwise the tariffs by China and the United States
remains in place. As advised by our international sanctions legal advisor, U.S. import tariffs
only apply of export of physical goods to the United States. On such basis, it is of the view of
our Directors that, given that we do not export physical goods to the United States, U.S. tariffs
are unlikely to have a material adverse impact on our business operations and financial
performance. As relevant policies are rapidly evolving, it may be difficult to evaluate these
tariff measures’ potential future impacts.
Geopolitical conflicts may also lead to volatility in financial markets, fluctuations in
currency exchange rates, increased procurement costs and declines in trading prices of our
Class A Ordinary Shares. In extreme cases, such conflicts could result in economic downturns
that materially and adversely impact our operations. It is unclear whether these challenges and
RISK FACTORS
– 82 –

<<<PAGE 246>>>
OVERVIEW
MiniMax is a global AI foundation model company. Founded by a group of forward-
thinking engineers, we are committed to driving AI innovation towards performing the full
range of human intellectual tasks, from learning and reasoning to planning and generalizing
knowledge across diverse domains.
The foundation model market is expanding at an unprecedented pace, rapidly reshaping
human society. The global foundation model market is projected to exceed US$300 billion by
2030. IDC estimates that AI will cumulatively contribute US$19.9 trillion to the global
economy through 2030 and drive 3.5% of global GDP in 2030. We believe we have established
a solid foundation to capture this market potential and have already made meaningful progress.
Our Journey
Our journey has been guided by a clear vision since inception centered on two key areas:
developing advanced foundation models and creating AI-native products that enhance
productivity and enrich life. Recognizing that real-world human interaction is inherently
multi-modal, we stand out as one of the few foundation model developers who are committed
to developing multi-modal models from day one. We take a cost-efficient approach in pursuing
AI advancement, delivering high performance while ensuring our technological breakthroughs
remain accessible and affordable to users globally. We adopted the Mixture-of-Experts (MoE)
architecture and hybrid attention mechanism at an early stage, which significantly reduced
computation resources while maintaining globally recognized performance.
Large 
Language 
Model
Product 
Launching
2022
2023
2024
2025
OPEN Platform
Video 
Generation 
Model
Audio Model
abab 1
abab 5.5 abab 6.0 (MoE)
Text-01
M1
M2
Hailuo-01
Hailuo-02
Music-01
Speech-02
Music-02
oi
d
u
A
x
a
M
i
n
i
M
e
y
g
n
i
X
/ei
k
la
T
MiniMax 
(with Agent)
Speech-01
BUSINESS
– 236 –

<<<PAGE 247>>>
We have been consistently iterating our models to higher intelligence levels. Today, our
proprietary foundation model suite, led by MiniMax-M2, Hailuo-02, and Speech-02, has long
context processing capacity and can understand, generate, and integrate a wide range of
modalities, including text, video, and audio. These models power our major AI-native products
— including MiniMax, Hailuo AI, MiniMax Audio, Talkie/Xingye, and our enterprise and
developer-facing Open Platform, delivering intelligent and dynamic experiences to users
globally.
As of September 30, 2025, our AI-native products had cumulatively served over
200 million individual users across over 200 countries and regions, and more than 100
thousand enterprises and developers across over 100 countries and regions.
Scalability
We believe scalability is pivotal to our long-term goal. To build one of the most scalable
AI businesses globally, we focus on three core competencies — original research, a sustainable
business model, and organizational efficiency. These pillars support both continuous model
advancement and product commercialization at scale. Together, the three core competencies
enable an elevated level of intelligence for everyone—powering productivity and enriching
life.
Original Research
•
Multi-modal Focus. We are among the first globally to pursue a multi-modal technology
strategy, and we commenced the development of models across multiple modalities in
2022. Our models consistently rank at the top across text, video, and speech benchmarks,
reflecting a systematic advantage in multi-modal architecture that empowers the
development of more scalable models and AI-native products.
•
Enhanced AI
Infrastructure.
We
have
prioritized
and
significantly
enhanced AI
infrastructure efficiency, achieving persistent improvement in training performance and
significantly
reducing
overall
inference
costs.
Our
proprietary AI
infrastructure
dynamically allocates computing resources, ensuring service availability and supporting
sustainable large-scale delivery of high-performance foundation models.
Sustainable Business Model
•
Technology as Product. We focus on developing scalable AI systems optimized for
real-world use cases. This strategy has enabled us to develop and commercialize
high-performing models across multiple modalities. Based on these foundation models,
we have developed a suite of AI-native products that serve both individual users,
developers and enterprise customers across a broad range of application scenarios. Our
multi-pronged
monetization
enables
a
self-reinforcing
cycle
of
innovation
and
commercial value, which further allows us to continuously reinvest in original research
and development.
BUSINESS
– 237 –

<<<PAGE 248>>>
•
Global Operations. From day one, we have launched all our foundation models and
products across international markets with one goal: to make next-generation AI
technologies truly broadly accessible at compelling value proposition. Our concurrent
growth across multiple international markets demonstrates the effectiveness of our global
approach and the strength of our technological moat.
Organizational Efficiency
•
Our flat, nimble organization enables model iteration, integration between research and
product, and scaling across model and product development. We operate with no more
than three layers beneath the CEO and structure teams around project-based missions
rather than rigid departmental silos. This dynamic setup empowers early ownership, fast
talent development fosters deep collaboration across tech, product, and business
functions, and facilitates the progression of research innovations toward real-world
launch and impact.
OUR MODELS AND PRODUCT OFFERINGS
Our Foundation Model Suite
We have leveraged our R&D capabilities to build a comprehensive suite of foundation
models, and maintain competitiveness across various modalities. Our foundation model suite
includes large language models, video generation models, and models for speech and music
generation.
Large Language Model: MiniMax
The MiniMax M Series, comprising MiniMax-M1 and MiniMax-M2, represents our
flagship family of large language models. MiniMax-M1, launched in June 2025, is an
open-source, large-scale hybrid-attention reasoning model. It adopts a hybrid MoE architecture
combined with a lightning attention mechanism, enabling long-context processing with a
context window of up to 1 million tokens and supporting the development of more capable AI
agents.
MiniMax-M2, our latest large language model, is engineered for elite performance in
coding and agentic tasks. Leveraging a carefully engineered, data-efficient MoE architecture
and activation-parameter design, MiniMax-M2 delivers higher-performance capabilities at
substantially faster inference speeds compared with MiniMax-M1, while maintaining an
optimized profile across model intelligence, responsiveness and cost-efficiency.
BUSINESS
– 238 –

<<<PAGE 249>>>
Video Generation Model: Hailuo-02
The Hailuo-02 series model generates high-quality video content from a variety form of
information inputs. Commercialized at scale with competitive results on global benchmarks
upon its release, Hailuo-02 offers cinematic video quality, advanced prompt adherence, smooth
motion, and style diversity. With user-friendly interface and ability to do aesthetic refinement,
it helps content creators and advertisers produce compelling videos out of simple prompts.
Speech Generation Model: Speech-02
The Speech-02 model series is designed to generate natural, high-quality speech from text
input. Widely recognized as a top performing speech model globally upon its release in April
2025, our Speech-02 model delivers hyper-realistic, personalized voice synthesis across
multiple languages.
Our AI-Native Product Offerings
Leveraging our multi-modal foundation model suite, we deliver AI-native products and
services that unleash the power of AI to benefit both individual users, developers and enterprise
customers around the world. The evolution of our AI-native products is rooted in advancements
in its underlying foundation models. Through continuous iterations and upgrades of foundation
models and the development of new ones, we are able to design and create AI-native products
with enhanced productivity and user experience.
MiniMax: Intelligent Agent Application
MiniMax is our intelligent AI agent application, which is designed to autonomously
perform a wide range of tasks through natural language instructions. Supported by our
foundation models, MiniMax Agent can plan, reason, and execute complex actions such as
coding, research, document drafting, and presentation creation within a unified workspace.
Hailuo AI: Flagship Visual Generation Platform
Hailuo AI fully integrates our Hailuo-02 model that has quickly become one of the
world’s most popular AI image and video creation platforms through organic user adoption. It
is offered in both web and app forms, and is designed for real-time, high-quality image and
video generation.
MiniMax Audio: Advanced Audio Generation Tool
MiniMax Audio is designed to provide users with high-fidelity audio generation
capabilities. Accessible via web platform, MiniMax Audio integrates the Company’s Speech-02
model to support interactive audio synthesis and generate natural, high-quality speech from
text input.
BUSINESS
– 239 –

<<<PAGE 250 起已省略：超出 business 字符上限；请人工复核覆盖范围>>>



## 基石投资者名单（CJ）

- `col_CJ` = Cornerstone investor names (type=text unit=investor_names missing=NA)

### 原文切片：基石投资者名单（CJ）


<<<PAGE 389>>>
THE CORNERSTONE PLACING
We have entered into cornerstone investment agreements (each a “Cornerstone
Investment Agreement”, and together the “Cornerstone Investment Agreements”) with the
cornerstone investors set out below (each a “Cornerstone Investor”, and together the
“Cornerstone Investors”), pursuant to which the Cornerstone Investors have agreed to,
subject to certain conditions, subscribe at the Offer Price for a certain number of Offer Shares
that
may
be
purchased
for
an
aggregate
amount
of
approximately
US$350
million
(approximately HK$2,723 million) (the “Cornerstone Placing”). The calculations in this
section, which are based on the exchange rates as disclosed in the section headed “Information
about this Prospectus and the Global Offering”, are for illustration purpose.
Assuming an Offer Price of HK$151.0, being the low-end of the indicative Offer Price
range set out in this Prospectus, the total number of Offer Shares to be subscribed by the
Cornerstone Investors would be 18,034,240 Offer Shares. The table below reflects the
shareholding percentage immediately after the completion of the Global Offering assuming
there is no other change made to the issued share capital of our Company between the Latest
Practicable Date and the Listing Date (or the date of exercise of Over-allotment Option (where
applicable)).
Assuming the Offer Size Adjustment Option
is not exercised
Assuming the Offer Size Adjustment Option
is exercised in full
Assuming the
Over-allotment Option
is not exercised
Assuming the
Over-allotment Option
is exercised in full
Assuming the
Over-allotment Option
is not exercised
Assuming the
Over-allotment Option
is exercised in full
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
71.03%
5.90%
61.77%
5.83%
61.77%
5.83%
53.71%
5.75%
Assuming an Offer Price of HK$158.0, being the mid-point of the Offer Price range set
out in this Prospectus, the total number of Offer Shares to be subscribed by the Cornerstone
Investors would be 17,235,120 Offer Shares. The table below reflects the shareholding
percentage immediately after the completion of the Global Offering assuming there is no other
change made to the issued share capital of our Company between the Latest Practicable Date
and the Listing Date (or the date of exercise of Over-allotment Option (where applicable)).
Assuming the Offer Size Adjustment Option
is not exercised
Assuming the Offer Size Adjustment Option
is exercised in full
Assuming the
Over-allotment Option
is not exercised
Assuming the
Over-allotment Option
is exercised in full
Assuming the
Over-allotment Option
is not exercised
Assuming the
Over-allotment Option
is exercised in full
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
67.88%
5.64%
59.03%
5.57%
59.03%
5.57%
51.33%
5.50%
CORNERSTONE INVESTORS
– 379 –

<<<PAGE 390>>>
Assuming an Offer Price of HK$165.0, being the high-end of the Offer Price range set out
in this Prospectus, the total number of Offer Shares to be subscribed by the Cornerstone
Investors would be 16,504,040 Offer Shares. The table below reflects the shareholding
percentage immediately after the completion of the Global Offering assuming there is no other
change made to the issued share capital of our Company between the Latest Practicable Date
and the Listing Date (or the date of exercise of Over-allotment Option (where applicable)).
Assuming the Offer Size Adjustment Option
is not exercised
Assuming the Offer Size Adjustment Option
is exercised in full
Assuming the
Over-allotment Option
is not exercised
Assuming the
Over-allotment Option
is exercised in full
Assuming the
Over-allotment Option
is not exercised
Assuming the
Over-allotment Option
is exercised in full
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
65.00%
5.40%
56.53%
5.34%
56.53%
5.34%
49.15%
5.26%
Our Company is of the view that the Cornerstone Placing will help to raise the profile of
our Company and to signify that such investors have confidence in our business and prospect.
Our Company became acquainted with each of the Cornerstone Investors through the Group’s
business network, previous financing, or introduction by the Overall Coordinators and Capital
Market Intermediaries in the Global Offering.
To the best knowledge of our Company and save as that certain Cornerstone Investors are
our existing Shareholders or close associates of existing Shareholders as disclosed below, each
of the Cornerstone Investors and their respective ultimate beneficial owners (i) is an
Independent Third Party; (ii) none of the Cornerstone Investors is accustomed to taking
instructions from our Company, the Directors, chief executive, our Controlling Shareholders,
substantial shareholders, existing Shareholders or any of their respective subsidiaries or their
respective close associates in relation to the acquisition, disposal, voting or other disposition
of the Offer Shares; (iii) none of the subscription of the relevant Offer Shares by any of the
Cornerstone Investors is financed directly or indirectly by our Company, the Directors, chief
executive, our Controlling Shareholders, substantial shareholders, existing Shareholders or any
of their respective subsidiaries or their respective close associates; (iv) each Cornerstone
Investor will be utilizing their internal resources as their source of funding for the subscription
of the Offer Shares; and (v) no approval from other stock exchange is required for each
Cornerstone Investor’s investment in our Company as described in this section.
Among the Cornerstone Investors, Alisoft China (as defined below), Aspex Master Fund,
Abstract Enigma Limited, IDG Breyer Fund (as defined below), Janchor Funds (as defined
below) and MPC VII (as defined below) are our existing Shareholders or close associates of
existing Shareholders. The Stock Exchange has granted us a waiver from strict compliance
with the requirements under Rule under Rule 10.04 of the Listing Rules and consent under
paragraph 1C of Appendix F1 to the Listing Rules to permit Offer Shares in the International
Offering to be placed to certain existing Shareholders and/or their close associates. For further
details, please see the section headed “Waivers and Exemption”.
CORNERSTONE INVESTORS
– 380 –

<<<PAGE 391>>>
The Cornerstone Placing will form part of the International Offering and the Cornerstone
Investors will not subscribe for any Offer Shares under the Global Offering other than pursuant
to the Cornerstone Investment Agreements. The Offer Shares to be subscribed by the
Cornerstone Investors will rank pari passu in all respect with the fully paid Shares in issue and
will be counted towards the public float of our Company under Rule 8.08 of the Listing Rules
(except for Alisoft China). Except for Alisoft China, immediately following the completion of
the Global Offering, none of the Cornerstone Investors will become a substantial shareholder
of the Company, and the Cornerstone Investors will not have any Board representation in our
Company. Other than a guaranteed allocation of the relevant Offer Shares at the final Offer
Price, the Cornerstone Investors do not have any preferential rights in the Cornerstone
Investment Agreements compared with other public Shareholders. There are no side
arrangements between our Company and the Cornerstone Investors or any benefit, direct or
indirect, conferred on the Cornerstone Investors by virtue of or in relation to the Cornerstone
Placing.
The total number of Offer Shares to be subscribed by the Cornerstone Investors may be
affected by reallocation of the Offer Shares between the International Offering and the Hong
Kong Public Offering in the event of over-subscription under the Hong Kong Public Offering
as described in the paragraph headed “Structure of the Global Offering — The Hong Kong
Public Offering — Reallocation” in this Prospectus. The number of Offer Shares to be acquired
by each Cornerstone Investor may be reduced on a pro rata basis in accordance with the terms
of the Cornerstone Investment Agreement to satisfy the short fall, after taking into account the
requirements under Appendix F1 to the Listing Rules as well as the discretion of the Joint
Global Coordinators and the Overall Coordinators (for themselves and on behalf of the
International Underwriters) to exercise the Over-allotment Option.
There will be no delayed delivery or deferred settlement of Offer Shares to be subscribed
by the Cornerstone Investors and the consideration will be settled by the Cornerstone Investors
before the Listing Date. The Offer Shares to be subscribed by the Cornerstone Investors may
be affected by reallocation in the event of over-subscription under the Hong Kong Public
Offering, as described in “Structure of the Global Offering — The Hong Kong Public Offering
— Reallocation”. Details of the actual number of Offer Shares to be allocated to the
Cornerstone Investors will be disclosed in the allotment results announcement to be issued by
us on or around January 8, 2026.
CORNERSTONE INVESTORS
– 381 –

<<<PAGE 392>>>
OUR CORNERSTONE INVESTORS
Set out below in the aggregate number of Offer Shares, and the corresponding percentages
to the Offer Shares and our Company’s total issued share capital under the Cornerstone
Placing:
Based on the Offer Price of HK$151.0 (being the low-end of the indicative Offer Price
range)
Assuming the Offer Size Adjustment Option
is not exercised
Assuming the Offer Size Adjustment Option
is exercised in full
Cornerstone Investor
Investment
amount(1)
Number of
Offer
Shares(2)
Assuming the
Over-allotment Option
is not exercised
Assuming the
Over-allotment Option
is exercised in full
Assuming the
Over-allotment Option
is not exercised
Assuming the
Over-allotment Option
is exercised in full
(US$)
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
ADIA       
65,000,000
3,349,220
13.19%
1.10%
11.47%
1.08%
11.47%
1.08%
9.97%
1.07%
Alisoft China    
30,000,000
1,545,800
6.09%
0.51%
5.29%
0.50%
5.29%
0.50%
4.60%
0.49%
Aspex Master Fund 
35,000,000
1,803,420
7.10%
0.59%
6.18%
0.58%
6.18%
0.58%
5.37%
0.58%
Boyu       
35,000,000
1,803,420
7.10%
0.59%
6.18%
0.58%
6.18%
0.58%
5.37%
0.58%
China Universal (HK)
15,000,000
772,900
3.04%
0.25%
2.65%
0.25%
2.65%
0.25%
2.30%
0.25%
Eastspring     
15,000,000
772,900
3.04%
0.25%
2.65%
0.25%
2.65%
0.25%
2.30%
0.25%
E Fund Management 
10,000,000
515,260
2.03%
0.17%
1.76%
0.17%
1.76%
0.17%
1.53%
0.16%
IDG Breyer Fund  
15,000,000
772,900
3.04%
0.25%
2.65%
0.25%
2.65%
0.25%
2.30%
0.25%
Janchor Funds    
35,000,000
1,803,420
7.10%
0.59%
6.18%
0.58%
6.18%
0.58%
5.37%
0.58%
Martis Fund, L.P.  
15,000,000
772,900
3.04%
0.25%
2.65%
0.25%
2.65%
0.25%
2.30%
0.25%
Mirae Asset
Securities    
20,000,000
1,030,520
4.06%
0.34%
3.53%
0.33%
3.53%
0.33%
3.07%
0.33%
MPC VII      
15,000,000
772,900
3.04%
0.25%
2.65%
0.25%
2.65%
0.25%
2.30%
0.25%
Perseverance Asset
Management   
25,000,000
1,288,160
5.07%
0.42%
4.41%
0.42%
4.41%
0.42%
3.84%
0.41%
Taikang Life    
20,000,000
1,030,520
4.06%
0.34%
3.53%
0.33%
3.53%
0.33%
3.07%
0.33%
Total       
350,000,000
18,034,240
71.03%
5.90%
61.77%
5.83%
61.77%
5.83%
53.71%
5.75%
Notes:
1.
The investment amount excludes brokerage, SFC transaction levy, AFRC transaction levy and Stock Exchange
trading fee, and is calculated based on the exchange rate set out in the section headed “Information about this
Prospectus and the Global Offering — Exchange Rate Conversion” in this Prospectus. The number of Offer
Shares to be subscribed by the Cornerstone Investors are subject to the exchange rate to be determined in
accordance with each relevant Cornerstone Investment Agreement.
2.
Rounded down to the nearest whole board lot of 20 Shares, and is calculated based on the exchange rate set
out in the section headed “Information about this Prospectus and the Global Offering — Exchange Rate
Conversion” in this Prospectus.
CORNERSTONE INVESTORS
– 382 –

<<<PAGE 393>>>
Based on the Offer Price of HK$158.0 (being the mid-point of the indicative Offer Price
range)
Assuming the Offer Size Adjustment Option
is not exercised
Assuming the Offer Size Adjustment Option
is exercised in full
Cornerstone Investor
Investment
amount(1)
Number of
Offer
Shares(2)
Assuming the
Over-allotment Option
is not exercised
Assuming the
Over-allotment Option
is exercised in full
Assuming the
Over-allotment Option
is not exercised
Assuming the
Over-allotment Option
is exercised in full
(US$)
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
ADIA       
65,000,000
3,200,840
12.61%
1.05%
10.96%
1.04%
10.96%
1.04%
9.53%
1.02%
Alisoft China    
30,000,000
1,477,300
5.82%
0.48%
5.06%
0.48%
5.06%
0.48%
4.40%
0.47%
Aspex Master Fund 
35,000,000
1,723,520
6.79%
0.56%
5.90%
0.56%
5.90%
0.56%
5.13%
0.55%
Boyu       
35,000,000
1,723,520
6.79%
0.56%
5.90%
0.56%
5.90%
0.56%
5.13%
0.55%
China Universal (HK)
15,000,000
738,640
2.91%
0.24%
2.53%
0.24%
2.53%
0.24%
2.20%
0.24%
Eastspring     
15,000,000
738,640
2.91%
0.24%
2.53%
0.24%
2.53%
0.24%
2.20%
0.24%
E Fund Management 
10,000,000
492,420
1.94%
0.16%
1.69%
0.16%
1.69%
0.16%
1.47%
0.16%
IDG Breyer Fund  
15,000,000
738,640
2.91%
0.24%
2.53%
0.24%
2.53%
0.24%
2.20%
0.24%
Janchor Funds    
35,000,000
1,723,520
6.79%
0.56%
5.90%
0.56%
5.90%
0.56%
5.13%
0.55%
Martis Fund, L.P.  
15,000,000
738,640
2.91%
0.24%
2.53%
0.24%
2.53%
0.24%
2.20%
0.24%
Mirae Asset
Securities    
20,000,000
984,860
3.88%
0.32%
3.37%
0.32%
3.37%
0.32%
2.93%
0.31%
MPC VII      
15,000,000
738,640
2.91%
0.24%
2.53%
0.24%
2.53%
0.24%
2.20%
0.24%
Perseverance Asset
Management   
25,000,000
1,231,080
4.85%
0.40%
4.22%
0.40%
4.22%
0.40%
3.67%
0.39%
Taikang Life    
20,000,000
984,860
3.88%
0.32%
3.37%
0.32%
3.37%
0.32%
2.93%
0.31%
Total       
350,000,000
17,235,120
67.88%
5.64%
59.03%
5.57%
59.03%
5.57%
51.33%
5.50%
Notes:
1.
The investment amount excludes brokerage, SFC transaction levy, AFRC transaction levy and Stock Exchange
trading fee, and is calculated based on the exchange rate set out in the section headed “Information about this
Prospectus and the Global Offering — Exchange Rate Conversion” in this Prospectus. The number of Offer
Shares to be subscribed by the Cornerstone Investors are subject to the exchange rate to be determined in
accordance with each relevant Cornerstone Investment Agreement.
2.
Rounded down to the nearest whole board lot of 20 Shares, and is calculated based on the exchange rate set
out in the section headed “Information about this Prospectus and the Global Offering — Exchange Rate
Conversion” in this Prospectus.
CORNERSTONE INVESTORS
– 383 –

<<<PAGE 394>>>
Based on the Offer Price of HK$165.0 (being the high-end of the indicative Offer Price
range)
Assuming the Offer Size Adjustment Option
is not exercised
Assuming the Offer Size Adjustment Option
is exercised in full
Cornerstone Investor
Investment
amount(1)
Number of
Offer
Shares(2)
Assuming the
Over-allotment Option
is not exercised
Assuming the
Over-allotment Option
is exercised in full
Assuming the
Over-allotment Option
is not exercised
Assuming the
Over-allotment Option
is exercised in full
(US$)
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
ADIA       
65,000,000
3,065,040
12.07%
1.00%
10.50%
0.99%
10.50%
0.99%
9.13%
0.98%
Alisoft China    
30,000,000
1,414,640
5.57%
0.46%
4.85%
0.46%
4.85%
0.46%
4.21%
0.45%
Aspex Master Fund 
35,000,000
1,650,400
6.50%
0.54%
5.65%
0.53%
5.65%
0.53%
4.92%
0.53%
Boyu       
35,000,000
1,650,400
6.50%
0.54%
5.65%
0.53%
5.65%
0.53%
4.92%
0.53%
China Universal (HK)
15,000,000
707,320
2.79%
0.23%
2.42%
0.23%
2.42%
0.23%
2.11%
0.23%
Eastspring     
15,000,000
707,320
2.79%
0.23%
2.42%
0.23%
2.42%
0.23%
2.11%
0.23%
E Fund Management 
10,000,000
471,540
1.86%
0.15%
1.61%
0.15%
1.61%
0.15%
1.40%
0.15%
IDG Breyer Fund  
15,000,000
707,320
2.79%
0.23%
2.42%
0.23%
2.42%
0.23%
2.11%
0.23%
Janchor Funds    
35,000,000
1,650,400
6.50%
0.54%
5.65%
0.53%
5.65%
0.53%
4.92%
0.53%
Martis Fund, L.P.  
15,000,000
707,320
2.79%
0.23%
2.42%
0.23%
2.42%
0.23%
2.11%
0.23%
Mirae Asset
Securities    
20,000,000
943,080
3.71%
0.31%
3.23%
0.30%
3.23%
0.30%
2.81%
0.30%
MPC VII      
15,000,000
707,320
2.79%
0.23%
2.42%
0.23%
2.42%
0.23%
2.11%
0.23%
Perseverance Asset
Management   
25,000,000
1,178,860
4.64%
0.39%
4.04%
0.38%
4.04%
0.38%
3.51%
0.38%
Taikang Life    
20,000,000
943,080
3.71%
0.31%
3.23%
0.30%
3.23%
0.30%
2.81%
0.30%
Total       
350,000,000
16,504,040
65.00%
5.40%
56.53%
5.34%
56.53%
5.34%
49.15%
5.26%
Notes:
1.
The investment amount excludes brokerage, SFC transaction levy, AFRC transaction levy and Stock Exchange
trading fee, and is calculated based on the exchange rate set out in the section headed “Information about this
Prospectus and the Global Offering — Exchange Rate Conversion” in this Prospectus. The number of Offer
Shares to be subscribed by the Cornerstone Investors are subject to the exchange rate to be determined in
accordance with each relevant Cornerstone Investment Agreement.
2.
Rounded down to the nearest whole board lot of 20 Shares, and is calculated based on the exchange rate set
out in the section headed “Information about this Prospectus and the Global Offering — Exchange Rate
Conversion” in this Prospectus.
CORNERSTONE INVESTORS
– 384 –

<<<PAGE 395>>>
The following information about the other Cornerstone Investors was provided to our
Company by the Cornerstone Investors in relation to the Cornerstone Placing.
ADIA
Abu Dhabi Investment Authority (“ADIA”) is a public institution established by the
Government of the Emirate of Abu Dhabi in 1976 as an independent investment institution.
ADIA’s objective is to receive funds of the Government of Abu Dhabi allocated for investment,
and invest and reinvest those funds, for the general benefit of the Emirate of Abu Dhabi.
ADIA manages a global investment portfolio that is diversified across more than two
dozen asset classes and sub-categories including developed equities, emerging market equities,
small cap equities, government bonds, credit, fixed income, real estate, infrastructure, private
equity, cash and alternatives.
Alisoft China
Alisoft China Holding Limited (“Alisoft China”) is a limited liability company
incorporated in Hong Kong and an indirect wholly-owned subsidiary of Alibaba Group Holding
Limited (“Alibaba Group”). Alisoft China is the holding company of certain PRC subsidiaries
of Alibaba Group primarily involved in the operation of cloud computing business. Alibaba
Group is a company incorporated in the Cayman Islands, with its American depositary shares,
each representing eight ordinary shares, listed on the New York Stock Exchange (Stock
Symbol: BABA), and its ordinary shares listed on the Main Board of the Stock Exchange
(Stock Code: 9988). Alibaba Group’s mission is to make it easy to do business anywhere.
Alibaba Group aims to build the future infrastructure of commerce and envisions that its
customers will meet, work and live at Alibaba, and that it aspires to be a good company that
will last for 102 years. Alibaba Group’s core businesses are comprised of e-commerce and
cloud computing.
Aspex Master Fund
Aspex Master Fund (“AMF”) is a company incorporated and registered as a mutual fund
in the Cayman Islands. AMF is managed by Aspex Management (HK) Limited (“Aspex
Management”), a company incorporated in Hong Kong and licensed by the Securities and
Futures Commission of Hong Kong to carry out type 9 (asset management) regulated activities
in Hong Kong. Mr. Li Ho Kei is the ultimate beneficial owner of Aspex Management and
controls the voting rights of AMF, in each case through a holding entity. Mr. Li Ho Kei is an
Independent Third Party to the Company. No other investor holds an ultimate beneficial
ownership of 30% or more in AMF or Aspex Management.
CORNERSTONE INVESTORS
– 385 –

<<<PAGE 396>>>
Boyu
Abstract Enigma Limited is a company incorporated under the laws of the Cayman
Islands and a controlled subsidiary of Boyu Capital Offshore Fund. Boyu Capital Offshore
Fund is an exempted company incorporated under the laws of the Cayman Island and an
investment fund managed by Boyu Capital Management (Singapore) Pte. Ltd. (“Boyu”). Boyu
holds a capital markets services license and is regulated by the Monetary Authority of
Singapore. Boyu provides catalytic capital and strategic support for leading companies in
sectors including technology, healthcare, consumer and sustainable energy. Boyu is 100%
indirectly owned by Boyu Group, LLC, which is in turn ultimately controlled by Mr. Xiaomeng
Tong, an Independent Third Party. There is no single investor holding 30% or more interest in
Abstract Enigma Limited through Boyu Capital Offshore Fund.
China Universal (HK)
China Universal Asset Management (Hong Kong) Company Limited (“China Universal
(HK)”), founded in November 2009, is a wholly owned subsidiary of China Universal Asset
Management Co., Ltd, an asset management company with assets under management of over
RMB1,100 billion as of 31 December 2024. China Universal (HK) is among the first group of
Chinese fund management company subsidiaries established outside of Mainland China. China
Universal (HK) is licensed by the Hong Kong Securities and Futures Commission to carry on
Type 1 (Dealing in Securities), Type 4 (Advising on Securities) and Type 9 (Asset
Management) regulated activities under Part V of the Securities and Futures Ordinance. China
Universal (HK) manages investment funds, provides investment advisory services, and
manages discretionary accounts.
The subscription of the Offer Shares as a cornerstone investor will be made by China
Universal (HK) in its capacity as the investment manager on a discretionary basis for and on
behalf Better Supply Chain (HK) Holdings Co., Limited and Seraphim Advantage Inc. Zimei
PENG and Jun WANG holds 30% or more interest in Better Supply Chain (HK) Holdings Co.,
Limited and Seraphim Advantage Inc. respectively.
Eastspring
Eastspring Investments (Singapore) Limited (“Eastspring”), established in 1994 and
headquartered in Singapore, brings over 30 years of investment expertise in Asia. Eastspring
is ultimately 100% held by Prudential plc, a publicly listed company, which has dual primary
listings on the Stock Exchange of Hong Kong (HKEX: 2378) and the London Stock Exchange
(LSE: PRU), and a secondary listing on the Singapore Stock Exchange (SGX: K6S) and a
listing on the New York Stock Exchange (NYSE: PUK) in the form of American Depositary
Receipts.
As of September 30, 2025, Eastspring manages US$286 billion in assets. Eastspring
offers a diverse range of investment strategies for both Asian and non-Asian institutions,
working closely with its local offices to deliver tailored solutions to institutional clients.
CORNERSTONE INVESTORS
– 386 –

<<<PAGE 397>>>
Eastspring, acting as the discretionary investment manager for and on behalf of two
discretionary funds (the “ESI Managed Funds”), has agreed to participate in the Global
Offering and for such ESI Managed Funds to invest as Cornerstone Investor. The ESI Managed
Funds comprise an open-end mutual fund (namely EASTSPRING INVESTMENTS — ASIA
OPPORTUNITIES EQUITY FUND) and a segregated mandate (namely AHAPAG — ASIA
PACIFIC ACTIVE GROWTH EQUITY PORTFOLIO) established under various jurisdictions
and have multiple holders, who together with their ultimate beneficial owners are, to the best
of the knowledge, information and belief of the Company, Independent Third Parties. The only
ultimate
beneficial
owner
for
each
of
EASTSPRING
INVESTMENTS
—
ASIA
OPPORTUNITIES EQUITY FUND and AHAPAG — ASIA PACIFIC ACTIVE GROWTH
EQUITY PORTFOLIO is Prudential plc.
E Fund Management
E Fund Management Co., Ltd. (“E Fund Management”), is a leading comprehensive
asset management company in the PRC. E Fund Management is a QDII approved by the
relevant PRC authority and targets at companies with competitive edge over its competitors.
E Fund Management is a fund manager managing assets on behalf of its underlying clients. The
shareholders of E Fund Management include (1) Guangdong Finance Trust Co., Ltd. (廣東粵
財信託有限公司), which is ultimately owned by The People’s Government of Guangzhou
Municipality (廣東省人民政府), (2) GF Securities Co., Ltd. (廣發証券股份有限公司) (“GF
Securities”), which is listed on the Stock Exchange (stock code: 1776) and the Shenzhen Stock
Exchange (stock code: 000776), and (3) Infore Group Co., Ltd (盈峰集團有限公司), which is
ultimately owned by He Jianfeng (何劍鋒), each holding 22.65% in E Fund Management and
an Independent Third Party. None of the remaining shareholders of E Fund Management owns
30% or more equity interest therein.
IDG Breyer Fund
IDG Breyer Capital Fund L.P. (“IDG Breyer Fund”) is an exempted limited partnerships
established under the laws of the Cayman Islands. IDG Breyer Fund is a capital fund with a
primary purpose of making equity and equity-related investments, in the next-generation
technology and technology-driven sectors, including, without limitation, artificial intelligence,
autonomous driving, intelligent manufacturing, genome technology, fintech and 5G enabled
next generation cloud services. It is ultimately controlled by Chi Sing HO and Fei YANG, both
being Independent Third Parties. The investor holding 30% or more stake in IDG Breyer Fund
is a listed company after equity penetration, save as disclosed above, none of the other ultimate
beneficial owners of IDG Breyer Fund is interested in it as to 30% or more.
Janchor Funds
Janchor Partners Pan-Asian Master Fund and Janchor Partners Opportunities Master Fund
III (together “Janchor Funds”) are investment funds established in the Cayman Islands.
Janchor Partners Limited (“Janchor Partners”) serves as investment manager of the Janchor
CORNERSTONE INVESTORS
– 387 –

<<<PAGE 398>>>
Funds. Established in 2009, Janchor Partners is a long-term industrialist investor, partnering
with companies that have superior business models, favourable growth prospects and the
potential to be part of long-term positive structural dynamics of Asian countries and
economies.
Janchor Partners is licensed by the SFC to conduct asset management and is an
experienced institutional investor with a track record of investing in technology companies.
None of the participating shareholders or limited partners of the Janchor Funds or their feeder
funds holds an interest of 30% or more of the Janchor Funds’ total capital.
Martis Fund, L.P.
Martis Fund, L.P. is an exempted limited partnership registered under the laws of Cayman
Islands, focusing on healthcare, telecommunication, media, technology and consumer
industries investment. The general partner of Martis Fund, L.P. is Pulsating Star GP Limited,
which is 100% ultimately controlled by Mr. Eric Li, an independent third party of the
Company. No limited partner holds 30% or more partnership interest in Martis Fund, L.P. Mr.
Eric Li is a Hong Kong citizen with extensive experience in the investment industry. Through
several investment funds he ultimately controls, Mr. Eric Li focuses on the investment in
healthcare,
telecommunication,
media,
technology
and
consumer
industries,
and
has
successfully invested in several companies listed in Hong Kong, including Giant Biogene
(stock code: 02367), WL Delicious (stock code: 09985) and SF Intra-City (stock code: 09699)
as pre-IPO investor, Guming (stock code: 01364), Sanhua (stock code: 02050), Chery Auto
(stock code: 09973) and CIG (stock code: 06166) as cornerstone investor.
Mirae Asset Securities
Mirae Asset Securities Co., Ltd. (“Mirae Asset Securities”) is one of the largest
investment banks in the Republic of Korea, providing a comprehensive range of financial
services, including brokerage, wealth management, investment banking, sales & trading, and
principal investments. It is ultimately controlled by Mirae Asset Capital Co., Ltd., a financial
investment company in the Republic of Korea. Mirae Asset Securities is listed on the Korea
Exchange under stock code 006800.KS.
MPC VII
MPC VII Pte. Ltd. (“MPC VII”) is a limited company incorporated and domiciled in
Singapore, which is owned as to 93.97% and 6.03% by MPC VII L.P. and MPC VII-A L.P.,
respectively. The general partner of both MPC VII L.P. and MPC VII-A L.P., each an exempted
limited partnership incorporated under the laws of the Cayman Islands, is MPC Management
VII L.P.. The general partner of MPC Management VII L.P. is MPC GPGP VII Ltd. David Su
is the controlling shareholder of MPC GPGP VII Ltd.. No single limited partner holds 30% or
more interests in MP VII L.P. or in MPC VII-A L.P.. To the best knowledge of MPC VII, David
Su is an Independent Third Party.
CORNERSTONE INVESTORS
– 388 –

<<<PAGE 399>>>
Perseverance Asset Management
Perseverance Asset Management International (Singapore) Pte. Ltd. (“Perseverance
Asset Management”) acts as the investment advisor or investment manager on a discretionary
basis of no more than six investment funds and/or separated managed accounts (collectively the
“Perseverance Funds”). No single ultimate beneficial owner holds 30% or more interest in
each of the Perseverance Funds. Perseverance Asset Management is a private limited company
incorporated in Singapore in October 2018, and holds a Capital Markets Services License for
fund management with Monetary Authority of Singapore. Perseverance Asset Management is
wholly owned by Perseverance Asset Management International, which is principally engaged
in investment management and investment advisory services and an Independent Third Party.
Certain investments funds for which Perseverance Asset Management acts as the investment
advisor or investment manager invested in ZIJIN GOLD INTERNATIONAL COMPANY
LIMITED
(紫金黃金國際有限公司)
(stock
code:
2259.HK),
Contemporary
Amperex
Technology Co. and Limited (寧德時代新能源科技股份有限公司) (stock code: 3750.HK) and
Acotec Scientific Holdings Limited (先瑞達醫療科技控股有限公司) (stock code: 6669.HK) as
cornerstone investor. Perseverance Asset Management is entering into the cornerstone
investment agreement with the Company in its capacity as an investment advisor or investment
manager and on behalf of the Perseverance Funds.
Taikang Life
Taikang Life Insurance Co., Ltd (“Taikang Life”), a company incorporated in China, is
a wholly owned subsidiary of Taikang Insurance Group Inc. There is no shareholder holding
30% or more in Taikang Insurance Group Inc. Taikang Life provides a full range of personal
security and investment and wealth management products and services for individuals and
families. The products on offer correspond to the different requirements of customers in terms
of market segments such as the children and teenagers, females and high-income population
groups. They also meet multidimensional demands regarding health care and accident cover,
pensions and wealth management, among others. Taikang Insurance Group Inc. is an insurance
and financial service conglomerate focused on insurance, asset management and health and
elderly care as main businesses. The Beijing-headquartered company consists of several
subsidiaries including Taikang Life, Taikang AMC, Taikang Pension, Taikang Healthcare,
Taikang Health, and TK.CN. Its product offering covers life insurance, internet-based financial
insurance, enterprise annuity, asset management, health and elderly care, health management
and commercial real estate, among others.
CORNERSTONE INVESTORS
– 389 –

<<<PAGE 400>>>
CLOSING CONDITIONS
The obligation of each Cornerstone Investor to subscribe for the Offer Shares under the
respective Cornerstone Investment Agreement is subject to, among other things, the following
closing conditions:
(i)
the Underwriting Agreements being entered into and having become effective and
unconditional (in accordance with their respective original terms or as subsequently
waived or varied by agreement of the parties thereto) by no later than the time and
date as specified in the Underwriting Agreements, and neither of the Underwriting
Agreements having been terminated;
(ii)
the Offer Price having been agreed according to the Underwriting Agreements and
price determination agreement to be signed among the parties thereto in connection
with the Global Offering;
(iii) the Listing Committee having granted the listing of, and permission to deal in, the
Class A Ordinary Shares (including the investors’ Shares as well as other applicable
waivers and approvals) and such approval, permission or waiver having not been
revoked prior to the commencement of dealings in the Class A Ordinary Shares on
the Stock Exchange;
(iv) no laws shall have been enacted or promulgated by any governmental authority
which prohibits the consummation of the transactions contemplated in the Global
Offering or the Cornerstone Investment Agreements and there shall be no orders or
injunctions from a court of competent jurisdiction in effect precluding or prohibiting
consummation of such transactions; and
(v)
the respective representations, warranties, undertakings and confirmations of the
relevant Cornerstone Investor under the relevant Cornerstone Investment Agreement
are and will be accurate and true in all respects and not misleading and that there is
no material breach of the Cornerstone Investment Agreement on the part of the
relevant Cornerstone Investor.
RESTRICTIONS ON THE CORNERSTONE INVESTORS
Each of the Cornerstone Investors has agreed that it will not, whether directly or
indirectly, at any time during the period of six months from and including the Listing Date (the
“Lock-up Period”), dispose of any of the Offer Shares they have purchased pursuant to the
relevant Cornerstone Investment Agreements, save for certain limited circumstances, such as
transfers to any of its wholly-owned subsidiaries who will be bound by the same obligations
of such Cornerstone Investor, including the Lock-up Period restriction.
CORNERSTONE INVESTORS
– 390 –

<<<PAGE 401>>>
AUTHORIZED AND ISSUED SHARE CAPITAL
The following is a description of the authorized and issued share capital of our Company
in issue and to be issued as fully paid or credited as fully paid upon Listing, assuming the
Presumptions.
Share capital as of the date of this Prospectus
(i)
Authorized share capital
Number
Description of Shares
Aggregate
Nominal Value
221,311,196
Class A Ordinary Shares with a nominal
value of US$0.0001 each in issue
US$22,131.1196
106,650,075
Class B Ordinary Shares with a nominal
value of US$0.0001 each in issue
US$10,665.0075
172,038,729
Preferred Shares with a nominal
value of US$0.0001 each in issue
US$17,203.8729
500,000,000
Total
US$50,000
(ii)
Issued and to be issued, fully paid or credited to be fully paid
Number
Description of Shares
Aggregate
Nominal Value
22,890,736(1)
Class A Ordinary Shares with a nominal
value of US$0.0001 each in issue
US$2,289.0736
85,759,339(2)
Class B Ordinary Shares with a nominal
value of US$0.0001 each in issue
US$8,575.9339
171,407,993
Preferred Shares with a nominal value of
US$0.0001 each in issue
US$17,140.7993
280,058,068
Total
US$28,005.8068
Notes:
(1)
representing 343,195 Class A Ordinary Shares, 20,890,736 Class A Ordinary Shares and 1,656,805 Class
A Ordinary Shares held by Alpha EXP, MiniMax Gene and Himalia Holding Limited, respectively, as
of the date of this Prospectus.
(2)
representing 15 Class B Ordinary Shares, 5,000,000 Class B Ordinary Shares, 11,509,339 Class B
Ordinary Shares, 62,249,985 Class B Ordinary Shares and 7,000,000 Class B Ordinary Shares held by
MiniMax Limited, MiniMax Matrix, MiniMax Awakening, Alpha EXP and Floating Sky, respectively,
as of the date of this Prospectus.
SHARE CAPITAL
– 391 –

<<<PAGE 402>>>
Share capital immediately following the completion of the Global Offering
(i)
Authorized share capital
Number
Description of Shares
Aggregate
Nominal Value
393,349,925
Class A Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$39,334.9925
106,650,075
Class B Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$10,665.0075
500,000,000
Total
US$50,000
(ii)
Issued and to be issued, fully paid or credited to be fully paid (assuming the Offer Size
Adjustment Option and the Over-allotment Option are not exercised)
Number
Description of Shares
Aggregate
Nominal Value
22,547,541(1)
Class A Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$2,254.7541
80,759,339(2)
Class B Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$8,075.9339
343,195(3)
Class A Ordinary Shares to be converted into
Class B Ordinary Shares
US$34.3195
5,000,000(4)
Class B Ordinary Shares to be converted into
Class A Ordinary Shares
US$500
171,407,993
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued on conversion of
Preferred Shares
US$17,140.7993
25,389,220
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued pursuant to the
Global Offering
US$2,538.9220
305,447,288
Total
US$30,544.7288
SHARE CAPITAL
– 392 –

<<<PAGE 403>>>
Notes:
(1)
representing 20,890,736 Class A Ordinary Shares and 1,656,805 Class A Ordinary Shares held by
MiniMax Gene and Himalia Holding Limited, respectively, upon Listing.
(2)
representing 15 Class B Ordinary Shares, 11,509,339 Class B Ordinary Shares, 62,249,985 Class B
Ordinary Shares and 7,000,000 Class B Ordinary Shares held by MiniMax Limited, MiniMax
Awakening, Alpha EXP and Floating Sky, respectively, upon Listing.
(3)
representing 343,195 Class A Ordinary Shares held by Alpha EXP to be converted into Class B Ordinary
Shares upon Listing.
(4)
representing 5,000,000 Class B Ordinary Shares held by MiniMax Matrix to be converted into Class A
Ordinary Shares upon Listing.
(iii) Issued and to be issued, fully paid or credited to be fully paid (assuming the Offer Size
Adjustment Option is fully exercised and the Over-allotment Option is not exercised)
Number
Description of Shares
Aggregate
Nominal Value
22,547,541(1)
Class A Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$2,254.7541
80,759,339(2)
Class B Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$8,075.9339
343,195(3)
Class A Ordinary Shares to be converted into
Class B Ordinary Shares
US$34.3195
5,000,000(4)
Class B Ordinary Shares to be converted into
Class A Ordinary Shares
US$500
171,407,993
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued on conversion of
Preferred Shares
US$17,140.7993
25,389,220
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued pursuant to the
Global Offering
US$2,538.9220
3,808,380
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued pursuant to the
Offer Size Adjustment Option
US$380.8380
309,255,668
Total
US$30,925.5668
Note:
please refer to the section headed “— (ii) Issued and to be issued, fully paid or credited to be fully paid
(assuming the Offer Size Adjustment Option and the Over-allotment Option are not exercised)” above.
SHARE CAPITAL
– 393 –

<<<PAGE 404>>>
(iv)
Issued and to be issued, fully paid or credited to be fully paid (assuming the Offer Size
Adjustment Option is not exercised and the Over-allotment Option is fully exercised)
Number
Description of Shares
Aggregate
Nominal Value
22,547,541(1)
Class A Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$2,254.7541
80,759,339(2)
Class B Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$8,075.9339
343,195(3)
Class A Ordinary Shares to be converted into
Class B Ordinary Shares
US$34.3195
5,000,000(4)
Class B Ordinary Shares to be converted into
Class A Ordinary Shares
US$500
171,407,993
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued on conversion of
Preferred Shares
US$17,140.7993
25,389,220
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued pursuant to the
Global Offering
US$2,538.9220
3,808,380
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued pursuant to the
Over-allotment Option
US$380.8380
309,255,668
Total
US$30,925.5668
Note:
please refer to the section headed “— (ii) Issued and to be issued, fully paid or credited to be fully paid
(assuming the Offer Size Adjustment Option and the Over-allotment Option are not exercised)” above.
SHARE CAPITAL
– 394 –

<<<PAGE 405>>>
(v)
Issued and to be issued, fully paid or credited to be fully paid (assuming the Offer Size
Adjustment Option and the Over-allotment Option are fully exercised)
Number
Description of Shares
Aggregate
Nominal Value
22,547,541(1)
Class A Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$2,254.7541
80,759,339(2)
Class B Ordinary Shares with a nominal value
of US$0.0001 each in issue
US$8,075.9339
343,195(3)
Class A Ordinary Shares to be converted into
Class B Ordinary Shares
US$34.3195
5,000,000(4)
Class B Ordinary Shares to be converted into
Class A Ordinary Shares
US$500
171,407,993
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued on conversion of
Preferred Shares
US$17,140.7993
25,389,220
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued pursuant to the
Global Offering
US$2,538.9220
3,808,380
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued pursuant to the
Offer Size Adjustment Option
US$380.8380
4,379,640
Class A Ordinary Shares with a nominal value
of US$0.0001 to be issued pursuant to the
Over-allotment Option
US$437.9640
313,635,308
Total
US$31,363.5308
Note:
please refer to the section headed “— (ii) Issued and to be issued, fully paid or credited to be fully paid
(assuming the Offer Size Adjustment Option and the Over-allotment Option are not exercised)” above.
SHARE CAPITAL
– 395 –

<<<PAGE 406>>>
WEIGHTED VOTING RIGHTS STRUCTURE
The Company has a weighted voting rights structure. Under our weighted voting rights
structure, our share capital comprises Class A Ordinary Shares and Class B Ordinary Shares.
Each Class B Ordinary Share entitles the holder to exercise ten votes, and each Class A
Ordinary Share entitles the holder to exercise one vote, respectively, on any matters subject to
the vote at general meetings of the Company, subject to Rule 8A.24 of the Listing Rules that
requires the Reserved Matters to be voted on a one vote per share basis.
The Reserved Matters are:
(i)
any amendment to the Memorandum and Articles;
(ii)
the variation of the rights attached to any class of Shares;
(iii) the appointment, election or removal of any independent non-executive Director;
(iv) the appointment or removal of the Company’s auditors; and
(v)
the voluntary liquidation or winding-up of the Company.
See “Summary of the Constitution of our Company and Cayman Islands Company Law
— 2 Articles of Association” in Appendix III to this Prospectus for further details.
Class B Ordinary Shares may be converted into Class A Ordinary Shares on a one to one
basis. Upon the conversion of all the issued and outstanding Class B Ordinary Shares into Class
A Ordinary Shares, the Company will issue 81,102,534 Class A Ordinary Shares, representing
approximately 26.55% of the total number of issued Class A Ordinary Shares immediately
following the Listing (assuming the Offer Size Adjustment Option and the Over-allotment
Option are not exercised).
The weighted voting rights attached to our Class B Ordinary Shares will cease when the
WVR Beneficiaries cease to have beneficial ownership of any of our Class B Ordinary Shares,
in accordance with Rule 8A.22 of the Listing Rules. This may occur:
(i)
upon the occurrence of any of the circumstances set out in Rule 8A.17 of the Listing
Rules, in particular where the WVR Beneficiaries are: (1) deceased; (2) no longer
a member of our Board; (3) deemed by the Stock Exchange to be incapacitated for
the purpose of performing his duties as a director; or (4) deemed by the Stock
Exchange to no longer meet the requirements of a director set out in the Listing
Rules;
(ii)
when the holders of Class B Ordinary Shares have transferred to another person the
beneficial ownership of, or economic interest in, the Class B Ordinary Shares or the
control over the voting rights attached to them, other than in the circumstances
permitted by Rule 8A.18 of the Listing Rule;
SHARE CAPITAL
– 396 –

<<<PAGE 407>>>
(iii) where a vehicle holding Class B Ordinary Shares on behalf of a WVR Beneficiary
no longer complies with Rule 8A.18(2) of the Listing Rule; or
(iv) when all of the Class B Ordinary Shares have been converted to Class A Ordinary
Shares.
Shareholding Structure of the WVR Beneficiaries
The table below sets out the beneficial interests entitled to and voting rights to be held
by the WVR Beneficiaries upon the completion of the Global Offering (assuming the Offer
Size Adjustment Option and the Over-allotment Option are not exercised):
Number of
Class B
Ordinary Shares
held
Number of Class
A Ordinary
Shares interested
in(3)
Approximate
percentage of
beneficial
interests
in the issued
share capital
Approximate
percentage of
voting rights
controlled(1)
Dr. Yan(2)   
74,102,534
3,355,030
25.36%
72.05%
Ms. Yun(2)   
7,000,000
1,644,970
2.83%
6.76%
Notes:
(1)
On the basis that each Class A Ordinary Share entitles the Shareholder to one vote per Share and each
Class B Ordinary Share entitles the Shareholder to ten votes per Share.
(2)
For details of the shareholding structure of our WVR Beneficiaries, please refer to the section headed
“History, Reorganization and Corporate Structure.”
(3)
Dr. Yan and Ms. Yun are interested in MiniMax Matrix as to 67.1% and 32.9%.
The Company confirms that the holding arrangement through which the WVR
Beneficiaries hold the Class B Ordinary Shares as described above meets the requirements in
Rule 8A.18 of the Listing Rules and the holding arrangement is permitted under the
“Consultation Conclusions — a listing regime for companies from emerging and innovative
sectors” issued by the Stock Exchange in April 2018, namely: (a) a partnership of which the
WVR Beneficiary is a partner and the terms of which must expressly specify that the voting
rights attached to any and all of the Class B Ordinary Shares held by such partnership are solely
dictated by the WVR Beneficiary; (b) a trust of which the WVR Beneficiary is a beneficiary
and that meets the following conditions: (i) the WVR Beneficiary must in substance retain an
element of control of the trust and any immediate holding companies of, or, if not permitted
in the relevant tax jurisdiction, retain a beneficial interest in any and all of the Class B Ordinary
Shares held by such trust; and (ii) the purpose of the trust must be for estate planning and/or
tax planning purposes; or (c) a private company or other vehicle wholly owned and wholly
controlled by the WVR Beneficiary or by a trust referred to in paragraph (b) above.
SHARE CAPITAL
– 397 –

<<<PAGE 408>>>
To ensure that there will not be any circumvention of Rule 8A.18(1), each of the
Company, Dr. Yan and Ms. Yun undertakes that so long there is any weighted voting rights
attached to the Shares held by Alpha EXP, MiniMax Gene, Floating Sky, MiniMax Awakening,
MiniMax Limited (the “WVR Management Shareholders”), respectively, Dr. Yan and Ms.
Yun will not transfer any beneficial ownership of or economic interest in the WVR
Management Shareholders or the control over the voting rights attached to the Shares held by
WVR Management Shareholders to another person. In the event that there is any change in the
beneficial ownership of or economic interest in the Shares held by the WVR Management
Shareholders or the control over the voting rights attached to the Shares held by the WVR
Management Shareholders to another person, the Company, Dr. Yan and Ms. Yun will notify
the Stock Exchange pursuant to Rule 8A.19 of the Listing Rules and comply with the relevant
statutory obligations including obligations of disclosure of interests under the SFO, and the
weighted voting rights attached to the Class B Ordinary Shares held by WVR Management
Shareholders shall cease upon such transfer accordingly. The Company will also comply with
Rule 8A.30 of the Listing Rules to confirm, on an annual basis, that the WVR Beneficiary has
complied with Rule 8A.18 of the Listing Rules.
Contribution of the WVR Beneficiaries
Dr. Yan and Ms. Yun, being the WVR beneficiaries, have been materially responsible for
the growth of the Company’s business during the Track Record Period by way of their
respective skills, knowledge and/or insights to the industry. As the core of the Group’s
leadership team and leveraging their professional experience in the industry, each of Dr. Yan
and Ms. Yun is pivotal to the success of the Group and has made significant contributions to
the Group from strategic, technological and operational perspectives.
We set forth below the academic background, work experience and contribution of the
proposed WVR beneficiaries to the success of the Company:
Dr. Yan
Dr. Yan is the founder, the chairman of the board of directors, chief executive officer and
chief technology officer of the Company. As the chief executive officer and chief technology
officer of the Company, Dr. Yan has been integral to the success of the Company and has been
materially responsible for the founding and growth of the Company during the Track Record
Period. Dr. Yan, with profound technical insight and deep understanding and knowledge of AI
technology, laid the foundation for the Company and was critical in shaping the Group’s
mission, vision and values, and devising long-term strategies for the R&D and operations of
the Group over the years. During the Track Record Period, Dr. Yan had spearheaded the team
in developing a trimodal large model that integrates text, audio, and visual capabilities and
have led our Group to achieve its key milestones. For example, he led the launch of our first
text model abab1 in 2022, our text model abab5.5 and speech model MiniMax-Speech-01 in
2023, our MoE text model abab6, visual generation platform Hailuo AI and video-generation
model Hailuo-01 and music model Music-01 in 2024 as well as our open-source text model
MiniMax-Text-01, MiniMax-M1 and MiniMax-M2 in 2025. In addition, leveraging the
SHARE CAPITAL
– 398 –

<<<PAGE 409>>>
reputation and experience of Dr. Yan in the industry, the Company has been able to secure
investments from numerous investors at a relatively early stage and before its significant
commercialization. Dr. Yan has also led the Company to develop a suite of AI-native products
that serve a broad range of user scenarios and lay a solid foundation for the Company’s path
to commercialization.
Ms. Yun
As the chief operating officer of the Company, Ms. Yun has been integral to the success
of the Company and has been materially responsible for the founding and growth of the
Company’s business and guiding its development since she co-founded the Group. With
profound industry insight and deep understanding and knowledge of AI technology as well as
her global vision, Ms. Yun led the rapid global business expansion of the Company and was
critical in shaping the Group’s mission, vision and values. She is also instrumental in devising
long-term R&D strategies, product development, commercialization and operations of the
Group over the years. With the deep insights in the global AI industry, she played a pivotal role
in designing and developing the Company’s foundation models and devising long-term
strategies and R&D focuses for the Company, with an emphasis on developing AI-native
products. In particular, leveraging her expertise and knowledge of the AI ecosystem, Ms. Yun
is able to envisage market needs and drive the Company’s creative product development efforts
and create AI-native offerings products that serve a broad range of user scenarios. For example,
for individual users, the Company has launched (i) MiniMax, its intelligent chat agent
application, (ii) Hailuo AI, its flagship artificial intelligence visual generation platform, and
(iii) Xingye/Talkie AI-powered Multi-modal Entertainment Platform. For enterprise customers,
the Company offers an open platform, which provides API access to its self-developed
multimodal models. As the chief operating officer, Ms. Yun led the day-to-day operation of the
Company and coordinated major matters of the Company, including but not limited to
corporate strategy, overall operational management, corporate governance and investor
relationship. Under the leadership of Ms. Yun, the Company was able to overcome challenges
and has achieved rapid growth in the past few years. Since the Company’s inception, Ms. Yun
has been overseeing talent acquisition and human resources functions of the Company, playing
a pivotal role in establishing a competitive organization from the ground up. Leveraging her
expertise in investment and financing, Ms. Yun is able to secure investments for the Company
from
numerous
investors
at
a
relatively
early
stage
and
before
its
significant
commercialization. With a global vision, Ms. Yun has led the Company to achieve its rapid
global expansion. During the early stages of the Company’s development, Ms. Yun has been
instrumental in building the Company’s department focusing on products commercialization
from the ground up. These strategic initiatives have laid the groundwork for the Company’s
forthcoming technological innovations and accelerated global expansion. With the contribution
from Ms. Yun, the Company’s open platform currently provides scalable and customizable AI
services to enterprise customers across more than 100 countries and regions, and is one of the
top-ranking open platforms in Asia in terms of daily token volume. The Company’s service has
reached more than 100 thousand registered enterprise customers and developers, including a
range of well-known enterprise customers.
SHARE CAPITAL
– 399 –

<<<PAGE 410>>>
RANKING
The Offer Shares will rank pari passu in all respects with all Class A Ordinary Shares
currently in issue or to be issued as mentioned in this Prospectus, and will qualify and rank
equally for all dividends or other distributions declared, made or paid on the Shares on a record
date which falls after the date of this Prospectus.
UNDERTAKINGS BY THE WVR BENEFICIARIES
Pursuant to Rule 8A.43 of the Listing Rules, each WVR Beneficiary is required to give
a legally enforceable undertaking to the Company that he will comply with the relevant
requirements as set out in Rule 8A.43, which is intended to be for the benefit of and
enforceable by the Shareholders. On December 22, 2025, each of Dr. Yan and Ms. Yun made
an undertaking to the Company (the “Undertaking”), that for so long as he/she is a WVR
Beneficiary:
(a)
He/she shall comply with (and, if the shares to which the weighted voting rights that
he/she is beneficially interested in are attached are held through a limited
partnership, trust, private company, or other vehicle, use his/her best endeavors to
procure that such limited partnership, trust, private company or other vehicle
complies with) all applicable requirements under Rules 8A.09, 8A.14, 8A.15,
8A.17. 8A.18 and 8A.24 of the Listing Rules from time to time in force (the
“Requirements”); and
(b)
He/she shall use his best endeavors to procure that the Company complies with all
applicable Requirements.
For the avoidance of doubt, the Requirements are subject to Rule 2.04 of the Listing
Rules. The WVR Beneficiaries acknowledged and agreed that the Shareholders rely on the
Undertaking in acquiring and holding their Shares. The WVR Beneficiaries acknowledged and
agreed that the Undertaking is intended to confer a benefit on the Company and all
Shareholders and may be enforced by the Company and/or any Shareholder against the WVR
Beneficiaries.
The Undertaking shall automatically terminate upon the earlier of (i) the date of delisting
of the Company from the Stock Exchange, and (ii) the date on which the relevant WVR
Beneficiary ceases to be a beneficiary of weighted voting rights in the Company. For the
avoidance of doubt, the termination of the Undertaking shall not affect any rights, remedies,
obligations or liabilities of the Company and/or any Shareholder and/or the WVR Beneficiary
himself that have accrued up to the date of termination, including the right to claim damages
and/or apply for any injunction in respect of any breach of the Undertaking which existed at
or before the date of termination.
The Undertaking shall be governed by the laws of Hong Kong and all matters, claims or
disputes arising out of the Undertaking shall be subject to the exclusive jurisdiction of the
courts of Hong Kong.
SHARE CAPITAL
– 400 –

<<<PAGE 411>>>
POTENTIAL CHANGES TO SHARE CAPITAL
Circumstances under which general meetings are required
Pursuant to the Cayman Companies Act and the terms of the Articles of Association, our
Company may from time to time by ordinary resolution of Shareholders (i) increase its share
capital; (ii) consolidate and divide its share capital into Shares of larger amount; (iii) divide its
Shares into several classes; and (iv) cancel any Shares which have not been taken or agreed to
be taken. In addition, our Company may, subject to the provisions of the Cayman Companies
Act, reduce its share capital or capital redemption reserve by its Shareholders passing a special
resolution. See “Summary of the Constitution of our Company and Cayman Islands Company
Law — 2. Articles of Association — 2.5 Alteration of capital” in Appendix III of this
Prospectus for further details.
General mandate to (i) issue shares and (ii) sell and/or transfer treasury shares
Subject to the Global Offering becoming unconditional, our Directors were granted a
general mandate to (i) allot, issue and deal with any Class A Ordinary Shares or securities
convertible into Shares, and (ii) sell and/or transfer Shares out of treasury that are held as
treasury shares of not more than the sum of:
•
20% of the total number of Shares in issue immediately following completion of the
Global Offering (excluding (i) the additional Class A Ordinary Shares which may be
issued pursuant to the exercise of the Over-allotment Option, (ii) the Class A
Ordinary Shares to be issued pursuant to the Post-IPO Share Incentive Plan, (iii) the
Class A Ordinary Shares that are issuable upon conversion of the Class B Ordinary
Shares, and (iv) treasury shares, if any); and
•
the aggregate nominal value of Shares repurchased by the Company under the
authority referred to in the paragraph headed “— General Mandate to Repurchase
Shares” in this section.
This general mandate to issue Class A Ordinary Shares and sell and/or transfer treasury
shares will expire at the earliest of:
•
the conclusion of the next annual general meeting of our Company unless otherwise
renewed by an ordinary resolution of our Shareholders in a general meeting, either
unconditionally or subject to conditions; or
•
the expiration of the period within which our Company’s next annual general
meeting is required by the Articles of Association or any other applicable laws to be
held; or
•
the date on which it is varied or revoked by an ordinary resolution of our
Shareholders in a general meeting.
SHARE CAPITAL
– 401 –

<<<PAGE 412>>>
General mandate to repurchase shares
Subject to the Global Offering becoming unconditional, our Directors have been granted
a general unconditional mandate, to exercise all the powers of our Company to repurchase our
own securities with nominal value of up to 10% of the total number of Shares in issue
immediately following the completion of the Global Offering (excluding (i) the additional
Class A Ordinary Shares which may be issued pursuant to the exercise of the Over-allotment
Option, (ii) the Class A Ordinary Shares to be issued pursuant to the Post-IPO Share Incentive
Plan, (iii) the Class A Ordinary Shares that are issuable upon conversion of the Class B
Ordinary Shares, and (iv) treasury shares, if any).
The repurchase mandate only relates to repurchases made on the Stock Exchange, or on
any other stock exchange on which our Shares are listed (and which are recognized by the SFC
and the Stock Exchange for this purpose), and which are in accordance with the Listing Rules.
A summary of the relevant Listing Rules is set out in “Statutory and General Information —
A. Further Information about our Group — 5. Repurchases of Our Own Securities” in
Appendix IV.
This general mandate to repurchase Shares will expire at the earliest of:
•
the conclusion of the next annual general meeting of our Company unless otherwise
renewed by an ordinary resolution of our Shareholders in a general meeting, either
unconditionally or subject to conditions; or
•
the expiration of the period within which our Company’s next annual general
meeting is required by Articles of Association or any other applicable laws to be
held; or
•
the date on which it is varied or revoked by an ordinary resolution of our
Shareholders in a general meeting.
See “Statutory and General Information — A. Further Information about Our Group —
4. Resolutions of Our Shareholders” in Appendix IV to this Prospectus for further details of the
repurchase mandate.
SHARE INCENTIVE PLAN
The Company has adopted the Pre-IPO Share Incentive Plan and the Post-IPO Share
Incentive Plan. See “Statutory and General Information — D. Share Incentive Plans” in
Appendix IV to this Prospectus for further details.
SHARE CAPITAL
– 402 –

<<<PAGE 413>>>
You should read the following discussion and analysis in conjunction with our
consolidated
financial
statements
and
the
accompanying
notes
included
in
the
Accountants’ Report set forth in Appendix I to this Prospectus. Our consolidated financial
statements have been prepared in accordance with IFRSs, which may differ in material
aspects from generally accepted accounting principles in other jurisdictions. You should
read the entire Accountants’ Report and not merely rely on the information contained in
this section.
The following discussion and analysis contain forward-looking statements that
reflect the current views with respect to future events and financial performance. These
statements are based on assumptions and analysis made by us in light of our experience
and perception of historical trends, current conditions and expected future developments,
as well as other factors that we believe are appropriate under the circumstances.
However, whether the actual outcome and developments will meet our expectations and
predictions depends on a number of risks and uncertainties over which we do not have
control. In evaluating our business, you should carefully consider all of the information
provided in this Prospectus.
For the purpose of this section, unless the context otherwise requires, references to
2022, 2023 and 2024 refer to our financial year ended December 31 of such year. Unless
the context otherwise requires, financial information described in this section is
described on a consolidated basis.
OVERVIEW
MiniMax is a global AI foundation model company. Founded by a group of forward-
thinking engineers, we are committed to driving AI innovation towards performing the full
range of human intellectual tasks, from learning and reasoning to planning and generalizing
knowledge across diverse domains.
We have been consistently iterating our models to higher intelligence levels. Today, our
proprietary foundation model suite, led by MiniMax-M2, Hailuo-02, and Speech-02, has long
context processing capacity and can understand, generate, and integrate a wide range of
modalities, including text, video and audio. These models power our major AI-native products
— including MiniMax, Hailuo AI, MiniMax Audio, Talkie/Xingye, and our enterprise and
developer-facing Open Platform, delivering intelligent and dynamic experiences to users
globally.
FINANCIAL INFORMATION
– 403 –

<<<PAGE 414>>>
BASIS OF PREPARATION
The historical financial information has been prepared in accordance with all applicable
IFRS Accounting Standards as issued by the International Accounting Standards Board (the
“IASB”). Further details of the material accounting policy information adopted are set out in
Note 2 of the Accountants’ Report included in Appendix I to this Prospectus.
The IASB has issued a number of new and revised IFRS Accounting Standards. For the
purpose of preparing this historical financial information, our Group has adopted all applicable
new and revised IFRS Accounting Standards throughout the Track Record Period, except for
any new standards or interpretations that are not yet effective for the accounting period
beginning on January 1, 2025. The revised and new accounting standards and interpretations
issued but not yet effective for the accounting period beginning on January 1, 2025 are set out
in Note 2 of the Accountants’ Report included in Appendix I to this Prospectus.
MAJOR FACTORS AFFECTING OUR RESULTS OF OPERATIONS
Our business and results of operations are influenced by various general factors that affect
overall end-user demands and market conditions for foundation models and AI-native products.
These factors include macroeconomic trends, industry dynamics, technological advances and
innovations, the pace of AI penetration and user adaptability across industries, government
policies and regulations (including those specifically targeting AI), and the competitive
landscape. Any negative change in these conditions may adversely impact our results of
operations.
In addition to these general factors, the following specific factors have a more direct
impact on our results of operations.
Ability to Maintain Technology Leadership in Model Intelligence
The intelligence, performance and competitiveness of our foundation models is the most
critical factor influencing our business and results of operations. Such competitiveness is
determined by our judgement of technological development trends, our capability for
continuous innovation, and the efficiency of our model research and development processes.
Specifically, the intelligence level and strength of our models directly impacts the user
adoption, market demand, product penetration, and pricing of our products, which in turn
affects our revenue growth and profitability.
FINANCIAL INFORMATION
– 404 –

<<<PAGE 415>>>
Ability to Diversify Product Offerings, Broaden Monetization Channels and Improve
Accessibility
Our revenue growth has been primarily driven by the rapid expansion of our AI-native
product suite and a diversified monetization strategy. Since inception, we have followed a
product-oriented growth approach to develop intelligent, use case-driven applications powered
by our proprietary foundation models. Our diversified product offerings serve both individual
users and enterprise customers across a broad range of application scenarios, such as video
generation, general purpose agent services, speech and music synthesis, and multi-modal chat
interfaces. With a rising number of users adopting our flagship products, including MiniMax,
Hailuo AI, MiniMax Audio, Talkie/Xingye, we have cumulatively served more than 212
million individual users across over 200 countries and regions, and more than 100 thousand
enterprise customers and developers across over 100 countries and regions.
We have developed diversified monetization channels including subscription services,
token-based in-app purchases, online marketing services, and usage-based enterprise APIs. For
our
consumer-facing
products
such
as
MiniMax,
Hailuo
AI,
MiniMax
Audio,
and
Talkie/Xingye, monetization is driven by premium feature subscriptions services, token-based
in-app purchases and online marketing services. For our Open Platform, monetization
primarily derives from API calls (i.e., user requests to utilize the Company’s models) based on
token volume.
We have achieved user growth and early monetization traction. Our average MAUs
increased from approximately 3.1 million in 2023 to approximately 19.1 million in 2024, and
further to approximately 27.6 million in the nine months ended September 30, 2025. Our
number of paying users for our AI-native products rose from approximately 119,700 in 2023
to approximately 650,300 in 2024, and further to approximately 1,771,600 in the nine months
ended September 30, 2025. Looking ahead, we plan to broaden our monetization channels and
increase revenue per user across our product lines. Specifically, we aim to expand value-added
features within consumer-facing products and enhance API tiering to support high-volume use
cases across various industries. We also intend to deepen the integration between our models
and products, unlocking more scalable commercial opportunities across modalities.
Ability to Grow Global User Base with High Brand Awareness
Our global strategy has supported simultaneous product launches across markets and
enabled rapid international growth. As of September 30, 2025, our products and services were
deployed in over 200 countries and regions, with revenue from international markets
contributing a significant portion of our total revenue throughout the Track Record Period.
Revenue generated outside the Mainland China contributed approximately 73.1% of our total
revenue in the nine months ended September 30, 2025.
We believe further growth is a natural result of highly competitive products and high
brand awareness, which is in turn determined by continuous advancement of model
intelligence. As we continue to elevate model intelligence, we expect to expand global user
base with an organic user acquisition approach, without relying upon heavy brand promotion
and user acquisition spending.
FINANCIAL INFORMATION
– 405 –

<<<PAGE 416>>>
Ability to Optimize Costs Through Improving Model Computing Efficiency
We believe that our ability to improve model computing efficiency, while supporting
increasingly complex AI models, is a critical driver of achieving profitability. During the Track
Record Period, costs associated with model inference activities were recorded under cloud
service costs related to inference activities within cost of sales. These costs accounted for more
than 90.0% of our total cost of sales in each year of the Track Record Period.
Through continuous innovation in model architecture and infrastructure, we have
improved cost efficiency related to inference activities. We maintain high compute utilization
rates through dynamic resource allocation and a unified training-inference framework. Our
proprietary AI infrastructure dynamically allocates computing resources, ensuring service
availability and supporting sustainable large-scale delivery of high-performance foundation
models. As a percentage of revenue, our cost of sales decreased from 124.7% in 2023 to 87.8%
in 2024, and further decreased from 97.4% in the nine months ended September 30, 2024 to
76.7% in the nine months ended September 30, 2025. This improvement reflects increased
inference efficiency and economies of scale arising from more intelligent model and greater
infrastructure utilization.
We consider the effective training of AI models to be essential to our long-term success.
Costs associated with model training, fine-tuning and experimentation are recognised as
research and development expenses. To enhance training efficiency, we have established an
in-house AI infrastructure team and independently developed a high-performance training
framework tailored to large-scale third-party computing clusters. Our AI infrastructure is
designed holistically — from the operator level to cross-cluster resource scheduling —
enabling model training execution.
Although R&D continues to represent our largest area of investment, our cloud services
expenses relating to training as a percentage of revenue decreased, from over 1,300% in 2023
to 460.8% in 2024, and further decreased from 530.0% in the nine months ended September
30, 2024 to 266.5% in the nine months ended September 30, 2025. This reduction reflects
improved training efficiency and the scalability of our infrastructure, as our business
transitions from research-intensive development to scaled commercial deployment.
Ability to Continue to Enhance Research and Development and Management Efficiency
We maintain a flat and nimble research and development team and mechanism. Our
research and development team operate under a lean, flat and closely coordinated organization
structure. To further enhance research, development and management efficiency, we are
integrating our proprietary model technologies into internal operations. This includes
deploying internally developed large language model (LLM) agents for software development
support, workflow automation, and routine task processing. We expect to drive higher
personnel efficiency to achieve greater outcomes by leveraging our AI capabilities.
FINANCIAL INFORMATION
– 406 –

<<<PAGE 417>>>
MATERIAL ACCOUNTING POLICY INFORMATION AND ESTIMATES
Some of our accounting policies require us to apply estimates, assumptions, and complex
judgments related to accounting items. These estimates, assumptions, and judgments have a
significant impact on our financial position and results of operations. Our management
continuously evaluates such estimates, assumptions, and judgments based on past experience,
industry practices, and expectations of future events that are deemed reasonable under the
circumstances. During the Track Record Period, there had not been any material deviation from
our management’s estimates or assumptions and actual results, and we had not made any
material changes to these estimates or assumptions. We do not expect any material changes to
these estimates and assumptions in the foreseeable future.
Our material accounting policy information, estimates and judgments, which are
important for understanding our financial condition and results of operations, are set forth in
further detail in Note 2 and Note 3 to the Accountants’ Report included in Appendix I to this
Prospectus.
Set forth below are accounting policies that we believe are material to us or involve the
most significant estimates, assumptions and judgments used in the preparation of our financial
statements.
Revenue recognition
Revenue from contracts with customers
Revenue from contracts with customers is recognised when control of goods or services
is transferred to the customers at an amount that reflects the consideration to which our Group
expects to be entitled in exchange for those goods or services.
(i)
Revenue from AI-native Products
•
Membership subscription
Our Group offers membership subscription service to individual users which
provides subscribing members access to premium functionality in our Group’s AI-native
products. The membership subscription fee should be paid upfront, and it is non-
refundable. Revenue is recognised ratably over the membership period as service is
rendered.
FINANCIAL INFORMATION
– 407 –

<<<PAGE 418>>>
•
Virtual items
Our Group also offers individual users with virtual items in its AI-native Products
to enhance the using experience. Users have option to pre-purchase additional credits to
recharge their accounts and buy these virtual items. For consumable virtual items, our
Group’s performance obligation is to provide one-off services to users. This performance
obligation is satisfied when the virtual items are consumed. Accordingly, our Group
recognises the revenues at the point in time. For non-consumable virtual items, our
Group’s performance obligation is to provide on-going services to users who purchased
virtual items. This performance obligation is satisfied over the acting period of the paying
users. Accordingly, our Group recognises the revenues ratably over the estimated average
acting period of these paying users.
•
Online marketing service
In addition, our Group provides performance-based online marketing service to
enterprise customers on certain of its AI-native applications, including through a
mediation platform. Revenues from online marketing service are primarily recognised at
a point in time when users view or click on the advertisement.
(ii)
Revenue from Open Platform and other AI-based enterprise services
Our Group provides enterprise customers with access to its core AI models through its
Open Platform. The performance obligation of such services is satisfied at a point in time when
the customers call APIs with tokens. At the end of each month, the consideration is fixed based
on tokens consumed and no variable consideration exists.
Our Group also provides enterprise customers with other AI-based enterprise services,
mainly
consists
of
arrangements
customized
to
enterprise
requirements
and
licensed
deliverables. For customised arrangements, we work with enterprise customers to set up
dedicated inference resource pools tailored to their needs, helping ensure stable and predictable
model inference performance. For licensed deliverables, we license our foundation models to
enable customers to deploy and operate such models in their own systems. Consideration for
such services is fixed and revenue from other AI-based enterprise services is typically
recognised at a point in time when the service is accepted by the customers.
Other income
Interest income is recognised on an accrual basis using the effective interest method by
applying the rate that exactly discounts the estimated future cash receipts over the expected life
of the financial instrument or a shorter period, when appropriate, to the net carrying amount
of the financial asset.
FINANCIAL INFORMATION
– 408 –

<<<PAGE 646 起已省略：超出 cornerstone 字符上限；请人工复核覆盖范围>>>



## 附加财务（AT–AY）

- `col_AT` = Year-1 financial period end (dd/mm/yy) (type=date unit=date missing=NA period=year-1_original_end annualize=False)
- `col_AU` = Operating cash flow in year-1 (before annualization) (type=number unit=basic_currency_units missing=NaN period=year-1_original annualize=False)
- `col_AV` = Cash and cash equivalents at year-1 end (type=number unit=basic_currency_units missing=NaN)
- `col_AW` = R&D expensed in year-1 (before annualization) (type=number unit=basic_currency_units missing=NaN period=year-1_original annualize=False)
- `col_AX` = Development costs capitalized in year-1 (additions, before annualization) (type=number unit=basic_currency_units missing=NaN period=year-1_original annualize=False)
- `col_AY` = Top 5 customers (% of year-1 revenue) (type=number unit=decimal missing=NaN period=year-1_original annualize=False)

### 原文切片：附加财务（AT–AY）


<<<PAGE 550>>>
CONSOLIDATED STATEMENTS OF CASH FLOWS
Year ended 31 December
Nine months ended
30 September
Notes
2022
2023
2024
2024
2025
USD’000
USD’000
USD’000
USD’000
USD’000
(unaudited)
CASH FLOWS FROM
OPERATING ACTIVITIES
Loss before tax            
(73,728)
(269,246)
(465,238)
(304,342)
(512,013)
Adjustments for:
Finance costs            
6
14
61
509
316
511
Interest income          
5
(39)
(7,785)
(20,448)
(17,199)
(7,876)
Fair value gain on financial
assets at fair value through
profit or loss          
5
(941)
(788)
(15,710)
(6,682)
(20,414)
Fair value loss on financial
liabilities             
7
60,509
176,826
214,172
128,063
313,477
(Gains)/losses on disposal of
right-of-use assets       
–
(70)
1
–
(175)
Depreciation of property, plant
and equipment         
13
25
180
451
325
582
Depreciation of right-of-use
assets               
14
182
631
1,450
1,072
1,478
Share-based payment expense 
26
1,069
3,346
6,823
6,100
8,581
Provision for impairment on
financial assets         
15
–
3
88
68
22
(12,909)
(96,842)
(277,902)
(192,279)
(215,827)
Increase in trade receivables    
–
(1,341)
(5,732)
(4,230)
(1,103)
(Increase)/decrease in
prepayments, other receivables
and other assets          
(513)
(4,190)
(9,272)
(11,925)
1,846
Increase in trade and bills
payables               
2,394
14,848
33,970
37,949
19,007
Increase/(decrease) in other
payables, accruals and other
liabilities              
2,191
12,624
21,048
4,557
(22,865)
Increase in other non-current
liabilities              
–
1,218
–
–
267
Increase in contract liabilities   
–
559
994
481
3,104
(Increase)/decrease in restricted
cash                 
(2,221)
2,182
(27,292)
(35,347)
2,193
Cash flows used in operating
activities              
(11,058)
(70,942)
(264,186)
(200,794)
(213,378)
Interest received           
39
6,487
5,703
5,198
3,982
Net cash flows used in operating
activities              
(11,019)
(64,455)
(258,483)
(195,596)
(209,396)
APPENDIX I
ACCOUNTANT’S REPORT
– I-13 –

<<<PAGE 551>>>
Year ended 31 December
Nine months ended
30 September
Notes
2022
2023
2024
2024
2025
USD’000
USD’000
USD’000
USD’000
USD’000
(unaudited)
CASH FLOWS FROM
INVESTING ACTIVITIES
Purchases of items of property,
plant and equipment       
(256)
(697)
(759)
(496)
(479)
Placement of time deposits     
–
(90,400)
(199,100)
(195,200)
–
Maturity of time deposits      
–
–
271,201
267,036
26,513
Proceeds from disposal of
financial assets at amortised
cost                 
–
–
982,359
862,084
2,531,476
Purchase of financial assets at
amortised cost           
–
–
(1,121,788)
(1,033,743)
(2,380,324)
Purchases of financial assets at
fair value through other
comprehensive income      
–
–
(4,174)
(4,174)
–
Proceeds from disposal of
financial assets at fair value
through profit or loss       
11,050
136,076
1,851,346
1,056,303
1,519,366
Purchases of financial assets at
fair value through profit or
loss                  
(45,950)
(85,299)
(2,210,385)
(1,582,273)
(1,822,783)
Net cash flows used in investing
activities              
(35,156)
(40,320)
(431,300)
(630,463)
(126,231)
CASH FLOWS FROM
FINANCING ACTIVITIES
Proceeds from issuance of
convertible bonds         
–
–
13,910
13,910
–
Proceeds from issuance of
convertible redeemable
preferred shares          
50,000
307,000
739,588
686,372
426,262
New bank and other borrowings 
–
–
19,455
19,455
44,565
Repayment of bank and
other borrowings         
–
–
–
–
(44,918)
Repayment of convertible bonds 
–
–
–
–
(14,668)
Interest paid for bank borrowings 
–
–
(355)
(199)
(404)
Principal portion of lease
payments              
14(b)
(200)
(696)
(1,352)
(1,097)
(1,364)
Interest paid for leases       
14(b)
(14)
(61)
(154)
(117)
(107)
Payment of Listing expenses    
–
–
–
–
(357)
Others                 
–
–
–
503
(1,096)
Net cash flows from financing
activities              
49,786
306,243
771,092
718,827
407,913
APPENDIX I
ACCOUNTANT’S REPORT
– I-14 –

<<<PAGE 552>>>
Year ended 31 December
Nine months ended
30 September
Notes
2022
2023
2024
2024
2025
USD’000
USD’000
USD’000
USD’000
USD’000
(unaudited)
NET INCREASE/(DECREASE)
IN CASH AND CASH
EQUIVALENTS         
3,611
201,468
81,309
(107,232)
72,286
Cash and cash equivalents at
beginning of year/period     
994
4,691
206,295
206,295
288,912
Effect of foreign exchange rate
changes, net            
86
136
1,308
500
1,449
CASH AND CASH
EQUIVALENTS AT END OF
YEAR/PERIOD          
18
4,691
206,295
288,912
99,563
362,647
APPENDIX I
ACCOUNTANT’S REPORT
– I-15 –

<<<PAGE 553>>>
STATEMENTS OF FINANCIAL POSITION OF THE COMPANY
As at 31 December
As at
30 September
Notes
2022
2023
2024
2025
USD’000
USD’000
USD’000
USD’000
NON-CURRENT ASSETS
Investments in subsidiaries     
17
1,069
4,415
11,238
19,819
Financial assets at fair value
through profit or loss       
17
–
–
95,331
70,228
Total non-current assets      
1,069
4,415
106,569
90,047
CURRENT ASSETS
Prepayments, other receivables
and other assets           
16
14,100
103,895
360,091
663,642
Financial assets at amortised
cost                    
17
–
–
147,444
–
Financial assets at fair value
through profit or loss       
17
65,791
10,152
295,220
639,899
Restricted cash              
18
–
–
11,802
–
Time deposits               
18
–
91,598
26,327
–
Cash and cash equivalents     
18
1,784
191,634
235,209
250,712
Total current assets         
81,675
397,279
1,076,093
1,554,253
CURRENT LIABILITIES
Convertible redeemable
preferred shares           
24
145,175
629,001
1,581,949
2,321,193
Other payables, accruals and
other liabilities            
–
330
71
1,319
Total current liabilities       
145,175
629,331
1,582,020
2,322,512
NET CURRENT
LIABILITIES            
(63,500)
(232,052)
(505,927)
(768,259)
TOTAL ASSETS LESS
CURRENT LIABILITIES  
(62,431)
(227,637)
(399,358)
(678,212)
NON-CURRENT
LIABILITIES
Total non-current liabilities   
–
–
–
–
Net liabilities              
(62,431)
(227,637)
(399,358)
(678,212)
DEFICITS
Share capital               
–
–
–
–
Deficits                   
25
(62,431)
(227,637)
(399,358)
(678,212)
Total deficits               
(62,431)
(227,637)
(399,358)
(678,212)
APPENDIX I
ACCOUNTANT’S REPORT
– I-16 –

<<<PAGE 554>>>
II
NOTES TO THE HISTORICAL FINANCIAL INFORMATION
1.
CORPORATE AND GROUP INFORMATION
MINIMAX GROUP INC. (the “Company”) was incorporated in the Cayman Islands as a limited liability
company in June 2021. The registered office address of the Company is Maples Corporate Services Limited, PO Box
309, Ugland House, Grand Cayman, KY1-1104, Cayman Islands.
During the Relevant Periods, the Company and its subsidiaries (together the “Group”) were principally
involved in the research and development of Artificial Intelligence (“AI”) foundation model, as well as rendering
relevant service based on open Application Programming Interface (“API”) platform, other Artificial Intelligence
(“AI”) based services and AI-native products.
Information about subsidiaries
As at the end of the Relevant Periods and the date of the Prospectus, the Company had direct and indirect
interests in its subsidiaries, all of which are private limited liability companies, particulars of the principal
subsidiaries are set out below:
Name
Place and date of
incorporation/
registration and place
of operations
Issued ordinary/
registered share
capital
Percentage of
equity attributable
to the Company
Principal activities
Direct
Indirect
SUBSUP PTE. LTD. (a)      Singapore,
14 September 2022
SGD50,000
–
100 Operation of
AI-native products
Beijing Xiyu Jizhi Technology
Co., Ltd.* (“Beijing Jizhi”)
(“北京稀宇極智科技有限公司”)
(b)                
PRC/Mainland China,
18 November 2021
RMB139,995,700
–
100 Research and
development of AI
foundation model
Shanghai Xiyu Jizhi Technology
Co., Ltd.* (“Shanghai Jizhi”)
(“上海稀宇極智科技有限公司”)
(c)                
PRC/Mainland China,
3 November 2021
RMB1,000,000,000
–
100 Research and
development of AI
foundation model
Shanghai Xiyu Technology
Co., Ltd.* (“Shanghai
MiniMax”) (“上海稀宇科技有
限公司”) (d)(e)         
PRC/Mainland China,
28 January 2023
RMB2,030,303
–
100 Operation of open
platform and AI-
native products
NanoNoble PTE. LTD. (a)     Singapore,
19 March 2024
SGD50,000
–
100 Operation of open
platform and AI-
native products
MiniMax HONGKONG
Limited (f)           
Hong Kong, 23 July
2021
HKD1
100
– Investment holding
*
The English names of the PRC companies above represent management’s best efforts in translating the
Chinese names of these companies as no English names have been registered.
(a)
No audited financial statements have been prepared for these entities for the years ended 31 December
2022, 2023 and 2024, as the entities were not subject to any statutory audit requirements under the
relevant rules and regulations in their jurisdictions of incorporation.
(b)
Beijing Jizhi is registered as a limited liability company under PRC law. The statutory financial
statements for the year ended December 31, 2022 under the PRC Generally Accepted Accounting
Principles (“PRC GAAP”) were audited by Beijing Dongcai Certified Public Accountants (General
Partnership), certified public accountants registered in the PRC. The statutory financial statements for
the year ended December 31, 2023 and 2024 under the PRC GAAP were audited by Shanghai Xuri
Certified Public Accountants (General Partnership), certified public accountants registered in the PRC.
APPENDIX I
ACCOUNTANT’S REPORT
– I-17 –

<<<PAGE 459>>>
Cash Flow Analysis
The following table sets forth our cash flows for the periods indicated.
For the year ended December 31,
For the nine months ended
September 30,
2022
2023
2024
2024
2025
(unaudited)
(US$ in thousands)
Net cash flows used
in operating
activities        
(11,019)
(64,455)
(258,483)
(195,596)
(209,396)
Net cash flows used
in investing
activities        
(35,156)
(40,320)
(431,300)
(630,463)
(126,231)
Net cash flows
generated from
financing activities
49,786
306,243
771,092
718,827
407,913
Net increase/
(decrease) in cash
and cash
equivalents      
3,611
201,468
81,309
(107,232)
72,286
Cash and cash
equivalents at the
beginning of the
year/period      
994
4,691
206,295
206,295
288,912
Effect of foreign
exchange
differences, net   
86
136
1,308
500
1,449
Cash and cash
equivalents at the
end of the
year/period      
4,691
206,295
288,912
99,563
362,647
FINANCIAL INFORMATION
– 449 –

<<<PAGE 460>>>
Net Cash Flows Used in Operating Activities
Net cash flows used in operating activities in the nine months ended September 30, 2025
was US$209.4 million, which primarily consists of loss before tax of US$512.0 million,
adjusted for certain non-cash and non-operating items. Adjustments for such non-cash and
non-operating items primarily include (i) a fair value loss on financial liabilities of US$313.5
million, and (ii) Share-based payment expenses of US$8.6 million. The amount was further
adjusted by changes in working capital, primarily including (i) an increase in trade and bills
payables of US$19.0 million, and (ii) an increase in contract liabilities of US$3.1 million,
partially offset by a decrease in other payables, accruals and other liabilities of US$22.9
million.
Net cash flows used in operating activities in 2024 was US$258.5 million, which
primarily consists of loss before tax of US$465.2 million, adjusted for certain non-cash and
non-operating items. Adjustments for such non-cash and non-operating items primarily include
fair value loss on financial liabilities of US$214.2 million. The amount was further adjusted by
changes in working capital, primarily including (i) an increase in trade and bills payables of
US$34.0 million, and (ii) an increase in other payables, accruals and other liabilities of
US$21.0 million, partially offset by an increase in restricted cash of US$27.3 million.
Net cash flows used in operating activities in 2023 was US$64.5 million, which consists
primarily of loss before tax of US$269.2 million, adjusted for certain non-cash and
non-operating items. Adjustments for such non-cash and non-operating items primarily include
fair value loss on financial liabilities of US$176.8 million. The amount was further adjusted by
changes in working capital, primarily including (i) an increase in trade and bills payables of
US$14.8 million, and (ii) an increase in other payables, accruals and other liabilities of
US$12.6 million, partially offset by an increase in prepayments, other receivables and other
assets of US$4.2 million.
Net cash flows used in operating activities in 2022 was US$11.0 million, which consists
primarily of loss before tax of US$73.7 million, adjusted for certain non-cash and non-
operating items. Adjustments for such non-cash and non-operating items primarily include (i)
fair value loss on financial liabilities of US$60.5 million. The amount was further adjusted by
changes in working capital, primarily including (i) an increase in other payables, accruals and
other liabilities of US$2.2 million, and (ii) an increase in trade and bills payables of US$2.4
million, partially offset by an increase in prepayments, other receivables and other assets of
US$0.5 million.
FINANCIAL INFORMATION
– 450 –

<<<PAGE 461>>>
We are still at a nascent stage in terms of monetization and commercialization as
historically we have been largely focused on developing and training our AI foundation
models, growing our customer base, and expanding our AI-native product suite, rather than
seeking immediate financial return or profitability, thus incurring net operating cash outflows
throughout the Track Record Period. It is industry norm that the initial research and training
of foundation model will take approximately 2-3 years, where investment in research and
development is needed (mainly the cloud and services expenses related to training) before the
models and products could generate commercial value in scale. In 2023, 2024 and the nine
months ended September 30, 2025, our cloud services expense related to training were
US$47.2 million, US$140.6 million and US$142.4 million. As model intelligence continues to
elevate and gradually unlock more application scenarios, we have been gradually monetizing
our models and products. For example, we commenced revenue generation of Open Platform
in May 2023, Talkie in June 2023, Hailuo AI in October 2024, and MiniMax in January 2025.
As we scaled up operations, our revenue increased from US$3.5 million in 2023 to
US$30.5 million in 2024, and for the nine months ended September 30, 2025, our revenue
further increased to US$53.4 million, compared to US$19.5 million in the nine months ended
September 30, 2024. We also significantly improved our gross profit margin, from negative
24.7% in 2023 to 12.2% in 2024, and further to 23.3% in the nine months ended September 30,
2025, primarily driven by advancement in the intelligence level of our models, improved model
and system efficiency, optimization of infrastructure allocation, and increased scale of revenue
relative to compute intensity, in line with our strategy to enhance efficiency of our AI
infrastructure. As a result, we significantly narrowed our adjusted net loss (non-IFRS measure)
as a percentage of revenue, from over 2,500% in 2023 to 800.2% in 2024 and further to 348.6%
in the nine months ended September 30, 2025.
In the future, we aim to continue to enhance our profitability and improve our net
operating cash outflows position through the following focus areas: (i) leveraging the rapid
growth of the foundation model industry, (ii) continuing to enhance foundation model
intelligence levels, (iii) enhancing the affordability of our AI technologies, (iv) broadening
monetization of our AI-native product suite, and (v) optimizing organizational efficiency and
scalability. Please refer to “Path to the Commercialization of our Specialist Technology
Products” for our detailed strategies.
Net Cash Flows Used in Investing Activities
Net cash flows generated from investing activities in the nine months ended September
30, 2025 was US$126.2 million, which consists primarily of (i) purchase of financial assets at
amortized cost of US$2,380.3 million, and (ii) purchases of financial assets at fair value
through profit or loss of US$1,822.8 million, partially offset by (i) proceeds from disposal of
financial assets at amortized cost of US$2,531.5 million, and (ii) proceeds from disposal of
financial assets at fair value through profit or loss of US$1,519.4 million.
FINANCIAL INFORMATION
– 451 –

<<<PAGE 462>>>
Net cash flows used in investing activities in 2024 was US$431.3 million, which consists
primarily of (i) purchases of financial assets at fair value through profit or loss of US$2,210.4
million and (ii) purchase of financial assets at amortised cost of US$1,121.8 million, partially
offset by (i) proceeds from disposal of financial assets at fair value through profit or loss of
US$1,851.3 million and (ii) proceeds from disposal of financial assets at amortised costs of
$982.4 million.
Net cash flows used in investing activities in 2023 was US$40.3 million, which consists
primarily of (i) placement of time deposits of US$90.4 million and (ii) purchases of financial
assets at fair value through profit or loss of US$85.3 million, partially offset by proceeds from
disposal of financial assets at fair value through profit or loss of US$136.1 million.
Net cash flows used in investing activities in 2022 was US$35.2 million, which consists
primarily of purchases of financial assets at fair value through profit or loss of US$46.0
million, partially offset by proceeds from disposal of financial assets at fair value through
profit or loss of US$11.1 million.
Net Cash Flows Generated from Financing Activities
Net
cash
flows
generated
from
financing
activities
in
the
nine
months
ended
September 30, 2025 was US$407.9 million, which consists primarily of proceeds from issuance
of convertible redeemable preferred shares of US$426.3 million.
Net cash flows generated from financing activities in 2024 was US$771.1 million, which
consists primarily of proceeds from issuance of convertible redeemable preferred shares of
US$739.6 million.
Net cash flows generated from financing activities in 2023 was US$306.2 million, which
consists primarily of proceeds from issuance of convertible redeemable preferred shares of
US$307.0 million.
Net cash flows generated from financing activities in 2022 was US$49.8 million, which
consists primarily of proceeds from issuance of convertible redeemable preferred shares of
US$50.0 million.
FINANCIAL INFORMATION
– 452 –

<<<PAGE 473>>>
our profitability, provided that our memorandum and articles of association do not prohibit
such payment and our Company is able to pay its debts as they fall due in the ordinary course
of business immediately after such payment.
If we pay dividends in the future, in order for us to distribute dividends to our
Shareholders, we will rely to some extent on any dividends distributed by our PRC
subsidiaries. Any dividend distributions from our PRC subsidiaries to us will be subject to PRC
withholding tax. In addition, regulations in the PRC currently permit payment of dividends of
a PRC company only out of accumulated distributable after-tax profits as determined in
accordance with its articles of association and the accounting standards and regulations in
China. See “Risk Factors — Risks Related to Doing Business in the Geographic Markets in
Which We Operate” in this Prospectus.
WORKING CAPITAL SUFFICIENCY
Our Directors are of the opinion that, taking into account (i) the financial resources
available to our Group, including the cash and cash equivalents of US$362.6 million as well
as the current portion of financial assets at fair value through profit and loss US$644.2 million,
as of September 30, 2025, (ii) the estimated net proceeds from the Global Offering and (iii)
expected net cash used in operating activities and capital expenditures, we have sufficient
working capital to cover at least 125% of our costs, including research and development costs
and administrative expenses for the next 12 months from the date of this Prospectus.
DISTRIBUTABLE RESERVES
As of September 30, 2025, our Company did not have any distributable reserves.
LISTING EXPENSES
Our
listing
expenses
mainly
include
(i)
underwriting-related
expenses,
such
as
underwriting fees and commissions, and (ii) non-underwriting-related expenses, comprising
professional fees paid to our legal advisors and reporting accountants for their services
rendered in relation to the Listing and the Global Offering, and other fees and expenses.
Assuming full payment of the discretionary incentive fee, the estimated total listing expenses
(based on the mid-point of the Offer Price range and assuming that the Offer Size Adjustment
Option and the Over-allotment Option are not exercised) for the Global Offering are
approximately HK$193.2 million, accounting for approximately 4.8% of our gross proceeds.
Among such estimated total listing expenses, we expect to pay underwriting-related expenses
of HK$133.0 million, professional fees for our legal advisors and reporting accountants of
HK$40.3 million and other fees and expenses of HK$19.9 million. During the Track Record
Period, the listing expenses charged to our consolidated statements of profit or loss were
US$3.7 million (HK$28.6 million) and the issuance costs which were recognized as
prepayments and are expected to be deducted from equity upon the Listing, were US$0.4
FINANCIAL INFORMATION
– 463 –

<<<PAGE 474>>>
million (HK$3.3 million). After the Track Record Period approximately HK$26.7 million is
expected to be charged to our consolidated statements of profit or loss, and approximately
HK$134.7 million is expected to be accounted for as a deduction from equity upon the Listing.
UNAUDITED PRO FORMA STATEMENT OF ADJUSTED CONSOLIDATED NET
TANGIBLE ASSETS
The following unaudited pro forma adjusted consolidated net tangible assets of our
Group, prepared in accordance with Rule 4.29 of the Listing Rules and with reference to
Accounting Guideline 7 Preparation of Pro Forma Financial Information for inclusion in
Investment Circulars issued by the Hong Kong Institute of Certified Public Accountants, is for
illustration purposes only and is set out here to illustrate the effect of the Global Offering on
the consolidated net tangible assets of our Group attributable to owners of the parent as of
September 30, 2025, as if the Global Offering had taken place on September 30, 2025.
The unaudited pro forma statement of adjusted consolidated net tangible assets of our
Group has been prepared for illustrative purposes only and, because of its hypothetical nature,
it may not give a true picture of the consolidated net tangible assets of our Group to owners
of the parent had the Global Offering been completed as of September 30, 2025 or at any future
dates. The unaudited pro forma statement of adjusted consolidated net tangible liabilities does
not form part of the Accountants’ Report.
Unadjusted
audited
consolidated net
tangible
liabilities
attributable to
the owners of
our Group as of
September 30,
2025
Estimated net
proceeds from
the Global
Offering
Estimated
impact related
to the
reclassification
of convertible
redeemable
preferred shares
upon Listing
Unaudited pro
forma adjusted
consolidated net
tangible assets
attributable to
owners of our
Group as of
September 30,
2025
Unaudited pro forma
adjusted consolidated net
tangible assets attributable
to owners of our Group
per Share as of September
30, 2025
US$’000
US$’000
US$’000
US$’000
US$
HK$
Note(1)
Note(2)
Note(3)
Note(3)
Note(4)
Based on an Offer Price of
HK$151.00
per Share          
(1,303,499)
472,382
2,321,193
1,490,076
4.88
37.96
Based on an Offer Price of
HK$158.00
per Share          
(1,303,499)
494,423
2,321,193
1,512,117
4.95
38.52
Based on an Offer Price of
HK$165.00
per Share          
(1,303,499)
516,464
2,321,193
1,534,158
5.02
39.08
FINANCIAL INFORMATION
– 464 –

<<<PAGE 475>>>
Notes:
(1)
The consolidated net tangible liabilities of our Group attributable to owners of the Company as of September
30, 2025 was based on the consolidated net liabilities attributable to owners of the Company as at September
30, 2025 of US$1,303,499,000 set out in the Accountants’ Report in Appendix I to this Prospectus.
(2)
The estimated net proceeds from the Global Offering are based on estimated low end, mid-point and high end
offer prices of HK$151.00, HK$158.00 and HK$165.00 per Share after deduction of underwriting fees and
commissions and other related expenses payable by the Company and do not take into account any shares
which may be issued upon exercise of the Offer Size Adjustment Option and the Over-allotment Option.
(3)
For the purpose of the unaudited pro forma financial information, considering the estimated impact related to
the reclassification of convertible redeemable preferred shares upon Listing, the unaudited pro forma adjusted
net tangible assets attributable to the owners of the Company will be increased by USD2,321,193,000 being
the fair value of the convertible redeemable preferred shares as at September 30, 2025. Upon the Listing and
the completion of the Global Offering, all the convertible redeemable preferred shares will be automatically
converted into Shares. These convertible redeemable preferred shares will be reclassified from liabilities to
equity. The amount that is reclassified from liabilities to equity will be the fair value of the Preferred Shares
on that date of the Global Offering.
(4)
The unaudited pro forma adjusted consolidated net tangible assets attributable to Shareholders of the Company
per Share is arrived at after the adjustments referred to in the preceding paragraphs (note 2 and 3 above) and
on the basis that 305,447,288 shares were in issue assuming that the Global Offering and reclassification of
financial liabilities arising from the convertible redeemable preferred shares and ordinary shares into equity
had been completed on September 30, 2025, without taking account of the exercise of the Offer Size
Adjustment Option and the Over-allotment Option.
(5)
For the purpose of this unaudited pro forma adjusted consolidated net tangible assets, The unaudited pro forma
adjusted consolidated net tangible assets attributable to Shareholders of the Company per Share amounts in
USD are converted into Hong Kong dollars at USD1.00 = HKD7.7805 prevailing on the latest practical date.
No representation is made that the Hong Kong dollar amounts have been, could have been or may be converted
to United States dollars, or vice versa, at that rate or any other rates or at all.
(6)
No other adjustment has been made to the unaudited pro forma adjusted consolidated net tangible asset of the
Group to reflect any trading result or other transactions entered into subsequent to September 30, 2025.
Please refer to “Appendix II — Unaudited Pro Forma Financial Information” for further
details.
NO MATERIAL ADVERSE CHANGE
Our Directors have confirmed that, up to the date of the Prospectus, there had been no
material adverse change in our financial, operational or trading position, indebtedness,
contingent liabilities or prospects since September 30, 2025, being the end date of the periods
reported on in the Accountants’ Report set out in Appendix I to this Prospectus, and there had
been no event since September 30, 2025, that would materially affect the information shown
in the Accountants’ Report set out in Appendix I to this Prospectus.
DISCLOSURE UNDER RULES 13.13 TO 13.19 OF THE LISTING RULES
Our Directors confirm that, except for the amounts due from related parties as disclosed
in this section, as of the Latest Practicable Date, there were no circumstances that would give
rise to a disclosure requirement under Rules 13.13 to 13.19 of the Listing Rules.
FINANCIAL INFORMATION
– 465 –

<<<PAGE 476>>>
FUTURE PLANS
See the section headed “Business — Our Strategies” for a detailed description of our
future plans.
USE OF PROCEEDS
We estimate that we will receive net proceeds from the Global Offering of approximately
HK$3,818.3 million, after deducting underwriting commissions, fees and estimated expenses
payable by us in connection with the Global Offering, assuming no Offer Size Adjustment
Option or Over-allotment Option is exercised and an Offer Price of HK$158.00 per Offer
Share, being the midpoint of the indicative Offer Price range stated in this Prospectus.
Approximately 90%, or HK$3,436.4 million of the net proceeds will be used for our
research and development over the next five years including the development of our foundation
models and our AI-native products. In line with our strategies, we intend to use the net
proceeds for the following purposes, subject to changes in light of our evolving business needs
and changing market conditions:
•
Development
of
Our
Foundation
Models.
To
reinforce
our
technological
leadership, we plan to allocate approximately 70.0%, or HK$2,672.8 million, of the
net proceeds over the next five years to the research and development of our
foundation models, including investments in AI infrastructure and R&D talent. Our
core competitive advantage lies in our innovation across the entire foundation model
stack. Advancing the intelligence, efficiency and scalability of our foundation
models is critical to strengthening our competitiveness and differentiation in the
global market. We have observed that our models’ competitiveness, is directly
related to our models’ market pricing and demand.
(i)
Enhancing AI
Infrastructure
for Model
R&D. We
plan
to
allocate
approximately 50.0%, or HK$1,909.1 million, of the net proceeds to enhance
the AI infrastructure* that supports the development of our foundation models.
This amount will be used entirely for R&D expenses. As our industry relies on
ever-increasing computing power to train advanced AI models, we believe
continuous upgrades to our AI infrastructure are essential. Our research and
development
activities,
such
as
training
large
foundation
models,
experimenting with model designs, conducting large-scale evaluations, and
developing early prototypes, all depend significantly on our AI infrastructure.
We will continue to work with our cloud infrastructure and computing services
vendors to expand and upgrade our AI infrastructure to support increasingly
*
Mainly includes computing services purchased from third-party cloud service providers, namely computing
power, storage and network capacity that we rent from external cloud platforms instead of building and owning
all the servers ourselves. In practice, this mainly includes high-performance servers, data storage and
high-speed network, which we use to train, test and run our large language models and to support user traffic
on our Open Platform and AI-native products.
FUTURE PLANS AND USE OF PROCEEDS
– 466 –

<<<PAGE 438>>>
Research and Development Expenses
Our research and development expenses increased by 30.0% from US$138.7 million for
the nine months ended September 30, 2024 to US$180.3 million during the same period in
2025, mainly attributed to an increase in cloud services expenses related to training activities,
driven by the increased model iteration and upgrades as we continued to develop and refine our
foundation models and multi-modal capabilities. The year over year growth rate of our research
and development expenses in the nine months ended September 30, 2025 was 30.0%,
significantly lower than our revenue growth rate of 174.7% during the same period,
demonstrating our improved research and development efficiency.
Fair Value Loss on Financial Liabilities
Our fair value loss on financial liabilities increased from US$128.1 million for the nine
months ended September 30, 2024 to US$313.5 million during the same period in 2025, mainly
driven by significant remeasurement losses on our preferred shares due to continued increases
in our valuation.
Finance Costs
Our finance costs increased by 61.7% from US$0.3 million for the nine months ended
September 30, 2024 to US$0.5 million during the same period in 2025, primarily due to an
increase in interest on bank and other borrowings from US$0.2 million to US$0.4 million over
the period.
Impairment Losses on Financial Assets, Net
We recorded impairment losses on financial assets, net of US$68.0 thousand for the nine
months ended September 30, 2024 and US$22.0 thousand during the same period in 2025. The
improvement over impairment losses on financial assets, net was primarily attributable to our
effective collection efforts, which resulted in the release of previously recognised expected
credit loss provisions.
Loss for the Period
As a result of the foregoing, our loss for the period increased by 68.2% from US$304.3
million for the nine months ended September 30, 2024 to US$512.0 million during the same
period in 2025.
Year Ended December 31, 2024 Compared with Year Ended December 31, 2023
Revenue
Our revenue increased significantly by 782.2% from US$3.5 million in 2023 to US$30.5
million in 2024. This increase was primarily driven by the advancement in intelligence level
of our foundation model, which resulted in rapid growth across both of our monetization
channels — Open Platform and other AI-based enterprise services and AI-native products —
as we scaled up commercialization of our AI-native product suite and user base.
FINANCIAL INFORMATION
– 428 –

<<<PAGE 439>>>
AI-native products. Revenue from AI-native products increased by 2,776.6% from
US$0.8
million
in
2023
to
US$21.8
million
in
2024,
as
we
began
ramping
up
commercialization mainly through online marketing services and value-added premium
features. Such initial monetization success was fueled by continued expansion in our
consumer-facing product suite. Specifically, we expanded value-added premium features in
core monetized products such as Hailuo AI and Talkie/Xingye, and actively optimized pricing
tiers to enhance monetization efficiency. Average MAUs grew from approximately 3.1 million
in 2023 to 19.1 million in 2024, and paying users for AI-native products rose from
approximately 119,700 in 2023 to approximately 650,300 in 2024, reflecting increased user
willingness to pay for premium and intelligent experiences. With an increasingly engaged user
base, we were able to grow our online marketing services associated with certain AI-native
products.
Open Platform and other AI-based enterprise services. Revenue from our Open
Platform and other AI-based enterprise services increased by 222.6% from US$2.7 million in
2023 to US$8.7 million in 2024. This was driven primarily by increased adoption of our Open
Platform, which experienced growth in token volume and enterprise developer subscriptions.
The number of key paying users, defined as users who have individually consumed no less than
US$50 worth of API calls (or its equivalent in other currencies) grew from approximately 100
in 2023 to 700 in 2024.
Cost of Sales
Our cost of sales increased by 520.9% from US$4.3 million in 2023 to US$26.8 million
in 2024, primarily attributable to a 533.8% increase in cloud service used to support inference
workloads across our AI-native consumer applications and open platform, which rose from
US$4.1 million to US$26.0 million over the same period. This increase was driven by greater
infrastructure usage to support inference workloads across our AI-native consumer applications
and
enterprise-facing
open
platform,
as
cumulative
user
interactions
and API
token
consumption surged during the year.
Gross Profit and Gross Profit Margin
As a result of the foregoing, our gross profit increased from negative US$0.9 million in
2023 to US$3.7 million in 2024. Our gross profit margin increased from negative 24.7% in
2023 to 12.2% in 2024, resulting from the changes in the mix of our revenue sources and their
respective gross profit margins.
The increase in our overall gross profit margin was primarily driven by improved
intelligence level of our foundation models and model inference efficiency. In particular, the
gross profit margin for AI-native products, which was the most significant contributor to our
revenue during the Track Record Period, significantly improved from negative 380.2% in 2023
to negative 8.1% in 2024, primarily attributed to improvements in the intelligence level of our
foundation models, user engagement and monetization, and introduction of new monetized
features.
FINANCIAL INFORMATION
– 429 –

<<<PAGE 440>>>
Other Income and Gains, Net
Our other income and gains, net increased by 304.3% from US$8.9 million in 2023 to
US$36.2 million in 2024, respectively. This increase was primarily attributable to a significant
rise in fair value gains on financial assets at fair value through profit or loss, which increased
by 1,893.7%, from US$0.8 million in 2023 to US$15.7 million in 2024. These gains primarily
reflected unrealized mark-to-market increases in the carrying value of certain financial
instruments, including investments designated at fair value. To a lesser extent, interest income
increased by 162.7% from US$7.8 million in 2023 to US$20.4 million in 2024, mainly due to
higher average cash balances.
Selling and Distribution Expenses
Our selling and distribution expenses increased by 281.1% from US$22.8 million in 2023
to US$87.0 million in 2024. This increase was primarily driven by a 285.1% increase in
business promotion expenses, which rose from US$22.0 million in 2023 to US$84.9 million in
2024. The increase was due to our exploration of various user growth channels during our
initial period of commercialization. To a lesser extent, staff costs increased by 168.0% from
US$0.7 million in 2023 to US$1.9 million in 2024, attributable to increases in headcount for
personnel engaged in sales and marketing.
Administrative Expenses
Our administrative expenses increased by 88.9% from US$7.6 million in 2023 to US$14.4
million in 2024, mainly driven by (i) a 130.0% increase in staff costs from US$2.4 million in
2023 to US$5.5 million in 2024 due to higher headcount for administrative personnel and (ii)
a 80.4% increase in professional service fees from US$1.9 million in 2023 to US$3.5 million
in 2024, mainly due to increased cost for legal, audit and advisory expenses and hiring
expenses in connection with our growing operations.
Research and Development Expenses
Our research and development expenses increased by 170.0% from US$70.0 million in
2023 to US$189.0 million in 2024, mainly attributed to (i) a 197.8% increase in cloud services
expenses related to training activities from US$47.2 million in 2023 to US$140.6 million in
2024 due to increased model training, evaluation, and architecture experimentation activities
as we continued to develop our foundation models and multi-modal capabilities and (ii) a
116.5% increase in staff costs, from US$18.7 million to US$40.4 million over the same period,
attributable to higher headcount for our in-house research and engineering teams. The year
over year growth rate of our research and development expense in 2024 was 170.0%,
significantly lower than our revenue growth rate of 782.2% during the same period,
demonstrating our improved research and development efficiency.
FINANCIAL INFORMATION
– 430 –

<<<PAGE 441>>>
Fair Value Loss on Financial Liabilities
Our fair value loss on financial liabilities increased by 21.1% from US$176.8 million in
2023 to US$214.2 million in 2024, primarily due to continued remeasurement losses on our
preferred shares in 2024, as our valuation increased during the year.
Finance Costs
Our finance costs increased by 734.4% from US$61 thousand in 2023 to US$0.5 million
in 2024. This increase was primarily attributable to the incurrence of interest expenses of
US$0.4 million in 2024 on bank loans and other borrowings, as we initiated financing
arrangements to support our working capital and operating needs. Interest on lease liabilities
also increased by 152.5%, from US$61.0 thousand in 2023 to US$0.2 million in 2024, as we
expanded our office footprint and entered into new lease agreements to accommodate
headcount growth across functions.
Impairment Losses on Financial Assets, Net
We recorded impairment losses on financial, net of US$3.0 thousand and US$88.0
thousand in 2023 and 2024, respectively. The increase was primarily attributable to provisions
recognised on trade receivables and contract assets in connection with our expanding revenue
base and customer coverage. As we scaled up monetization activities, we implemented
expected credit loss assessments across a broader set of accounts to align with our credit risk
management policies.
Loss for the Year
As a result of the foregoing, our loss for the year increased by 72.8% from US$269.2
million in 2023 to US$465.2 million in 2024.
Year Ended December 31, 2023 Compared with Year Ended December 31, 2022
Revenue
Our revenue increased from nil in 2022 to US$3.5 million in 2023. This increase was
primarily driven by initial commercialization across both monetization channels as we
launched our AI-native products and began scaling user and enterprise adoption.
AI-native products. We did not generate any revenue from our AI-native products in
2022. In 2023, we recorded US$0.8 million revenue generated by our AI-native products,
attributable to the introduction of paid tiers across our consumer-facing applications. Our
average MAUs reached approximately 3.1 million during the year and our paying users for
AI-native products reached approximately 119,700, as early monetization efforts, including for
Talkie/Xingye, gained initial traction.
FINANCIAL INFORMATION
– 431 –

<<<PAGE 443>>>
Administrative Expenses
Our administrative expenses increased by 137.0% from US$3.2 million in 2022 to US$7.6
million in 2023, mainly driven by (i) an increase in staff costs from US$0.7 million to US$2.4
million due to headcount growth across administrative functions and (ii) a rise in professional
service fees from US$0.7 million in 2022 to US$1.9 million in 2023, as we engaged legal,
financial, and compliance consultants in connection with operational expansion and financing
activities.
Research and Development Expenses
Our research and development expenses increased by 562.9% from US$10.6 million in
2022 to US$70.0 million in 2023. This increase was primarily driven by (i) cloud services
expenses related to training activities, which rose by from US$4.1 million in 2022 to US$47.2
million in 2023, due to intensified model training and evaluation activity, and (ii) staff costs,
which increased from US$5.5 million to US$18.7 million, due to growth in our research and
engineering team headcount and compensation levels.
Fair Value Loss on Financial Liabilities
Our fair value loss on financial liabilities increased by 192.2% from US$60.5 million in
2022 to US$176.8 million in 2023, mainly driven by higher remeasurement losses on our
preferred shares due to valuation appreciation during the period.
Finance Costs
Our finance costs increased by 335.7% from US$14.0 thousand in 2022 to US$61.0
thousand in 2023, primarily due to higher interest on lease liabilities, reflecting additional lease
arrangements entered into to support team expansion and infrastructure needs.
Impairment Losses on Financial and Contract Assets, Net
We did not record impairment losses on financial and contract assets in 2022. In 2023, we
recognised US$3.0 thousand in impairment losses, primarily reflecting expected credit losses
assessed on a limited set of customer accounts in our early revenue-generating activities.
Loss for the Year
As a result of the foregoing, our loss for the year increased by 265.2% from US$73.7
million in 2022 to US$269.2 million in 2023.
FINANCIAL INFORMATION
– 433 –

<<<PAGE 444>>>
DISCUSSION
OF
CERTAIN
KEY
ITEMS
FROM
OUR
CONSOLIDATED
STATEMENTS OF FINANCIAL POSITION
The table below sets forth selected information from our consolidated statements of
financial position as of the dates indicated, which has been extracted from our consolidated
financial statements included in Appendix I to this Prospectus.
As of December 31,
As of
September 30,
2022
2023
2024
2025
(US$ in thousands)
NON-CURRENT ASSETS
Property, plant and
equipment             
231
709
1,093
1,134
Right-of-use assets        
458
3,313
3,077
2,746
Prepayments, other
receivables and other
assets                
–
435
561
731
Financial assets at fair value
through profit or loss    
–
–
95,331
70,228
Financial assets at fair value
through other
comprehensive income   
–
–
4,836
6,440
Restricted cash           
–
39
38
41
Total non-current assets   
689
4,496
104,936
81,320
CURRENT ASSETS
Trade receivables         
–
1,338
6,982
8,063
Prepayments, other
receivables and other
assets                
569
4,378
13,470
11,811
Financial assets at amortised
costs                 
–
–
147,444
–
Financial assets at fair value
through profit or loss    
65,791
15,802
295,220
644,154
Time deposits            
–
91,698
26,327
–
Restricted cash           
2,221
–
27,293
25,097
Cash and cash equivalents  
4,691
206,295
288,912
362,647
Total current assets      
73,272
319,511
805,648
1,051,772
FINANCIAL INFORMATION
– 434 –

<<<PAGE 445>>>
As of December 31,
As of
September 30,
2022
2023
2024
2025
(US$ in thousands)
CURRENT LIABILITIES
Interest-bearing bank
borrowings            
–
–
19,455
19,102
Trade and bills payables    
2,394
17,242
51,212
70,219
Other payables, accruals and
other liabilities         
2,326
14,741
51,512
17,322
Contract liabilities        
–
559
1,553
4,657
Lease liabilities          
349
1,248
1,964
1,694
Convertible redeemable
preferred shares        
145,175
629,001
1,581,949
2,321,193
Total current liabilities    
150,244
662,791
1,707,645
2,434,187
NET CURRENT
LIABILITIES         
(76,972)
(343,280)
(901,997)
(1,382,415)
TOTAL ASSETS LESS
CURRENT
LIABILITIES         
(76,283)
(338,784)
(797,061)
(1,301,095)
NON-CURRENT
LIABILITIES
Lease liabilities          
91
1,912
1,059
937
Other non-current liabilities 
–
1,218
1,200
1,467
Total non-current
liabilities             
91
3,130
2,259
2,404
Net liabilities           
(76,374)
(341,914)
(799,320)
(1,303,499)
FINANCIAL INFORMATION
– 435 –

<<<PAGE 446>>>
ASSETS
Non-Current Assets
Property, Plant and Equipment
Our property, plant and equipment primarily consist of leasehold improvements and office
equipment. Our property, plant and equipment increased from US$0.2 million as of December
31, 2022 to US$0.7 million as of December 31, 2023. The increase was due to US$0.2 million
in leasehold improvements and US$0.3 million in office equipment, which supported our
infrastructure build-out during early commercialization. Our property, plant and equipment
further increased to US$1.1 million as of December 31, 2024, mainly due to new leasehold
improvements of US$0.4 million and office equipment of US$0.5 million to support headcount
expansion and office upgrades, partially offset by depreciation of US$0.5 million recognised
for the year. Our property, plant and equipment remained relatively stable at US$1.1 million
as of September 30, 2025.
The following table sets forth a breakdown of our property, plant and equipment as of the
dates indicated.
As of December 31,
As of
September 30,
2022
2023
2024
2025
(US$ in thousands)
Leasehold improvements   
–
210
394
526
Office equipment         
231
499
699
608
Total                  
231
709
1,093
1,134
Right-of-Use Assets
Our right-of-use assets primarily consist of leased office premises. Our right-of-use assets
increased from US$0.5 million as of December 31, 2022 to US$3.3 million as of December 31,
2023, mainly due to new office lease agreements of US$3.7 million entered into during the year
to support business expansion and headcount growth. Our right-of-use assets decreased slightly
to US$3.1 million as of December 31, 2024, primarily as a result of depreciation and lease
amortization charges of US$1.5 million, partially offset by new office lease agreements of
US$1.2 million. Our right-of-use assets decreased to US$2.7 million as of September 30, 2025,
primarily due to the amortization of right-of-use assets and the early disposal of right-of-use
assets being greater than the new additions.
As at December 31, 2022, 2023, 2024 and September 30, 2025, no indicators of the
impairment for our non-financial assets were identified because (i) our non-financial assets
were no obsolete of physical damage, and (ii) our actual losses for the years ended December
31, 2022, 2023, 2024 and the nine months ended September 30, 2025 did not exceed the
estimated losses.
FINANCIAL INFORMATION
– 436 –

<<<PAGE 103>>>
•
the use of substantial amounts of cash and potentially dilutive issuances of equity
securities;
•
the occurrence of significant amortization expenses for other intangible assets; and
•
uncertainties
in
achieving
the
expected
benefits
of
synergies
and
growth
opportunities in connection with these acquisitions and investments.
Any such negative developments described above could disrupt our existing business and
have a material adverse effect on our business, reputation, financial condition and results of
operations.
We are subject to the risks associated with sanctions and export controls laws and
regulations, and developing domestic and foreign laws and regulations on AI and related
technologies, and our business, financial condition and results of operations could be
materially and adversely affected.
International trade frictions have been escalating continuously in recent years. Certain
foreign jurisdictions have imposed or may impose export controls, economic sanctions or other
trade-related measures in various forms, such as heavy tariffs or harsh trade conditions, against
certain countries, individuals and legal entities, which, from time to time, prohibit or restrict
export and import activities to a certain extent. The United States and other jurisdictions or
organization, including the European Union, the United Nations, the United Kingdom and
Australia, have, through executive order, passing of legislation or other governmental means,
implemented measures that impose economic sanctions against such countries or against targeted
industry sectors, groups of companies or persons, and/or organization within such countries.
With the escalation of the trade dispute between the U.S. and China, the U.S. government
may impose additional export control measures on components and technologies developed by
U.S. companies. For example, on April 9, 2025, the U.S. government informed NVIDIA
Corporation that the U.S. government requires a license for export to China, including Hong
Kong and Macau, or to companies headquartered or with an ultimate parent therein, of the
NVIDIA Corporation’s H20 integrated circuits and any other circuits achieving the H20’s
memory bandwidth, interconnect bandwidth, or combination thereof. The U.S. government
indicated that the license requirement addresses the risk that the covered products may be used
in, or diverted to, a supercomputer in China. Our operations may be negatively affected if any
of our business partners are added to the Entity List or subject to other forms of export control,
which may result in our failures to obtain crucial components or access to the latest
technologies originated from the U.S., and in turn, may have material and adverse impacts on
our business, results of operations, financial conditions and business prospects.
International trade policies and international export controls and economic sanctions laws
and regulations are constantly evolving. The U.S. Department of Commerce’s Bureau of
Industry and Security (“BIS”) has issued an entity list (the “Entity List”), and had been
frequently updating the Entity List to include more PRC-based hi-tech companies. New
RISK FACTORS
– 93 –

<<<PAGE 104>>>
persons and entities are regularly added to the Entity List and the list of Sanctioned Targets.
PRC-based companies on the Entity List are subject to trade sanctions and export controls on
a number of components and technologies developed by U.S. companies. Further, new
requirements or restrictions could come into effect which might increase the scrutiny on our
business or result in one or more of our business activities being deemed to have violated
sanctions. We cannot provide any assurance that our future business will be free of sanctions
risk, or our business will conform to the expectations and requirements of the authorities of
U.S. or any other jurisdictions.
On August 9, 2023, U.S. President Biden issued an executive order and his administration
issued an ANPRM providing a conceptual framework for outbound investment controls focused
on China, including Hong Kong and Macau. Further to this ANPRM, on June 21, 2024, the U.S.
Department of the Treasury issued a proposed rule on outbound U.S. investments involving
China that generally follows the ANPRM. On October 28, 2024, the U.S. Department of the
Treasury issued the Final Rule, which became effective on January 2, 2025. The Final Rule
imposes investment prohibition and notification requirements on U.S. Persons for a wide range
of investments in entities associated with China (including Hong Kong and Macau) that are
engaged in activities relating to three sectors: (i) semiconductors and microelectronics, (ii)
quantum information technologies, and (iii) AI systems, collectively defined as “covered foreign
persons.” U.S. persons subject to the Final Rule are prohibited from making, or required to
report, certain investments in covered foreign persons, which are defined as “covered
transactions,” and include acquisitions of equity interests (including contingent equity interests),
certain debt financing, joint ventures, and certain investments as a limited partner in a non-U.S.
person pooled investment fund. The Final Rule excludes some investments from the scope of
covered transactions, including certain ones in publicly traded securities. The Final Rule is aimed
at exerting greater U.S. government oversight over U.S. direct and indirect investments involving
China, and may introduce new hurdles and uncertainties for cross-border collaborations,
investments, and funding opportunities of China-based issuers including us. Since our principal
place of business is in China and we engage in the development of certain AI models, we are
likely to be deemed as a “covered foreign person” as described in the Final Rule. The acquisition
of our equity by U.S. persons may be deemed as a “covered transaction” as defined in the Final
Rule, and such “covered transaction” is likely to be deemed as a “notifiable transaction,” but not
a “prohibited transaction,” based on the level of computing power used to train the AI systems
we develop and the end-uses of such systems. As a result, such U.S. persons may need to make
a notification pursuant to the Final Rule. U.S. persons’ acquisitions of certain publicly traded
securities may be exempted from the prohibition and the notification requirement under the Final
Rule (e.g., the publicly traded securities of the Company following the completion of the Global
Offering). Investors, including those that are U.S. persons or are subsidiaries of U.S. persons,
should consult their legal counsel regarding any potential notification obligations. Certain
Underwriters have informed us that they may consider making notifications with the U.S.
Department of the Treasury. None of the Underwriters has any obligation to inform us or any
investor if they later decide that they will not file such notifications. No publicly available
precedent exists regarding the application of the OIP regulations by the U.S. Department of the
Treasury or by any court or other regulatory, judicial or legal authority to specific transactions.
In addition, the technologies of our business could change such that we are engaged in “covered
RISK FACTORS
– 94 –

<<<PAGE 105>>>
activities” that trigger the OIP’s prohibitions, or the OIP may be changed by executive actions
of the U.S. government, including modifications to the scope of activities and technologies that
are subject to prohibitions or notification requirements, or changes to the scope and availability
of applicable exceptions to the OIP’s prohibitions or notification requirements.
Specifically, on January 20, 2025, the U.S. government issued a national security
presidential memorandum entitled “America First Trade Policy”, which, among other things,
directs the Secretary of the Treasury and several other executive departments and agencies to
review the OIP to determine whether it contains “sufficient controls to address national
security threats” and to determine whether the executive order implementing the OIP “should
be modified or rescinded and replaced.” In addition, on February 21, 2025, the U.S.
government issued another national security presidential memorandum entitled “America First
Investment Policy”, which, among other things, states that the U.S. government will consider
potential expansion of the OIP to a wider range of technology sectors, including biotechnology,
hypersonics, aerospace, advanced manufacturing, directed energy, and other areas “implicated
by the PRC’s national Military-Civil Fusion strategy,” and application of restrictions to a
broader range of investments, including “publicly traded securities”. On April 3, 2025, the U.S.
government further stated that it intends to evaluate whether the scope of outbound investment
restrictions should be expanded “to be responsive to developments in technology and the
strategies of countries of concern.”
Changes to our technologies or to the OIP could limit, or in the worst-case scenario,
eliminate our ability to raise capital or contingent capital (such as convertible instruments)
from U.S. investors in the future. Our ability to raise such capital may be significantly and
adversely affected, which could negatively impact our capital-raising capacity and our
business, financial condition and prospects. In addition, changes to the Publicly Traded
Securities Exception or other aspects of the OIP could restrict or prohibit the purchase or
trading of our Shares by U.S. persons, impose new notification or other regulatory
requirements, or otherwise make our Shares less attractive to investors. In such circumstances,
the value and liquidity of our Shares may be materially and adversely affected, and in extreme
cases, our Shares could experience significant declines in trading value.
The successful operation of our business depends on the performance and reliability of the
Internet infrastructure and telecommunications networks in the countries where we
operate.
Our business depends in part on the performance, reliability and security of the
telecommunications and Internet infrastructure in the countries where we operate. In the event
of disruptions, failures or other problems with the relevant Internet infrastructure, our business
operation may be adversely affected. In addition, the Internet infrastructure in the countries in
which we operate may not support the demands associated with continued growth in Internet
usage.
RISK FACTORS
– 95 –

<<<PAGE 106>>>
The failure of telecommunications network operators to provide us with the requisite
bandwidth could also interfere with the speed and availability of our products. We have no
control over the costs of the services provided by the telecommunications operators. If the
prices that we pay for telecommunications and Internet services rise significantly, our margins
could be adversely affected. In addition, if Internet access fees or other charges to users
increase, the user base of our products may decrease, which in turn may significantly decrease
our revenue.
In particular, if the security of domain names is compromised, we will be unable to use
the domain names in our business operations, which could materially and adversely affect our
business operations, reputation and brand image. If we fail to implement adequate encryption
of data transmitted through the networks of the telecommunications and Internet operators we
rely upon, there is a risk that telecommunications and Internet operators or their business
partners may misappropriate our data, which could materially and adversely affect our business
operations and reputation.
We depend on cloud services and infrastructure operated by third parties and any
disruption of or interference with our use of such third-party services and infrastructure
would adversely affect our business, results of operations and financial conditions.
We provide our foundation model products through a number of third-party cloud services
and infrastructure providers. Our third-party cloud services and infrastructure providers may
experience problems, including but not limited to, software and hardware breakdowns, power
shortages or natural disasters, which may expose us to the risks of interruptions, delays or
outages with respect to our third-party cloud services and infrastructure. The level of cloud
services and infrastructure provided by these third-party providers, or regular or prolonged
interruptions in that particular cloud services or infrastructure, could affect the use of, and our
users’ satisfaction with, our products and could harm our reputation.
Furthermore, in some circumstances, our cloud service and infrastructure providers may
discontinue or restrict our access to one or more services or terminate or seek to terminate
contractual relationship with us. If our contractual relationship with our current third-party
providers were terminated, we could experience temporary interruptions in our ability to
provide services to our users and may incur additional costs in searching for alternative cloud
services and infrastructure providers.
As a result of the above, we may experience temporary disruptions to our operation
leading to the dissatisfaction of our users, incur additional costs or be subject to actual or
potential liability, any of which could have an adverse impact on our business, results of
operations and financial conditions.
RISK FACTORS
– 96 –

<<<PAGE 107>>>
Disruptions and unauthorized access such as cyberattacks on our IT systems or those of
third-party service providers could have a material adverse effect on our business
operations, results of operations, reputation and financial condition.
Our products and technologies may provide us with access to data or information, which
pose a tempting target for malicious actors who may seek to carry out cyberattacks against us
or our suppliers or service providers. Actual or perceived breaches of our or our service
providers’ security measures or any failure to maintain reliability, security and integrity of our
products and technical platform, including third-party cloud platform and information
technology, or IT, services upon which we rely, may expose us to significant consequences. We
can provide no assurance that our IT systems or those of third-party service providers are fully
protected against third-party intrusions, viruses, hacker attacks, ransomware attacks and other
cyberattacks, information or data theft or other similar threats. Additionally, software
authorized or licensed by third parties which is incorporated into our products and technologies
may present certain risks related to cybersecurity, such as the general lack of support for such
software which could result in vulnerabilities that could compromise the security of our
systems. See “— We make certain of our models and products available on an open-source
basis and may use open-source technology, which may pose particular risks to our business”
for further details describing the risks associated with our use of open-source software.
Therefore, our systems, servers and equipment, and those of our service providers, may
be subject to such incidents, which may lead to damages to our IT systems, material disruption
to our business, or theft, rendering inaccessible, improper disclosure or misappropriation of our
or our users’ business information, trade secrets, user data and other confidential or proprietary
information. Any such event could have a material adverse effect on our business even if we
recover using our backup information. Consequences may include legal and financial exposure,
loss of business and users, loss or unauthorized disclosure of trade secrets or other proprietary
information or personal information, and could give rise to litigation (including class-action
litigation and litigation and indemnity claims against us by our users based on our customer
agreements and other commercial arrangements), regulatory actions and fines, consumer
protection actions, other related costs (including in connection with our investigation and
remediation efforts) and significant harm to our reputation. This may hinder our ability to
retain existing users and business partners and attract new partners and users. To the extent we
experience a cyberattack or security breach, we may be unsuccessful in implementing
remediation plans to address exposure and future harm. Also, we do not maintain insurance
coverage relating to cybersecurity incidents, and so any expenses or costs incurred as a result
of, or related to, any cyberattacks or security breaches, which could be significant, would be
at our own expense. Any such actual or perceived disruptions, access, breaches, uncertainties
or events could materially and adversely affect our business operations, results of operations,
and financial condition.
RISK FACTORS
– 97 –

<<<PAGE 22>>>
CUSTOMERS AND SUPPLIERS
Our customers comprise a broad and diverse base across various sectors and geographies.
In 2023, 2024 and nine months ended September 30, 2025, revenue from our five largest
customers in each year/period during the Track Record Period amounted to US$2.1 million,
US$13.4 million and US$11.6 million, representing 60.5%, 44.1% and 21.7% of our total
revenue for the respective periods. In 2023, 2024 and nine months ended September 30, 2025,
revenue derived from our largest customer in each year/period during the Track Record Period
amounted to US$1.3 million, US$9.4 million and US$7.8 million, representing 37.2%, 30.9%
and 14.7% of our total revenue for the respective periods.
We maintain stable and long-standing relationships with a select group of suppliers,
principally in the areas of cloud infrastructure services. In 2022, 2023, 2024 and the nine
months ended September 30, 2025, purchases from our five largest suppliers in each
year/period during the Track Record Period amounted to US$4.5 million, US$49.8 million,
US$149.0 million and US$143.6 million, representing 63.9%, 63.0%, 57.3% and 62.5% of our
total purchases for the respective periods. In 2022, 2023, 2024 and the nine months ended
September 30, 2025, purchases derived from our largest supplier in each year/period during the
Track Record Period amounted to US$1.6 million, US$23.0 million, US$72.8 million and
US$54.9 million, representing 22.8%, 29.1%, 28.0% and 23.9% of our total purchases for the
respective periods. See “Business — Ecosystem of Partners.”
LEGAL PROCEEDINGS
On September 16, 2025, a group of major U.S. movie studio companies, including Disney,
Universal and Warner Bros. Discovery (the “Plaintiffs”), filed a civil complaint (the
“Complaint”) in the United States District Court for the Central District of California, against
our Group in relation to Hailuo AI, our visual generation platform. The Plaintiffs allege (i)
direct infringement, on the basis that the Company itself, through Hailuo AI, created and
displayed videos and images depicting a number of well-known film and animation characters
owned by the Plaintiffs, and (ii) secondary infringement, including contributory and vicarious
infringement, on the basis that the Company knew or should have known that users could
create content depicting the Plaintiffs’ characters, and because the Company is allegedly
benefiting from that use. In their prayer for relief, the Plaintiffs primarily seek, among other
things, monetary relief in the form of actual or statutory damages, injunctive relief, attorneys’
fees and other equitable remedies.
These claims are commercial disputes in nature, and having considered advice from our
U.S. litigation advisor, our Directors believe, that they are without merit in all material respects
and that there is insufficient evidence to support them. Based on the Joint Sponsors’ due
diligence conducted, there was no reasonable basis for the Joint Sponsors to disagree with the
Directors’ view that the claims are without merits in all material respects. The Company
categorically denies the allegations of direct infringement, as Hailuo AI only produces outputs
in response to user prompts and therefore lacks the volitional conduct required for direct
liability. In respect of the secondary infringement claims, Hailuo AI is a general-purpose
SUMMARY
– 12 –

<<<PAGE 23>>>
creative tool created for lawful uses, and the Company does not have any direct financial
benefit tied to alleged infringements, such that the elements required for contributory or
vicarious liability are not satisfied.
The Plaintiffs have alleged in their Complaint that they are entitled to statutory damages
of up to US$150,000 per infringed work, which is the maximum amount awardable per work
under U.S. copyright law and is only awarded if infringement is found to be willful. The
attachments to the Complaint identify approximately 500 registrations for motion pictures and
television programs that are at issue in this case. Therefore, assuming the plaintiffs prevail and
fully succeed in their claims, the worst-case scenario, as alleged by the plaintiffs, would be a
monetary claim of US$75 million in statutory damages, calculated by multiplying the number
of alleged works by the alleged maximum statutory damages amount, and injunctive relief. The
overwhelming majority of Hailuo AI outputs user-created content have nothing to do with the
Plaintiffs’ characters. Having considered advice from our U.S. litigation advisor, our Directors
consider the likelihood of the Plaintiffs fully succeeding on both liability and maximum
statutory damages to be extremely remote. While the Plaintiffs claim each of the 500
registrations they have identified is eligible to be counted as a “work”, having considered
advice from our U.S. litigation advisor, our Directors are of the view that the number of
“works” properly eligible for statutory calculation is likely to be significantly lower than the
approximately 500 registrations referenced in the Complaint, as U.S. law does not assess
statutory damages on a per-registration basis, and many of the alleged characters appear
repeatedly across multiple registrations without new protectable expression; therefore, they
would not be considered unique “works”. Having further considered advice from our U.S.
litigation advisor, our Directors are of the view that statutory damages of US$150,000 per work
are rarely awarded absent willful and repeated infringement — a standard that the Directors
believe is not supported by the facts — and that statistical studies indicate such maximum
awards occur only in exceptional, deliberate-infringement scenarios. Based on the independent
due diligence steps performed by the Joint Sponsors, including interviewing and discussing
with the Company’s U.S. litigation advisor, the Joint Sponsors have reasonable grounds to
believe that the view of the Directors expressed above fairly represents the views of the
Company’s U.S. litigation advisor.
Based on the above, having considered advice from our U.S. litigation advisor, the
Directors are of the view that the claims will not have a material adverse effect on our business,
results of operations or financial condition because (i) even in the extremely remote scenario
where the Plaintiffs prevail in full and obtain the maximum statutory damages claimed, the
maximum alleged damages of approximately US$75 million would represent only around 4.9%
of our available financial resources (including cash and cash equivalents, current portion of our
available financial assets and expected IPO proceeds), and this proportion is expected to
decline over time given the typically protracted nature of U.S. civil litigation and the
Company’s expected continued growth; (ii) the likelihood of an injunction materially
disrupting our business is low, as preliminary injunctions require a strong showing of factors
including likelihood of success on the merits, irreparable harm absent an injunction and
urgency, none of which have been substantiated, and courts in comparable technology cases
generally favor narrow output-specific remedies rather than broad platform-wide restrictions,
SUMMARY
– 13 –

<<<PAGE 24>>>
making any such operational impact unlikely even in a final judgment; and (iii) the Plaintiffs’
intellectual property is not material to the commercial viability of Hailuo AI, which is a
general-purpose creative platform created for lawful uses, and the Directors do not consider
such intellectual property to be a meaningful driver of user engagement, revenue generation or
growth, such that exclusion of such content would not be expected to affect our business,
financial performance or prospects in a material manner. Based on the independent due
diligence steps performed by the Joint Sponsors, including, among other things, (a) discussing
with the Company’s U.S. litigation advisor regarding the potential worst-case scenario, the
possibility of granting the injunctive relief and their legal analysis in this regard, (b) reviewing
of the Group’s financial information, and (c) examination of the MAU data of Hailuo AI from
June to November 2025 and the system-check results of Hailuo AI’s outputs, the Joint Sponsors
concur with the Directors’ view above. For details, see “Business — Legal Proceedings and
Compliance — Copyright Infringement Lawsuit,” Risk Factors — Risks Related to Our
Business and Industry — The content or data that we use to train our foundation models and
the content generated by our foundation models could be subject to third-party intellectual
property infringement claims which may materially and adversely affect our business, financial
condition and results of operations” and “Risk Factors — Risks Related to Our Business and
Industry — We may become subject to litigation brought by third parties claiming infringement
by us of their intellectual property rights.”
OUR MARKET OPPORTUNITIES AND COMPETITION
The global model-based foundation model market is still in the early stages of
commercialization. As technologies continue to mature and the willingness of users to pay
steadily increases, the global model-based foundation model market is expected to grow
rapidly from US$10.7 billion in 2024 to US$206.5 billion by 2029, representing a CAGR of
80.7%.
We differentiate ourselves through our technical focus on long-context modeling and
scalable multi-modal architecture design, which allow us to build models capable of handling
complex, multi-dimensional interactions across text, visual and audio. We are the tenth largest
foundation model company globally, with a market share of 0.3%. Additionally, we are the
fourth largest pureplay foundation model company globally in terms of model-based revenues
in 2024.
See “Industry Overview” for details.
SUMMARY
– 14 –

<<<PAGE 25>>>
RISK FACTORS
We are a Specialist Technology Company seeking Listing on the Main Board of the Stock
Exchange under Chapter 18C of the Listing Rules. Our business and the Global Offering
involve certain risks as set out in “Risk Factors” in this document. You should read that section
in its entirety carefully before you decide to invest in our Shares. We believe the most
significant risks we face include but are not limited to the following:
•
We have recorded net losses, net liabilities and operating cash outflow during the
Track Record Period and recorded net current liabilities as of September 30, 2025,
and we may not be able to achieve or subsequently maintain profitability.
•
We operate in a rapidly evolving and increasingly competitive global foundation
model industry. Our business is subject to constant technological advancements and
industry transformation. If we fail to continuously innovate and adapt to evolving
customer needs, our competitive position would be impacted and our business,
financial condition and results of operations may be materially and adversely
affected.
•
The content or data that we use to train our foundation models and the content
generated by our foundation models could be subject to third-party intellectual
property infringement claims which may materially and adversely affect our
business, financial condition and results of operations.
•
Any actual or perceived flaws or inappropriate usage of foundation model
technologies committed by us or other third parties intentionally or inadvertently,
could materially and adversely impact our reputation, business, financial condition,
results of operations and the broader acceptance of foundation model products by
society at-large.
•
The competitiveness of our foundation models and offerings depends on our
continuous and significant investment in research and development, and we intend
to continue investing significantly in research and development. Such investment
may negatively impact our profitability and operating cash flow in the short term
and may not generate the results we expect to achieve.
See “Risk Factors” for details.
INTELLECTUAL PROPERTY RIGHTS
Intellectual property lies at the heart of our research, product development and
commercial success. We safeguard our proprietary technologies through a layered strategy that
combines (i) statutory protection under patent, copyright, trademark, trade-secret and
unfair-competition laws in the PRC and other jurisdictions, and (ii) contractual safeguards such
as confidentiality undertakings, invention-assignment covenants and license agreements. All
SUMMARY
– 15 –

<<<PAGE 26>>>
employment and key commercial contracts expressly delineate ownership of, and obligations
to protect, intellectual property created or used in the course of our business. During the Track
Record Period, our core technologies were patented. Such patents are typically valid for 10 to
20 years.
As of the Latest Practicable Date, we had 75 patents registered with the National
Intellectual Property Administration of the PRC, 144 trademarks registered in the PRC, 73
copyrights registered with the National Copyright Administration of the PRC, 28 registered
strategic domain names in the PRC and 87 trademarks registered internationally. See
“Appendix IV — Statutory and General Information — B. Further Information about our
Business — 2. Intellectual Property Rights of our Group” for a schedule of material intellectual
property rights.
During the Track Record Period and up to the Latest Practicable Date, we were not
involved in any IP litigation, arbitration or administrative proceedings, nor have we received
any claim alleging infringement of third-party rights that would have a material adverse effect
on our business, results of operations, or financial condition. We will continue to monitor the
landscape and, where necessary, defend or enforce our rights vigorously.
Notwithstanding the foregoing measures, we cannot rule out the possibility of future
challenges to our IP or allegations of infringement against us. Enforcement actions may involve
significant cost and management distraction. For a discussion of these and other related risks,
please refer to “Risk Factors — We may not be able to adequately protect or enforce our
intellectual property rights throughout the world, and our efforts to do so may be costly” and
“Risk Factors — We may become subject to litigation brought by third parties claiming
infringement by us of their intellectual property rights.” See “Business — Intellectual
Property.”
WEIGHTED VOTING RIGHTS STRUCTURE
Our Company has a weighted voting rights structure. The Company satisfies the
presumption for the “Innovative Company Requirements” and the “external validation”
requirements under Chapter 2.2 of the Guide for New Listing Applicants published by the
Stock Exchange pursuant to the Joint Announcement on Launch of Technology Enterprises
Channel published on 6 May 2025 as it meets all relevant requirements under Chapter 18C of
the Rules and Chapter 2.5 of the Guide for New Listing Applicants. Under our weighted voting
rights structure, our share capital comprises Class A Ordinary Shares and Class B Ordinary
Shares. Each Class B Ordinary Share entitles the holder to exercise ten votes, and each Class
A Ordinary Share entitles the holder to exercise one vote, respectively, on any matters subject
to the vote at general meetings of the Company, subject to Rule 8A.24 of the Listing Rules that
requires the Reserved Matters to be voted on a one vote per share basis.
SUMMARY
– 16 –

<<<PAGE 27>>>
The table below sets out the beneficial interests entitled to and voting rights to be held
by the WVR Beneficiaries upon the completion of the Global Offering (assuming the Offer
Size Adjustment Option and the Over-allotment Option are not exercised):
Number of
Class B
Ordinary Shares
held
Number of Class
A Ordinary
Shares interested
in(3)
Approximate
percentage of
beneficial
interests
in the issued
share capital
Approximate
percentage of
voting rights
controlled(1)
Dr. Yan(2)   
74,102,534
3,355,030
25.36%
72.05%
Ms. Yun(2)   
7,000,000
1,644,970
2.83%
6.76%
Notes:
(1)
On the basis that each Class A Ordinary Share entitles the Shareholder to one vote per Share and each
Class B Ordinary Share entitles the Shareholder to ten votes per Share.
(2)
For details of the shareholding structure of our WVR Beneficiaries, please refer to the section headed
“History, Reorganization and Corporate Structure.”
(3)
Dr. Yan and Ms. Yun are interested in MiniMax Matrix as to 67.1% and 32.9%.
Our Company is adopting the WVR structure to enable the WVR Beneficiaries to exercise
voting control over our Company. This will enable our Company to benefit from the continuing
vision and leadership of the WVR Beneficiaries who will control our Company with a view to
its long-term prospects and strategy. Taking into account the WVR Beneficiaries’ contribution
to the Group, such arrangement is in the best interests of the Company and its Shareholders as
a whole.
Prospective investors are advised to be aware of the potential risks of investing in
companies with weighted voting rights structures, in particular that interests of the WVR
Beneficiaries may not necessarily always be aligned with those of our Shareholders as a whole,
and that the WVR Beneficiaries will be in a position to exercise their higher voting power to
influence the affairs of our Company and the outcome of Shareholders’ resolutions,
irrespective of how other Shareholders vote.
Prospective investors should make the decision to invest in the Company only after due
and careful consideration. For further information about the risks associated with the WVR
structure adopted by the Company, see “Risk Factors — Risks Related to the WVR Structure.”
Save for the weighted voting rights attached to Class B Ordinary Shares, the rights attached to
both classes of Shares are identical. For further information about the rights, preferences,
privileges and restrictions of the Class A Ordinary Shares and Class B Ordinary Shares, please
see “Summary of the Constitution of our Company and Cayman Islands Company Law — 2
Articles of Association” in Appendix III to this Prospectus for further details.
SUMMARY
– 17 –

<<<PAGE 303>>>
We actively collaborate with prominent partners for co-development of advanced AI solutions
and the establishment of shared technical standards. We also maintain strategic relationships to
foster innovation, interoperability, and responsible AI governance.
Our Customers
Our customers comprise a broad and diverse base across various sectors and geographies
including the PRC, the United States, and Singapore. Our customers span key industries such
as finance, healthcare, smart devices and education. Our sales and marketing team,
predominantly from technology and cloud computing backgrounds, ensures effective client
engagement and retention. Our customers primarily consist of: (i) enterprises, including those
operating in the smart devices, cultural tourism, healthcare, finance, and internet services
sectors, which utilize our AI models and solutions via API and SDK integrations; (ii)
developers, who access and build upon our open platform to create and deploy their own
AI-powered products; and (iii) individual end-users, primarily through our AI-native products.
Customer acquisition strategies are diversified, incorporating direct sales outreach,
partnerships with cloud service providers, developer community engagements, promotional
activities, and targeted marketing initiatives.
We had no customers and generated no revenue in 2022. In 2023, 2024 and nine months
ended September 30, 2025, revenue from our five largest customers in each year/period during
the Track Record Period amounted to US$2.1 million, US$13.4 million and US$11.6 million,
representing 60.5%, 44.1% and 21.7% of our total revenue for the respective periods. In 2023,
2024 and nine months ended September 30, 2025, revenue derived from our largest customer
in each year/period during the Track Record Period amounted to US$1.3 million, US$9.4
million and US$7.8 million, representing 37.2%, 30.9% and 14.7% of our total revenue for the
respective periods.
We typically enter into framework agreements with major customers, and the salient
terms of which are set forth below:
•
Duration and Subscription: Customers may subscribe to one or more services as set
out in their orders, subject to the actual services provided. Prior to purchase,
customers are required to review the applicable service terms and determine
suitability based on their needs;
•
Payment Terms: Customers are required to make timely payments for ordered
services, which may be subject to availability or promotional limits. Charges may
continue to accrue after service activation due to ongoing resource usage, regardless
of further customer activity. Preferential pricing is conditional and may not apply if
relevant criteria are not met, in which case standard rates shall apply;
BUSINESS
– 293 –

<<<PAGE 304>>>
•
Duration: We typically do not assign a set duration to our framework agreement
with our customers. Our framework agreement shall remain effective unless
terminated by either party or by operation of law;
•
Privacy and Data Protection: Our customers are responsible for ensuring that all
data submitted to or processed through our platform is lawfully collected and
processed in full compliance with applicable data protection laws and regulations.
They are required to obtain all necessary consents from data subjects and bear
responsibility for any non-compliance. We are authorized to access and process
customer data solely for the purpose of providing and improving our services;
•
Intellectual Properties: We retain all intellectual property rights in our products.
Use of our services does not constitute any transfer or licence of our intellectual
property or branding. Our customers are responsible for ensuring that all content
they upload or process does not infringe any third-party rights and shall indemnify
us for any resulting claims. Unauthorized use, reproduction, reverse engineering or
disclosure of our technology or materials is strictly prohibited;
•
Confidentiality: Customers are required to keep our confidential information strictly
confidential and use it only for purposes permitted under the agreement. Disclosure
is
only
allowed
where
required
by
applicable
laws
or
regulations.
These
confidentiality obligations shall survive the termination of the agreement;
•
Termination: We may suspend or terminate services with immediate effect if the
customer breaches its obligations, becomes subject to sanctions or insolvency, or if
continued performance would breach applicable laws. Upon termination, the
customer must settle all outstanding fees and cease use of our services.
During the Track Record Period and up to the Latest Practicable Date, all of our five
largest customers in each period during the Track Record Period were independent third
parties. During the Track Record Period and as of the Latest Practicable Date, none of our
Directors, their associates or any of our Shareholders (who or which to the knowledge of the
Directors owned more than 5% of our issued share capital) had any interest in any of our five
largest customers in each period during the Track Record Period.
BUSINESS
– 294 –

<<<PAGE 305>>>
The following tables set forth details about our five largest customers in each period
during the Track Record Period:
Rank
Customers
Type of
Products
Purchased
Background
Approximate
Years of
Business
Relationship
Credit Terms
Revenue
% of Our
Total
Revenue
(US$ in
millions)
%
For the year ended December 31, 2023
1     Customer A
Open
Platform
A comprehensive cultural industry
group headquartered in Shanghai,
China, with digital reading as its
foundation and IP cultivation and
development at its core.
since 2023
Net 15 days
1.3
37.2
2     Customer B
Open
Platform
An office productivity software
developer, which provides cross-
platform solutions for word
processing, spreadsheets, and
presentations.
since 2023
Net 45 days
0.4
12.3
3     Customer C
Open
Platform
A social e-commerce platform that
integrates lifestyle sharing, product
reviews, and online shopping.
since 2023
Net 45 days
0.2
6.2
4     Customer D
Open
Platform
An online recruitment platform
operator, providing comprehensive
HR solutions and job-matching
services.
since 2023
Net 44 days
0.1
2.7
5     Customer E
Open
Platform
A digital content innovation company
specializing in IP development and
digital reading solutions, integrating
technology with cultural creativity to
deliver immersive reading
experiences.
since 2023
Net 20 days
0.1
2.1
For the year ended December 31, 2024
1     Customer F
(Supplier K)
Talkie
A technology company based in
Singapore, providing digital
advertising, cloud service, and online
service solutions.
since 2024
Net 30 days
9.4
30.9
2     Customer A
Open
Platform
A comprehensive cultural industry
group headquartered in Shanghai,
China, with digital reading as its
foundation and IP cultivation and
development at its core.
since 2023
Net 30 days
1.1
3.7
BUSINESS
– 295 –

<<<PAGE 306>>>
Rank
Customers
Type of
Products
Purchased
Background
Approximate
Years of
Business
Relationship
Credit Terms
Revenue
% of Our
Total
Revenue
(US$ in
millions)
%
3     Customer B
Open
Platform
An office productivity software
developer, which provides cross-
platform solutions for word
processing, spreadsheets, and
presentations.
since 2023
Net 45 days
1.0
3.4
4     Customer C
Open
Platform
A social e-commerce platform that
integrates lifestyle sharing, product
reviews, and online shopping.
since 2023
Net 45 days
1.0
3.2
5     Customer G
(Supplier I)
Talkie
An entity incorporated in Singapore,
engaged in digital marketing and
mobile app monetization services.
since 2024
Net 30 days
0.9
2.9
For the nine months ended September 30, 2025
1     Customer F
(Supplier K)
Talkie
A technology company based in
Singapore, providing digital
advertising, cloud service, and online
service solutions.
since 2024
Net 30 days
7.8
14.7
2     Customer H
Open
Platform
and other
AI-based
enterprise
services
An AI-powered digital human and
video synthesis platform that enables
hyper-realistic avatar creation and
multilingual video generation for
global enterprises.
since 2025
Net 45 days
1.2
2.2
3     Customer I
Open
Platform
and other
AI-based
enterprise
service
A developer centric platform that
provides infrastructure and APIs for
generative AI media (images, audio,
video) and high speed model
inference.
since 2024
Net 14 days
1.0
1.8
4     Customer J
Open
Platform
and other
AI-based
enterprise
service
A Chinese AI and big data company
specializing in intelligent customer
service solutions and conversational
AI platforms for enterprises.
since 2024
Net 30 days
0.9
1.6
5     Customer K
Talkie
A mobile technology company that
provides end-to-end app distribution
and monetization solutions for
carriers, OEMs, and advertisers
worldwide.
since 2024
Net 60 days
0.7
1.4
BUSINESS
– 296 –

<<<PAGE 307>>>
Our Suppliers
We maintain stable and long-standing relationships with a select group of suppliers,
principally in the areas of cloud infrastructure services. Our procurement strategy emphasizes
supplier diversification, competitive bidding, and the establishment of stable, long-term
contractual arrangements, thereby ensuring business continuity and the quality of our technical
infrastructure. Our procurement team, consisting of specialists, is responsible for supplier
identification, negotiation, and performance monitoring. Typical purchasing terms include
clearly defined service level agreements (SLAs), penalty clauses for non-compliance, and
standardized post-delivery payment schedules, generally ranging from 30 to 90 days following
invoice issuance.
We operate under a light-asset business model, whereby critical computing infrastructure
assets are owned and maintained by our suppliers, who provide computing services in
accordance with our customized technical specifications. We conduct stringent quality
inspections and acceptance checks on all goods and services received to ensure full compliance
with our contractual requirements.
Our suppliers are primarily major technology service providers and cloud infrastructure
vendors. We regularly review our supplier network to assess service reliability, cost
competitiveness, and alignment with our evolving business needs.
In 2022, 2023, 2024 and the nine months ended September 30, 2025, purchases from our
five largest suppliers in each year/period during the Track Record Period amounted to US$4.5
million, US$49.8 million, US$149.0 million and US$143.6 million, representing 63.9%,
63.0%, 57.3% and 62.5% of our total purchases for the respective periods. In 2022, 2023, 2024
and the nine months ended September 30, 2025, purchases derived from our largest supplier in
each year/period during the Track Record Period amounted to US$1.6 million, US$23.0
million, US$72.8 million and US$54.9 million, representing 22.8%, 29.1%, 28.0% and 23.9%
of our total purchases for the respective periods.
As of the Latest Practicable Date, all of our five largest suppliers in each period during
the Track Record Period were independent third parties, except that Supplier J comprises five
subsidiaries of Alisoft China Holding Limited, which is a substantial shareholder of our
company. During the Track Record Period and as of the Latest Practicable Date, none of our
Directors, their associates or any of our Shareholders (who or which to the knowledge of the
Directors owned more than 5% of our issued share capital) had any interest in any of our five
largest suppliers in each period during the Track Record Period except Supplier J.
BUSINESS
– 297 –

<<<PAGE 308>>>
The following tables set forth details about our five largest suppliers in each period during
the Track Record Period:
Rank
Suppliers
Type of
Products/Services
Provided
Background
Approximate
Years of
Business
Relationship
Credit
Terms
Purchase
Amount
% of Our
Total
Purchase
(US$ in
millions)
%
For the year ended December 31, 2022
1    Supplier A
Cloud service
A cloud service provider registered in
Beijing, China, primarily engaged in
infrastructure and platform cloud
services.
since 2022
Net 90
days
1.6
22.8
2    Supplier B
Cloud service
An enterprise cloud solutions
provider based in Beijing, China,
delivering cloud services.
since 2022
Net 90
days
1.3
19.1
3    Supplier C
Cloud service
A technology company incorporated
in Beijing, China, specializing in
cloud computing, artificial
intelligence, and data analytics
services.
since 2022
Net 30
days
1.2
17.1
4    Supplier D
Outsourcing
service
An IT services company
headquartered in Shenzhen, China,
providing software development,
outsourced research and
development, and system integration
services.
since 2022
Net 30
days
0.2
2.6
5    Supplier E
Technical service
– data processing
A regional technology company
registered in Shanxi Province, China,
engaged in local IT services and
solutions.
since 2022
Net 30
days
0.2
2.3
For the year ended December 31, 2023
1    Supplier C
Cloud service
A technology company incorporated
in Beijing, China, specializing in
cloud computing, artificial
intelligence, and data analytics
services.
since 2022
Net 30
days
23.0
29.1
2    Supplier A
Cloud service
A cloud service provider registered in
Beijing, China, primarily engaged in
infrastructure and platform cloud
services.
since 2022
Net 90
days
12.2
15.5
BUSINESS
– 298 –

<<<PAGE 569>>>
(b)
Non-current assets
As at 31 December
As at
30 September
2022
2023
2024
2025
USD’000
USD’000
USD’000
USD’000
Mainland China             
689
4,022
4,170
3,880
Total non-current assets        
689
4,022
4,170
3,880
The non-current asset information above is based on the locations of the assets and include Property, plant and
equipment and Right-of-use assets.
Information about major customers
Revenues from customers, including a group of entities which are known to be under common control, which
individually accounted for over 10% of the Group’s total revenue during the year ended 31 December 2022,2023 and
2024 and the nine months ended 30 September 2024 and 2025 are as follows:
Year ended 31 December
Nine months ended 30 September
2022
2023
2024
2024
2025
USD’000
USD’000
USD’000
USD’000
USD’000
(unaudited)
Customer A          
N/A
1,286
N/A
N/A
N/A
Customer B          
N/A
426
N/A
N/A
N/A
Customer C          
N/A
N/A
9,438
6,504
7,828
5.
REVENUE, OTHER INCOME AND GAINS
An analysis of revenue from contracts with customers is as follows:
(a)
Disaggregation of revenue from contracts with customers
Revenue during the year ended 31 December 2022, 2023 and 2024 and the nine months ended 30 September
2024 and 2025 is as follows:
Year ended 31 December
Nine months ended 30 September
2022
2023
2024
2024
2025
USD’000
USD’000
USD’000
USD’000
USD’000
(unaudited)
AI-native products     
–
758
21,805
13,529
38,020
Open Platform and other
AI-based enterprise
services           
–
2,702
8,718
5,925
15,417
Revenue from services
provided          
–
3,460
30,523
19,454
53,437
APPENDIX I
ACCOUNTANT’S REPORT
– I-32 –

<<<PAGE 570>>>
Year ended 31 December
Nine months ended 30 September
2022
2023
2024
2024
2025
USD’000
USD’000
USD’000
USD’000
USD’000
(unaudited)
Timing of revenue
recognition
Services transferred at a
point in time       
–
2,702
25,695
15,825
30,322
Services transferred over
time             
–
758
4,828
3,629
23,115
Total              
–
3,460
30,523
19,454
53,437
(b)
Performance obligations
Information about the Group’s performance obligations is described in note 2.4 to the consolidated financial
statement Under “Revenue recognition”. The Group also obtained advance payment from the Membership
subscription and the Virtual items.
The Company elected to use the practical expedient to not disclose the remaining performance obligations, as
substantially all of the Company’s contracts have duration of one year or less.
(c)
Revenue recognised in relation to contract liabilities
The amounts of revenue recognised during the years ended 31 December 2022, 2023 and 2024 and the nine
months ended 30 September 2024 and 2025 that were included in the contract liabilities at the beginning of those
periods were nil, nil, USD559,000, USD487,000 (unaudited) and USD1,358,000, respectively.
The amounts of transaction prices allocated to the remaining performance obligations (unsatisfied or partially
unsatisfied) as at the end of each of the Relevant Periods were nil, USD559,000, USD1,553,000 and USD4,657,000.
The revenue attributable to these remaining performance obligations is expected to be recognised within one year.
Other income and gains, net
An analysis of other income and gains is as follows:
Year ended 31 December
Nine months ended 30 September
2022
2023
2024
2024
2025
USD’000
USD’000
USD’000
USD’000
USD’000
(unaudited)
Interest income   
39
7,785
20,448
17,199
7,876
Foreign exchange
gains, net     
175
311
2
1,415
1,600
Fair value gain on
financial assets at
fair value through
profit or loss   
941
788
15,710
6,682
20,414
Others         
–
58
(9)
(18)
1,342
Total          
1,155
8,942
36,151
25,278
31,232
APPENDIX I
ACCOUNTANT’S REPORT
– I-33 –

<<<PAGE 571>>>
6.
FINANCE COSTS
An analysis of finance costs is as follows:
Year ended 31 December
Nine months ended 30 September
2022
2023
2024
2024
2025
USD’000
USD’000
USD’000
USD’000
USD’000
(unaudited)
Interest on interest-bearing
bank borrowings     
–
–
355
199
404
Interest on lease liabilities
14
61
154
117
107
Total              
14
61
509
316
511
7.
LOSS BEFORE TAX
The Group’s loss before tax is arrived at after charging/(crediting):
Year ended 31 December
Nine months ended 30 September
2022
2023
2024
2024
2025
USD’000
USD’000
USD’000
USD’000
USD’000
(unaudited)
Cost of services provided
(excluding employment
benefit)           
–
4,314
26,785
18,944
40,348
Depreciation of property,
plant and equipment   
25
180
451
325
582
Depreciation of right-of-
use assets         
182
631
1,450
1,072
1,478
Listing expenses       
–
–
–
–
3,675
Research and development
costs (excluding
employee benefit
expenses, depreciation
and amortisation costs) 
5,011
49,465
143,807
105,410
145,434
Employee benefit
expenses:
Wages and salaries    
5,676
19,762
44,036
30,676
38,851
Pension scheme
contributions      
188
1,106
2,402
1,803
2,009
Share-based payment
expenses         
106
2,068
4,548
4,442
7,338
Fair value loss on financial
liabilities          
60,509
176,826
214,172
128,063
313,477
Impairment losses on
financial assets, net   
–
3
88
68
22
Fair value gains on
financial assets at fair
value through profit or
loss             
(941)
(788)
(15,710)
(6,682)
(20,414)
APPENDIX I
ACCOUNTANT’S REPORT
– I-34 –

<<<PAGE 572>>>
8.
DIRECTORS’ AND CHIEF EXECUTIVE’S REMUNERATION
Directors’ and chief executive’s remuneration for the year/period, disclosed pursuant to the Listing Rules,
section 383(1)(a), (b), (c) and (f) of the Hong Kong Companies Ordinance and Part 2 of the Companies (Disclosure
of Information about Benefits of Directors) Regulation, is as follows:
Year ended 31 December
Nine months ended 30 September
2022
2023
2024
2024
2025
USD’000
USD’000
USD’000
USD’000
USD’000
(unaudited)
Salaries, allowances and
benefits in kind      
358
625
1,144
832
1,011
Performance related
bonuses           
131
247
170
–
–
Pension scheme
contributions       
9
24
39
31
23
Equity-settled share option
expense           
963
1,278
2,275
1,658
1,243
Total              
1,461
2,174
3,628
2,521
2,277
During the year ended 31 December 2022,2023 and 2024 and the nine months ended 30 September 2024 and
2025, certain directors were granted share options, in respect of their services to the Group, under the share option
scheme of the Company, further details of which are set out in note 26 to the Historical Financial Information. The
fair value of such options, which has been recognised in the statement of profit or loss over the vesting period, was
determined as at the date of grant and the amount included in the financial statements for the current year is included
in the above directors’ and chief executive’s remuneration disclosures.
(a)
Independent non-executive directors
During the Relevant Periods, Mr. Huang Guobin, Mr. Wang Pengcheng and Mr. Zhu Huaxing were appointed
as independent non-executive directors of the Company from listing Date.
There was no emolument payable to the independent non-executive directors during the year ended 31
December 2022,2023 and 2024 and the nine months ended 30 September 2024 and 2025.
(b)
Executive directors, a non-executive director and the chief executive
Salaries,
allowances and
benefits in kind
Performance
related bonuses
Pension scheme
contributions
Equity-settled
share option
expense
Total
remuneration
USD’000
USD’000
USD’000
USD’000
USD’000
2022
Executive directors:
Ms. Yun Yeyi (i)     
94
80
4
963
1,141
Mr. Yang Bin (ii)     
180
51
2
–
233
Ms. Wang Meng (iii)  
84
–
3
–
87
Total              
358
131
9
963
1,461
APPENDIX I
ACCOUNTANT’S REPORT
– I-35 –

<<<PAGE 573>>>
Salaries,
allowances and
benefits in kind
Performance
related bonuses
Pension scheme
contributions
Equity-settled
share option
expense
Total
remuneration
USD’000
USD’000
USD’000
USD’000
USD’000
2023
Executive directors:
Ms. Yun Yeyi (i)     
179
94
7
1,278
1,558
Mr. Yang Bin (ii)     
216
43
7
–
266
Mr. Zhang Mozhi (iv)  
159
55
7
–
221
Mr. Yan Junjie (v)    
71
55
3
–
129
Total              
625
247
24
1,278
2,174
Salaries,
allowances and
benefits in kind
Performance
related bonuses
Pension scheme
contributions
Equity-settled
share option
expense
Total
remuneration
USD’000
USD’000
USD’000
USD’000
USD’000
2024
Executive directors:
Ms. Yun Yeyi (i)     
267
86
7
1,282
1,642
Mr. Wei Wei (vi)     
212
–
7
736
955
Mr. Zhang
Qianchuan (vii)    
123
–
4
257
384
Mr. Yan Junjie (v)    
173
42
7
–
222
Mr. Zhang Mozhi (iv)  
168
42
7
–
217
Mr. Yang Bin (ii)     
201
–
7
–
208
Total              
1,144
170
39
2,275
3,628
Salaries,
allowances and
benefits in kind
Performance
related bonuses
Pension scheme
contributions
Equity-settled
share option
expense
Total
remuneration
USD’000
USD’000
USD’000
USD’000
USD’000
30 September 2024
(unaudited)
Executive directors:
Ms. Yun Yeyi (i)     
126
–
5
960
1,091
Mr. Wei Wei (vi)     
159
–
5
441
605
Mr. Zhang
Qianchuan (vii)    
123
–
4
257
384
Mr. Yang Bin (ii)     
166
–
6
–
172
Mr. Yan Junjie (v)    
130
–
5
–
135
Mr. Zhang Mozhi (iv)  
128
–
6
–
134
Total              
832
–
31
1,658
2,521
Salaries,
allowances and
benefits in kind
Performance
related bonuses
Pension scheme
contributions
Equity-settled
share option
expense
Total
remuneration
USD’000
USD’000
USD’000
USD’000
USD’000
30 September 2025     
Executive directors:
Ms. Yun Yeyi (i)     
518
–
5
956
1,479
Mr. Yan Junjie (v)    
139
–
7
–
146
Mr. Zhao Pengyu (viii) 
166
–
5
125
296
Mr. Zhou Yucong (viii) 
188
–
6
162
356
Total              
1,011
–
23
1,243
2,277
APPENDIX I
ACCOUNTANT’S REPORT
– I-36 –

<<<PAGE 574 起已省略：超出 extra_financial 字符上限；请人工复核覆盖范围>>>



## 公司中文名（DP）

- `col_DP` = Company Chinese Name (type=text unit=text missing=NA)

### 原文切片：公司中文名（DP）


<<<PAGE 1>>>
Stock Code : 0100
(A company controlled through weighted voting rights and 
incorporated in the Cayman Islands with limited liability)
MiniMax Group Inc.
GLOBAL 
OFFERING
Joint Sponsors, Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Overall Coordinators, Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
(in alphabetical order)
(in alphabetical order)

<<<PAGE 2>>>
IMPORTANT: If you are in any doubt about any of the contents of this Prospectus, you should seek independent professional advice.
MiniMax Group Inc.
(A company controlled through weighted voting rights and incorporated in the Cayman Islands with limited liability)
GLOBAL OFFERING
Number of Offer Shares under
the Global Offering
:
25,389,220 Offer Shares (subject to the
Offer Size Adjustment Option and the
Over-allotment Option)
Number of Hong Kong Offer Shares
:
1,269,480 Offer Shares (subject to
reallocation)
Number of International Offer Shares
:
24,119,740 Offer Shares (subject to
reallocation, the Offer Size Adjustment
Option and the Over-allotment Option)
Maximum Offer Price
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
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this Prospectus, make no
representation as to its accuracy or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any part of the contents of this Prospectus.
A copy of this Prospectus, having attached thereto the documents specified in the section headed “Appendix V — Documents Delivered to the Registrar of Companies in Hong Kong and Available on Display”, has been
registered by the Registrar of Companies in Hong Kong as required by section 342C of the Companies (Winding Up and Miscellaneous Provisions) Ordinance (Chapter 32 of the Laws of Hong Kong). The Securities
and Futures Commission and the Registrar of Companies in Hong Kong take no responsibility for the contents of this Prospectus or any other document referred to above.
The final Offer Price is expected to be fixed by agreement between the Overall Coordinators (for themselves and on behalf of the Underwriters) and the Company on the Price Determination Date, which is expected
to be on or around Wednesday, January 7, 2026. The Offer Price will be not more than HK$165.00 per Offer Share and is currently expected to be not less than HK$151.00 per Offer Share unless otherwise announced.
If, for any reason, the final Offer Price is not agreed by 12:00 noon on Wednesday, January 7, 2026 between the Overall Coordinators (for themselves and on behalf of the Underwriters) and the Company, the Global
Offering will not proceed and will lapse.
The Offer Shares have not been and will not be registered under the U.S. Securities Act or any state securities laws of the United States and may not be offered, sold, pledged, or transferred within the United States,
except that Offer Shares may be offered, sold or delivered (a) in the United States solely to QIBs in reliance on Rule 144A or another exemption from, or in a transaction not subject to, the registration requirements
of the U.S. Securities Act; or (b) outside the United States in offshore transactions in reliance on Regulation S.
Applicants for Hong Kong Offer Shares may be required to pay, on application (subject to application channels), the Offer Price of HK$165.00 for each Hong Kong Offer Share together with a brokerage fee of 1%, a
SFC transaction levy of 0.0027%, Stock Exchange trading fee of 0.00565% and AFRC transaction levy of 0.00015%.
Prior to making an investment decision, prospective investors should consider carefully all of the information set out in this Prospectus, including the risk factors set out in the section headed “Risk Factors”.
The obligations of the Hong Kong Underwriters under the Hong Kong Underwriting Agreement are subject to termination by the Overall Coordinators (for themselves and on behalf of the Hong Kong Underwriters) if
certain grounds arise prior to 8:00 a.m. on the Listing Date. See “Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering — Grounds for Termination”.
Our Company is a Specialist Technology Company (as defined in Chapter 18C of the Listing Rules). The securities of Specialist Technology Companies carry high investment risks including risks of share price volatility
and inflated valuation due to the difficulty in valuing such companies. Investors should fully understand the investment risks of a Specialist Technology Company and the risks disclosed by our Company before making
their investment decisions. In addition, our Company is a Pre-Commercial Company (as defined in Chapter 18C of the Listing Rules). Pre-Commercial Companies are Specialist Technology Companies that cannot meet
the revenue requirement as set out in Rule 18C.03(4) of the Listing Rules, and so are subject to a higher risk of corporate failure if they are unable to secure sufficient external funding and/or cannot generate sufficient
revenue to sustain their operations after listing.
Our Company will be controlled through weighted voting rights upon Listing. Prospective investors should be aware of the potential risks of investing in a company with a WVR structure, in particular that the WVR
Beneficiary, whose interests may not necessarily be aligned with those of our Shareholders as a whole, will be in a position to exert significant influence over the outcome of our Shareholders’ resolutions, irrespective
of how other Shareholders vote. For further information about the risks associated with the WVR structure, see “Risk Factors — Risks Related to the WVR Structure”. Prospective investors should make the decision
to in our Company only after due and careful consideration.
ATTENTION
We have adopted a fully electronic application process for the Hong Kong Public Offering. We will not provide printed copies of this prospectus to the public in relation to the Hong Kong Public Offering.
This prospectus is available at the website of the Stock Exchange at www.hkexnews.hk and our website at https://www.minimaxi.com. If you require a printed copy of this prospectus, you may download
and print from the website addresses above.
IMPORTANT
December 31, 2025

<<<PAGE 3>>>
IMPORTANT NOTICE TO INVESTORS OF HONG KONG OFFER SHARES
FULLY ELECTRONIC APPLICATION PROCESS
The Company has adopted a fully electronic application process for the Hong Kong
Public Offering.
This prospectus is available at the website of the Stock Exchange at www.hkexnews.hk
under the “HKEXnews > New Listings > New Listing Information” section, and our website at
https://www.minimaxi.com.
The Company will not provide any physical channels to accept any application for the
Hong Kong Offer Shares by the public. The contents of the electronic version of this prospectus
are identical to the prospectus as registered with the Registrar of Companies in Hong Kong
pursuant to section 342C of the Companies (Winding Up and Miscellaneous Provisions)
Ordinance.
To apply for the Hong Kong Offer Shares, you may:
(1)
apply online through the HK eIPO White Form service at www.hkeipo.hk; or
(2)
apply electronically through the HKSCC EIPO channel and cause HKSCC
Nominees to apply on your behalf by instructing your broker or custodian who is a
HKSCC Participant to give electronic application instructions via HKSCC’s FINI
system to apply for the Hong Kong Offer Shares on your behalf.
If you are an intermediary, broker or agent, please remind your customers, clients or
principals, as applicable, that this prospectus is available online at the website addresses stated
above. Please refer to the section headed “How to Apply for Hong Kong Offer Shares” in this
prospectus for further details of the procedures through which you can apply for the Hong
Kong Offer Shares.
Your application through the HK eIPO White Form service or the HKSCC EIPO
channel must be for a minimum of 20 Hong Kong Offer Shares and in one of the numbers set
out in the table.
If you are applying through the HK eIPO White Form service, you may refer to the table
below for the amount payable for the number of Hong Kong Offer Shares you have selected.
You must pay the respective maximum amount payable on application in full upon application
for Hong Kong Offer Shares.
IMPORTANT
– ii –




## 上市前投资与控制权（BA–BD/BP/BR）

- `col_BA` = Pre-IPO VC/PE backing (1=yes; 0=no) (type=integer unit=flag missing=NaN)
- `col_BB` = Ultimate controller type (type=text unit=text missing=NA)
- `col_BC` = Controller economic interest at listing (%) (type=number unit=decimal missing=NaN)
- `col_BD` = Controller voting rights at listing (%) (type=number unit=decimal missing=NaN)
- `col_BP` = Incorporation date (type=date unit=date missing=NA)
- `col_BR` = Principal place of business (type=text unit=text missing=NA)

### 原文切片：上市前投资与控制权（BA–BD/BP/BR）


<<<PAGE 219>>>
PRE-IPO INVESTMENTS
1.
Overview
We have received several rounds of Pre-IPO Investments since our inception. The following table summarizes the key terms of the Pre-IPO
Investments to our Company made by the Pre-IPO Investors:
Pre-IPO Investment
Series Angel
Series Pre-A
Series A
Series A+
Series Pre-B
Series Pre-B+
Series Pre-B++
Date of the last share
purchase agreement     
Dec 2, 2021
Mar 29 2022
May 4, 2023
Jul 6, 2023
Mar 15, 2024
Dec 4, 2024
August 16, 2025
Date of last payment of
consideration         
Dec 27, 2021
Apr 11, 2022
Dec, 14, 2023
Jul 13, 2023
Feb 19, 2025
Jun 20, 2025
August 19, 2025
Cost per Share (US$)     
$1.69
$4.23
$6.91
$8.81
$10.46
$12.28
$15.14
Discount to the Offer Price(1)
91.7%
79.2%
66.0%
56.6%
48.5%
39.5%
25.4%
Total consideration received
by our Company (US$
million)             
31.0
50.0
257.0
50.0
654.0
123.5
390.4
Implied pre-money valuations
(US$ million)         
169.0
500.0
900.0
1,550.0
1,900.0
3,000.0
3,850.0
Implied post-money valuation
(US$ million)         
200.0
550.0
1,157.0
1,600.0
2,554.0
3,123.5
4,240.4
Use of proceeds from the
Pre-IPO Investments     
As of the Latest Practicable Date, approximately 30% of the funds raised from the Pre-IPO Investments had been utilized. Such
proceeds were utilized for the research and development, capital expenditures and general working capital needs of our Group.
The Company plans to utilise the remaining proceeds from the Pre-IPO Investments for cloud services procurement related to
training and inferencing, human resources matters and marketing activities.
HISTORY, REORGANIZATION AND CORPORATE STRUCTURE
– 209 –

<<<PAGE 220>>>
Pre-IPO Investment
Series Angel
Series Pre-A
Series A
Series A+
Series Pre-B
Series Pre-B+
Series Pre-B++
Strategic benefits the Pre-IPO
Investments brought to our
Company            
At the time of the Pre-IPO Investments, our Directors were of the view that our Company would benefit from the additional
capital provided by the Pre-IPO Investors’ investments in our Company and their knowledge and experience.
Basis of determining the
consideration paid      
The consideration for the Pre-IPO Investments was determined based on arm’s length negotiations between our Company and the
Pre-IPO Investors after taking into consideration various factors including but not limited to, (i) status of milestones and
prospects of commercialization of our specialist technology products; (ii) our expansion capacity and R&D management system;
(iii) strategic layout, execution efficiency and other factors of our Company, and (iv) the timing of the investments, the market
condition, and the prospects of our business.
Lock-up period          
Sophisticated investors (including our Pathfinder SIIs) under Chapter 2.2 of the Guide for New Listing Applicants are expected to
retain at least an aggregate of 50% of their investment at the time of Listing for a period of at least six months following the
Listing, in accordance with paragraph 6 under Chapter 2.2 of the Guide for New Listing Applicants.
For lock-up period of our key persons and Pathfinder SIIs pursuant to Rule 18C.14 of the Listing Rules, see the section headed
“— Lock-up Periods” below. For lock-up period of our other existing Shareholders (including all the other Pre-IPO Investors),
see the section headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong Public Offering —
Undertaking by the other existing shareholders”.
HISTORY, REORGANIZATION AND CORPORATE STRUCTURE
– 210 –

<<<PAGE 221>>>
Pre-IPO Investment
Series Angel
Series Pre-A
Series A
Series A+
Series Pre-B
Series Pre-B+
Series Pre-B++
Reasons for fluctuations in
valuation as compared to
the immediate previous
round of pre-IPO
Investment and the Global
Offering             
(a)
the increase of our valuation from series angel financing to series pre-A financing was primarily due to the potential launch
of our new products such as text model abab1;
(b)
the increase of our valuation from series pre-A financing to series A financing was primarily due to our business
development such as the entering of agreement with our first API customer and the launch of our text model abab5.5;
(c)
the increase of our valuation from series A financing to series A+ financing was primarily due to the launch of our new
platform such as AI-native multi-modal entertainment platform Talkie;
(d)
the increase of our valuation from series A+ financing to series pre-B financing was primarily due to our further business
breakthrough including the launch of our AI-powered multi-modal entertainment platform Xingye, speech model MiniMax-
Speech-01 and MoE text model abab6;
(e)
the increase of our valuation from series pre-B financing to series pre-B+ financing was primarily due to the launch of our
visual generation platform Hailuo AI and video generation model Hailuo-01, our music model Music-01, and that our MAU
surpassed 10 million;
(f)
the increase of our valuation from series pre-B+ financing to series pre-B++ financing was primarily due to our business
development such as the launch of our open-source reasoning model MiniMax-M1 with proprietary “Linear Attention”
mechanism, our video generation model Hailuo-02, our multilingual speech model Speech-02, our audio generation tool
MiniMax Audio and our intelligent agent application MiniMax;
(g)
the increase of our valuation from series pre-B++ financing to the Global Offering was primarily due to revenue growth in
the year of 2025 and our business prospects as a result of our repaid business development.
Note:
(1)
The discount to the Offer Price is calculated based on the assumption that the Offer Price is HK$158 per Offer Share, being the mid-point of the indicative Offer Price
range and the exchange rates as disclosed in the section headed “Information about this Prospectus and the Global Offering — Exchange Rate Conversion”.
HISTORY, REORGANIZATION AND CORPORATE STRUCTURE
– 211 –

<<<PAGE 222>>>
2.
Special rights of the Pre-IPO Investors
The Pre-IPO Investors have been granted certain special rights in relation to our
Company, including but not limited to redemption rights, the pre-emptive rights, right of
co-sale, liquidation preferences, rights of first refusal, information rights and director
appointment rights. Pursuant to a shareholders’ agreement dated June 23, 2025, the redemption
rights have been suspended immediately prior to the first filing of the listing application and
all special rights (including the redemption rights) will only be terminated upon Listing.
3.
Compliance with the Guide for New Listing Applicants
On the basis that (i) the consideration for the last Pre-IPO Investment was irrevocably
settled on a date, which is more than 120 clear days before the Listing Date, and (ii) the special
rights granted to the Pre-IPO Investors will be suspended immediately prior to the first filing
of a listing application and/or shall cease to be effective and be discontinued upon Listing, the
Joint Sponsors confirm that the Pre-IPO Investments are in compliance with Chapter 4.2 of the
Guide for New Listing Applicants issued by the Stock Exchange.
4.
Information relating to our key Pre-IPO Investors
Our Sophisticated Independent Investors and Pathfinder SIIs
Set out below is a description of our Sophisticated Independent Investors (as defined
in Chapter 2.5 of the Guide for New Listing Applicants issued by the Stock Exchange).
We have four Sophisticated Independent Shareholders, namely Alisoft China (as defined
below), miHoYo SIIs (as defined below), IDG SIIs (as defined below) and Image Frame
(as defined below), and two of which, namely IDG SIIs and miHoYo SIIs, are our
Pathfinder SIIs. Save for being a shareholder of our Company and as disclosed otherwise,
each of our Sophisticated Independent Investors and their ultimate beneficial owners is
independent from and not connected with any Director, chief executive or other
substantial shareholders of our Company, its subsidiaries or any of their respective
associates (within the meaning of the Listing Rules). Each of the Pre-IPO Investors and
their ultimate controller and ultimate beneficial owners who is interested in it as to more
than 30% is independent from other Pre-IPO Investors and their ultimate controller and
ultimate beneficial owners who is interested in it as to more than 30%.
Alisoft China
Alisoft China Holding Limited (“Alisoft China”) is a limited liability company
incorporated in Hong Kong and an indirect wholly-owned subsidiary of Alibaba Group
Holding Limited (“Alibaba Group”). Alisoft China is the holding company of certain
PRC subsidiaries of Alibaba Group primarily involved in the operation of cloud
computing business. Alibaba Group is a company incorporated in the Cayman Islands,
with its American depositary shares, each representing eight ordinary shares, listed on the
New York Stock Exchange (symbol: BABA), and its ordinary shares listed on the Stock
Exchange (stock code: 9988). Alibaba Group’s mission is to make it easy to do business
HISTORY, REORGANIZATION AND CORPORATE STRUCTURE
– 212 –

<<<PAGE 223>>>
anywhere. Alibaba Group aims to build the future infrastructure of commerce and
envisions that its customers will meet, work and live at Alibaba, and that it aspires to be
a good company that will last for 102 years. Alibaba Group’s core businesses are
comprised of e-commerce and cloud computing. According to CIC, Alibaba ranked as the
largest player in China’s cloud computing market in 2024, with a market share of
approximately 22%.
Alisoft China was interested in approximately 15.66% of our Company as of the date
of 12 months prior to the date of the listing application and its shareholding was
decreased to 15.04% of our Company as of the date of our listing application. Alisoft
China is expected to be our substantial shareholder under the Listing Rules upon Listing.
Despite that Alisoft China or its close associates maintains business relationship with the
Company
as
disclosed
in
the
section
headed
“Connected Transactions”,
having
considered, among others, (i) our business relationship with Alisoft China commerced
prior to its investments in our Company, (ii) Alisoft China has no involvement in our daily
operations and management, and (iii) all of the transactions contemplated thereunder are
conducted under normal commercial terms and in the ordinary course of our business, the
Company is of the view that the existence of such business relationship will not affect the
independence of Alisoft China as one of our sophisticated independent investors.
miHoYo SIIs
miHoYo Limited and Shanghai Mihoyo Argo Technology Co., Ltd (上海米哈游阿爾
戈科技有限公司) (“miHoYo SIIs”) collectively held 7.34% beneficial interests in the
Company as of the date of 12 months prior to the date of the listing application and their
beneficial interests were decreased to 7.05% in the Company as of the date of our listing
application, which is in compliance with 18C.05 of the Listing Rules. miHoYo Limited
is indirectly wholly owned by Mr. Luo Yuhao and Shanghai Mihoyo Argo Technology
Co., Ltd is collectively owned by Mr. Cai Haoyu, Mr. Liu Wei and Mr. Luo Yuhao. The
aforesaid companies are part of the private enterprise groups founded by Mr. Cai Haoyu,
Mr. Liu Wei and Mr. Luo Yuhao. Mr. Cai Haoyu, Mr. Liu Wei and Mr. Luo Yuhao are
responsible for all investment decisions in such private enterprise groups and there had
been no investment in an entity without the unanimous agreement of Mr. Cai Haoyu, Mr.
Liu Wei and Mr. Luo Yuhao for all of the investments made by its investment department,
which has been conducting investments to more than 27 companies or partnerships with
focus on artificial intelligence, the metaverse, nuclear fusion, mobile games and
entertainment industry since establishment. Mr. Cai Haoyu, Mr. Liu Wei and Mr. Luo
Yuhao jointly own, make decisions and control such private enterprise groups and they
are also empowered to decide on the composition of the investment committee of the
investment
department. As
such,
miHoYo
Limited
and
Shanghai
Mihoyo Argo
Technology Co., Ltd shall be aggregated as one Pathfinder SII pursuant to Chapter 2.5 of
the Guide for New Listing Applicants issued by the Stock Exchange.
HISTORY, REORGANIZATION AND CORPORATE STRUCTURE
– 213 –

<<<PAGE 224>>>
Such private enterprise groups focus on video game development and publishing and
their key video game products include Genshin Impact (原神), the video game with
highest overseas revenue in the PRC from 2021 to 2023 according to Sensor Tower, which
is a leading digital market insights platform and the leading source of mobile
applications, digital advertising, retail media, and audience insights for the largest brands
and application publishers cross the globe. According to CIC, they ranked the fifth with
a market share of 3% among Chinese mobile game companies in 2021 as to revenue. For
the year ended December 31, 2022, they recorded a revenue of nearly RMB30 billion and
a net profit of more than RMB16 billion from domestic market. As of December 31, 2022,
they recorded a total assets in the PRC of more than RMB37 billion. Their businesses
have expanded to over 200 countries and regions to date. As confirmed by CIC, such
private enterprise groups are key participants in the downstream gaming industry with a
meaningful market share and size and they ranked the third among Chinese mobile game
companies as to revenue in 2024 according to Sensor Tower. As confirmed by CIC, they
have a market share of 6% among Chinese mobile game companies as to revenue in 2024.
They are also downstream customers of the Group which applied our models in their
ordinary course of businesses in 2023. As of a date which is no more than six months
prior to the date of signing of the definitive agreement and as of a date which is no more
than six months prior to the date of the listing application, they had the relevant
investment experience, knowledge and expertise to be considered sophisticated. miHoYo
Limited and Shanghai Mihoyo Argo Technology Co., Ltd irrevocably and fully settled
their investment in the Company on September 3, 2024. Based on the information
provided by miHoYo Group, examination against publicly available materials, and
discussions with the Company’s Hong Kong legal advisor, the Joint Sponsors are of the
view that relevant miHoYo entities listed above satisfy applicable requirements of the
SIIs.
Mr. Liu Wei was appointed as our non-executive Director in April 2023 after
miHoYo SIIs’ first investment into the Company in 2021. Since Mr. Liu Wei does not hold
any shares of miHoYo Limited and his beneficial interests in Shanghai Mihoyo Argo
Technology Co., Ltd do not exceed 30%, the miHoYo SIIs are not close associates of Mr.
Liu Wei under the Listing Rules and therefore, Mr. Liu Wei’s directorship in the Company
will not affect the independence of the miHoYo SIIs.
IDG SIIs
Cosmic
Station
Limited
(“Cosmic
Station”)
and
Seasonal
Charm
Limited
(“Seasonal Charm”, together with Cosmic Station, “IDG SIIs”) are investment holding
companies incorporated under the laws of the British Virgin Islands. Cosmic Station is a
wholly-owned subsidiary of IDG China Venture Capital Fund VI L.P. (“IDG China VC
VI”). Seasonal Charm is a wholly-owned subsidiary of IDG China VI Investors L.P.
(“IDG China VI Investors”). Both of IDG China VC VI and IDG China VI Investors are
exempted limited partnerships established under the laws of the Cayman Islands. They are
managed by IDG Capital Fund Management Ltd., an exempted company incorporated
under the laws of the Cayman Islands which is responsible for the overall management
and conduct of the funds’ business and affairs. IDG Capital Fund Management Ltd. is
controlled by the senior management of IDG Capital. Cosmic Station and Seasonal Charm
HISTORY, REORGANIZATION AND CORPORATE STRUCTURE
– 214 –

<<<PAGE 225>>>
collectively held approximately 3.21% beneficial interests in the Company as of the date
of 12 months prior to the date of the listing application and their beneficial interests were
decreased to 3.08% in the Company as of the listing application. Relevant considerations
were irrevocably and fully settled on May 30, 2023.
IDG China VC VI and IDG China VI Investors are venture capital funds with a
primary purpose of making equity investments, mainly in seed and growth stage
companies in China, focusing on companies in the information technology, media,
healthcare, energy, clean technology and non-technology consumer businesses and
services related industries, including, but not limited to, companies engaged in software,
internet, telecom, media and managed healthcare business. None of the ultimate
beneficial owners in each of IDG China VC VI or IDG China VI Investors is interested
in it as to more than 30%. There are more than 50 ultimate beneficial owners in IDG
China VC VI and IDG China VI Investors which mainly include well-known overseas
companies, pension funds and fund of funds. Both IDG China VC VI and IDG China VI
Investors are ultimately controlled by Mr. Ho Chi Sing and Mr. Zhou Quan, both being
Independent Third Parties.
As at a date which is no more than six months prior to the date of signing of the
definitive agreement for their investment in the Company (being October 28, 2023) and
as at a date which is no more than six months prior to the date of the Company’s listing
application (being June 26, 2025), the assets under management of IDG Capital Fund
Management Ltd. (the fund manager of IDG China VC VI and IDG China VI Investors)
were over HK$30 billion and HK$30 billion, respectively. Both IDG China VC VI and
IDG China VI Investors are operated on a discretionary basis in accordance with the
relevant partnership agreements. In compliance with Rule 18C.05 of the Listing Rules,
IDG SIIs held approximately 3.08% and 3.21% of the total issued share capital of our
Company, as of the date of submission of the Company’s first listing application) and the
commencement date of the pre-application 12-month period, respectively.
Tencent
Image
Frame
Investment
(HK)
Limited
(“Image
Frame”)
is
a
company
incorporated in Hong Kong and is a wholly owned subsidiary of Tencent Holdings
Limited (“Tencent”), a company listed on the Hong Kong Stock Exchange (stock code:
00700.HK). Tencent is a world-leading internet and technology company that develops
innovative products and services to improve the quality of life of people around the
world,
including
communications
and
social
networks,
games,
digital
content,
advertising, fintech and cloud services. Each of Image Frame and its ultimate beneficial
owners is an Independent Third Party. Image Frame held approximately 2.96% beneficial
interests in the Company as of the date of 12 months prior to the date of the listing
application and its beneficial interests were decreased to 2.84% in the Company as of the
date of the listing application. According to CIC, Tencent ranked as the third player in
China’s cloud computing market in both 2023 and 2024, with a market share of
approximately 13% in both years.
HISTORY, REORGANIZATION AND CORPORATE STRUCTURE
– 215 –

<<<PAGE 226>>>
Other key Pre-IPO Investors
We set out below descriptions of our other key Pre-IPO Investors which are of
strategic importance and provided long-term support to our Group in the issued share
capital of the Company. All of the Pre-IPO Investors whose background are disclosed in
the section headed “— Pre-IPO Investments — 4. Information relating to our key Pre-IPO
Investors” (the “Key Pre-IPO Investors”) are not required to be aggregated with the
other Pre-IPO investors on the basis that the other Pre-IPO investors are not under
common control of the Key Pre-IPO Investors. Save as Key Pre-IPO Investors, none of
the Pre-IPO Investors has a shareholding in the Company of more than 1.90% as of the
date of this Prospectus.
MNM Holdings Limited and XAM Holdings Limited
Each of MNM Holdings Limited (“MNM”) and XAM Holdings Limited (“XAM”)
is an exempted company with limited liability incorporated under the laws of the Cayman
Islands.
MNM is a subsidiary of BXA Holdings, L.P. (a limited liability partnership
established in the Cayman Islands, “BXA”), and the general partner of BXA is BXA
Holdings II GP Limited (an exempted company with limited liability incorporated in the
Cayman Islands, “BXA GP”.)
XAM is a subsidiary of NVMB IV Holdings Limited (an exempted company with
limited liability incorporated in the Cayman Islands) which is wholly-owned by BXA
Holdings II, L.P. (a limited liability partnership established in the Cayman Islands, “BXA
II”), and the general partner of BXA II is JNR Holdings GP Limited (an exempted
company with limited liability incorporated in the Cayman Islands, “JNR GP”). Each of
BXA GP and JNR GP is wholly-owned by Mr. Colm O’Connell, an Independent Third
Party. There is no individual who directly or indirectly holds an interest of 30% or more
in BXA and BXA II.
Miheng Holdings Limited
Miheng
Holdings
Limited
is
an
exempted
company
with
limited
liability
incorporated under the laws of Cayman Islands, which is wholly controlled by Beijing
Miheng Enterprise Management Consulting Partnership (Limited Partnership) (北京覓恒
企業管理諮詢合夥企業(有限合夥)) (“Beijing Miheng”), which is controlled by Zhuhai
Gao Ling Private Fund Management Co., Ltd. The general partner of Beijing Miheng is
Wuxi Ningjun Enterprise Management Co., Ltd. (無錫寧袀企業管理有限公司), which is
controlled by Hillhouse Capital. The limited partners of Beijing Miheng are five private
equity funds that are record-filed with Asset Management Association of China. There is
no individual who directly or indirectly holds an interest of 30% or more in Beijing
Miheng.
HISTORY, REORGANIZATION AND CORPORATE STRUCTURE
– 216 –

<<<PAGE 227>>>
HSG
HSG Growth VII Holdco E, Ltd. and Himalia Holding Limited are companies
incorporated in the Cayman Islands with limited liability. The sole shareholder of HSG
Growth VII Holdco E, Ltd. is HongShan Capital Growth Fund VII, L.P. (“HSG GVII
Fund”), whose general partner is HSG Growth VII Management, L.P. The sole
shareholder of Himalia Holding Limited is HongShan Capital Growth Fund VI, L.P.
(“HSG GVI Fund”), whose general partner is HSG Growth VI Management, L.P. HSG
GVII Fund and HSG GVI Fund are investment funds whose primary purpose is to make
equity investments in private companies. The general partner of each of HSG Growth VII
Management, L.P. and HSG Growth VI Management, L.P. is HSG Holding Limited,
which is a wholly-owned subsidiary of SNP China Enterprises Limited. Neil Nanpeng
Shen is the sole shareholder of SNP China Enterprises Limited.
MPC VII Pte. Ltd.
MPC VII Pte. Ltd. (“MPC VII”) is a limited company incorporated and domiciled
in Singapore, which is owned as to 93.97% and 6.03% by MPC VII L.P. and MPC VII-A
L.P., respectively. The general partner of both MPC VII L.P. and MPC VII-A L.P., each
an exempted limited partnership incorporated under the laws of the Cayman Islands, is
MPC Management VII L.P.. The general partner of MPC Management VII L.P. is MPC
GPGP VII Ltd. David Su is the controlling shareholder of MPC GPGP VII Ltd.. No single
limited partner holds 30% or more interests in MP VII L.P. or in MPC VII-A L.P..
Astrend Entities
Astrend Opportunity IV Beta Limited, Astrend X Fund, L.P., Astrend X-2 Limited,
and Golden Horizon Limited (collectively “Astrend Entities”) are entities under common
control.
Astrend Opportunity IV Beta Limited is a company incorporated under the laws of
the British Virgin Islands, which is wholly owned by Shunwei China Internet Opportunity
Fund IV, L.P.. The general partner of Shunwei China Internet Opportunity Fund IV, L.P.
is Shunwei Capital Partners V GP, L.P., and the general partner of Shunwei Capital
Partners V GP, L.P. is Shunwei Capital Partners V GP Limited. Silver Unicorn Ventures
Limited holds more than 50% of the issued and outstanding shares of Shunwei Capital
Partners V GP Limited, and Mr. Koh Tuck Lye, an Independent Third Party, is the sole
shareholder of Silver Unicorn Ventures Limited.
Astrend X Fund, L.P. is an exempted limited partnership incorporated under the laws
of the Cayman Islands. The general partner of Astrend X Fund, L.P. is Astrend X Partners
GP, L.P., and the general partner of Astrend X Partners GP, L.P. is Astrend X Partners GP
Limited. Silver Unicorn Ventures Limited holds more than 50% of the issued and
outstanding shares of Astrend X Partners GP Limited, and Mr. Koh Tuck Lye, an
Independent Third Party, is the sole shareholder of Silver Unicorn Ventures Limited.
HISTORY, REORGANIZATION AND CORPORATE STRUCTURE
– 217 –

<<<PAGE 228>>>
Astrend X-2 Limited is a company incorporated under the laws of the British Virgin
Islands, which is wholly owned by Astrend X Fund, L.P.
Golden Horizon Limited is a company incorporated under the laws of the British
Virgin Islands, which is ultimately controlled by Mr. Koh Tuck Lye.
Pacific Century Group
Bravo Ideas Investments Limited is an investment holding company incorporated in
the Cayman Islands ultimately controlled by Mr. Li Tzar Kai, Richard (“Mr. Li”). Mr. Li
is the founder, chairman and chief executive of Pacific Century Group, an Asia-based
private investment group founded in 1993.
Future Capital
Each of Future Capital Discovery Fund IV, L.P. and Ideafication Holdings L.P. is a
limited partnership whose general partner is Golden Equinox Ltd. and there are no limited
partners who are interested in Future Capital Discovery Fund IV, L.P. as to more than
30%. The fund is ultimately controlled by Huang Mingming, an Independent Third Party
and the controller of Golden Equinox Ltd. Each partnership is organized for the primary
purposes of identifying, analyzing, investing in, managing, otherwise dealing with and
realizing investments directly or indirectly in equity and equity-linked securities of
privately-held seed and early-stage high-growth companies.
Meaningful investment from Sophisticated Independent Investors
We have received investments from two Pathfinder SIIs, namely IDG SIIs and
miHoYo SIIs, each having invested in the Group for at least 12 months prior to the first
submission of our listing application to the Stock Exchange for the purpose of the Global
Offering. In accordance with Chapter 2.5 of the Guide for New Listing Applicants issued
by the Stock Exchange, each of IDG SIIs and miHoYo SIIs holds more than 3%, and in
aggregate held approximately 10.13% of the Company’s total issued share capital as at
the date of the first listing application throughout the period from June 27 2024 (being the
commencement date of the pre-application 12-month period) to June 26, 2025 (being the
date of submission of the Company’s first listing application). For details of the
ownership percentage of shareholding in our Company’s share capital of each of the
Sophisticated Independent Investors, see “— Capitalization of Our Company”.
As of the Latest Practicable Date, our Sophisticated Independent Investors (as
identified above) held, in aggregate, approximately 25.44% in the total issued share
capital of our Company and approximately 23.32% upon Listing assuming the Offer Size
Adjustment Option and the over-allotment option are not exercised. At Listing, our
expected market capitalization at the time of Listing will exceed HK$30 billion based on
the indicative Offer Price range and such Sophisticated Independent Investors will hold,
in aggregate, no less than 15% in the total issued share capital of our Company.
HISTORY, REORGANIZATION AND CORPORATE STRUCTURE
– 218 –

<<<PAGE 229>>>
CAPITALIZATION OF OUR COMPANY
The following table sets out our shareholding structure (a) as of the Latest Practicable Date and (b) immediately upon the completion of the
Global Offering (assuming that (i) the Offer Size Adjustment Option and the Over-allotment Option are not exercised, (ii) all Preferred Shares have
been converted into Shares on a one-to-one basis immediately upon the completion of the Global Offering, and (iii) without taking into account any
Shares that may further be issued under the Post-IPO Share Incentive Plan).
As of the Latest
Practicable Date
Upon Completion of
the Global Offering
(assuming the Offer Size
Adjustment Option and
the Over-allotment Option
are not exercised)
Shareholders
Class A
Ordinary
Shares
Class B
Ordinary
Shares
Preferred
Shares
Aggregate
number of
Shares
Aggregate
ownership
percentage
Voting power
in our
Company
Aggregate
beneficiary
interest
Aggregate
Voting Power
percentage(1)
Our Controlling Shareholders and Entities Controlled by Our WVR Beneficiary(9)
MiniMax Limited             
–
15
–
15
0.00001%
0.00001%
0.000005%
0.00001%
MiniMax Matrix(2)
           
5,000,000
–
–
5,000,000
1.79%
4.75%
1.64%
0.48%
MiniMax Awakening            
–
11,509,339
–
11,509,339
4.11%
10.94%
3.77%
11.12%
Alpha EXP(3)                
–
62,593,180
–
62,593,180
22.35%
59.21%
20.49%
60.45%
Entities Controlled by Our WVR Beneficiary(10)
Floating Sky(12)               
–
7,000,000
–
7,000,000
2.50%
6.65%
2.29%
6.76%
Our Employee Shareholding Platform
MiniMax Gene               
20,890,736
–
–
20,890,736
7.46%
1.99%
6.84%
2.02%
HISTORY, REORGANIZATION AND CORPORATE STRUCTURE
– 219 –

<<<PAGE 230>>>
As of the Latest
Practicable Date
Upon Completion of
the Global Offering
(assuming the Offer Size
Adjustment Option and
the Over-allotment Option
are not exercised)
Shareholders
Class A
Ordinary
Shares
Class B
Ordinary
Shares
Preferred
Shares
Aggregate
number of
Shares
Aggregate
ownership
percentage
Voting power
in our
Company
Aggregate
beneficiary
interest
Aggregate
Voting Power
percentage(1)
Our Pathfinder SIIs
miHoYo Limited
(米哈遊有限公司)            
–
–
16,015,779
16,015,779
5.72%
1.52%
5.24%
1.55%
Shanghai Mihoyo Argo Technology
Co., Ltd (上海米哈游阿爾戈科技有限
公司)                    
–
–
1,912,399
1,912,399
0.68%
0.18%
0.63%
0.18%
Sub-total(4)                 
–
–
17,928,178
17,928,178
6.40%
1.70%
5.87%
1.73%
Cosmic Station Limited          
–
–
7,301,687
7,301,687
2.61%
0.69%
2.39%
0.71%
Seasonal Charm Limited         
–
–
535,263
535,263
0.19%
0.05%
0.18%
0.05%
Sub-total(4)                 
–
–
7,836,950
7,836,950
2.80%
0.75%
2.57%
0.76%
Our Other SIIs
Alisoft China Holding Limited(11)   
–
–
38,247,987
38,247,987
13.66%
3.64%
12.52%
3.69%
Image Frame Investment (HK)
Limited                  
–
–
7,232,084
7,232,084
2.58%
0.69%
2.37%
0.70%
HISTORY, REORGANIZATION AND CORPORATE STRUCTURE
– 220 –

<<<PAGE 231>>>
As of the Latest
Practicable Date
Upon Completion of
the Global Offering
(assuming the Offer Size
Adjustment Option and
the Over-allotment Option
are not exercised)
Shareholders
Class A
Ordinary
Shares
Class B
Ordinary
Shares
Preferred
Shares
Aggregate
number of
Shares
Aggregate
ownership
percentage
Voting power
in our
Company
Aggregate
beneficiary
interest
Aggregate
Voting Power
percentage(1)
Our Other Key Pre-IPO Investors
XAM Holdings Limited
        
–
–
14,201,184
14,201,184
5.07%
1.35%
4.65%
1.37%
MNM Holdings Limited         
–
–
2,343,196
2,343,196
0.84%
0.22%
0.77%
0.23%
Sub-total(4)                 
–
–
16,544,380
16,544,380
5.91%
1.57%
5.42%
1.60%
Miheng Holdings Limited        
–
–
3,442,472
3,442,472
1.23%
0.33%
1.13%
0.33%
Himalia Holding Limited         
1,656,805
–
–
1,656,805
0.59%
0.16%
0.54%
0.16%
HSG Growth VII Holdco E, Ltd.    
–
–
9,011,235
9,011,235
3.22%
0.86%
2.95%
0.87%
Sub-total(4)                 
1,656,805
–
9,011,235
10,668,040
3.81%
1.01%
3.49%
1.03%
MPC VII Pte. Ltd             
–
–
7,772,332
7,772,332
2.78%
0.74%
2.54%
0.75%
Astrend Opportunity IV Beta Limited 
–
–
2,260,471
2,260,471
0.81%
0.21%
0.74%
0.22%
Astrend X Fund, L.P.           
–
–
1,446,417
1,446,417
0.52%
0.14%
0.47%
0.14%
Astrend X-2 Limited            
–
–
814,054
814,054
0.29%
0.08%
0.27%
0.08%
Golden Horizon Limited         
–
–
411,097
411,097
0.15%
0.04%
0.13%
0.04%
Sub-total(4)                 
–
–
4,932,039
4,932,039
1.76%
0.47%
1.61%
0.48%
HISTORY, REORGANIZATION AND CORPORATE STRUCTURE
– 221 –

<<<PAGE 232>>>
As of the Latest
Practicable Date
Upon Completion of
the Global Offering
(assuming the Offer Size
Adjustment Option and
the Over-allotment Option
are not exercised)
Shareholders
Class A
Ordinary
Shares
Class B
Ordinary
Shares
Preferred
Shares
Aggregate
number of
Shares
Aggregate
ownership
percentage
Voting power
in our
Company
Aggregate
beneficiary
interest
Aggregate
Voting Power
percentage(1)
Bravo Ideas Investments Limited    
–
–
3,633,558
3,633,558
1.30%
0.35%
1.19%
0.35%
Future Capital Discovery Fund IV,
L.P.                     
–
–
2,519,330
2,519,330
0.90%
0.24%
0.82%
0.24%
Ideafication Holdings L.P.        
–
–
1,111,903
1,111,903
0.40%
0.11%
0.36%
0.11%
Sub-total(4)                 
–
–
3,631,233
3,631,233
1.30%
0.35%
1.19%
0.35%
Our Other Pre-IPO Investors
Lingham Beauty Limited         
–
–
4,817,351
4,817,351
1.72%
0.46%
1.58%
0.47%
Forever Gain Limited           
–
–
478,100
478,100
0.17%
0.05%
0.16%
0.05%
Sub-total(8)                 
–
–
5,295,451
5,295,451
1.89%
0.50%
1.73%
0.51%
HISTORY, REORGANIZATION AND CORPORATE STRUCTURE
– 222 –

<<<PAGE 233>>>
As of the Latest
Practicable Date
Upon Completion of
the Global Offering
(assuming the Offer Size
Adjustment Option and
the Over-allotment Option
are not exercised)
Shareholders
Class A
Ordinary
Shares
Class B
Ordinary
Shares
Preferred
Shares
Aggregate
number of
Shares
Aggregate
ownership
percentage
Voting power
in our
Company
Aggregate
beneficiary
interest
Aggregate
Voting Power
percentage(1)
China Life (Shenzhen) Technology
Innovation Private Equity Investment
Fund Partnership (Limited
Partnership) (國壽(深圳)科技創新私
募股權投資基金合夥企業(有限合
夥))                     
–
–
2,825,791
2,825,791
1.01%
0.27%
0.93%
0.27%
Hefei China Life Carbon Peak and
Carbon Neutrality Phase I Equity
Investment Fund Partnership
(Limited Partnership) (合肥國壽碳峰
碳中一期股權投資基金合夥企業(有限
合夥))                   
–
–
330,021
330,021
0.12%
0.03%
0.11%
0.03%
Sub-total(5)                 
–
–
3,155,812
3,155,812
1.13%
0.30%
1.03%
0.30%
Planetree PARTNERS HARVEST I,
L.P.                     
–
–
478,100
478,100
0.17%
0.05%
0.16%
0.05%
Planetree Partners III, L.P.        
–
–
2,154,046
2,154,046
0.77%
0.20%
0.71%
0.21%
Planetree Partners III-A, L.P.      
–
–
253,416
253,416
0.09%
0.02%
0.08%
0.02%
Sub-total(6)                 
–
–
2,885,562
2,885,562
1.03%
0.27%
0.94%
0.28%
HISTORY, REORGANIZATION AND CORPORATE STRUCTURE
– 223 –

<<<PAGE 386>>>
SUBSTANTIAL SHAREHOLDERS
So far as our Directors are aware, immediately following completion of the Global
Offering, assuming the Offer Size Adjustment Option and the Over-allotment Option are not
exercised, the following persons will have interests and/or short positions in the Shares or
underlying shares of our Company which would fall to be disclosed to us pursuant to the
provisions of Divisions 2 and 3 of Part XV of the SFO, or, who are directly or indirectly,
interested in 10% or more of the nominal value of any class of share capital carrying rights to
vote in all circumstances at general meetings of our Company:
Name of substantial shareholder
Capacity/Nature
of Interest(1)
Number
of Shares
Approximate
percentage of
shareholding in
respective class of
Share of our Company
upon completion of the
Global Offering
assuming the Offer
Size Adjustment
Option and the
Over-allotment Option
are not exercised
Approximate
percentage of
shareholding in the
issued share capital of
our Company upon
completion of the
Global Offering
assuming the Offer
Size Adjustment
Option and the
Over-allotmen Option
are not exercised(2)
Class B Ordinary Shares
Alpha EXP(3)                  Beneficial owner
62,593,180
77.18%
20.49%
Scaling EXP Limited(3)             Interest in controlled
corporations
62,593,180
77.18%
20.49%
Trident Trust Company (HK) Limited(3)   Trustee
62,593,180
77.18%
20.49%
MiniMax Limited(3)              Beneficial owner
15
0.00002%
0.000005%
MiniMax Awakening(3)             Beneficial owner
11,509,339
14.19%
3.77%
Local Linearity(3)                Interest in controlled
corporations
11,509,354
14.19%
3.77%
Dr. Yan                     Interest in controlled
corporations
74,102,534
91.37%
24.26%
Floating Sky                  Beneficial Owner
7,000,000
8.63%
2.29%
Floating Cloud Limited            Interest in controlled
corporations
7,000,000
8.63%
2.29%
Trident Trust Company (HK) Limited(3)
  Trustee
7,000,000
8.63%
2.29%
Ms. Yun                     Interest in controlled
corporations
7,000,000
8.63%
2.29%
Class A Ordinary Shares
MiniMax Matrix(3)               Beneficial owner
5,000,000
2.23%
1.64%
Local Linearity(3)
              Interested in controlled
corporations
5,000,000
2.23%
1.64%
Dr. Yan                     Interested in controlled
corporations
5,000,000
2.23%
1.64%
Alibaba China Holding Limited        Beneficial owner
38,247,987
17.05%
12.52%
SUBSTANTIAL SHAREHOLDERS
– 376 –

<<<PAGE 387>>>
Name of substantial shareholder
Capacity/Nature
of Interest(1)
Number
of Shares
Approximate
percentage of
shareholding in
respective class of
Share of our Company
upon completion of the
Global Offering
assuming the Offer
Size Adjustment
Option and the
Over-allotment Option
are not exercised
Approximate
percentage of
shareholding in the
issued share capital of
our Company upon
completion of the
Global Offering
assuming the Offer
Size Adjustment
Option and the
Over-allotmen Option
are not exercised(2)
Alisoft Investment Holding Limited(4)    Interest in controlled
corporations
38,247,987
17.05%
12.52%
Alisoft Holding Limited(4)           Interest in controlled
corporations
38,247,987
17.05%
12.52%
Alibaba Group Holding Limited(4)       Interest in controlled
corporations
38,247,987
17.05%
12.52%
miHoYo Limited                Beneficial owner
16,015,779
7.14%
5.24%
Shanghai Fanxing Dingchuang Technology
Company Limited(5)            
Interest in controlled
corporations
16,015,779
7.14%
5.24%
Luo Yuhao(5)                  Interest in controlled
corporations
16,015,779
7.14%
5.24%
XAM Holdings Limited(6)           Beneficial owner
14,201,184
6.33%
4.65%
NVMB IV Holdings Limited(6)        Interest in controlled
corporations
14,201,184
6.33%
4.65%
BXA Holdings II,
L.P.(6)                    
Interest in controlled
corporations
14,201,184
6.33%
4.65%
JNR Holdings GP Limited(6)          Interest in controlled
corporations
14,201,184
6.33%
4.65%
Mr. Colm O’Connell(1) (7)           Interest in controlled
corporations
16,544,380
7.37%
5.42%
Notes:
(1)
All interests stated are long positions.
(2)
The table above assumes the Preferred Shares will be automatically converted into Class A Ordinary Shares
on a 1:1 basis.
(3)
MiniMax Awakening and MiniMax Limited are wholly owned by Dr. Yan through Local Linearity. MiniMax
Matrix is also a controlled entity of Dr. Yan through Local Linearity. Alpha EXP is held by Scaling EXP
Limited as to 99% and Local Linearity as to 1%. Scaling EXP Limited is wholly-owned by Trident Trust
Company (Hong Kong) Limited, which acts as the trustee of Alpha EXP Trust. Alpha EXP Trust is a trust
established by Dr. Yan (as settlor) for the benefit of himself.
Floating Sky is held by Floating Cloud Limited as to 99% and Apricity Investment Limited as to 1%. Apricity
Investment Limited is wholly-owned by Ms. Yun. Floating Cloud Limited is wholly-owned by Trident Trust
Company (Hong Kong) Limited, which acts as the trustee of Floating Sky Trust. Floating Sky Trust is a trust
established by Ms. Yun (as settlor) for the benefit of herself.
SUBSTANTIAL SHAREHOLDERS
– 377 –

<<<PAGE 388>>>
Accordingly, under the SFO, Dr. Yan is deemed to be interested in the Shares held by MiniMax Awakening,
MiniMax Limited, MiniMax Matrix and Alpha EXP. Local Linearity is deemed to be interested in the Shares
held by MiniMax Awakening, MiniMax Limited and MiniMax Matrix. Scaling EXP Limited and Trident Trust
Company (Hong Kong) Limited is deemed to be interested in the Shares held by Alpha EXP. Ms. Yun, Floating
Cloud Limited and Trident Trust Company (Hong Kong) Limited is deemed to be interested in the Shares held
by Floating Sky.
(4)
Alibaba China Holding Limited is controlled by Alisoft Investment Holding Limited, a company controlled
Alisoft Holding Limited, which is in turn controlled by Alibaba Group Holding Limited. Therefore, each of
Alisoft Investment Holding Limited, Alisoft Holding Limited, and Alibaba Group Holding Limited is deemed
to be interested in the Shares held by Alibaba China Holding Limited. The number of Shares held by Alibaba
China Holding Limited upon Listing does not take into account the cornerstone investment to be made by
Alisoft China as disclosed in the section headed “Cornerstone Investors”.
(5)
miHoYo Limited is wholly owned by Shanghai Fanxing Dingchuang Technology Company Limited, which is
wholly owned by Luo Yuhao. Therefore, each of Shanghai Fanxing Dingchuang Technology Company Limited
and Luo Yuhong is deemed to be interested in the Shares held by miHoYo Limited.
(6)
For further details, please refer to the section headed “History, Reorganization and Corporate Structure — 4.
Information relating to our key Pre-IPO Investors — MNM Holdings Limited and XAM Holdings Limited” of
this Prospectus.
(7)
Mr. Colm O’Connell is the sole shareholder of each of JNR Holdings GP Limited and BXA Holdings II GP
Limited, being the general partner of BXA Holdings II, L.P. and BXA Holdings, L.P., respectively, which in
turn indirectly held 14,201,184 Shares and 2,343,196 Shares through XAM Holdings Limited and MNM
Holdings Limited, respectively. Mr. Colm O’Connell is deemed to be interested in these Shares.
Save as disclosed above and the section headed “Statutory and General Information — C.
Further Information about our Directors and Substantial Shareholders” in Appendix IV to this
Prospectus, our Directors are not aware of any person who will, immediately following
completion of the Global Offering, assuming the Offer Size Adjustment Option and the
Over-allotment Option are not exercised, have any interest and/or short position in the Shares
or underlying Shares of our Company which will be required to be disclosed to our Company
and the Stock Exchange pursuant to the provisions of Divisions 2 and 3 of Part XV of the SFO,
or, who are directly or indirectly, interested in 10% or more of the nominal value of any class
of share capital carrying rights to vote in all circumstances at general meeting of our Company
or other members of the Group.
SUBSTANTIAL SHAREHOLDERS
– 378 –

<<<PAGE 389>>>
THE CORNERSTONE PLACING
We have entered into cornerstone investment agreements (each a “Cornerstone
Investment Agreement”, and together the “Cornerstone Investment Agreements”) with the
cornerstone investors set out below (each a “Cornerstone Investor”, and together the
“Cornerstone Investors”), pursuant to which the Cornerstone Investors have agreed to,
subject to certain conditions, subscribe at the Offer Price for a certain number of Offer Shares
that
may
be
purchased
for
an
aggregate
amount
of
approximately
US$350
million
(approximately HK$2,723 million) (the “Cornerstone Placing”). The calculations in this
section, which are based on the exchange rates as disclosed in the section headed “Information
about this Prospectus and the Global Offering”, are for illustration purpose.
Assuming an Offer Price of HK$151.0, being the low-end of the indicative Offer Price
range set out in this Prospectus, the total number of Offer Shares to be subscribed by the
Cornerstone Investors would be 18,034,240 Offer Shares. The table below reflects the
shareholding percentage immediately after the completion of the Global Offering assuming
there is no other change made to the issued share capital of our Company between the Latest
Practicable Date and the Listing Date (or the date of exercise of Over-allotment Option (where
applicable)).
Assuming the Offer Size Adjustment Option
is not exercised
Assuming the Offer Size Adjustment Option
is exercised in full
Assuming the
Over-allotment Option
is not exercised
Assuming the
Over-allotment Option
is exercised in full
Assuming the
Over-allotment Option
is not exercised
Assuming the
Over-allotment Option
is exercised in full
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
71.03%
5.90%
61.77%
5.83%
61.77%
5.83%
53.71%
5.75%
Assuming an Offer Price of HK$158.0, being the mid-point of the Offer Price range set
out in this Prospectus, the total number of Offer Shares to be subscribed by the Cornerstone
Investors would be 17,235,120 Offer Shares. The table below reflects the shareholding
percentage immediately after the completion of the Global Offering assuming there is no other
change made to the issued share capital of our Company between the Latest Practicable Date
and the Listing Date (or the date of exercise of Over-allotment Option (where applicable)).
Assuming the Offer Size Adjustment Option
is not exercised
Assuming the Offer Size Adjustment Option
is exercised in full
Assuming the
Over-allotment Option
is not exercised
Assuming the
Over-allotment Option
is exercised in full
Assuming the
Over-allotment Option
is not exercised
Assuming the
Over-allotment Option
is exercised in full
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
Approximate
% of the
Offer Share
Approximate
% of the
Shares in
issue
67.88%
5.64%
59.03%
5.57%
59.03%
5.57%
51.33%
5.50%
CORNERSTONE INVESTORS
– 379 –

<<<PAGE 390 起已省略：超出 ownership 字符上限；请人工复核覆盖范围>>>



## 发售时间表（CC–CD）

- `col_CC` = Subscription opening date (type=date unit=date missing=NA)
- `col_CD` = Subscription closing date (type=date unit=date missing=NA)

### 原文切片：发售时间表（CC–CD）


<<<PAGE 7>>>
Notes:
(1)
All times refer to Hong Kong local time, except as otherwise stated.
(2)
You will not be permitted to submit your application through the designated website at www.hkeipo.hk after
11:30 a.m. on the last day for submitting applications. If you have already submitted your application and
obtained an application reference number from the designated website at or before 11:30 a.m., you will be
permitted to continue the application process (by completing payment of application monies) until 12:00 noon
on the last day for submitting applications, when the application lists close.
(3)
If there is/are a tropical cyclone warning signal number 8 or above, a “black” rainstorm warning and/or
Extreme Conditions in force in Hong Kong at any time between 9:00 a.m. and 12:00 noon on Tuesday,
January 6, 2026, the application lists will not open or close on that day. Please see “How to Apply for Hong
Kong Offer Shares — E. Severe Weather Arrangements”.
(4)
Applicants who apply for Hong Kong Offer Shares through HKSCC EIPO channel or by instructing your
broker or custodian to apply on your behalf via HKSCC EIPO Channel should see “How to Apply for Hong
Kong Offer Shares — A. Application for Hong Kong Offer Shares — 2. Application Channels”.
(5)
The Price Determination Date is expected to be on or before Wednesday, January 7, 2026 and, in any event,
not later than 12:00 noon on Wednesday, January 7, 2026. If, for any reason, the Offer Price is not agreed
between the Overall Coordinators (for themselves and on behalf of the Underwriters) and us by 12:00 noon
on Wednesday, January 7, 2026, the Global Offering will not proceed and will lapse.
(6)
None of the website or any of the information contained on the website forms part of this prospectus.
(7)
The Share certificates will only become valid evidence of title at 8:00 a.m. on the Listing Date provided that
the Global Offering has become unconditional and the right of termination described in “Underwriting —
Underwriting arrangements and expenses — Hong Kong Public Offering — Grounds for termination” has not
been exercised. Investors who trade Class A Ordinary Shares on the basis of publicly available allocation
details or prior to the receipt of Share certificates or the Share certificates becoming valid do so entirely at their
own risk.
(8)
HK eIPO White Form e-Auto Refund payment instructions/refund checks will be issued in respect of wholly
or partially unsuccessful applications pursuant to the Hong Kong Public Offering and also in respect of wholly
or partially successful applications in the event that the final Offer Price is less than the price payable per Offer
Share on application. Part of the applicant’s identification document number, or, if the application is made by
joint applicants, part of the identification document number of the first-named applicant, provided by the
applicant(s) may be printed on the refund check, if any. Such data would also be transferred to a third party
for refund purposes. Banks may require verification of an applicant’s identification document number before
encashment of the refund check. Inaccurate completion of an applicant’s identification document number may
invalidate or delay encashment of the refund check.
(9)
Applicants who have applied for Hong Kong Offer Shares through HKSCC EIPO channel should refer to the
section headed “How to Apply for Hong Kong Offer Shares — D. Despatch/Collection of Share Certificates
and Refund of Application Monies” for details.
Applicants who have applied through the HK eIPO White Form service and paid their applications monies
through single bank accounts may have refund monies (if any) dispatched to the bank account in the form of
HK eIPO White Form e-Auto Refund payment instructions. Applicants who have applied through the HK
eIPO White Form service and paid their application monies through multiple bank accounts may have refund
monies (if any) dispatched to the address as specified in their application instructions in the form of refund
checks in favor of the applicant (or, in the case of joint applications, the first-named applicant) by ordinary
post at their own risk.
Any uncollected Share certificates will be dispatched by ordinary post, at the applicants’ risk, to the addresses
specified in the relevant applications.
Further information is set out in the section headed “How to Apply for Hong Kong Offer Shares — D.
Despatch/Collection of Share Certificates and Refund of Application Monies”.
EXPECTED TIMETABLE(1)
– vi –

<<<PAGE 8>>>
The above expected timetable is a summary only. You should see “Structure of the
Global Offering” and “How to Apply for Hong Kong Offer Shares” for details of the
structure of the Global Offering, including the conditions of the Global Offering, and the
procedures for application for the Hong Kong Offer Shares.
If the Global Offering does not become unconditional or is terminated in accordance
with its terms, the Global Offering will not proceed. In such a case, the Company will
make an announcement as soon as practicable thereafter.
EXPECTED TIMETABLE(1)
– vii –

<<<PAGE 9>>>
IMPORTANT NOTICE TO INVESTORS
This Prospectus is issued by us solely in connection with the Hong Kong Public
Offering and does not constitute an offer to sell or a solicitation of an offer to buy any
security other than the Hong Kong Offer Shares offered by this Prospectus pursuant to
the Hong Kong Public Offering. This Prospectus may not be used for the purpose of, and
does not constitute, an offer or a solicitation of an offer to subscribe for or buy, any
security in any other jurisdiction or in any other circumstances. No action has been taken
to permit a public offering of the Offer Shares or the distribution of this Prospectus in any
jurisdiction other than Hong Kong. The distribution of this Prospectus and the offering
and sale of the Offer Shares in other jurisdictions are subject to restrictions and may not
be made except as permitted under the applicable securities laws of such jurisdictions
pursuant to registration with or authorization by the relevant securities regulatory
authorities or an exemption therefrom.
You should rely only on the information contained in this Prospectus to make your
investment decision. We have not authorized anyone to provide you with information that
is different from what is contained in this Prospectus. Any information or representation
not made in this Prospectus must not be relied on by you as having been authorized by
us, the Joint Sponsors, the Overall Coordinators, the Joint Global Coordinators, the Joint
Bookrunners, the Joint Lead Managers, the Capital Market Intermediaries, the
Underwriters, any of our or their respective directors, officers or representatives, or any
other person or party involved in the Global Offering.
Page
EXPECTED TIMETABLE. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
iv
CONTENTS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
viii
SUMMARY . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
1
DEFINITIONS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
34
GLOSSARY OF TECHNICAL TERMS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
49
FORWARD-LOOKING STATEMENTS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
58
RISK FACTORS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
60
WAIVERS AND EXEMPTION . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
116
INFORMATION ABOUT THIS PROSPECTUS AND THE GLOBAL
OFFERING. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
126
CONTENTS
– viii –

<<<PAGE 10>>>
DIRECTORS AND PARTIES INVOLVED IN THE GLOBAL OFFERING . . . . .
131
CORPORATE INFORMATION . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
141
INDUSTRY OVERVIEW . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
144
REGULATORY OVERVIEW . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
168
HISTORY, REORGANIZATION AND CORPORATE STRUCTURE . . . . . . . . . .
201
BUSINESS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
236
DIRECTORS AND SENIOR MANAGEMENT . . . . . . . . . . . . . . . . . . . . . . . . . . . .
350
RELATIONSHIP WITH OUR CONTROLLING SHAREHOLDERS . . . . . . . . . .
366
CONNECTED TRANSACTIONS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
370
SUBSTANTIAL SHAREHOLDERS. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
376
CORNERSTONE INVESTORS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
379
SHARE CAPITAL . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
391
FINANCIAL INFORMATION. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
403
FUTURE PLANS AND USE OF PROCEEDS. . . . . . . . . . . . . . . . . . . . . . . . . . . . .
466
UNDERWRITING . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
474
STRUCTURE OF THE GLOBAL OFFERING. . . . . . . . . . . . . . . . . . . . . . . . . . . .
491
HOW TO APPLY FOR HONG KONG OFFER SHARES . . . . . . . . . . . . . . . . . . .
509
APPENDIX I
ACCOUNTANT’S REPORT . . . . . . . . . . . . . . . . . . . . . . . .
I-1
APPENDIX II
UNAUDITED PRO FORMA FINANCIAL
INFORMATION . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
II-1
APPENDIX III
SUMMARY OF THE CONSTITUTION OF
OUR COMPANY AND CAYMAN ISLANDS
COMPANY LAW . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
III-1
APPENDIX IV
STATUTORY AND GENERAL INFORMATION . . . . . . . .
IV-1
APPENDIX V
DOCUMENTS DELIVERED TO THE REGISTRAR OF
COMPANIES IN HONG KONG AND AVAILABLE
ON DISPLAY . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
V-1
CONTENTS
– ix –

<<<PAGE 11>>>
This summary aims to give you an overview of the information contained in this
Prospectus. As it is a summary, it does not contain all the information that may be
important to you. You should read the whole Prospectus before you decide to invest in the
Offer Shares. In particular, we are a specialist technology company seeking to list on the
Main Board of the Hong Kong Stock Exchange under Chapter 18C of the Listing Rules
because we are unable to meet the requirements under Rule 8.05 (1), (2) or (3) of the
Listing Rules. There are unique challenges, risks and uncertainties associated with
investing in companies such as ours. In addition, we have incurred operating loss since
our inception, and we may incur adjusted net loss (non-IFRS measure) and operating loss
for the foreseeable future. We had negative net cash flow from operating activities during
the Track Record Period. We did not declare or pay any dividends during the Track
Record Period and may not pay any dividends in the foreseeable future. Your investment
decision should be made in light of these considerations.
There are risks associated with any investment. Some of the particular risks in
investing in the Offer Shares are set out in the section headed “Risk Factors” in this
Prospectus. You should read that section carefully in full before you decide to invest in
the Offer Shares.
OVERVIEW
MiniMax is a global AI foundation model company. Founded by a group of forward-
thinking engineers, we are committed to driving AI innovation towards performing the full
range of human intellectual tasks, from learning and reasoning to planning and generalizing
knowledge across diverse domains.
The foundation model market is expanding at an unprecedented pace, rapidly reshaping
human society. The global foundation model market is projected to exceed US$300 billion by
2030. IDC estimates that AI will cumulatively contribute US$19.9 trillion to the global
economy through 2030 and drive 3.5% of global GDP in 2030. We believe we have established
a solid foundation to capture this market potential and have already made meaningful progress.
Our Journey
Our journey has been guided by a clear vision since inception centered on two key areas:
developing advanced foundation models and creating AI-native products that enhance
productivity and enrich life. Recognizing that real-world human interaction is inherently
multi-modal, we stand out as one of the few foundation model developers who are committed
to developing multi-modal models from day one. We take a cost-efficient approach in pursuing
AI advancement, delivering high performance while ensuring our technological breakthroughs
remain accessible and affordable to users globally. We adopted the Mixture-of-Experts (MoE)
architecture and hybrid attention mechanism at an early stage, which significantly reduced
computation resources while maintaining globally recognized performance.
SUMMARY
– 1 –

<<<PAGE 12>>>
Large 
Language 
Model
Product 
Launching
2022
2023
2024
2025
OPEN Platform
Video 
Generation 
Model
Audio Model
abab 1
abab 5.5 abab 6.0 (MoE)
Text-01
M1
M2
Hailuo-01
Hailuo-02
Music-01
Speech-02
Music-02
oi
d
u
A
x
a
M
i
n
i
M
e
y
g
n
i
X
/ei
k
la
T
MiniMax 
(with Agent)
Speech-01
We have been consistently iterating our models to higher intelligence levels. Today, our
proprietary foundation model suite, led by MiniMax-M2, Hailuo-02, and Speech-02, has long
context processing capacity and can understand, generate, and integrate a wide range of
modalities, including text, video, and audio. These models power our major AI-native products
— including MiniMax, Hailuo AI, MiniMax Audio, Talkie/Xingye, and our enterprise and
developer-facing Open Platform, delivering intelligent and dynamic experiences to users
globally.
As of September 30, 2025, our AI-native products had cumulatively served over
200 million individual users across over 200 countries and regions, and more than 100
thousand enterprises and developers across over 100 countries and regions.
Scalability
We believe scalability is pivotal to our long-term goals. To build one of the most scalable
AI businesses globally, we focus on three core competencies — original research, a sustainable
business model, and organizational efficiency. These pillars support both continuous model
advancement and product commercialization at scale. Together, the three core competencies
enable an elevated level of intelligence for everyone—powering productivity and enriching
life. See “Business — Scalability.”
SUMMARY
– 2 –

<<<PAGE 13>>>
OUR MODELS AND PRODUCT OFFERINGS
Our Foundation Model Suite
We have leveraged our R&D capabilities to build a comprehensive suite of foundation
models, and maintain competitiveness across various modalities. Our foundation model suite
includes large language models, video generation models, and models for speech and music
generation.
Large Language Model: MiniMax M Series
The MiniMax M Series, comprising MiniMax-M1 and MiniMax-M2, represents our
flagship family of large language models. MiniMax-M1, launched in June 2025, is an
open-source, large-scale hybrid-attention reasoning model. It adopts a hybrid MoE architecture
combined with a lightning attention mechanism, enabling long-context processing with a
context window of up to 1 million tokens and supporting the development of more capable AI
agents.
MiniMax-M2, our latest large language model, is engineered for elite performance in
coding and agentic tasks. Leveraging a carefully engineered, data-efficient MoE architecture
and activation-parameter design, MiniMax-M2 delivers higher-performance capabilities at
substantially faster inference speeds compared with MiniMax-M1, while maintaining an
optimized profile across model intelligence, responsiveness and cost-efficiency.
Video Generation Model: Hailuo-02
The Hailuo-02 series model generates high-quality video content from a variety form of
information inputs. Commercialized at scale with competitive results on global benchmarks
upon its release, Hailuo-02 offers cinematic video quality, advanced prompt adherence, smooth
motion, and style diversity. With user-friendly interface and ability to do aesthetic refinement,
it helps content creators and advertisers produce compelling videos out of simple prompts.
Speech Generation Model: Speech-02
The Speech-02 model series is designed to generate natural, high-quality speech from text
input. Widely recognized as a top performing speech model globally upon its release in April
2025, our Speech-02 model delivers hyper-realistic, personalized voice synthesis across
multiple languages.
Our AI-Native Product Offerings
Leveraging our multi-modal foundation model suite, we deliver AI-native products and
services that unleash the power of AI to benefit both individual users, developers and enterprise
customers around the world. The evolution of our AI-native products is rooted in advancements
SUMMARY
– 3 –

<<<PAGE 14>>>
in its underlying foundation models. Through continuous iterations and upgrades of foundation
models and the development of new ones, we are able to design and create AI-native products
with enhanced productivity and user experience.
MiniMax: Intelligent Agent Application
MiniMax is our intelligent AI agent application, which is designed to autonomously
perform a wide range of tasks through natural language instructions. Supported by our
foundation models, MiniMax Agent can plan, reason, and execute complex actions such as
coding, research, document drafting, and presentation creation within a unified workspace.
Hailuo AI: Flagship Visual Generation Platform
Hailuo AI fully integrates our Hailuo-02 model that has quickly become one of the
world’s most popular AI image and video creation platforms through organic user adoption. It
is offered in both web and app forms, and is designed for real-time, high-quality image and
video generation.
MiniMax Audio: Advanced Audio Generation Tool
MiniMax Audio is designed to provide users with high-fidelity audio generation
capabilities. Accessible via web platform, MiniMax Audio integrates the Company’s Speech-02
model to support interactive audio synthesis and generate natural, high-quality speech from
text input.
Talkie/Xingye: Multi-modal Entertainment Platform
Talkie (for international markets)/Xingye (for Chinese domestic market) is a globally
recognized AI-native multi-modal entertainment platform. Users of Talkie/Xingye can engage
with emotionally responsive AI themes or virtual characters powered by the Company’s
proprietary AI-models.
MiniMax Open Platform
Our Open Platform offers scalable, configurable AI services to enterprise customers and
developers across more than 100 countries and regions as of September 30, 2025. Through
public APIs and services, enterprise and developer customers can access the Company’s
foundation models and integrate such text, video and audio model capabilities into their own
products and services. Our Open Platform supports rapid business deployment in key industry
sectors such as smart devices, healthcare, cultural tourism, finance, and internet services —
making it one of the world’s largest open platforms for enterprises and developers in terms of
average daily token volume, signifying widespread adoption.
SUMMARY
– 4 –

<<<PAGE 519 起已省略：超出 offering 字符上限；请人工复核覆盖范围>>>



<<< 抽取包结束 >>>


## 手册硬规则（必须遵守）
1. 金额一律换算成**基本货币单位**（HK$125.6 million -> 125600000）；百分比填小数；确认的零填数字 0。
2. **合并报表唯一原则（严防母公司单体报表混淆）**：所有资产、权益、负债、销售、利润、现金流、有息债务等财务指标（V–AN、AU–AY、BE 等）**必须且只能**取自**合并财务报表（CONSOLIDATED Financial Statements / Group）**；**绝对严禁**采纳母公司单体报表（`STATEMENT OF FINANCIAL POSITION OF THE COMPANY` / `COMPANY BALANCE SHEETS`）。year-1/2/3 必须是**同一套历史期间**；year-1 销售/利润若不是全年（如 9 个月），按手册年化并在 quote 注明原始期间；附加流量 AU/AW/AX 一律**不年化**；AV（年末现金）和 BE（有息负债）是期末余额，AY 是比例。
3. AU 经营现金流 = net cash from operating activities，**不是**经营利润；AV 现金及等价物**不自动包含**受限现金。
4. AX 只填**当期新增**的资本化开发成本，不是期末余额；表中明确写 `–`/nil 时填数字 0。
5. AL/AM/AN 是净利润（profit for the year）；AI/AJ/AK 是税前利润。
6. 承销佣金：招股书按全球发售披露时 AO/AP 填同一比例；只按香港公开发售披露时 AP=0；给金额时用金额÷对应基数；
   **不能**把总上市费用当佣金。AQ 绿鞋只能按招股书披露，**不能默认 15%**。
7. col_CJ 基石名单必须来自真正的 Cornerstone Investors / Cornerstone Placing 名单表，
   **不要**用目录、豁免段、风险因素里的普通提及；无基石填 `"NA"`；用分号分隔全称。
8. col_AS 上市途径按招股书披露的 basis of listing / 适用章节填（如 Chapter 18C），**不能**按行业推断；col_DP 中文名填简体。
9. **Pre-IPO VC/PE 十个字段（所有 cohort 均适用）**：先检索 `HISTORY AND DEVELOPMENT — Pre-IPO Investments`，再用 `SUBSTANTIAL SHAREHOLDERS`、股本表和董事章节核对。名单、轮次、持股比例、协议日期必须按该公司自己的招股书取值；严禁从其他公司 JSON、旧 cohort 数据或投资机构常识补值。
   - `col_pre_ipo_investors` 仅列招股书披露的上市前投资者，分号分隔；同一投资者只记一次。
   - VC、PE、CVC、国资可同时为 1；按投资者/基金性质分类并在各自 quote 中给出该公司披露依据。普通产业股东不自动算 CVC，国资身份不自动等于 VC/PE。
   - 只有招股书明确披露上市前投资，或可从上市前股东表确认，才填 1。没有找到证据不等于 0；只有披露明确确认无此类投资时填 0，否则填 NaN/NA。
   - `col_vc_pe_stake` 取上市前所有机构投资者持股合计，统一使用紧邻上市前的股权口径，避免把上市后新股或基石配售重复计入；无明确合计时逐项核对并说明计算，不得猜。
   - 董事席位只在能把董事/观察员与上市前机构投资者明确关联时填 1；最早轮次与持有年限按最早投资协议日期计算至该公司的招股书日期。缺日期则持有年限填 NaN。
   - 十个字段分别引用支持本字段的页码和连续原文；不得把一条通用 Pre-IPO 引文复制到所有字段。审慎分类或关键日期不确定时留缺失并说明原因。
10. 不确定就填 NaN/NA 并在 quote 里写明原因，**绝对不要猜**；**不要**为了配平等式修改原文数字。
## 输出位置
- out：`/Users/georgezhu/Desktop/UROP HK IPO/pipeline/prospectus_pipeline/out/extracted/HKIPO-MB0100.json`

## 任务：定向重抽（验证驱动升级）
1. 上方内联的是**相关主题分片**（不是完整包），下方 only_fields 列出本次必须补齐/修正的字段。
2. 只处理 only_fields 列出的字段；其余字段以现有 JSON 为准，不要改动。
3. 找不到证据的字段按契约填 NaN/NA，并在 quote 里说明已检索过。
4. 写 JSON 到指定 out 路径（完整契约结构），运行 `validate --only <code>` 确认后记录 state。

## only_fields（本次范围）
-（见 validation）

