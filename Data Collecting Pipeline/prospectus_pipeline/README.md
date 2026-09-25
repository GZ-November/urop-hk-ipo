# HK IPO Prospectus & Allotment Pipeline (v2.0)

Automated and semi-automated extraction, deterministic validation, semantic verification, and cryptographic hash-gated write-back toolkit for Hong Kong Main Board IPO filings. The active workbook schema and dataset determine the current field and sample counts.

---

## Core Architecture & Principles

1. **Deterministic-First, AI-Assisted**:
   - Document downloading, text extraction, section slicing, deterministic derivation (pricing date, green shoe results, cornerstone confirmation, free-float equations), type validation, accounting identities, and Excel write-back are all executed via deterministic Python code (0 LLM Token cost).
   - Complex unstructured semantic comprehension and multi-period financial tables are handled by AI agents (e.g. Gemini / LLMs).
2. **Fail-Closed Verification with Hash-Gating**:
   - Four-stage lifecycle gates: `extracted` → `validated` → `reviewed` → `written`.
   - Each stage binds to the SHA-256 hash of the exact JSON payload. Any discrepancy, quotation error, or identity mismatch immediately halts write-back.
3. **Strict Formatting Fidelity & Snapshots**:
   - Write-back populates only target cell values, preserving original workbook fonts, fills, alignments, borders, and number formats.
   - Automatic timestamped backups are generated prior to any workbook modification.

---

## Repository Structure

```text
prospectus_pipeline/
├── run.py                          # Unified CLI entry point (status/audit/cross_check/report/export/search/state)
├── config.yaml                     # Pipeline configuration
├── pyproject.toml / requirements.txt # Python project specification and dependencies
├── README.md                       # Pipeline documentation
│
├── src/                            # Core pipeline package
│   ├── audit.py                    # Read-only cell-by-cell Excel vs. JSON auditing engine
│   ├── cross_check.py              # Cross-field business logic and HKEX Listing Rules auditor
│   ├── report.py                   # Academic market report generator
│   ├── codebook.py                 # Econometric variable codebook and clean CSV exporter
│   ├── cohort.py                   # Runtime workbook, period, paths, and issuer cohort resolution
│   ├── auto_fill.py                # Pipeline scheduler and status monitor
│   ├── contracts.py                # Strict JSON contract and quote verification
│   ├── state.py                    # Four-phase hash-signed state management
│   ├── storage.py                  # Atomic JSON I/O and prospectus retrieval
│   ├── validate.py                 # Deterministic structural and identity validation engine
│   ├── write_back.py               # Safe Excel write-back with automatic snapshots
│   ├── write_back_expansion.py     # Transactional write-back engine for academic expansion (Cols 162–202)
│   ├── expansion_mapping.py        # Expansion field catalog and research-source value mapping
│   ├── sample_builder.py           # Multi-year IPO master sample builder & statutory screening (2021–2026)
│   ├── market_panel.py             # Daily OHLCV microstructure panel & multi-horizon return calculator
│   ├── market_observations.py      # Shared daily market CSV reader and date-sorted observations
│   ├── stabilization_panel.py      # Price stabilization & green shoe event calculator
│   ├── lockup_panel.py             # Multi-horizon statutory lockup & unlock event calculator
│   ├── relational_tables.py        # Relational investor & underwriting syndicate graph tables
│   ├── pricing_date.py             # Pricing date deterministic derivation
│   ├── pdfprep.py                  # Prospectus PDF download, text extraction, and section slicing
│   ├── allotprep.py                # Allotment results download, slicing, and evidence packaging
│   ├── greenshoe.py                # Over-allotment option (Green Shoe) announcement crawler
│   ├── cornerstone.py              # Cornerstone investor deterministic audit
│   └── hkex.py                     # HKEX News announcement search client
│
├── tools/                          # Domain utilities and scripts
│   ├── search.py                   # Interactive document search (outline/pages/periods/bundle)
│   ├── state.py                    # Hash state authentication CLI
│   ├── validate_ext.py             # External field validation utility
│   └── external/                   # External market and macroeconomic collectors
│       ├── market.py               # First-day trading performance and 20-day HSI returns
│       ├── hkma_import.py          # Fast HIBOR and aggregate balance collector
│       ├── hkma.py                 # HKMA online API scraper
│       ├── ipo_count.py            # 90-day ordinary IPO count
│       ├── flags.py                # HKEX Chapter flags (18A, 18C, WVR, secondary listings)
│       ├── rules.py                # Offering mechanisms and FINI clawback rules
│       └── hsic_codes.py           # Hang Seng Industry Classification (HSIC) codes
│
├── schema/                         # Contract schemas
│   ├── fields.json                 # Prospectus extraction field specifications
│   ├── allot_fields.json           # 18 allotment field specifications
│   └── relational_schemas.json     # Strict JSON Schema for 8 master relational & event tables
│
├── tests/                          # Portable unit, integration, and production acceptance tests
│   ├── test_audit_excel.py         # Read-only Excel audit, null-equivalence, and float tolerance
│   ├── test_cross_check.py         # Cross-field rules, Chapter 18C valuation, and clawbacks
│   ├── test_report.py              # Report aggregation and markdown generation
│   ├── test_codebook.py            # Variable dictionary and CSV exporter tests
│   ├── test_pipeline_safety.py     # Hash-gating, quotation forgery, and range safety tests
│   ├── test_master_expansion.py    # Master sample screening, microstructure panel & maturity tests
│   ├── test_market_observations.py # Shared event-panel market observation loading
│   ├── test_expansion_mapping.py   # Expansion field catalog and value mapping
│   ├── test_expansion_writer.py    # Cohort-scoped workbook expansion write-back
│   └── test_pipeline_robustness.py # Dynamic column resolution, 100% audit mapping, codebook metadata
│
└── workflows/                      # Extraction and review workflow definitions
    ├── prospectus_extract.js       # Prospectus 70-field extraction workflow
    └── allot_extract.js            # Allotment results extraction workflow
```

