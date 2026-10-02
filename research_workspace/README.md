# Research Workspace

This is the daily entry point for research data, reports, and results.
All directory and file names use English.
The current 2026 sample contains 113 IPOs: Q1 38, Q2 45, and Q3 30.
The observation cutoff is 30 September 2026.

| Directory | Contents |
|---|---|
| [01_workbooks](01_workbooks/) | Canonical 2026 quarterly Excel workbooks |
| [02_research_inputs](02_research_inputs/) | Clean quarterly CSVs, master panel, A+H references, and margin observations |
| [03_data_dictionary](03_data_dictionary/) | Quarterly codebooks, variable registry, and terminology |
| [04_reports_and_plans](04_reports_and_plans/) | PDF/LaTeX progress report, current plan, design, and repair status |
| [05_analysis_results](05_analysis_results/) | Generated tables and figures, grouped by research topic |
| [06_sources_and_audits](06_sources_and_audits/) | Official sources, source evidence, extraction records, and audits |
| [07_historical_data](07_historical_data/) | Stored 2025 Q1/Q2 workbooks and cross-year inputs |

## Frequently used files

- [2026 Q3 Excel workbook](01_workbooks/2026_Q3_IPO_Data.xlsx)
- [English research progress report](04_reports_and_plans/Research_Progress_Report.pdf)
- [Current research plan](04_reports_and_plans/Current_Research_Plan.md)
- [All-years master panel](02_research_inputs/All_Years_Master_Panel.csv)

The master includes both 2025 and 2026 listings. Select actual 2026 listing dates for the current study. The analysis input module applies this rule.

## How updates work

These entries are relative links to canonical files, not independent copies. Opening a link opens the original. Updated canonical files appear here automatically. Follow the pipeline's source, validation, and review requirements before changing data.

The PDF is an exported snapshot. Changes to its LaTeX source require a new PDF export.

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
python run.py analysis --study underpricing
python run.py analysis --study ah --study margin
```

The default `make analysis` runs all registered studies in their established order. Pipeline commands and canonical paths remain available.

Do not distribute this directory alone: it contains links. Copy the actual files you want to share, or distribute the project with their targets.
