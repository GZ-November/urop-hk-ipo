# Pipeline subsystem

The collection layer maintains issuer cohorts from public HKEX disclosures. Current statistical and econometric analysis is limited to 2026 listings; historical cohort artifacts remain available for collection and validation.

| Directory | Purpose |
|---|---|
| `cohorts/` | Canonical 202-variable research workbooks |
| `exports/` | Cohort clean CSVs and the master analysis panel |
| `codebooks/` | Per-cohort rendered variable definitions |
| `registry/` | Machine-readable derived registry snapshot |
| `reports/` | Drift, exclusions, evidence manifest and market reports |
| `templates/`, `sources/` | Collection templates and official listing reports |
| `docs/` | Original construction manuals and collection notes |
| `prospectus_pipeline/` | CLI, configuration, source, schema, tools and tests |
| `backups/` | Local pre-write snapshots |

Run commands from the repository root:

```bash
python run.py status --config prospectus_pipeline/config_2026q3.yaml
python run.py audit --target all --config prospectus_pipeline/config_2026q3.yaml
python run.py registry --check
python run.py master --derive
make check-code
make analysis
```

From this directory, use `python prospectus_pipeline/run.py ...`. Cohort configs keep the workbook, listing-date interval and runtime paths together. `paths.py` defines canonical artifact locations; `master_contracts.py` defines event-table contracts.

The extracted → validated → reviewed → written lifecycle binds the exact reviewed JSON to its hash. Workbook transactions preserve styles and snapshot before saving. Unknown inputs and unmatured windows remain missing. Public research artifacts are versioned; raw PDFs, text/packet caches, scratch utilities, run logs and snapshots remain local.

[Engine guide](prospectus_pipeline/README.md) · [Maintenance manual](SYSTEM_MANAGEMENT.md) · [Analysis guide](../analysis/README.md) · [Data policy](../SECURITY.md)
