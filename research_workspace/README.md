# Research Workspace

本地日常入口：双击项目根目录的 **[00_START_HERE.html](../00_START_HERE.html)**，可用中文搜索 Excel、CSV、报告、模板和历史文件。Finder 中的 **`00_Research_Files`** 快捷目录也直接进入这里。

This is the daily entry point for research data, reports, and results.
All directory and file names use English.
The stored data include 2025 Q1–Q2 and 2026 Q1–Q3. The current 2026 study contains 113 IPOs: Q1 38, Q2 45, and Q3 30.
The observation cutoff is 30 September 2026.

| Directory | Contents |
|---|---|
| [01_workbooks](01_workbooks/) | Canonical 2025 Q1–Q2 and 2026 Q1–Q3 Excel workbooks |
| [02_research_inputs](02_research_inputs/) | Clean quarterly CSVs, master panel, A+H references, and margin observations |
| [03_data_dictionary](03_data_dictionary/) | Quarterly codebooks, variable registry, and terminology |
| [04_reports_and_plans](04_reports_and_plans/) | Current comprehensive report, mentor draft, plans, and source assessment |
| [05_analysis_results](05_analysis_results/) | Generated tables and figures, grouped by research topic |
| [06_sources_and_audits](06_sources_and_audits/) | Official sources, source evidence, extraction records, and audits |
| [07_historical_data](07_historical_data/) | Cross-year references and historical-data navigation |

## Current English research reports

- [2026 comprehensive report: LaTeX source](04_reports_and_plans/2026_Comprehensive_Report.tex) / [text](04_reports_and_plans/2026_Comprehensive_Report.md)
- [Mentor discussion draft: corrected one-lot results, no simulation](04_reports_and_plans/Retail_Mentor_Brief.md)
- [Source reassessment and exclusion results](04_reports_and_plans/Retail_Evidence_Assessment.md)
- [Retail IPO applications: consolidated report](04_reports_and_plans/Current_Empirical_Research_Report.md)
- [Implementation and reproduction](04_reports_and_plans/Retail_Research_Implementation.md)
- [Subscription demand results](05_analysis_results/12_subscription_demand/)
- [Tier-based retail allocation results](05_analysis_results/13_retail_allocation_profit/)
- [Profit distributions, fee frontiers and robustness](05_analysis_results/14_retail_profit_distributions/)
- [Deterministic source-corrected tables](05_analysis_results/15_retail_evidence_brief/)
- [Comprehensive report tables and workbook field coverage](05_analysis_results/16_comprehensive_report_tables/)

## Frequently used files

- [2026 Q3 Excel workbook](01_workbooks/2026_Q3_IPO_Data.xlsx)
- [Latest comprehensive report](04_reports_and_plans/2026_Comprehensive_Report.tex)
- [Current research plan](04_reports_and_plans/Current_Research_Plan.md)
- [2025 Q1 workbook](01_workbooks/2025_Q1_IPO_Data.xlsx) / [2025 Q2 workbook](01_workbooks/2025_Q2_IPO_Data.xlsx)
- [All-years master panel](02_research_inputs/All_Years_Master_Panel.csv)

The master includes both 2025 and 2026 listings. Select actual 2026 listing dates for the current study. The analysis input module applies this rule.

## How updates work

These entries are relative links to canonical files, not independent copies. Opening a link opens the original. Updated canonical files appear here automatically. Follow the pipeline's source, validation, and review requirements before changing data.

Retired PDF reports and Markdown/Excel versions have been moved to macOS Trash. The current comprehensive report uses a separate LaTeX source and the editor's PDF preview.

Each directory has a short `README.md` with file links and a description. Cleanup and recovery records are in [project maintenance](../docs/maintenance/README.md). Local reference papers are in [literature](../docs/literature/README.md).

The catalog in [config/research_workspace.json](../config/research_workspace.json) defines the links. To recreate missing links or validate the index:

```bash
make workspace
make workspace-check
```

The manager checks all sources and conflicts before creating links. It does not replace existing user files or conflicting links. If a source is missing, produce or restore that source first.

## Code and reproducibility

The [architecture guide](../docs/ARCHITECTURE.md) explains the code modules and their responsibilities. List or run studies through the root command:

```bash
python run.py analysis --list
python run.py analysis --study basic
python run.py analysis --study underpricing
python run.py analysis --study ah --study margin
```

The default `make analysis` runs all registered studies in their established order. Pipeline commands and canonical paths remain available.

Do not distribute this directory alone: it contains links. Copy the actual files you want to share, or distribute the project with their targets.
