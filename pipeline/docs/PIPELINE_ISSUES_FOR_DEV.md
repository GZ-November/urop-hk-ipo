# HK IPO Pipeline 问题报告

**背景**：我们在用这套 pipeline 采集 **2026 Q2 香港主板 IPO** 全量数据（NLR 筛出 60 家）。
为了跑 Q2，本地 `prospectus_pipeline/config.yaml` 被改指向 `HKIPO-MB2026Q2.xlsx`。
以下问题都是在这个过程中实际撞到并复现的，环境基于 commit `2f0d572`。

按严重程度排序。每条都写了**现象 / 复现 / 根因 / 影响 / 建议**。

---

## P0 · `search periods` 期间判定会给出「不可能的期间」（未修）

这是本次发现的最严重问题，因为它直接决定 19 个财务字段的正确性。

### 现象

样本 `6656.HK`（Sigenergy，思格新能源，2026-04-16 上市）：

```
$ python run.py search periods 6656.HK
# 招股书出现的中期与年度
  中期: ['9M2022@09']
  年度: [2023, 2024, 2025]
  （各中期出现次数：9M2022@09x2）

# 判定：year-1 = 9M2022（期末 09/2022）；year-2 = FY2021；year-3 = FY2020
  col_AT = 30/09/22
  年化：销售/税前/净利 ×1.333（9 个月 -> 12 个月）；AU/AW/AX/AY/AV 一律不年化
```

**这个判定是错的。** 招股书原文（p.20 / p.157）明确写着：

> We were incorporated in **May 2022** and began commercial production and sales in May 2023.

公司 2022 年 5 月才成立，**FY2020 / FY2021 根本不可能存在**。招股书实际的报表期间是
**FY2023 / FY2024 / FY2025**，三个完整年度，不需要年化。

### 复现

```bash
cd "Data Collecting Pipeline"
python prospectus_pipeline/run.py download --only 6656.HK
python prospectus_pipeline/run.py prepare  --only 6656.HK
python prospectus_pipeline/run.py search periods 6656.HK     # 上表输出
```

### 根因

在 `prospectus_pipeline/tools/search.py:187 detect_periods()` → `:246 cmd_periods()`。

`detect_periods()` 返回两组信息：`stubs`（中期）和 `years`（年度）。对企业 6656.HK 实际得到：

- `stubs = {(2022, 9): "9M2022"}`，`freq = {(2022,9): 2}` —— 全文只有 **2 次**提及，属于零星的偶发提法
- `years = [2023, 2024, 2025]` —— 三个真实的年度报表期间，**已正确检出**

问题出在 `cmd_periods()` 的分支逻辑（`tools/search.py:257-280`）：

```python
if stubs:
    sy, sm, label = max(stubs, key=lambda x: (x[0], x[1]))   # 只看 stubs 之间谁最新
    ...
    print(f"# 判定：year-1 = {label}（期末 {sm:02d}/{sy}）；"
          f"year-2 = FY{sy-1}；year-3 = FY{sy-2}")            # 靠减法"造"出前两年
else:
    ly = max(y for y in years ...)                            # years 只在这个分支被用到
    ...
```

三处缺陷叠加：

1. **`years` 在 `if stubs:` 分支里完全没被使用。** 已经正确检出的 `[2023, 2024, 2025]`
   被一个出现 2 次的 `9M2022` 直接覆盖，两者之间没有任何一致性校验。
2. **`year-2 = FY{sy-1}` / `year-3 = FY{sy-2}` 是减法推出来的，不校验是否真实存在。**
   代码没有回头确认 `FY2021`/`FY2020` 是否在招股书里出现过（`years` 里并没有）。
   于是输出了文档中不存在的期间。
3. **`max(stubs, ...)` 只在 stubs 内部比较**，无法识别「这个 stub 比已检出的年度还旧」这种情形。
   代码注释里写了「频次只用于显示诊断，不能让重复出现较多的旧比较期覆盖更新期间」——
   那是防「旧比较期覆盖新期间」，而这里是**反向**的失效：一个更旧的偶发 stub 压过了更新的年度，
   而 `freq`（=2，明显是噪声）恰好没被用作任何门槛。

### 影响（高）

- **单家公司 19 个财务字段全错**：`col_Z`–`col_AN` 三年资产/权益/负债/销售/税前/净利润，
  以及 `col_AT`（期末日）、年化系数。期间取错 → 数值不仅错，还会被乘上一个错误的年化系数 1.333。
- **错误是"貌似合理"的**：输出带着精确的日期和系数，看起来非常可信，不会自曝。
  本次是抽取代理自己发现「公司 2022 年成立却出现 FY2020」这个矛盾才纠正的。
- **被指令放大**：`workflows/prospectus_extract.js` 的抽取提示词明确要求
  > `periods` 给**财务期间判定**……**19 个财务字段一律以它的输出为准，不要自己判断期间。**

  即工具被定义为权威来源、并要求代理不要自行判断。那么工具出错时，听话的代理就会照错填。
  这条设计意图是好的（防止代理乱猜期间），但前提是工具本身必须正确 —— 目前不成立。

### 建议

1. 在 `if stubs:` 分支里**引入 `years` 做交叉校验**。最小改动：若已检出的年度集合非空，
   且 `max(years) > sy`（即存在比该 stub 更新的完整年度），则判定该 stub 已过期，
   走年度分支或至少输出警告。
2. **不要用减法造期间。** `year-2` / `year-3` 应从 `years` 里取真实存在且连续的前两年；
   取不到就明确报错，而不是输出 `FY{sy-1}`。
3. 用 `freq` 作为**噪声门槛**（例如 `freq < 3` 的孤立中期不参与判定），或要求 stub 与
   `years` 的区间能构成连续的 Track Record Period。
4. 建议补一条回归测试：用 6656.HK 的页级文本做 fixture，断言判定结果为
   `year-1 = FY2023 / year-2 = FY2024 / year-3 = FY2025`（或至少断言不含 FY2020/FY2021、
   且 `year-1` 的年 ∈ 已检出年度集合）。
