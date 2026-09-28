你是 HK IPO 数据库的数据员，负责公司 9976.HK Shenzhen Longsys Electronics Co., Ltd. - H Shares 的字段质量。

## 公司
- 公司：9976.HK Shenzhen Longsys Electronics Co., Ltd. - H Shares


<<< 抽取包开始（权威字段契约与种子切片） >>>

--- 分片：HKIPO-MB9976-topic_offering.md ---
# 招股书抽取主题分片：9976.HK Shenzhen Longsys Electronics Co., Ltd. - H Shares - 【基础发售与股本结构 (Offering & Share Capital)】

- 股票代码：9976.HK ｜ 公司：Shenzhen Longsys Electronics Co., Ltd. - H Shares
- 主题标识：topic_offering ｜ 包含字段数：15 个
- 覆盖组：share_structure, price, offering, chinese_name

## 唯一输出契约（必须严格遵守）

只输出一个 JSON 对象，顶层必须是：
`{"code":"9976.HK","topic":"topic_offering","fields":{"col_X":{"value":...,"page":...,"quote":"...","confidence":"high|medium|low"}}}`。

本分片必须且只能输出下列 15 个字段的 entry，不要输出其它主题的字段。

## 本分片核心规则
- 严格依赖 Share Capital 汇总表，严禁采纳历史沿革中的发行数字
- 核验 5 个股本恒等式：M=R+S、M=Q+P、L=N+Q、L=O+M
- 价格区间 T/U 换算为港元原币，U <= T
- 中文名 DP 必须填简体中文

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


<<<PAGE 295>>>
BEFORE THE GLOBAL OFFERING
As of the Latest Practicable Date, the total issued share capital of our Company was
429,668,149 A Shares of nominal value of RMB1.00 each, all of which are listed on the ChiNext
Market of the Shenzhen Stock Exchange.
Description of Shares
Number of Shares
Approximate % of
issued share
capital
A Shares in issue                          
429,668,149
100.0%
UPON COMPLETION OF THE GLOBAL OFFERING
Immediately following the completion of the Global Offering, assuming the Offer Size
Adjustment Option and the Over-allotment Option are not exercised and no additional Shares are
issued pursuant to the 2026 Restricted Share Incentive Scheme, the share capital of our Company
will be as follows:
Description of Shares
Number of Shares
Approximate % of
issued share
capital
A Shares in issue                          
429,668,149
94.28%
H Shares to be issued pursuant to the Global
Offering                               
26,077,800
5.72%
Total:                                  
455,745,949
100.0%
Immediately following the completion of the Global Offering, assuming the Offer Size
Adjustment Option is fully exercised, the Over-allotment Option is not exercised, and no additional
Shares are issued pursuant to the 2026 Restricted Share Incentive Scheme, the share capital of our
Company will be as follows:
Description of Shares
Number of Shares
Approximate % of
issued share
capital
A Shares in issue                          
429,668,149
93.48%
H Shares to be issued pursuant to the Global
Offering                               
29,989,450
6.52%
Total:                                  
459,657,599
100.0%
Immediately following the completion of the Global Offering, assuming the Offer Size
Adjustment Option is not exercised and the Over-allotment Option is fully exercised but no
additional Shares are issued pursuant to the 2026 Restricted Share Incentive Scheme, the share
capital of our Company will be as follows:
Description of Shares
Number of Shares
Approximate % of
issued share
capital
A Shares in issue                          
429,668,149
93.48%
H Shares to be issued pursuant to the Global
Offering                               
29,989,450
6.52%
Total:                                  
459,657,599
100.0%
SHARE CAPITAL
– 286 –

<<<PAGE 296>>>
Immediately following the completion of the Global Offering, assuming both the Offer Size
Adjustment Option and the Over-allotment Option are fully exercised but no additional Shares are
issued pursuant to the 2026 Restricted Share Incentive Scheme, the share capital of our Company
will be as follows:
Description of Shares
Number of Shares
Approximate % of
issued share
capital
A Shares in issue                          
429,668,149
92.57%
H Shares to be issued pursuant to the Global
Offering                               
34,487,850
7.43%
Total:                                  
464,155,999
100.0%
OUR SHARES
Our H Shares in issue upon completion of the Global Offering, and our A Shares, are ordinary
Shares in our share capital and are considered as one class of Shares. Shenzhen-Hong Kong Stock
Connect has established a stock connect mechanism between Chinese Mainland and Hong Kong.
Our A Shares can be subscribed for and traded by Chinese Mainland investors, qualified foreign
institutional investors or qualified foreign strategic investors and must be traded in Renminbi. As
our A Shares are eligible securities under the Northbound Trading Link, they can also be subscribed
for and traded by Hong Kong and other overseas investors pursuant to the rules and limits of
Shenzhen-Hong Kong Stock Connect. Our H Shares can be subscribed for or traded by Hong Kong
and other overseas investors and qualified domestic institutional investors. If our H Shares are
eligible securities under the Southbound Trading Link, they can also be subscribed for and traded
by Chinese Mainland investors in accordance with the rules and limits of Shanghai-Hong Kong
Stock Connect or Shenzhen-Hong Kong Stock Connect.
RANKING
Our H Shares and our A Shares are regarded as one class of Shares and will rank pari passu
with each other in all other respects and, in particular, will rank equally for all dividends or
distributions declared, paid or made after the date of this document. All dividends in respect of our
H Shares are to be paid by us in Hong Kong dollars whereas all dividends in respect of our A Shares
are to be paid by us in Renminbi. In addition to cash, dividends may also be distributed in the form
of Shares. Holders of our H Shares will receive share dividends in the form of H Shares, and holders
of our A Shares will receive share dividends in the form of A Shares.
NO CONVERSION OF OUR A SHARES INTO H SHARES FOR LISTING AND TRADING
ON THE HONG KONG STOCK EXCHANGE
Our A Shares and our H Shares are generally neither interchangeable nor fungible, and the
market prices of our A Shares and our H Shares may be different after the Global Offering. The
Guidelines on Application for “Full Circulation” of Domestic Unlisted Shares of H-share
Companies (《H股公司境內未上市股份申請“全流通”業務指引》) announced by the CSRC are not
applicable to companies dual listed in the PRC and on the Hong Kong Stock Exchange. As of the
Latest Practicable Date, there were no relevant rules or guidelines from the CSRC providing that
A Shareholders may convert A shares held by them into H shares for listing and trading on the Hong
Kong Stock Exchange.
SHARE CAPITAL
– 287 –

<<<PAGE 297>>>
APPROVAL FROM HOLDERS OF A SHARES REGARDING THE GLOBAL OFFERING
Approval from holders of A Shares is required for our Company to issue H Shares and seek
the listing of H Shares on the Hong Kong Stock Exchange. Such approval was obtained by us at the
shareholders’ general meeting of our Company held on January 3, 2025 and is subject to the
following conditions:
(i)
Size of the Offer. The proposed number of H Shares to be offered shall not exceed 20%
of the total issued share capital enlarged by the H Shares to be issued pursuant to the
Global Offering (before the exercise of the Over-allotment Option). The number of H
Shares to be issued pursuant to the full exercise of the Over-allotment Option shall not
exceed 15% of the total number of H Shares to be offered initially under the Global
Offering.
(ii)
Method of Offering. The method of offering shall be by way of an international offering
to institutional investors and a public offer for subscription in Hong Kong.
(iii) Target Investors. The offering of H Shares will be conducted globally to target investors
including but not limited to qualified offshore PRC (for the purpose of the offering,
including (a) Hong Kong, (b) Macau, China, (c) Taiwan, China, and (d) foreign
countries) institutional investors, corporations and individuals, qualified onshore
institutional investors and other qualified investors.
(iv)
Price Determination Basis. The issue price of the H Shares will be determined, among
others, after due consideration of the interests of existing shareholders of our Company,
acceptance of investors and the risks related to the offering, according to international
practice, through the demands for orders and book building process, subject to the
capital market conditions.
(v)
Validity Period. The issue of H Shares and listing of H Shares on the Hong Kong Stock
Exchange shall be completed within 18 months from the date when the shareholders’
meeting was held on January 3, 2025, and such validity period should be extended to the
date of completion of the Global Offering if approval from competent authorities is
obtained within 18 months. Since we have received a filing notice from the CSRC dated
September 9, 2025, the validity period of approval from holders of A Shares has been
extended accordingly.
There is no other approved offering plans for our Shares except the Global Offering.
SHAREHOLDERS’ GENERAL MEETINGS
For details of circumstance under which our shareholders’ general meeting is required, please
refer to the section headed “Summary of the Articles of Association — Shareholders and
Shareholders’ General Meetings” in Appendix V to this document.
RESTRICTED SHARE INCENTIVE SCHEMES
Certain employees of our Company and our subsidiaries are eligible to subscribe in interests
of our Shares through the Restricted Share Incentive Schemes. For details, please refer to the
section headed “Statutory and General Information — 4. Restricted Share Incentive Schemes” in
Appendix VI to this document.
SHARE CAPITAL
– 288 –

<<<PAGE 298>>>
SUBSTANTIAL SHAREHOLDERS
So far as our Directors are aware, immediately following completion of the Global Offering
and no other changes are made to the issued share capital of our Company between the Latest
Practicable Date and Listing, the following persons will have an interest or short position (as
applicable) in our Shares or underlying Shares which would fall to be disclosed to us under the
provisions of Divisions 2 and 3 of Part XV of the SFO, or, will be, directly or indirectly, interested
in 10% or more of the issued voting shares of our Company or any other member of our Group:
Assuming that the Offer Size
Adjustment Option and the Over-
allotment Option are not exercised
Assuming that the Offer Size
Adjustment Option and the Over-
allotment Option are fully exercised
Shareholder
Nature of interest
Description of
Shares
Number of Shares
directly or
indirectly held
Approximately
% of
shareholding in
our A Shares
immediately
after the Global
Offering
Approximately
% of
shareholding in
the total share
capital of our
Company
immediately
after the Global
Offering
Approximately
% of
shareholding in
our A Shares
immediately
after the Global
Offering
Approximately
% of
shareholding in
the total share
capital of our
Company
immediately
after the Global
Offering
Mr. Cai      Beneficial owner
A Shares
162,071,900(2)
37.72%
35.56%
37.72%
34.92%
Interest held
jointly with
another
person(1)
A Shares
14,700,000
3.42%
3.23%
3.42%
3.17%
Ms. Cai     Beneficial owner
A Shares
14,700,000
3.42%
3.23%
3.42%
3.17%
Interest held
jointly with
another
person(1)
A Shares
162,071,900
37.72%
35.56%
37.72%
34.92%
Notes:
(1)
Pursuant to the Concert Party Agreement dated August 9, 2021, Mr. Cai and Ms. Cai agreed that they shall act in
concert with respect to all matters which are subject to approval in general meetings or Board meetings of the
Company, for the period since the date of the Concert Party Agreement and upon the termination of the Concert Party
Agreement. For further details, please refer to the section headed “History and Corporate Structure — Concert Party
Arrangement”. As such, each of Mr. Cai and Ms. Cai are deemed to be interested in the Shares each other is interested
in.
(2)
As of the Latest Practicable Date, Mr. Cai has pledged 2,600,000 A Shares, representing approximately 0.61% of the
total issued share capital of our Company, in favour of Shenzhen Zhongxiaodan Small Loan Co., Ltd.* (深圳市中小
擔小額貸款有限公司), an Independent Third Party, for personal financing needs (the “Share Pledge”). Mr. Cai shall
repay the aforesaid financing loan before September 20, 2027, and the Share Pledge shall be released upon the full
repayment of such financing loan.
For further information on any other person who will be, immediately following completion
of the Global Offering, directly or indirectly, interested in 10% or more of the issued voting Shares
of any other member of our Group, please refer to the section headed “Statutory and General
Information — 3. Further Information about our Directors — C. Disclosure of Interests — (ii)
Interest in our Company’s subsidiaries” in Appendix VI to this document.
SUBSTANTIAL SHAREHOLDERS
– 289 –

