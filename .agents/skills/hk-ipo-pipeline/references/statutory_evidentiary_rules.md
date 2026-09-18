# HK IPO Statutory Evidentiary Rules & Chapter Authority Hierarchy
# 招股书法定效力与审计权威层级手册 (Legal Evidentiary Standard)

本项目采集的所有数据用于金融计量经济学实证研究，**必须具备严格的法律约束力（Legal Enforceability）与审计凭据（Auditor Certification）**。

在香港证券与资本市场法（《公司（清盘及杂项条文）条例》、《证券及期货条例》、香港交易所《主板上市规则》）监管体系下，招股书（Prospectus）各章节具有截然不同的法律效力与责任层级。流水线必须严格固定在具有**最高法定效力、法定披露义务与申报会计师审计认证**的正式章节中获取数据，杜绝非正式或辅助章节（如 Definitions、Summary）的起草笔误与口径偏离。

---

## 1. 招股书章节权威层级矩阵 (Chapter Evidentiary Hierarchy)

```
+---------------------------------------------------------------------------------------+
|  Tier 1: 最高法定效力与会计师审计认证章节 (Primary Statutory & Audit Authority)         |
|  - Appendix I: Accountants' Report (附录一：申报会计师报告)                          |
|  - Appendix V: Statutory and General Information (附录五：法定及一般资料)              |
|  - Share Capital (股本章节)                                                           |
|  - Structure of the Global Offering & Underwriting (发售架构与承销合同章节)            |
|  - Expected Timetable (预期时间表)                                                    |
|  - Cornerstone Investors (基石配售协议章节)                                           |
|  - History, Development and Corporate Structure (历史、重组及公司架构)                |
+---------------------------------------------------------------------------------------+
                                           |
                                           v
+---------------------------------------------------------------------------------------+
|  Tier 2: 业务与管理层讨论章节 (Business & MD&A)                                        |
|  - Business (业务章节：主营业务、商业化运营阶段、前五大客户集中度)                    |
|  - Financial Information / MD&A (资本性开支计划、所得款项用途)                        |
+---------------------------------------------------------------------------------------+
                                           |
                                           x [严禁作为法定第一数据源]
                                           v
+---------------------------------------------------------------------------------------+
|  Tier 3: 辅助、术语释义与宣传摘要章节 (Non-Binding / Low Evidentiary Weight)           |
|  - DEFINITIONS (释义)：仅为阅读便利提供的词汇定义，常有笔误或沿用草稿，严禁作为第一数据源 |
|  - SUMMARY (概要)：营销宣传性执行摘要，若与附录审计表/法定表格冲突，一律作废          |
|  - COMPANY-LEVEL STATEMENTS (母公司单体报表)：必须剔除，绝不可用于集团综合财务指标   |
+---------------------------------------------------------------------------------------+
```

---

## 2. 各字段组的法定权威取值来源 (Statutory Sourcing Rules)

### 2.1 法律主体与设立资质 (Legal Entity & Incorporation)
* **包含字段**：`col_BP` (成立日期)、`col_BQ` (注册地)、`col_BR` (主要营业地点)
* **唯一权威取值来源**：
  1. **Appendix V: Statutory and General Information** —— 第 1 节「1. Incorporation of our Company」或「1. Further Information about our Company」（发行人依据公司法正式宣誓注册成立的法定日期与地点）；
  2. **History, Development and Corporate Structure** ——「Early History and Establishment of Our Company」（历史正文详细披露的主体工商设立核准）；
  3. **Appendix I: Accountants' Report Note 1** ——「Corporate Information」（会计师经审计确认的公司成立日与注册地址）。
* **绝对禁区**：**严禁从 DEFINITIONS (释义) 章节取值**（释义常将发起人协议签署日、名称预先核准日或非正式口径混用）。

### 2.2 历史财务、负债与会计准则 (Financial Statements & Indebtedness)
* **包含字段**：
  * 资产负债：`col_W`–`col_Y` (总资产), `col_Z`–`col_AB` (净资产/权益), `col_AC`–`col_AE` (总负债)
  * 利润表：`col_AF`–`col_AH` (营业收入), `col_AI`–`col_AK` (税前利润), `col_AL`–`col_AN` (净利润)
  * 现金流与负债：`col_AU` (经营现金流净额), `col_AV` (现金及等价物), `col_AW`–`col_AX` (研发支出/资本化), `col_BE` (有息负债)
  * 审计与准则：`col_V` (记账币种), `col_BT` (会计准则), `col_CF` (毛利), `col_CG` (资本开支), `col_CH` (审计意见)
* **唯一权威取值来源**：
  1. **Appendix I: Accountants' Report (申报会计师报告)** —— 经国际/香港会计准则独立审计的**综合报表 (Consolidated Statements)** 及附注。
* **绝对禁区**：
  1. **严禁引用母公司单体报表**（`...OF THE COMPANY` / `PARENT STATEMENT OF FINANCIAL POSITION`），必须使用 Group/Consolidated 报表；
  2. 严禁使用 Definitions 或未审计的新闻简报。

### 2.3 股本结构与发行股份类别 (Share Capital Structure)
* **包含字段**：`col_L` (总股本), `col_M` (发售总股数), `col_N`–`col_O` (未上市/非H股), `col_P`–`col_Q` (老股/新股), `col_R` (国际配售), `col_S` (公开发售), `col_BI` (股份类别), `col_CE` (全流通转换股数)
* **唯一权威取值来源**：
  1. **Share Capital (股本章节)** —— 法定股本明细表（Table of Issued and to be Issued Share Capital）；
  2. **Information about this Prospectus and the Global Offering** / **Structure of the Global Offering** 正文发售份额拆解。
* **绝对禁区**：严禁采用 Definitions 中对 Share 单词的笼统定义。