---

## Command Reference (CLI Usage)

Execute commands from `Data Collecting Pipeline`:

```bash
cd "Data Collecting Pipeline"
```

### Choose the cohort from a prompt

The default workbook and period in `config.yaml` remain the defaults. To collect or review a different period, pass the requested dates directly to the CLI; dates are inclusive and selection uses listing date (prospectus date when listing date is blank). A supplied workbook is read as-is, so it must contain the issuer rows for that period.

```bash
python3 prospectus_pipeline/run.py all \
  --workbook "HKIPO-MB2026H1.xlsx" \
  --period-start 2026-01-01 \
  --period-end 2026-06-30
```

You can express the same request in a prompt, for example: “收集 2026-01-01 到 2026-06-30 上市的港股主板 IPO，使用 `HKIPO-MB2026H1.xlsx`。” The caller translates the requested period and workbook into CLI arguments; the pipeline does not parse free-form prompt text. If only one date endpoint is supplied, the missing endpoint is inferred from the earliest or latest issuer membership date in the selected workbook. Omitting both date options uses the configured default period. Each non-default workbook or period gets its own `datasets/<dataset-id>/` data, output, and hash-state directories.

Issuer fields are read through the `id_columns` mapping in `config.yaml`, including the market panel's offer-price field. Workbooks with a different column layout need an explicit mapping for those fields.

### Collect an issuer cohort from dates alone

`collect` finds ordinary Main Board IPOs in the inclusive listing-date interval (prospectus date is used only if the listing date is absent). It obtains missing annual HKEX New Listing Reports, checks that every requested year is covered, creates a workbook from `templates/HKIPO-MB-template-final.xlsx`, and prepares prospectus and allotment extraction packets. The workbook, artifacts, hash state, and generated `cohort.yaml` live together under `prospectus_pipeline/datasets/HKIPO_<start>_<end>_HKIPO-MB/`.