<<<PAGE 299>>>
THE CORNERSTONE PLACING
We have entered into cornerstone investment agreements (each a “Cornerstone
Investment Agreement”, and together the “Cornerstone Investment Agreements”) with the
cornerstone investors set out below (each a “Cornerstone Investor”, and together the
“Cornerstone Investors”), pursuant to which the Cornerstone Investors have agreed to,
subject to certain conditions, subscribe, or cause their designated entities to subscribe, at the
Offer Price for such number of Offer Shares (rounded down to the nearest whole board lot of
50 H Shares) that may be purchased for an aggregate amount of approximately US$151.13
million (or approximately HK$1,185.32 million, calculated based on the exchange rate as
disclosed in this prospectus) and exclusive of brokerage fee, the SFC transaction levy, the
AFRC transaction levy and the Stock Exchange trading fee (the “Cornerstone Placing”).
Based on the Offer Price of HK$240.60 per H Share, being the maximum Offer Price, the
total number of Offer Shares to be subscribed for by the Cornerstone Investors would be
4,926,050 H Shares. The table below reflects the shareholding percentage immediately after the
completion of the Global Offering.
Assuming the Offer Size Adjustment Option is not exercised
Assuming the Offer Size Adjustment Option is exercised in full
Assuming the Over-allotment
Option is not exercised
Assuming the Over-allotment
Option is exercised in full
Assuming the Over-allotment
Option is not exercised
Assuming the Over-allotment
Option is exercised in full
Approximate
% of the
Offer Shares
Approximate
% of the total
issued share
capital
Approximate
% of the
Offer Shares
Approximate
% of the total
issued share
capital
Approximate
% of the
Offer Shares
Approximate
% of the total
issued share
capital
Approximate
% of the
Offer Shares
Approximate
% of the total
issued share
capital
18.89%
1.08%
16.43%
1.07%
16.43%
1.07%
14.28%
1.06%
We believe that the Cornerstone Placing signifies our Cornerstone Investors’ confidence
in our Company and its business prospect, and that the Cornerstone Placing will help to raise
the profile of our Company. We became acquainted with each of the Cornerstone Investors in
its ordinary course of operation through our Group’s business network, or through introduction
by our Company’s business partners or the Overall Coordinators of the Global Offering.
The Cornerstone Placing will form part of the International Offering, and save as
otherwise obtained consent from the Stock Exchange, the Cornerstone Investors, and their
respective close associates will not subscribe for any Offer Shares under the Global Offering
(other than pursuant to the Cornerstone Investment Agreements). The Offer Shares to be
subscribed by the Cornerstone Investors will rank pari passu in all respects with the fully paid
H Shares in issue following the Global Offering of the Company and will be counted towards
the public float of our Company under Rule 19A.13A of the Listing Rules. Immediately
following the completion of the Global Offering, the Cornerstone Investors or their close
associates will not, by virtue of their cornerstone investments, have any Board representation
in our Company; and none of the Cornerstone Investors and their close associates will become
a substantial Shareholder of our Company. Each of (i) an affiliate of Transsion International
Limited; (ii) the parent company of SDMC HK; (iii) an affiliate of Colorful Technology; (iv)
CORNERSTONE INVESTORS
– 290 –

<<<PAGE 300>>>
the parent company of the investment manager of AHGO SPC; and (v) Lenovo is an existing
customer of our Group. Other than a guaranteed allocation of the relevant Offer Shares at the
final Offer Price, the Cornerstone Investors do not have any preferential rights under each of
their
respective
Cornerstone
Investment Agreements,
as
compared
with
other
public
Shareholders. There are no side arrangements or agreements between our Company and the
Cornerstone Investors or any benefit, direct or indirect, conferred on the Cornerstone Investors
by virtue of or in relation to the Listing, other than a guaranteed allocation of the relevant Offer
Shares at the final Offer Price, following the principles as set out in Chapter 4.15 of the Guide
for New Listing Applicants.
Among the Cornerstone Investors, CITIC AM HK is a close associate of an existing
minority Shareholders. The Stock Exchange has granted a waiver from strict compliance with
the requirements under Rule 10.04 and consent under Paragraph 1C(2) of Appendix F1 to the
Listing Rules and paragraph 17 of Chapter 4.15 of the Guide for New Listing Applicants to
permit H Shares in the International Offering to be placed to certain existing minority
Shareholders and/or their close associates. For further details, see “Waivers and Exemption —
Allocation of our H Shares to Existing Minority Shareholders and their Close Associates under
Rule 10.04 and Paragraph 1C(2) of Appendix F1 to the Listing Rules”. In addition, CITIC AM
HK and CLSA Limited, being one of the Overall Coordinators and Underwriters of the Global
Offering, are members of the same group of companies. Accordingly, CITIC AM HK is a
connected client of CLSA Limited. The Stock Exchange has granted a consent under Paragraph
1C(1) of the Appendix F1 to the Listing Rules to permit CITIC AM HK to participate in the
Global Offering as a cornerstone investor on the following basis and conditions as set out in
Paragraph 6 of Chapter 4.15 of the Guide. For further details, see “Waivers and Exemption —
Consent in respect of the Proposed Subscription of H Shares by a Cornerstone Investor who is
a Connected Client”.
Save as otherwise disclosed, to the best knowledge of our Company, (i) each of the
Cornerstone Investors is an Independent Third Party; (ii) other than CITIC AM HK, none of
the Cornerstone Investors is accustomed to taking instructions from our Company, the
Directors, the chief executive, substantial Shareholders, existing Shareholders or any of their
respective subsidiaries or their respective close associates in relation to the acquisition,
disposal, voting or other disposition of the Offer Shares; (iii) other than CITIC AM HK, none
of the subscription of the relevant Offer Shares by any of the Cornerstone Investors is financed
by
our
Company,
the
Directors,
chief
executive,
substantial
Shareholders,
existing
Shareholders or any of their respective subsidiaries or their respective close associates, each
Cornerstone Investor will be utilizing its internal financial resources, financial resources of its
shareholders or (in the case of Cornerstone Investors which are funds or investment managers)
the assets managed for its investors as its source of funding for the subscription of the Offer
Shares, and each Cornerstone Investor has sufficient funds to settle its respective investment
under the Cornerstone Placing; and (iv) each of the Cornerstone Investors has confirmed that
all necessary approvals have been obtained with respect to the Cornerstone Placing and that no
specific approval from any stock exchange (if relevant) is required for the relevant Cornerstone
Placing. We further confirm that (i) none of the Cornerstone Investors has the right to nominate
any Director nor has any representative on our Board; and (ii) none of the Cornerstone
Investors is expected to be involved in the management of the business of our Company. In
addition, to the best knowledge of our Company, save as otherwise disclosed, each of the
CORNERSTONE INVESTORS
– 291 –

<<<PAGE 301>>>
Cornerstone Investors is independent from each other and makes independent investment
decisions. CITIC AM HK, as a discretionary investment manager for certain managed
accounts, is a close associate of China Asset Management Co., Ltd. (“CAMC”), one of the
2025 A Share Placees, and has confirmed that (i) its decision to participate in the Global
Offering as a Cornerstone Investor is independent of CAMC’s participation in the 2025 A
Shares Issuance; and (ii) no side agreement, bundling arrangement or other understanding
exists linking CAMC’ s participation in the 2025 A Shares Issuance with its participation in the
Global Offering. The Overall Coordinators have also confirmed that their allocation of H
Shares under the Global Offering has been, and will be, conducted entirely separately and
independently of the 2025 A Shares Issuance, and that no bundling arrangement, side
agreement or other understanding linking participation in the 2025 A Shares Issuance with any
allocation of H Shares under the Global Offering exists. To the best knowledge of the
Company, none of the Cornerstone Investor and/or its ultimate beneficial owner is a 2025 A
Share Placee and/or its close associate or ultimate beneficial owner, save for CITIC AM HK
being a close associate of CAMC.
The Cornerstone Investors have agreed to pay for the relevant Offer Shares that they have
subscribed before dealings in the Company’s H Shares commence on the Stock Exchange.
Some of the Cornerstone Investors have agreed that, our Company, the Joint Sponsors and the
Overall Coordinators may in their sole discretion defer the delivery of all or part of the Offer
Shares it will subscribe to on a date later than the Listing Date. Such delayed delivery
arrangement is in place to facilitate the over-allocation in the International Offering. There will
be no delayed delivery if there is no over-allocation in the International Offering. Where
delayed delivery takes place, (i) there would be delayed delivery of Offer Shares to some of
the Cornerstone Investors based on commercial negotiations with the Cornerstone Investors,
(ii) the delayed delivery date should be no later than three business days following the last day
on which the Over-allotment Option may be exercised, (iii) no extra payment will be made to
the relevant Cornerstone Investors for the purpose of the delayed delivery arrangement, and
(iv) each of the Cornerstone Investors has agreed that it shall nevertheless pay for the relevant
Offer Shares in full before the Listing. As such, there will not be any deferred settlement in
payment by the Cornerstone Investors.
Details of the actual number of Offer Shares to be allocated to the Cornerstone Investors
will be disclosed in the allotment results announcement of our Company to be published on or
around Monday, September 7, 2026.
To the best knowledge of the Company and the Overall Coordinators, and based on the
indicative interest of investment of the Cornerstone Investors and/or their close associates as
of the date of this prospectus, certain Cornerstone Investors and/or their close associates may
participate in the International Offering as placees and subscribe for further Offer Shares in the
Global Offering. Our Company will seek the Stock Exchange’s consent and/or waiver to allow
the Cornerstone Investors and/or their close associates to participate in the International
Offering as placees pursuant to Chapter 4.15 of the Guide for New Listing Applicants. Whether
such Cornerstone Investors and/or their close associates will place orders in the International
Offering are uncertain and will be subject to the final investment decisions of such investors
and the terms and conditions of the Global Offering.
CORNERSTONE INVESTORS
– 292 –