5. 因为该工具被定义为权威，建议再复跑 **全部 60 家 Q2** 的 `search periods`，
   把输出与各招股书的成立/报表年度做一次自动一致性检查（如 `year-1` 年 < 成立年份即报警）。

---

## P1 · 5 个生产测试隐式依赖 `config.yaml`（已修，见 PR #1）

### 现象

把 `config.yaml` 指向 Q2 之后，测试套件从 `74 passed / 11 skipped` 变成
**`69 passed / 5 failed / 11 skipped`**：

```
FAILED tests/test_codebook.py::CodebookTests::test_build_codebook_full_production_coverage
FAILED tests/test_cross_check.py::CrossCheckTests::test_run_cross_check_all_companies
FAILED tests/test_cross_check.py::CrossCheckTests::test_run_cross_check_single_company
FAILED tests/test_report.py::ReportTests::test_generate_report_metrics_production
FAILED tests/test_report.py::ReportTests::test_generate_report_with_mock_fixture
```

典型报错：

```
AssertionError: '香港主板 2026 Q1 IPO 全景学术与市场分析报告'
                not found in '# 香港主板 2026 Q2 IPO 全景学术与市场分析报告\n...'
ZeroDivisionError: division by zero
```

### 根因

这 5 个测试在调用时**没有传 `cfg`**，于是模块内部 `if cfg is None: cfg = load_cfg()`
会去读检出目录的 `config.yaml`：

```python
build_codebook()                 # test_codebook.py
run_cross_check(out_dir=...)     # test_cross_check.py ×2
generate_report(out_path=...)    # test_report.py ×2
```

`config.yaml` 是**工作配置**，采集新 cohort 时必然被改指。于是「采集新季度」这个正常动作，
会静默改变这些测试所度量的数据集 → 测试失败，而被测代码其实没动。

之前之所以没暴露：`HKIPO-MB2026Q1.xlsx` 原先被 gitignore，工作簿缺失时这些测试带
`@unittest.skipUnless(WORKBOOK_PATH.exists())` 会直接 skip。commit `a2ed770` 把 Q1 工作簿
纳入仓库后，它们不再 skip，问题才浮出水面。（这一点不是这次改动的错，只是它揭开了既有隐患。）

### 影响

- **回归门槛失效**：`make test` / CI 在采集新 cohort 期间无法作为通过标准，
  要么误报失败，要么被迫忽略失败。CI 上只跑 Q1 config，所以 CI 一直是绿的 —— 
  这个问题只在「本地正在采集新 cohort」时出现，正好是最需要跑测试的时候。

### 已修（PR #1）

让这些断言 Q1 生产数据的测试**显式钉住自己要测的数据集**，通过已有的
`cfg["workbook_path"]` 覆盖机制，不再继承本地 config 的指向；报告测试同时钉住驱动标题的
`dataset.cohort`。仅改测试文件，不动生产代码。

PR：https://github.com/GZ-November/urop-hk-ipo/pull/1 （CI 已通过）

验证矩阵：

| 运行器 | Q1 config | Q2 config |
|---|---|---|
| `pytest` | 74 passed / 11 skipped | 74 passed / 11 skipped |
| `python -m unittest discover` | Ran 78, **OK** (skipped=5) | Ran 78, **OK** (skipped=5) |

### 建议（后续）

如果希望更进一步，可以考虑让 `load_cfg()` 支持环境变量指定配置文件（如
`PIPELINE_CONFIG=...`），这样 CI / 测试 / 多 cohort 并行开发都能各自隔离配置，
不必在每个测试里手动 pin。这属于设计层面的改进，PR #1 是最小修复。

---

## P2 · 抽取提示词与工作流里的路径硬编码，换机器即失效

### 现象

`prompts/agy_extract.md` 第 4 行写死了原作者的绝对路径，且引用了**不存在的脚本**：

```
工作目录：
`/Users/georgezhu/Desktop/UROP HK IPO/Data Collecting Pipeline`
...
   python3 prospectus_pipeline/tools_search.py outline {{CODE}}
   python3 prospectus_pipeline/tools_search.py search {{CODE}} "<正则>" --context 3 --max 8
   python3 prospectus_pipeline/tools_search.py pages {{CODE}} 413-415
```

- `tools_search.py` **不存在**（实际是 `tools/search.py`，且入口是 `run.py search ...`）
- `/Users/georgezhu/...` 是原作者机器上的路径，其他协作者/CI 上必然不存在

`workflows/prospectus_extract.js` 同样硬编码 `python3 prospectus_pipeline/run.py`（18 处）。

### 影响

- **换机器/换协作者直接跑不通**：按提示词照抄命令会 `No such file`。
- **venv 场景下会 ImportError**：若依赖装在 `.venv`（`CONTRIBUTING.md` 就是这么要求的），
  系统 `python3` 通常没有 `pymupdf`。我们本次就踩到：
  `ModuleNotFoundError: No module named 'fitz'`。
  提示词必须用解释器的绝对路径或 `<venv>/bin/python`，不能裸写 `python3`。
- 本次我们在调用工作流时是**临时改写提示词**（替换成 venv 绝对路径 + 绝对 `run.py`）
  才跑通的，属于绕过而非修复。

### 建议

1. 把 `tools_search.py` 的引用统一改成 `run.py search {outline,search,pages}`（与 workflow 注释一致）。
2. 提示词里的工作目录改为**相对/占位**表述，或由调用方注入（workflow 已经有模板变量
   `{{CODE}}`/`{{PACKET}}` 的机制，可以再加一个 `{{RUN}}` / `{{PY}}`）。
3. 在 workflow 里统一用可配置的解释器，例如 `${PY} ${RUN} search ...`，
   而不是写死 `python3 prospectus_pipeline/run.py`。
4. `prompts/agy_extract.md` 看起来已不是活跃路径（workflow 内联了自己的提示词），
   若确已弃用建议删除或在文件头标注，避免误导。

---

## P2 · 6656.HK 抽取质量：复核闸门拦下 3 处（属预期行为，但值得看代理错误率）

