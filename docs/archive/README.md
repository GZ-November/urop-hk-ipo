# 旧文件处理记录

按用户要求，旧 Excel、被取代的研究报告、早期采集问题和成本记录的归档包已移到 macOS 垃圾桶。

垃圾桶内的文件名：

- `legacy_excel_and_markdown_2026-10-04.tar.gz`：9 份旧 Excel、21 份旧 Markdown、1 份旧 PDF 和 1 份 LaTeX。
- `legacy_collection_excel_snapshots.tar.gz`：37 份旧采集 Excel 快照。

归档包含 **9 份 Excel、21 份 Markdown、1 份旧 PDF 和 1 份 LaTeX**。每个文件在移除旧路径前均已核对 SHA-256。归档保留原项目相对路径。

需要找回时，在 Finder 的垃圾桶中找到上述文件，右键选择“放回”；再解压到一个新的空目录，按下列原路径选择文件，避免覆盖当前版本。当前数据入口见 [文件导航](../../00_START_HERE.html)。

## Excel 原路径

- `pipeline/cohorts/backups/excel_snapshots/HKIPO-MB2025Q1.backup-aftermarket-20260930-102800-d7bc24.xlsx`
- `pipeline/cohorts/backups/excel_snapshots/HKIPO-MB2025Q2.backup-aftermarket-20260930-102809-cb4952.xlsx`
- `pipeline/cohorts/backups/excel_snapshots/HKIPO-MB2026Q1.backup-academic_expansion-20260930-151415-fdd4ba.xlsx`
- `pipeline/cohorts/backups/excel_snapshots/HKIPO-MB2026Q2.backup-applied-reconcile-20261003-154153.xlsx`
- `pipeline/cohorts/backups/excel_snapshots/HKIPO-MB2026Q3.backup-applied-reconcile-20261003-154153.xlsx`
- `pipeline/docs/reports/HKIPO_Flash成本汇报.xlsx`
- `pipeline/prospectus_pipeline/datasets/HKIPO_2025-01-01_2025-03-31_HKIPO-MB/HKIPO-MB.xlsx`
- `pipeline/prospectus_pipeline/datasets/HKIPO_2025-04-01_2025-06-30_HKIPO-MB/HKIPO-MB.xlsx`
- `pipeline/prospectus_pipeline/datasets/HKIPO_2025-07-01_2025-09-30_HKIPO-MB/HKIPO-MB.xlsx`

## Markdown 与旧报告原路径

- `docs/ACADEMIC_EXTENSIONS_2026.md`
- `docs/EXTENDED_ANALYSIS_2026.md`
- `docs/archive/README.md`
- `docs/archive/pre-basics-replan/RESEARCH_PLAN_2026.md`
- `docs/archive/pre-raw-price-correction/ACADEMIC_EXTENSIONS_2026.md`
- `docs/archive/pre-raw-price-correction/EXTENDED_ANALYSIS_2026.md`
- `docs/archive/pre-raw-price-correction/RESEARCH_PLAN_2026.md`
- `docs/archive/pre-retail-distribution-2026-10-03/EMPIRICAL_RESEARCH_REPORT_2026.md`
- `docs/archive/pre-retail-distribution-2026-10-03/README.md`
- `docs/archive/research-progress-2026-10-02/HK_IPO_RESEARCH_PROGRESS_STE_2026.pdf`
- `docs/archive/research-progress-2026-10-02/HK_IPO_RESEARCH_PROGRESS_STE_2026.tex`
- `docs/archive/research-progress-2026-10-02/README.md`
- `docs/archive/reviews-2026-09-30/AGY_INTEGRATION_2026-09-30.md`
- `docs/archive/reviews-2026-09-30/CODE_REVIEW_2026-09-30.md`
- `docs/archive/reviews-2026-09-30/README.md`
- `pipeline/docs/PIPELINE_ISSUES_FOR_DEV.md`
- `pipeline/docs/Q2_ACCEPTANCE_GAP.md`
- `pipeline/docs/guides/Q1_浅绿字段采集记录.md`
- `pipeline/docs/reports/Flash低成本采集计划.md`
- `pipeline/docs/template_compatibility_audit.md`
- `pipeline/prospectus_pipeline/archive/HANDOFF_浅蓝42字段.md`
- `pipeline/prospectus_pipeline/archive/reviews/CODE_REVIEW_2026-09-13.md`
- `pipeline/prospectus_pipeline/archive/reviews/WORKFLOW_REVIEW.md`

五个正式季度工作簿、当前 CSV、原始披露与审核证据继续保留。37 份旧 Excel 快照也已移到垃圾桶，原处理记录见 [上轮整理说明](../maintenance/FILE_ORGANIZATION_2026-10-04.md)。逐文件哈希和处理清单位于 `pipeline/backups/legacy_versions_2026-10-04/manifest.json`。

## 清理核验

32 个归档成员均已重新读取并核对哈希；6,891 个保留的数据、来源和输出文件内容未变。61 个分类快捷链接及 85 个导航链接检查通过。当前报告仅替换了旧归档链接，结果清单补充了这次文字维护及新输出哈希，原运行输入记录保留；未重新运行统计或数据写回。

2026-10-04：两个归档包已通过 Finder 移入垃圾桶，并在垃圾桶中确认存在。项目内的归档下载入口和旧快捷链接已经移除。

## GitHub 中的历史版本

垃圾桶位置仅描述本机的处理。仓库中曾追踪的旧报告仍可从 Git 历史找回：整理前的版本是 `70be0d6`，例如 `git show 70be0d6:docs/archive/pre-basics-replan/RESEARCH_PLAN_2026.md`。本地未追踪的 Excel 备份需从本机垃圾桶恢复。
