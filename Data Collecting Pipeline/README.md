# Data Collecting Pipeline Subsystem

This directory contains the end-to-end automated data collection pipeline, canonical research dataset workbooks, extraction templates, regulatory sources, disaster recovery snapshots, and verification engines for Hong Kong Stock Exchange (HKEX) Main Board IPO disclosures.

For comprehensive systems architecture, state ledger models, data governance, and collaborator standard operating procedures, refer to the [Systems Engineering & Management Manual](SYSTEM_MANAGEMENT.md).

---

## Directory Architecture

```text
Data Collecting Pipeline/
├── README.md                      # This document (Subsystem Overview)
├── SYSTEM_MANAGEMENT.md           # Senior Systems Engineering & Governance Manual
├── HKIPO-MB2026Q1.xlsx            # Active Canonical Research Workbook (Single Source of Truth)
│
├── templates/                     # Blank Research Collection Templates
│   ├── HKIPO-GEM-template-students.xlsx   # GEM Board Template (Historical / Students)
│   └── HKIPO-MB-template-students.xlsx   # Main Board 120-Variable Canonical Template
│
├── sources/                       # Immutable Official HKEX Sources
│   ├── NLR2025_Eng.xlsx           # HKEX New Listing Report 2025
│   └── NLR2026_Eng.xlsx           # HKEX New Listing Report 2026
│
├── docs/                          # Specifications, Domain Rules & Manuals
│   ├── specs/                     # Field schemas, construction manuals, rule tables
│   ├── guides/                    # Field collection and audit guides
│   └── reports/                   # Feasibility, cost and token reports
│
├── reports/                       # Academic Progress Reports & Compilers
│   ├── build_weekly_report.py     # Faculty Progress Report compiler (.docx)
│   └── Weekly_Research_Progress_Report_HKIPO_2026Q1.docx
│
├── backups/                       # Automated Recovery & Safety Snapshots
│   ├── excel_snapshots/           # Timestamped pre-write Excel snapshots
│   └── code_archives/             # Historical milestone archives
│
└── prospectus_pipeline/           # Core Automation Engine Subsystem
    ├── run.py                     # Pipeline Subsystem CLI Entry Point
    ├── config.yaml                # Engine Configuration
    ├── pyproject.toml             # Engine Package Metadata
    ├── requirements.txt           # Engine Dependencies
    ├── README.md                  # Engine Technical Manual
    ├── src/                       # Extraction, validation, audit & write-back modules
    ├── tools/                     # Utility scripts (search, state, external indicators)
    ├── schema/                    # Contract schemas (fields.json, allot_fields.json, relational_schemas.json)
    ├── prompts/                   # LLM Extraction schemas & few-shot instructions
    ├── workflows/                 # Headless workflow definitions
    ├── tests/                     # Automated regression and safety tests
    ├── data/                      # PDF store, page text, and evidence packets (gitignored)
    └── out/                       # Verifiable state ledger, clean CSV, and Codebook
```

---

## Command Reference (CLI Usage)

All operations can be dispatched either from the **repository root** (recommended):
```bash
python3 run.py <COMMAND> [OPTIONS]
# or via Makefile
make <TARGET>
```

Or from within `Data Collecting Pipeline`:
```bash
# 1. Inspect pipeline and state alignment status
python3 prospectus_pipeline/run.py status

# 2. Run read-only cell-by-cell audit against the target workbook
python3 prospectus_pipeline/run.py audit --target all

# 3. Perform HKEX Listing Rules cross-checks (Chapter 18C, FINI, Green Shoe, Lockup)
python3 prospectus_pipeline/run.py cross_check

# 4. Generate academic market report
python3 prospectus_pipeline/run.py report

# 5. Export clean econometric CSV and variable codebook
python3 prospectus_pipeline/run.py export

# 6. Run external indicator collection (market returns, HIBOR, HKMA liquidity, flags)
python3 prospectus_pipeline/run.py external

# 7. Run automated test suite
python3 -m unittest discover -s prospectus_pipeline/tests -v

# 8. Compile official Faculty Progress Word Report
python3 reports/build_weekly_report.py
```

---

## Data Governance & Safety Guarantees

1. **Deterministic-First (0 Token Cost)**: PDF parsing, section slicing, mathematical identities, Listing Rules cross-checks, and Excel write-back require zero LLM calls.
2. **Cryptographic Hash-Gating**: Every cell write is gated by SHA-256 state signatures (`extracted` → `validated` → `reviewed` → `written`).
3. **Format-Preserving Excel Engine**: Target values are written cell-by-cell without disturbing existing styles, fonts, borders, or workbook macros.
4. **Automated Safety Backups**: Every write-back automatically snapshots the current target workbook into `backups/excel_snapshots/` prior to disk modification.
