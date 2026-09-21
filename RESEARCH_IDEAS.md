# 香港主板 IPO 实证金融研究课题库与计量设计指南
## Empirical IPO Research Ideas, Theoretical Frameworks & Econometric Specifications

> **学术基石**：以 **Michelle Lowry, Roni Michaely, and Ekaterina Volkova (2017)** 经典综述单行本《*Initial Public Offerings: A Synthesis of the Literature and Directions for Future Research*》（Foundations and Trends® in Finance）为核心理论纲领。  
> **数据依托**：香港联交所主板 2026 年第一季度新股全量数据库（`HKIPO-MB2026Q1.xlsx`，138 维完整跨学科指标，38 家发行人，双门禁 100% 确证）。

---

## 目录导览

- [一、 课题一：VC/PE 异质性、董事会派驻与 18C 特专科技 IPO 抑价之谜](#一-课题一vcpe-异质性董事会派驻与-18c-特专科技-ipo-抑价之谜)
- [二、 课题二：基石投资者筹码锁定、自由流通盘挤压与首日翻转抛售（Flipping）机制](#二-课题二基石投资者筹码锁定自由流通盘挤压与首日翻转抛售flipping机制)
- [三、 课题三：FINI 制度改革、发售机制（Mechanism A/B）与动态信息提取异化](#三-课题三fini-制度改革发售机制mechanism-ab与动态信息提取异化)
- [四、 课题四：承销商辛迪加网络膨胀、保荐分肥与询价区间发散度](#四-课题四承销商辛迪加网络膨胀保荐分肥与询价区间发散度)
- [五、 课题五：生命周期公司治理：创始人超级投票权（WVR）与留在桌面上的财富](#五-课题五生命周期公司治理创始人超级投票权wvr与留在桌面上的财富)
- [六、 计量模型核心变量与 138 列主表映射字典](#六-计量模型核心变量与-138-列主表映射字典)
- [七、 论文推进路线图与工作流规范](#七-论文推进路线图与工作流规范)

---

## 一、 课题一：VC/PE 异质性、董事会派驻与 18C 特专科技 IPO 抑价之谜

### 1. 论文工作题目 (Working Title)
> **"Venture Capital Heterogeneity, Board Representation, and the Pricing of Deep-Tech IPOs: Evidence from HKEX Chapter 18C"**  
> （风险投资异质性、董事会席位与硬科技企业新股定价：来自港交所第 18C 章的实证证据）

### 2. 理论机制与文献脉络
- **认证效应假说 (Certification Hypothesis, Megginson & Weiss 1991; Brav & Gompers 1997)**：顶级专业 VC/PE（如红杉、高瓴、启明等）通过严谨的尽职调查和投后赋能，为信息极度模糊的硬科技初创企业提供声誉背书，缓解外部投资者与发行人之间的逆向选择（Rock 1986），从而**降低新股首日抑价率**。
- **名誉造势假说 (Grandstanding Hypothesis, Gompers 1996)**：年轻、募资周期紧迫的 VC 基金倾向于牺牲发行人定价（接受更高的折价与抑价），强行将尚未达到成熟商业化阶段的被投企业推向公开市场，以此向 LP 证明其项目退出能力并募集后续基金。
- **治理与顾问价值 (Advising vs. Monitoring, Field, Lowry, & Mkrtchyan 2013)**：Pre-IPO 机构投资者在董事会派驻非执行董事（NED）或观察员席位，主要发挥战略顾问与商业网络连接作用，能够显著降低发行人的事后经营波动与事前不确定性（Beatty & Ritter 1986）。

### 3. 可检验研究假说 (Testable Hypotheses)
- **$H_{1a}$（认证假说）**：拥有顶级机构认证（`col_top_tier_vc = 1`）及长期持有年限（`col_holding_duration > 5.0`）的 IPO，其首日抑价率（`col_underpricing`）显著低于普通机构投资或无 VC 支持的企业。
- **$H_{1b}$（18C 特专科技造势效应）**：对于第 18C 章特专科技公司（`col_chapter_18c = 1`，如芯片算力、大模型），由于研发强度极高且无稳定盈利，VC 持股比例（`col_vc_pe_stake`）与首日抑价率呈显著正相关，呈现典型的造势与热点炒作特征。
- **$H_{1c}$（董事会治理效应）**：Pre-IPO 投资人派驻董事席位（`col_vc_board_seat = 1`）能显著降低询价区间相对宽度（`col_range_width`），表明专业机构深度参与治理能够缩小市场对硬科技估值的事前分歧。

### 4. 计量实证模型设计
$$\begin{aligned}
\text{Underpricing}_i = &\ \alpha_0 + \beta_1 \text{TopTierVC}_i + \beta_2 \text{VCHoldingYears}_i + \beta_3 \text{VCBoardSeat}_i \\
&+ \beta_4 (\text{TopTierVC}_i \times \text{Chapter18C}_i) + \beta_5 \text{StateGovBacked}_i \\
&+ \gamma \mathbf{X}_i + \text{IndustryFE} + \varepsilon_i
\end{aligned}$$

- **核心控制变量向量 $\mathbf{X}_i$**：
  - 成立年限：$\ln(\text{FirmAge}_i + 1)$（取自 `col_firm_age`）
  - 发行规模：$\ln(\text{Proceeds}_i)$（取自 `col_funds_raised_int`）
  - 研发强度：$\text{R\&D Expensed} / \text{Net Sales}$
  - 前五大客户集中度：`Top 5 customers (% of year-1 revenue)`
  - 市场情绪：`HSI return over 20 trading days before prospectus (%)`

---

## 二、 课题二：基石投资者筹码锁定、自由流通盘挤压与首日翻转抛售（Flipping）机制

### 1. 论文工作题目 (Working Title)
> **"Cornerstone Lock-ins, Float Squeeze, and Short-Term Flipping: How Pre-Allocated Quality Signals Distort Secondary Market Liquidity"**  
> （基石投资者锁定、流通盘挤压与首日翻转交易：预配售质量信号如何扭曲二级市场流动性）

### 2. 理论机制与文献脉络
- **制度背景（港股独有红利）**：美股 IPO 严格禁止基石投资者，承销商依靠 15% 绿鞋超额配售及二级市场折价回购进行价格稳定（Ellis, Michaely, & O'Hara 2000）。港股则设立了法定 6 个月禁售期的“基石投资（Cornerstone Investors）”制度。
- **双重信号冲突**：
  - 一方面，基石认购比例高传递了主权基金/知名长线资本背书的高质量信号；
  - 另一方面，基石投资者吞噬了 30%~60% 的发售股份，导致上市首日实际不受限的自由流通量（`col_unrestricted_public_shareholding`）极度紧俏（平均仅 8%）。
- **短线翻转抛售假说 (Flipping Hypothesis, Aggarwal 2003)**：在自由流通盘严重紧缩的市场结构下，投机性散户与套利对冲基金的挂单竞争极易引发首日换手狂热。高翻转率（Flipping Velocity）不再反映基本面抛压，而是筹码稀缺性导致的博傻换手。

### 3. 可检验研究假说
- **$H_{2a}$（流通盘挤压假说）**：基石获配比例（`col_cornerstone_ratio`）越高，首日实际自由流通盘越小，首日交易翻转率（`col_flipping_ratio`）和首日振幅（$(P_{\text{high}} - P_{\text{low}})/P_{\text{offer}}$）显著越高。
- **$H_{2b}$（绿鞋替代效应）**：基石投资者锁定比例超过 40% 的发行，主承销商全额行使绿鞋（`col_greenshoe_rate = 1.0`）的概率显著降低，绿鞋机制对二级市场托单护盘的依赖度被基石资本的筹码锁定所替代。

### 4. 计量实证模型设计
$$\begin{aligned}
\text{FlippingRatio}_i = &\ \alpha_0 + \beta_1 \text{CornerstoneAllocationPct}_i + \beta_2 \text{UnrestrictedFloatPct}_i \\
&+ \beta_3 \text{SubscriptionRatio}_i + \beta_4 \text{Underpricing}_i + \gamma \mathbf{X}_i + \varepsilon_i
\end{aligned}$$

$$\text{Prob}(\text{FullGreenshoe}_i = 1) = \Phi\left(\theta_0 + \theta_1 \text{CornerstoneAllocationPct}_i + \theta_2 \text{Underpricing}_i + \mathbf{\Gamma} \mathbf{Z}_i\right)$$

---

## 三、 课题三：FINI 制度改革、发售机制（Mechanism A/B）与动态信息提取异化

### 1. 论文工作题目 (Working Title)
> **"Does Shortened Settlement Erode Bookbuilding Efficiency? Empirical Evidence from the FINI Reform and Offer Mechanisms"**  
> （结算周期压缩是否损害了簿记建档效率？来自香港 FINI 改革与双轨发售机制的实证证据）

### 2. 理论机制与文献脉络
- **动态信息提取假说 (Benveniste & Spindt 1989; Hanley 1993)**：承销商通过簿记建档收集机构投资者的私有需求信号。机构透露积极估值时，投行仅将发售价上调至区间中点上方一定幅度（留存一部分抑价给机构作为透露真相的报酬）。
- **制度外生冲击（2023 年 FINI 数字化改革 + 2025 年发售机制双轨制）**：
  - 资金锁定周期从 T+5 骤降至 T+2，大幅消除了过往由于巨额散户打新资金冻结对银行间拆借利率（HIBOR）造成的冲击；
  - 允许发行人自主选择传统固定回拨（Mechanism A）或灵活回拨（Mechanism B）。
- **实证异化之谜**：2026 Q1 数据中，多达 **22 家公司采用固定发售价（Fixed Price）**，放弃了区间询价弹性！这是否意味着在 FINI 快速发售节奏下，投行正在抛弃传统动态信息提取，转向“前置锁定核心锚定订单 + 固定价发售”模式？

### 3. 可检验研究假说
- **$H_{3a}$（机制选择内生性）**：信息不对称程度较高（18C特专科技、研发强度大、无稳定营收）的企业更倾向于选择灵活发售机制（Mechanism B），以便在机构超购时具有更大的国际配售自由度。
- **$H_{3b}$（价格修正与抑价敏感度异化）**：在采用价格区间发售的样本中，正向上修（$\Delta P^+$）对抑价率的解释力度在 FINI 实施后显著削弱，反映出国际机构在 T+2 压缩周期内博弈不充分。

### 4. 计量实证模型设计
$$\begin{aligned}
\text{Underpricing}_i = &\ \alpha + \beta_1 \Delta P_i^+ + \beta_2 \Delta P_i^- + \beta_3 \text{MechanismB}_i \\
&+ \beta_4 (\Delta P_i^+ \times \text{MechanismB}_i) + \beta_5 \text{RangeWidth}_i + \gamma \mathbf{X}_i + \varepsilon_i
\end{aligned}$$

---

## 四、 课题四：承销商辛迪加网络膨胀、保荐分肥与询价区间发散度

### 1. 论文工作题目 (Working Title)
> **"Syndicate Bloating and Rent-Seeking in Emerging Equity Markets: Why Do Mega IPOs Hire Dozens of Underwriters?"**  
> （新兴资本市场中的承销辛迪加膨胀与寻租：为什么大型 IPO 聘请数十家投行？）

### 2. 理论机制与文献脉络
- **辛迪加信息聚集假说 (Corwin & Schultz 2005)**：多个承销商共同组团能够扩大机构覆盖面，从更多买方基金处收集互补的需求信息，降低定价不确定性。
- **承销代理冲突与分肥假说 (Khanna, Noe, & Sonti 2008; Lowry et al. 2017 Ch 4)**：
  - 随着 IPO 市场竞争白热化，发行人通过分派“联席账簿管理人（JBR）”、“联席全球协调人（JGC）”等头衔作为商业利益交换；
  - 承销团层级过多导致“搭便车（Free-riding）”效应，没有任何一家投行有动力深入开展尽职调查与投资者需求摸底。

### 3. 可检验研究假说
- **$H_{4a}$（利益分肥假说）**：主承销商与账簿管理人数量（`Joint Bookrunners Count`）越多，询价区间相对宽度（`col_range_width`）不仅没有收窄，反而显著放大（投行估值模型分歧无法统一）。
- **$H_{4b}$（酌情奖励与抑价惩罚）**：发行人设立的酌情奖励费率（Incentive Fee %）能够作为委托-代理治理工具，激励主承销商收紧区间宽度，降低极端破发概率。

---

## 五、 课题五：生命周期公司治理：创始人超级投票权（WVR）与留在桌面上的财富

### 1. 论文工作题目 (Working Title)
> **"Dual-Class Structures, Controller Wedge, and Money Left on the Table: A Life-Cycle Corporate Governance Perspective"**  
> （双重股权结构、控制权两权分离与留在桌面上的财富：基于生命周期公司治理视角）

### 2. 理论机制与文献脉络
- **生命周期治理理论 (Kim & Michaely 2017; Field & Lowry 2017)**：
  - 创业初期，创始人超级投票权（WVR / Chapter 8A）能够保护企业家长远愿景，免受二级市场短期业绩压力与敌意收购威胁；
  - 控制人投票权与现金流权的“两权分离度（Wedge）”越大，控制人侵害外部中小股东的隧道挖掘（Tunneling）代理风险越高。
- **财富流失度量 (Loughran & Ritter 2002)**：留在桌面上的财富（$\text{Money Left on the Table} = (P_{\text{close}} - P_{\text{offer}}) \times \text{Shares}$）度量了发行人在上市首日直接拱手让渡给一级市场认购者的账面财富总额。控制权极度集中的创始人是否更愿意“让利”以换取友好机构持股？

### 3. 可检验研究假说
- **$H_{5a}$（两权分离与折价发售）**：控制人两权分离度（`col_controller_voting - col_controller_economic`）越大的公司，留在桌面上的财富金额（`col_money_left`）显著更高，反映创始人通过低定价绑定外部机构投资者以稳固控制地位。
- **$H_{5b}$（高管二合一壕沟效应）**：董事长与 CEO 二合一（CEO Duality）与首日抑价率显著正相关，但在非科技制造企业中会引发长期经营业绩更大幅度的下滑。

---

## 六、 计量模型核心变量与 138 列主表映射字典

下表梳理了上述五大课题涉及的所有因变量、自变量与控制变量在主表 `HKIPO-MB2026Q1.xlsx`（Sheet: `NLR`）及纯净数据文件 `HKIPO-MB2026Q1_clean.csv` 中的精确列位：

| 变量角色 | 变量名称 | 代码本表头 (Standardized Header) | 主表列号 | 数据层级与格式 |
|---|---|---|:---:|:---:|
| **因变量 1** | 首日抑价率 (Initial Return) | `First-day return / Underpricing (%)` | **Col 128** | 深蓝 / `0.00%` |
| **因变量 2** | 首日翻转抛售率 (Flipping) | `First-day flipping ratio (%)` | **Col 134** | 深蓝 / `0.00%` |
| **因变量 3** | 留在桌面上的财富 (Money Left) | `Money left on the table (HK$)` | **Col 129** | 深蓝 / `#,##0.00` |
| **因变量 4** | 绿鞋实际行使比例 | `Greenshoe exercise rate (%)` | **Col 115** | 深蓝 / `0.00%` |
| **自变量 1** | 定价偏离区间中点 ($\Delta P$) | `Filing price revision (%)` | **Col 22** | 浅蓝 / `0.00%` |
| **自变量 2** | 询价区间相对宽度 | `Filing range width (%)` | **Col 23** | 浅蓝 / `0.00%` |
| **自变量 3** | 定价落点分类体系 | `Pricing position in filing range` | **Col 24** | 浅蓝 / `@` |
| **自变量 4** | VC 支持标识 | `Pre-IPO VC backing (1=yes; 0=no)` | **Col 54** | 浅蓝 / `0` |
| **自变量 5** | 顶级投资机构认证 | `Top-tier VC/PE backing (1=yes; 0=no)` | **Col 58** | 浅蓝 / `0` |
| **自变量 6** | Pre-IPO 机构持股比例 | `Pre-IPO institutional shareholding (%)` | **Col 60** | 浅蓝 / `0.00%` |
| **自变量 7** | 投资机构派驻董事席位 | `Pre-IPO investor board seat (1=yes; 0=no)` | **Col 61** | 浅蓝 / `0` |
| **自变量 8** | Pre-IPO 最早投资持有年限 | `Pre-IPO holding duration (years)` | **Col 63** | 浅蓝 / `0.00` |
| **自变量 9** | 基石投资者获配比例 | `Final cornerstone allocation (% of base offer)` | **Col 103** | 深蓝 / `0.00%` |
| **自变量 10**| 发售与回拨机制 (A/B) | `Offer mechanism` | **Col 136** | 深蓝 / `@` |
| **控制变量 1**| 公司成立至上市年限 | `Firm age at IPO (years)` | **Col 82** | 浅蓝 / `0.00` |
| **控制变量 2**| 第 18C 章特专科技标识 | `Chapter 18C flag` | **Col 78** | 深蓝 / `0` |
| **控制变量 3**| 第 18A 章生物科技标识 | `Chapter 18A flag` | **Col 77** | 深蓝 / `0` |
| **控制变量 4**| 控制人经济利益 (持股%) | `Controller economic interest at listing (%)` | **Col 68** | 浅蓝 / `0.00%` |
| **控制变量 5**| 控制人投票权比例 (%) | `Controller voting rights at listing (%)` | **Col 69** | 浅蓝 / `0.00%` |
| **控制变量 6**| 公开发售认购超额倍数 | `Subscription Ratio (times)` | **Col 105** | 深蓝 / `#,##0.00` |
| **控制变量 7**| 招股前20日恒指累计收益 | `HSI return over 20 trading days before prospectus (%)` | **Col 123** | 深蓝 / `0.00%` |
| **控制变量 8**| 招股日前1个月 HIBOR 利率 | `1-month HIBOR before prospectus (%)` | **Col 125** | 深蓝 / `0.00%` |
| **标识字段** | 上市时股份代号 | `Stock Code` | **Col 2** | 浅绿 / `@` |
| **标识字段** | 公司中文名称 (末列) | `Company Chinese Name` | **Col 138** | 浅蓝 / `@` |

---

## 七、 论文推进路线图与工作流规范

```
[阶段一：选题论证与开题答辩]
  - 从上述五大课题中选取 1~2 个核心题目（推荐：课题一 "18C 特专科技 VC 异质性" 或 课题二 "基石锁定与翻转机制"）
  - 输出 3-5 页开题 Proposal，明确文献定位（Lowry et al. 2017 + Aggarwal 2003 / Gompers 1996）
                            │
                            ▼
[阶段二：基准实证回归 (Baseline Regressions)]
  - 导入 out/HKIPO-MB2026Q1_clean.csv 至 Stata / Python (statsmodels)
  - 跑 OLS 核心方程，汇报描述性统计表（Table 1）与基准相关系数矩阵（Table 2）
  - 生成主回归回归表（Table 3: 逐步加入企业基本面、宏观情绪与行业固定效应）
                            │
                            ▼
[阶段三：内生性处理与稳健性检验 (Identification & Robustness)]
  - 2SLS 工具变量法（解决 VC 投资与企业质量的反向因果，参考 Lowry & Shu 2002）
  - 倾向得分匹配（PSM：匹配相似规模与行业但无 VC 支持的企业）
  - 替换被解释变量（例如使用首周/首月超额收益 CAR 替代首日抑价率）
                            │
                            ▼
[阶段四：样本跨期扩充与季度追踪]
  - 依托 prospectus_pipeline 自动化流水线，顺延跑通 2026 Q2 / Q3 季度新上市公司
  - 保持 138 维指标口径绝对连续可比，将样本量由 38 家稳步扩充至 100+ 家
```
