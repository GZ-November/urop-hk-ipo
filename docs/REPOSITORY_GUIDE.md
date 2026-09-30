# 仓库组织与维护

## 放在哪里

| 工件 | 归属 | 维护方式 |
|---|---|---|
| CLI / pipeline 逻辑 | `run.py`、`pipeline/prospectus_pipeline/src/`、`tools/` | 路径遵循 `paths.py` 与 `master_contracts.py` |
| 研究代码与测试 | `analysis/`、`analysis/tests/` | 每个研究模块一个明确入口；新增模块更新分析索引 |
| 工作簿、导出、证据 | `pipeline/cohorts/`、`exports/`、`prospectus_pipeline/data/`、`out/` | 保留现行合同；人工采集须有来源；导出由 producer 生成 |
| 表格与图 | `analysis/out/<module>/` | 由代码生成，避免手工修正文内数值 |
| 研究设计与证据说明 | `docs/` | 更新 [文档索引](README.md)，标明样本、基准日期与结果链接 |
| 被取代的数值稿 | `docs/archive/<reason>/` | 加历史说明；旧入口保留导航链接 |
| 审计、修正与排除记录 | `pipeline/reports/` | 保留可追溯明细和观测截止日期 |
| 待核实候选 | 如 `pipeline/reports/margin_review/*UNVERIFIED*` | 与正式来源 ledger 和分析输入隔离 |
| skill | `.agents/skills/` | 项目版本受 Git 管理；修改时同步相关入口 |
| 临时实验、日志与大缓存 | `pipeline/scratch/` 等 `.gitignore` 指定位置 | 仅本地；验证后再转为正式模块或来源工件 |

公开披露形成的工作簿、CSV、提取证据及复现输出是有意追踪的研究工件。不能按扩展名批量删除 JSON/CSV/XLSX，也不能把复现数据当成普通缓存清理。原始 PDF、全文切片、模型日志和工作簿备份按 [贡献指南](../CONTRIBUTING.md) 与 [ignore 规则](../.gitignore) 保留在本地。

## 分支和多个 checkout

整理于 2026-09-30：研究修正已通过 PR #20 合并到 main；本次整理从该 main 新建 `codex/repo-research-organization`。此前的研究分支和 worktree 仍保留用于追溯。

桌面主 checkout 存在 agy 的未提交修改及未追踪材料，且当时 main 落后一个提交。它们没有在本次整理中覆盖或删除。继续研究应先确认自己所在 checkout 的提交和工作区状态，不要从这些旧本地结果误读当前研究结论。

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

文档变更检查链接与 `git diff --check`。代码或数据口径变化运行相关回归测试及 `make check-code`；分析行为变化重新生成对应输出。行情刷新、证据审计和代码测试各有不同覆盖，不能用其中一项宣称所有数据已核实。

新增研究应在提交中同时包含代码、样本筛选与生成结果，并在设计文档里链接输出；保留来源与覆盖记录。归档旧数值报告时保留其内容，不把新结论写入历史稿。
