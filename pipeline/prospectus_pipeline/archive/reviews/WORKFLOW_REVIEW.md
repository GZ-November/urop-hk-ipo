# HK IPO 数据采集流水线 — 代码 Review 说明

工作目录：`/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Templates/News`
目标工作簿：`HKIPO-MB2026Q1.xlsx`（sheet `NLR`，120 列 × 38 家公司，2026 Q1 上市）

**请重点 review 第 5、6 节的契约与闸门，以及第 8 节列出的已知薄弱点。**

---

## 1. 目标与交付物

把 38 家港股 IPO 公司的数据从**三个来源**采齐，写进老师给的 Excel 模板：

| 块 | 列 | 列数 | 来源 | 状态 |
|---|---|---|---|---|
| 浅绿 | A:K | 11 | HKEX 新上市报告 | ✅ 38/38 |
| 浅蓝 | L:CI | 76 | **招股书** | ✅ 42 个契约字段 38/38 |
| 深蓝 | CJ:DP | 33 | 配发公告 / 行情 / 规则 / HKMA | ✅ 30/38（缺 CJ/CL/DP 随招股书） |

**颜色 = 数据来源**，这是老师手册的口径。程序的铁律：**只改单元格 value，绝不碰 font / fill / alignment / number_format**（那些是模板格式）。

---

## 2. 端到端数据流

```
                        ┌─ HKEX 新上市报告 Excel ──────────────► 浅绿 A:K
                        │
HKIPO-MB2026Q1.xlsx ────┼─ 招股书（HKEXnews PDF 600+ 页）
                        │     find → download → 抽页级文本 → 切片 → packet
                        │     → LLM 抽取 42 字段 → 证据闸门 → 写回 L:AY/CJ/DP
                        │
                        ├─ 配发结果公告（14–50 页）
                        │     download → 抽文本 → packet → LLM 抽 18 字段
                        │     → + 绿鞋核实 → + 基石核实 → 闸门 → 写回 CK:DC
                        │
                        ├─ 腾讯行情 ────────────────────────► DD, DH–DM
                        ├─ HKMA API ────────────────────────► DF, DG
                        ├─ HKEX 新上市页（25+26 两年表）────► DE
                        └─ 规则表（纯代码判定）─────────────► DN, DO
```

**核心模式**：能确定性算的，一行 LLM 都不用；只有"从非结构化长文本里找数"才交给 LLM，且必须带**页码 + 原文引证**，由闸门复核。

---

## 3. 文件职责

### 3.1 主入口

| 文件 | 行数 | 作用 |
|---|---|---|
| `run.py` | 212 | 招股书/配发主 CLI：`find / download / prepare / allot / greenshoe / cornerstone / validate / write` |
| `auto_fill.py` | 349 | 调度器：`status / prepare / next-batch / write-ready / finish`，给「一键填表」流程用 |
| `config.yaml` | — | 工作簿名、HKEX 接口参数、路径、切片上限、校验容差 |

### 3.2 核心库 `src/`

| 文件 | 行数 | 作用 |
|---|---|---|
| `contracts.py` | 264 | **JSON 契约 + 证据校验**。定义缺失哨兵、entry 键集、引文覆盖率阈值、`evidence_issues()` |
| `validate.py` | 390 | **闸门**：结构契约 + 证据核验 + 勾稽等式 + 绿鞋/基石/DA 交叉校验，输出 `gate_pass` |
| `write_back.py` | 189 | 写回。按**规范化表头**运行时解析列（不硬编码列字母），只赋值，先备份 |
| `hkex.py` | 167 | 两段式定位招股书：`prefix.do` 取内部 stockId → `titleSearchServlet.do` 按 ID 拉文档 |
| `pdfprep.py` | 372 | PDF → 页级文本 jsonl → 按 8 个字段组关键词切片 → 生成 packet |
| `allotprep.py` | 207 | 配发公告：下载 → 抽文本 → **整篇不切片**生成 packet |
| `greenshoe.py` | 261 | **绿鞋核实**：检索行使公告 → 取实际配发股数 → 确定性回填 `col_CV` |
| `cornerstone.py` | 95 | **基石核实**：判「确认无基石」→ 确定性回填 `col_CK = 0` |
| `allot.py` | 74 | 早期版本的配发证据准备（**当前 CLI 未使用**，属技术债） |

### 3.3 工具脚本（按数据源）

