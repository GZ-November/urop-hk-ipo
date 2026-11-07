# Hong Kong IPO Research

[![CI](https://github.com/GZ-November/urop-hk-ipo/actions/workflows/ci.yml/badge.svg)](https://github.com/GZ-November/urop-hk-ipo/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Language / 语言**: [English](#hong-kong-ipo-research) | [简体中文 (Bilingual Workflow & 2000–2026 Guide)](#港股-ipo-数据采集与实证研究流水线20002026-全周期中英双语指南) · [End-to-End Workflow & 2000–2026 Architecture (EN / 中文)](docs/WORKFLOW_2000_2026.md)

**Tell an AI agent a listing period; get evidence-backed Hong Kong IPO data and reproducible analysis.**

This project turns HKEX disclosures into evidence-linked datasets for ordinary Hong Kong Main Board and GEM IPOs. Every value carries its source page, and an independent reviewer checks it before it enters the workbook. The research studies first-day returns, retail allocation, cornerstone investors, A+H pricing, margin financing, and returns after listing.

**Current study: 113 Main Board IPOs listed in 2026 Q1-Q3 | 202-variable workbook schema | Observation cutoff: 30 September 2026.**

## Give this repository to an agent

New teammates: start with the **[one-page team instructions (PDF)](docs/TEAM_INSTRUCTIONS.pdf)**
([LaTeX source](docs/TEAM_INSTRUCTIONS.tex)) or the **[quickstart (中文 / English)](docs/QUICKSTART.md)**.

```bash
git clone https://github.com/GZ-November/urop-hk-ipo.git
cd urop-hk-ipo
python3 tools/bootstrap.py   # locked dependencies + the hk-ipo-collect agent skill
claude                       # or codex; then type the request below
```

> Collect Hong Kong IPOs listed in 2025 Q4. &nbsp;/&nbsp; 收集 2025 年第四季度的港股 IPO

Use an agent that runs shell commands, reaches the Internet and launches subagents
(Claude Code recommended; Codex CLI works). It plans board × quarter jobs, collects,
extracts, has each payload independently reviewed, and delivers a ZIP in `deliverables/`.
Optional details go in the [request template](docs/COLLECTION_REQUEST_TEMPLATE.md);
`python3 run.py plan 2025Q4` previews the jobs without collecting.

For every detail and the manual commands, read the **[complete English user and agent
instructions](docs/AGENT_INSTRUCTIONS.md)**. **[GEM has its own template, schema,
source parser and review target](docs/GEM_PIPELINE.md)**; Main Board-only fields
are removed rather than filled with artificial zeros.

Bootstrap installs locked collection, analysis and test dependencies, including
managed project Python when needed. Generic agents use portable work orders;
the legacy JavaScript extraction adapters require DSH. The ZIP contains Excel,
CSV, dictionaries and evidence/quality reports. A normal ZIP can contain explicitly
reported legacy or pending-review gaps; it does not certify the data.

## Understand the project in one diagram

```text
  OFFICIAL DISCLOSURES          MARKET DATA          DATED SURVEYS
  Prospectus + allotment       Prices + indices      Margin financing
           |                         |                      |
           v                         |                      |
  +---------------------+            |                      |
  | Extract + validate  |            |                      |
  | Independent review  |            |                      |
  | Version-bound gates |            |                      |
  +----------+----------+            |                      |
             |                       |                      |
             v                       v                      v
  +---------------------------------------------------------------+
  | DATA LAYER                                                    |
  | Quarterly Excel -> clean CSV -> all-years master + references  |
  | Sources, units, dates, missing values, and audit records        |
  +------------------------------+--------------------------------+
                                 |
                    Select actual 2026 listings
                                 |
                                 v
  +---------------------------------------------------------------+
  | RESEARCH LAYER                                                |
  | Study specifications + shared estimation and inference        |
  | Underpricing | retail returns | A+H | margin | supply events   |
  +------------------------------+--------------------------------+
                                 |
                                 v
                 Tables + figures + research reports
                                 |
                                 v
           research_workspace/ : one English file index
```

The workspace links to canonical files; it does not create another dataset. Each study reports its actual sample size. Missing evidence and incomplete return windows remain missing.

## Open the data or read the results

| I want to... | Open this |
|---|---|
| Browse all research files locally | [Research Workspace](research_workspace/README.md) |
| Open the latest Q3 workbook | [2026 Q3 Excel](pipeline/cohorts/HKIPO-MB2026Q3.xlsx) |
| Open Q1 or Q2 workbooks | [2026 Q1](pipeline/cohorts/HKIPO-MB2026Q1.xlsx) / [2026 Q2](pipeline/cohorts/HKIPO-MB2026Q2.xlsx) |
| Use the combined data | [All-years master CSV](pipeline/exports/HKIPO-MB-MASTER_clean.csv) |
| Understand fields and units | [Variable registry](pipeline/registry/HKIPO_Variable_Registry.yaml) / [Q3 codebook](pipeline/codebooks/HKIPO_2026Q3_Codebook.md) |
| Read the English progress report | [PDF snapshot](docs/reports/HK_IPO_RESEARCH_PROGRESS_STE_2026.pdf) / [LaTeX source](docs/reports/HK_IPO_RESEARCH_PROGRESS_STE_2026.tex) |
| Start with coverage and basic statistics | [Basic report](analysis/out/basic_statistics/basic_statistics.md) / [Data gaps](docs/DATA_GAPS_2026.md) |
| Read first-day return results | [Descriptive tables](analysis/out/module_a/table1_stylized_facts.md) / [Regressions](analysis/out/module_b/table4_regressions.md) |
| Read retail allocation results | [Retail returns and cornerstone sensitivity](analysis/out/research_frontier/research.md) |
| Read A+H or margin results | [A+H prices](analysis/out/ah_anchor/ah_anchor.md) / [Margin financing](analysis/out/margin/margin.md) |
| Continue the research | [Current plan](docs/RESEARCH_PLAN_2026.md) / [Research start](docs/RESEARCH_START.md) |
| Understand the code | [Architecture guide](docs/ARCHITECTURE.md) / [Analysis guide](analysis/README.md) |

The master stores multiple years. Current studies select **2026 by actual listing date**, rather than treating the entire master as the study sample. The sample contains Q1: 38, Q2: 45, and Q3: 30 IPOs. The independent A+H flag identifies 38 issuers; model-specific samples can be smaller.

On GitHub, use the direct file links above. The workspace's relative links are intended for a local checkout with the canonical files present.

## Repository layout

```text
urop-hk-ipo/
|
+-- research_workspace/       DAILY USE: English names, linked files
|   +-- 01_workbooks/            2026 quarterly Excel
|   +-- 02_research_inputs/      CSV, A+H and margin inputs
|   +-- 03_data_dictionary/      Field definitions and codebooks
|   +-- 04_reports_and_plans/    Research report and next steps
|   +-- 05_analysis_results/     Tables and figures by topic
|   +-- 06_sources_and_audits/   Evidence and audit records
|   `-- 07_historical_data/     Stored 2025 data
|
+-- analysis/                 RESEARCH CODE
|   +-- research_inputs.py       Data loading and sample selection
|   +-- specifications/         Study hypotheses and sample rules
|   +-- shared/                 Estimation, inference, presentation
|   +-- run.py                  Study registry and execution
|   +-- tests/                  Analysis contracts
|   `-- out/                    Generated results
|
+-- pipeline/                 DATA PRODUCTION
|   +-- cohorts/                Canonical quarterly workbooks
|   +-- exports/                Clean CSV and master panel
|   +-- codebooks/ + registry/   Generated field descriptions
|   +-- sources/ + reports/     Listing sources and evidence reviews
|   `-- prospectus_pipeline/    Collection, validation and writeback
|
+-- config/                   Research workspace artifact catalog
+-- tools/                    Workspace maintenance
+-- docs/                     Research plans, architecture, reports
+-- run.py                    One command entry point
`-- Makefile                  Checks, refresh, and analysis commands
```

## Start using the project

Use Python 3.9 or later, from a source checkout:

```bash
git clone https://github.com/GZ-November/urop-hk-ipo.git
cd urop-hk-ipo
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[analysis,dev]'
make check-code
```

Editable installation supplies dependency profiles and project metadata. Keep the source checkout, configs, schemas, and research artifacts together.

### Browse files or run a study

```bash
# Verify the English index; recreate missing links when needed.
make workspace-check
make workspace

# List studies without changing data or results.
python run.py analysis --list

# Begin with the current basic-statistics plan.
make basic-analysis

# Run one study, or several in the registered order.
python run.py analysis --study underpricing
python run.py analysis --study ah --study margin

# Regenerate all current 2026 analysis outputs.
make analysis
```

The runner uses separate processes and stops at the first failed study. Shared inference and reporting do not import study report scripts. The existing direct script commands remain available.

### Inspect or update the data pipeline

```bash
# Config paths are relative to pipeline/.
python run.py status --config prospectus_pipeline/config_2026q3.yaml
python run.py audit --target all --config prospectus_pipeline/config_2026q3.yaml

# After an authorized workbook update, export that cohort first.
python run.py export --config prospectus_pipeline/config_2026q3.yaml
python run.py master --derive

# Start collection for an explicit listing interval.
python run.py collect --period-start 2026-04-01 --period-end 2026-06-30
```

Collection exits with code `3` while extraction or independent review is pending. Complete those gates, then resume the same command. Workbook writes retain the existing evidence checks, transaction handling, styles, and pre-write snapshots.

The current plan starts with coverage and basic statistics, then prioritizes subscription demand and retail allocation returns. A+H pricing is a third candidate. PR #28 includes the 6872.HK disclosure repair and additional A+H references; see the [collection ledger](pipeline/reports/data_gap_collection/README.md). The PDF progress report is an earlier result snapshot; generated reports contain the current estimates.

## How to interpret the results

- **Exploratory research:** existing data and results have already been examined. The current models do not establish causal effects.
- **Correct price units:** first-day returns compare raw offer and raw closing prices. HDR quantities use the documented unit conversion.
- **Honest missing values:** unknown investor classifications and immature windows are not zeros.
- **Comparable regression columns:** nested underpricing models share a complete-case sample. HC3, month-clustered inference, and restricted wild bootstrap tests are reported.
- **Different return denominators:** first-day returns, allocation-weighted returns, and returns on application funds answer different questions.
- **Limited event coverage:** later-return and lockup samples depend on observed windows. The cutoff is not the report publication date.

Completed repairs and remaining source limitations are documented in [research readiness](pipeline/reports/research_readiness/README.md). A hash identifies a file version; it does not prove an economic interpretation. Field-level review does not certify every field for an issuer.

## <a id="港股-ipo-数据采集与实证研究流水线20002026-全周期中英双语指南"></a>End-to-End Collection Workflow & 2000–2026 Architecture / 港股 IPO 数据采集与实证研究流水线（2000–2026 全周期中英双语指南）

> For the comprehensive operational manual with detailed architecture diagrams and checklists, see **[End-to-End Workflow & 2000–2026 Collection Guide (docs/WORKFLOW_2000_2026.md)](docs/WORKFLOW_2000_2026.md)**.
> 完整系统架构图、算子细则与工程规范详见 **[全周期工作流与 2000–2026 指南 (docs/WORKFLOW_2000_2026.md)](docs/WORKFLOW_2000_2026.md)**。

---

### 1. 6-Stage End-to-End Workflow / 全流程六步工作流

```text
  [Stage 1: Plan & Scope]           python3 run.py plan <period>
           |
           v
  [Stage 2: Official Discovery]     python3 run.py start --board <MB|GEM> ...
  (0-Token Native Tables)           -> Emits Exit Code 3 (WORK_PENDING)
           |
           v
  [Stage 3: Bundled Extraction]     python3 run.py work next --config CONFIG
  (Orchestrator + Subagents)        -> Issuer bundle (prospectus + allot + gem)
           |
           v
  [Stage 4: Independent Review]     python3 run.py work next --config CONFIG
  (Dual-Blind Sign-Off)             -> 700-char excerpts + payload SHA-256
           |
           v
  [Stage 5: Hash-Gated Write-Back]  python3 run.py resume --run-dir ...
  (Deterministic Enrichment)        -> market, hkma, hsic, aftermarket, audit
           |
           v
  [Stage 6: Export, Master & ZIP]   export -> master --derive -> bundle
```

#### Stage 1: Plan & Scope / 第一步：计划编制与周期划分
- **English**: Run `python3 run.py plan <period>` (e.g. `2000..2026` or `2025Q4`). The planner deterministically partitions the target listing interval into non-overlapping `[board × calendar quarter]` cohort jobs, automatically identifies and reuses existing `stored` cohorts in `pipeline/cohorts/`, and prints reproducible `run.py start` commands.
- **中文**: 运行 `python3 run.py plan <period>`（如 `2000..2026` 或 `2025Q4`）。系统自动将跨度区间分解为不重叠的 `[板块 × 自然季度]` 执行单元，自动检测并复用 `pipeline/cohorts/` 下已归档的 `stored` 队列，输出标准可重现的 `run.py start` 命令。

#### Stage 2: Official Discovery, Download & 0-Token Native Table Pre-Parsing / 第二步：官方发现、披露下载与 0-Token 原生表格预解析
- **English**: Runs official discovery from HKEX listing reports (`.xls` via `xlrd` for pre-2020 cohorts and `.xlsx` for 2020+), isolates ordinary IPOs, downloads official Prospectus and Allotment PDFs, and generates a single deduplicated packet (`HKIPO-MBxxxx.md`, `--no-topics` by default).
  - **Native Geometric Table Parser (`src/table_parser.py`)**: Extracts Financial Summary/Accountants' Report tables, Share Capital tables (via a robust 2-pass total scan), Cornerstone tables, and Underwriting tables directly from PDF coordinates at **0 LLM token cost**, wrapping them in `<!-- TABLE_START --> ... <!-- TABLE_END -->`. It preserves all actual historical period columns through X-coordinate alignment (no `nums[:4]` truncation or synthetic `Year-3/2/1` headers), strips extraneous `% of revenue` columns, and skips parent-only balance sheets (`is_company_level_statement`) in favor of Group Consolidated/Combined statements.
- **中文**: 自动下载港交所官方新上市公司报告（2020 之前采用 `xlrd` 解析 `.xls`，2020 及以后采用 `.xlsx`），甄别排除介绍上市与转板，下载招股书及配发结果 PDF，并生成单一去重的抽取底稿（`HKIPO-MBxxxx.md`，默认启用 `--no-topics`）。
  - **0-Token 原生空间几何表格解析引擎 (`src/table_parser.py`)**: 直接基于 PDF 空间几何坐标簇解析财务摘要三表、股本结构表（两轮全扫描回退机制）、基石配售表和承销费用表，注入 `<!-- TABLE_START -->` 区块，**完全零消耗 LLM Token**。通过 X 轴视网膜投影严格保留真实会计期间（杜绝截断或伪造年份头），过滤收入百分比列，并基于 `is_company_level_statement` 严格剔除母公司单体报表以确保集团口径。

#### Stage 3: Exit Code 3 Protocol & Lease-Scheduled Extraction / 第三步：Exit 3 协议与租约抽取
- **English**: The collection process deterministically exits with **Exit Code 3 (`WORK_PENDING`)** when extraction or review is pending, safeguarding research workbooks against unverified edits.
  - **Orchestrator + Subagent Architecture**: The orchestrator (e.g., Argon / parent agent) claims work leases via `python3 run.py work next --config CONFIG`. Each lease bundles all targets of an issuer (`prospectus`, `allot`, and `gem`) so a single extractor subagent handles the issuer in one context without redundant reading.
  - **Fixed Financial-Period Standard (Teacher's Manual §2.3)**: `year-1` is the latest period of the audited Track Record in the Accountants' Report (full fiscal year or 3–11 month stub; `col_AT` records its end date); `year-2` and `year-3` are the two preceding complete financial years (never derived by subtraction); unaudited post-track-record disclosures are never `year-1`; only Net Sales (`col_AH`), PBT (`col_AK`), and PAT (`col_AN`) are annualised (`× 12 / months`).
  - **Token Optimization**: Extractors read pre-injected `search periods`, `search sharecap`, `col_CR`, and `<!-- TABLE_START -->` tables first, and batch remaining queries into a single `run.py search bundle CODE --fields ...` call. Subagents finish with `work finish-extract`, triggering deterministic derivation (`derive_allot` for `col_CV` greenshoe, `col_CK` cornerstone absence, `col_CQ` pricing date, `col_DA/DB/DC` free float) and schema validation.
- **中文**: 当存在待抽取或待复核数据时，流水线规范退出并返回**退出码 3 (`WORK_PENDING`)**，杜绝未经验证的数据静默写入。
  - **父智能体编排与子智能体并发**: 主调度器运行 `python3 run.py work next --config CONFIG` 申领发行人绑定的抽取租约（单一发行人的 `prospectus`、`allot`、`gem` 捆绑由一个子智能体在单轮会话中完成，避免重复阅读公司背景与股本信息）。
  - **固定会计期间准则（导师手册 §2.3）**: `year-1` 严格为申报会计师报告（Accountants' Report）中经审计营业纪录期（Track Record Period）的最近一期（完整年或 3–11 个月 Stub 期间，`col_AT` 为其截止日）；`year-2` 与 `year-3` 为其前两个完整会计年度（严禁倒减生成）；未经审计的期后数字绝不能作为 `year-1`；仅主营收入 (`col_AH`)、税前利润 (`col_AK`) 与净利润 (`col_AN`) 进行年化折算 (`× 12 / months`)。
  - **Token 极致优化**: 抽取子智能体优先读取 Brief 中预注入的会计期间、股本及 `<!-- TABLE_START -->` 结构化表格，余下字段通过 `run.py search bundle CODE --fields ...` 单次批量查询；调用 `work finish-extract` 自动完成确定性衍生（`derive_allot` 结算绿鞋 `col_CV`、基石缺失 `col_CK`、定价日 `col_CQ`、自由流通盘 `col_DA/DB/DC`）与校验。

#### Stage 4: Independent Review / 第四步：独立双盲交叉复核
- **English**: A separate independent review subagent claims a review lease via `work next`. It inspects the 700-character original page excerpts embedded in the brief's `Review sheet`. It opens full pages or runs full-text searches only when an excerpt is truncated, a validation warning exists, or a field is marked missing (`NaN`/`NA`). Approval is recorded with `work finish-review --verdict pass`, anchoring the exact `payload sha256`.
- **中文**: 独立的复核子智能体申领复核租约，优先核对 Brief `Review sheet` 中内嵌的 700 字符原文切片。仅在原文切片被截断、出现校验警告或字段缺失（`NaN`/`NA`）时才检索全文。复核通过后调用 `work finish-review --verdict pass` 签署并锁定该载荷的 SHA-256 哈希凭证。

#### Stage 5: Hash-Gated Write-Back & External Enrichment / 第五步：哈希门禁回写与外部计量增广
- **English**: Running `python3 run.py resume --run-dir ...` validates reviewer credentials, creates timestamped Excel workbook backup snapshots, writes reviewed cells into the cohort workbook, and executes deterministic external pipelines:
  - `disclosure_notes`: Derives `col_BC = months / 12` and writes unadjusted values to `col_CN/CO/CP`.
  - `market`: Fetches split-adjusted daily prices via Tencent Quote API with Yahoo Finance fallback.
  - `hkma`: Obtains Exchange Fund base rates and HIBOR with local CSV interval caching.
  - `hsic`, `flags`, `rules`, `aftermarket` (1M/6M BHR, Wealth Relatives, liquidity decay), `academic` (underpricing, retail rationing, cornerstone demands), and `audit` & `cross_check`.
- **中文**: 运行 `python3 run.py resume --run-dir ...` 校验复核凭证，生成带有时间戳的 Excel 备份快照，将通过复核的数据安全回写至工作簿，并自动化执行后续确定性衍生增广：
  - `disclosure_notes`：计算年化因子 `col_BC = months / 12`，原始未折算值归档于 `col_CN/CO/CP`。
  - `market`：通过腾讯证券高频接口获取前复权日 K 线（雅虎财经自动热备降级）。
  - `hkma`：获取金管局基准利率与 HIBOR（支持本地 CSV 区间缓存）。
  - `hsic` 恒生行业分类、`aftermarket`（1M/6M BHR、财富相对比 WR、流动性衰减比）、`academic` 学术变量及 `audit` / `cross_check` 规则合规审查。

#### Stage 6: Export, Master Panel & Delivery / 第六步：数据导出、主面板合并与成果归档
- **English**: `run.py export` outputs clean econometric CSVs and Markdown Codebooks. `run.py master --derive` merges the cohort into the multi-year master panel (`HKIPO-MB-MASTER_clean.csv`). `run.py bundle` compiles deliverables into a verified ZIP containing `manifest.json` and `quality_summary.json`.
- **中文**: `run.py export` 导出符合计量经济学规范的纯净 CSV 与学术变量字典 Markdown。`run.py master --derive` 将季度数据合并入跨年度总面板（`HKIPO-MB-MASTER_clean.csv`）。`run.py bundle` 生成包含完整工件、`manifest.json` 与 `quality_summary.json` 的交付 ZIP 压缩包。

---

### 2. 2000–2026 Historical Compatibility Guarantees / 2000–2026 跨周期历史兼容保障

| Compatibility Dimension / 兼容维度 | Technical Implementation / 核心技术实现 | Source References / 对应源码 |
|---|---|---|
| **1997–1999 Track Record & 2-Digit Century**<br>(1997–1999 营业纪录期与两位数世纪年份转换) | All year regexes expanded to `(?:199\d\|20\d\d)` to support 2000–2002 IPOs whose 3-year Track Record spans 1997–1999. Two-digit year mapping implements `year = (year + 1900 if year >= 70 else year + 2000) if year < 100 else year`, ensuring `31/12/99 -> 1999-12-31`. | `src/periods.py`<br>`src/table_parser.py`<br>`tools/search.py` |
| **Historical Accounting Standards**<br>(合并前结合报表与历史会计准则) | Recognizes pre-IPO reorganization `COMBINED` financial statements alongside `CONSOLIDATED` statements. Recognizes historical UK/HKGAAP terms: `Turnover` (Revenue), `PROFIT AND LOSS ACCOUNT` (Statement of Profit or Loss), `Net assets` (Total Equity), and `SSAP` / `HKGAAP`. | `src/periods.py`<br>`src/pdfprep.py`<br>`src/table_parser.py`<br>`tools/search.py` |
| **Date-Aware Rule 8.09(2) Market Cap**<br>(动态法定最低市值门槛校验) | Enforces statutory Main Board Rule 8.09(2) market cap thresholds based on listing date: `< 2004-03-31`: HK$100M; `2004-03-31 .. 2018-02-14`: HK$200M; `>= 2018-02-15`: HK$500M (plus Chapter 18A HK$1.5B and Chapter 18C HK$4B/8B). | `src/cross_check.py` |
| **Cross-Decade Stabilization Dates**<br>(跨年代价格稳定公告日期识别) | Accurately extracts price stabilization termination and exercise dates under Cap 571W across British order (`15 July 2004`) and US order (`Wednesday, January 28, 2026`) across `199\d\|20\d\d`. | `src/stabilization_panel.py` |
| **Pre-HSTECH Fallback & K-Line Chunking**<br>(恒科指数前置平滑、K线分块与视界截断) | Gracefully returns empty HSTECH bars for pre-2015/2020 IPOs without raising errors, ensuring HSI returns compute uninterrupted. Automatically chunks Tencent K-line requests (`> 750` days) into 730-day windows to prevent 640-bar truncation, falls back to `fqkline/get` on 404 yearly `.js` files, and strictly bounds queries to 12M (`aftermarket.py`) or 36M (`market_panel.py`). | `src/market_fetcher.py`<br>`tools/external/aftermarket.py`<br>`src/market_panel.py` |

---

## Checks, data distribution, and contribution

`make check-code` runs syntax/static checks, pipeline tests, analysis tests, and registry consistency. CI uses the same command. `make workspace-check` checks catalog links separately. Code tests do not constitute a full semantic audit of every disclosure.

The repository versions public-disclosure research artifacts, including workbooks, CSVs, extraction evidence, codebooks, and reports. Raw PDF/full-text caches, credentials, workbook backups, and local run logs stay local. Some collection jobs require those locally stored source files; see [Contributing](CONTRIBUTING.md) and [Security and data policy](SECURITY.md).

Further reading: [Documentation index](docs/README.md), [artifact placement](docs/REPOSITORY_GUIDE.md), [pipeline operations](pipeline/SYSTEM_MANAGEMENT.md), and [pipeline CLI](pipeline/prospectus_pipeline/README.md).

[MIT License](LICENSE)
