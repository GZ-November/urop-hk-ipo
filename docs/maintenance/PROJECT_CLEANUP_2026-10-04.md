# 项目目录整理（2026-10-04）

日常查看从 [Research Workspace](../../research_workspace/README.md) 开始。七个分类目录各有简短索引。最新综合报告、Markdown 文本及配套统计表已补入目录；旧报告与当前结果分开。

## 实际处理

| 处理 | 数量 | 说明 |
|---|---:|---|
| 删除可再生成的缓存 | 196 个文件，15 个缓存目录 | Python 字节码与 pytest 缓存；约 2.53 MiB |
| 删除重复快捷链接 | 28 个 | 带“2”的链接与原链接存储的目标路径完全相同；只删除链接，不删除目标 |
| 移除空测试目录 | 45 个 | 四个空 mock／tmp 测试目录及其空子目录；删除前逐项确认无文件 |
| 移动已有文件 | 6 个 | 旧报告、历史检查、清理记录和本地文献，见下表 |
| 补充日常目录入口 | 4 个 | 当前报告 LaTeX、Markdown、配套表格和历史检查目录 |
| 迁移旧报告入口 | 2 个 | 从当前报告分类移至历史分类 |
| 补充分类说明 | 7 份 | 每个日常目录说明用途、文件及正式位置 |

## 文件的新位置

| 原位置 | 新位置 |
|---|---|
| `docs/reports/HK_IPO_RESEARCH_PROGRESS_STE_2026.pdf` | [旧报告 PDF](../archive/research-progress-2026-10-02/HK_IPO_RESEARCH_PROGRESS_STE_2026.pdf) |
| `docs/reports/HK_IPO_RESEARCH_PROGRESS_STE_2026.tex` | [旧报告 LaTeX](../archive/research-progress-2026-10-02/HK_IPO_RESEARCH_PROGRESS_STE_2026.tex) |
| `docs/CODE_REVIEW_2026-09-30.md` | [历史代码检查](../archive/reviews-2026-09-30/CODE_REVIEW_2026-09-30.md) |
| `docs/AGY_INTEGRATION_2026-09-30.md` | [历史来源集成复核](../archive/reviews-2026-09-30/AGY_INTEGRATION_2026-09-30.md) |
| `docs/reports/PROJECT_CLEANUP_2026-10-03.md` | [上一轮清理记录](PROJECT_CLEANUP_2026-10-03.md) |
| `Survey Paper/Lowry, Michaely & Volkova 2017 IPO survey.pdf` | `docs/literature/Lowry, Michaely & Volkova 2017 IPO survey.pdf`（仅本地） |

旧报告 PDF、LaTeX、上一轮清理记录和文献的字节未变。两份历史检查只调整相对链接，保留原有发现、数值和时间口径。已更新仓库内的现有引用与 workspace catalog。根目录的空 `Survey Paper/` 已移除，文献 PDF 在新位置继续由 Git 忽略。

## 保留与检查

清理前后核对了 8,683 个保护文件。其中 8,682 个 SHA-256 完全相同；另一份 `pipeline/reports/margin_review/README.md` 只更新了历史集成报告的链接。保护范围包括正式工作簿、导出、字典、官方来源、原始披露、提取 JSON、采集状态、修正证据、历史采集数据、分析输出，以及当前综合报告的 LaTeX 和 Markdown 文件。哈希一致仅证明本次整理没有改变文件，不代表重新核实了数据内容。

当前打开的 `HK_IPO_2026_COMPREHENSIVE_REPORT.tex` 保持原位置和内容。正式数据路径与生成器入口未改动。仍在使用的未提交报告草稿和来源笔记也保留原位置。

57 个 catalog 快捷链接已检查。文档的本地链接及 `git diff --check` 已检查。本次没有修改研究计算或运行数据写回。

原始披露、2025 历史采集目录、Python 环境、有效验证运行和前次清理归档仍有用途，因此保留。`pipeline/` 负责数据采集、存储和核对；研究代码与产物位于 `analysis/`。

## 本地清单与恢复

逐文件移动、删除、链接目标和保护哈希保存在 [本次清单](../../pipeline/backups/local_cleanup_2026-10-04/manifest.json)。这是被 Git 忽略的本地维护文件。

移动文件可按清单反向恢复；先确认旧路径为空，避免覆盖后续文件。重复快捷链接可按清单中的 `path` 和 `target` 重建。删除的缓存由正常运行重新生成。上一轮旧运行的压缩归档与恢复方式仍见 [2026-10-03 清理记录](PROJECT_CLEANUP_2026-10-03.md)。
