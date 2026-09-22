# 香港主板新股市场全景实证与理论研究课题库 (20 大核心 Research Ideas)
# The Hong Kong Main Board IPO Panoramic Research Compendium: Theoretical Frameworks, Institutional Realities & Econometric Specifications

> **学术基石**：以 **Michelle Lowry, Roni Michaely, and Ekaterina Volkova (2017)** 经典综述单行本《*Initial Public Offerings: A Synthesis of the Literature and Directions for Future Research*》（Foundations and Trends® in Finance）为核心理论与实证基准，融贯公司金融学、微观市场结构与合同理论前沿经典文献。  
> **数据依托**：全量香港主板 2026 年第一季度新股数据库（`HKIPO-MB2026Q1.xlsx`，Sheet: `NLR`，138 维完整跨学科指标，38 家挂牌样本，覆盖 18C 特专科技、18A 生物科技、FINI 数字化结算改革、Pre-IPO VC/PE 细分股权、基石投资者配售及二级市场量价，100% 审计级穿透确证）。  
> **使用定位**：本课题库专为构建香港新股市场“全景全生态学术研究”而设立。不再按照单一论文的章节划分，而是**收录 20 个独立、完整、且高度细化的 Research Ideas**。每个 Idea 均包含：
> 1. 💡 研究课题与核心科学问题 (Research Title & Core Question)
> 2. 📚 经典文献基准与美股经验事实 (Literature Baseline & U.S. Stylized Facts - Lowry et al. 2017)
> 3. 🏛️ 香港主板制度背景与样本微观现实 (HKEX Institutional Realities & 2026 Q1 Distribution)
> 4. 🔬 待检验学术假说体系 (Testable Empirical Hypotheses: $H_a, H_b$)
> 5. 📐 规范计量经济学回归模型 (Econometric Specifications with LaTeX Equations)
> 6. 📊 138 列主表变量与字段映射 (Exact Column Mapping to `HKIPO-MB2026Q1.xlsx`)
> 7. 🧭 经济学直觉与学术边际贡献 (Economic Intuition & Contribution)

---

## 目录索引 (Directory of 20 Research Ideas)