| 文件 | 行数 | 数据源 |
|---|---|---|
| `tools_search.py` | 442 | **给 LLM 代理用的检索工具**：`sharecap / periods / bundle / pages / search / outline / info` |
| `tools_market.py` | 260 | 腾讯行情 → DD（恒指 20 日回报）、DH–DM（首日 OHLC/量/额） |
| `tools_fetch_hkma.py` | 143 | HKMA 开放 API → HIBOR + 银行体系总结余 |
| `tools_import_market_csv.py` | 186 | 把 HIBOR/总结余按「严格早于招股书日」join 进 DF/DG |
| `tools_ipo_count.py` | 158 | 近 90 日主板普通 IPO 家数 → DE |
| `tools_rules.py` | 165 | 发售机制/适用规则 → DN/DO |
| `tools_greenshoe.py` | 139 | 绿鞋检索（`greenshoe.py` 的早期版本） |
| `tools_greenshoe_shares.py` | 186 | 行使股数提取（同上，早期版本） |
| `tools_*template*.py` / `tools_group_colors.py` / `tools_reclassify.py` / `tools_final_clean.py` / `tools_place_cornerstone_column.py` | — | **一次性**模板改造脚本，已执行完毕，保留作审计 |

### 3.4 LLM 编排 `workflows/`

| 文件 | 行数 | 作用 |
|---|---|---|
| `prospectus_extract.js` | 230 | 招股书 42 字段：抽取 + 独立复核两阶段 |
| `allot_extract.js` | 182 | 配发公告 18 字段：抽取 + 独立复核 |

### 3.5 schema

| 文件 | 字段数 | 说明 |
|---|---|---|
| `schema/fields.json` | 42 | 浅蓝字段：key / 列 / 表头 / 类型 / 单位 / 缺失约定 / 提示 |
| `schema/allot_fields.json` | 18 | 配发字段（同上） |

### 3.6 产物

```
out/found.json              38/38 招股书定位结果
out/downloaded.json         38 份 PDF 下载结果
out/packets.json            38 个 packet 索引
out/extracted/*.json        38 份招股书抽取结果
out/validation.json         闸门报告（gate_pass）
out/allotment_index.json    38/38 配发公告索引
out/allot/{greenshoe,cornerstone_absence,greenshoe_shares}.json   确定性核实结果
out/allot/extracted/*.json  38 份配发抽取结果
data/pdf|text|packets|sections   中间产物（351MB + 61MB + ...）
```

---

## 4. 设计原则

### 4.1 LLM 只做一件事：在长文本里定位数值

| 交给 LLM | 交给确定性代码 |
|---|---|
| 从 600 页招股书找 42 个数 | 下载、抽文本、切片、打包 |
| 判断"哪一行是 Sale Shares" | 所有勾稽等式 |
| 从配发公告找 18 个数 | 绿鞋是否行使（查港交所公告） |
| 写业务描述、中文名 | 有无基石投资者（全文扫关键词） |
| | 行情、HIBOR、IPO 家数、机制判定 |
| | **引文是否真在所指页**（覆盖率闸门） |

### 4.2 确定性优先：能算的绝不问模型

三个典型例子（都是踩坑后加进来的）：

1. **`col_CV` 绿鞋股数**：配发公告只写"假设未行使"，**不能**据此填 0。必须单独检索上市后 45 天内港交所的《行使超额配售权》公告。实测 38 家里 **18 家实际行使了**——早期靠推断填 0 全错。
2. **`col_CK` 基石占比**：无基石时必须填 **0**（"确定的零"），不能留 NaN。判据 = 招股书全文 0 处「基石投资者」且公告无基石章节。实测 4 家无基石。
3. **`col_DA/DC` 自由流通**：公告常不给，用约定公式 `DA = (CS − CK×CS) / CZ`，`DC = CZ`。

### 4.3 证据必须可核验

LLM 每填一个非缺失字段，必须给 `page` + `quote`（≤200 字符）。闸门验：

- `page` 必须真实存在（packet 或全文页级 jsonl）
- `quote` 与该页原文的**词覆盖率 ≥90%**，且**最长连续片段 ≥75%**

第二条专治"两处真话拼一句"——试点时模型把"超额配售 42,726,800 股"和另一份公告的"其后悉数行使"拼在一起，数值恰好对但证据链不成立。

---

## 5. 契约（`contracts.py`）

```jsonc
{
  "code": "3355.HK",
  "fields": {
    "col_L": {"value": 400000000, "page": 314,
              "quote": "<=200字符连续原文", "confidence": "high"}
  }
}
```

