# 2026 comprehensive report tables

The [English LaTeX report](../../../docs/reports/HK_IPO_2026_COMPREHENSIVE_REPORT.tex) covers 113 ordinary IPOs listed in 2026 Q1 to Q3. The price cutoff is 30 September 2026. The [text version](../../../docs/reports/HK_IPO_2026_COMPREHENSIVE_REPORT.md) contains the same prose and tables.

Reproduce tables and source in place from the repository root:

```bash
.venv/bin/python analysis/retail_2026_report.py
```

The script reads the three canonical 2026 workbooks, the variable registry, the master export, and verified one-lot return outputs. It checks source hashes and joins the same 113 issuers. It creates no simulation and writes no workbook. Compile the existing `.tex` file in the built-in editor for the PDF preview.

- `workbook_field_coverage.csv` lists all 202 registered fields, their source layer, recorded definitions and units, and presence counts in the workbooks and analysis export. Presence is not a semantic source approval.
- `company_data_uses.csv` and `market_data_uses.csv` explain selected field groups and possible research uses.
- `descriptive_statistics_raw.csv` retains full precision, minima and maxima. Descriptive returns use exact prices rather than the rounded exported headline return.
- Other CSV files contain the report's sample, industry, route, return and sensitivity tables.
- `language_check.json` records descriptive sentence and paragraph checks. It does not certify full ASD-STE100 dictionary compliance.
- `run_manifest.json` binds inputs and generated source/tables to SHA-256 hashes.

Fee scenarios are hypothetical. Expected application returns do not describe observed account performance. Later return horizons and event studies require their own mature, matched samples.
