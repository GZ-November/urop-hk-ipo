# 本地文件导航与归档（2026-10-04）

从项目根目录双击 [00_START_HERE.html](../../00_START_HERE.html)，可搜索 Excel、CSV、报告、模板、来源和历史材料。Finder 中双击 `00_Research_Files`，直接进入原有 `research_workspace/` 的七个分类目录。

## 已完成

| 处理 | 数量 | 内容 |
|---|---:|---|
| 中文可搜索导航 | 82 个文件与目录入口 | 当前 Excel、CSV、报告、分析结果、字段与来源、模板、历史与恢复；顶部可直接打开 2026 三个季度的 Excel |
| 维护分类快捷目录 | 62 个链接 | 补入两个本地 PDF 所在目录、概览草稿和三个来源笔记入口 |
| 集中本地 PDF | 2 个文件 | `Reports/` 移到 `docs/reports/exported_pdfs/`；原文件名和内容保留 |
| 归档旧采集 Excel 快照 | 37 个文件 | 原位于 2025 Q1/Q2 旧采集目录的 `backups/excel_snapshots/`；每个成员先核对 SHA-256，再移除旧路径 |
| 清理可再生成的缓存与目录元数据 | 201 个文件 | Python/pytest 缓存和 `.DS_Store`，合计 2.60 MiB |
| 移除空目录 | 64 个 | 空测试、空运行及归档后空目录 |
| 核对研究材料 | 8949 个文件 | 正式工作簿、导出、原始披露、提取、状态、研究输出和文档的字节保持一致；移动的 PDF 按新路径核对 |

37 份旧快照原占 18.05 MiB，归档包占 5.12 MiB。它们不是正式季度数据。五个正式季度的最新快照仍在 `pipeline/cohorts/backups/excel_snapshots/`。

正式工作簿与 CSV 的路径保持稳定。2025 Q1/Q2 数据、2025 Q3 旧采集工作簿、原始披露、审核证据和采集状态都保留。导航明确区分正式数据、空白模板、来源表和恢复快照。现有报告草稿与来源笔记继续保留，PDF 作为静态导出稿。

## 日常存放方式

- 正式 Excel：`pipeline/cohorts/`；常用入口 `00_Research_Files/01_workbooks/`。
- 合并和季度 CSV：`pipeline/exports/`；常用入口 `00_Research_Files/02_research_inputs/`。
- 当前报告、草稿与本地 PDF：`docs/reports/`；常用入口 `00_Research_Files/04_reports_and_plans/`。
- 研究结果：`analysis/out/<study>/`；常用入口 `00_Research_Files/05_analysis_results/`。
- 历史报告：`docs/archive/`；旧运行与恢复材料：`pipeline/backups/`。

更新 `config/research_workspace.json` 后运行 `make workspace` 维护快捷链接，再运行 `python3 tools/build_file_index.py` 重建导航。导航生成器会同时发现模板目录与官方来源目录中的 Excel。

## 恢复

- [本次旧 Excel 快照归档](../archive/README.md)
- [原路径、SHA-256 与逐文件处理清单](../../pipeline/backups/file_organization_2026-10-04/manifest.json)

归档成员保留原项目相对路径。恢复时先解压到一个新的空目录，按清单选择所需文件，再复制到项目内的合适位置，避免覆盖后续版本。两个 PDF 可按清单反向移动回原 `Reports/`。快捷链接可重新生成；Python 缓存由正常运行重新生成。

本轮核对仅验证整理没有改变研究文件的字节，不等于重新审核数据经济含义或来源。未运行数据写回或研究结果再生成。

## 导航检查

62 个 catalog 快捷链接和导航页的 89 个本地链接全部有效。搜索脚本通过全部入口、当前 Excel、季度、导师、PDF 和无匹配六种情况的逻辑检查；Python 静态检查与 Git diff 格式检查通过。工具内浏览器不支持 `file://` 本地页面，因此未进行浏览器截图核验；可在 Finder 中双击 HTML 使用。

后续处理（2026-10-04）：按用户要求，五个正式季度的旧备份、三份旧采集 Excel、旧成本表和过时 Markdown 已进一步合并收起，当前恢复位置见 [旧版本归档说明](../archive/README.md)。本记录中的原位置描述的是本轮整理当时状态。

最终处理（2026-10-04）：按用户要求，以上本轮创建的两个旧文件归档包已移到 macOS 垃圾桶，项目中不再保留这些包；需要时可从垃圾桶放回。

发布准备（2026-10-04）：两份本地 PDF 内容完全一致，保留的一份统一命名为 `HK_IPO_2026_Comprehensive_Report.pdf`；重复副本已移入垃圾桶。导航不再包含只有本机才存在的备份目录，`make workspace` 同时维护快捷链接与导航页。2025 Q1、Q2 数据与 2026 数据并列保留。