| 规则 | 值 |
|---|---|
| 顶层键 | 只能 `code` + `fields` |
| entry 键 | 必须 `value/page/quote/confidence`；可选 `source/note`（仅确定性回填用） |
| 数值缺失 | 字符串 `"NaN"` |
| 文本/日期缺失 | 字符串 `"NA"` |
| `confidence` | `high/medium/low` |
| 引文覆盖率 | `COVERAGE_MIN = 0.90` |
| 最长连续片段 | `LONGEST_SPAN_MIN = 0.75` |
| 检索型来源 | `SEARCH_SOURCES = {greenshoe_lapse, greenshoe_search, cornerstone_absence, da_formula}` —— 这些证据来自检索结论而非文档片段，由 `check_allot` 拿 JSON 做确定性核对 |

---

## 6. 闸门（`validate.py`）

唯一位于写回之前的关卡。**`gate_pass=True` 才允许写 Excel。**

### 6.1 招股书（42 字段）

- 结构契约（键集、类型、缺失哨兵、引文长度）
- 证据核验（页码真实 + 引文覆盖率 + 最长连续片段）
- 勾稽等式：
  - `M = R + S`（全球发售 = 配售 + 公开发售）
  - `M = Q + P`（全球发售 = 新股 + 老股）
  - `L = N + Q`（总股本 = 资本化旧股 + 新股）
  - `L = O + M`（总股本 = 资本化后旧股 + 全球发售）
  - 三年 `资产 = 权益 + 负债`
  - `U ≤ T`（最低价 ≤ 最高价）
  - `AO/AP/AQ/AZ ∈ [0,1]`

### 6.2 配发（18 字段）

- `CT + CU = CS`（最终公开 + 配售 = 最终全球发售）
- `CS ≥ 初始 M`（规模调整权只能扩大）
- `CV ≤ 25% × CS`
- `DA ≤ CY`（不受限公众持股 ≤ 公众持股）
- `CX ∈ (0, CS × 发售价)`（净募资在 0 和毛募资之间）
- `CR` = 港交所元数据刊发时间
- `DA` 与 `(CS×(1−CK))/CZ` 相差 ≤20%
- **绿鞋**：与 `greenshoe.json` / `greenshoe_shares.json` 严格对齐（行使则股数必须一致；未行使且窗口已过必须为 0）
- **基石**：缺 `CK` 且 `cornerstone_absence.json` 判「无基石」→ 必须填 0
- 核心字段全缺报警

### 6.3 写回（`write_back.py`）

- 列位置**运行时**用规范化表头解析，不硬编码列字母；表头重复/找不到就中止
- 闸门有 ERROR → 拒绝写回
- 写前自动备份带时间戳
- 先写临时文件再原子替换
- `--fill-missing` 按手册把缺失写 `NaN`/`NA`（不留空）

---

## 7. 外部数据源与坑

| 源 | 用途 | 坑 |
|---|---|---|
| HKEXnews `prefix.do` + `titleSearchServlet.do` | 招股书/公告定位 | 必须两段式；直接按代码搜是空 |
| HKMA 开放 API | HIBOR + 总结余 | **忽略 `from`/`to`**，要 `pagesize=1000` + 本地过滤；偶发 502 |
| 腾讯行情 `ifzq.gtimg.cn` | 首日 OHLC/量/额 | 成交额单位是**万元**，要 ×10,000 |
| HKEX 新上市报告 | 浅绿 + DE | 2025 与 2026 是**两张表**，`www2.hkexnews.hk/-/media/...` |
| 港交所公告检索 | 绿鞋是否行使 | 标题形如 `FULL/PARTIAL EXERCISE OF THE OVER-ALLOTMENT OPTION` / `LAPSE OF...` |

---

## 8. 已知薄弱点（请重点看）

### 8.1 架构

1. **没有单元测试**。所有验证靠端到端跑 + 人工抽查。`validate.py` 里那些勾稽等式是最该有测试的。
2. **历史脚本未清理**。`tools_greenshoe.py` / `tools_greenshoe_shares.py` / `src/allot.py` 已被 `src/greenshoe.py` 取代但仍在仓库里，容易误用。
3. **一次性模板脚本**（`tools_*template*.py` 等 8 个）与运行时逻辑混在同一目录。
4. **`validate.py` 已 390 行**，招股书校验和配发校验挤在一个文件，`check_firm` / `check_allot` 职责不同却共用 `num()`/`close()`。

### 8.2 校验逻辑