- [Idea 01: 多元化监管通道选择、信息不对称与上市估值折价 (Chapter 18A / 18C / 19A A+H)](#idea-01-多元化监管通道选择信息不对称与上市估值折价-chapter-18a--18c--19a-ah)
- [Idea 02: FINI 数字化结算、双轨发售机制（Mechanism A vs. B）与固定价格发行的动态信息提取异化](#idea-02-fini-数字化结算双轨发售机制mechanism-a-vs-b与固定价格发行的动态信息提取异化)
- [Idea 03: 基石投资者法定限售、自由流通盘极端挤压（Float Squeeze）与首日翻转抛售](#idea-03-基石投资者法定限售自由流通盘极端挤压float-squeeze与首日翻转抛售)
- [Idea 04: Pre-IPO VC/PE 机构异质性：声誉认证、持有期深化与特专科技造势狂热](#idea-04-pre-ipo-vcpe-机构异质性声誉认证持有期深化与特专科技造势狂热)
- [Idea 05: 承销辛迪加网络多头膨胀、搭便车与初步估值区间发散](#idea-05-承销辛迪加网络多头膨胀搭便车与初步估值区间发散)
- [Idea 06: 留在桌面上的财富、前景理论心理账户与双重发行成本膨胀](#idea-06-留在桌面上的财富前景理论心理账户与双重发行成本膨胀)
- [Idea 07: 生命周期公司治理：WVR 同股不同权、控制权两权分离与高管堑壕防御](#idea-07-生命周期公司治理wvr-同股不同权控制权两权分离与高管堑壕防御)
- [Idea 08: 宏观流动性周期、公开发售散户抽签狂热与公开市场信息吸收效率](#idea-08-宏观流动性周期公开发售散户抽签狂热与公开市场信息吸收效率)
- [Idea 09: 双重解禁日期的“筹码雪崩效应”：基石投资者 6 个月解禁 vs. 控股股东限售期满](#idea-09-双重解禁日期的筹码雪崩效应基石投资者-6-个月解禁-vs-控股股东限售期满)
- [Idea 10: 商业银行系投行保荐与信贷关系认证效应](#idea-10-商业银行系投行保荐与信贷关系认证效应)
- [Idea 11: 承销商场内托单与 30 天稳价期结束后的“悬崖效应”](#idea-11-承销商场内托单与-30-天稳价期结束后的悬崖效应)
- [Idea 12: 招股书文本诉讼保险与跨国监管风险对冲](#idea-12-招股书文本诉讼保险与跨国监管风险对冲)
- [Idea 13: 散户“孖展”杠杆融资狂热与信息瀑布羊群效应](#idea-13-散户孖展杠杆融资狂热与信息瀑布羊群效应)
- [Idea 14: 跨界基金（Crossover Funds）双重身份：Pre-IPO 股东兼任基石的信号传递与利益冲突](#idea-14-跨界基金crossover-funds双重身份pre-ipo-股东兼任基石的信号传递与利益冲突)
- [Idea 15: 大客户集中度、专用性资产投资与创始人控制权绑定](#idea-15-大客户集中度专用性资产投资与创始人控制权绑定)
- [Idea 16: 同行业科技竞品防御性上市浪潮与估值溢出](#idea-16-同行业科技竞品防御性上市浪潮与估值溢出)
- [Idea 17: 卖方明星分析师覆盖与抑价“隐性贿赂”假说](#idea-17-卖方明星分析师覆盖与抑价隐性贿赂假说)
- [Idea 18: 发行费用分拆中的“软美元寻租”：固定承销佣金 vs. 酌情奖励费率博弈](#idea-18-发行费用分拆中的软美元寻租固定承销佣金-vs-酌情奖励费率博弈)
- [Idea 19: 卖方跨期期望效用最大化与“理性抑价”：发行流产保险、解禁期多阶段套现与激励相容信息租金](#idea-19-卖方跨期期望效用最大化与理性抑价发行流产保险解禁期多阶段套现与激励相容信息租金)
- [Idea 20: 港股 IPO 长期收益之谜：上市后 3 年买入持有回报（BHR）、基准指数加权偏误（EW vs. VW）与同风格匹配检验](#idea-20-港股-ipo-长期收益之谜上市后-3-年买入持有回报bhr基准指数加权偏误ew-vs-vw与同风格匹配检验-long-run-underperformance-wealth-relatives--benchmark-contamination)
- [附录：全景课题库统一变量定义与 138 列主表映射全景矩阵](#附录全景课题库统一变量定义与-138-列主表映射全景矩阵)

---

## Idea 01: 多元化监管通道选择、信息不对称与上市估值折价 (Chapter 18A / 18C / 19A A+H)

### 1.1 研究课题与核心科学问题
- **研究课题**：多元化上市监管通道（Chapter 18C 特专科技、Chapter 18A 未盈利生物科技、Chapter 19A A+H 股及常规主板）如何重塑企业事前估值不确定性与二级市场定价效率？
- **核心问题**：缺乏商业化营收或利润的特专科技公司（18C）是否承受了更高的事前定价不确定性？内地 A 股连续交易形成的公开二级市场价格锚（Price Anchor），能否有效消除赴港发行 H 股时的信息不对称并压缩发售区间宽度与抑价波动？

### 1.2 经典文献基准与美股经验事实
- **理论基准 (Lowry, Michaely, & Volkova 2017 Ch 2)**：
  - **企业上市权衡假说 (Going-public Trade-off, Celikyurt et al. 2010; Zingales 1995)**：企业在获得公开市场流动性溢价与承担合规披露、代理成本之间权衡。
  - **信息生产与折价假说 (Information Production & Valuation Uncertainty, Ritter 1984)**：缺乏可比财务业绩与高研发强度的企业，投资者必须开展高成本尽职调查，承销商须通过扩大初步询价区间和提高首日抑价以补偿信息风险。
- **美股事实**：由于私募成长型资本充沛，美股科技企业 IPO 年龄从 1980 年代的 6.0 年推迟至 2016 年的 11.2 年；缺乏盈利的科技公司在美股 IPO 中的首日抑价率（24.8%）显著高于传统成熟盈利企业（9.7%）。

### 1.3 香港主板制度背景与样本微观现实
- **制度创新**：
  1. **第 18A 章**：未盈利生物医药企业上市通道；
  2. **第 18C 章**：特专科技公司通道，设“已商业化”（收入 $\ge 2.5$ 亿港元）与“未商业化”（研发开支占比 $\ge 50\%$）双轨；
  3. **第 19A 章与 A+H 双重上市**：内地注册股份公司赴港发行 H 股。若已在 A 股上市，A 股现货价格直接构成跨境信息锚。
- **2026 Q1 数据分布**：全量 38 家样本中，**A+H 发行人 12 家（31.6%）**，**第 18C 章特专科技 6 家（15.8%）**，**第 18A 章生物科技 3 家（7.9%）**，传统主板 17 家（44.7%）。不同监管通道在研发投入、历史财务与估值区间宽度上呈现巨大跨度。

### 1.4 待检验学术假说体系
- **$H_{1a}$（高科技通道估值不确定性与折价补偿假说）**：采用 18C 或 18A 通道上市的发行人，由于缺乏历史商业化盈利记录，其事前估值不确定性显著高于普通主板企业，表现为**显著更宽的初步询价区间相对宽度（`Filing range width (%)`）与更高的首日抑价率**。
- **$H_{1b}$（A+H 跨境现货价格锚约束假说）**：A+H 发行人的内地 A 股二级市场价格为 H 股询价提供了高透明度公开参照，显著抑制了信息不对称。因此，A+H 发行人的发售区间相对宽度显著收窄，首日抑价率的条件方差显著低于纯 H 股或红筹企业。

### 1.5 规范计量经济学模型
#### 模型 1.1：监管通道选择对事前估值区间宽度的影响 (OLS)
$$\begin{aligned}
\text{RangeWidth}_i = &\ \alpha_0 + \beta_1 \text{Chapter18C}_i + \beta_2 \text{Chapter18A}_i + \beta_3 \text{APlusH}_i \\
&+ \beta_4 \ln(\text{RDExpensed}_i + 1) + \beta_5 \ln(\text{FirmAge}_i + 1) + \beta_6 \ln(\text{TotalAssets}_i) \\
&+ \text{IndustryFE} + \varepsilon_i
\end{aligned}$$

#### 模型 1.2：A+H 价格锚与科技通道对首日抑价的联合检验 (OLS)
$$\begin{aligned}
\text{IR}_i = &\ \alpha_0 + \beta_1 \text{APlusH}_i + \beta_2 \text{Chapter18C}_i + \beta_3 \text{Chapter18A}_i \\
&+ \beta_4 \ln(\text{Proceeds}_i) + \beta_5 \text{SubscriptionRatio}_i + \gamma \mathbf{X}_i + \varepsilon_i
\end{aligned}$$

### 1.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 发售区间相对宽度 | **Col 23** | `Filing range width (%)` | 数值百分比 | 模型 1.1 被解释变量 (Y) |
| 首日抑价率 | **Col 128**| `First-day return / Underpricing (%)` | 数值百分比 | 模型 1.2 被解释变量 (Y) |
| 18C 特专科技标识 | **Col 78** | `Chapter 18C flag` | 0/1 虚拟变量 | 核心解释变量 (X) |
| 18A 生物科技标识 | **Col 77** | `Chapter 18A flag` | 0/1 虚拟变量 | 核心解释变量 (X) |
| A+H 双重上市标识 | **Col 75** | `A+H issuer flag` | 0/1 虚拟变量 | 核心解释变量 (X) |
| 研发费用开支 | **Col 52** | `R&D expensed in year-1 (before annualization)` | 货币数值 | 核心控制变量 |
| 公司成立年限 | **Col 82** | `Firm age at IPO (years)` | 数值浮点 | 基础控制变量 |
| 上市前一年总资产 | **Col 28** | `total assets in year-1` | 货币数值 | 规模控制变量 |

### 1.7 经济学直觉与学术贡献
拓展了 Lowry et al. (2017) 探讨的上市动机与制度通道选择理论。在同一交易所体系内，首次验证了“未盈利硬科技包容通道”与“跨境存量价格锚通道”对信息不对称与定价效率的相反作用力。

---

## Idea 02: FINI 数字化结算、双轨发售机制（Mechanism A vs. B）与固定价格发行的动态信息提取异化

### 2.1 研究课题与核心科学问题
- **研究课题**：港交所 FINI 结算周期由 T+5 压缩至 T+2、推出 Mechanism A（传统阶梯回拨）与 Mechanism B（灵活回拨）后，发行人普遍转向“固定发售价（Fixed Price）”对承销商信息提取机制与首日抑价结构产生了怎样的冲击？
- **核心问题**：固定发售法定价是否彻底破坏了 Benveniste & Spindt (1989) 和 Hanley (1993) 的动态信息提取功能？Mechanism B 赋予保荐人回拨自主权后，是否缓解了散户过量认购对机构订单的稀释扭曲？

### 2.2 经典文献基准与美股经验事实
- **经典信息提取假说 (Benveniste & Spindt 1989)**：簿记建档本质上是投行通过有倾向性的配售份额向常规机构买方提取私有估值信号的重复博弈；
- **Hanley (1993) 部分修正规律 (Partial Adjustment)**：
  - 定价突破区间上限（Upward revision, $\Delta P > 0$）：传递强烈利好信号，平均抑价高达 **+50.2%**；
  - 定价跌破区间下限（Downward revision, $\Delta P < 0$）：传递利空信号，平均抑价仅 **+3.9%**（Lowry et al. 2017 Table 3.3）。
- **经验对比**：美股 95% 以上采取询价区间簿记建档，固定发售法仅见于少数直接上市（Direct Listing）或低价小微股。

### 2.3 香港主板制度背景与样本微观现实
- **制度变革**：2023 年底全面启用 FINI，并明确两大机制：
  - **Mechanism A**：严格按散户认购倍数法定强制回拨（超购 15~50 倍回拨至 30%、50~100 倍回拨至 40%、100 倍以上回拨至 50%）；
  - **Mechanism B**：允许发行人与保荐人在满足公开发售底线下根据实际需求弹性微调，保护国际配售机构份额。
- **2026 Q1 数据异化事实**：
  - **38 家样本中有 22 家实行单一固定价格发售（Fixed Price），占比高达 57.9%**；
  - 采用发售区间的 16 家中：**6 家顶格定价（At high）、6 家区间内、4 家底格定价（At low）**；
  - 港股发行人大幅减少价格微调，转而在路演前直接锚定基石投资者份额并固定价格发售。

### 2.4 待检验学术假说体系
- **$H_{2a}$（信息提取丧失与波动放大假说）**：固定发售法定价（Fixed Price）剥夺了投行动态调整价格以提取机构私有信息的能力。因此，固定发售定价的新股首日抑价率条件方差显著高于区间询价发行样本，呈现出极高破发率与极端暴涨并存的两极分化。
- **$H_{2b}$（Mechanism B 需求信号保留假说）**：在 Mechanism B 下，国际配售部分不因散户认购过热而被强制回拨腰斩，机构真实需求信号得到保留。因此，价格修正（$\Delta P_i$）对首日抑价率的解释系数 $\beta$ 在 Mechanism B 样本中显著大于 Mechanism A。

### 2.5 规范计量经济学模型
#### 模型 2.1：发售机制与部分修正交互模型 (OLS)
$$\begin{aligned}
\text{IR}_i = &\ \alpha_0 + \beta_1 \Delta P_i + \beta_2 \text{RangeWidth}_i + \beta_3 \text{MechanismB}_i + \beta_4 (\Delta P_i \times \text{MechanismB}_i) \\
&+ \beta_5 \text{FixedPriceDummy}_i + \beta_6 \ln(\text{SubscriptionRatio}_i) + \gamma \mathbf{X}_i + \varepsilon_i
\end{aligned}$$

#### 模型 2.2：Hanley (1993) 不对称信息提取检验模型
$$\text{IR}_i = \alpha_0 + \beta_1 \Delta P_i^+ + \beta_2 \Delta P_i^- + \beta_3 \text{RangeWidth}_i + \beta_4 \text{FixedPriceDummy}_i + \gamma \mathbf{X}_i + \varepsilon_i$$
- 检验假说：$\beta_1 > \beta_2$ 且 $\beta_1 > 0$（验证正向上修对抑价率的非对称驱动）。

### 2.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 首日抑价率 | **Col 128**| `First-day return / Underpricing (%)` | 数值百分比 | 被解释变量 (Y) |
| 发售价格修正幅度 | **Col 22** | `Filing price revision (%)` | 数值百分比 | 核心自变量 ($\Delta P$) |
| 发售区间相对宽度 | **Col 23** | `Filing range width (%)` | 数值百分比 | 核心自变量 |
| 定价落点分类 | **Col 24** | `Pricing position in filing range` | 文本分类 | 分组/自变量 |
| 发售回拨机制 | **Col 136**| `Offer mechanism` | 文本分类 | 机制分类自变量 |
| 散户超购倍数 | **Col 105**| `Subscription Ratio (times)` | 数值浮点 | 市场需求控制变量 |
| 恒指前 20 日收益率 | **Col 123**| `HSI return over 20 trading days before prospectus (%)` | 数值百分比 | 市场情绪控制变量 |

### 2.7 经济学直觉与学术贡献
首次系统检验了 FINI 时代下港股独特的“固定价格主流化”反常现象，对经典 Benveniste & Spindt 簿记建档理论提供了来自中国香港市场的全新制度反思与经验实证。

---

## Idea 03: 基石投资者法定限售、自由流通盘极端挤压（Float Squeeze）与首日翻转抛售

### 3.1 研究课题与核心科学问题
- **研究课题**：港交所独有的基石投资者（Cornerstone Investors）法定 6 个月限售锁定，如何造成新股上市首日自由流通盘的极端挤压（Float Squeeze）？这如何反向激化了二级市场的短线翻转抛售（Flipping）与绿鞋机制失灵？
- **核心问题**：基石锁定的高比例是否从“信任背书（Certification）”异化为了“逼空炒作（Short Squeeze）”的筹码结构温床？

### 3.2 经典文献基准与美股经验事实
- **短线翻转抛售假说 (Flipping Hypothesis, Aggarwal 2003)**：
  - 美股新股上市首两天内，机构投资者平均翻转卖出约 **15%** 的发售股份；
  - 翻转率与抑价率正相关，反映获配者逢高套现锁定收益（Free-riding）。
- **绿鞋价格稳定机制 (Greenshoe Mechanics, Ellis, Michaely, & O'Hara 2000)**：
  - 承销商利用 15% 超额配售权建立裸空头。破发时在二级市场低价回购股票托单并赚取买卖差价；热门时全额行使绿鞋平仓。

### 3.3 香港主板制度背景与样本微观现实
- **港交所基石制度**：上市前引入基石投资者，签订法定协议，招股书实名披露，且**法定必须锁定 6 个月（180 天）禁售**；
- **2026 Q1 数据极端事实**：
  - **38 家中有 34 家配置基石（覆盖率 89.5%）**，基石认购占基础发售平均高达 **38.3%**；
  - **自由流通盘极端挤压**：扣除基石锁定与大股东限售后，上市首日实际不受限自由流通比例（`Unrestricted public shareholding`）**均值仅 8.0%（中位数 7.0%）**！
  - **首日翻转率惊人**：`First-day flipping ratio (%)` **均值高达 38.79%**，最高个股达 92.26%，是美股基准（15%）的 2.5 倍以上；
  - **绿鞋分化失灵**：全样本绿鞋行使率仅 **38.21%**（21 家执行率为 0%）。

### 3.4 待检验学术假说体系
- **$H_{3a}$（自由流通盘挤压与投机翻转假说）**：基石投资者获配比例越高，首日不受限自由流通盘越小，供求失衡引发的博傻交易越剧烈，首日翻转抛售率（`First-day flipping ratio (%)`）与盘中振幅显著放大。
- **$H_{3b}$（基石对绿鞋护盘的替代假说）**：基石投资者的大额锁定（锁住 30%~60% 基础份额）在结构上吸收了大量下行抛压，从而替代了承销商二级市场托底护盘的需求。基石认购比例越高，承销商最终全额行使绿鞋（`Greenshoe exercise rate == 100%`）的概率显著降低。

### 3.5 规范计量经济学模型
#### 模型 3.1：自由流通盘挤压对首日翻转率的驱动模型 (OLS)
$$\begin{aligned}
\text{FlippingRatio}_i = &\ \alpha_0 + \beta_1 \text{CornerstoneAllocationPct}_i + \beta_2 \text{UnrestrictedFloatPct}_i \\
&+ \beta_3 \text{IR}_i + \beta_4 \ln(\text{SubscriptionRatio}_i) + \gamma \mathbf{X}_i + \varepsilon_i
\end{aligned}$$

#### 模型 3.2：基石投资对绿鞋行使率的替代模型 (Tobit / Probit)
$$\text{GreenshoeRate}_i = \theta_0 + \theta_1 \text{CornerstoneAllocationPct}_i + \theta_2 \text{IR}_i + \theta_3 \text{UnderwriterPrestige}_i + \mathbf{\Gamma} \mathbf{Z}_i + \mu_i$$

### 3.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 首日翻转抛售率 | **Col 134**| `First-day flipping ratio (%)` | 数值百分比 | 模型 3.1 被解释变量 (Y) |
| 绿鞋实际行使比例 | **Col 115**| `Greenshoe exercise rate (%)` | 数值百分比 | 模型 3.2 被解释变量 (Y) |
| 基石配售占基础发售比 | **Col 103**| `Final cornerstone allocation (% of base offer)` | 数值百分比 | 核心自变量 (X) |
| 首日不受限自由流通比 | **Col 120**| `Unrestricted public shareholding at listing (%)`| 数值百分比 | 核心自变量 (X) |
| 首日抑价率 | **Col 128**| `First-day return / Underpricing (%)` | 数值百分比 | 交易回报自变量 |
| 首日全天成交股数 | **Col 133**| `First trading day volume (shares)` | 整数数值 | 交易活跃度控制变量 |
| 实际发行超额配售股数 | **Col 114**| `Over-allotment shares actually issued` | 整数数值 | 绿鞋结果变量 |

### 3.7 经济学直觉与学术贡献
将 Aggarwal (2003) 的翻转假说与 Ellis et al. (2000) 的绿鞋价格稳定机制，深度植根于香港独特的基石限售制度土壤，揭示了“高基石护航”反而诱发“微小流通盘投机暴炒”的微观市场结构机制。

---

## Idea 04: Pre-IPO VC/PE 机构异质性：声誉认证、持有期深化与特专科技造势狂热

### 4.1 研究课题与核心科学问题
- **研究课题**：Pre-IPO 风险投资机构的异质性（知名顶尖 VC、政府/国资引导基金、产业资本 CVC、私募股权 PE）、投资持有期长短及派驻董事会席位，如何影响 IPO 估值定价与首日抑价？
- **核心问题**：VC 机构在香港市场究竟发挥了 Megginson & Weiss (1991) 的“声誉认证与公司治理价值”，还是表现为 Gompers (1996) 描述的年轻基金急于变现退出的“名誉造势（Grandstanding）”？

### 4.2 经典文献基准与美股经验事实
- **声誉认证假说 (Certification, Megginson & Weiss 1991; Brav & Gompers 1997)**：知名 VC 拥有宝贵声誉资本，通过尽调为企业背书，降低信息不对称，从而抑制首日抑价。
- **名誉造势假说 (Grandstanding, Gompers 1996)**：年轻 VC 急于向 LP 证明退出变现能力以募集后续基金，倾向于过早催熟企业上市，容忍更高的抑价折让（美股 VC 抑价 27.4% vs 非 VC 11.9%）。
- **投后治理赋能 (Advising, Sørensen 2007)**：VC 增值价值的三分之二来源于投后运营管控与董事会治理介入，仅三分之一来自初始选拔。

### 4.3 香港主板制度背景与样本微观现实
- **2026 Q1 数据分布深度**：
  - **61% 的样本企业拥有 VC 背景**，**58% 获得顶级知名机构（如红杉、高瓴、启明、君联等）背书**；
  - 机构上市前平均持股 **25.0%**，**50.0% 的企业中派驻了董事会非执行董事或观察员席位**；
  - 最早入股时间平均持有长达 **5.38 年**，覆盖从天使轮到 Pre-IPO 轮的完整周期。

### 4.4 待检验学术假说体系
- **$H_{4a}$（持有期深化与治理认证主导假说）**：Pre-IPO 机构持有年限越长（`Pre-IPO holding duration`）、派驻董事会席位（`Pre-IPO investor board seat == 1`）的企业，其“治理赋能与认证效应”越强，首日抑价率显著更低。
- **$H_{4b}$（18C 特专科技造势狂热假说）**：在尚无商业化盈利的第 18C 章特专科技样本中，VC 机构持股集中度与首日抑价率呈显著正相关，反映出机构在硬科技风口期赶场上市、利用二级市场投机情绪实现溢价套现的“造势共谋”。

### 4.5 规范计量经济学模型
#### 模型 4.1：VC 异质性与治理特征对抑价的回归方程 (OLS)
$$\begin{aligned}
\text{IR}_i = &\ \alpha_0 + \beta_1 \text{TopTierVC}_i + \beta_2 \text{VCHoldingYears}_i + \beta_3 \text{VCBoardSeat}_i \\
&+ \beta_4 (\text{TopTierVC}_i \times \text{Chapter18C}_i) + \beta_5 \text{StateGovBacked}_i \\
&+ \beta_6 \text{InstitutionalStakePct}_i + \gamma \mathbf{X}_i + \varepsilon_i
\end{aligned}$$

#### 模型 4.2：内生性处理之 2SLS 工具变量回归系统
- **第一阶段 (First Stage)**：
  $$\widehat{\text{VCBacked}}_i = \pi_0 + \pi_1 \text{IndustryVCClustering}_i + \pi_2 \text{HQCtyTier}_i + \mathbf{\Pi} \mathbf{X}_i + \mu_i$$
- **第二阶段 (Second Stage)**：
  $$\text{IR}_i = \alpha_0 + \alpha_1 \widehat{\text{VCBacked}}_i + \alpha_2 \text{Chapter18C}_i + \mathbf{\Gamma} \mathbf{X}_i + \varepsilon_i$$

### 4.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 首日抑价率 | **Col 128**| `First-day return / Underpricing (%)` | 数值百分比 | 被解释变量 (Y) |
| VC 机构持股标识 | **Col 57** | `Pre-IPO VC backing (1=yes; 0=no)` | 0/1 虚拟变量 | 核心自变量 |
| PE 机构持股标识 | **Col 58** | `Pre-IPO PE backing (1=yes; 0=no)` | 0/1 虚拟变量 | 核心自变量 |
| 国资/政府引导基金标识| **Col 60** | `Pre-IPO State/Gov backing (1=yes; 0=no)` | 0/1 虚拟变量 | 核心自变量 |
| 顶尖机构背书标识 | **Col 61** | `Top-tier VC/PE backing (1=yes; 0=no)` | 0/1 虚拟变量 | 核心自变量 |
| 机构上市前合计持股比 | **Col 63** | `Pre-IPO institutional shareholding (%)` | 数值百分比 | 核心股权变量 |
| 机构派驻董事席位标识 | **Col 64** | `Pre-IPO investor board seat (1=yes; 0=no)` | 0/1 虚拟变量 | 治理介入变量 |
| 机构最早入股持有年限 | **Col 66** | `Pre-IPO holding duration (years)` | 数值浮点 | 资本耐心度量 |
| 18C 特专科技标识 | **Col 78** | `Chapter 18C flag` | 0/1 虚拟变量 | 交互调节变量 |

### 4.7 经济学直觉与学术贡献
将 Gompers (1996) 与 Megginson & Weiss (1991) 的美股经典之争引入港股特专科技改革前沿，通过 138 列数据中的派驻董事、持有年限与顶级机构标签，实现了对 VC“认证 vs 造势”的精准微观解构。

---

## Idea 05: 承销辛迪加网络多头膨胀、搭便车与初步估值区间发散

### 5.1 研究课题与核心科学问题
- **研究课题**：承销团联席保荐人（Joint Sponsors）、联席全球协调人（JGC）与联席账簿管理人（JBR）数量的急剧膨胀，如何导致辛迪加内部的信息搭便车与估值分歧？
- **核心问题**：过度庞大的承销团是否导致各投行在估值建模和客户推介中缺乏排他性激励，从而导致发售价格区间被迫拉宽？

### 5.2 经典文献基准与美股经验事实
- **承销辛迪加组织理论 (Corwin & Schultz 2005; Khanna, Noe, & Sonti 2008)**：
  - 辛迪加成员增加能够扩大机构客户覆盖网络，但容易诱发搭便车行为（Free-riding）；
  - 承销商声誉与历史承销份额（Carter & Manaster 1990; Loughran & Ritter 2004）是制约搭便车的核心机制。
- **美股事实 (Lowry et al. 2017 Table 3.6)**：美股联席主承数量从 1970 年代的 1.00 家稳步增至 2016 年的 3.89 家。

### 5.3 香港主板制度背景与样本微观现实
- **港股“超级辛迪加”常态**：香港大型高科技及国企 IPO（如壁仞科技、智谱华章、顺丰控股等）动辄聘用 **10~18 家** 联席账簿管理人；
- **佣金结构分拆**：港股承销协议中普遍包含固定佣金（Fixed Commission）与全权酌情奖励费（Discretionary Incentive Fee），发行人管理层在上市后决定奖金池向哪家投行倾斜。

### 5.4 待检验学术假说体系
- **$H_{5a}$（辛迪加网络膨胀与估值区间发散假说）**：联席账簿管理人（JBR）数量越多，承销团内部的估值模型与销售策略越难达成共识，事前信息收集的搭便车效应越严重，初步询价区间相对宽度（`Filing range width (%)`）显著拉大。
- **$H_{5b}$（酌情奖励费率的激励逆转假说）**：设立较高全权酌情奖励费率（Discretionary Fee %）的发行人，保荐人为了争取奖金池，具有更强的冲动促成发售价顶格定价（`Pricing position == 'At high'`）。

### 5.5 规范计量经济学模型
#### 模型 5.1：承销辛迪加规模对估值区间发散度的影响 (OLS)
$$\text{RangeWidth}_i = \alpha_0 + \beta_1 \ln(\text{SyndicateSize}_i) + \beta_2 \text{UnderwritingCommissionPct}_i + \beta_3 \ln(\text{NetProceeds}_i) + \gamma \mathbf{X}_i + \varepsilon_i$$

#### 模型 5.2：辛迪加结构对顶格定价落点的 Logistic 模型
$$\text{Logit}\left(\text{Prob}(\text{PricingPosition}_i = \text{'At high'})\right) = \theta_0 + \theta_1 \ln(\text{SyndicateSize}_i) + \theta_2 \ln(\text{SubscriptionRatio}_i) + \mathbf{\Gamma} \mathbf{Z}_i$$

### 5.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 发售区间相对宽度 | **Col 23** | `Filing range width (%)` | 数值百分比 | 模型 5.1 被解释变量 (Y) |
| 定价落点分类 | **Col 24** | `Pricing position in filing range` | 文本分类 | 模型 5.2 被解释变量 (Y) |
| 保荐人团队名单 | **Col 6**  | `Sponsor(s)` | 文本列表 | 辛迪加规模提取源 (X) |
| 香港公开发售承销佣金率| **Col 44** | `Underwriting Commission (% of fund raised HK (a)` | 数值百分比 | 核心自变量 (X) |
| 显性总上市开支 | **Col 101**| `Listing expenses (HK$)` | 货币数值 | 成本控制变量 |
| 最终发行人净募资额 | **Col 117**| `Net IPO proceeds to issuer (HK$)` | 货币数值 | 发行规模控制变量 |

### 5.7 经济学直觉与学术贡献
从微观承销辛迪加组织设计视角切入，解释了香港投行界“多头联合保荐”如何加剧估值预期发散，为承销协议中的佣金与奖金契约优化提供了实证支持。

---

## Idea 06: 留在桌面上的财富、前景理论心理账户与双重发行成本膨胀

### 6.1 研究课题与核心科学问题
- **研究课题**：香港 IPO 发行人在承担显性现金上市费用（律所、审计师、保荐人费用）的同时，通过首日抑价向二级市场让渡了多少隐性财富（留在桌面上的财富，Money Left on the Table）？
- **核心问题**：为何理性控股股东愿意容忍巨额财富流失？前景理论的“心理账户（Mental Accounting）”假说是否能够解释这一现象？

### 6.2 经典文献基准与美股经验事实
- **行为金融学前景理论假说 (Loughran & Ritter 2002)**：
  - 发行人并不厌恶抑价让利，因为当发售价向上修正时（$\Delta P > 0$），原股东持有的巨额存量股份市值暴增，其带来的“收益心理账户”彻底掩盖了新股折价稀释的“损失心理账户”。
  - **留在桌面上的财富公式**：
    $$\text{Money Left on the Table}_i = (P_{i, \text{day1\_close}} - P_{i, \text{offer}}) \times \text{Base Global Offering Shares}$$
- **美股事实**：1980-2016 年美股 IPO 留在桌面上的累计财富超过 660 亿美元，远超现金承销费用总额。

### 6.3 香港主板制度背景与样本微观现实
- **2026 Q1 数据惊人事实**：
  - 38 家样本首日累计让渡财富高达 **256.64 亿港元**，单家平均让渡 **6.75 亿港元**；
  - 同期 38 家公司支付的显性现金上市费用（`Listing expenses`）总额约为 **40.4 亿港元**；
  - **隐性财富流失是显性现金费用的 6.35 倍！** 发行成本的主体并非账面费用，而是抑价流失。

### 6.4 待检验学术假说体系
- **$H_{6a}$（前景理论心理账户假说）**：发售价偏离初步询价区间中点上修幅度越大（$\Delta P_i > 0$）的发行人，由于原股东财富增值效应更强，对财富流失的痛苦感越低，其留在桌面上的绝对金额（`Money left on the table`）显著更高。
- **$H_{6b}$（控股股东稀释防御假说）**：上市时控股股东经济利益持股比例（`Controller economic interest`）越高的企业，对自身股权被过度低价稀释越敏感，其留在桌面上的财富显著更小。

### 6.5 规范计量经济学模型
#### 模型 6.1：留在桌面上的财富决定方程 (OLS / Tobit)
$$\begin{aligned}
\ln(\text{MoneyLeft}_i + 1) = &\ \alpha_0 + \beta_1 \Delta P_i + \beta_2 \text{ControllerEconomicPct}_i + \beta_3 \ln(\text{ListingExpenses}_i) \\
&+ \beta_4 \ln(\text{NetProceeds}_i) + \beta_5 \text{WVRFlag}_i + \gamma \mathbf{X}_i + \varepsilon_i
\end{aligned}$$

### 6.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 留在桌面上的财富 | **Col 129**| `Money left on the table (HK$)` | 货币数值 | 被解释变量 (Y) |
| 发售价格修正幅度 | **Col 22** | `Filing price revision (%)` | 数值百分比 | 核心自变量 ($\Delta P$) |
| 显性总上市开支 | **Col 101**| `Listing expenses (HK$)` | 货币数值 | 核心自变量 |
| 控制人上市经济持股比 | **Col 68** | `Controller economic interest at listing (%)` | 数值百分比 | 控股股东治理自变量 |
| 最终全球发售基础股数 | **Col 111**| `Final global offering shares (before over-allotment)`| 整数数值 | 规模基础变量 |
| 最终发售价 | **Col 11** | ` IPO Subscription Price (HK$)` | 货币数值 | 价格核算变量 |
| 首日收盘价 | **Col 127**| `First trading day closing price (HK$)` | 货币数值 | 价格核算变量 |

### 6.7 经济学直觉与学术贡献
精准测算了香港主板真实且庞大的“隐性发行成本”，实证检验了 Loughran & Ritter (2002) 的行为心理账户理论在远东国际金融中心的适用边界。

---

## Idea 07: 生命周期公司治理：WVR 同股不同权、控制权两权分离与高管堑壕防御

### 7.1 研究课题与核心科学问题
- **研究课题**：香港第 8A 章同股不同权（WVR）与控制人投票权-经济利益分离（Controller Wedge），如何在企业 IPO 估值与首日定价中产生代理成本折价？
- **核心问题**：创始人兼任董事长与首席执行官（CEO Duality）是否强化了管理层堑壕防御（Entrenchment），导致外部机构投资者索要更高的安全边际与抑价补偿？

### 7.2 经典文献基准与美股经验事实
- **双重股权生命周期衰减假说 (Kim & Michaely 2017)**：
  - 初创期（高研发、高不确定性），双重股权保护创始人聚焦长期创新，享有估值溢价；
  - 随企业迈向成熟期（上市 5~10 年后），两权分离导致的控制权自利与利益输送（Tunneling）主导，转变为严峻的估值折价。
- **管理层防御与两权分离 (Gompers, Ishii, & Metrick 2010; Bebchuk et al. 2002)**：投票权与现金流权的分离度越大，控股股东转移公司资源的激励越强。

### 7.3 香港主板制度背景与样本微观现实
- **港交所制度特色**：2018 年增设第 8A 章允许特权股（一股最多享 10 票投票权），但未设立强制性的“固定年限时间日落条款（Time-based Sunset）”；
- **2026 Q1 数据分布**：
  - 样本涵盖多家同股不同权硬科技龙头；
  - 深度追踪控股股东的**经济利益持股比例（Economic Interest %）**与**投票权比例（Voting Rights %）**，构造纯净的控制权两权分离度指标（$\text{Wedge} = \text{Voting} - \text{Economic}$）。

### 7.4 待检验学术假说体系
- **$H_{7a}$（两权分离控制权折价假说）**：控股股东两权分离度（Wedge）越大的企业，外部机构投资者对未来代理冲突的担忧越强烈，要求更高的发售折让，表现为**发售定价更倾向于区间底格（`Pricing position == 'At low'`）及更高的首日抑价率补偿**。
- **$H_{7b}$（高管堑壕与经营波动放大假说）**：董事长与首席执行官合一（CEO Duality）的企业，在经历宏观行业下行时，其经营性现金流波动率与存货减值幅度显著高于治理制衡完备的企业。

### 7.5 规范计量经济学模型
#### 模型 7.1：两权分离跨度对首日抑价折让的回归方程 (OLS)
$$\begin{aligned}
\text{IR}_i = &\ \alpha_0 + \beta_1 (\text{VotingRights}_i - \text{EconomicInterest}_i) + \beta_2 \text{WVRFlag}_i \\
&+ \beta_3 \text{CEODuality}_i + \beta_4 \ln(\text{FirmAge}_i + 1) + \gamma \mathbf{X}_i + \varepsilon_i
\end{aligned}$$

### 7.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 首日抑价率 | **Col 128**| `First-day return / Underpricing (%)` | 数值百分比 | 被解释变量 (Y) |
| WVR 同股不同权标识 | **Col 76** | `WVR flag` | 0/1 虚拟变量 | 核心解释变量 |
| 控制人上市经济持股比 | **Col 68** | `Controller economic interest at listing (%)` | 数值百分比 | 两权分离基础变量 |
| 控制人上市投票权比 | **Col 69** | `Controller voting rights at listing (%)` | 数值百分比 | 两权分离基础变量 |
| 最终控制人类型 | **Col 67** | `Ultimate controller type` | 文本分类 | 分类控制变量 |
| 往绩经营性现金流 | **Col 50** | `Operating cash flow in year-1 (before annualization)`| 货币数值 | 财务健康度控制 |
| 公司成立年限 | **Col 82** | `Firm age at IPO (years)` | 数值浮点 | 生命周期控制变量 |

### 7.7 经济学直觉与学术贡献
突破了传统文献仅用虚拟变量衡量双重股权的局限，精确依托主表第 68 列与 69 列量化计算“两权分离连续跨度”，为香港主板 WVR 规则完善与日落条款设置提供经验证据。

---

## Idea 08: 宏观流动性周期、公开发售散户抽签狂热与公开市场信息吸收效率

### 8.1 研究课题与核心科学问题
- **研究课题**：香港本地银行间拆借利率（HIBOR）、银行体系结余及恒指公开大盘收益率，如何通过散户杠杆抽签传导至新股首日定价？
- **核心问题**：港股承销商的簿记建档机制能否像美股一样完全吸收大盘公开市场信息？公开发售的非理性散户超购倍数是否具有完全独立的超额回报预测能力？

### 8.2 经典文献基准与美股经验事实
- **市场情绪与发行热潮假说 (Lowry 2003)**：投资者情绪与宏观流动性对 IPO 密度的驱动效应远超过企业的实际资本投资需求；
- **公开信息吸收完全假说 (Lowry & Schwert 2004)**：完全有效的簿记建档应将招股期间的大盘指数公开收益完全内化至最终发售价中。因此，大盘收益对首日抑价应无任何增量预测力；
- **胜者诅咒模型 (Winner's Curse, Rock 1986)**：信息劣势散户在劣质发行中全额获配，在优质发行中被过度稀释。

### 8.3 香港主板制度背景与样本微观现实
- **散户抽签狂热**：2026 Q1 全样本公开发售超额认购倍数（`Subscription Ratio`）**均值达 1,438.5 倍（中位数 1,072.1 倍，最高达 5,297 倍）**；
- **主表包含完备的宏观金融时间序列变量**：招股日前 20 个交易日恒指回报（`col_hsi_return_20d`）、前 90 日主板 IPO 家数（`col_hk_ipo_count_90d`）、1 个月 HIBOR 拆借利率（`col_hibor_1m`）与香港银行体系总结余（`col_aggregate_balance`）。

### 8.4 待检验学术假说体系
- **$H_{8a}$（散户狂热情绪独立溢价假说）**：与美股机构主导逻辑不同，香港公开发售超购倍数对首日抑价具有极其强劲的独立正向预测力，即使控制了簿记建档价格修正幅度，散户狂热仍能产生显著超额估值溢价。
- **$H_{8b}$（大盘公开信息吸收不完全假说）**：在香港市场中，招股期间恒指累计回报并不能被发售价完全吸收（$\beta_2 > 0$），存在显著的信息传递时滞与抑价溢出。

### 8.5 规范计量经济学模型
#### 模型 8.1：公开信息与散户情绪分离实证方程 (OLS)
$$\begin{aligned}
\text{IR}_i = &\ \alpha_0 + \beta_1 \Delta P_i + \beta_2 \text{HSIReturn20d}_i + \beta_3 \ln(\text{SubscriptionRatio}_i) \\
&+ \beta_4 \text{HIBOR1m}_i + \beta_5 \ln(\text{BankingAggregateBalance}_i) + \beta_6 \text{IPOCount90d}_i + \varepsilon_i
\end{aligned}$$

### 8.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 首日抑价率 | **Col 128**| `First-day return / Underpricing (%)` | 数值百分比 | 被解释变量 (Y) |
| 公开发售超购倍数 | **Col 105**| `Subscription Ratio (times)` | 数值浮点 | 核心自变量 (散户情绪) |
| 招股前 20 日恒指收益率| **Col 123**| `HSI return over 20 trading days before prospectus (%)` | 数值百分比 | 核心自变量 (公开信息) |
| 前 90 日主板新股家数 | **Col 124**| `HK ordinary IPO count in 90 calendar days before prospectus`| 整数数值 | 宏观 IPO 浪潮变量 |
| 招股前 1 个月 HIBOR | **Col 125**| `1-month HIBOR before prospectus (%)` | 数值百分比 | 货币借贷成本变量 |
| 香港银行体系总结余 | **Col 126**| `Banking system aggregate balance before prospectus (HK$)` | 货币数值 | 宏观流动性底盘 |

### 8.7 经济学直觉与学术贡献
直接检验了 Lowry & Schwert (2004) 的经典假说在港股高散户参与度环境下的稳健性，揭示了远东离岸金融中心独特的“宏观流动性-杠杆孖展-二级市场首日狂欢”传导链条。

---

## Idea 09: 双重解禁日期的“筹码雪崩效应”：基石投资者 6 个月解禁 vs. 控股股东限售期满

### 9.1 研究课题与核心科学问题
- **研究课题**：香港主板上市后第 180 天（6 个月整），基石投资者的法定解禁与上市规则第 10.07 条控股股东第一阶段限售期满重合，如何诱发二级市场的“双重筹码雪崩（Double Avalanche）”与流动性冲击？
- **核心问题**：基石投资者与 Pre-IPO 机构投资者的异质性（外资长线基金 vs. 国内私募 VC），如何差异化地影响解禁窗口前后的非正常累计超额回报率（CAR）？

### 9.2 经典文献基准与美股经验事实
- **限售解禁效应 (Lockup Expiration, Field & Hanka 2001; Brav & Gompers 2003)**：
  - 美股 IPO 普遍存在 180 天自愿锁定协议；
  - 解禁窗口前后 3 天内，股价平均产生 **-1.5% 至 -3.0%** 的显著负向异常超额收益（Negative Abnormal Returns），伴随交易量剧增 40%；
  - VC 机构支持的上市企业在解禁时的下跌幅度（-2.8%）显著高于非 VC 支持企业。

### 9.3 香港主板制度背景与样本微观现实
- **港交所双重刚性锁定**：
  1. 《上市规则》第 10.07 条规定：控股股东自挂牌之日起 6 个月内不得处置任何股份（第一个 6 个月绝对禁售，第二个 6 个月不得丧失控股权）；
  2. 基石投资者在《基石投资协议》中法定承诺 6 个月绝对限售。
- **筹码雪崩集中爆发**：在上市后第 180 天，**基石股份（平均占总盘 38.3%）与控股股东原持股（平均占 50%~70%）在同一天同时进入可减持窗口**，二级市场不受限流动盘瞬间成倍暴增。主表第 104 列精准确证了每家公司的 `Earliest cornerstone unlock date`。

### 9.4 待检验学术假说体系
- **$H_{9a}$（双重解禁筹码雪崩假说）**：在上市后第 180 天窗口前后（$[-5, +5]$ 交易日），公司累计异常收益率（CAR）显著为负；且基石获配比例（`Final cornerstone allocation`）越高的个股，负向超额收益幅度越大。
- **$H_{9b}$（机构类型减持分化假说）**：由纯财务型 VC 作为基石投资者的个股，在解禁日的抛售动能和负向 CAR 显著强于由产业巨头（CVC）或国资战略资本背书的个股。

### 9.5 规范计量经济学模型
#### 模型 9.1：解禁窗口期累计异常回报率（CAR）回归方程 (OLS)
$$\begin{aligned}
\text{CAR}[-5, +5]_i = &\ \alpha_0 + \beta_1 \text{CornerstoneAllocationPct}_i + \beta_2 \text{TopTierVC}_i + \beta_3 \text{StateGovBacked}_i \\
&+ \beta_4 \text{IR}_i + \beta_5 \text{ControllerEconomicPct}_i + \gamma \mathbf{X}_i + \varepsilon_i
\end{aligned}$$

### 9.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 基石配售占基础发售比 | **Col 103**| `Final cornerstone allocation (% of base offer)` | 数值百分比 | 核心解释变量 (X) |
| 最早基石解禁法定日期 | **Col 104**| `Earliest cornerstone unlock date (dd/mm/yy)` | 日期字段 | 事件研究基准日 ($T_0$) |
| 顶尖机构背书标识 | **Col 61** | `Top-tier VC/PE backing (1=yes; 0=no)` | 0/1 虚拟变量 | 机构异质性调节变量 |
| 国资/政府引导基金标识| **Col 60** | `Pre-IPO State/Gov backing (1=yes; 0=no)` | 0/1 虚拟变量 | 稳定资金调节变量 |
| 控制人上市经济持股比 | **Col 68** | `Controller economic interest at listing (%)` | 数值百分比 | 筹码集中度控制 |
| 首日抑价率 | **Col 128**| `First-day return / Underpricing (%)` | 数值百分比 | 历史累计收益控制 |

### 9.7 经济学直觉与学术贡献
首次利用香港主板独有的 180 天“控股股东+基石投资者”双重刚性解禁事件窗口，检验了 Field & Hanka (2001) 的理论，为监管层评估基石投资者制度对二级市场长周期流动性的负外部性提供了核心实证依据。

---

## Idea 10: 商业银行系投行保荐与信贷关系认证效应

### 10.1 研究课题与核心科学问题
- **研究课题**：商业银行背景的投资银行（如中银国际、工银国际、建银国际、农银国际、交银国际、招银国际、汇丰等）担任独家或主要保荐人时，是否通过调动其商业银行母公司的企业私有信贷记录发挥“信贷认证效应（Lending Certification）”？
- **核心问题**：若新股募资用途主要是“偿还母行贷款（Debt Repayment）”，银行系保荐人是否存在严重的利益冲突，从而通过过度抑价以保障股票发售成功和贷款回笼？

### 10.2 经典文献基准与美股经验事实
- **信贷关系认证假说 (Lending Certification, Schenone 2004; Puri 1996)**：与发行人存在既往贷款关系的商业银行承销商，掌握企业的长期私有违约风险与现金流监控信息，能够有效降低信息不对称，使得新股发行折价显著收窄。
- **利益冲突假说 (Conflict of Interest, Gonzalez & James 2007)**：当承销商母行是发行人的主要债权人且企业财务杠杆极高时，银行具有强烈动机压低发售价以确保募资完成用于还债，引发严峻的代理冲突。

### 10.3 香港主板制度背景与样本微观现实
- **港股中资及外资大行保荐生态**：香港新股市场被各大商业银行系投行高度渗透；
- **2026 Q1 数据分布**：主表第 6 列记录了保荐人名单，第 70 列记录了上市前一年的有息负债（`Interest-bearing debt`），第 72 列记录了招股书明确声明用于“偿还银行债务的募集资金比例（`Debt repayment %`）”，提供了检验双重假说的绝佳指标。

### 10.4 待检验学术假说体系
- **$H_{10a}$（银行系保荐认证假说）**：在有息负债率适度的正常企业中，由商业银行系投行担任保荐人的 IPO，其首日抑价率显著低于独立券商或精品投行保荐的样本，体现了信贷私有信息的认证价值。
- **$H_{10b}$（偿还贷款利益冲突假说）**：当拟将募资净额的较高比例用于偿还有息债务（`Debt repayment %` 较高）时，银行系保荐人主导的项目首日抑价率反而显著上升，展现出“自保债权而压低发售价”的利益倾斜。

### 10.5 规范计量经济学模型
#### 模型 10.1：银行系保荐人与债务偿还交互对抑价的回归模型 (OLS)
$$\begin{aligned}
\text{IR}_i = &\ \alpha_0 + \beta_1 \text{BankAffiliatedSponsor}_i + \beta_2 \text{DebtRepaymentPct}_i \\
&+ \beta_3 (\text{BankAffiliatedSponsor}_i \times \text{DebtRepaymentPct}_i) \\
&+ \beta_4 \ln(\text{InterestBearingDebt}_i + 1) + \beta_5 \text{LeverageRatio}_i + \gamma \mathbf{X}_i + \varepsilon_i
\end{aligned}$$

### 10.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 首日抑价率 | **Col 128**| `First-day return / Underpricing (%)` | 数值百分比 | 被解释变量 (Y) |
| 保荐人团队名单 | **Col 6**  | `Sponsor(s)` | 文本列表 | 银行系保荐识别源 (X) |
| 上市前有息负债总额 | **Col 70** | `Interest-bearing debt at year-1 end` | 货币数值 | 负债规模变量 |
| 偿还债务拟用募资占比 | **Col 72** | `Debt repayment (% of planned net IPO proceeds)` | 数值百分比 | 利益冲突核心变量 (X) |
| 发售价格修正幅度 | **Col 22** | `Filing price revision (%)` | 数值百分比 | 簿记建档控制变量 |
| 最终发行人净募资额 | **Col 117**| `Net IPO proceeds to issuer (HK$)` | 货币数值 | 发行规模控制变量 |

### 10.7 经济学直觉与学术贡献
直接回应了 Lowry et al. (2017 Ch 3) 对商业银行介入投行业务后“认证效应 vs. 债权利益冲突”的经典论辩，以港股详尽的募资偿债用途披露填补了微观机制的实证空白。

---

## Idea 11: 承销商场内托单与 30 天稳价期结束后的“悬崖效应”

### 11.1 研究课题与核心科学问题
- **研究课题**：承销商在上市首 30 天法定期限内利用绿鞋机制进行“场内低位托单（Price Support）”，如何在二级市场构筑虚假的人造价格底线？
- **核心问题**：在法定期限届满（Day 31）稳价人（Stabilizing Manager）彻底撤除托单后，疲弱个股是否会产生急剧的“悬崖式暴跌（Price Cliff）”？

### 11.2 经典文献基准与美股经验事实
- **价格支持与非对称托底 (Price Support, Ellis, Michaely, & O'Hara 2000)**：
  - 承销商对于交易疲软或跌破发行价的新股，会动用超额配售所建立的空头头寸在买一价持续挂单承接；
  - 托单行为显著扭曲了上市初期的真实价格发现，使得冷门股的下行风险被暂时掩盖。
- **美股事实**：破发新股在承销商停止托单后的第一周内，往往补跌 **5% 至 10%**。

### 11.3 香港主板制度背景与样本微观现实
- **港交所稳价期规定**：稳价人依据《证券及期货（稳定价格）规则》行使权力，稳价期从招股书刊发日或上市日起计，**最长不得超过 30 个自然日**；稳价期结束时必须发布法定《稳价行动及绿鞋失效公告》；
- **2026 Q1 数据分布异化**：
  - 38 家样本中，**多达 21 家公司的绿鞋实际行使比例为 0%（`Greenshoe exercise rate == 0.0`）**；
  - 这意味着在这 21 家公司中，承销商超额配售的 15% 股份全部转化为场内低位买入平仓，提供了巨大的虚假买盘托底支撑。

### 11.4 待检验学术假说体系
- **$H_{11a}$（30 天法定期人造价格支撑假说）**：在绿鞋行使率为 0% 的个股中，上市首 30 天内日均收盘价紧贴发售价（波动率极低），显著受到稳价人买盘的人为维稳干预。
- **$H_{11b}$（稳价期届满悬崖补跌假说）**：在上市后第 31 至 45 个交易日内，失去稳价人资金护盘的疲弱个股会出现显著的负向超额收益（CAR[+31, +45] < 0），且超额回撤幅度与绿鞋未行使比例（场内回购股票比例）呈显著正相关。

### 11.5 规范计量经济学模型
#### 模型 11.1：稳价期结束后累计异常收益（CAR[+31, +45]）回归模型 (OLS)
$$\begin{aligned}
\text{CAR}[+31, +45]_i = &\ \alpha_0 + \beta_1 (1 - \text{GreenshoeRate}_i) + \beta_2 \text{IR}_i + \beta_3 \text{UnderwriterPrestige}_i \\
&+ \beta_4 \text{UnrestrictedFloatPct}_i + \gamma \mathbf{X}_i + \varepsilon_i
\end{aligned}$$

### 11.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 绿鞋实际行使比例 | **Col 115**| `Greenshoe exercise rate (%)` | 数值百分比 | 核心自变量 (X) |
| 实际发行超额配售股数 | **Col 114**| `Over-allotment shares actually issued` | 整数数值 | 绿鞋执行结果 |
| 招股书最大超额配售权比| **Col 46** | `Over-allotment Option (%)` | 数值百分比 | 契约授权上限 |
| 上市首日收盘价 | **Col 127**| `First trading day closing price (HK$)` | 货币数值 | 价格比较基准 |
| 首日抑价率 | **Col 128**| `First-day return / Underpricing (%)` | 数值百分比 | 首日表现控制 |
| 首日不受限自由流通比 | **Col 120**| `Unrestricted public shareholding at listing (%)`| 数值百分比 | 流动性控制变量 |

### 11.7 经济学直觉与学术贡献
为 Ellis et al. (2000) 价格支持理论提供了精准的自然实验场景。利用港交所强制披露的 30 天法定稳价结束节点，清晰测度了“承销商隐性护盘资金撤出”对二级市场微观流动性与资产重定价的因果冲击。

---

## Idea 12: 招股书文本诉讼保险与跨国监管风险对冲

### 12.1 研究课题与核心科学问题
- **研究课题**：香港上市招股书中详尽冗长的“风险因素（Risk Factors）”文本篇幅、特异性（Idiosyncratic Risk）与制式化免责条款（Boilerplate），如何作为法律诉讼保险与跨国监管风险（如中国证监会境外备案、海外出口管制、生物安全审查）的对冲工具？
- **核心问题**：招股书风险披露的详尽程度是真正降低了事前估值不确定性（信息增量假说），还是仅仅被用作防范投资者事后诉讼的法律保护伞（诉讼保险假说）？

### 12.2 经典文献基准与美股经验事实
- **诉讼保险假说 (Lawsuit Avoidance, Tinic 1988; Lowry & Shu 2002)**：
  - 发行人面临潜在诉讼风险越高时，越倾向于通过高抑价向投资者让利，以降低上市后虚假陈述诉讼的发生率和赔付额；
- **文本信息披露与区间调整 (Hanley & Hoberg 2012)**：
  - 招股书中包含的信息增量（Informative Text）有助于承销商在簿记建档中精准定价，减少对首日抑价的被动依赖；
  - 制式化样本语句（Boilerplate）对信息提取毫无帮助。

### 12.3 香港主板制度背景与样本微观现实
- **地缘与监管跨国双重夹击**：香港上市公司面临中资监管合规、境外投资者跨国法律维权（普通法系下的虚假陈述责任）以及 18A/18C 硬科技的技术断供风险；
- **招股书结构特征**：招股书“风险因素”章节动辄长达 60~120 页，包含业务风险、行业政策风险、地缘政治与外汇管制风险。

### 12.4 待检验学术假说体系
- **$H_{12a}$（特异性风险信息增量假说）**：招股书中针对前沿技术研发（18A/18C）的特异性风险披露越深入、篇幅越充实，越能有效消除二级市场的信息不对称，从而收窄初步询价区间宽度（`Filing range width (%)`）。
- **$H_{12b}$（制式化诉讼保险替代假说）**：充斥大量免责制式词汇的冗长风险披露，并不降低估值不确定性，反而与高首日抑价率同向膨胀，展现出以高抑价配合文本免责作为诉讼双重保险的自保特征。

### 12.5 规范计量经济学模型
#### 模型 12.1：文本风险披露对发售估值区间与抑价的影响 (OLS)
$$\begin{aligned}
\text{RangeWidth}_i = &\ \alpha_0 + \beta_1 \text{InformativeRiskLength}_i + \beta_2 \text{BoilerplateScore}_i \\
&+ \beta_3 \text{Chapter18C}_i + \beta_4 \text{APlusH}_i + \beta_5 \ln(\text{ListingExpenses}_i) + \varepsilon_i
\end{aligned}$$

$$\begin{aligned}
\text{IR}_i = &\ \theta_0 + \theta_1 \text{BoilerplateScore}_i + \theta_2 \text{InformativeRiskLength}_i \\
&+ \theta_3 \text{ListingExpenses}_i + \mathbf{\Gamma} \mathbf{X}_i + \mu_i
\end{aligned}$$

### 12.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 发售区间相对宽度 | **Col 23** | `Filing range width (%)` | 数值百分比 | 模型 12.1 被解释变量 (Y) |
| 首日抑价率 | **Col 128**| `First-day return / Underpricing (%)` | 数值百分比 | 模型 12.2 被解释变量 (Y) |
| 显性总上市开支 | **Col 101**| `Listing expenses (HK$)` | 货币数值 | 律所中介法律成本控制 |
| 18C 特专科技标识 | **Col 78** | `Chapter 18C flag` | 0/1 虚拟变量 | 高风险监管通道控制 |
| 18A 生物科技标识 | **Col 77** | `Chapter 18A flag` | 0/1 虚拟变量 | 医药研发风险控制 |
| A+H 双重上市标识 | **Col 75** | `A+H issuer flag` | 0/1 虚拟变量 | 跨境监管风险控制 |

### 12.7 经济学直觉与学术贡献
将 Hanley & Hoberg (2012) 与 Lowry & Shu (2002) 的文本实证范式引入香港资本市场，量化分析在中美跨境监管博弈背景下，中国科技企业赴港上市如何通过文本工程平衡信息披露与诉讼防御。

---

## Idea 13: 散户“孖展”杠杆融资狂热与信息瀑布羊群效应

### 13.1 研究课题与核心科学问题
- **研究课题**：香港独具特色的散户券商“孖展（Margin Financing）”高倍杠杆借贷打新，如何在公开发售招股期间催生“信息瀑布（Information Cascades）”与羊群效应（Herding Behavior）？
- **核心问题**：招股首日的孖展认购数据公布后，是否引发了后序投资者的非理性盲从？极度膨胀的散户杠杆认购如何放大上市首日的日内暴涨与翻转破发风险？

### 13.2 经典文献基准与美股经验事实
- **信息瀑布理论 (Information Cascades, Bikhchandani, Hirshleifer, & Welch 1992; Welch 1992)**：
  - 后续决策者观察到先验决策者的集体行为（如排队疯抢），会理性地忽略自己的私有低估值信号，选择盲从跟投，形成脆弱的信息瀑布。
- **散户投机与过度认购 (Amihud, Hauser, & Kirsh 2003)**：
  - 极端超额认购往往伴随着日内流动性博傻，上市首日开盘即透支全部估值空间，随后伴随巨幅反转。

### 13.3 香港主板制度背景与样本微观现实
- **港式打新生态**：香港互联网券商（富途、老虎、辉立、耀才等）为散户提供高达 10 倍至 20 倍的孖展杠杆融资，并在招股期间每天向全市场公开各大券商累计借出的孖展资金总额；
- **2026 Q1 数据事实**：
  - 38 家样本平均公开发售超额认购倍数高达 **1,438.5 倍**；
  - 主表第 106 列追踪了公开发售申请总人数（`Public applicants`），第 107 列记录了有效申购总股数（`Public valid applied shares`），第 125 列记录了 1 个月 HIBOR 借贷成本。

### 13.4 待检验学术假说体系
- **$H_{13a}$（孖展发酵与信息瀑布非线性加速假说）**：招股首日券商孖展倍数越高，招股后两日散户有效申购股数呈超线性的指数级爆发，反映出典型的信息瀑布羊群踩踏效应。
- **$H_{13b}$（杠杆退潮与日内极端振幅假说）**：由极度高额的孖展超购所堆积的 IPO，其上市首日的盘中振幅（`High - Low`）与换手率显著偏高；由于获配散户面临极高的借贷利息成本，首日翻转抛售意愿极其强烈。

### 13.5 规范计量经济学模型
#### 模型 13.1：散户超购对首日盘中价格极端振幅的影响 (OLS)
$$\begin{aligned}
\text{IntradayVolatility}_i = &\ \alpha_0 + \beta_1 \ln(\text{SubscriptionRatio}_i) + \beta_2 \ln(\text{PublicApplicants}_i) \\
&+ \beta_3 \text{HIBOR1m}_i + \beta_4 \text{UnrestrictedFloatPct}_i + \gamma \mathbf{X}_i + \varepsilon_i
\end{aligned}$$
其中 $\text{IntradayVolatility}_i = \frac{P_{i, \text{high}} - P_{i, \text{low}}}{P_{i, \text{offer}}}$。

### 13.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 首日最高价 | **Col 131**| `First trading day high (HK$)` | 货币数值 | 盘中振幅核算分子 |
| 首日最低价 | **Col 132**| `First trading day low (HK$)` | 货币数值 | 盘中振幅核算分子 |
| 最终发售价 | **Col 11** | ` IPO Subscription Price (HK$)` | 货币数值 | 盘中振幅分母 |
| 公开发售超购倍数 | **Col 105**| `Subscription Ratio (times)` | 数值浮点 | 核心自变量 (X) |
| 公开发售有效申请人数 | **Col 106**| `Public applicants` | 整数数值 | 散户广度指标 |
| 公开发售有效申购股数 | **Col 107**| `Public valid applied shares` | 整数数值 | 散户申购体量指标 |
| 招股前 1 个月 HIBOR | **Col 125**| `1-month HIBOR before prospectus (%)` | 数值百分比 | 孖展杠杆利息成本 |
| 首日翻转抛售率 | **Col 134**| `First-day flipping ratio (%)` | 数值百分比 | 散户抛售行为变量 |

### 13.7 经济学直觉与学术贡献
将 Welch (1992) 的信息瀑布理论与香港独特的孖展打新融资格局深度结合，实证揭示了杠杆利息成本如何成为引爆散户首日不计成本抛售的微观催化剂。

---

## Idea 14: 跨界基金（Crossover Funds）双重身份：Pre-IPO 股东兼任基石的信号传递与利益冲突

### 14.1 研究课题与核心科学问题
- **研究课题**：跨界基金（如博裕资本、高瓴资本、启明创投、OrbiMed 等）在拟上市企业中同时兼任“Pre-IPO 存量股东”与“IPO 基石投资者”的双重身份，向市场传递了何种信号？
- **核心问题**：这一现象究竟是成熟机构用真金白银再度加码认购的“极致质量信誉背书”，还是存量老股东为了护航 IPO 顺利发行、掩护其他早期轮次股东借机套现的“托底共谋”？

### 14.2 经典文献基准与美股经验事实
- **跨界基金治理与定价理论 (Crossover Investors, Kwon, Lowry, & Qian 2017; Chemmanur et al. 2014)**：
  - 传统公募互惠基金或对冲基金在上市前提前入局成为跨界投资者；
  - 跨界基金不仅提供了充沛的成长期非公开资本，而且其在新股发行中的积极参与显著提升了上市成功率与机构簿记覆盖率。
- **老股变现与道德风险 (Secondary Shares Selling, Lowry et al. 2017 Ch 2)**：若上市发行中包含老股东减持（Sale Shares），通常被市场视为负面内部人套现信号。

### 14.3 香港主板制度背景与样本微观现实
- **港股跨界双重身份常态**：在 18A 生物科技与 18C 特专科技板块中，大量知名专业医疗/硬科技基金既出现在招股书历史 Pre-IPO 股东名册中，又出现在基石投资者认购名单中；
- **2026 Q1 数据深度**：主表第 62 列记录了 `Key Pre-IPO investors`，第 102 列详细记录了 `Cornerstone investor names`，两者的文本交集构成了精准的跨界双重身份指标。

### 14.4 待检验学术假说体系
- **$H_{14a}$（跨界再加码强认证假说）**：既往 Pre-IPO 机构投资者自愿以基石投资者身份额外追加资金认购新发行股份的个股，向二级市场传递了极强的内部信心背书，其初步询价区间更窄，首日抑价率显著更低。
- **$H_{14b}$（老股掩护与利益冲突假说）**：若在跨界基金出任基石的同时，公司发售结构中包含了大量老股转让（`Sale Shares > 0`），其对抑价的平抑效应消失，二级市场将其判定为掩护早期资本出逃的信号，导致二级市场交易破发率显著上升。

### 14.5 规范计量经济学模型
#### 模型 14.1：跨界双重身份对发售定价与抑价的实证模型 (OLS)
$$\begin{aligned}
\text{IR}_i = &\ \alpha_0 + \beta_1 \text{DualRoleCrossover}_i + \beta_2 \text{SaleSharesFlag}_i \\
&+ \beta_3 (\text{DualRoleCrossover}_i \times \text{SaleSharesFlag}_i) \\
&+ \beta_4 \text{PreIPOHoldingYears}_i + \gamma \mathbf{X}_i + \varepsilon_i
\end{aligned}$$

### 14.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 首日抑价率 | **Col 128**| `First-day return / Underpricing (%)` | 数值百分比 | 被解释变量 (Y) |
| Pre-IPO 关键投资人名单| **Col 62** | `Key Pre-IPO investors` | 文本列表 | 跨界交集提取源 (X) |
| 基石投资者法定名单 | **Col 102**| `Cornerstone investor names` | 文本列表 | 跨界交集提取源 (X) |
| 老股发售转让数量 | **Col 16** | `Sale Shares` | 整数数值 | 老股东套现核心变量 |
| 机构最早入股持有年限 | **Col 66** | `Pre-IPO holding duration (years)` | 数值浮点 | 资本沉淀年限控制 |
| 顶级机构背书标识 | **Col 61** | `Top-tier VC/PE backing (1=yes; 0=no)` | 0/1 虚拟变量 | 机构声誉控制变量 |

### 14.7 经济学直觉与学术贡献
拓展了 Kwon, Lowry, & Qian (2017) 的跨界投资者假说，在港股特有的基石法定锁定期架构下，首次测算了同一资本在“一级半市场”多重身份切换时的微观经济学信号净值。

---

## Idea 15: 大客户集中度、专用性资产投资与创始人控制权绑定

### 15.1 研究课题与核心科学问题
- **研究课题**：高科技与生物医药企业在上市前极高的大客户集中度（Top 5 Customer Revenue Concentration），如何驱动企业在公司治理结构中采用双重股权（WVR）与控制权绑定？
- **核心问题**：关系专用性资产投资（Relationship-Specific Investment）是否促使创始团队构建更高的控制权两权分离壕沟以抵御外部恶意收购与客户敲竹杠（Hold-up）？

### 15.2 经典文献基准与美股经验事实
- **专用性投资与防御性治理契约 (Johnson, Karpoff, & Yi 2015; Titman 1984)**：
  - 拥有重要商业伙伴（大客户、核心供应商）的企业，更倾向于在上市时设立强有力的反收购条款（Takeover Defenses）和双重股权结构；
  - 这种治理壕沟能够保护企业与大客户之间沉淀的长期专用性契约不被短期掠夺性收购破坏。
- **客户集中度与融资成本 (Campello & Gao 2017)**：客户集中度过高的企业面临更高的经营现金流脆弱性，资本市场索要更高的风险补偿。

### 15.3 香港主板制度背景与样本微观现实
- **2026 Q1 数据分布核心指标**：主表第 54 列严谨追踪了每家企业上市前一年的**前五大客户销售额占比（`Top 5 customers (% of year-1 revenue)`）**；
- 样本中硬科技与供应链上游芯片企业的前五大客户集中度普遍高达 **40% 至 85%**，构成了极佳的截面方差。

### 15.4 待检验学术假说体系
- **$H_{15a}$（客户专用性与控制权绑定假说）**：前五大客户集中度（`Top 5 customers %`）越高的企业，上市时创始人越倾向于采用第 8A 章同股不同权（WVR）架构，并构建更高的投票权-经济利益分离跨度（$\text{Voting} - \text{Economic}$）。
- **$H_{15b}$（客户集中度与事前发售区间发散假说）**：前五大客户集中度越高的企业，由于经营业务极易受到单一大客户订单流失的剧烈冲击，其事前估值不确定性更高，表现为更宽的发售区间（`Filing range width (%)`）。

### 15.5 规范计量经济学模型
#### 模型 15.1：大客户集中度对 WVR 治理选择的 Logistic 回归
$$\text{Logit}\left(\text{Prob}(\text{WVRFlag}_i = 1)\right) = \alpha_0 + \beta_1 \text{Top5CustomerPct}_i + \beta_2 \ln(\text{RDExpensed}_i + 1) + \beta_3 \ln(\text{FirmAge}_i + 1) + \gamma \mathbf{X}_i$$

#### 模型 15.2：大客户集中度对估值区间相对宽度的影响 (OLS)
$$\text{RangeWidth}_i = \theta_0 + \theta_1 \text{Top5CustomerPct}_i + \theta_2 \text{OperatingCashFlow}_i + \theta_3 \ln(\text{NetSales}_i) + \mathbf{\Gamma} \mathbf{Z}_i + \varepsilon_i$$

### 15.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 前五大客户营收占比 | **Col 54** | `Top 5 customers (% of year-1 revenue)` | 数值百分比 | 核心自变量 (X) |
| WVR 同股不同权标识 | **Col 76** | `WVR flag` | 0/1 虚拟变量 | 模型 15.1 被解释变量 (Y) |
| 发售区间相对宽度 | **Col 23** | `Filing range width (%)` | 数值百分比 | 模型 15.2 被解释变量 (Y) |
| 控制人上市投票权比 | **Col 69** | `Controller voting rights at listing (%)` | 数值百分比 | 控制权绑定变量 |
| 控制人上市经济持股比 | **Col 68** | `Controller economic interest at listing (%)` | 数值百分比 | 控制权绑定变量 |
| 往绩最近一年营收总额 | **Col 37** | `Net sales in year-1` | 货币数值 | 经营规模控制变量 |
| 往绩经营性现金流 | **Col 50** | `Operating cash flow in year-1 (before annualization)`| 货币数值 | 经营风险控制变量 |

### 15.7 经济学直觉与学术贡献
直接连通了产业组织理论中的“不完全契约敲竹杠模型（Grossman & Hart 1986）”与公司金融中的“生命周期治理选择理论（Johnson et al. 2015）”，为理解香港主板高科技企业为何坚定捍卫同股不同权提供了坚实的微观产业基础。

---

## Idea 16: 同行业科技竞品防御性上市浪潮与估值溢出

### 16.1 研究课题与核心科学问题
- **研究课题**：处于同一垂直高科技细分赛道的竞品公司（如 GPU 芯片领域的壁仞科技 vs. 天数智芯；通用大模型领域的智谱华章 vs. MiniMax），为何在时间上呈现出密集的“结伴成群防御性上市（Rival Preemption Waves）”？
- **核心问题**：率先完成上市的行业领头羊（First-Mover），是否为后序跟进上市的竞品公司确立了关键的“估值价格锚”，从而消除信息不对称并压缩后者的区间宽度？

### 16.2 经典文献基准与美股经验事实
- **先发优势与产品市场防御性上市 (Chemmanur & He 2011; Spiegel & Tookes 2020)**：
  - 企业上市不仅为了融资，更为了通过先发公开挂牌树立行业知名度，夺取产品市场份额（Product Market Share）；
  - 这种先发优势会迫使竞争对手即使在估值折价的不利环境下，也必须跟进上市以免在行业整合中出局。
- **行业信息外溢与上市浪潮 (IPO Clusters, Lowry 2003; Benveniste et al. 2003)**：同一行业首家企业的询价过程生产了大量的宏观与行业私有信号，产生正外部性。

### 16.3 香港主板制度背景与样本微观现实
- **2026 Q1 特专科技风口集群**：香港第 18C 章正式开放后，中国头部生成式 AI、AI 芯片及具身智能机器人独角兽在 2025 年底至 2026 年初集中向港交所提交招股书并密集挂牌；
- **2026 Q1 样本分布**：主表第 47 列（主营业务行业）、第 78 列（18C 标识）与第 4 列（招股书日期）完整记录了行业竞品的时间先后序。

### 16.4 待检验学术假说体系
- **$H_{16a}$（行业领头羊先发募资优势假说）**：在垂直硬科技赛道中，率先完成上市的第一家龙头企业，其实际募集资金净额、估值溢价率及机构认购覆盖度显著高于紧随其后的追赶者。
- **$H_{16b}$（行业信息溢出与估值区间收敛假说）**：首家龙头企业的成功上市为该细分赛道提供了公开的市场定价基准。因此，后序紧跟上市的同业竞品，其事前询价区间相对宽度（`Filing range width (%)`）显著收窄，呈现出明显的信息溢出吸收效应。

### 16.5 规范计量经济学模型
#### 模型 16.1：行业上市先后序对发售规模与区间宽度的回归模型 (OLS)
$$\text{RangeWidth}_i = \alpha_0 + \beta_1 \text{FollowerOrderDummy}_i + \beta_2 \text{DaysSinceLeaderListed}_i + \beta_3 \ln(\text{RDExpensed}_i + 1) + \gamma \mathbf{X}_i + \varepsilon_i$$

### 16.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 发售区间相对宽度 | **Col 23** | `Filing range width (%)` | 数值百分比 | 模型 16.1 被解释变量 (Y) |
| 最终发行人净募资额 | **Col 117**| `Net IPO proceeds to issuer (HK$)` | 货币数值 | 募资先发优势因变量 |
| 招股书刊登日期 | **Col 4**  | `Date of Prospectus (dd/mm/yy)` | 日期字段 | 时间先后序判定基准 |
| 行业分类代码 | **Col 79** | `Industry classification code` | 文本编码 | 赛道集群配对变量 |
| 18C 特专科技标识 | **Col 78** | `Chapter 18C flag` | 0/1 虚拟变量 | 硬科技集群标识 |
| 往绩研发开支 | **Col 52** | `R&D expensed in year-1 (before annualization)` | 货币数值 | 科技含金量控制 |

### 16.7 经济学直觉与学术贡献
将 Spiegel & Tookes (2020) 的“产品市场竞争与上市时机博弈模型”置于香港 18C 硬科技上市潮中检验，阐明了在资本寒冬背景下硬科技独角兽“抢滩港股”的防御性博弈逻辑。

---

## Idea 17: 卖方明星分析师覆盖与抑价“隐性贿赂”假说

### 17.1 研究课题与核心科学问题
- **研究课题**：香港 IPO 发行人聘用知名外资或中资头部保荐人（如摩根士丹利、高盛、中金公司、中信证券）并容忍巨额首日抑价，是否是为了换取这些顶级投行内部“新财富/《机构投资者》全明星分析师”在上市后的积极研报覆盖？
- **核心问题**：首日抑价让利是否构成发行人向承销商研究部门支付的“隐性买路钱（Analyst Lust）”？

### 17.2 经典文献基准与美股经验事实
- **分析师覆盖买路钱假说 (Analyst Lust, Loughran & Ritter 2004; Cliff & Denis 2004)**：
  - 发行人并不厌恶留存高额抑价，其核心诉求之一是锁定全明星卖方分析师在上市静默期（Quiet Period）结束后的“买入（Buy）”评级与高目标价；
  - 拥有顶尖明星分析师覆盖的企业，平均多让渡了 **15%** 的首日抑价率。
- **更换主承销商的惩罚 (Krigman, Shaw, & Womack 2001)**：若企业后续增发（SEO）更换主承，原分析师会迅速下调评级。

### 17.3 香港主板制度背景与样本微观现实
- **港股卖方研究话语权**：香港是高度机构化的离岸资本市场，外资长线资金与对冲基金极其依赖投行卖方研究团队的开篇研报（Initiation of Coverage）；
- **2026 Q1 数据事实**：主表第 6 列记录了保荐人，第 129 列记录了留在桌面上的财富，第 135 列记录了首日二级市场全天成交金额（`Turnover HK$`），反映了投行号召力对流动性的直接调动。

### 17.4 待检验学术假说体系
- **$H_{17a}$（明星分析师抑价置换假说）**：由拥有行业顶尖卖方研究团队的高声誉保荐人（`Top-tier Sponsor`）主导的项目，其首日抑价率与留在桌面上的财富显著高于中小型精品投行项目，验证发行人以抑价置换研究声量的逻辑。
- **$H_{17b}$（研报覆盖流动性溢价假说）**：由顶级投行保荐并留存高额财富的项目，其上市首月二级市场的机构换手率与交易深度显著更优，证实了卖方分析师对二级市场定价效率的持续激活。

### 17.5 规范计量经济学模型
#### 模型 17.1：保荐人声誉与首日财富留存的联立方程系统 (2SLS)
$$\begin{aligned}
\ln(\text{MoneyLeft}_i) = &\ \alpha_0 + \beta_1 \text{TopTierSponsor}_i + \beta_2 \ln(\text{Proceeds}_i) + \beta_3 \Delta P_i \\
&+ \beta_4 \text{InstitutionalShareholdingPct}_i + \gamma \mathbf{X}_i + \varepsilon_i
\end{aligned}$$

### 17.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 留在桌面上的财富 | **Col 129**| `Money left on the table (HK$)` | 货币数值 | 被解释变量 (Y) |
| 首日抑价率 | **Col 128**| `First-day return / Underpricing (%)` | 数值百分比 | 备选被解释变量 |
| 保荐人团队名单 | **Col 6**  | `Sponsor(s)` | 文本列表 | 明星投行识别源 (X) |
| 首日成交金额 | **Col 135**| `First trading day turnover (HK$)` | 货币数值 | 二级市场流动性因变量 |
| 发售价格修正幅度 | **Col 22** | `Filing price revision (%)` | 数值百分比 | 簿记控制变量 |
| 上市前机构持股比例 | **Col 63** | `Pre-IPO institutional shareholding (%)` | 数值百分比 | 机构偏好控制变量 |

### 17.7 经济学直觉与学术贡献
将 Loughran & Ritter (2004) 的分析师狂热假说移植至以中环外资大行与中资头部券商并存的香港资本市场，量化了“卖方研报覆盖”这一软性资产在 IPO 抑价契约中的隐性定价对价。

---

## Idea 18: 发行费用分拆中的“软美元寻租”：固定承销佣金 vs. 酌情奖励费率博弈

### 18.1 研究课题与核心科学问题
- **研究课题**：香港主板招股书中披露的承销总费率中，固定承销佣金（Fixed Underwriting Commission %）与全权酌情奖励费率（Discretionary Incentive Fee %）的比例构成，如何影响保荐人的承销努力程度与发售定价落点？
- **核心问题**：全权酌情奖金池是否有效缓解了投行与发行人之间的代理冲突？在超大承销团中，酌情奖金是否沦为主承销商排挤普通副承销商的“软美元寻租工具”？

### 18.2 经典文献基准与美股经验事实
- **承销佣金契约理论 (Underwriting Contract Structure, Chen & Ritter 2000; Goldstein et al. 2011)**：
  - 美股 90% 以上的中小市值 IPO 佣金率被严格固定在 **7%**（The 7% gross spread clustering）；而在大型百亿美元项目中佣金降至 2%~3%；
  - 美股较少在公开合同中拆分“酌情奖金”，多通过后续二级市场经纪分仓佣金（Soft Dollars）进行隐性利益输送。

### 18.3 香港主板制度背景与样本微观现实
- **港式双轨公开费率结构**：
  - 招股书 UNDERWRITING 章节严格披露承销商费用分为两层：
    1. **固定承销佣金率**（通常为 1.5% 至 2.5%，记录于主表第 44 与 45 列）；
    2. **全权酌情奖励费率**（通常为 0.5% 至 1.5%），由发行人董事会在上市后根据其对各保荐人定价销售表现的主观考核自由分配；
- **2026 Q1 数据事实**：主表第 101 列精准核算了总上市现金开支，第 24 列记录了发售价落点（`Pricing position`）。

### 18.4 待检验学术假说体系
- **$H_{18a}$（酌情奖金的绩效激励效应假说）**：酌情奖励费率在总承销费中占比越高的企业，保荐人为了争取该笔浮动奖金，越有动力在簿记建档中顶格推价，促使最终发售价落在询价区间顶端（`Pricing position == 'At high'`）。
- **$H_{18b}$（大盘股辛迪加利益分肥假说）**：在聘请了庞大联席账簿管理人（JBR）的超级项目中，发行人倾向于大幅提高酌情奖金池的比例，将其作为甄别承销商真实下单贡献、抑制辛迪加内部搭便车的有效治理契约。

### 18.5 规范计量经济学模型
#### 模型 18.1：酌情奖励费率对最终发售价顶格落点的 Logistic 模型
$$\text{Logit}\left(\text{Prob}(\text{PricingPosition}_i = \text{'At high'})\right) = \alpha_0 + \beta_1 \text{DiscretionaryIncentivePct}_i + \beta_2 \ln(\text{SubscriptionRatio}_i) + \beta_3 \ln(\text{Proceeds}_i) + \gamma \mathbf{X}_i$$

#### 模型 18.2：费用分拆结构对留在桌面上的财富的影响 (OLS)
$$\ln(\text{MoneyLeft}_i) = \theta_0 + \theta_1 \text{DiscretionaryIncentivePct}_i + \theta_2 \text{FixedCommissionPct}_i + \theta_3 \Delta P_i + \mathbf{\Gamma} \mathbf{Z}_i + \varepsilon_i$$

### 18.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 定价落点分类 | **Col 24** | `Pricing position in filing range` | 文本分类 | 模型 18.1 被解释变量 (Y) |
| 留在桌面上的财富 | **Col 129**| `Money left on the table (HK$)` | 货币数值 | 模型 18.2 被解释变量 (Y) |
| 香港公开发售承销佣金率| **Col 44** | `Underwriting Commission (% of fund raised HK (a)` | 数值百分比 | 核心自变量 (固定佣金) |
| 国际配售承销佣金率 | **Col 45** | `Underwriting Commission (% of fund raised Int.(b)` | 数值百分比 | 核心自变量 (固定佣金) |
| 显性总上市开支 | **Col 101**| `Listing expenses (HK$)` | 货币数值 | 总显性成本控制变量 |
| 公开发售超购倍数 | **Col 105**| `Subscription Ratio (times)` | 数值浮点 | 市场认购需求控制 |
| 最终发行人净募资额 | **Col 117**| `Net IPO proceeds to issuer (HK$)` | 货币数值 | 发行规模控制变量 |

### 18.7 经济学直觉与学术贡献
首次利用香港招股书独有的“固定佣金 vs. 酌情奖金”明细披露，突破了美股 7% 粗糙费率的理论瓶颈，从委托-代理理论（Principal-Agent Theory）视角为投资银行激励契约设计提供了开创性的实证度量。

---

## Idea 19: 卖方跨期期望效用最大化与“理性抑价”：发行流产保险、解禁期多阶段套现与激励相容信息租金

### 19.1 研究课题与核心科学问题
- **研究课题**：为什么表面上看似导致发行人遭受巨额“财富流失（Money Left on the Table）”的 IPO 首日抑价，在动态博弈与跨期效用最优化框架下，反而是卖方（拟上市公司原股东、管理层与承销商投行）的主动最优策略？
- **核心问题**：
  1. 拟上市公司原股东与投行如何权衡“多融 10% 资金”与“交易彻底流产（Broken Deal）的灭顶之灾”？抑价作为一种“发行成功保险费”，其边际对冲价值如何受企业前期沉没成本与破产压力的驱动？
  2. IPO 通常仅发售总股本的 10%~25%，原股东持有 75%~90% 的绝大多数筹码被锁定至 6 个月甚至数年后。原股东如何通过在 IPO 当天适度让利营造“开门红（IPO Pop）”与口碑，以换取解禁期后巨额存量股份在大宗交易与后续增发（FPO/SEO）中的流动性溢价与高估值变现？
  3. 投行在面对“单次博弈发行人”与“长线重复博弈买方机构（BlackRock、Fidelity 等）”时，如何利用自主配售权与抑价配额进行隐性利益输送以换取长久交易佣金（Soft Dollars）？
  4. 簿记建档中，投行为了诱导掌握私有真实估值信息的买方机构如实申报需求，如何依据机制设计（Mechanism Design）的激励相容约束（Incentive Compatibility, IC），必须在最终定价中向机构让渡正的信息租金（Information Rents）？

### 19.2 经典文献基准与美股经验事实
- **发行流产风险与确定性保险 (Broken Deal Risk & Sunk Costs, Busaba, Benveniste, & Guo 2001; Dunbar 2000)**：
  - 美股历史上约 20% 的 IPO 申请最终因市场动荡或定价分歧被迫撤回（Withdrawn IPOs）；
  - 发行失败不仅导致数百万至数千万不可逆沉没中介费（法律、审计、保荐）血本无归，更带来毁灭性的声誉重创、竞品挤压与后续降估值融资（Down-round）；
  - 发行人宁愿主动折价 10%~15% 锁定超额认购，本质上是支付一笔风险对冲的“确定性保险费”。
- **多阶段套现与信号假说 (Staged Divestment & Signaling Theory, Allen & Faulhaber 1989; Grinblatt & Hwang 1989; Welch 1989)**：
  - **发售比例有限**：企业 IPO 通常仅出让 15%~25% 股份，75%~85% 留存原股东手中；
  - **动态市值管理**：若上市定高价导致破发 20%，市场口碑坍塌，半年禁售期后原股东根本无法减持；而首日开门红树立牛股预期，解禁期减持剩余 80% 筹码的收益远超 IPO 当天让利损失（Jegadeesh, Weinstein, & Welch 1993）。
- **投行重复博弈与代理冲突 (Repeated Game & Quid Pro Quo, Loughran & Ritter 2002, 2004; Reuter 2006)**：
  - 发行人是一次性客户，买方大机构是终身佣金客户；
  - 投行利用自由配售权（Discretionary Allocation）把折价新股分给高频交易 VIP 买方，换取买方长期向投行贡献大额经纪佣金（Soft Dollars）。
- **机制设计与激励相容约束 (Mechanism Design & Incentive Compatibility, Benveniste & Spindt 1989; Biais et al. 2002)**：
  - 买方拥有私有需求信号 $\theta_i \in \{\text{Low}, \text{High}\}$；
  - 若投行在收到 High 信号后把价格完全压榨至保留价格（$P = \text{High}$），买方的占优策略就是撒谎或保持沉默；
  - 为了满足激励相容约束 $U(\text{High} | \text{High}) \ge U(\text{Low} | \text{High})$，投行必须在定价向上部分修正（Hanley 1993）时，留存正的信息租金返还买方（$\text{IR} > 0$）。
- **核心理论方程式**：
  $$\text{IPO 抑价成本} = \text{发行成功保险费} + \text{解禁期多阶段套现宣传费} + \text{诱导买方如实申报的信息租金}$$

### 19.3 香港主板制度背景与样本微观现实
- **微观现实 1：原股东存量筹码锁定与绝大部分财富留存**：
  - 港交所《上市规则》第 8.08 条要求公众持股量通常为 25%（大型股豁免至 10%~15%）；
  - 2026 Q1 数据中，38 家样本上市时公众持股比例（`Public shareholding at listing (%)`，Col 118）均值仅为 **21.5%**，原股东留存了 **78.5%** 的绝对控股筹码，且受到 6 个月（第 10.07 条）严格禁售；
  - 主表第 16 列显示老股发售（`Sale Shares`）极少，绝大多数为新股发行（`New shares`，Col 17）。
- **微观现实 2：沉没成本的刚性压迫**：
  - 38 家样本上市显性现金开支（`Listing expenses`，Col 101）均值高达 **1.06 亿港元**，最高突破 2.5 亿港元；
  - 对 18A 生物科技与 18C 特专科技等尚未盈利企业而言，若因咬死高定价导致发行流产，沉没成本足以导致企业资金链断裂。
- **微观现实 3：FINI 阳光化机制下的不可逆流产惩罚**：
  - 数字化 FINI 联网，国际配售与散户认购完全实时透明，承销商无法通过抽屉协议掩盖发行冷场，一旦定价过高遭遇撤单，流产是公开毁灭性事件。

### 19.4 待检验学术假说体系
- **$H_{19a}$（原股东存量筹码留存与跨期套现动机假说）**：控股股东及原股东上市后留存的存量股份比例（$100\% - \text{PublicShareholdingPct}$）及控股股东经济利益持股比例（Col 68）越高的企业，其容忍的首日抑价率（Col 128）和留在桌面上的财富（Col 129）显著更高。原股东主动以初始低溢价发售营造开门红，为解禁期后 80% 存量资产的高流动性、高估值套现铺路。
- **$H_{19b}$（沉没成本、现金流饥渴与发行成功保险费假说）**：显性上市费用占拟募资净额比重（$\text{ListingExpenses} / \text{NetProceeds}$）越高、往绩经营性现金流越紧张（Col 50 为负）的企业，对发行流产风险的厌恶程度越极端，其发售定价越倾向于区间底格（`Pricing position == 'At low'`）或低廉的固定价格发售，反映出通过压低定价支付高额“发行成功保险费”的行为。
- **$H_{19c}$（激励相容信息租金与部分修正假说）**：在机构认购火爆、定价相对中点显著上修（$\Delta P > 0$）的样本中，首日抑价率显著大于 0 且与价格上修幅度正相关，严格验证了投行在机制设计中为了满足买方真实申报私有信息的激励相容约束而主动让渡的信息租金。

### 19.5 规范计量经济学模型
#### 模型 19.1：跨期动态套现与原股东存量筹码检验模型 (OLS)
$$\begin{aligned}
\text{IR}_i = &\ \alpha_0 + \beta_1 (100\% - \text{PublicShareholdingPct}_i) + \beta_2 \text{ControllerEconomicPct}_i \\
&+ \beta_3 \Delta P_i + \beta_4 \frac{\text{ListingExpenses}_i}{\text{NetProceeds}_i} + \beta_5 \text{OperatingCashFlowNegativeDummy}_i \\
&+ \beta_6 \text{TopTierVC}_i + \gamma \mathbf{X}_i + \varepsilon_i
\end{aligned}$$

#### 模型 19.2：发行保险需求对低位定价落点的选择模型 (Ordered Probit / Logistic)
$$\begin{aligned}
\text{Logit}\left(\text{Prob}(\text{PricingPosition}_i = \text{'At low'})\right) = &\ \theta_0 + \theta_1 \frac{\text{ListingExpenses}_i}{\text{NetProceeds}_i} + \theta_2 \text{OperatingCashFlowNegativeDummy}_i \\
&+ \theta_3 \text{DebtRepaymentPct}_i - \theta_4 \ln(\text{FirmAge}_i + 1) + \mathbf{\Gamma} \mathbf{Z}_i
\end{aligned}$$

#### 模型 19.3：信息租金结构方程（Benveniste-Spindt 机制设计检验）
$$\text{MoneyLeft}_i = \lambda_0 + \lambda_1 \max(0, \Delta P_i) \times \text{NetProceeds}_i + \lambda_2 \ln(\text{SubscriptionRatio}_i) + \lambda_3 \text{TopTierSponsor}_i + \mu_i$$

### 19.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 上市首日抑价率 | **Col 128**| `First-day return / Underpricing (%)` | 数值百分比 | 模型 19.1 被解释变量 (Y) |
| 定价落点分类 | **Col 24** | `Pricing position in filing range` | 文本分类 | 模型 19.2 被解释变量 (Y) |
| 留在桌面上的财富 | **Col 129**| `Money left on the table (HK$)` | 货币数值 | 模型 19.3 被解释变量 (Y) |
| 上市时公众持股比例 | **Col 118**| `Public shareholding at listing (%)` | 数值百分比 | 存量留存筹码核心自变量 ($1 - \text{Float}$) |
| 控股股东上市经济利益比| **Col 68** | `Controller economic interest at listing (%)`| 数值百分比 | 跨期套现动机自变量 |
| 显性总上市开支 | **Col 101**| `Listing expenses (HK$)` | 货币数值 | 沉没成本保险核心自变量 |
| 最终发行人净募资额 | **Col 117**| `Net IPO proceeds to issuer (HK$)` | 货币数值 | 保险费相对基准 |
| 往绩经营性现金流 | **Col 50** | `Operating cash flow in year-1 (before annualization)`| 货币数值 | 流产风险压力自变量 |
| 价格修正幅度 | **Col 22** | `Filing price revision (%)` | 数值百分比 | 激励相容信息租金核心自变量 |
| 拟用于偿债募资比 | **Col 72** | `Debt repayment (% of planned net IPO proceeds)`| 数值百分比 | 偿债避险控制变量 |
| 老股发售转让股数 | **Col 16** | `Sale Shares` | 整数数值 | 首发减持控制变量 |
| 新股发行股数 | **Col 17** | `New shares ` | 整数数值 | 规模基础变量 |

### 19.7 经济学直觉与学术贡献
彻底扭转了传统实证研究将首日抑价单纯视为“代理成本”或“承销商剥削发行人”的单维视角，建立了**涵盖“发行流产保险”、“解禁期多阶段套现”、“投行重复博弈”与“信息提取激励相容租金”四位一体的卖方跨期理性博弈模型**。该假说体系为现代企业金融学（Corporate Finance）对 IPO 抑价之谜（Underpricing Puzzle）提供了最具现实说服力的统一解释框架。

---

## Idea 20: 港股 IPO 长期收益之谜：上市后 3 年买入持有回报（BHR）、基准指数加权偏误（EW vs. VW）与同风格匹配检验 (Long-Run Underperformance, Wealth Relatives & Benchmark Contamination)

### 20.1 研究课题与核心科学问题
- **研究课题**：香港主板新股上市后 3 年（36 个月）买入持有回报（Buy-and-Hold Return, BHR）与财富相对比（Wealth Relative, WR）的真实经验分布，以及基准指数构造方式（等权重 EW vs. 市值加权 VW）对“长期跑输之谜”的决定性影响。
- **核心科学问题**：
  1. 港股 IPO 是否真如经典行为金融学文献所述，在上市后 3 年遭受系统性的长期异常低迷（Long-Run Underperformance）？
  2. 这一长期跑输现象究竟是投资者初始非理性亢奋破灭与管理层择机套现（Ritter 1991; Loughran & Ritter 1995），还是由**选错比较基准（Benchmark Contamination）**引发的计量经济学假象（Lowry, Michaely, & Volkova 2017 Ch 3 & Ch 7; Brav & Gompers 1997）？
  3. 当比较基准从全市场等权重指数（EW Index）切换为带 8% 权重上限的市值加权恒生指数（VW Index with 8% Cap），并进一步切换为**同等规模（Size / Market Cap）与账面市值比（Book-to-Market / PB）特征匹配投资组合（Matched Portfolios）**时，港股 3 年财富相对比（WR）是否会系统性向 1.00（无异常表现）靠拢？
  4. 港股特有的制度通道（18A 未盈利生物科技、18C 特专科技、A+H 双重上市价格锚）以及基石投资者的 6 个月限售解禁，如何异质性地塑造新股 3 年后横截面累积收益的分化？

### 20.2 经典文献基准与美股经验事实
- **早期经典：行为过度乐观与择机假说 (Ritter 1991; Loughran & Ritter 1995)**：
  - 传统观点认为，投资者在发行初期存在认知偏差，对成长前景盲目乐观；管理层择机在估值泡沫顶峰窗口期发行；
  - 导致在首日收盘后买入并持有 3 年至 5 年的累计回报严重逊于大盘，形成金融学著名的“IPO 长期弱势之谜（Long-Run Underperformance Puzzle）”。
- **现代实证批判：基准污染与风格聚集效应 (Brav & Gompers 1997; Mitchell & Stafford 2000; Lowry et al. 2017 Ch 3 & Ch 7)**：
  - **规模与价值/成长聚集**：IPO 企业绝大多数属于小型、高成长、低账面市值比（Low B/M）股票。同期美股市场上所有老牌小型成长股表现同样疲软，并非 IPO 企业特有；
  - **Lowry et al. (2017) 40 年全美股大样本（Table 3.10）实证结论**：
    - 样本：1973–2013 年 8,592 家美股 IPO，3 年买入持有平均收益为 **+24.4%**；
    - 对比等权重基准（EW Index，+86.7%）：财富相对比 $WR = 0.67$（表面上严重跑输 33%）；
    - 对比市值加权基准（VW Index，+41.6%）：$WR = 0.88$（跑输幅度明显收窄）；
    - 对比**同规模（Size）与同账面市值比（Book-to-Market）匹配组合**（基准收益 +23.8%）：**$WR = 1.00$（完全打平，跑输现象彻底消失）**！
  - **日历时间组合四因子回归（CTPR，Table 3.11）**：
    - 在控制市场（RMRF）、规模（SMB）、估值（HML）与动量（UMD）四个风险因子后，3 年等权组合超额收益 $\alpha = +0.101\%$ ($t = 0.67$)，市值加权组合 $\alpha = -0.002\%$ ($t = -0.01$)，**在统计上精确等于 0**。所谓的“长期异常跑输”纯属选错尺子的幻觉。

### 20.3 香港主板制度背景与样本微观现实
- **微观现实 1：恒生指数特殊的“8% 权重上限市值加权（VW with 8% Cap）”**：
  - 美股 S&P 500 为纯自由流通市值加权；而港股为防止腾讯、阿里、美团等少数科技巨头垄断指数，设定了**单只成分股 8% 权重天花板**；
  - 这种折中设计使得恒指兼具大盘与中盘特征。若直接使用等权重（EW）基准，会因港股大量缺乏流动性的微盘股产生极高的换手磨损与买卖价差弹跳偏差（Bid-Ask Bounce）；
- **微观现实 2：极端二元分化的市场流动性（Liquidity Polarization）**：
  - 港股缺乏散户普惠资金垫底，大量中小市值新股上市 1~3 年后沦为日均成交额不足百万港元的“流动性孤岛”；
  - 若不控制换手率与流动性因子，长周期持有回报的计算极易受到非同步交易（Nontrading Days）的严重扭曲；
- **微观现实 3：双重限售解禁冲击与基本面实质出清（Lock-up Expiration & Fundamental Shakeout）**：
  - 基石投资者面临 6 个月法定锁定期（Col 104），控股股东面临 6 个月完全锁定期及后续 6 个月控股权锁定；
  - 上市后 6 至 12 个月是抛售套现的流动性挤压期，而**第 3 年（36 个月）**则是 18A 生物科技能否商业化摘 B、18C 特专科技能否兑现营收指标、传统制造业业绩是否变脸的“终极基本面检验窗口”。

### 20.4 待检验学术假说体系
- **$H_{20a}$（基准加权偏误假说，Benchmark Weighting Bias）**：
  在以首日收盘价（Col 127）为起点的 3 年买入持有回报（BHR）检验中，对比全市场等权重基准（EW Index）时，港股 IPO 样本显示出显著的长期负向异常收益（$WR < 1.00$）；而当基准切换为市值加权指数（VW Index，含 8% 封顶修正）时，财富相对比显著提升，表明等权重基准对微盘股的高权重赋予夸大了新股跑输程度。
- **$H_{20b}$（同规模同风格匹配吸收假说，Style-Matching Resolution）**：
  一旦采用同行业、同市值区间（Size）以及同等市净率/账面市值比（PB / Book-to-Market）的非新股港股上市公司作为 1:1 或特征匹配组合基准，港股新股的 3 年财富相对比向 1.00 显著收敛，且在日历时间四因子回归（CTPR）中异常收益 $\alpha$ 统计上不显著异于 0，证实长期表现落后本质上是小型成长股因子的共有风险特征。
- **$H_{20c}$（监管通道与价格锚异质性假说，Regulatory Channel & Price Anchor）**：
  采用 A+H 双重上市通道（Col 75）的企业，由于内地 A 股存量二级市场估值锚的持续约束，其 3 年异常买入持有回报方差显著低于纯红筹企业；而 18A（Col 77）和 18C（Col 78）等未商业化科技企业，3 年期收益分布呈现极度右偏（极少数核心管线爆发企业带来数十倍收益，拉高中位数以下的大面积亏损）。

### 20.5 规范计量经济学模型

#### 1. 3 年买入持有回报（BHR）与财富相对比（Wealth Relative）定义
设股票 $i$ 在上市首日二级市场收盘后（$t = 1$）买入，持有至第 36 个月末（或破产退市日）：
$$R_{i, 36} = \prod_{t=1}^{36} (1 + R_{it}) - 1$$

同期对应基准资产 $B$（EW 指数、VW 指数或风格匹配组合）的买入持有回报为：
$$R_{B, 36} = \prod_{t=1}^{36} (1 + R_{Bt}) - 1$$

样本总体 3 年财富相对比（Wealth Relative, $WR$）定义为：
$$WR_{36} = \frac{1 + \bar{R}_{\text{IPO}, 36}}{1 + \bar{R}_{B, 36}}$$
* 若 $WR_{36} < 1.00$，表明相对于该基准表现落后；
* 若 $WR_{36} = 1.00$，表明表现完全平手，不存在异常跑输；
* 若 $WR_{36} > 1.00$，表明产生正向超额回报。

#### 模型 20.1：个股 3 年异常买入持有回报（BHAR）横截面解释模型 (OLS)
定义个股 3 年异常回报 $\text{BHAR}_{i, 36} = R_{i, 36} - R_{\text{Match}, 36}$，检验影响长期收益分化的核心发行特征：
$$\text{BHAR}_{i, 36} = \beta_0 + \beta_1 \text{IR}_i + \beta_2 \text{CornerstoneRatio}_i + \beta_3 \text{Chapter18C}_i + \beta_4 \text{APlusH}_i + \beta_5 \ln(\text{Proceeds}_i) + \beta_6 \text{ControllerEconomicPct}_i + \beta_7 \text{HighTechDummy}_i + \varepsilon_i$$

#### 模型 20.2：月度日历时间四因子组合回归模型 (Calendar-Time Portfolio Regression, CTPR)
为彻底消除事件研究法中的横截面时间自相关偏差（Cross-sectional Correlation），每月将过去 36 个月内完成 IPO 的所有港股公司构建为一个投资组合（分为等权重 EW 和市值加权 VW 两组），进行 Fama-French 三因子加 Carhart 动量因子的时间序列回归：
$$(R_{pt} - R_{ft}) = \alpha + \beta_1 (R_{mt} - R_{ft}) + \beta_2 \text{SMB}_t + \beta_3 \text{HML}_t + \beta_4 \text{UMD}_t + \varepsilon_t$$
* $R_{pt}$：由过去 36 个月内上市的 IPO 企业构成的月度投资组合收益率；
* $R_{ft}$：香港外汇基金票据或 1 个月 HIBOR 无风险收益率；
* $(R_{mt} - R_{ft})$：恒生指数全市场超额收益；
* $\text{SMB}_t$、$\text{HML}_t$、$\text{UMD}_t$：港股市场的规模因子、估值因子与动量因子；
* **核心检验目标**：截距项 $\alpha$（Alpha）是否显著异于 0。若 $\alpha$ 在统计上不显著，则直接拒绝“IPO 长期异常跑输”假说。

### 20.6 138 列主表变量与字段映射
| 变量名称 | 主表列号 | 表头英文字段名 | 字段类型 | 计量经济学角色 |
|---|:---:|---|:---:|:---:|
| 发行认购价 | **Col 11** | `IPO Subscription Price (HK$)` | 货币数值 | 收益率基准起点参考 |
| 首日收盘价 | **Col 127**| `First trading day closing price (HK$)` | 货币数值 | **3 年 BHR 买入持有起始点 ($P_0$)** |
| 首日抑价率 | **Col 128**| `First-day return / Underpricing (%)` | 数值百分比 | 模型 20.1 核心自变量 ($\text{IR}_i$) |
| 基石配售比例 | **Col 103**| `Final cornerstone allocation (% of base offer)`| 数值百分比 | 初始筹码锁定自变量 |
| 最早基石解禁日 | **Col 104**| `Earliest cornerstone unlock date (dd/mm/yy)`| 日期 | 中期流动性释放节点 |
| 18C 特专科技标识 | **Col 78** | `Chapter 18C flag` | 0/1 虚拟变量 | 科技通道异质性自变量 |
| 18A 生物科技标识 | **Col 77** | `Chapter 18A flag` | 0/1 虚拟变量 | 研发管线不确定性自变量 |
| A+H 双重上市标识 | **Col 75** | `A+H issuer flag` | 0/1 虚拟变量 | 跨境价格锚约束自变量 |
| 控股股东经济利益比 | **Col 68** | `Controller economic interest at listing (%)`| 数值百分比 | 代理成本与掏空风险控制 |
| 最终净募资额 | **Col 117**| `Net IPO proceeds to issuer (HK$)` | 货币数值 | 企业资本规模控制变量 |
| 公司成立年限 | **Col 82** | `Firm age at IPO (years)` | 数值浮点 | 成熟度基础控制变量 |
| 行业分类代码 | **Col 79** | `Industry classification code` | 编码 | 匹配基准与行业固定效应 |

### 20.7 经济学直觉与学术贡献
1. **打破“IPO 长期必输”的学术迷信**：将 Lowry et al. (2017) 针对美股的现代计量经济学基准检验首次完整引入港股新股市场，系统揭示了等权重（EW）与市值加权（VW，带 8% 上限）在衡量港股长线收益时的系统性偏差；
2. **连接一级发行与二级长线资产定价**：建立了一级市场制度特征（基石份额、18A/18C 监管通道、首日抑价让利）对二级市场 3 年期真实累积回报的传导链条；
3. **为港股投资者与监管政策提供理性证据**：为买方机构评估 IPO 长期配置价值、以及港交所评估特专科技（18C）和未盈利生物科技（18A）长周期资本形成质量提供了扎实的量化分析框架。

---

## 附录：全景课题库统一变量定义与 138 列主表映射全景矩阵

下表系统汇编了上述 20 大独立 Research Ideas 涉及的核心学术与微观制度指标，在主数据库 `HKIPO-MB2026Q1.xlsx`（Sheet: `NLR`）及纯净数据文件 `HKIPO-MB2026Q1_clean.csv` 中的法定列号、英文标准表头、中文含义、所属 Idea 索引及计量经济学角色：

| 列号 | 列标 | 规范英文字段名 (Standard Header) | 中文口径释义 | 所属 Idea 索引 | 计量角色 | 格式规范 |
|:---:|:---:|---|---|:---:|:---:|:---:|
| **Col 1** | `A` | `HKEx file# of the year` | 港交所年度申请编号 | 全库通用 | 样本索引 | 整数 |
| **Col 2** | `B` | `Stock Code` | 股份代号（四位港股代码） | 全库通用 | 唯一主键 | `@` |
| **Col 3** | `C` | `Company Name at time of listing` | 公司上市时法定英文名称 | 全库通用 | 样本标识 | `@` |
| **Col 4** | `D` | `Date of Prospectus (dd/mm/yy)` | 招股书法定刊发日期 | Idea 16 | 时间基准 | `YYYY-MM-DD` |
| **Col 6** | `F` | `Sponsor(s)` | 独家/联席保荐人名单 | Idea 05, 10, 17 | 核心解释 | 文本列表 |
| **Col 11**| `K` | `IPO Subscription Price (HK$)` | 最终发售价 (HK$) | Idea 02, 06, 13, 20 | 核心价格 | `0.00` |
| **Col 16**| `P` | `Sale Shares` | 老股发售转让股数 | Idea 14, 19 | 解释变量 | `#,##0` |
| **Col 17**| `Q` | `New shares ` | 新股发售发行股数 | Idea 19 | 规模基准 | `#,##0` |
| **Col 20**| `T` | `Maximum Offer Price` | 最高发售价 (HK$) | Idea 01, 02 | 价格区间 | `0.00` |
| **Col 21**| `U` | `Minimum Offer Price` | 最低发售价 (HK$) | Idea 01, 02 | 价格区间 | `0.00` |
| **Col 22**| `V` | `Filing price revision (%)` | 偏离区间中点修正幅度 ($\Delta P$) | Idea 02, 06, 08, 19 | 核心自变量 | `0.00%` |
| **Col 23**| `W` | `Filing range width (%)` | 询价区间相对宽度 (不确定性) | Idea 01, 05, 12, 15, 16 | 核心被解释/自变量 | `0.00%` |
| **Col 24**| `X` | `Pricing position in filing range` | 定价落点分类 (At high/Fixed等) | Idea 02, 05, 18, 19 | 核心因变量/分组 | `@` |
| **Col 28**| `AB`| `total assets in year-1` | 上市前一年总资产 | Idea 01, 10 | 规模控制 | `#,##0` |
| **Col 37**| `AK`| `Net sales in year-1` | 上市前一年营业收入 | Idea 15 | 经营控制 | `#,##0` |
| **Col 44**| `AR`| `Underwriting Commission (% of fund raised HK (a)`| 香港公开发售法定承销佣金率 | Idea 05, 18 | 核心自变量 | `0.00%` |
| **Col 45**| `AS`| `Underwriting Commission (% of fund raised Int.(b)`| 国际配售法定承销佣金率 | Idea 18 | 核心自变量 | `0.00%` |
| **Col 46**| `AT`| `Over-allotment Option (%)` | 招股书最大超额配售权比例 | Idea 03, 11 | 契约基准 | `0.00%` |
| **Col 47**| `AU`| `Principal business / industry` | 主营业务与细分行业分类 | Idea 16 | 赛道集群 | 文本 |
| **Col 50**| `AX`| `Operating cash flow in year-1 (before annualization)`| 上市前一年经营现金流净额 | Idea 07, 15, 19 | 财务控制 | `#,##0` |
| **Col 52**| `AZ`| `R&D expensed in year-1 (before annualization)`| 上市前一年研发费用开支 | Idea 01, 04, 15, 16 | 科技控制 | `#,##0` |
| **Col 54**| `BB`| `Top 5 customers (% of year-1 revenue)` | 前五大客户销售额合计占比 | Idea 15 | 核心自变量 | `0.00%` |
| **Col 56**| `BD`| `Pre-IPO VC/PE backing (1=yes; 0=no)` | 机构投资人综合背书标识 | Idea 04 | 基础自变量 | `0/1` |
| **Col 57**| `BE`| `Pre-IPO VC backing (1=yes; 0=no)` | 风险投资（VC）入股标识 | Idea 04, 09 | 核心解释 | `0/1` |
| **Col 58**| `BF`| `Pre-IPO PE backing (1=yes; 0=no)` | 私募股权（PE）入股标识 | Idea 04 | 核心解释 | `0/1` |
| **Col 60**| `BH`| `Pre-IPO State/Gov backing (1=yes; 0=no)`| 国资/政府引导基金入股标识 | Idea 04, 09 | 核心解释 | `0/1` |
| **Col 61**| `BI`| `Top-tier VC/PE backing (1=yes; 0=no)` | 顶级机构认证标识 (红杉高瓴等) | Idea 04, 09, 14 | 核心解释 | `0/1` |
| **Col 62**| `BJ`| `Key Pre-IPO investors` | 上市前关键机构投资者名单 | Idea 14 | 身份匹配 | 文本列表 |
| **Col 63**| `BK`| `Pre-IPO institutional shareholding (%)`| 机构投资者上市前合计持股比例 | Idea 04, 09, 17 | 核心自变量 | `0.00%` |
| **Col 64**| `BL`| `Pre-IPO investor board seat (1=yes; 0=no)`| 机构投资者派驻董事会席位 | Idea 04 | 治理介入 | `0/1` |
| **Col 66**| `BN`| `Pre-IPO holding duration (years)` | 机构最早入股至上市持有年限 | Idea 04, 14 | 资本耐心 | `0.00` |
| **Col 67**| `BO`| `Ultimate controller type` | 最终控制人性质分类 | Idea 07 | 治理控制 | `@` |
| **Col 68**| `BP`| `Controller economic interest at listing (%)`| 控股股东上市时经济利益持股比 | Idea 06, 07, 09, 15, 19, 20 | 核心自变量 | `0.00%` |
| **Col 69**| `BQ`| `Controller voting rights at listing (%)` | 控股股东上市时投票权比例 | Idea 07, 15 | 核心自变量 | `0.00%` |
| **Col 70**| `BR`| `Interest-bearing debt at year-1 end` | 上市前一年有息债务总额 | Idea 10 | 债务负荷 | `#,##0` |
| **Col 72**| `BT`| `Debt repayment (% of planned net IPO proceeds)`| 拟用于偿还债务的募资比例 | Idea 10, 19 | 核心自变量 | `0.00%` |
| **Col 75**| `BW`| `A+H issuer flag` | A+H 双重上市发行人标识 | Idea 01, 12, 20 | 核心解释 | `0/1` |
| **Col 76**| `BX`| `WVR flag` | 同股不同权 (Chapter 8A) 标识 | Idea 06, 07, 15 | 核心解释 | `0/1` |
| **Col 77**| `BY`| `Chapter 18A flag` | 第 18A 章未盈利生物科技标识 | Idea 01, 12, 20 | 核心解释 | `0/1` |
| **Col 78**| `BZ`| `Chapter 18C flag` | 第 18C 章特专科技公司标识 | Idea 01, 04, 12, 16, 20 | 核心解释 | `0/1` |
| **Col 79**| `CA`| `Industry classification code` | 行业分类标准代码 | Idea 16, 20 | 行业固定效应 | 编码 |
| **Col 82**| `CD`| `Firm age at IPO (years)` | 公司成立至上市年限 (岁) | 全库通用 | 基础控制 | `0.00` |
| **Col 101**| `CS`| `Listing expenses (HK$)` | 总上市费用 (港元，显性发行成本) | Idea 05, 06, 12, 18, 19 | 核心自变量 | `#,##0` |
| **Col 102**| `CT`| `Cornerstone investor names` | 基石投资者法定披露名单 | Idea 14 | 跨界匹配 | 文本列表 |
| **Col 103**| `CU`| `Final cornerstone allocation (% of base offer)`| 基石投资者最终获配占基础发售比 | Idea 03, 09, 20 | 核心自变量 | `0.00%` |
| **Col 104**| `CV`| `Earliest cornerstone unlock date (dd/mm/yy)`| 最早基石解禁法定日期 | Idea 09, 20 | 事件日期 | `YYYY-MM-DD` |
| **Col 105**| `CW`| `Subscription Ratio (times)` | 公开发售散户认购超购倍数 | Idea 02, 08, 13, 18 | 核心自变量 | `#,##0.00` |
| **Col 106**| `CX`| `Public applicants` | 公开发售有效申请总人数 | Idea 13 | 散户广度 | 整数 |
| **Col 107**| `CY`| `Public valid applied shares` | 公开发售有效申请总股数 | Idea 13 | 散户深度 | 整数 |
| **Col 111**| `DC`| `Final global offering shares (before over-allotment)`| 全球发售基础总发售股数 | Idea 06 | 规模基准 | `#,##0` |
| **Col 114**| `DF`| `Over-allotment shares actually issued` | 实际发行的超额配售股份数量 | Idea 03, 11 | 稳价结果 | `#,##0` |
| **Col 115**| `DG`| `Greenshoe exercise rate (%)` | 绿鞋实际行使比例 (0%~100%) | Idea 03, 11 | 核心因/自变量 | `0.00%` |
| **Col 117**| `DI`| `Net IPO proceeds to issuer (HK$)` | 发行人实际所得净募资金额 | Idea 19, 20, 全库通用 | 规模控制 | `#,##0` |
| **Col 118**| `DJ`| `Public shareholding at listing (%)` | 上市时公开发售股份占总股本比 | Idea 19 | 留存筹码核心自变量 | `0.00%` |
| **Col 120**| `DL`| `Unrestricted public shareholding at listing (%)`| 上市首日不受限自由流通盘比例 | Idea 03, 11, 13 | 核心自变量 | `0.00%` |
| **Col 123**| `DO`| `HSI return over 20 trading days before prospectus (%)`| 招股日前 20 日恒指大盘累计收益率 | Idea 02, 08 | 宏观公开信息 | `0.00%` |
| **Col 124**| `DP`| `HK ordinary IPO count in 90 calendar days` | 招股日前 90 日主板新股数量 | Idea 08 | 市场周期 | 整数 |
| **Col 125**| `DQ`| `1-month HIBOR before prospectus (%)` | 招股前一日 1 个月期 HIBOR 利率 | Idea 08, 13 | 资金成本 | `0.00%` |
| **Col 126**| `DR`| `Banking system aggregate balance before prospectus`| 招股前一日香港银行体系总结余 | Idea 08 | 宏观流动性 | `#,##0` |
| **Col 127**| `DS`| `First trading day closing price (HK$)` | 上市首日二级市场收盘价 (HK$) | Idea 20, 全库通用 | 基础价格 | `0.00` |
| **Col 128**| `DX`| `First-day return / Underpricing (%)` | 上市首日抑价率 / 初始回报率 | Idea 19, 20, 全库核心 | 核心因变量 (Y) | `0.00%` |
| **Col 129**| `DY`| `Money left on the table (HK$)` | 留在桌面上的财富 / 财富流失金额 | Idea 06, 17, 18, 19 | 核心因变量 (Y) | `#,##0.00` |
| **Col 130**| `DZ`| `First trading day opening price (HK$)` | 上市首日二级市场开盘价 (HK$) | 全库通用 | 开盘表现 | `0.00` |
| **Col 131**| `EA`| `First trading day high (HK$)` | 上市首日二级市场最高价 (HK$) | Idea 13 | 盘中振幅 | `0.00` |
| **Col 132**| `EB`| `First trading day low (HK$)` | 上市首日二级市场最低价 (HK$) | Idea 13 | 盘中振幅 | `0.00` |
| **Col 133**| `EC`| `First trading day volume (shares)` | 上市首日二级市场全天成交股数 | Idea 03 | 交易活跃度 | `#,##0` |
| **Col 134**| `ED`| `First-day flipping ratio (%)` | 首日短线翻转抛售率 (换手速率) | Idea 03, 13 | 核心因变量 (Y) | `0.00%` |
| **Col 135**| `EE`| `First trading day turnover (HK$)` | 上市首日二级市场成交金额 (港元) | Idea 17 | 交易体量 | `#,##0` |
| **Col 136**| `EF`| `Offer mechanism` | 发售机制 (Mechanism A vs. B) | Idea 02 | 核心自变量 | `@` |
| **Col 137**| `EG`| `Applicable IPO rules / transition basis` | 适用监管规则与过渡期基准 | 全库通用 | 制度背景 | `@` |
| **Col 138**| `EH`| `Company Chinese Name` | 公司中文法定名称 (末列确证) | 全库通用 | 样本主键 | `@` |
| **Col 139**| `EI`| `Current listing status` | 当前挂牌存续状态 (Active/Suspended/Delisted)| Idea 20, 全库通用 | 存续状态 | `@` |
| **Col 140**| `EJ`| `1-month post-IPO close price (HK$)` | 上市满 1 个月(T+20交易日)收盘价 (HK$) | Idea 20 | 跨期价格 | `0.00` |
| **Col 141**| `EK`| `1-month BHR from Day-1 close (%)` | 1 个月二级买入持有收益率 (%) | Idea 20 | 核心因变量 (Y) | `0.00%` |
| **Col 142**| `EL`| `1-month total return from offer price (%)`| 1 个月一级申购累计回报率 (%) | Idea 20 | 因变量 (Y) | `0.00%` |
| **Col 143**| `EM`| `1-month HSI return (%)` | 同期恒生指数累计收益率 (%) | Idea 20 | 宏观基准 | `0.00%` |
| **Col 144**| `EN`| `1-month HSTECH return (%)` | 同期恒生科技指数累计收益率 (%) | Idea 20 | 风格基准 | `0.00%` |
| **Col 145**| `EO`| `1-month wealth relative vs HSI` | 1 个月对标恒指财富相对比 ($WR_{\text{HSI}}$) | Idea 20 | 相对超额绩效 | `0.000` |
| **Col 146**| `EP`| `1-month wealth relative vs HSTECH` | 1 个月对标恒科财富相对比 ($WR_{\text{HSTECH}}$)| Idea 20 | 风格相对绩效 | `0.000` |
| **Col 147**| `EQ`| `1-month average daily turnover (HK$)` | 首月日均成交金额 (港元) | Idea 20 | 流动性指标 | `#,##0` |
| **Col 148**| `ER`| `6-month post-IPO close price (HK$)` | 上市满 6 个月(基石解禁日)收盘价 (HK$) | Idea 20 | 解禁期价格 | `0.00` |
| **Col 149**| `ES`| `6-month BHR from Day-1 close (%)` | 6 个月二级买入持有收益率 (%) | Idea 20 | 核心因变量 (Y) | `0.00%` |
| **Col 150**| `ET`| `6-month total return from offer price (%)`| 6 个月一级申购累计回报率 (%) | Idea 20 | 因变量 (Y) | `0.00%` |
| **Col 151**| `EU`| `6-month HSI return (%)` | 同期恒生指数累计收益率 (%) | Idea 20 | 宏观基准 | `0.00%` |
| **Col 152**| `EV`| `6-month HSTECH return (%)` | 同期恒生科技指数累计收益率 (%) | Idea 20 | 风格基准 | `0.00%` |
| **Col 153**| `EW`| `6-month wealth relative vs HSI` | 6 个月对标恒指财富相对比 ($WR_{\text{HSI}}$) | Idea 20 | 相对超额绩效 | `0.000` |
| **Col 154**| `EX`| `6-month wealth relative vs HSTECH` | 6 个月对标恒科财富相对比 ($WR_{\text{HSTECH}}$)| Idea 20 | 风格相对绩效 | `0.000` |
| **Col 155**| `EY`| `6-month average daily turnover (HK$)` | 第 6 个月日均成交金额 (港元) | Idea 20 | 流动性指标 | `#,##0` |
| **Col 156**| `EZ`| `Liquidity decay ratio (6M vs Day-1 turnover)`| 6 个月相对首日流动性衰减比率 (%) | Idea 20 | 核心因变量 (Y) | `0.00%` |
| **Col 157**| `FA`| `1-year post-IPO return (%) [Reserved]` | 1 年期持有收益率 [预留待填充] | Idea 20 | 远期因变量 | `0.00%` |
| **Col 158**| `FB`| `1-year wealth relative vs HSI [Reserved]` | 1 年期对标恒指财富相对比 [预留] | Idea 20 | 远期绩效 | `0.000` |
| **Col 159**| `FC`| `3-year post-IPO return (%) [Reserved]` | 3 年期持有收益率 [预留待填充] | Idea 20 | 长期因变量 | `0.00%` |
| **Col 160**| `FD`| `3-year wealth relative vs HSI [Reserved]` | 3 年期对标恒指财富相对比 [预留] | Idea 20 | 长期绩效 | `0.000` |
| **Col 161**| `FE`| `18A/18C regulatory milestone status` | 监管资格演变与商业化里程碑状态 | Idea 20, 全库通用 | 治理与监管分类 | `@` |

---

*本课题库与计量矩阵由 HK IPO Prospectus Pipeline 科研引擎全自动维护与校准。数据源：`Data Collecting Pipeline/HKIPO-MB2026Q1.xlsx`（Sheet: `NLR`）。计量纯净镜像源：`out/HKIPO-MB2026Q1_clean.csv`。*
