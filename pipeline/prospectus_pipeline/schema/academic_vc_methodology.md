# 香港 IPO 数据库：学术衍生变量与 Pre-IPO VC/PE 抽取方法论及工程契约规范

本文档为香港主板 IPO 科研级数据库中 **10 个 Pre-IPO VC/PE 细分变量** 与 **8 个第一阶段学术衍生变量** 的法定抽取规范、方法论契约与工程固化标准。规则适用于所有 cohort；每个季度的样本、输出路径和状态凭证由所选 `PIPELINE_CONFIG` 决定。

---

## 一、 方法论文献基石

本套指标体系全面对齐公司金融与实证资产定价顶级文献：
- **Lowry, Michaely, and Volkova (2017)**, *"Initial Public Offerings: A Synthesis of the Literature and Directions for Future Research"*, **Foundations and Trends® in Finance**.
- **Rock (1986)** / **Ritter (1984)**: 胜者诅咒与首日抑价 (Underpricing)
- **Benveniste & Spindt (1989)** / **Hanley (1993)**: 簿记建档动态信息提取与部分修正假说 (Partial Adjustment)
- **Beatty & Ritter (1986)**: 事前估值不确定性 (Ex-Ante Valuation Uncertainty)
- **Aggarwal (2003)**: 机构短线获利翻转抛售机制 (Day-1 Flipping)
- **Loughran & Ritter (2002)**: 行为金融学与留在桌面上的财富 (Money Left on the Table)
- **Ellis, Michaely, & O'Hara (2000)**: 绿鞋价格支持与超额配售执行机制 (Greenshoe Mechanics)
- **Gompers (1996)** / **Brav & Gompers (1997)**: 风险投资认证效应 (Certification) 与名誉造势假说 (Grandstanding)
- **Field, Lowry, & Mkrtchyan (2013)**: IPO 企业治理与董事会顾问价值

---

## 二、 10 个 Pre-IPO VC/PE 细分维度抽取与分类规范

### 1. 招股书法定锚定章节与搜索关键词
- **法定第一源**：`HISTORY AND DEVELOPMENT — Pre-IPO Investments`（历史、重组及公司架构 — 上市前投资）。
- **法定第二源**：`SUBSTANTIAL SHAREHOLDERS`（主要股东）/ `SHARE CAPITAL`。
- **法定第三源**：`DIRECTORS AND SENIOR MANAGEMENT`（董事及高级管理层），核实非执行董事与投资人背景。

### 2. 字段详细分类契约

| 字段名称 | 英文表头 | 数据类型 | 提取与判定规则 |
|---|---|:---:|---|
| **VC 机构入股** | `Pre-IPO VC backing (1=yes; 0=no)` | 0/1 | 识别早期、成长期专业风险投资基金（如红杉、启明、五源、源码、经纬、高榕、纪源等）；设立初期的领投机构。 |
| **PE 机构入股** | `Pre-IPO PE backing (1=yes; 0=no)` | 0/1 | 识别中晚期私募股权基金、大型并购基金或主权/养老金私募平台（如高瓴、中信资本、弘毅、CPE 源峰、华平、黑石等）。 |
| **CVC 产业资本** | `Pre-IPO CVC backing (1=yes; 0=no)` | 0/1 | 实体产业龙头企业或其战略投资/CVC 平台（如美团、阿里巴巴、腾讯、小米、比亚迪、宁德时代等）。 |
| **国资/政府引导基金** | `Pre-IPO State/Gov backing (1=yes; 0=no)` | 0/1 | 地方国资委、财政局产业引导基金、央企母基金或高新区创投平台（如上海国资母基金、北京 AI 产业基金、招商局创投等）。 |
| **顶级机构认证** | `Top-tier VC/PE backing (1=yes; 0=no)` | 0/1 | 清科/投中前 20 强或国际一线顶级机构（红杉、高瓴、启明、经纬、IDG、淡马锡、君联等）持有重要股权或担任领投方。 |
| **主要机构名单** | `Key Pre-IPO investors` | 文本 | 招股书披露的主要专业投资机构规范化标准英文或拼音名单，分号（`; `）隔开。 |
| **机构合计持股比例** | `Pre-IPO institutional shareholding (%)` | 百分比 | 上市前所有专业机构投资者（VC/PE/CVC/国资）合计持股比例（取上市前即完成重组后的股份比例，小数或百分比）。 |
| **董事会席位** | `Pre-IPO investor board seat (1=yes; 0=no)` | 0/1 | 机构投资者是否在发行人董事会派驻非执行董事（NED）或拥有正式董事会观察员（Observer）席位。 |
| **最早入股轮次** | `Earliest Pre-IPO investment round` | 文本 | 公司历史上最早引入外部投资的轮次规范名（如 `Series Angel`, `Series Pre-A`, `Series A`, `Series B`, `Pre-IPO`, `None`）。 |
| **投资持有年限** | `Pre-IPO holding duration (years)` | 浮点数 | 从最早一轮 Pre-IPO 投资协议签订日期至招股书刊发日期的持有跨度年限（保留 2 位小数）。 |

---

## 三、 8 个第一阶段学术衍生变量数学公式与边界规则

