# 仓库组织与维护

## 放在哪里

本地从根目录 [00_START_HERE.html](../00_START_HERE.html) 查找文件；Finder 中 `00_Research_Files` 直接进入分类目录。

根目录 [Research Workspace](../research_workspace/README.md) 是英文命名的日常资料入口，采用相对文件链接，不改变下表正式路径。链接由 `config/research_workspace.json` 管理，使用 `make workspace` 建立、`make workspace-check` 验证。代码职责与接口见 [Architecture Guide](ARCHITECTURE.md)；PDF仍是导出快照。

| 工件 | 归属 | 维护方式 |
|---|---|---|
| CLI / pipeline 逻辑 | `run.py`、`pipeline/prospectus_pipeline/src/`、`tools/` | 路径遵循 `paths.py` 与 `master_contracts.py` |
| 研究代码与测试 | `analysis/`、`analysis/tests/` | 每个研究模块一个明确入口；新增模块更新分析索引 |
| 工作簿、导出、证据 | `pipeline/cohorts/`、`exports/`、`prospectus_pipeline/data/`、`out/` | 保留现行合同；人工采集须有来源；导出由 producer 生成 |
| 表格与图 | `analysis/out/<module>/` | 由代码生成，避免手工修正文内数值 |
| 研究设计与证据说明 | `docs/` | 更新 [文档索引](README.md)，标明样本、基准日期与结果链接 |
| 当前综合报告与导师短稿 | `docs/reports/` | 当前 LaTeX 与 Markdown 稿；配套表格链接到 `analysis/out/` |
| 被取代的 Excel、数值稿与历史检查 | `docs/archive/README.md` 处理记录 | 已移到本机垃圾桶；曾追踪的文件可从 Git 历史找回 |
| 清理和恢复记录 | `docs/maintenance/` | 逐次记录移动、删除及核验；本地清单放 `pipeline/backups/` |
| 文献副本 | `docs/literature/` | PDF 仅本地保存，说明文件受 Git 管理 |
| 审计、修正与排除记录 | `pipeline/reports/` | 保留可追溯明细和观测截止日期 |
| 待核实候选 | 如 `pipeline/reports/margin_review/*UNVERIFIED*` | 与正式来源 ledger 和分析输入隔离 |
| skill | `.agents/skills/` | 项目版本受 Git 管理；修改时同步相关入口 |
| 临时实验、日志与大缓存 | `pipeline/scratch/` 等 `.gitignore` 指定位置 | 仅本地；验证后再转为正式模块或来源工件 |

公开披露形成的工作簿、CSV、提取证据及复现输出是有意追踪的研究工件。不能按扩展名批量删除 JSON/CSV/XLSX，也不能把复现数据当成普通缓存清理。原始 PDF、全文切片、模型日志和工作簿备份按 [贡献指南](../CONTRIBUTING.md) 与 [ignore 规则](../.gitignore) 保留在本地。

## 分支和多个 checkout

整理于 2026-09-30：研究修正已通过 PR #20 合并到 main；本次整理从该 main 新建 `codex/repo-research-organization`。此前的研究分支和 worktree 仍保留用于追溯。

以下为2026-09-30历史工作区说明，不描述当前checkout：当时桌面主checkout存在agy的未提交修改及未追踪材料，且main落后一个提交。它们没有在本次整理中覆盖或删除。继续研究应先确认自己所在 checkout 的提交和工作区状态，不要从这些旧本地结果误读当前研究结论。

```bash
# 确认当前 checkout 与所有 worktree
pwd
git status --short
git log -1 --oneline
git worktree list

# 开新研究分支前更新 remote，然后从 main 创建
# 仅在当前工作区已妥善保存时切换
git fetch origin
git switch -c codex/your-research origin/main
```

一个 checkout 同时只交给一个写入任务；不同 agent 的 Git 分支与工作簿写回不应共享同一工作区。保留旧分支、worktree 或本地候选直到确认无需恢复后再单独清理。

## 修改后的检查

2026-10-03 的[本地清理记录](maintenance/PROJECT_CLEANUP_2026-10-03.md)列出已删除的缓存、已归档的历史运行、保留材料及恢复位置。带编号的副本只有在与原文件 SHA-256 完全一致时才直接删除；有差异的副本归档保留。

2026-10-04 的[目录整理记录](maintenance/PROJECT_CLEANUP_2026-10-04.md)列出旧报告、历史检查和文献的新位置。日常查看用 `research_workspace/` 的七个分类目录；每个目录都有简短索引。生成器依赖的正式数据路径保持稳定。

文档变更检查链接与 `git diff --check`。代码或数据口径变化运行相关回归测试及 `make check-code`；分析行为变化重新生成对应输出。行情刷新、证据审计和代码测试各有不同覆盖，不能用其中一项宣称所有数据已核实。

新增研究应在提交中同时包含代码、样本筛选与生成结果，并在设计文档里链接输出；保留来源与覆盖记录。归档旧数值报告时保留其内容，不把新结论写入历史稿。

[2026-10-04 文件导航与快照归档](maintenance/FILE_ORGANIZATION_2026-10-04.md)记录本轮导航入口、PDF 集中和旧 Excel 快照归档。修改导航来源后运行 `python3 tools/build_file_index.py`；分类快捷链接继续用 `make workspace` 维护。

## 用户确认的保留范围（2026-10-04）

2025 Q1、2025 Q2 的正式 Excel、季度 CSV、变量说明及对应来源证据是用户明确需要的研究数据，长期保留。与 2026 数据一起放入日常入口；不能仅因年份较早而作为旧版本清理。原数据内容及 pipeline 正式路径保持稳定。