fail-closed 的复核闸门**正常工作**并拦下了错误（写回被正确拒绝，Excel 未被修改）。
但拦下的内容反映了代理的失误模式：

| 字段 | 抽取值 | 正确值 | 依据 | 性质 |
|---|---|---|---|---|
| `col_BE`（year-1 期末总有息负债） | 1,720,433,000 | **1,744,898,000** | `fields.json` 的 `hint` 明示「取 INDEBTEDNESS 表格的 Total 余额」，含租赁负债 | 代理取了合并资产负债表的银行借款，**漏计租赁负债** |
| `col_N` | 缺失 | **233,223,030** | p.213 | 缺失导致恒等式 `L=N+Q` 无法核验 |
| `col_O` | 缺失 | **233,223,030** | p.213 | 缺失导致恒等式 `L=O+M` 无法核验 |

其中 `col_BE` 值得注意：**手册并不含糊**，`hint` 已明确要求「取 INDEBTEDNESS 表格的 Total，
包含短期借款、长期借款、**租赁负债**及带息应付票据债券」，代理仍按资产负债表口径取了
`Interest-bearing bank borrowings`。这说明该字段的歧义对代理而言是真实存在的，
建议在提示词里把这条硬规则再强化（或直接给出正/反例：合并资产负债表 vs INDEBTEDNESS 表）。

另外 `col_N`/`col_O` 的缺失会**静默通过**确定性校验（只报 `WARNING_MISSING`，
`errors=0`，写回闸门 = PASS），但恒等式 `L=N+Q`、`L=O+M` 因此不可核验。
建议：当某字段是已实现恒等式的必要组成项时，缺失应升级为 ERROR 而非 WARNING。

复核**独立确认正确**的部分（说明整体质量尚可）：合并报表唯一性（无字段引用母公司单体报表）、
三年会计恒等式、股份结构恒等式、价格区间、期间口径、基石名单 21 家、承销佣金口径、
中文名简体。

---

## P3 · 仓库卫生

### 1. 16.7 MB 二进制入库

commit `a2ed770` 把 `templates/HKIPO-GEM-template-students.xlsx`（**16,667,417 字节**）
纳入 git。git 对二进制不做增量存储，每次改动都会在历史里新增一份完整副本，仓库会持续膨胀。
建议改用 **git-lfs**，或该文件确实需要版本管理时再评估。

### 2. `.gitignore` 例外只覆盖 Q1

`a2ed770` 新增的例外是：

```gitignore
!Data Collecting Pipeline/HKIPO-MB2026Q1.xlsx
!Data Collecting Pipeline/templates/*.xlsx
```

我们采集 Q2 得到的 `HKIPO-MB2026Q2.xlsx` **仍被 `*.xlsx` 忽略**，不会进版本控制。
如果团队打算按 Q1 的方式归档每个季度的成品工作簿，需要为每个新 cohort 补一条例外
（或者改成约定的命名模式，如 `!Data Collecting Pipeline/HKIPO-MB20*.xlsx`）。

---

## P3 · 模板血统需要明确哪份是权威

仓库里 `templates/HKIPO-MB-template-final.xlsx` 与外部流传的
「Copy of HKIPO-MB-template-final.xlsx」**不是同一个文件**，内部结构不同：

| 文件 | 大小 | theme1.xml | styles.xml | sheet1.xml |
|---|---|---|---|---|
| 仓库模板 | 484,507 B | 7705 | 43031 | 5,240,948 |
| 团队 Q1 成品 | 535,497 B | 7705 | 42692 | 5,435,355 |
| 外部流传的 copy | 687,140 B | 7623 | 47627 | 3,624,285 |

从 theme/styles 看，**仓库模板与团队 Q1 成品同源**，外部那份是另一条血统
（典型是 Excel「另存为 Copy of…」整包重写导致）。

**功能上三者完全等价**（我们验证过）：表头 220 列名称 **0 差异**、202/202 表头单元格都有
实心填充色、数据验证均为 12 条，`resolve_columns()` 对 `fields.json` 与
`allot_fields.json` 都是 **70/70 + 18/18 唯一命中**。

所以这不是 bug，但存在**可复现性风险**：协作者手上可能拿着外观同名、内部不同的模板，
产出的工作簿在样式层与团队成品不一致。建议在 README 或 `templates/README` 里明确
「此处为唯一权威模板，请勿使用 Excel 另存副本」。

---

## 附：本次已验证正常的方面（供参考）

- 202 列模板与 pipeline schema **完全兼容**：`fields.json` 70/70、
  `allot_fields.json` 18/18 唯一命中；202/202 表头通过 `resolve_columns` 的
  `fill_type == "solid"` 门禁。
- 注意 `schema/*.json` 里记录的 `col` 字母是**旧版布局、系统性偏移**的，
  但 `resolve_columns()` 按规范化**表头**匹配，不依赖列字母，故实际无碍。
  （若不熟悉这一点，容易误判为严重错位 —— 建议在 schema 里注明 `col` 仅为历史 key 命名。）
- `report.py` 新增的 HSICS 前缀回退（`2f0d572`）只影响 markdown 报告；
  `cross_check.py` 不读 `hsic_codes.json`，`schema/hsic_codes.json` 目前只有 6082.HK 一条，
  属 CI 兜底 stub，不影响采集链路。
- `find` 对 2026 Q2 的 60 家主板 IPO **全部命中**招股书（60/60）。
- 哈希状态机（extracted → validated → reviewed）工作正常，
  复核 `fail` 时写回被正确拒绝，未污染工作簿。


---

# 追加发现（2026Q2 全量采集过程中）

以下两条是在用 commit `1ed49a9` 跑 2026Q2 全量流程时新发现的，都会**直接阻断开箱即用**。

## P1 · `workflows/prospectus_extract.js` 依赖 DSH 沙箱不提供的 Node API

`workflows/prospectus_extract.js:262` 是**无条件执行**的：

```js
// 若为主题模式，自动运行确定性合并
const { execFileSync } = require("child_process");   // ← 无条件执行
const mergedSuccessCodes = new Set();
if (isTopicMode) { ... }
```