5. **证据闸门依赖 packet 或全文 jsonl**。`alt_texts["prospectus"]` 每次校验都把 61MB 的 jsonl 拼成字符串读进内存——38 家跑全量时内存/耗时需要评估。
6. **`_page_text()` 用正则从大字符串里抠页**，页多时是线性扫描，可能有性能问题（实测 38 家 1 秒级，但没做规模测试）。
7. **引文覆盖率是词袋 + 最长连续片段**，理论上仍可能被"同一页内两段真话拼接"骗过（阈值 75% 是经验值）。
8. **`COVERAGE_MIN` / `LONGEST_SPAN_MIN` 没有依据**，是试错调出来的。

### 8.3 数据正确性

9. **财务期间口径**靠 `tools_search.py periods` 的确定性判定，但**判定规则是从 38 家样本反推的**：
   - 中期（如 9M2025）优先于整年
   - 只在"报表页"里认中期
   - 多中期并存时按**出现频次**选
   
   这套规则在样本上 3355/6082/0600 正确，但**换一批招股书可能失效**。
   
   **状态更新**：经后续 realign，38 家现已**全部统一为 2025 年中期**
   （32 家 `yy` 格式 + 6 家 `yyyy` 格式，仅写法差异，值一致）。
   但 `col_AT` 的**字符串格式仍不统一**（`30/09/25` 与 `30/06/2025` 混用），
   写回 Excel 时会被 `parse_date` 归一成真日期，所以只在 JSON 层面存在不一致。
10. **`col_AS`（上市途径）**是自由文本，38 家写法不统一（"Main Board (Chapter 19A...)" vs "Main Board (H Shares)"）。
11. **`col_CQ`（定价日）** 38 家全填 `NA`——配发公告确实不给，候选来源是招股书 Expected Timetable，**尚未实现**。
12. **`col_P`（Sale Shares）** 有的填 0、有的填 NaN，不统一。

### 8.4 流程

13. **LLM 抽取非确定性**。同一家公司重跑结果会有措辞差异，数值应稳定但未做重复性测试。
14. **`run_agy_remaining.py` / `run_writeback_watch.py` 是运维脚本**，用了 `agy`（Gemini）——**已被现行 skill 禁止**（成本高且 SSE 会静默挂死），保留仅为记录。
17. **`out/extracted/` 里混着 4 个备份 JSON**（`HKIPO-MB1641.backup-before-realign-*.json` 等）。
    任何按 `HKIPO-MB*.json` 通配的脚本都会把它们当成抽取结果读进来——
    建议把备份移到 `backups/`，或让加载逻辑校验文件名严格等于 `HKIPO-MB<4位数字>.json`。
15. **并发没做**。38 家串行跑。
16. **`auto_fill.py next-batch` 的高峰时段限制**是硬编码的北京时间窗口。

---

## 9. 成本与 token 画像（实测）

| 项 | 数值 |
|---|---|
| 一家公司（抽取 + 复核） | 未命中输入 124,804 ／ 缓存命中 3,519,744 ／ 输出 67,842 |
| 缓存命中率 | **96.5%** |
| 成本（空闲时段） | **¥0.47 / 家** |
| 成本（高峰时段） | **¥0.93 / 家** |
| 38 家 | ¥17.7 ／ ¥35.5 |
| 成本结构 | 输出 58% ／ 未命中输入 27% ／ 缓存命中 15% |

**成本由输出 token（主要是推理）主导**，不是输入。实测：输出最多的版本（96,766）反而错 2 处，输出最少的版本（32,684）全对——**输出量和质量不成正比，返工才是浪费**。

---

## 10. 想请 reviewer 回答的问题

1. `validate.py` 的勾稽等式是否有遗漏或错误？特别是**股份结构的四条恒等式在不同上市架构下（H 股 / W 股 / 18C / 介绍上市）是否都成立**？
2. 证据闸门的 90%/75% 双阈值设计是否合理？有没有更严谨的做法（比如逐字符比对 + 允许 OCR 噪声）？
3. `periods` 的期间判定规则是否可靠？**口径不一致的 3–4 家该怎么处理**？
4. `write_back.py` 只赋值不改样式的做法，在 openpyxl 下是否有边界情况（合并单元格、共享样式、条件格式）？
5. 把 61MB jsonl 拼成字符串做证据核验，有无更省内存的写法？
6. 38 家的**口径一致性**该如何系统性检查（而不是靠抽样）？
7. 历史脚本与运行时脚本混放，建议的重构边界在哪？
