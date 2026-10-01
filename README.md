# Hong Kong IPO Research

[![CI](https://github.com/GZ-November/urop-hk-ipo/actions/workflows/ci.yml/badge.svg)](https://github.com/GZ-November/urop-hk-ipo/actions) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A reproducible research project for Hong Kong Main Board IPOs, connecting official disclosures, evidence-linked datasets and empirical analysis of offering costs, investor allocation, pricing and aftermarket outcomes.

The current research snapshot contains **113 IPOs listed from 2 January through 30 September 2026**: 38 in Q1, 45 in Q2 and 30 in Q3. The disclosure registry contains **202 source variables**. Historical cohorts remain in the data layer; the maintained research modules select 2026 listings explicitly and report their own valid sample sizes.

## Read the Research

| Report | What it covers |
|---|---|
| [Offering and company facts](analysis/out/offer_facts/facts.md) | 60 descriptive indicators, offering concentration, financial profiles, backing, demand, ownership and fees; excludes trading performance |
| [Offering economics](analysis/out/offering_economics/analysis.md) | Listing-expense elasticity, disclosed commission rates, cornerstone shares, retail participation, demand decomposition and VC/PE overlap |
| [IPO literature and methods](docs/IPO_LITERATURE_METHODS_2026.md) | Eight IPO publications, inspected source access, transferable methods and data limitations |
| [Underpricing regressions](analysis/out/module_b/table4_regressions.md) | Nested first-day-return regressions; [month-cluster inference](analysis/out/module_b/table6_inference.md) |
| [Aftermarket analysis](analysis/out/event_time/event_time.md) | Event-time BHAR and calendar-time portfolios with horizon-specific coverage |

The new offering reports are in English. They distinguish issuer-level associations from causal effects, retain missing observations, document denominators and use small-cluster inference where applicable. Existing field coverage is not a claim that every original disclosure has been independently re-audited.

## Install and Verify

Python 3.9+; run from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[analysis,dev]'
make check-code
python run.py --help
```

This is a source-checkout CLI. Editable installation supplies dependencies and project metadata; keep the repository's schemas, configurations and research artifacts alongside its code.

`make check-code` runs static checks, pipeline tests, analysis tests and registry consistency. CI and the pre-push hook use the same entry point. Some original-PDF tests require local materials absent from the checkout and report explicit skips.

## Reproduce the Current Reports

Use the committed master export for the existing snapshot:

```bash
# Offering/company facts only
make offer-facts

# Advanced offering models, inference and robustness
make offering-economics

# All maintained 2026 analyses, including pricing and aftermarket studies
make analysis
```

Outputs live in `analysis/out/<module>/`: English reports, tables, figures, estimation-sample logs, diagnostics and manifests. Offering-economics models use 110–112 valid issuers, depending on missing inputs; 113 is the overall sample, not every model's denominator. See the [analysis index](analysis/README.md) for individual scripts and definitions.

Each offering report records its input hash and cutoff. Regenerating output does not refresh original disclosures, workbooks or market observations. The fixed-snapshot modules intentionally check that the requested 113-issuer September sample is still present.

## Collect and Update Data

```bash
# Inspect an existing cohort; configuration paths are relative to pipeline/
python run.py status --config prospectus_pipeline/config_2026q3.yaml
python run.py audit --target all --config prospectus_pipeline/config_2026q3.yaml

# Prepare a new listing-date cohort
python run.py collect --period-start 2026-04-01 --period-end 2026-06-30

# Merge existing cohort exports into the research master
python run.py master --derive
```

The pipeline collects prospectuses and allotment disclosures, prepares extraction packets, validates deterministic contracts, records independent review and writes workbooks transactionally. `collect` returns exit code 3 while extraction or review is pending; resume it after the required evidence gates are complete.

After changing a cohort workbook, export that cohort with `python run.py export --config ...` before rebuilding the master. Missing evidence and immature event windows remain missing. `make refresh-2026` additionally fetches market data and rewrites workbooks, exports and reports; use it when a deliberate source refresh is needed, rather than for ordinary report reproduction.

## Repository Map

| Location | Purpose |
|---|---|
| `pipeline/cohorts/` | Canonical quarterly workbooks |
| `pipeline/exports/` | Clean cohort exports, master and reference panels |
| `pipeline/codebooks/`, `pipeline/registry/` | Definitions, units, missing-value contracts and provenance |
| `pipeline/prospectus_pipeline/` | Collection, extraction, validation, review and export code |
| `pipeline/reports/` | Evidence reviews, reconciliation, exclusions and source-quality reports |
| `analysis/`, `analysis/tests/` | Research modules, shared inputs and regression tests |
| `analysis/out/` | Versioned, reproducible research results |
| `docs/`, `docs/archive/` | Current methods, research navigation and superseded write-ups |

Start with the [research guide](docs/RESEARCH_START.md), [documentation index](docs/README.md) and [repository conventions](docs/REPOSITORY_GUIDE.md). The [offering-economics design](docs/OFFERING_ECONOMICS_DESIGN_2026.md) records the new specifications and inference choices.

Public-disclosure workbooks, clean exports, extraction evidence and research reports are intentionally versioned. Original prospectus PDFs, full-text extraction packets, temporary collection workspaces, workbook backups and runtime caches stay local under [.gitignore](.gitignore). Preserve evidence and historical artifacts when cleaning the repository.

[Pipeline guide](pipeline/prospectus_pipeline/README.md) · [Domain definitions](CONTEXT.md) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [MIT License](LICENSE)