`require` 只在 `isTopicMode` 分支内才被*使用*，但这一行本身在**任何模式**下都会先执行。而 DSH workflow 沙箱明确不提供 Node API（无 filesystem / child_process）。后果：

- 脚本会在**抽取阶段全部跑完之后**（第 262 行位于 extract 与 verify 之间）崩溃；
- 独立复核阶段**不会执行**，`return` 值也拿不到；
- 表现上像是"抽取卡住了"，实际是抽取成功但脚本在衔接处挂掉 —— 非常难排查。

**建议**：把 `require` 移进 `if (isTopicMode) { ... }` 内部，或改成惰性获取：

```js
let execFileSync = null;
if (isTopicMode) { ({ execFileSync } = require("child_process")); }
```

## P1 · `run.py allot` 的输入索引没有任何生产者

`run.py:135` 与 `allotprep.download_all` 都要求读取 `out/allotment_index.json`：

```python
index = json.loads((cfg["paths"]["out"] / "allotment_index.json").read_text())
```

但**全仓库检索 `allotment_index` 只有读取方、没有写入方**：

```
./run.py:135          读
./src/validate.py:330 读
./src/allot.py:26     读
./src/allotprep.py:115 文档里提到「来源索引」
```

即：从干净检出开始，`python run.py allot` 必然抛 `FileNotFoundError`，`allot` 这条链路**开箱即用是断的**。`found.json` 由 `run.py find` 生成，但配发公告索引没有对应的 `find` 阶段。

**已补齐**：我们新增了 `prospectus_pipeline/tools/build_allotment_index.py`，逐家检索 HKEXnews 的
「ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS」（窗口取上市日前后数日），
输出 `allotprep` 需要的 `[{code, file, datetime, title, url}]`。60 家实测可解析，例如：

```
6656.HK  15/04/2026 22:32  ANNOUNCEMENT OF ALLOTMENT RESULTS
0068.HK  16/04/2026 20:59  ANNOUNCEMENT OF FINAL OFFER PRICE AND ALLOTMENT RESULTS
```

该工具是独立新增文件，不影响既有行为；建议正式纳入 `run.py`（例如加 `allot_find` 子命令或在
`cmd_allot` 前置自动构建）。

## 已修正的口径缺口（供团队参考，建议并入仓库）

跑 2026Q2 时发现 5 处口径/证据规则缺失，导致 3 家试点**全部**复核失败。逐条实测后已补入
`schema/fields.json` 与 `workflows/prospectus_extract.js` 硬规则 11–15：

| 规则 | 内容 | 实测依据 |
|---|---|---|
| 11 | `col_N`=`col_O`=`L − M`（发行前已发行股数）；`col_P`=0（全部为新股时） | **2026Q1 成品工作簿 38/38 行**全部如此 |
| 12 | 引文必须直接支撑数值；派生合计须含被加项；零值须有正面依据；缺失字段 `quote` 必须为空串 | 试点 3 家共 13 处引文类失败 |
| 13 | `col_BE` 取 INDEBTEDNESS 表 **Total（含租赁负债）**，不得只取资产负债表的银行借款 | 2476.HK **连续两轮**因漏计租赁负债失败 |
| 14 | `col_AO`/`col_AP` 用招股书**披露费率**，禁止用「上市费用 ÷ 募资额」倒推 | 3296.HK 倒推 0.007，实际披露 0.3% |
| 15 | 派生值（自行相加）的引文必须包含被加的原始数字 | 3296.HK 负债合计引文只含流动负债合计 |

补入后回归验证：`6656.HK` 第 2 轮 pass、`2476.HK` 第 3 轮 pass（0 discrepancies）。

> 其中 `fields.json` 的 `col_N`/`col_O`/`col_P` 原先**完全没有 `hint`**（`hint: null`），
> 是代理各行其是的直接原因；建议所有股本结构字段都补上口径说明。


## P1 · `cmd_external` 缺少在线抓取器，只跑离线入表器（导致两条链路必挂）

`run.py:cmd_external` 的工具清单是：

```python
external_scripts = [market, hkma_import, ipo_count, flags, rules, hsic_codes, aftermarket]
```

但其中两个是**离线入表器**，需要先由**在线抓取器**产出原始数据；而那两个抓取器
（`tools/external/hkma.py`、`tools/external/hsic.py`）**不在清单里**：

| 消费者（在清单里） | 需要的前置文件 | 生产者（不在清单里） |
|---|---|---|
| `hkma_import.py` | `data/manual/hibor_balance.csv` | `hkma.py` |
| `hsic_codes.py` | `out/hsic.json` | `hsic.py` |

`cmd_external` 是 fail-closed 的（任一工具非 0 退出即终止），所以从干净检出跑
`run.py external` 必然在 `hkma_import` 处中断，**后面 5 个工具（含 aftermarket）全都不执行**。
我们实测就是这个结果。

**建议**：把 `hkma.py`、`hsic.py` 作为「fetch」步骤加入 `cmd_external` 清单（或在各自
consumer 前自动调用），README 里也说明需要先联网抓取。

## P1 · `hkma.py` 的 ROOT 解析错误 + 日期范围写死

1. **路径不一致（明确 bug）**：

   ```python
   # tools/external/hkma.py:30
   ROOT = Path(__file__).resolve().parent          # -> tools/external
   DEFAULT_OUT = ROOT / "data" / "manual" / "hibor_balance.csv"

   # tools/external/hkma_import.py:25
   ROOT = Path(__file__).resolve().parents[2]      # -> prospectus_pipeline  ✅
   ```

   抓取器把 CSV 写到 `tools/external/data/manual/`，而导入器从
   `prospectus_pipeline/data/manual/` 读 —— **两者永远对不上**，必须先手工搬文件。
   修复：`hkma.py` 改用 `parents[2]`，与 `hkma_import.py` 一致。