```bash
python3 run.py collect --period-start 2026-04-01 --period-end 2026-06-30
```

The first invocation exits with code `3` when AI extraction or independent review is pending. Pass the printed `cohort.yaml` as `config_path` to `workflows/prospectus_extract.js` and `workflows/allot_extract.js`. Those workflows create extracted JSON and hash-bound review records. Rerun the **same** `collect` command afterward; it validates, writes the reviewed fields, collects external indicators, and audits the workbook. Existing workbook values are preserved on resume.

If an annual report is unavailable or the current-year report ends before the requested date, `collect` stops and names the missing year. Reports before 2020 use `.xls`; the pipeline requires `xlrd>=2.0.1` for them. Dates after today are rejected. `--source-dir` selects a local annual-report cache if needed.

The 90-day IPO count may require reports from the year before the selected cohort. `collect` checks those reports before writing reviewed fields; the generated config remembers `--source-dir` for later runs. A cohort whose count window reaches a year with no official Main Board report stops with that year in the error message.

This command preserves the existing independent review requirement: it never approves extracted evidence by itself. A missing prospectus or allotment document also stops the run rather than silently producing an incomplete workbook.

### 1. Status, Audit, Cross-Check, and Export
```bash
# Check pipeline lifecycle and hash alignment status
python3 prospectus_pipeline/run.py status

# Run cell-by-cell read-only audit against Excel workbook
python3 prospectus_pipeline/run.py audit --target all

# Run HKEX Listing Rules cross-check (Chapter 18C, FINI clawback, green shoe, cornerstone lockup)
python3 prospectus_pipeline/run.py cross_check

# Generate comprehensive macro market report (Markdown)
python3 prospectus_pipeline/run.py report

# Export clean econometric CSV and variable codebook
python3 prospectus_pipeline/run.py export
```

### 2. Core Extraction Stages

```bash
# Prospectus preparation
python3 prospectus_pipeline/run.py find [--only <CODE>.HK]
python3 prospectus_pipeline/run.py download [--only <CODE>.HK]
python3 prospectus_pipeline/run.py prepare [--only <CODE>.HK]

# Allotment preparation & deterministic derivations
python3 prospectus_pipeline/run.py allot [--only <CODE>.HK]
python3 prospectus_pipeline/run.py derive_allot [--only <CODE>.HK]

# Validation (gatekeeper)
python3 prospectus_pipeline/run.py validate --target prospectus [--only <CODE>.HK]
python3 prospectus_pipeline/run.py validate --target allot [--only <CODE>.HK]

# Safe Excel write-back (requires passed hash gates)
python3 prospectus_pipeline/run.py write --target prospectus --fill-missing [--only <CODE>.HK]
python3 prospectus_pipeline/run.py write --target allot --fill-missing [--only <CODE>.HK]
```

### 3. State Management (`run.py state`)

```bash
# Record extraction completion
python3 prospectus_pipeline/run.py state extracted --target prospectus --all

# Record review sign-off
python3 prospectus_pipeline/run.py state reviewed --target prospectus --all --verdict pass
```

### 4. Interactive Document Search (`run.py search`)

```bash
python3 prospectus_pipeline/run.py search info <CODE>.HK
python3 prospectus_pipeline/run.py search outline <CODE>.HK
python3 prospectus_pipeline/run.py search pages <CODE>.HK 10-15
python3 prospectus_pipeline/run.py search sharecap <CODE>.HK
```

### 5. External Indicators (`run.py external`)

```bash
# Collect market returns, HIBOR, HKMA liquidity, IPO count, and Chapter flags
python3 prospectus_pipeline/run.py external [--only <CODE>.HK]
```

### 6. Automated Testing

```bash
python3 -m unittest discover -s prospectus_pipeline/tests -v
```
