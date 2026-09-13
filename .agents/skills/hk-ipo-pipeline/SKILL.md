---
name: hk-ipo-pipeline
description: >-
  Inspect, audit, validate, and execute the Hong Kong Main Board IPO dataset collection pipeline.
  Use when the user asks to check pipeline status, audit Excel cells against verified JSON extractions,
  cross-check HKEX Listing Rules (Chapter 18C, FINI Mechanism A/B clawbacks, green shoe 15%, cornerstone lockup),
  generate academic and macro Q1 market reports, export clean econometric CSVs or 120-variable codebooks,
  or collect and process new IPO companies.
---

# Hong Kong Main Board IPO Pipeline Skill (v2.0)

Standard operating runbook and execution guide for the Hong Kong Main Board IPO automated data collection, deterministic validation, dual-gate auditing, and econometric delivery pipeline.

Core Architecture: **Deterministic First (0 LLM Token overhead) + Cryptographic Hash-Gates (Hallucination-proof) + Exact Excel Formatting Preservation**.

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

Or from within `Data Collecting Templates/News`:

```bash
python3 prospectus_pipeline/run.py <STAGE> [OPTIONS]
```

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
- Reference details: [listing_rules_guide.md](./references/listing_rules_guide.md).

### 4. Macro Market & Academic Report (`report`)
Aggregates all 120 variables into macro proceeds, industry breakdown (HSICS 2026), retail subscription multiples, and first-day returns:
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

### 6. Automated Regression & Safety Test Suite (`test`)
```bash
cd "Data Collecting Templates/News" && python3 -m unittest discover -s prospectus_pipeline/tests -v
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