2. **默认日期范围写死为 `2025-11-01 ~ 2026-04-30`**：

   ```python
   ap.add_argument("--from", dest="frm", default="2025-11-01")
   ap.add_argument("--to",   dest="to",  default="2026-04-30")
   ```

   采集新 cohort 时（Q2 招股书日期跨 4–6 月）会**取不到 5/6 月的数据**，且不会报错，
   只会静默缺失。建议默认改为「今天回溯 N 天」或由 cohort 的 `period_start/period_end` 推导。

## P1 · `hsic_codes.py` 依赖不存在的 `data/manual/hsics.json`，且 `HSIC_EN2CODE` 不完整

1. **手工分类表缺失**：`hsic_codes.py:85` 读取
   `prospectus_pipeline/data/manual/hsics.json`（HSICS 6 位码 → 门类/业务类别/子类别），
   但 `data/manual/` 目录在仓库中**不存在**（连它引用的 `data/manual/README.md` 也没有）。
   实测直接 `FileNotFoundError`。

2. **`HSIC_EN2CODE` 覆盖不足**：该字典只有 21 个子类别，而 2026Q2 实际出现 31 个。
   以下 10 个不在表内，工具 fail-closed 直接拒绝写回（影响 **14 家公司**、`BN`/`BO` 两列）：

   | 缺失子类别 | 涉及家数 |
   |---|---|
   | Pharmaceuticals | 3 |
   | Computers & Peripherals | 2 |
   | Energy Storage Units | 2 |
   | Consumer Electronics / Environmental Engineering / Other Retailers / Insurance / Advertising & Marketing / Pharma & Biotech Contract Services / Gold & Precious Metals | 各 1 |

   另外 `hkex` 抓回的 `out/hsic.json` **只有英文名称、没有 6 位码**，所以无法绕过映射表。

   **建议**：把权威 HSICS 码表（`data/manual/hsics.json`）纳入仓库（xlsx/csv 即可，
   注意 `.gitignore` 里 `**/prospectus_pipeline/data/` 被整体忽略），或补全 `HSIC_EN2CODE`。
   我们**没有猜测这 10 个码**——写错码比暂时缺失更糟。

## 提示 · `external` 的 `flags` 依赖招股书抽取结果（不是 bug，但要注意顺序）

`tools/external/flags.py:151` 需要读取
`out/extracted/HKIPO-MB<code>.json` 的 `col_AS` 来判断上市章节，缺 JSON 就跳过该家：

```python
if not jf.exists():
    print(f"{code:9s} 缺抽取 JSON，跳过")
    continue
```

因此 `flags` 必须在招股书抽取**之后**再跑一次，否则只有已抽取的公司会被填上
`Listing board / A+H / WVR / 18A / 18C / Place of incorporation / 基石解禁日`。
建议在 README 的 stage 顺序里注明，或让 `cmd_external` 对 flags 做前置检查与提示。


## P2 · `cmd_external` 给所有工具统一传 `--book`，在线抓取器会 argparse 崩掉

即使把 `hkma` / `hsic` 加进清单，还会再撞一次：

```python
for name, script in external_scripts:
    cmd = [sys.executable, str(script)]
    ...
    cmd.extend(["--book", book_target])     # 无条件传
```

但这两个抓取器**没有 `--book`**：

| 工具 | 实际支持的参数 |
|---|---|
| `hkma.py` | `--from --to --out --pagesize --retries --base` |
| `hsic.py` | `--out` |
| 其余 7 个 | 均含 `--book`（多数含 `--only` / `--dry-run`） |

结果：argparse 报错退出码 **2**，fail-closed 再次中断整条链。我们已改为按工具声明
`(name, script, 接受 --book, 接受 --only)` 三元组，只给支持的传参。

## P2 · `HSIC_EN2CODE` 缺 10 个子类别（已补，附权威码）

2026Q2 实际出现 31 个子类别，`hsic_codes.py` 的 `HSIC_EN2CODE` 只有 21 个，
缺失的 10 个会让工具 fail-closed 拒绝写回（影响 14 家公司、`BN`/`BO` 两列）：

| 子类别 | HSICS 码 | 依据 |
|---|---|---|
| Advertising & Marketing | `235010` | |
| Computers & Peripherals | `701020` | |
| Consumer Electronics | `232020` | |
| Energy Storage Units | `101070` | |
| Environmental Engineering | `101030` | |
| Gold & Precious Metals | `051010` | |
| Insurance | `502010` | |
| Other Retailers | `237050` | |
| Pharma & Biotech Contract Services | `281050` | |
| Pharmaceuticals | `281010` | |

码值取自恒生指数公司公开文件 `B_HSICSe.pdf` 与分类变更公告，**两处交叉验证**；
未从编号规律猜测。已补入 `HSIC_EN2CODE`，`BN`/`BO` 随即写满 60 家。

## P2 · `report.py` 的 `HSICS_PREFIX_MAP` 门类映射有误且不全

该映射用于报告里的行业分布，但与前缀实际含义不符：

| 前缀 | `report.py` 现值 | 实测应为 | 证据 |
|---|---|---|---|
| `05` | 能源業 | **原材料業** | Copper `052020`、Specialty Chemicals `053040`、Gold `051010` |
| `10` | 原材料業 | **工業** | Industrial Components `101020`、Environmental Eng. `101030` |
| `50` | 電訊業 | **金融業** | Insurance `502010` |
| `60` | （缺失） | **地產建築業** | Property Investment `601030` |
| `23` | 非必需性消費 | ✅ 正确 | Consumer Electronics `232020`、Other Retailers `237050` |

由于 `hkex` 返回的 `hsic_ind`（如 `"Materials - ..."`）本身带门类名，我们的做法是
**从公司级 `hsic_ind` 反推前缀→门类**，据此生成 `data/manual/hsics.json`，
没有直接改 `report.py`。建议按上表校正该映射，并补齐 `60`。

## 备注 · `write` 拒绝部分写回（设计如此，但影响分批交付）

`write_back.write_all` 会检查**目标集合内每家都必须有抽取 JSON**：

```python
wanted = [normalize_code(x) for x in only] if only else sorted(row_of)
missing_records = [c for c in wanted if c not in files]
if missing_records or unmatched:
    raise SystemExit("拒绝部分写回；...")
```

