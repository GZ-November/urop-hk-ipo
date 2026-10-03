# Hong Kong IPO Research

[![CI](https://github.com/GZ-November/urop-hk-ipo/actions/workflows/ci.yml/badge.svg)](https://github.com/GZ-November/urop-hk-ipo/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**From HKEX disclosures to research data and reproducible IPO analysis.**

This project builds evidence-linked datasets for ordinary Hong Kong Main Board IPOs. It studies first-day returns, retail allocation, cornerstone investors, A+H pricing, margin financing, and returns after listing.

**Current study: 113 IPOs listed in 2026 Q1-Q3 | 202-variable workbook schema | Observation cutoff: 30 September 2026.**

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
| Discuss the retail study with a supervisor | [Latest mentor brief](docs/reports/RETAIL_MENTOR_BRIEF_2026-10-03.md) / [Source reassessment and exclusions](docs/reports/RETAIL_EVIDENCE_ASSESSMENT_2026-10-03.md) |
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

## Checks, data distribution, and contribution

`make check-code` runs syntax/static checks, pipeline tests, analysis tests, and registry consistency. CI uses the same command. `make workspace-check` checks catalog links separately. Code tests do not constitute a full semantic audit of every disclosure.

The repository versions public-disclosure research artifacts, including workbooks, CSVs, extraction evidence, codebooks, and reports. Raw PDF/full-text caches, credentials, workbook backups, and local run logs stay local. Some collection jobs require those locally stored source files; see [Contributing](CONTRIBUTING.md) and [Security and data policy](SECURITY.md).

Further reading: [Documentation index](docs/README.md), [artifact placement](docs/REPOSITORY_GUIDE.md), [pipeline operations](pipeline/SYSTEM_MANAGEMENT.md), and [pipeline CLI](pipeline/prospectus_pipeline/README.md).

[MIT License](LICENSE)
