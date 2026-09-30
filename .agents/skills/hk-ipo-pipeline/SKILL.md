---
name: hk-ipo-pipeline
description: >-
  Collect, audit, validate, refresh, and export Hong Kong Main Board IPO data across
  years and cohorts, from official disclosures through market and event panels.
  Use for pipeline status, evidence reconciliation, listing-rule cross-checks,
  dataset coverage, research reports, econometric exports, and new IPO collection.
---

# Hong Kong Main Board IPO Pipeline

Use this skill for the complete dataset lifecycle: issuer membership, prospectus
and allotment extraction, external market data, stabilization and lockup events,
workbooks, exports, registry, master panel, and analysis inputs.

## Scope and routing

The skill is year- and cohort-general. Resolve the requested years, listing-date
interval, cohorts, variables and observation cutoff from the task. For a request
for all data, inventory every configured cohort and report coverage and gaps;
do not silently select the default config or narrow the dataset to one year.
A restriction in a particular research plan applies to that study, not to data
collection, storage, auditing, or other studies. Read `analysis/README.md` before
running existing analysis scripts to check their implemented sample scope.

Read the relevant reference for the task:
- [Variable and provenance map](references/variable_codebook_overview.md): fields,
  types, sources, and stable header resolution.
- [Data quality and event regeneration](references/data_quality_and_events.md):
  missing evidence, event windows, old outputs, and safe reconciliation.
- [Empirical analysis](references/empirical_analysis_guide.md): sample selection,
  missing values, model definitions, and the repository's current study.
- [Source preferences](references/statutory_evidentiary_rules.md): disclosure
  chapters, consolidated financial statements, units and reporting periods.
- [Listing-rule guide](references/listing_rules_guide.md): implemented regulatory
  checks. Verify dated official HKEX sources, issuer terms and waivers when
  assessing a rule; a stored guide or passing check is not a legal determination.

## Execution and cohort selection

Run commands from the repository root using the wrapper; it selects the project
interpreter and changes into `pipeline`:

```bash
./.agents/skills/hk-ipo-pipeline/scripts/run_pipeline.sh status --config /absolute/path/to/cohort.yaml
./.agents/skills/hk-ipo-pipeline/scripts/run_pipeline.sh audit --target all --config /absolute/path/to/cohort.yaml
```

Discover cohort configs rather than hardcoding a list. Inspect each config's
workbook, sheet, dataset dates, `filter_period`, paths and optional `state_dir`.
Some configs share output paths: run those jobs sequentially and preserve each
cohort's report before the next job overwrites it. Dataset period labels are not
proof of full-year or full-quarter coverage; check observed issuer dates and
reconcile membership against official new-listing reports.

`check_env.sh` checks core imports and installs missing requirements. Use it for
environment repair when needed, not before every read-only inspection. Analysis
and development dependencies are separate profiles in root `pyproject.toml`.

## Core operations

| Command | Purpose and interpretation |
|---|---|
| `status` | Extraction/validation/review/write state and hash alignment |
| `audit --target all` | Workbook vs available formal prospectus/allotment JSON; inspect coverage separately from matches |
| `cross_check` | Cross-field identities, market bounds and implemented listing rules |
| `report` | Configured cohort's descriptive report; respect the requested research sample |
| `export` | Updated workbook to clean CSV and Markdown/JSON codebooks |
| `registry` / `registry --check` | Build definitions snapshot / check consistency |
| `master --derive` | Merge existing cohort exports, drift checks and optional derived ratios |
| `exclusions` | Selected cohort's membership and exclusion log |
| `evidence` | SHA-256 artifact manifest; freezes bytes, not source correctness |
| `aftermarket` | Refresh selected cohort's aftermarket fields as windows mature |
| `expansion --dry-run` | Preview academic expansion writeback and conflicts |

The master can retain multiple years; its contents do not determine a study's
sample automatically. Export changed workbooks before rebuilding the master.
Registry metadata originates in `src/variable_catalog.py` and the extraction
schemas; do not hand-edit generated definitions to hide drift. `master` reports
listing-date/identity/fill-rate warnings as well as hard errors: inspect both.

From the repository root, `make check-code` runs maintained-source static checks,
pipeline and analysis tests, and registry consistency. `make check` additionally
runs status, audit and cross-check for the selected/default config. Neither
establishes complete source evidence or audit coverage for every cohort.
`make aftermarket-refresh` processes all canonical cohort configs; it writes
workbook fields, so use the individual stage for a narrower refresh.

## Collection and evidence gates

For a new issuer/cohort, use `collect` with the requested listing interval and
workbook/config. It prepares official disclosures and extraction packets, then
exits with code 3 while extraction or independent review is pending. Resume the
same command after completing the requested gates. Individual stages are
`find`, `download`, `prepare`, `allot`, `validate`, `write`, `external`, `academic`,
and the audit/export operations above; inspect CLI help for their options.
`collect` does not support `--dry-run`.

Formal extraction needs the field's value, source page/quote and applicable
provenance, with disclosed units and reporting period reconciled. Validation
checks deterministic contracts; independent semantic review checks that the
quote supports the value and definition. Writeback requires passing extracted,
validated and reviewed records bound to the same payload hash. Editing the
payload invalidates earlier authorization; validate and obtain review again.
Do not generate a passing review record merely to unblock writing.

For missing JSON or failed evidence, inspect the original disclosure, reconstruct
or correct the extraction, validate and independently review it. An existing
Excel value, another output file, a zero discrepancy count or a manifest hash
cannot substitute for this evidence. Keep unsupported fields missing and report
why. See the data-quality reference before regenerating event-derived cells.

## Completion

Report the actual cohorts/dates and layers examined, comparable cells and missing
evidence, event maturity and benchmark gaps, checks run, and artifacts refreshed.
Distinguish code fixes from data regeneration and reconciliation. If only a subset
was covered, state it; do not label the whole dataset verified. Archive snapshots
and regenerate exports/master/analysis/manifest only for the authorized workflow.
