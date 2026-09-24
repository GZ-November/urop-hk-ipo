# HK IPO Prospectus & Allotment Pipeline (v2.0)

Automated and semi-automated extraction, deterministic validation, semantic verification, and cryptographic hash-gated write-back toolkit for Hong Kong Main Board IPO filings (70 prospectus fields, 18 allotment fields, and 114 external market/macro/academic expansion fields, totaling 202 variables; plus multi-year master sample panel architecture).

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
│   ├── auto_fill.py                # Pipeline scheduler and status monitor
│   ├── contracts.py                # Strict JSON contract and quote verification
│   ├── state.py                    # Four-phase hash-signed state management
│   ├── storage.py                  # Atomic JSON I/O and prospectus retrieval
│   ├── validate.py                 # Deterministic structural and identity validation engine
│   ├── write_back.py               # Safe Excel write-back with automatic snapshots
│   ├── write_back_expansion.py     # Transactional write-back engine for academic expansion (Cols 162–202)
│   ├── sample_builder.py           # Multi-year IPO master sample builder & statutory screening (2021–2026)
│   ├── market_panel.py             # Daily OHLCV microstructure panel & multi-horizon return calculator
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
│   ├── fields.json                 # 70 prospectus field specifications
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
│   └── test_pipeline_robustness.py # Dynamic column resolution, 100% audit mapping, codebook metadata
│
└── workflows/                      # Extraction and review workflow definitions
    ├── prospectus_extract.js       # Cohort-configured prospectus extraction workflow
    └── allot_extract.js            # Allotment results extraction workflow
```

---

## Command Reference (CLI Usage)

Execute commands from `Data Collecting Pipeline`:

```bash
cd "Data Collecting Pipeline"
```

### Collecting another quarter

`config.yaml` is the Q1 reference configuration; the extraction code does not encode a quarter. Copy the configuration for each cohort, then set its workbook, cohort metadata, date window, expected sample size, and cohort-specific `paths`/`state_dir`. Keep the workbook headers compatible with the shared schema. Select that config with `--config` or `PIPELINE_CONFIG` for **every** stage so prepare, search, validation, state, write-back, export, and VC/PE reporting use the same cohort.

```bash
cp prospectus_pipeline/config.yaml prospectus_pipeline/config-2026Q2.yaml
# Edit config-2026Q2.yaml with the new workbook, dataset fields, and isolated paths.
python3 prospectus_pipeline/run.py prepare --config prospectus_pipeline/config-2026Q2.yaml
python3 prospectus_pipeline/run.py validate --config prospectus_pipeline/config-2026Q2.yaml
python3 prospectus_pipeline/run.py write --config prospectus_pipeline/config-2026Q2.yaml
```

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