不带 `--only` 时 `wanted` 是全部 60 家，因此**只要有一家没抽完就整体拒写**。
fail-closed 本身合理（避免半个数据集被写进"单一真相"工作簿），但意味着无法按波次交付。
需要分批写回时必须显式给 `--only <code...>`。我们实测：`--only` 6 家 → 写入 70 列，
`audit` 回读 **420/420 格匹配、0 差异**。

## 备注 · 数据目录下的手工输入文件清单（建议纳入版本控制或文档化）

跑通全流程实际需要以下**手工/外部输入**，仓库里都没有（且 `prospectus_pipeline/data/`
被 `.gitignore` 整体忽略）：

| 文件 | 用途 | 生产者 |
|---|---|---|
| `data/manual/hibor_balance.csv` | 1M HIBOR + 银行体系总结余 | `hkma.py` 可生成（但路径 bug 见上） |
| `data/manual/hsics.json` | HSICS 6 位码 → 门类/类别/子类别 | **无**（需课题组提供或按上表重建） |
| `out/allotment_index.json` | 配发结果公告索引 | **无**（我们补了 `tools/build_allotment_index.py`） |
| `sources/NLR2026_Eng.xlsx` | Q2 公司清单 + A:K | HKEX 官方 |


## P1 · 配发链路缺 `greenshoe` 前置阶段：`col_CV` 无法从公告推断

跑配发抽取时，`validate --target allot` 稳定报错：

```
ERROR: 绿鞋未核实: 缺 greenshoe.json 记录：不能从配发公告推断 CV，须先跑 greenshoe 阶段
```

`col_CV`（绿鞋**实际**行使股数）必须由独立的 `run.py greenshoe` 阶段检索港交所行使公告得出
（写入 `out/allot/greenshoe.json` / `greenshoe_shares.json`），然后由
`derive_allot` → `apply_cv` 回填。但：

- `workflows/allot_extract.js` 的提示词只让代理跑 `derive_allot` + `validate`，
  **没有提到 `greenshoe`**，代理会撞上一个「改 JSON 也修不了」的 ERROR；
- README / 命令参考里的 allot 流程也没把这个阶段串进去。

实测：先跑 `run.py greenshoe`（60 家 → **27 家行使 / 33 家未行使**，行使股数取到 26/27），
再 `validate --target allot` 即 `errors=0 / 闸门=PASS`，`col_CV` 正确回填为 `2,036,000`。

**建议**：把 `greenshoe` 写进 allot 流程的文档与提示词（我们已在 `allot_extract.js` 的步骤 3
补了一条自愈指令：若 validate 报缺 `greenshoe.json`，则先跑
`run.py greenshoe --only <code>` 再重试），或让 `cmd_allot` 前置自动调用。

> 顺带称赞一下：这条错误信息写得很好 —— 直接告知缺哪个文件、以及「不能从公告推断」的原因，
> 排查成本几乎为零。仓库里其它失败路径（如 `hsic_codes` 只报 FileNotFoundError）可以借鉴这种写法。


## P1 · 41 个「学术扩展列」（Col 162–202）的四个脚本全部未接入 CLI

差距分析显示 **Col 162–202 共 41 列一个都没填**。排查后确认这条链的四个脚本
**都自带 `__main__` 入口，但 `run.py` 没有任何子命令调用它们**：

| 脚本 | 作用 | 产出 |
|---|---|---|
| `src/market_panel.py` | 逐日行情与微观结构面板 | `out/master/daily_market_panel.csv`（4498 日线）、`horizon_summary.csv` |
| `src/stabilization_panel.py` | 稳价事件 | `stabilization_events.csv`（60 家） |
| `src/lockup_panel.py` | 法定解禁事件 | `lockup_events.csv`（180 条） |
| `src/write_back_expansion.py` | 写回 41 列 | 工作簿 Col 162–202 |

`write_back_expansion.py` 消费 `daily_market_panel.csv`，而后者只有 `market_panel.py`
会生产 —— 所以即使单独跑写回工具，也只会写入 2460 个**空**格子（我们第一次跑就是这样）。
按正确顺序跑完四个脚本后，扩展区从 **20/41 → 34/41 列满 60 行**。

**已修复**：新增 `run.py expansion` 子命令，按
`market_panel → stabilization_panel → lockup_panel → write_back_expansion` 顺序执行，
fail-closed。同时新增 `run.py allot_index` 子命令（见上），并让 `cmd_allot` 在索引缺失时自动构建。

> 这是第 **3** 类「模块/命令存在但未接线」的问题（前两类：`hkma`/`hsic` 抓取器、
> `allotment_index`）。建议对 `src/`、`tools/` 下所有带 `__main__` 的脚本做一次
> 「是否有 CLI 入口」审计，避免继续漏掉。

## 备注 · `write` 是「全或无」：任一目标未过哈希门即整体拒写

```python
for code in targets:
    try:
        authorized(cfg, code, target, by_code.get(code, {}))
    except ValueError as exc:
        blocked_targets.append(str(exc))
if blocked_targets:
    raise SystemExit("写回授权失败：" + " | ".join(blocked_targets))
```

因此不带 `--only` 时，**必须 60 家全部通过复核**才能写回任何一家。结合实测约 43% 的复核通过率，
这意味着要先完成数十家公司的返工，才能执行一次「全量写回」。
分批交付必须显式使用 `--only <code...>`（我们已用此法写入 9 家，`audit` 630/630 匹配、0 差异）。

fail-closed 的初衷是对的（避免半成品进入"单一真相"工作簿），但建议在文档里明确写清
「全量写回需先满足全部哈希门」以及「分批需 `--only`」，否则使用者会以为可以逐波推进。


## 使用提示 · workflow 文件必须**内联执行**，不能让代理「先读 JS 再执行」

`workflows/*.js` 的设计是**整体作为 DSH workflow 的 script 体内联提交**（脚本里 `extractPrompt()` 返回的模板字符串就是代理的 prompt）。
我们曾为省 token 尝试另一种做法：内联一个**短脚本**，让每个代理先读取
`workflows/prospectus_extract.js`，再照其中的 `extractPrompt()` 执行。实测结果：