### 1. 公司成立至上市年限 (Firm Age at IPO)
- **英文表头**：`Firm age at IPO (years)`
- **数据层级**：浅蓝 (Theme 4 Tint 0.8)
- **公式**：
  $$\text{Firm Age} = \frac{\text{Listing Date} - \text{Incorporation Date}}{365.25}$$
- **边界规则**：严格排除 Definitions 段笔误，以 Appendix 法定注册日为准；保留 2 位小数。

### 2. 询价偏离区间中点幅度 (Filing Price Revision / Partial Adjustment)
- **英文表头**：`Filing price revision (%)`
- **数据层级**：浅蓝 (Theme 4 Tint 0.8)
- **公式**：
  $$\Delta P = \frac{P_{\text{offer}} - \bar{P}_{\text{file}}}{\bar{P}_{\text{file}}}, \quad \text{其中 } \bar{P}_{\text{file}} = \frac{P_{\text{low}} + P_{\text{high}}}{2}$$
- **边界规则**：固定价格发售（无最低价或 $P_{\text{low}} == P_{\text{max}}$）时，$\Delta P = 0.00\%$。

### 3. 询价区间相对宽度 (Filing Range Width)
- **英文表头**：`Filing range width (%)`
- **数据层级**：浅蓝 (Theme 4 Tint 0.8)
- **公式**：
  $$\text{Range Width} = \frac{P_{\text{high}} - P_{\text{low}}}{\bar{P}_{\text{file}}}$$
- **边界规则**：固定价格发售时，$\text{Range Width} = 0.00\%$。

### 4. 定价落点分类 (Pricing Position in Filing Range)
- **英文表头**：`Pricing position in filing range`
- **数据层级**：浅蓝 (Theme 4 Tint 0.8)
- **分类逻辑**：
  - 若为固定价格发售：`Fixed price`
  - 若 $P_{\text{offer}} > P_{\text{high}}$：`Above range`
  - 若 $P_{\text{offer}} = P_{\text{high}}$：`At high`
  - 若 $P_{\text{offer}} = \bar{P}_{\text{file}}$：`Midpoint`
  - 若 $P_{\text{offer}} = P_{\text{low}}$：`At low`
  - 若 $P_{\text{offer}} < P_{\text{low}}$：`Below range`
  - 其他区间内取值：`Within range`

### 5. 首日抑价率 (First-day return / Underpricing)
- **英文表头**：`First-day return / Underpricing (%)`
- **数据层级**：深蓝 (RGB FF00B0F0)
- **公式**：
  $$\text{IR} = \frac{P_{\text{day1\_close}} - P_{\text{offer}}}{P_{\text{offer}}}$$
- **格式**：`0.00%`

### 6. 留在桌面上的财富 (Money Left on the Table)
- **英文表头**：`Money left on the table (HK$)`
- **数据层级**：深蓝 (RGB FF00B0F0)
- **公式**：
  $$\text{Money Left} = (P_{\text{day1\_close}} - P_{\text{offer}}) \times \text{Base Global Offering Shares}$$
- **格式**：`#,##0.00`

### 7. 首日翻转/换手率 (First-day flipping ratio)
- **英文表头**：`First-day flipping ratio (%)`
- **数据层级**：深蓝 (RGB FF00B0F0)
- **公式**：
  $$\text{Flipping Ratio} = \frac{\text{First trading day volume (shares)}}{\text{Base Global Offering Shares}}$$
- **格式**：`0.00%`

### 8. 绿鞋实际行使比例 (Greenshoe exercise rate)
- **英文表头**：`Greenshoe exercise rate (%)`
- **数据层级**：深蓝 (RGB FF00B0F0)
- **公式**：
  $$\text{Greenshoe Rate} = \frac{\text{Over-allotment shares actually issued}}{\text{Base Global Offering Shares} \times \text{Over-allotment Option \%}}$$
- **边界规则**：无超额配售选择权（0%）或实际未发行超额股份（0 股）时，归为 0.00%；浮点容差 $\le 10^{-4}$ 自动归一化为 100.00%。

---

## 四、 自动化维护与运行规范

1. **衍生推导纯函数**：位于 `src/academic_derivations.py`，必须无副作用、支持单步单元测试；
2. **主表同步与注入器**：位于 `tools/enrich_master_dataset.py`，强制执行写前时间戳备份；
3. **代码本与 CSV 自动联动**：任何列的变动必须同步触发 `src/codebook.py`；输出文件名应从当前配置的 `dataset.id` 生成，不得固定为某个季度。
4. **跨季度执行**：10 个字段定义维护在 `schema/fields.json`，抽取由通用 `prepare` 工作流生成的 ownership packet 驱动。为新季度复制配置、指向该 cohort 工作簿，并设置独立的输出/状态目录；随后按 `prepare → 抽取 → validate → write` 执行。写回继续使用规范化表头解析及 hash-bound extracted/validated/reviewed 闸门。
5. **VC/PE 覆盖审计**：可运行 `python prospectus_pipeline/tools/vc_pe_enricher.py status --config <cohort-config>` 检查当前 cohort 十个字段的覆盖率和引文证据。该审计器不携带发行人答案，也不直接写工作簿；缺失值保持缺失，不自动推断为无 VC/PE。
6. **历史 Q1 值**：`schema/archive/HKIPO-MB2026Q1_vc_pe_legacy.json` 仅用于追溯旧手工数据，不参与任何季度的抽取、验证或写回。