<<<PAGE 302>>>
OUR CORNERSTONE INVESTORS
The table below sets forth details of the Cornerstone Placing, assuming an Offer Price of HK$240.60, being the maximum Offer Price:
Cornerstone Investor
Subscription
amount(1)
Number of
Offer Shares(2)
Assuming an Offer Price of HK$240.60 per H Share (being the maximum Offer Price)
Assuming the Offer Size Adjustment Option is not exercised
Assuming the Offer Size Adjustment Option is exercised in full
Assuming the Over-allotment
Option is not exercised
Assuming the Over-allotment
Option is exercised in full
Assuming the Over-allotment
Option is not exercised
Assuming the Over-allotment
Option is exercised in full
Approximate %
of the Offer
Shares
Approximate %
of the issued
share capital
Approximate %
of the Offer
Shares
Approximate %
of the issued
share capital
Approximate %
of the Offer
Shares
Approximate %
of the issued
share capital
Approximate %
of the Offer
Shares
Approximate %
of the issued
share capital
Transsion International Limited  
USD25,000,000
814,950
3.13%
0.18%
2.72%
0.18%
2.72%
0.18%
2.36%
0.18%
YuFeng
YuFeng             
USD10,000,000
325,950
1.25%
0.07%
1.09%
0.07%
1.09%
0.07%
0.95%
0.07%
YuFeng LPF          
USD10,000,000
325,950
1.25%
0.07%
1.09%
0.07%
1.09%
0.07%
0.95%
0.07%
CITIC AM HK           HKD150,000,000
623,400
2.39%
0.14%
2.08%
0.14%
2.08%
0.14%
1.81%
0.13%
AHGO SPC            
USD12,750,000
415,600
1.59%
0.09%
1.39%
0.09%
1.39%
0.09%
1.21%
0.09%
Lenovo              
USD10,000,000
325,950
1.25%
0.07%
1.09%
0.07%
1.09%
0.07%
0.95%
0.07%
Lens Technology HK       
USD10,000,000
325,950
1.25%
0.07%
1.09%
0.07%
1.09%
0.07%
0.95%
0.07%
Ingenic Semiconductor HK    
USD10,000,000
325,950
1.25%
0.07%
1.09%
0.07%
1.09%
0.07%
0.95%
0.07%
Ju Yuen International       
USD10,000,000
325,950
1.25%
0.07%
1.09%
0.07%
1.09%
0.07%
0.95%
0.07%
Colorful Technology        HKD75,000,000
311,700
1.20%
0.07%
1.04%
0.07%
1.04%
0.07%
0.90%
0.07%
HOSIN HK             HKD56,000,000
232,750
0.89%
0.05%
0.78%
0.05%
0.78%
0.05%
0.67%
0.05%
Huadeng Technology       
USD5,000,000
162,950
0.62%
0.04%
0.54%
0.04%
0.54%
0.04%
0.47%
0.04%
Wind Sabre            
USD5,000,000
162,950
0.62%
0.04%
0.54%
0.04%
0.54%
0.04%
0.47%
0.04%
CQTech              
USD5,000,000
162,950
0.62%
0.04%
0.54%
0.04%
0.54%
0.04%
0.47%
0.04%
SDMC HK             HKD20,000,000
83,100
0.32%
0.02%
0.28%
0.02%
0.28%
0.02%
0.24%
0.02%
Total               
4,926,050
18.89%
1.08%
16.43%
1.07%
16.43%
1.07%
14.28%
1.06%
CORNERSTONE INVESTORS
– 293 –

<<<PAGE 362>>>
CONSOLIDATED STATEMENTS OF CHANGES IN EQUITY
Year ended 31 December 2023
Attributable to owners of the parent
Share
capital
Capital
reserve*
Share-
based
payment
reserve*
Foreign
currency
translation
reserve*
Statutory
surplus
reserve*
Retained
earnings*
Total
Non-
controlling
interests
Total
equity
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
(note 31)
(note 32)
(note 32)
(note 32)
(note 32)
(note 32)
At 1 January 2023       
412,864
3,879,139
–
137,013
51,792
2,157,945
6,638,753
–
6,638,753
Loss for the year       
–
–
–
–
–
(827,809)
(827,809)
(9,447)
(837,256)
Other comprehensive income
for the year:
Foreign currency translation 
–
–
–
11,578
–
–
11,578
–
11,578
Total comprehensive
income/(loss) for the year  
–
–
–
11,578
–
(827,809)
(816,231)
(9,447)
(825,678)
Share-based payments     
–
–
198,607
–
–
–
198,607
–
198,607
Transfer from retained earnings 
–
–
–
–
10,708
(10,708)
–
–
–
Non-controlling interests arising
from acquisition of
subsidiaries (note 34)    
–
–
–
–
–
–
–
437,722
437,722
At 31 December 2023     
412,864
3,879,139
198,607
148,591
62,500
1,319,428
6,021,129
428,275
6,449,404
Year ended 31 December 2024
Attributable to owners of the parent
Share
capital
Capital
reserve*
Share-
based
payment
reserve*
Foreign
currency
translation
reserve*
Statutory
surplus
reserve*
Retained
earnings*
Total
Non-
controlling
interests
Total
equity
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
(note 31)
(note 32)
(note 32)
(note 32)
(note 32)
(note 32)
At 1 January 2024       
412,864
3,879,139
198,607
148,591
62,500
1,319,428
6,021,129
428,275
6,449,404
Profit for the year       
–
–
–
–
–
498,684
498,684
6,547
505,231
Other comprehensive loss
for the year:
Foreign currency translation 
–
–
–
(289,318)
–
–
(289,318)
(2,806)
(292,124)
Total comprehensive
(loss)/income for the year  
–
–
–
(289,318)
–
498,684
209,366
3,741
213,107
Issuance of shares upon
exercising of share-based
payment scheme (note 33)  
3,118
269,615
(159,824)
–
–
–
112,909
–
112,909
Share-based payments     
–
–
231,647
–
–
–
231,647
–
231,647
Repurchase of restricted
share units cancelled during
the year           
–
–
(3,567)
–
–
–
(3,567)
–
(3,567)
Dividends declared (note 11)  
–
–
–
–
–
(103,995)
(103,995)
–
(103,995)
At 31 December 2024     
415,982
4,148,754
266,863
(140,727)
62,500
1,714,117
6,467,489
432,016
6,899,505
APPENDIX I
ACCOUNTANTS’ REPORT
– I-9 –

<<<PAGE 363>>>
Year ended 31 December 2025
Attributable to owners of the parent
Share
capital
Capital
reserve*
Share-
based
payment
reserve*
Foreign
currency
translation
reserve*
Statutory
surplus
reserve*
Retained
earnings*
Total
Non-
controlling
interests
Total
equity
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
(note 31)
(note 32)
(note 32)
(note 32)
(note 32)
(note 32)
At 1 January 2025
     
415,982
4,148,754
266,863
(140,727)
62,500
1,714,117
6,467,489
432,016
6,899,505
Profit for the year       
–
–
–
–
–
1,423,298
1,423,298
74,473
1,497,771
Other comprehensive income for
the year:
Foreign currency translation 
–
–
–
82,114
–
–
82,114
882
82,996
Total comprehensive income for
the year
         
–
–
–
82,114
–
1,423,298
1,505,412
75,355
1,580,767
Issuance of shares upon
exercising of share-based
payment scheme (note 33)  
3,163
257,886
(147,250)
–
–
–
113,799
–
113,799
Share-based payments     
–
–
91,481
–
–
–
91,481
–
91,481
Acquisition of non-controlling
interests
         
–
(323,887)
–
–
–
–
(323,887)
–
(323,887)
Transfer from retained
earnings
         
–
–
–
–
2,066
(2,066)
–
–
–
At 31 December 2025     
419,145
4,082,753
211,094
(58,613)
64,566
3,135,349
7,854,294
507,371
8,361,665
Period ended 30 April 2025
Attributable to owners of the parent
Share
capital
Capital
reserve*
Share-
based
payment
reserve*
Foreign
currency
translation
reserve*
Statutory
surplus
reserve*
Retained
earnings*
Total
Non-
controlling
interests
Total
equity
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
(note 31)
(note 32)
(note 32)
(note 32)
(note 32)
(note 32)
At 1 January 2025       
415,982
4,148,754
266,863
(140,727)
62,500
1,714,117
6,467,489
432,016
6,899,505
Profit for the period      
–
–
–
–
–
(165,985)
(165,985)
16,763
(149,222)
Other comprehensive income for
the period:
Foreign currency translation  
–
–
–
137,597
–
–
137,597
970
138,567
Total comprehensive income for
the period          
–
–
–
137,597
–
(165,985)
(28,388)
17,733
(10,655)
Share-based payments     
–
–
44,496
–
–
–
44,496
–
44,496
At 30 April 2025 (unaudited)  
415,982
4,148,754
311,359
(3,130)
62,500
1,548,132
6,483,597
449,749
6,933,346
APPENDIX I
ACCOUNTANTS’ REPORT
– I-10 –

<<<PAGE 364>>>
Period ended 30 April 2026
Attributable to owners of the parent
Share
capital
Capital
reserve*
Share-
based
payment
reserve*
Foreign
currency
translation
reserve*
Statutory
surplus
reserve*
Retained
earnings*
Total
Non-
controlling
interests
Total
equity
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
(note 31)
(note 32)
(note 32)
(note 32)
(note 32)
(note 32)
At 1 January 2026       
419,145
4,082,753
211,094
(58,613)
64,566
3,135,349
7,854,294
507,371
8,361,665
Profit for the period      
–
–
–
–
–
6,300,282
6,300,282
126,881
6,427,163
Other comprehensive income for
the period:
Foreign currency translation  
–
–
–
(7,690)
–
–
(7,690)
3,134
(4,556)
Total comprehensive income for
the period          
–
–
–
(7,690)
–
6,300,282
6,292,592
130,015
6,422,607
Issuance of shares upon
exercising of share-based
payment scheme
     
–
(6,409)
–
–
–
–
(6,409)
6,409
–
Share-based payments     
–
–
20,950
–
–
–
20,950
–
20,950
Acquisition of non-controlling
interests           
–
433,707
–
–
–
–
433,707
(428,666)
5,041
Transfer from retained earnings 
–
–
–
–
64,824
(64,824)
–
–
–
At 30 April 2026       
419,145
4,510,051
232,044
(66,303)
129,390
9,370,807 14,595,134
215,129 14,810,263
*
These
reserve
accounts
represent
the
total
reserves
of
RMB5,608,265,000,
RMB6,051,507,000,
RMB7,435,149,000, RMB6,067,615,000, RMB14,175,989,000 in the consolidated statements of financial
position as at 31 December 2023, 2024, 2025 and 30 April 2025 and 2026, respectively.
APPENDIX I
ACCOUNTANTS’ REPORT
– I-11 –