### 2.4 发行定价、承销协议与回拨机制 (Offering, Underwriting & Mechanism)
* **包含字段**：`col_T`–`col_U` (最高/最低发售价), `col_AO`–`col_AP` (承销固定佣金/总佣金率), `col_CI` (总上市费用), `col_AQ` (超额配股权比例上限)
* **唯一权威取值来源**：
  1. **Underwriting (承销章节)** ——「Underwriting Arrangements and Expenses」中具法律约束力的《香港承销协议》与《国际承销协议》佣金约定条款；
  2. **Structure of the Global Offering (全球发售的架构)** —— 超额配股权（Over-allotment Option）法定上限条款（Listing Rules 法定 15% 上限）；
  3. **Expected Timetable (预期时间表)** —— 发行认购起止日与定价日法定日程（`col_CC`, `col_CD`）。

### 2.5 基石投资与法定禁售期 (Cornerstone Placement)
* **包含字段**：`col_CJ` (基石投资者名单), `col_CK` (基石分配比例), `col_CL` (最早解禁日期)
* **唯一权威取值来源**：
  1. **Cornerstone Investors (基石投资者章节)** —— 具法律效力的《基石投资协议》披露表格与法定 6 个月禁售期承诺（Lock-up Undertakings）；
  2. **配发结果公告 (Allotment Announcement)** —— 最终行使及确权获配股份数。

### 2.6 业绩期期间锚定与未年化法定口径 (Track Record Period Binding & Annualization)
* **包含字段**：`col_AT` (Year-1 截止日), `col_CF` (毛利), `col_CG` (资本开支), `col_BE` (有息负债), `col_AH` (销售额), `col_AK` (税前利润), `col_AN` (净利润)
* **唯一权威取值来源**：
  1. **期间强绑定（`col_AT` 锚定）**：
     - 若公司存在最新中期报告期（如 6M/8M/9M/10M 截至 2025 年），则 `col_AT` 为该中期报告期末；
     - `col_CF`（毛利）与 `col_CG`（资本开支）**必须强制提取该中期报告期对应列的披露原值**，绝对严禁跨列错采前一完整财年（FY2024）的数值；
     - `col_BE` 必须提取截至该中期报告期末的**总有息负债**（包含流动与非流动借款、租赁负债等带息债务），取 INDEBTEDNESS 表格的 Total 总计。
  2. **年化与未年化法定边界**：
     - **仅**流速类规模指标 `col_AH`（销售额）、`col_AK`（税前利润）、`col_AN`（净利润）在中期时进行年化计算；
     - 毛利 `col_CF`、资本开支 `col_CG`、现金流 `col_AU`、研发支出 `col_AW`**一律不年化，直接填列当期原始披露值**。
  3. **货币基本单位强制转换**：
     - 必须换算为披露货币（`col_V`）的基本单位（元/RMB/HK$/US$）；若招股书表格表头注明 `(RMB'000)` 或 `(in thousands)`，必须乘以 1,000；若注明 `(in millions)`，必须乘以 1,000,000。严禁直接照抄千元数值。

---

## 3. 流水线自动化硬防线实现 (Pipeline Enforcement)

流水线在代码层级建立以下五重不可绕过的物理闸门：

1. **切片层 (`pdfprep.py`)**：
   - 强制将附录五《法定及一般资料》（`STATUTORY AND GENERAL INFORMATION`）、附录一《会计师报告》（`ACCOUNTANTS' REPORT`）、《股本》（`SHARE CAPITAL`）作为固定最高权重窗口切入抽取包；
   - 标点自动规范化，彻底消除 `HISTORY, DEVELOPMENT` 与 `HISTORY AND DEVELOPMENT` 的识别盲区。

2. **检索候选层 (`search.py`)**：
   - 全字段检索默认剔除 Definitions 释义页面；
   - 正则锚点直接锁定主体法定句式：`The predecessor of our Company was incorporated under the laws of the PRC...`、`Our Company was established as a limited liability company in the PRC on...`。

3. **规则与 Prompt 层 (`fields.json` & `ext_packet.py`)**：
   - 字段提示与代理指令明确写入：「必须优先取自附录五法定资料、会计师报告或历史章节，严禁从 Definitions 取值」；
   - 明文规定：`col_CF` 与 `col_CG` 必须严格与 `col_AT` 期间强绑定，严禁错采 2024 全年列；金额必须乘以单位乘数换算为基本货币单位。

4. **审计与合约核验层 (`contracts.py` & `validate.py`)**：
   - `is_definitions_page(pg_text)` 硬门禁：任何法定字段若引用页码落在 Definitions 章节，校验阶段直接判定为 `ERROR` 阻断写回；
   - `is_company_level_statement(pg_text)` 硬门禁：严禁集团财务指标引用母公司单体资产负债表；
   - **毛利率天花板硬门禁（Gross Margin Ceiling Gate）**：
     $$col\_CF \le col\_AH \times \frac{\text{stub\_months}}{12} \times 1.01$$
     毛利不可超过未年化销售额，错采全年数据即刻被数学拦截；
   - **货币基准单位数量级硬门禁（Monetary Scale Guard）**：
     大中型企业若 `CF`、`BE` 处于 $(0, 500,000)$ 或 `CG` 处于 $(0, 100,000)$，判定为漏乘表格千元乘数，直接判定为 `ERROR`。

5. **宏观与微观跨列全量勾稽层 (`cross_check.py`)**：
   - 成立日期 `col_BP` 必须早于上市日期 `col_E`；
   - 全量 38 家公司毛利率与期间对齐勾稽（Check 8）；
   - 全量货币单位基准数量级一致性校验（Check 9）；
   - 资本开支边界与合理性校验（Check 10）。

