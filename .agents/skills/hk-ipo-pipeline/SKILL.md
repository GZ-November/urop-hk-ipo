---
name: hk-ipo-pipeline
description: >-
  Inspect, audit, validate, and execute the Hong Kong Main Board IPO dataset collection pipeline.
  Use when the user asks to check pipeline status, audit Excel cells against verified JSON extractions,
  cross-check HKEX Listing Rules (Chapter 18C, FINI Mechanism A/B clawbacks, green shoe 15%, cornerstone lockup),
  generate cohort-specific academic and macro market reports, export clean econometric CSVs or codebooks,
  or collect and process new IPO companies.
---

# Hong Kong Main Board IPO Pipeline Skill (v2.0)

Standard operating runbook and execution guide for the Hong Kong Main Board IPO automated data collection, deterministic validation, dual-gate auditing, and econometric delivery pipeline.

Current research scope: all statistical and econometric analysis, including Module A, uses observed 2026 listing dates only. Collection remains cohort-general. See `analysis/README.md` and `docs/RESEARCH_PLAN_2026.md`.

Core Architecture: **Deterministic First (0 LLM Token overhead) + SHA-256 Payload Version Gates (independent semantic review required) + Exact Excel Formatting Preservation**.

---

## 1. Environment Verification & Self-Healing (Prerequisites)

Before executing any pipeline tasks, agents can verify and self-heal the environment with:

```bash
# Checks Python 3.9+ and verifies 4 lightweight dependencies (openpyxl, pyyaml, requests, pymupdf)
./.agents/skills/hk-ipo-pipeline/scripts/check_env.sh
```

---

## 2. Universal CLI Wrapper

All pipeline operations are unified under `run.py`. Agents can invoke the wrapper from anywhere in the repository:

```bash
./.agents/skills/hk-ipo-pipeline/scripts/run_pipeline.sh <STAGE> [OPTIONS]
```

Or from within `pipeline`:

```bash
"${PYTHON_BIN:-.venv/bin/python}" prospectus_pipeline/run.py <STAGE> [OPTIONS]
```

Select another cohort with `PIPELINE_CONFIG=/path/to/cohort.yaml` or `--config /path/to/cohort.yaml`. Keep each cohort's workbook, paths, dataset metadata, and optional `state_dir` together in its config.

---

## 3. Standard Operating Procedures (SOP) & Command Matrix

### 1. Check System State (`status`)
Inspect pipeline stages and hash authorization across all issuers:
```bash
./.agents/skills/hk-ipo-pipeline/scripts/run_pipeline.sh status
```

### 2. Cell-by-Cell Audit (`audit`)
Performs a read-only comparison between the deliverable Excel cells and authorized JSON extractions:
```bash
./.agents/skills/hk-ipo-pipeline/scripts/run_pipeline.sh audit --target all
```
- Produces: `out/audit_report.md` and `out/audit_report.json`.

### 3. HKEX Listing Rules Cross-Check (`cross_check`)
Validates econometric consistency against official HKEX Listing Rules:
- Chapter 18C expected market cap threshold (adjusted to 2024 reform HK$ 4.0B);
- FINI Allocation Mechanism A (statutory clawback schedule) vs Mechanism B (custom ceiling);
- Green Shoe allotment ceiling (<= 15.00% of base offer);
- Cornerstone 6-month statutory lockup compliance;
- First-day trading OHLC price boundaries.
```bash
./.agents/skills/hk-ipo-pipeline/scripts/run_pipeline.sh cross_check
```
- Reference details: [listing_rules_guide.md](./references/listing_rules_guide.md) and [statutory_evidentiary_rules.md](./references/statutory_evidentiary_rules.md).

### 4. Macro Market & Academic Report (`report`)
Aggregates all 202 variables into macro proceeds, industry breakdown (HSICS 2026), retail subscription multiples, and first-day returns:
```bash
./.agents/skills/hk-ipo-pipeline/scripts/run_pipeline.sh report
```

### 5. Econometric CSV & Codebook Exporter (`export`)
Exports clean data and comprehensive data dictionary for econometric research:
```bash
./.agents/skills/hk-ipo-pipeline/scripts/run_pipeline.sh export
```
- Produces:
  - Clean CSV formatted in UTF-8 with BOM;
  - Comprehensive Markdown Data Codebook with summary statistics;
  - Structured machine-readable Codebook JSON.
- Econometric modeling and empirical workflows: [empirical_analysis_guide.md](./references/empirical_analysis_guide.md).

### 5b. Variable Registry Builder (`registry`)
Merges all quarterly Markdown Codebooks into one machine-readable variable registry
(`HKIPO_Variable_Registry.yaml`, versioned) — a derived snapshot of variable_catalog.py for column
name / type / layer / unit. Cross-cohort definition conflicts are recorded under
`meta.conflicts` and resolved to the newest Codebook:
```bash
./.agents/skills/hk-ipo-pipeline/scripts/run_pipeline.sh registry
```

### 5c. Master Panel & Drift Report (`master`)
Merges every cohort `_clean.csv` into one analysis-ready master panel
(`HKIPO-MB-MASTER_clean.csv`, versioned research artifact) prefixed with `cohort` and
`cross_cohort_duplicate` columns, and writes `HKIPO-MB-MASTER_Drift_Report.md`:
```bash
./.agents/skills/hk-ipo-pipeline/scripts/run_pipeline.sh master
```
- Checks: header alignment across cohorts (order-sensitive), headers vs registry,
  duplicate stock codes within/across cohorts, listing date vs cohort quarter,
  per-variable fill rates per cohort, and share-count identities
  (`L = N + Q`, `L = O + M`, `M = Q + P`, tolerance ±1 share).