| 交付方式 | 批次 | 抽取成功率 |
|---|---|---|
| 完整内联 | 批次 1–4 | **10/10**（4 批一致） |
| 让代理读 JS | 试跑批次 5 | **1/10** |
| 让代理读 JS | 返工批次 R1 | **0/10**（JSON 完全未被改写） |

**结论**：不要让代理「读工作流源码再执行」——即使模板可读，失败率也会从 0% 跳到 90–100%。
如果将来要把提示词外置，应改为「生成时把模板**展开**进 prompt」，而不是让代理运行时去读文件。
建议在 workflow 文件头注明这一点，避免他人重蹈。


## P0 · 抽取指令与复核判据冲突：packet 是「种子切片」，复核却按「全文边界」判 fail

这是实测中**单点影响最大**的问题，同时打中 0901 / 1392 / 2290 / 2493 等多家公司。

**现象**：抽取代理引用某个页码作为字段依据，复核以
「Cited page 384 is outside the packet's covered page range」判 fail —— 但同时又在同一条里写明
「value verified correct on full prospectus p.384」。即**数值对、引文真实、只是该页不在 packet 里**。

**根因**：`data/packets/HKIPO-MB*.md` 只含**部分页**（种子切片）。以 0901.HK 为例：

```
packet 页标记数: 138
覆盖页码: 1-26, 65-74, 123-124, 149-159, 235-251, 261-267, 274-277, 302-307, 325-33x, ...
grep '<<<PAGE 384>>>' packet -> 0 命中
```

但 `run.py search pages 0901.HK 384` **能返回 p.384 的完整原文**。

而抽取工作流的指令明确写着：

> packet 里的切片只是种子，**很多披露并不模板化**。凡是在 packet 里找不到、或你不确定的地方，
> **必须用检索工具在全文里自己找**。

**冲突**：抽取代理照指令用 `search` 取证并引用该页；复核却要求 quote 必须落在 packet 切片内。
两边对「证据边界」的理解不一致，导致**正确的工作被判 fail**。

**建议**：统一为「**以招股书全文为证据边界**」——

- 复核应接受「能通过 `search pages <code> <p>` 取到的页」作为有效证据，不应仅因该页不在 packet 内就判 fail；
  只有当引文**在全文里也找不到**时才判「引文不实」。
- 或反之：若确实要求「只能引 packet 内页」，就必须在抽取指令里写明，并让 `search` 只返回 packet 内的页。
  （我们倾向第一种，因为 `search` 的存在意义正是查非模板化披露。）

我们已按第一种在 `workflows/prospectus_extract.js` 的复核清单顶部加了「页码有效性判定」段落。


### P0 证据补录 · 误杀已用具体案例坐实（1191.HK）

为确认这不是个别现象，我们对 1191.HK 做了一个可复现的三步验证：

```bash
# 1) packet 是否包含该页
grep -c '<<<PAGE 23>>>' data/packets/HKIPO-MB1191.md      # -> 0
# 2) 该页能否通过 search 取到
python run.py search pages 1191.HK 23                     # -> 返回 p.23 全文
# 3) 该页内容是否正是代理引用的句子
#    p.23 原文: "…they will be collectively interested in 17.95% … and will
#                remain the single largest group of Shareholders"
```

抽取结果对 `col_BC` / `col_BD` / `col_BB` 填的正是 **17.95% / single largest group**，页码 **23**。
复核判 fail 的理由是：

> "page 23 is not in the packet" / "'21.11%' and 'single largest group' appear nowhere in the packet
> and page 23 is not in the packet"

而复核自己在同一条 `should_be` 里给出的正确答案是 **17.95%**、来源为「substantial-shareholder table,
extracted page 208」—— **与代理的取值完全一致**。

**结论**：这是「值正确、引文真实、页码可检索」，仅因不在 packet 切片内而被判失败。
`search pages` 与 packet 的页标记使用**同一套编号**（我们用 `<<<PAGE 218>>>` 双端核对过），
所以问题不是编号体系不一致，而是**复核把「packet 切片」当成了证据边界**。

同一模式在 1191 / 2667 / 1770 / 9971 / 0901 / 1392 / 2290 / 2493 等公司中反复出现，
是本项目**通过率的最大单一损耗源**。


## P0（第二处）· 字段键契约冲突：`contracts.py` 允许 `source`/`note`，工作流提示词却禁止

与「页码边界」同类：**管线自身写入的数据，被它自己的复核判为违规**。

**权威定义**（`src/contracts.py:13, 109-112`）：

```python
FIELD_ENTRY_KEYS = {"value", "page", "quote", "confidence"}

# source/note 为流水线确定性回填（目前只有 col_CV 的绿鞋核实）留的可选元数据，
# 必填仍是 value/page/quote/confidence。
extra = set(entry) - FIELD_ENTRY_KEYS - {"source", "note"}
if not FIELD_ENTRY_KEYS <= set(entry) or extra:
    issues.append(...)
```

并且 `SEARCH_SOURCES = {"greenshoe_lapse", "greenshoe_search", "cornerstone_absence", "da_formula"}`。

**谁在写这些键**（都是管线自己）：

| 位置 | 写入 |
|---|---|
| `src/greenshoe.py:235` | `"source": "greenshoe"`（col_CV 绿鞋回填） |
| `src/cornerstone.py:109` | `"source": "cornerstone_absence"` |
| `derive_allot`（da_formula） | `source` / `note` |

实测 **44 家配发 JSON** 的字段条目含 `source`/`note`。

**冲突**：`workflows/allot_extract.js` 与 `workflows/prospectus_extract.js` 的输出契约原本写的是
「每个 entry **只能有** value/page/quote/confidence 四个键」，复核据此判 fail：

> "The packet's output contract allows exactly value/page/quote/confidence;
> these five entries add a 'source' key and col_CV also adds 'note', violating ..."

即**管线回填的字段反而成了失败原因**。

