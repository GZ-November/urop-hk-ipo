# Hong Kong IPO pipeline: complete user and agent instructions

This repository provides source discovery, document download, structured evidence,
validation, review gates, Excel writeback, CSV export and data delivery for ordinary
Hong Kong Main Board and GEM IPOs. Give an agent the repository URL and the prompt
below. The agent must have terminal/file access, Internet access, and the ability
to read documents and use an independent reviewer. A chat agent with only browser
access cannot execute the pipeline. A repository link alone does not supply a
model runtime, independent reviewer or network permissions.

## 1. Copy this prompt to your agent

Replace the dates, boards and observation cutoff with your research scope.
The cutoff governs the requested research dataset; see the horizon limitation
below before claiming that every market series respects it.

```text
Use https://github.com/GZ-November/urop-hk-ipo to collect ordinary Hong Kong IPOs.

Boards: Main Board and GEM.
Inclusive listing-date interval: 2026-01-01 through 2026-03-31.
Requested market observation cutoff: 2026-09-30.
Delivery: separate board/cohort Excel and CSV files, dictionaries, evidence,
review/gate status, missing-data and maturity reports, plus a downloadable ZIP.

Clone the repository into a clean working directory. Read AGENTS.md,
docs/AGENT_INSTRUCTIONS.md, docs/GEM_PIPELINE.md and the collection skill.
Run python3 tools/bootstrap.py --profile dev, diagnose any installation failure,
and run make check-code. Use the repository's locked dependencies.

Collect each board sequentially. Treat exit code 3 as work awaiting extraction
or independent review. Read the generated handoff work orders and perform the
extraction against the actual issuer's disclosures. Use a separate independent
reviewer with source access, record the reviewer's identity and review report,
and resume the same collection command. You are authorized to delegate the
independent review to a separate agent if your runtime supports this.

Do not create passing review records merely to unlock writeback. Keep unsupported
values missing. In GEM use its own template/schema; do not reintroduce Main
Board-only fields or apply Main Board admission rules. Respect the documented
units, financial periods, initial/final offering definitions and maturity rules.

After collection, export each selected cohort, inspect audit and cross-check
reports, and build a ZIP with run.py bundle. Separate complete, partially covered
and review-pending data. Give me the ZIP path/link, cohort workbook/CSV paths,
issuer counts, actual listing dates, field coverage, unresolved evidence/review,
and all network or source limitations. Do not claim that tests alone prove data
correctness. Analyze GEM separately; existing built-in studies select Main Board
2026 listings. Do not stop at a plan if tools allow the work to continue.
```

For a request containing only the repository URL, the repository's agent entry
point uses the latest completed Hong Kong calendar quarter for both boards and
reports that assumption. Explicit dates in your prompt take precedence. A recent
quarter can fail official coverage checks; the agent must report that failure
instead of treating absent data as an empty IPO sample.

For an existing-data request, replace the collection paragraph with:

```text
Use the stored cohorts without refreshing source or market data. Inventory every
canonical cohort config, audit each separately, report coverage, and bundle all
stored cohorts. Include legacy/unreviewed gaps in the delivery summary.
```

## 2. Installation and dependencies

Start with Git, an existing Python 3.9+ with `venv`/`pip`, write access to the
checkout, and Internet access. `make` is required for the developer check command.
Windows users can use WSL for the full documented Bash/Make workflow; native
Python bootstrap and ZIP packaging are also available, but native Windows has
not been verified in this audit.

```bash
git clone https://github.com/GZ-November/urop-hk-ipo.git
cd urop-hk-ipo

# Option A: One-command automatic bootstrap and dual-board collection:
python3 run.py agent-start --board both

# Option B: Explicit developer bootstrap and validation:
python3 tools/bootstrap.py --profile dev
.venv/bin/python run.py doctor
make check-code
```