- Exits non-zero on hard errors (header drift, registry mismatch, duplicate codes);
  listing-date, identity and fill-rate findings are reported as warnings.
- Add `--derive` to append currency-free derived ratio columns to the master panel
  (`leverage_y1`, `roa_y1`, `sales_growth_y1`, `log_proceeds_hkd`,
  `public_offer_fraction`; sources missing -> column skipped, invalid -> NaN).
  `log_proceeds_hkd` = ln(`IPO Subscription Price (HK$)` x `Final global offering
  shares (before over-allotment)`), i.e. log base-deal proceeds in HK$ (excludes the
  over-allotment option). It is not a share-count log. Derived-column definitions
  live in `DERIVED_SPECS` (`master_panel.py`) and are mirrored in the registry's
  `derived_variables` section (`run.py registry --check` fails on drift).
- Section 5.1 reports fill-rate changes vs the previous cohort (>=10pp) so
  extraction-quality regressions surface immediately.
- Regenerate after each cohort closes so an analysis-ready master always exists.

### 5d. Analysis Entry Point (`panel.py`)
Load the master panel as a registry-driven pandas DataFrame (identity columns
`cohort` / `cross_cohort_duplicate` / `stock_code` always kept):
```python
import sys
sys.path.insert(0, "pipeline/prospectus_pipeline/src")
from panel import available_slugs, load_master
df = load_master(slugs=["ipo_subscription_price_hk", "filing_price_revision_pct"])
```
Column names become registry slugs; `date` -> datetime64, `numeric`/`boolean` ->
numeric. FX conversion and unit normalization are intentionally out of scope.

### 5e. Collection-Time Membership Guards (`collect`)
`build_cohort_workbook` now enforces the listing-date cohort rule on every run:
- refuses issuers whose stock code already exists in a sibling cohort workbook
  (cross-cohort duplicates);
- refuses an existing cohort workbook containing known listing dates outside the
  cohort period (issuers collected before their listing date was known must be
  reassigned once the date lands in a later quarter).
Both raise `ValueError` for manual reconciliation instead of writing.

### 5f. Evidence Manifest & Sample Selection Logs
- `evidence` (`make evidence`): freezes a SHA-256 manifest (`HKIPO-Evidence_SHA256.txt`,
  versioned) of every research artifact — cohort workbooks, clean CSVs, codebooks,
  registry, master panel, drift report, selection logs. Run when a cohort closes and
  commit the snapshot; any later modification shows up as a hash mismatch, keeping
  every cell traceable to the prospectus it was extracted from.
- `exclusions` (`make exclusions`): per-cohort sample selection log
  (`HKIPO_{tag}_Exclusions.md`, versioned) listing included issuers, excluded ones
  with statutory reasons (GEM transfer / SPAC / listing by introduction), and
  workbook-consistency warnings (included-but-missing issuers).
- `make aftermarket-refresh`: refreshes aftermarket columns (1M/6M BHR, liquidity
  decay) for every cohort config pointing at canonical workbooks. Rerun monthly as
  listing-age windows mature (6M data needs 6 calendar months after listing).
- Codebook dtype for Reserved/Unmatured (empty) columns comes from the registry's
  `declared_dtype` (the cohort where the column held data), not from inference —
  this keeps codebooks conflict-free across quarters. The drift report's section
  5.2 flags boolean columns left empty (convention: 0/1, never blank).

### 6. Automated Regression & Safety Test Suite (`test`)
```bash
cd "pipeline" && python3 -m unittest discover -s prospectus_pipeline/tests -v
```

---

## 4. Ingestion Runbook for New IPO Companies

To process new IPO companies (e.g. `6082.HK` or future quarters):

```
[1. find announcement] ──> [2. download PDF] ──> [3. prepare text & slice packets]
                                                                  │
┌─────────────────────────────────────────────────────────────────┘
▼
[4. AI agent extracts packet] (or run workflows/prospectus_extract.js)
│
▼
[5. run.py validate] ──> Schema & quotation proof verified ──> Issued SHA256 signature
│
▼
[6. run.py write] ────> Automated timestamped snapshot ──> Cells written (styling preserved)
│
▼
[7. run.py external] ─> Enriches market OHLC, HIBOR, balance, HSICS industry codes
│
▼
[8. run.py check] ────> audit + cross_check + test closed-loop verification
```

---

## 5. Troubleshooting & Self-Healing

1. **`VALIDATION_ERROR` (Mismatched quote or missing evidence)**:
   - Use search tool to inspect original prospectus pages:
     ```bash
     ./.agents/skills/hk-ipo-pipeline/scripts/run_pipeline.sh search pages <CODE>.HK <START>-<END>
     ```
   - Correct JSON and re-run `run.py validate`.
2. **`HASH_MISMATCH` (Stale or unauthorized extraction)**:
   - Always run `validate` before attempting to write back to Excel.
3. **Restoring Snapshots**:
   - Revert to timestamped snapshots in `backups/excel_snapshots/` at any time.