<<<PAGE 365>>>
CONSOLIDATED STATEMENTS OF CASH FLOWS
Year ended 31 December
Four months ended 30 April
Notes
2023
2024
2025
2025
2026
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
(Unaudited)
CASH FLOWS FROM
OPERATING ACTIVITIES
(Loss)/profit before tax      
(1,058,278)
589,656
1,744,965
(145,837)
7,725,195
Adjustments for:
Bank interest income       
5
(34,084)
(16,874)
(19,081)
(4,441)
(4,747)
Finance costs            
6
82,150
271,304
230,372
79,869
111,294
Write-down of inventories to net
realisable value         
7
356,363
566,297
313,661
116,935
77,256
Depreciation of property, plant
and equipment          
7, 13
88,848
373,614
348,037
107,089
125,014
Depreciation of right-of-use
assets               
7, 14(a)
15,611
32,275
36,482
12,377
10,981
Amortisation of other intangible
assets               
7, 16
29,943
51,899
60,939
17,279
23,706
Loss/(gain) on disposal of items
of property, plant and
equipment and other
intangible assets         
7
732
(1,474)
(5,259)
(438)
(15,733)
Impairment of trade receivables,
net                 
7
1,141
1,732
749
1,639
2,206
Equity-settled share-based
payment expenses        
33
198,081
232,173
91,481
44,496
20,950
(Gain)/loss on disposal of
financial assets/liabilities, net 
(71)
(33,013)
56,434
11,880
60,703
Dividend income received from
an equity investment
measured at fair value through
profit or loss           
5
(70)
(210)
(193)
–
–
Fair value gains on financial
assets at fair value through
profit or loss, net        
(39,168)
(306,765)
(178,258)
15,771
(112,483)
Gain on deemed disposal of
investment in an associate   
5
–
(14,095)
–
–
–
Share of (profit)/loss of
associates             
(371)
266
225
–
35
(359,173)
1,746,785
2,680,554
256,619
8,024,377
APPENDIX I
ACCOUNTANTS’ REPORT
– I-12 –

<<<PAGE 366>>>
Year ended 31 December
Four months ended 30 April
Notes
2023
2024
2025
2025
2026
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
(Unaudited)
Increase in inventories      
(2,277,880)
(2,506,285)
(4,158,253)
(455,044)
(9,743,197)
(Increase)/decrease in restricted
cash                
(9,461)
7,866
1,040
(11,527)
770
Increase in trade and bill
receivables            
(231,694)
(328,054)
(369,480)
(322,859)
(1,604,681)
(Increase)/decrease in receivable
financing             
–
–
(4,434)
–
2,373
(Increase)/decrease in
prepayments, other receivables
and other assets         
(333,354)
(371,654)
(694,010)
213,755
(1,113,559)
Increase/(decrease) in trade
payables              
346,785
(6,822)
876,187
276,792
525,207
Increase in contract liabilities  
50,237
28,959
259,832
227,813
1,382,078
Increase/(decrease) in other
payables and accruals     
134,772
241,014
344,471
(152,346)
(160,642)
Increase in deferred income   
10,226
6,070
14,613
7,789
(4,452)
Increase in provision       
5,880
14,822
23,876
51,964
17,074
Cash used in operations      
(2,663,662)
(1,167,299)
(1,025,604)
92,956
(2,674,652)
Interest received          
34,084
16,874
19,081
4,441
4,747
Income tax paid          
(168,822)
(39,317)
(194,679)
(7,536)
(277,609)
Net cash flows (used)/from in
operating activities       
(2,798,400)
(1,189,742)
(1,201,202)
89,861
(2,947,514)
CASH FLOWS FROM
INVESTING ACTIVITIES
Purchases of items of property,
plant and equipment      
(422,966)
(888,713)
(744,324)
(235,609)
(172,976)
Purchase of intangible assets  
(76,021)
(54,833)
(100,448)
(9,195)
(47,815)
Purchases of financial assets at
fair value through profit or
loss                 
(590,000)
(1,006,725)
(692,107)
(282,190)
(442,559)
Purchase of equity in an
associate             
–
(30,000)
(348)
–
–
Proceeds from disposal of items
of property, plant and
equipment and other
intangible assets         
1
7,224
14,114
7,383
15,428
Proceeds from disposal of
finance products         
1,150,000
845,874
819,661
404,098
476,567
Investment income/(loss) from
financial assets at fair value
through profit or loss      
4,705
33,219
(55,855)
(11,880)
(60,703)
Acquisition of subsidiaries    
34
(1,727,178)
(8,037)
(208,613)
–
–
Net cash flows used in investing
activities             
(1,661,459)
(1,101,991)
(967,920)
(127,393)
(232,058)
APPENDIX I
ACCOUNTANTS’ REPORT
– I-13 –

<<<PAGE 367>>>
Year ended 31 December
Four months ended 30 April
Notes
2023
2024
2025
2025
2026
RMB’000
RMB’000
RMB’000
RMB’000
RMB’000
(Unaudited)
CASH FLOWS FROM
FINANCING ACTIVITIES
New bank and other borrowings
6,114,978
7,949,040
9,878,402
2,106,274
7,953,704
Repayment of bank and other
borrowings            
(2,301,614)
(5,527,600)
(7,076,456)
(1,580,996)
(2,343,503)
Cash received under the
subsidiary’s employee stock
ownership plan
        
–
–
7,102
–
12,970
Acquisition of non-controlling
interests              
–
–
–
–
(320,612)
Payments of lease liabilities   
14(b)
(13,211)
(25,494)
(34,794)
(11,715)
(10,921)
Share issue expenses       
(6,950)
–
(28,623)
(20,476)
(10,240)
Issuance of shares upon
exercising of the share-based
payment scheme         
–
112,909
113,799
86,485
142,466
Repurchase of restricted share
units cancelled during the
year/period            
–
(1,424)
–
–
–
Dividends paid           
11
–
(103,995)
–
–
–
Interest paid             
(75,335)
(262,694)
(234,634)
(68,748)
(90,414)
Net cash flows from financing
activities             
3,717,868
2,140,742
2,624,796
510,824
5,333,450
NET (DECREASE)/INCREASE
IN CASH AND CASH
EQUIVALENTS         
(741,991)
(150,991)
455,674
473,292
2,153,878
Cash and cash equivalents at
beginning of year/period    
1,908,239
1,200,523
1,014,411
1,014,411
1,468,811
Effect of foreign exchange rate
changes, net           
34,275
(35,121)
(1,274)
3,896
(14,920)
CASH AND CASH
EQUIVALENTS AT END OF
YEAR/PERIOD         
24
1,200,523
1,014,411
1,468,811
1,491,599
3,607,769
ANALYSIS OF BALANCES OF
CASH AND CASH
EQUIVALENTS
Cash and bank balances     
24
1,218,949
1,024,971
1,478,331
1,513,686
3,616,519
Less: Restricted deposits     
(18,426)
(10,560)
(9,520)
(22,087)
(8,750)
Cash and cash equivalents as
stated in the consolidated
statements of financial
position              
1,200,523
1,014,411
1,468,811
1,491,599
3,607,769
APPENDIX I
ACCOUNTANTS’ REPORT
– I-14 –

<<<PAGE 368>>>
STATEMENTS OF FINANCIAL POSITION OF THE COMPANY
As at 31 December
As at
30 April
Notes
2023
2024
2025
2026
RMB’000
RMB’000
RMB’000
RMB’000
NON-CURRENT ASSETS
Investments in subsidiaries      
42
2,284,382
2,515,432
2,590,885
2,608,710
Property, plant and equipment    
13
15,063
22,995
22,305
23,243
Right-of-use assets            
14
–
14,280
10,348
9,037
Other intangible assets         
16
9,602
8,742
14,814
15,623
Deferred tax assets            
18
10,332
36,609
46,815
8,696
Financial assets at fair value
through profit or loss         
23
10,870
5,250
21,449
25,341
Prepayments, other receivables and
other assets                
22
5,534
9,526
8,597
9,029
Total non-current assets         
2,335,783
2,612,834
2,715,213
2,699,679
CURRENT ASSETS
Inventories                  
19
1,022,694
955,833
693,170
1,398,962
Trade and bills receivables      
20
1,245,071
2,718,710
1,493,435
2,862,845
Prepayments, other receivables and
other assets                
22
3,442,986
6,173,015
8,322,296 10,956,231
Financial assets at fair value
through profit or loss         
23
–
727
–
–
Pledged deposits              
24
–
–
–
154
Cash and cash equivalents       
24
195,248
298,183
470,252
570,603
Total current assets            
5,905,999 10,146,468 10,979,153 15,788,795
CURRENT LIABILITIES
Trade and bills payables        
25
159,789
1,951,245
1,383,512
2,043,052
Other payables and accruals     
26
68,810
319,374
273,874
640,880
Contract liabilities             
28
2,443
1,513
53,257
294,000
Interest-bearing bank borrowings  
27
1,175,866
3,120,382
2,967,586
2,797,577
Tax payables                 
1,990
–
–
64,275
Lease liabilities               
14
–
4,076
4,440
4,315
Total current liabilities         
1,408,898
5,396,590
4,682,669
5,844,099
NET CURRENT ASSETS       
4,497,101
4,749,878
6,296,484
9,944,696
TOTAL ASSETS LESS CURRENT
LIABILITIES               
6,832,884
7,362,712
9,011,697 12,644,375
NON-CURRENT LIABILITIES
Interest-bearing bank borrowings  
27
1,975,800
2,284,700
3,708,248
6,672,998
Lease liabilities               
14
–
11,911
7,471
6,136
Deferred tax liabilities          
18
895
134
4,073
5,043
Total non-current liabilities      
1,976,695
2,296,745
3,719,792
6,684,177
Net assets                   
4,856,189
5,065,967
5,291,905
5,960,198
EQUITY
Share capital                 
31
412,864
415,982
419,145
419,145
Reserves                    
32
4,443,325
4,649,985
4,872,760
5,541,053
Total equity                  
4,856,189
5,065,967
5,291,905
5,960,198
APPENDIX I
ACCOUNTANTS’ REPORT
– I-15 –

