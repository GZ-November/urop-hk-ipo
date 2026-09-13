# HK IPO Pipeline Workspace (`News`)

This workspace contains the core automation pipeline, schema definitions, and verification tools for Hong Kong Main Board IPO disclosure extraction.

---

## Directory Overview

```text
News/
├── README.md                    # This document
│
└── prospectus_pipeline/         # Automated extraction, validation, and audit pipeline
    ├── run.py                   # Unified CLI entry point
    ├── config.yaml              # Pipeline configuration
    ├── pyproject.toml           # Project metadata
    ├── requirements.txt         # Core dependencies
    ├── README.md                # Pipeline technical documentation
    ├── src/                     # Pipeline package (audit, cross-check, report, codebook, etc.)
    ├── tools/                   # Utility scripts (search, state, external tools)
    ├── schema/                  # Contract definitions (prospectus and allotment fields)
    ├── tests/                   # Automated test suite (17/17 passed)
    └── workflows/               # Extraction workflow definitions
```

---

## Common CLI Operations

All pipeline commands are dispatched via `prospectus_pipeline/run.py`. From this directory:

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

# 8. Interactive document search
python3 prospectus_pipeline/run.py search info <STOCK_CODE>.HK
```