The bootstrap automatically creates a local `.bootstrap` installer environment,
installs the pinned `uv` tool, locates/downloads project Python 3.12 when needed,
and creates `.venv` using `uv sync --locked`. It checks imports and collection
assets afterward. It does not change global Python or require activating a shell.
Run it again to repair the selected profile. `--locked` refuses stale dependency
metadata; `--frozen` would have silently accepted the old incomplete lockfile.
See [uv's project guide](https://docs.astral.sh/uv/guides/projects/) and
[Python management](https://docs.astral.sh/uv/concepts/python-versions/).

| Profile | Automatically installed |
|---|---|
| `--profile core` | openpyxl, PyYAML, requests, PyMuPDF, xlrd and transitive dependencies |
| `--profile analysis` | Core plus pandas, NumPy, SciPy, statsmodels and matplotlib |
| `--profile dev` (default) | Analysis plus pytest, coverage and flake8 |

Git and an initial bootstrap Python remain host prerequisites; the bootstrap
cannot execute on a machine without any Python. On Debian/Ubuntu, an unavailable
`venv` module may require the distribution's `python3-venv` package. Use your
agent's normal tool permissions for installation/network access.

Optional diagnostics:

```bash
.venv/bin/python run.py doctor --network --output deliverables/environment.json
```

HTTP probes check availability at that moment, not complete downloads, source
correctness or provider reliability. Public collection does not require a GitHub
token, HKEX API key, commercial data subscription, Node.js or DSH. Your agent's
own model access is supplied by its host. The `.js` workflows are adapters for
DSH's `agent`, `pipeline`, `phase` and `log` APIs; installing Node does not supply
those APIs. Generic agents should use the generated portable work orders.
The optional offline dashboard in newer local checkouts has separate Node checks;
it is not required for data collection or CSV analysis.

A manual unpinned fallback is available if `uv` cannot run on your platform:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[analysis,dev]'
```

Record that this fallback does not reproduce the locked dependency versions.
Root `pyproject.toml` is the dependency authority; nested requirements are legacy
core-only descriptions, not another environment to install separately.

## 3. Select the board and cohort

Dates are inclusive and membership follows actual listing date. Main Board
screening excludes transfers from GEM, SPAC/de-SPAC cases and introductions.
GEM uses GEM reports and its own source adapter. GEM is not identified solely by
a stock-code range. A GEM listing that later transfers to Main Board remains a
GEM IPO observation in its original cohort; the transfer is not a second IPO.

Run these commands from the repository root:

```bash
.venv/bin/python run.py collect --board main \
  --period-start 2026-01-01 --period-end 2026-03-31

.venv/bin/python run.py collect --board gem \
  --period-start 2026-01-01 --period-end 2026-03-31
```

Each command obtains official listing reports, resolves issuers, creates a
styled blank cohort workbook, finds prospectuses and allotment/results notices,
downloads PDFs, extracts text and prepares packets. Generated workspaces are:

```text
pipeline/prospectus_pipeline/datasets/
  HKIPO_2026-01-01_2026-03-31_HKIPO-MB/
    HKIPO-MB.xlsx
    cohort.yaml
    ... resolved data/output/state paths ...
  HKIPO_2026-01-01_2026-03-31_HKIPO-GEM/
    HKIPO-GEM.xlsx
    cohort.yaml
    ... resolved data/output/state paths ...
```

Follow the resolved paths printed by the command/config; Main Board and GEM
base configs use different directory suffixes. Generated datasets, PDFs, packets
and hash-state records are intentionally ignored by Git. A plain clone does not
include the local raw-document caches; `collect` rebuilds them from disclosures.

The command prints a config and a `work_orders.json` path when extraction is
pending. Use that config for **every** following stage. Relative pipeline config
paths passed to `run.py` are resolved under `pipeline/`; `bundle --config` paths
are relative to the repository root, as shown below. Absolute paths work in both.

For long periods, collect one board and quarter at a time. Canonical historical
configs can share `out/`; run them sequentially and preserve each audit report
before the next overwrites it. Newly generated date/board workspaces are isolated.
Never run two writers on the same workbook concurrently.

Official report coverage is a gate. Main Board caches live in `pipeline/sources/`;
GEM caches live in `pipeline/sources/GEM/`. `--source-dir /absolute/cache` selects
a board-specific cache. Do not put reports from both boards in the same custom
cache. The collector verifies current-year printed coverage dates. Historical
GEM annual reports print their last IPO date even in sparse years, so the GEM
adapter treats the dated archived annual report as the completed historical year.
A missing annual report is not proof that the year had zero IPOs.

GEM reports use `e_newlistingsYYYY.xlsx`, nonadjacent columns and multi-row
headers, and omit the prospectus date. The adapter gets prospectus publication
date from HKEX's document index and records that source in `GEM_details`.
The GEM official gross funds raised is retained as a total: it is never silently
assigned to either the public-offer or placing tranche.

## 4. Extract and independently review

If the first collection exits with `3`, continue with the work orders. To rebuild
instructions for a selected cohort:

```bash
.venv/bin/python run.py handoff --config \
  prospectus_pipeline/datasets/HKIPO_2026-01-01_2026-03-31_HKIPO-GEM/cohort.yaml
```

### 4.1 Exit Code 3 Protocol: Autonomous Work-Order Resolution and Resume

> **Exit Code 3 (`WORK_PENDING`) is an intentional governance boundary, NOT a crash or failure.**

When a collection command exits with code `3`, the pipeline has completed official source discovery, created the cohort directory, downloaded disclosure PDFs, prepared text/Markdown extraction packets, and generated machine-readable work orders. It pauses deterministically because unverified data must never be silently written into research workbooks.

#### Step-by-Step Autonomous Action for Agents:

1. **Locate Work Orders**:
   Read `out/agent_handoff/work_orders.json` in the cohort directory (or inspect `START_HERE.html` generated in your `--run-dir`). Each item in `work_orders.json` defines:
   - `code`: Stock code (e.g. `8610.HK`)
   - `target`: Extraction target (`prospectus`, `allot`, or `gem`)
   - `packet_path`: Absolute path to the prepared Markdown source packet
   - `out_path`: Target path for extracted JSON payload
   - `schema_path`: Target field schema (keys, types, descriptions)

2. **Execute Field Extraction**:
   Extract all required fields from the packet text into `out_path`. Every populated field must contain `value`, `page`, and `quote`. Save the JSON payload and record deterministic validation:
   ```bash
   .venv/bin/python run.py derive_allot --config CONFIG --only CODE
   .venv/bin/python run.py validate --config CONFIG --target TARGET --only CODE
   .venv/bin/python run.py state extracted --config CONFIG --target TARGET --code CODE
   ```

3. **Perform Independent Review (Dual-Agent or Multi-Turn Handshake)**:
   A passing review requires an independent reviewer who inspects the original disclosures and verifies that extracted quotes and values match. If your runtime supports subagents, spawn a separate review subagent. Record the passing review credential:
   ```bash
   .venv/bin/python run.py state reviewed --config CONFIG --target TARGET \
     --code CODE --verdict pass --reviewer "IndependentReviewerAgent" \
     --evidence-ref "Path/to/review_notes.md" --review-note "Verified against disclosure packet"
   ```
   *Note: If no independent review capability is available in your runtime, deliver the prepared packets and report `WORK_PENDING` honestly. Never forge passing credentials.*

4. **Seamless Resume**:
   Rerun the resume command printed at the end of the run:
   ```bash
   python3 run.py resume --run-dir deliverables/run_<board>_<period>
   # or:
   python3 run.py agent-start --resume --run-dir deliverables/run_<board>_<period>
   ```
   The resume runner reloads preserved configurations, verifies reviewer hashes, writes approved cells through snapshot backups into the Excel workbook, collects external/market data, runs cross-checks, and exports clean CSVs and Codebooks with **Exit Code 0**.

The index contains issuer/target, packet path, output JSON path, packet readiness,
and extraction/review instruction files. Main Board has prospectus and allotment
targets. GEM has a board-adjusted prospectus target, allotment target and 15-field
`gem` extension target. Read the specified schema; do not hardcode the field count.
Legacy evidence filenames such as `HKIPO-MB8610.json` are internal compatibility
keys inside isolated GEM paths; the config/source report determines the board.

For each issuer, the extracting agent reads the packet and original pages. The
search CLI supports share-capital tables, financial periods, candidate bundles,
page ranges and regular expressions. Use issuer-specific detailed chapters and
consolidated accounts, verify currency/unit multipliers, preserve actual periods,
and distinguish current additions from year-end balances. The GEM instruction
supplements the legacy extraction workflow rules where the board differs.

Payloads use exactly the field schema's keys. Each entry has `value`, `page`,
`quote`, and `confidence`. Missing numeric values are the string `NaN`; missing
text/date values are the string `NA`. Real zeros require evidence. Every populated
field needs a real source page and short supporting quote. Missing third-year
financial history does not justify copying a second year into it. Public tranches,
cornerstones or greenshoe cannot be assumed from another issuer's structure.

Run deterministic allotment derivation **before** recording the final payload:

```bash
# Replace CONFIG and CODE; do not execute these placeholders literally.
.venv/bin/python run.py derive_allot --config CONFIG --only CODE
.venv/bin/python run.py validate --config CONFIG --target prospectus --only CODE
.venv/bin/python run.py state extracted --config CONFIG --target prospectus --code CODE
.venv/bin/python run.py validate --config CONFIG --target allot --only CODE
.venv/bin/python run.py state extracted --config CONFIG --target allot --code CODE
# GEM extension evidence:
.venv/bin/python run.py validate --config CONFIG --target gem --only CODE
.venv/bin/python run.py state extracted --config CONFIG --target gem --code CODE
```

The independent reviewer goes back to the original disclosure and checks every
populated field's definition, unit, period, page and quote. Save a report with
checked fields, missing/uncertain fields, corrections and source pages. A separate
agent/person should perform this review; the extracting process's self-check is
not independent sign-off. Actual approval is recorded with:

```bash
.venv/bin/python run.py state reviewed --config CONFIG --target prospectus \
  --code CODE --verdict pass --reviewer "Actual independent reviewer" \
  --evidence-ref "Actual review report path" --review-note "Actual review summary"
```

Use the corresponding `allot` or `gem` target and `--verdict fail` for a failed
review. The record's reviewer label must reflect a real review, not just a name
chosen to satisfy the CLI. If your host has no independent review capability,
deliver prepared packets and a pending-review report instead of bypassing gates.

Changing JSON, schema or supporting evidence invalidates the hash-bound approval.
Correct the source extraction, validate, record extracted, and independently
review the changed payload again. Rerun the same `collect` command afterward;
it checks the current credentials, writes reviewed values through snapshots,
collects external data and runs audits. Resume preserves collected cells and
stops if official issuer membership differs from the existing workbook.

## 5. Quality, maturity and completion

```bash
.venv/bin/python run.py status --config CONFIG
.venv/bin/python run.py audit --target all --config CONFIG
.venv/bin/python run.py cross_check --config CONFIG
```

Audit failures now return nonzero for missing formal extraction files, workbook/
JSON discrepancies or missing supported values. Both-sides-missing remains a
separate coverage category, so an audit with no discrepancies can still lack
values. Inspect `matches_with_value`, `both_missing`, absent JSON, review status
and written-cell alignment separately. GEM's `--target all` also checks its
extension sheet. `status`/bundle summary distinguish pending GEM extension gates.

Main Board cross-checks contain implemented regulatory checks and warnings.
GEM uses a separate consistency checker; it checks share identities and the
filing range and explicitly leaves dated GEM eligibility, float thresholds,
waivers and offering terms to source review. Neither is a legal certification.

GEM intervals with complete official coverage and no ordinary IPOs produce an empty cohort with zero issuers. Empty exports contain headers, not an invented observation.

Collection enriches common fields but does not automatically finish every
advanced event-table/expansion variable. Use `aftermarket`, event-table tools
and `expansion --dry-run` where those measures are required for Main Board. The advanced expansion writer does not yet support GEM; use common market horizons and separately reviewed GEM-specific evidence, and report this limitation. Preserve unresolved
source gaps and inspect write conflicts before using expansion. In particular,
review horizon definitions, benchmark matches, raw/adjusted price bases and
turnover provenance; Yahoo fallback turnover can be estimated.

The pipeline currently lacks one common historical `--as-of` option across all
collection and event tools. Recording a requested cutoff does not enforce it.
For a historical-cutoff analysis, explicitly filter stock and benchmark series,
recompute maturity consistently and record the actual effective cutoff. Avoid
claiming reproducibility at a historical cutoff unless those inputs were audited.
Unmatured windows remain missing; collect's successful exit does not mean all
future return horizons are available.

| Exit | Meaning |
|---|---|
| `0` | That stage completed; inspect scope/coverage before declaring collection complete |
| `3` from collect | Extraction, current credentials or independent review still required |
| `1` | Failed collection/check/tool, missing evidence, or data inconsistency |
| `2` | Invalid arguments or source/cohort coverage/configuration error |

Define completion by actual issuer coverage, evidence/review/write alignment,
audit discrepancies, supported field coverage and required market windows.
Report partial coverage explicitly. Tests verify implemented behavior; no finite
test suite establishes that this pipeline or every stored value has zero errors.

## 6. Export and download the data

Export each selected workbook first:

```bash
.venv/bin/python run.py export --config CONFIG
```

Main Board canonical outputs go to `pipeline/exports/` and `pipeline/codebooks/`.
GEM goes to their `GEM/` subdirectories and never enters the Main Board master
automatically. Rebuild the Main Board master only when its cohort exports changed:

```bash
.venv/bin/python run.py master --derive
.venv/bin/python run.py registry --check
```

Build an easy-to-share archive from generated cohort configs:

```bash
.venv/bin/python run.py bundle \
  --config pipeline/prospectus_pipeline/datasets/HKIPO_2026-01-01_2026-03-31_HKIPO-MB/cohort.yaml \
  --config pipeline/prospectus_pipeline/datasets/HKIPO_2026-01-01_2026-03-31_HKIPO-GEM/cohort.yaml \
  --output deliverables/ipo-data-2026Q1.zip
```

With no `--config`, bundle discovers the existing canonical year/quarter configs,
including both boards if configured. Use a new output filename for each snapshot;
an existing ZIP is never overwritten. Packaging operates on workbook copies and
does not modify original research workbooks or invent review records.

The ZIP contains per-cohort Excel, clean CSV, Markdown/JSON codebooks, available
formal extraction/schema/credential evidence, disclosure URL indices, audit/gate
reports, an English README, `quality_summary.json` and SHA-256 `manifest.json`.
GEM additionally has its original-layout research CSV and GEM extension CSV/
dictionary. PDFs, full text, environments and secrets are excluded. Review-report
references in credentials may point to local files not included in the archive;
retain the actual source review reports separately with the research project.

A normal bundle can distribute an honest legacy or incomplete snapshot. Add
`--require-reviewed` to reject cohorts without current written alignment or
without workbook/JSON reconciliation. Even that flag allows correctly documented
missing fields and does not establish the semantics of source evidence.

The agent should return the ZIP path/link plus the key Excel/CSV/codebook paths.
You can download/unzip it, open Excel, or load CSV in Python/R/Stata. Preserve the
quality reports with any shared dataset. If the host cannot expose local downloads,
use the user's authorized artifact export/storage mechanism; do not claim an
upload occurred merely because a local ZIP was created.

## 7. Organize and analyze

```bash
.venv/bin/python run.py workspace --check
.venv/bin/python run.py analysis --list
.venv/bin/python run.py analysis --study basic
.venv/bin/python run.py analysis --study underpricing
```

Existing built-in studies use actual Main Board 2026 listing dates and the Main
Board master. They do not analyze newly collected GEM rows or other years
implicitly. For GEM, start from `GEM_research_view.csv` and
`GEM_extensions.csv`, merge on stock code plus listing date where required,
inspect missingness and develop a separate explicit study specification. Do not
concatenate unlike board-specific CSVs by physical column number.

A basic inspection of a delivered GEM research view:

```python
import pandas as pd

frame = pd.read_csv("GEM_research_view.csv", na_values=["NA", "NaN"])
print(frame.shape)
print(frame.isna().mean().sort_values(ascending=False).head(20))
print(frame[["Stock Code", "Company", "Listing Date", "Offer Price (HK$)"]])
```

Review currency, financial annualization and return definitions before fitting
models. IPO underpricing uses raw first-day close divided by raw offer price
minus one, with any documented quotation-unit conversion. Allocation/application
returns have different denominators. Financial ratios must use consistently
measured consolidated periods; stale, partial or differently defined periods
must not be disguised by automatic filling.

## 8. Troubleshooting and maintenance

| Symptom | Action |
|---|---|
| Missing imports / obsolete lock | Rerun bootstrap; maintainers regenerate `uv.lock` from pyproject, then test; do not quietly switch to frozen |
| Git/PyPI/HKEX blocked | Request host network access and report exact failed stage; preserve successful caches |
| Annual coverage ends before requested date | Narrow the interval only if the user changes scope, or obtain valid official/reviewed coverage; report the gap |
| No independent reviewer | Prepare extraction/packets and a pending-review delivery; keep writeback blocked |
| Missing/incorrect quote or period | Return to original pages, correct payload and redo all affected gates |
| Changed official membership | Reconcile the existing workbook manually; preserve existing research cells |
| Excel open/locked | Close the workbook and rerun; preserve snapshot and transaction failure details |
| GEM field absent from source | Keep applicable unknown fields missing; do not resurrect deleted Main Board-only template columns |
| Market/benchmark unavailable or window immature | Record provenance and missing reason; do not substitute zero returns |
| Missing ZIP output | Inspect bundler error; fix the selected config/definitions before claiming delivery |

Routine developer validation is `make check-code`. Audit all selected cohorts
separately and retain each report. `make check` uses a single configured/default
cohort and therefore is not an all-years evidence certification. Never delete
raw source caches or historical snapshots just because Git ignores them.

See [GEM design](GEM_PIPELINE.md), [pipeline skill](../.agents/skills/hk-ipo-pipeline/SKILL.md),
[architecture](ARCHITECTURE.md), [analysis scope](../analysis/README.md), and
[contribution rules](../CONTRIBUTING.md).