<<<PAGE 369>>>
II
NOTES TO THE HISTORICAL FINANCIAL INFORMATION
1.
CORPORATE INFORMATION
The Company is a joint stock company with limited liability incorporated in Shenzhen, the People’s Republic
of China (the “PRC”) on 27 April 1999. With the approval of the China Securities Regulatory Commission, the
Company completed its initial public offering and was listed on the ChiNext market of the Shenzhen Stock Exchange
(stock code: 301308) on 5 August 2022. The registered office address of the Company is Floor 20, 22, 23, B Tower,
Horoy Qianhai Finance Centre Centre Phase II, No. 5059, Tinghai Avenue, Qianhai, Shenzhen, PRC.
During the Relevant Periods, the Company and its subsidiaries (collectively, the “Group”) were principally
engaged in the research and development, design, packaging and testing, back-end manufacturing (SMT and
assembly) and sales of semiconductor memory application products.
As at the date of this report, the Company had direct and indirect interests in its subsidiaries, all of which are
private limited liability companies, the particulars of the Company’s principal subsidiaries are set out below:
Name
Notes
Place and date of
registration and
place of operations
Registered share
capital
Percentage of
equity attributable
to the Company
Principal activities
Direct
Indirect
Zhongshan Longsys Electronics
Co., Limited*
(中山市江波龍電子有限公
司)              
(a)
Chinese
Mainland, 12
October 2015
RMB850,000,000
100%
– Research and
development,
testing and sales
of storage
products
Lexar Electronics (Shenzhen)
Co., Ltd.*
(雷克沙電子(深圳)有限公司) 
(a)
Chinese
Mainland, 24
November
2015
RMB30,000,000
100%
– Sales of storage
products
MESTOR Electronics (HK)
Co., Limited (Formerly
known as: Damai Electronics
(HK) Limited)        
(b)
Hong Kong,
10 May 2016
HKD10,000
–
100% Sales and
procurement of
storage products
Longsys Electronics (HK)
Co., Limited (江波龍電子(香
港)有限公司         
(b)
Hong Kong,
19 April 2013
HKD62,500,000
–
100% Sales and
procurement of
storage products
Lexar Co., Limited （雷克沙有
限公司）          
(b)
Hong Kong,
14 September
2017
HKD1,000,000
–
100% Sales of storage
products
Shanghai Longsys Digital
Technology Co., Limited*
(上海江波龍數字技術有限公
司)              
(c)
Chinese
Mainland, 3
July 2020
RMB736,000,000
–
100% Research and
development of
storage products
Shanghai Longsys Storage
Technology Co., Limited*
(上海江波龍存儲技術有限公
司)              
(c)
Chinese
Mainland, 29
May 2020
RMB1,136,000,000
100%
– Procurement of
raw materials
Zilia Technologies Indústria e
Comércio de Componentes
Eletrônicos Ltda. (Formerly
known as: SMART Modular
Technologies do Brasil-
Indústria e Comércio de
Componentes Ltda.) (“Zilia
Eletrônicos”)**        
(d)
Brazil,
19 October
2009
BRL479,815,000
–
100% Back-end
manufacturing
and sales of
universal
storage products
APPENDIX I
ACCOUNTANTS’ REPORT
– I-16 –

<<<PAGE 106 起已省略：超出 share_structure 字符上限；请人工复核覆盖范围>>>



## 价格区间（T–U）

- `col_T` = Maximum Offer Price (type=number unit=HKD_per_share missing=NaN)
- `col_U` = Minimum Offer Price (type=number unit=HKD_per_share missing=NaN)

### 原文切片：价格区间（T–U）


<<<PAGE 1>>>
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators, 
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Stock Code : 09976
(A joint stock company incorporated in the People’s Republic of China with limited liability)
深圳市江波龍電子股份有限公司
Shenzhen Longsys Electronics Co., Ltd.
G L O B A L 
O F F E R I N G

<<<PAGE 2>>>
If you are in any doubt about any of the contents in this document, you should obtain independent professional advice.
Shenzhen Longsys Electronics Co., Ltd.
深圳市江波龍電子股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the
Global Offering
:
26,077,800 H Shares (subject to the
Offer Size Adjustment Option and the
Over-allotment Option)
Number of Hong Kong Offer Shares
:
2,607,800 H Shares (subject to
reallocation)
Number of International Offer Shares
:
23,470,000 H Shares (subject to
reallocation, the Offer Size Adjustment
Option and the Over-allotment Option)
Maximum Offer Price
:
HK$240.60 per H Share plus brokerage
of 1%, SFC transaction levy of
0.0027%, Stock Exchange trading fee
of 0.00565% and AFRC transaction
levy of 0.00015% (payable in full on
application in Hong Kong dollars and
subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
09976
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators,
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this
document, make no representation as to its accuracy or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any part
of the contents of this document.
A copy of this document, having attached thereto the documents specified in “Documents Delivered to the Registrar of Companies and Available on Display” in Appendix VII, has been registered
by the Registrar of Companies in Hong Kong as required by Section 342C of the Companies (Winding Up and Miscellaneous Provisions) Ordinance (Chapter 32 of the Laws of Hong Kong). The
Securities and Futures Commission of Hong Kong and the Registrar of Companies in Hong Kong take no responsibility for the contents of this document or any other document referred to above.
The Offer Price is expected to be fixed by agreement between the Sponsor-Overall Coordinators (for themselves and on behalf of the Underwriters) and us on or before Friday, September 4, 2026
(Hong Kong time). If, for any reason, the Offer Price is not agreed by 12:00 noon on Friday, September 4, 2026 (Hong Kong time) between the Sponsor-Overall Coordinators (for themselves and
on behalf of the Underwriters) and us, the Global Offering will not proceed and will lapse. The Offer Price will be no more than HK$240.60 per Offer Share unless otherwise announced.
The Sponsor-Overall Coordinators (for themselves and on behalf of the Underwriters) may, where considered appropriate and with our consent, reduce the number of Offer Shares being
offered under the Global Offering and/or the maximum Offer Price below that stated in this document at any time on or prior to the morning of the last day for lodging applications under
the Hong Kong Public Offering. Please refer to the sections headed “Structure of the Global Offering” and “How to Apply for Hong Kong Offer Shares” for further details.
The obligations of the Hong Kong Underwriters under the Hong Kong Underwriting Agreement are subject to termination by the Sponsor-Overall Coordinators (for themselves and on behalf of the
Hong Kong Underwriters) if certain grounds arise prior to 8:00 a.m. on the Listing Date. Please refer to the section headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong
Public Offering— Grounds for Termination” for further details.
Prior to making an investment decision, prospective investors should consider carefully all of the information set out in this document, including the risk factors set out in the section headed “Risk
Factors.”
The Offer Shares have not been and will not be registered under the U.S. Securities Act or any state securities laws of the United States and may not be offered or sold within or to the United States,
or to or for the account or benefit of any U.S. person (as defined in Regulation S), except in transactions exempt from, or not subject to, the registration requirements of the U.S. Securities Act.
The Offer Shares are being offered and sold (i) solely to QIBs pursuant to an exemption from registration under Rule 144A of the U.S. Securities Act and (ii) outside the United States in offshore
transactions in accordance with Regulation S.
IMPORTANT
August 31, 2026

<<<PAGE 3>>>
IMPORTANT NOTICE TO INVESTORS:
FULLY ELECTRONIC APPLICATION PROCESS
We have adopted a fully electronic application process for the Hong Kong
Public Offering. We will not provide printed copies of this prospectus in relation to
the Hong Kong Public Offering.
This prospectus is available at the website of the Stock Exchange at
www.hkexnews.hk
under
the
“HKEXnews
>
New
Listings
>
New
Listing
Information” section, and our website at https://www.longsys.com. You may
download and print from these website addresses if you want a printed copy of this
prospectus.
To apply for the Hong Kong Offer Shares, you may:
(1)
apply online via the White Form eIPO service at www.eipo.com.hk; or
(2)
apply electronically through the HKSCC EIPO channel and cause HKSCC
Nominees to apply on your behalf by instructing your broker or custodian
who is an HKSCC Participant to give electronic application instructions via
HKSCC’s FINI system to apply for the Hong Kong Offer Shares on your
behalf.
We will not provide any physical channels to accept any application for the Hong
Kong Offer Shares by the public. The contents of the electronic version of this
prospectus are identical to the printed prospectus as registered with the Registrar of
Companies in Hong Kong pursuant to Section 342C of the Companies (Winding Up and
Miscellaneous Provisions) Ordinance.
If you are an intermediary, broker or agent, please remind your customers, clients
or principals, as applicable, that this prospectus is available online at the website
addresses stated above.
IMPORTANT
– ii –

<<<PAGE 4>>>
Please refer to the section headed “How to Apply for Hong Kong Offer Shares” in
this prospectus for further details on the procedures through which you can apply for the
Hong Kong Offer Shares electronically.
Your application through the White Form eIPO service or the HKSCC EIPO
channel must be made for a minimum of 50 Hong Kong Offer Shares and in multiples
of that number of Hong Kong Offer Shares as set out in the table below. No application
for any other number of Hong Kong Offer Shares will be considered and such an
application is liable to be rejected.
If you are applying through the White Form eIPO service, you may refer to the
table below for the amount payable for the number of H Shares you have selected. You
must pay the respective amount payable on application in full upon application for Hong
Kong Offer Shares.
If you are applying through the HKSCC EIPO channel, your broker or custodian
may require you to pre-fund your application in such amount as determined by the broker
or custodian, based on the applicable laws and regulations in Hong Kong. You are
responsible for complying with any such pre-funding requirement imposed by your
broker or custodian with respect to the Hong Kong Offer Shares you applied for.
No. of
Hong Kong
Offer
Shares
applied for
Amount
payable(2) on
application
No. of
Hong Kong
Offer
Shares
applied for
Amount
payable(2) on
application
No. of
Hong Kong
Offer
Shares
applied for
Amount
payable(2) on
application
No. of
Hong Kong
Offer
Shares
applied for
Amount
payable(2) on
application
HK$
HK$
HK$
HK$
50
12,151.32
600
145,815.88
7,000
1,701,185.16
80,000
19,442,116.08
100
24,302.65
700
170,118.52
8,000
1,944,211.61
90,000
21,872,380.59
150
36,453.96
800
194,421.17
9,000
2,187,238.07
100,000
24,302,645.10
200
48,605.29
900
218,723.80
10,000
2,430,264.51
200,000
48,605,290.20
250
60,756.61
1,000
243,026.45
20,000
4,860,529.02
300,000
72,907,935.30
300
72,907.94
2,000
486,052.90
30,000
7,290,793.54
400,000
97,210,580.40
350
85,059.26
3,000
729,079.35
40,000
9,721,058.05
500,000
121,513,225.50
400
97,210.58
4,000
972,105.80
50,000
12,151,322.56
750,000
182,269,838.26
450
109,361.90
5,000
1,215,132.25
60,000
14,581,587.05
1,000,000
243,026,451.00
500
121,513.23
6,000
1,458,158.71
70,000
17,011,851.56
1,303,900(1)
316,882,189.47
(1)
Maximum number of Hong Kong Offer Share you may apply for.
(2)
The amount payable is inclusive of brokerage, SFC transaction levy, the Stock Exchange trading fee
and AFRC transaction levy. If your application is successful, brokerage will be paid to the Exchange
Participants (as defined in the Listing Rules) and the SFC transaction levy, the Stock Exchange trading
fee and AFRC transaction levy are paid to the Stock Exchange (in the case of the SFC transaction levy,
collected by the Stock Exchange on behalf of the SFC; and in the case of the AFRC transaction levy,
collected by the Stock Exchange on behalf of the AFRC).
IMPORTANT
– iii –

<<<PAGE 5>>>
If there is any change in the following expected timetable of the Hong Kong Public
Offering, our Company will issue an announcement to be published on the website of the
Stock
Exchange
at
www.hkexnews.hk
and
the
website
of
our
Company
at
www.longsys.com.
Date(1)
Hong Kong Public Offering commences . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .9:00 a.m. on
Monday, August 31, 2026
Latest time to complete electronic applications under
White Form eIPO service through the designated
website at www.eipo.com.hk(2) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .11:30 a.m. on
Thursday, September 3, 2026
Application lists of the Hong Kong Public Offering open(3)
. . . . . . . . . . . . . .11:45 a.m. on
Thursday, September 3, 2026
Latest time to (a) complete payment of White Form eIPO
applications by effecting internet banking transfer(s) or
PPS payment transfer(s) and (b) give electronic
application instructions to HKSCC(4) . . . . . . . . . . . . . . . . . . . . . . . . . . . .12:00 noon on
Thursday, September 3, 2026
If you are instructing your broker or custodian who is a HKSCC Participant will submit
electronic application instructions on your behalf through HKSCC’s FINI system in
accordance with your instruction, you are advised to contact your broker or custodian for the
earliest and latest time for giving such instructions, as this may vary by broker or custodian.
Application lists of the Hong Kong Public Offering close(3) . . . . . . . . . . . . . .12:00 noon on
Thursday, September 3, 2026
Expected Price Determination Date(5) . . . . . . . . . . . . . . . . . . . . . . . . . . . .by 12:00 noon on
Friday, September 4, 2026
Announcement of the final Offer Price, the results of applications in
the Hong Kong Public Offering, the level of indications of interest
in the International Offering and the basis of allocation of the
Hong Kong Offer Shares under the Hong Kong Public Offering
to be published on the website of the Stock Exchange at
www.hkexnews.hk and the website of
our Company at www.longsys.com(6) . . . . . . . . . . . . . . . . . . .no later than 11:00 p.m. on
Monday, September 7, 2026
EXPECTED TIMETABLE(1)
– iv –

<<<PAGE 6>>>
Results of allocations in the Hong Kong Public Offering (with successful applicants’
identification document numbers, where appropriate) to be available through a variety of
channels, including:
(1)
A full announcement of the Hong Kong Public Offering
to be published on the website of the Stock Exchange at
www.hkexnews.hk and the website of
our Company at www.longsys.com(6) . . . . . . . . . . . . . no later than 11:00 p.m. on
Monday, September 7, 2026
(2)
Results of allocations in the Hong Kong Public Offering
will be available at www.iporesults.com.hk (alternatively:
www.eipo.com.hk/eIPOAllotment) with a “search by ID”
function on a 24-hour basis from . . . . . . . . . . . . . . . . . . . . . . . . . . .11:00 p.m. on
Monday, September 7, 2026 to
12:00 midnight on
Sunday, September 13, 2026
(3)
Allocation results telephone enquiry by
calling +852 2862 8555. . . . . . . . . . . . . . . . . . . .between 9:00 a.m. and 6:00 p.m.
on Tuesday, September 8, 2026,
Wednesday, September 9, 2026,
Thursday, September 10, 2026 and
Friday, September 11, 2026
Despatch of H Share certificates in respect of wholly or
partially successful applications, or deposit of
H Share certificate into CCASS pursuant to
Hong Kong Public Offering, on or before(7)(9) . . . . . . . . . . . .Monday, September 7, 2026
Dispatch/collection of refund cheques and White Form
e-Refund payment instructions in respect of (i) wholly or
partially successful applications (if applicable) and
(ii) wholly or partially unsuccessful applications pursuant
to the Hong Kong Public Offering on or before(8)(9) . . . . . . . Tuesday, September 8, 2026
Dealings in H Shares on the Stock Exchange
expected to commence at . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9:00 a.m. on
Tuesday, September 8, 2026
EXPECTED TIMETABLE(1)
– v –

<<<PAGE 8>>>
IMPORTANT NOTICE TO PROSPECTIVE INVESTORS
This document is issued by us solely in connection with the Hong Kong Public
Offering and the Hong Kong Offer Shares and does not constitute an offer to sell or a
solicitation of an offer to buy any security other than the Hong Kong Offer Shares by this
document pursuant to the Hong Kong Public Offering. This document may not be used for
the purpose of making, and does not constitute, an offer or invitation in any other
jurisdiction or in any other circumstances. No action has been taken to permit a public
offering of the Hong Kong Offer Shares in any jurisdiction other than Hong Kong and no
action has been taken to permit the distribution of this document in any jurisdiction other
than Hong Kong. The distribution of this document for purposes of a public offering and
the offering and sale of the Hong Kong Offer Shares in other jurisdictions are subject to
restrictions and may not be made except as permitted under the applicable securities laws
of such jurisdictions pursuant to registration with or authorization by the relevant
securities regulatory authorities or an exemption therefrom.
You should rely only on the information contained in this document to make your
investment decision. The Hong Kong Public Offering is made solely on the basis of the
information contained and the representations made in this document. We have not
authorized anyone to provide you with information that is different from what is
contained in this document. Any information or representation not contained nor made in
this document must not be relied on by you as having been authorized by us, any of the
Joint Sponsors, Sponsor-Overall Coordinators, the Overall Coordinators, the Capital
Market Intermediaries, the Joint Global Coordinators, the Joint Bookrunners, the Joint
Lead Managers, any of the Underwriters, any of our or their respective directors,
officers, employees, agents, or representatives of any of them or any other parties
involved in the Global Offering.
Page
EXPECTED TIMETABLE. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
iv
CONTENTS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
vii
SUMMARY . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
1
DEFINITIONS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
28
GLOSSARY OF TECHNICAL TERMS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
40
FORWARD-LOOKING STATEMENTS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
47
RISK FACTORS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
48
WAIVERS AND EXEMPTION . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
84
INFORMATION ABOUT THIS DOCUMENT AND THE GLOBAL OFFERING.
97
CONTENTS
– vii –

<<<PAGE 9>>>
DIRECTORS AND PARTIES INVOLVED IN THE GLOBAL OFFERING . . . . .
100
CORPORATE INFORMATION . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
106
INDUSTRY OVERVIEW . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
108
REGULATORY OVERVIEW . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
119
HISTORY AND CORPORATE STRUCTURE . . . . . . . . . . . . . . . . . . . . . . . . . . . .
145
BUSINESS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
164
FINANCIAL INFORMATION. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
227
RELATIONSHIP WITH OUR CONTROLLING SHAREHOLDERS . . . . . . . . . .
283
CONNECTED TRANSACTION . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
285
SHARE CAPITAL . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
286
SUBSTANTIAL SHAREHOLDERS. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
289
CORNERSTONE INVESTORS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
290
DIRECTORS AND SENIOR MANAGEMENT . . . . . . . . . . . . . . . . . . . . . . . . . . . .
301
FUTURE PLANS AND USE OF PROCEEDS. . . . . . . . . . . . . . . . . . . . . . . . . . . . .
314
UNDERWRITING . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
317
STRUCTURE OF THE GLOBAL OFFERING. . . . . . . . . . . . . . . . . . . . . . . . . . . .
325
HOW TO APPLY FOR HONG KONG OFFER SHARES . . . . . . . . . . . . . . . . . . .
333
APPENDIX I
ACCOUNTANTS’ REPORT . . . . . . . . . . . . . . . . . . . . . . . .
I-1
APPENDIX IA
UNAUDITED INTERIM CONDENSED
CONSOLIDATED FINANCIAL INFORMATION. . . . . .
IA-1
APPENDIX II
UNAUDITED PRO FORMA FINANCIAL
INFORMATION . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
II-1
APPENDIX III
TAXATION AND FOREIGN EXCHANGE. . . . . . . . . . . . .
III-1
APPENDIX IV
SUMMARY OF PRINCIPAL LEGAL AND
REGULATORY PROVISIONS. . . . . . . . . . . . . . . . . . . . .
IV-1
APPENDIX V
SUMMARY OF THE ARTICLES OF ASSOCIATION . . . .
V-1
APPENDIX VI
STATUTORY AND GENERAL INFORMATION . . . . . . . .
VI-1
APPENDIX VII
DOCUMENTS DELIVERED TO THE REGISTRAR OF
COMPANIES AND AVAILABLE ON DISPLAY . . . . . . .
VII-1
CONTENTS
– viii –

<<<PAGE 10>>>
This summary aims to give you an overview of the information contained in this
prospectus. As this is a summary, it does not contain all the information that may be
important to you and is qualified in its entirety by, and should be read in conjunction with,
the full text of this prospectus. You should read the entire document before you decide to
invest in the Offer Shares. There are risks associated with any investment. Some of the
particular risks in investing in the Offer Shares are set out in the section headed “Risk
Factors” in this prospectus. You should read that section carefully before you decide to
invest in the Offer Shares. Various expressions used in this section are defined in the
sections headed “Definitions” and “Glossary of Technical Terms” in this prospectus.
Overview
We are a branded independent semiconductor memory product enterprise. We procure memory
wafers and controller chips from IDMs and controller chip suppliers and do not engage in wafer
fabrication. Based on our capabilities including controller and memory chip design, firmware
development, back-end manufacturing (including system-level packaging, testing and assembly),
we design, develop, back-end manufacture and sell a comprehensive portfolio of memory products
for consumer, enterprise and industrial applications. We have a market share of 1.2% in the global
memory product market in 2025, representing a meaningful position for an independent memory
enterprise given the large scale of the industry. According to CIC, we are the ninth largest memory
product enterprise worldwide, the second largest independent semiconductor memory product
enterprise worldwide among more than 100 market players and the largest independent memory
product enterprise in China among more than 30 market players, in terms of revenue from memory
products in 2025. We currently own and operate three primary brands — FORESEE, Zilia and Lexar
— each focusing on different customer segments and enjoying strong recognition in its respective
market. These achievements, together with the scale of our global presence and the strength of our
brand and product portfolio, underscoring our pivotal role within the broader semiconductor
memory industry.
Founded in 1999, we have been dedicated to the semiconductor memory industry for over two
decades. Our founding team, led by our Chairman Mr. Cai, recognized the significant global market
potential for semiconductor memory early on. Through persistent dedication and strategic
development, we expanded from trading semiconductor memory products to developing our own
memory products back-end manufacturing expertise, and further into core competencies such as
controller and memory chip design, firmware development, packaging and testing capacities. These
capabilities along the semiconductor memory value chain have allowed us to establish a portfolio
of high-quality, high-performance products and have earned us widespread recognition from
business partners and users alike.
Our steadfast focus on the semiconductor memory product industry and consistent innovation
have resulted in strong brand recognition, establishing us as a key player in the memory market. Our
brands: FORESEE (primarily serves the B2B market), Zilia (primarily serves the Latin American
B2B market) and Lexar (primarily serves B2C market), collectively driving balanced growth in both
enterprise and consumer markets.
•
FORESEE, which we have developed organically for more than a decade, enjoys a
strong reputation and significant first-mover advantages, particularly in edge devices
such as mobile phone and computers, as well as the automotive sector.
•
Zilia
was
introduced
in
2023
after
we
acquired
SMART
Brazil,
a
Brazilian
semiconductor memory company of SMART Global.
•
Lexar is a global premium brand we acquired in 2017. To date, Lexar-branded products
have been sold in over 60 countries and regions and have received numerous
international awards. Lexar primarily targets and serves the B2C memory market such
as photography, videography and gaming.
SUMMARY
– 1 –

<<<PAGE 11 起已省略：超出 price 字符上限；请人工复核覆盖范围>>>



## 发售时间表（CC–CD）

- `col_CC` = Subscription opening date (type=date unit=date missing=NA)
- `col_CD` = Subscription closing date (type=date unit=date missing=NA)

### 原文切片：发售时间表（CC–CD）


<<<PAGE 7>>>
Notes:
(1)
All dates and times refer to Hong Kong local dates and times, except as otherwise stated.
(2)
You will not be permitted to submit your application to the White Form eIPO Service Provider through the
designated website at www.eipo.com.hk after 11:30 a.m. on the last day for submitting applications. If you
have already submitted your application and obtained an application reference number from the designated
website on or before 11:30 a.m., you will be permitted to continue the application process (by completing
payment of application monies) until 12:00 noon on the last day for submitting applications, when the
application lists close.
(3)
If there is a “black” rainstorm warning or a tropical cyclone warning signal number 8 or above and/or Extreme
Conditions in force in Hong Kong at any time between 9:00 a.m. and 12:00 noon on Thursday, September 3,
2026, the application lists will not open or close on that day. See “How to Apply for Hong Kong Offer Shares
— E. Severe Weather Arrangements” in this prospectus.
(4)
Applicants who apply for Hong Kong Offer Shares through HKSCC EIPO channel should see “How to Apply
for Hong Kong Offer Shares — A. Application for Hong Kong Offer Shares — 2. Application Channels” in
this prospectus.
(5)
The Price Determination Date is expected to be on or before Friday, September 4, 2026, and in any event, not
later than 12:00 noon on Friday, September 4, 2026. If, for any reason, the Offer Price is not agreed between
the Sponsor-Overall Coordinators and us by 12:00 noon on Friday, September 4, 2026, the Global Offering will
not proceed and will lapse.
(6)
None of the websites or any of the information contained on the websites forms part of this prospectus.
(7)
H Share certificates for the Offer Shares will become valid evidence of title at 8:00 a.m. on the Listing Date
provided that (i) the Global Offering has become unconditional in all respects and (ii) none of the Underwriting
Agreements have been terminated in accordance with its terms.
(8)
White Form e-Refund payment instructions/refund cheques will be issued in respect of wholly or partially
unsuccessful applications pursuant to the Hong Kong Public Offering. Part of the applicant’s Hong Kong
identity card number or passport number, or, if the application is made by joint applicants, part of the Hong
Kong identity card number or passport number of the first-named applicant, provided by the applicant(s) may
be printed on the refund cheque, if any. Such data would also be transferred to a third party for refund purposes.
Banks may require verification of an applicant’s Hong Kong identity card number or passport number before
encashment of the refund cheque. Inaccurate completion of an applicant’s Hong Kong identity card number or
passport number may invalidate or delay encashment of the refund cheque.
(9)
Applicants who have applied for Hong Kong Offer Shares through HKSCC EIPO channel should refer to the
section headed “How to Apply for Hong Kong Offer Shares — D. Despatch/Collection of Share Certificates
and Refund of Application Monies” in this prospectus for details.
For applicants who apply through the White Form eIPO service and paid the application monies from a single
bank account, White Form e-Refund payment instructions (if any) will be dispatched to their application
payment bank account. For applicants who apply through the White Form eIPO service and used multi-bank
accounts to pay the application monies, refund cheque (if any) will be dispatched to the address specified in
their electronic application instruction to the White Form eIPO Service Provider at their own risk.
Applicants being individuals who are eligible for personal collection may not authorize any other person to
collect on their behalf. If you are a corporate applicant which is eligible for personal collection, your
authorized representative must bear a letter of authorization from your corporation stamped with your
corporation’s chop. Both individuals and authorized representatives must produce evidence of identity
acceptable to our H Share Registrar at the time of collection. Any uncollected H Share certificates and/or
refund cheques will be dispatched by ordinary post, at the applicants’ risk, to the addresses specified in the
relevant applications.
Further information is set out in the sections headed “How to Apply for Hong Kong Offer Shares — D.
Despatch/Collection of Share Certificates and Refund of Application Monies” in this prospectus.
The above expected timetable is a summary only. See the sections headed “Structure of
the Global Offering” and “How to Apply for Hong Kong Offer Shares” in this prospectus for
details of the structure and conditions of the Global Offering, as well as the application
procedures for Hong Kong Public Offering.
EXPECTED TIMETABLE(1)
– vi –

<<<PAGE 8>>>
IMPORTANT NOTICE TO PROSPECTIVE INVESTORS
This document is issued by us solely in connection with the Hong Kong Public
Offering and the Hong Kong Offer Shares and does not constitute an offer to sell or a
solicitation of an offer to buy any security other than the Hong Kong Offer Shares by this
document pursuant to the Hong Kong Public Offering. This document may not be used for
the purpose of making, and does not constitute, an offer or invitation in any other
jurisdiction or in any other circumstances. No action has been taken to permit a public
offering of the Hong Kong Offer Shares in any jurisdiction other than Hong Kong and no
action has been taken to permit the distribution of this document in any jurisdiction other
than Hong Kong. The distribution of this document for purposes of a public offering and
the offering and sale of the Hong Kong Offer Shares in other jurisdictions are subject to
restrictions and may not be made except as permitted under the applicable securities laws
of such jurisdictions pursuant to registration with or authorization by the relevant
securities regulatory authorities or an exemption therefrom.
You should rely only on the information contained in this document to make your
investment decision. The Hong Kong Public Offering is made solely on the basis of the
information contained and the representations made in this document. We have not
authorized anyone to provide you with information that is different from what is
contained in this document. Any information or representation not contained nor made in
this document must not be relied on by you as having been authorized by us, any of the
Joint Sponsors, Sponsor-Overall Coordinators, the Overall Coordinators, the Capital
Market Intermediaries, the Joint Global Coordinators, the Joint Bookrunners, the Joint
Lead Managers, any of the Underwriters, any of our or their respective directors,
officers, employees, agents, or representatives of any of them or any other parties
involved in the Global Offering.
Page
EXPECTED TIMETABLE. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
iv
CONTENTS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
vii
SUMMARY . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
1
DEFINITIONS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
28
GLOSSARY OF TECHNICAL TERMS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
40
FORWARD-LOOKING STATEMENTS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
47
RISK FACTORS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
48
WAIVERS AND EXEMPTION . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
84
INFORMATION ABOUT THIS DOCUMENT AND THE GLOBAL OFFERING.
97
CONTENTS
– vii –

<<<PAGE 9>>>
DIRECTORS AND PARTIES INVOLVED IN THE GLOBAL OFFERING . . . . .
100
CORPORATE INFORMATION . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
106
INDUSTRY OVERVIEW . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
108
REGULATORY OVERVIEW . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
119
HISTORY AND CORPORATE STRUCTURE . . . . . . . . . . . . . . . . . . . . . . . . . . . .
145
BUSINESS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
164
FINANCIAL INFORMATION. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
227
RELATIONSHIP WITH OUR CONTROLLING SHAREHOLDERS . . . . . . . . . .
283
CONNECTED TRANSACTION . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
285
SHARE CAPITAL . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
286
SUBSTANTIAL SHAREHOLDERS. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
289
CORNERSTONE INVESTORS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
290
DIRECTORS AND SENIOR MANAGEMENT . . . . . . . . . . . . . . . . . . . . . . . . . . . .
301
FUTURE PLANS AND USE OF PROCEEDS. . . . . . . . . . . . . . . . . . . . . . . . . . . . .
314
UNDERWRITING . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
317
STRUCTURE OF THE GLOBAL OFFERING. . . . . . . . . . . . . . . . . . . . . . . . . . . .
325
HOW TO APPLY FOR HONG KONG OFFER SHARES . . . . . . . . . . . . . . . . . . .
333
APPENDIX I
ACCOUNTANTS’ REPORT . . . . . . . . . . . . . . . . . . . . . . . .
I-1
APPENDIX IA
UNAUDITED INTERIM CONDENSED
CONSOLIDATED FINANCIAL INFORMATION. . . . . .
IA-1
APPENDIX II
UNAUDITED PRO FORMA FINANCIAL
INFORMATION . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
II-1
APPENDIX III
TAXATION AND FOREIGN EXCHANGE. . . . . . . . . . . . .
III-1
APPENDIX IV
SUMMARY OF PRINCIPAL LEGAL AND
REGULATORY PROVISIONS. . . . . . . . . . . . . . . . . . . . .
IV-1
APPENDIX V
SUMMARY OF THE ARTICLES OF ASSOCIATION . . . .
V-1
APPENDIX VI
STATUTORY AND GENERAL INFORMATION . . . . . . . .
VI-1
APPENDIX VII
DOCUMENTS DELIVERED TO THE REGISTRAR OF
COMPANIES AND AVAILABLE ON DISPLAY . . . . . . .
VII-1
CONTENTS
– viii –

<<<PAGE 10>>>
This summary aims to give you an overview of the information contained in this
prospectus. As this is a summary, it does not contain all the information that may be
important to you and is qualified in its entirety by, and should be read in conjunction with,
the full text of this prospectus. You should read the entire document before you decide to
invest in the Offer Shares. There are risks associated with any investment. Some of the
particular risks in investing in the Offer Shares are set out in the section headed “Risk
Factors” in this prospectus. You should read that section carefully before you decide to
invest in the Offer Shares. Various expressions used in this section are defined in the
sections headed “Definitions” and “Glossary of Technical Terms” in this prospectus.
Overview
We are a branded independent semiconductor memory product enterprise. We procure memory
wafers and controller chips from IDMs and controller chip suppliers and do not engage in wafer
fabrication. Based on our capabilities including controller and memory chip design, firmware
development, back-end manufacturing (including system-level packaging, testing and assembly),
we design, develop, back-end manufacture and sell a comprehensive portfolio of memory products
for consumer, enterprise and industrial applications. We have a market share of 1.2% in the global
memory product market in 2025, representing a meaningful position for an independent memory
enterprise given the large scale of the industry. According to CIC, we are the ninth largest memory
product enterprise worldwide, the second largest independent semiconductor memory product
enterprise worldwide among more than 100 market players and the largest independent memory
product enterprise in China among more than 30 market players, in terms of revenue from memory
products in 2025. We currently own and operate three primary brands — FORESEE, Zilia and Lexar
— each focusing on different customer segments and enjoying strong recognition in its respective
market. These achievements, together with the scale of our global presence and the strength of our
brand and product portfolio, underscoring our pivotal role within the broader semiconductor
memory industry.
Founded in 1999, we have been dedicated to the semiconductor memory industry for over two
decades. Our founding team, led by our Chairman Mr. Cai, recognized the significant global market
potential for semiconductor memory early on. Through persistent dedication and strategic
development, we expanded from trading semiconductor memory products to developing our own
memory products back-end manufacturing expertise, and further into core competencies such as
controller and memory chip design, firmware development, packaging and testing capacities. These
capabilities along the semiconductor memory value chain have allowed us to establish a portfolio
of high-quality, high-performance products and have earned us widespread recognition from
business partners and users alike.
Our steadfast focus on the semiconductor memory product industry and consistent innovation
have resulted in strong brand recognition, establishing us as a key player in the memory market. Our
brands: FORESEE (primarily serves the B2B market), Zilia (primarily serves the Latin American
B2B market) and Lexar (primarily serves B2C market), collectively driving balanced growth in both
enterprise and consumer markets.
•
FORESEE, which we have developed organically for more than a decade, enjoys a
strong reputation and significant first-mover advantages, particularly in edge devices
such as mobile phone and computers, as well as the automotive sector.
•
Zilia
was
introduced
in
2023
after
we
acquired
SMART
Brazil,
a
Brazilian
semiconductor memory company of SMART Global.
•
Lexar is a global premium brand we acquired in 2017. To date, Lexar-branded products
have been sold in over 60 countries and regions and have received numerous
international awards. Lexar primarily targets and serves the B2C memory market such
as photography, videography and gaming.
SUMMARY
– 1 –

<<<PAGE 11>>>
Our Products and Applications
We design, back-end manufacture and sell a broad range of memory and storage products to
meet diverse customer needs. Our portfolio comprises four major product lines:
•
Embedded storage solutions that integrate memory directly into the main systems of
electronic products such as smartphones, smart wearables, automotive electronics,
tablets and other consumer electronics;
•
SSDs, which are standalone storage devices known for fast data access speeds, high
reliability and ease of replacement, serving servers, computers, data centers and other
applications;
•
Mobile storage products, including USB flash drives, memory cards and portable SSDs,
which primarily support data transfer and backup for consumer storage devices, smart
vehicles and other use cases; and
•
DIMMs, which are circuit boards equipped with DRAM chips for temporary data
processing and program execution in servers, computers, data centers and related
applications.
We currently focus on the sales of consumer grade products. During the Track Record Period,
revenue from consumer-grade products accounted for 94.7%, 92.9%, 89.8% and 88.4% of our
revenue for the years of 2023, 2024 and 2025 and the four months ended April 30, 2026,
respectively, while revenue from non-consumer-grade products, which comprised of both enterprise
grade and industrial grade products, accounted for 5.3%, 7.1%, 10.2% and 11.6% of our revenue for
the same period. Our non-consumer-grade products achieved growth in both absolute amount and
revenue contribution, demonstrating accelerating growth momentum. This reflects our diversified
product portfolio and technological capabilities in addressing diverse market needs, as well as our
differentiated competitive strategy relative to memory IDMs.
Our memory and storage products have applications in various segments, covering both
consumer grade and non-consumer grade products. Our consumer grade products are primarily
designed for use in mass-market consumer electronics, such as smartphones, tablets, computers and
wearable devices. They focus on providing competitive performance, capacity, power efficiency and
form factor at attractive cost and to meet the requirements of consumer electronics manufacturers.
These products are generally used in relatively controlled operating environments. Our non-
consumer grade products comprise enterprise-grade and industrial-grade products. Our enterprise-
grade products are used in enterprise servers and data centers, where end customers include cloud
service providers, internet companies and telecommunication operators that require high-
performance, high-reliability and large-scale storage solutions. Our industrial-grade products are
used in industrial automation equipment, industrial computers, smart vehicles and a wide range of
other industrial and embedded applications, where operating environments are more demanding
(such as over wider temperature ranges, for example from approximately –40°C to 85°C; outdoor
and semi-outdoor usage, such as exposure to direct sunlight, rain splash and dust in outdoor
monitoring devices; and vibration and shock in factory machinery, construction equipment and
automotive applications).
Our consumer-grade products leverage the opportunities from the frequent iteration of
consumer electronics and the expanding of AI functionalities in edge devices. The integration of
large models into edge devices such as smartphones and computers continued to increase local data
storage and processing requirements, driving growing demand for higher-capacity and higher-
performance embedded memory products. The consumer grade products include both edge AI
devices and traditional consumer grade products. The global market of memory products for
consumer-grade products reached US$118.3 billion in 2025, and is expected to increase to
US$224.4 billion in 2030, representing a CAGR of 13.7%, according to CIC.
SUMMARY
– 2 –

<<<PAGE 12 起已省略：超出 offering 字符上限；请人工复核覆盖范围>>>



## 公司中文名（DP）

- `col_DP` = Company Chinese Name (type=text unit=text missing=NA)

### 原文切片：公司中文名（DP）


<<<PAGE 1>>>
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators, 
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Stock Code : 09976
(A joint stock company incorporated in the People’s Republic of China with limited liability)
深圳市江波龍電子股份有限公司
Shenzhen Longsys Electronics Co., Ltd.
G L O B A L 
O F F E R I N G

<<<PAGE 2>>>
If you are in any doubt about any of the contents in this document, you should obtain independent professional advice.
Shenzhen Longsys Electronics Co., Ltd.
深圳市江波龍電子股份有限公司
(A joint stock company incorporated in the People’s Republic of China with limited liability)
GLOBAL OFFERING
Number of Offer Shares under the
Global Offering
:
26,077,800 H Shares (subject to the
Offer Size Adjustment Option and the
Over-allotment Option)
Number of Hong Kong Offer Shares
:
2,607,800 H Shares (subject to
reallocation)
Number of International Offer Shares
:
23,470,000 H Shares (subject to
reallocation, the Offer Size Adjustment
Option and the Over-allotment Option)
Maximum Offer Price
:
HK$240.60 per H Share plus brokerage
of 1%, SFC transaction levy of
0.0027%, Stock Exchange trading fee
of 0.00565% and AFRC transaction
levy of 0.00015% (payable in full on
application in Hong Kong dollars and
subject to refund)
Nominal value
:
RMB1.00 per H Share
Stock code
:
09976
Joint Sponsors, Sponsor-Overall Coordinators, Overall Coordinators,
Joint Global Coordinators, Joint Bookrunners and Joint Lead Managers
Overall Coordinator, Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Global Coordinator, Joint Bookrunner and Joint Lead Manager
Joint Bookrunners and Joint Lead Managers
Hong Kong Exchanges and Clearing Limited, The Stock Exchange of Hong Kong Limited and Hong Kong Securities Clearing Company Limited take no responsibility for the contents of this
document, make no representation as to its accuracy or completeness and expressly disclaim any liability whatsoever for any loss howsoever arising from or in reliance upon the whole or any part
of the contents of this document.
A copy of this document, having attached thereto the documents specified in “Documents Delivered to the Registrar of Companies and Available on Display” in Appendix VII, has been registered
by the Registrar of Companies in Hong Kong as required by Section 342C of the Companies (Winding Up and Miscellaneous Provisions) Ordinance (Chapter 32 of the Laws of Hong Kong). The
Securities and Futures Commission of Hong Kong and the Registrar of Companies in Hong Kong take no responsibility for the contents of this document or any other document referred to above.
The Offer Price is expected to be fixed by agreement between the Sponsor-Overall Coordinators (for themselves and on behalf of the Underwriters) and us on or before Friday, September 4, 2026
(Hong Kong time). If, for any reason, the Offer Price is not agreed by 12:00 noon on Friday, September 4, 2026 (Hong Kong time) between the Sponsor-Overall Coordinators (for themselves and
on behalf of the Underwriters) and us, the Global Offering will not proceed and will lapse. The Offer Price will be no more than HK$240.60 per Offer Share unless otherwise announced.
The Sponsor-Overall Coordinators (for themselves and on behalf of the Underwriters) may, where considered appropriate and with our consent, reduce the number of Offer Shares being
offered under the Global Offering and/or the maximum Offer Price below that stated in this document at any time on or prior to the morning of the last day for lodging applications under
the Hong Kong Public Offering. Please refer to the sections headed “Structure of the Global Offering” and “How to Apply for Hong Kong Offer Shares” for further details.
The obligations of the Hong Kong Underwriters under the Hong Kong Underwriting Agreement are subject to termination by the Sponsor-Overall Coordinators (for themselves and on behalf of the
Hong Kong Underwriters) if certain grounds arise prior to 8:00 a.m. on the Listing Date. Please refer to the section headed “Underwriting — Underwriting Arrangements and Expenses — Hong Kong
Public Offering— Grounds for Termination” for further details.
Prior to making an investment decision, prospective investors should consider carefully all of the information set out in this document, including the risk factors set out in the section headed “Risk
Factors.”
The Offer Shares have not been and will not be registered under the U.S. Securities Act or any state securities laws of the United States and may not be offered or sold within or to the United States,
or to or for the account or benefit of any U.S. person (as defined in Regulation S), except in transactions exempt from, or not subject to, the registration requirements of the U.S. Securities Act.
The Offer Shares are being offered and sold (i) solely to QIBs pursuant to an exemption from registration under Rule 144A of the U.S. Securities Act and (ii) outside the United States in offshore
transactions in accordance with Regulation S.
IMPORTANT
August 31, 2026

<<<PAGE 3>>>
IMPORTANT NOTICE TO INVESTORS:
FULLY ELECTRONIC APPLICATION PROCESS
We have adopted a fully electronic application process for the Hong Kong
Public Offering. We will not provide printed copies of this prospectus in relation to
the Hong Kong Public Offering.
This prospectus is available at the website of the Stock Exchange at
www.hkexnews.hk
under
the
“HKEXnews
>
New
Listings
>
New
Listing
Information” section, and our website at https://www.longsys.com. You may
download and print from these website addresses if you want a printed copy of this
prospectus.
To apply for the Hong Kong Offer Shares, you may:
(1)
apply online via the White Form eIPO service at www.eipo.com.hk; or
(2)
apply electronically through the HKSCC EIPO channel and cause HKSCC
Nominees to apply on your behalf by instructing your broker or custodian
who is an HKSCC Participant to give electronic application instructions via
HKSCC’s FINI system to apply for the Hong Kong Offer Shares on your
behalf.
We will not provide any physical channels to accept any application for the Hong
Kong Offer Shares by the public. The contents of the electronic version of this
prospectus are identical to the printed prospectus as registered with the Registrar of
Companies in Hong Kong pursuant to Section 342C of the Companies (Winding Up and
Miscellaneous Provisions) Ordinance.
If you are an intermediary, broker or agent, please remind your customers, clients
or principals, as applicable, that this prospectus is available online at the website
addresses stated above.
IMPORTANT
– ii –




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
- out：`/Users/georgezhu/Desktop/UROP HK IPO/pipeline/prospectus_pipeline/out/extracted/HKIPO-MB9976.json`

## 任务：定向重抽（验证驱动升级）
1. 上方内联的是**相关主题分片**（不是完整包），下方 only_fields 列出本次必须补齐/修正的字段。
2. 只处理 only_fields 列出的字段；其余字段以现有 JSON 为准，不要改动。
3. 找不到证据的字段按契约填 NaN/NA，并在 quote 里说明已检索过。
4. 写 JSON 到指定 out 路径（完整契约结构），运行 `validate --only <code>` 确认后记录 state。

## only_fields（本次范围）
- col_U