**已修复**：两个工作流的契约描述改为「**必须**含四个键，另**可**含可选的 `source`/`note`」，
并在复核清单顶部加入「字段键判定」：含 `source`/`note` **不得**判 fail。

> 建议：`contracts.py` 的注释已经写得很清楚，但工作流提示词是独立维护的文本，容易漂移。
> 更稳妥的做法是**由 `contracts.py` 生成提示词里的契约段落**，避免两处各写一遍。


## P0（第三处，且是硬性不可能）· 200 字符引文上限 vs「合计须含全部组成项」

这是三处契约冲突里**最严重**的一处，因为它**不是措辞不一致，而是逻辑上不可能同时满足**。

**两侧的要求**：

| 来源 | 要求 |
|---|---|
| `src/contracts.py:124` | `if not isinstance(quote, str) or len(quote) > 200: issues.append("quote must be string <=200 chars")` |
| 复核（以及我们按手册写的提示词） | `col_CO`（公开有效申请股数）是**合计类**字段，quote 必须能支撑全表合计，即覆盖 Pool A 全 28 档 + Pool B 全 12 档，或至少 Pool A/Pool B 的汇总 |

**实测**：`out/allot/extracted/HKIPO-MB6067.json` 的 `col_CO.quote` 长度为 **3115 字符**
（代理按复核要求贴了整张 `BASIS OF ALLOCATION` 表），`validate` 立刻报
`quote must be string <=200 chars`，整份被 BLOCK。

于是出现死循环：

- 贴全表 → **校验失败**（>200 字符）
- 贴 ≤200 字符 → **复核失败**（「不能支撑合计」）

这也直接解释了我们在定向修复批次里观察到的 **`repair_failed`**：修复代理照复核意见改，改完
`validate` 不过，于是整个条目标记为修复失败。

**建议（任选其一，我们倾向前两者）**：

1. **给合计类字段放宽引文上限**，或在 `contracts.py` 增加一个可选的 `components` 数组
   （只对 `col_CO`、`col_CJ`、`col_pre_ipo_investors` 等合计/名单类字段），让「组成项」有处可放；
2. **明确接受 200 字符内的「交叉验证式」引文**，例如
   `初始香港公开发售 1,283,900 股 × 认购 1,007.22 倍 = 1,293,166,900 股`
   ——复核在 §9630 的意见里其实已经认可这种写法（"or an explicit cross-check such as ..."），
   但工作流提示词没有写清楚，代理只能猜；
3. 放宽到按「字段类别」设上限（名单类可长、数值类 200）。

**我们已做的缓解**：把 `workflows/allot_extract.js` 的规则 13 改写为
「引文必须在 200 字符内，任选 Total 行 / 交叉验证等式 / 两池合计行之一」，
并明确写「不要把整张分配表贴进 quote」。

> 三处契约冲突的共同根因：**权威定义分散在 `contracts.py`、`search` 的实现与工作流提示词三处**。
> 提示词是手写文本，最容易漂移。建议把契约段落改为**从 `contracts.py` 生成**。


### P0 第三处 · 影响面补充：**名单类字段同样被 200 字符上限卡死**

初判时以为该冲突只影响「数值合计类」（如 `col_CO`）。诊断复核（3 家公司、逐条分类）显示它同时卡死**名单类**：

| 字段 | 值的内容 | 长度 |
|---|---|---|
| `col_CJ`（基石投资者名单） | 14–21 家投资者全称 | 远超 200 |
| `col_pre_ipo_investors`（上市前投资者名单） | 21 家全称 | 远超 200 |

复核意见里反复出现「名单不完整 / quote 只含某几家 / 引文不含组成项」——但**把 14–21 个公司全称写进引文必然超过 200 字符**，
于是又是同一个死循环。

诊断分类统计（3 家）：

```
证据不支撑数值              12
合计/名单类引文不含组成项      6
字段口径错误                 5
零值缺正面依据                4
其它（全部为 quote 超 200 字符） 3
引文在全文找不到              1
```

**我们已在两个工作流加入「引文长度判定」**，明确：

- quote **≤200 字符是硬上限**；
- 因此**不得**要求合计/名单类字段的引文含全部组成项；
- 只要引文给出 **Total 行 / 算术恒等式 / 表头+家数**之一，即视为已支撑数值；
- 组成明细由 `value` 与可选 `note` 承载；
- 反之，**引文超过 200 字符本身就是 fail**。

**根治建议**：在 `contracts.py` 的字段条目里增加可选的 `components` 数组（合计类放组成项、名单类放全名单），
使「证据完整性」与「引文长度上限」不再互相排斥。


## P1 · `validate.is_company_level_statement()` 误报：把 Accountants' Report 页判为母公司单体报表

`src/contracts.py:199` 的 `COMPANY_LEVEL_TITLE_PATTERN` + `is_company_level_statement()` 会取**页面前 15 行**
判断是否为单体报表。但会计师报告（Accountants' Report）首页通常是：

```
ACCOUNTANTS' REPORT ON HISTORICAL FINANCIAL INFORMATION TO THE DIRECTORS OF ...
Introduction ... Opinion ...
```

而**同一页**往往还包含母公司单体报表标题 `STATEMENTS OF FINANCIAL POSITION OF THE COMPANY`（位于前 15 行内），
于是整页被判为 company-level。

**后果**：`col_CH`（审计意见）在 1511.HK 上被彻底锁死 —— 全文只有 p.326 一处载有
`In our opinion, the Historical Financial Information gives ... a true and fair view ... of the Group and the Company`，
而该页必被拒绝。我们实测确认：

```
is_company_level_statement(p326) -> True
正则命中: STATEMENTS OF FINANCIAL POSITION OF THE COMPANY
p326 是否含 'OF THE COMPANY': False   # 误报来自标题行拼接
```

**建议**：把判据从「页面前 15 行含标题」改为「**引文所在段落**含标题」，或对
`col_CH`（审计意见）这类“报告正文”字段豁免该检查。当前实现会把「审计意见页」与「单体报表页」
一起误杀——而这两者在同一页上是常见排版。
