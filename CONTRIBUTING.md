# Contributing

## Development and checks

Use a source checkout and a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[analysis,dev]'
git checkout -b codex/your-change
make check-code
```

`make` selects the root `.venv/bin/python` when available; use `make PYTHON=/path/to/python check-code` to override it. `make test` runs both the pipeline and analysis suites. Production acceptance tests use versioned artifacts when available; portable tests build temporary fixtures.

Activate the optional local push gate with `git config core.hooksPath .githooks`. The hook and CI run the same `make check-code` target. Missing lint tooling is an error, not a successful skipped check.

## Source and research contracts

- Follow `.editorconfig`; public functions and CLI stages should explain their inputs and behavior. Use type hints where they clarify the contract.
- Keep parsing, calculations, validation and writeback deterministic. Use AI for bounded unstructured extraction and independent semantic review.
- Never bypass schema, quotation or hash-state checks. Missing evidence remains missing; zero is a measured value, not a missing-data substitute.
- Preserve workbook styles and create the existing pre-write snapshot. Prefer `workbook_transaction.py` for atomic workbook changes.
- Author variable definitions in `pipeline/prospectus_pipeline/src/variable_catalog.py`; regenerate the registry and codebooks, then run `make registry-check`. See [ADR-0001](docs/adr/0001-variable-definitions-authoring.md).
- Use `paths.py` and `master_contracts.py` for pipeline artifact paths and producer/consumer contracts.
- Add focused regression tests for changes to field interpretation, financial formulas, maturity guards, validation and writeback. Run relevant tests, then `make check-code` before pushing.

## Analysis scope

All current regressions and descriptive statistics, including Module A, use **2026 listings only**. Use `select_2026(load_panel())`; do not select by cohort label alone or add historical comparison observations. Prior literature and the frozen sponsor ranking can inform definitions without contributing observations to the estimation sample.

Follow [the 2026 research plan](docs/RESEARCH_PLAN_2026.md). Report N and missing inputs, keep the nested regression sample constant, include the April-June control, and distinguish exploratory associations from causal claims. Unmatured event windows must remain missing. Regenerate outputs with `make analysis` after changing analysis behavior.

## Data distribution

This repository versions research artifacts built from public disclosures, including canonical workbooks, clean CSVs, extraction JSON, codebooks, registry snapshots, official listing reports and research outputs. This is consistent with `.gitignore`; there is no blanket ban on spreadsheets or JSON.

Keep credentials, private material, virtual environments, raw prospectus PDFs, full-text/packet caches, isolated `datasets/` workspaces, workbook snapshots, extraction run logs and one-off debugging scripts local. Ignore rules do not remove already tracked files or guarantee that a file is safe to publish. Stage intentional paths and inspect the staged diff.

## Review and contribution

Open a PR against `main` for collaborative changes. Describe the concrete behavior change, relevant evidence and validation. For regulatory changes, use official sources, preserve the applicable date/regime distinction, and add boundary cases in `tests/test_cross_check.py` or the affected module's tests.
