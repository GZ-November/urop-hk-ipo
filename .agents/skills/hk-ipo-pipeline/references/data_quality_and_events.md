# Evidence gaps and event-data reconciliation

## What an audit establishes

Run a separate audit for each requested cohort and retain its JSON/Markdown
report. `audit_dataset` compares workbook cells to the values in available formal
extraction files; it does not re-review disclosure semantics or establish that
all extraction hashes are currently authorized. Inspect `status` and review
records separately.

Report these categories independently:
- `excel_missing`: extracted value exists but the workbook cell is missing.
- `json_missing`: workbook value exists but no corresponding extracted value
  exists (the file or individual field may be absent).
- `value_mismatch`: both values exist but differ under the comparison rules.
- Both missing: counted as a match by the current auditor, not verified evidence.

Zero value mismatches therefore does not imply complete evidence. Group gaps by
issuer, target and semantic field; distinguish an absent formal file from a
partially populated extraction. The 70+18-field comparison does not validate all
202 workbook variables or all external/event inputs. SHA-256 manifests detect
byte changes; they do not prove source linkage, semantic correctness or coverage.

Repair evidence from original disclosures and preserve the existing workbook
value as a reconciliation candidate. Validate the corrected payload and obtain
independent, hash-bound semantic review before source-field writeback. Do not
copy workbook values into JSON just to obtain an all-matched report. Rerun the
audit after writing. For a dated audit snapshot, see
`docs/archive/reviews-2026-09-30/CODE_REVIEW_2026-09-30.md`; rerun audits rather than hardcoding its counts.

## Event and horizon definitions

For market/event tasks inspect `market_panel.py`, `stabilization_panel.py`,
`lockup_panel.py`, `market_observations.py` and `expansion_mapping.py` under
`pipeline/prospectus_pipeline/src`.

| Output | Rules to preserve |
|---|---|
| `daily_market_panel.csv` | Chronological observations; missing daily return stays missing; real zero turnover stays zero |
| `horizon_summary.csv` | Day_5/Day_20 use trading-observation definitions. Month_1/3/6/12/24/36 use calendar-month targets and the first observed trade date on/after the target. Record target/actual dates and maturity; exclude bars after the chosen market-engine cutoff |
| `stabilization_events.csv` | Generic stabilizing-actions text is insufficient proof of market purchases. Announcement date needs independent evidence. Require full [-5,+5] endpoints and full +20 endpoints for the respective price/volume measures; never clamp incomplete windows |
| `lockup_events.csv` | CAR includes both endpoint daily returns: 11/41/61 observations for [-5,+5]/[-20,+20]/[0,+60]. Require the prior benchmark close and finite observed stock/benchmark returns throughout. No benchmark-zero substitution or assumed locked-share percentages |
| Six-month expansion statistics | Fields 181–184 (Amihud, zero-volume days, daily volatility, drawdown) require a mature observed Month_6 horizon. Date-sort bars and use its inclusive actual-date endpoint; no immature partial-window estimate |

Metrics can mature independently. Inspect each value as well as event status:
`IMMATURE_WINDOW`, `INCOMPLETE_WINDOW`, `MISSING_BENCHMARK_DATA` and
`MISSING_RETURN_DATA` are not interchangeable. Turnover ratios retain true zeros
and require a usable denominator. Cornerstone events require an actual cornerstone
allocation; resolve stale absence against the final allocation before mapping.

For reproducibility record the observation cutoff, raw/provider provenance,
algorithm version and missing reasons. `MarketPanelEngine(today=...)` accepts an
explicit cutoff; the standalone event scripts do not expose a common `--as-of`
flag. A historical-cutoff study needs consistent filtering of daily and benchmark
inputs and event maturity, rather than assuming all engines share that cutoff.
The separate `tools/external/aftermarket.py` writes some 1M/6M workbook fields;
trace the actual producer before attributing a value to `horizon_summary.csv`.

## Regenerating previously written values

An algorithm fix changes future calculations; it does not automatically repair
existing CSVs, Excel cells, cohort exports, master data or statistical outputs.
Previously generated data from any year can need reconciliation. For the requested
cohorts:

1. Inventory configs and snapshot old event tables/workbooks with their hashes.
   Use isolated output paths or temporary cohort-config copies for candidate
   regeneration when comparing old and new results. Shared `out/master` paths can
   otherwise replace another cohort's panels.
2. Regenerate the daily/horizon inputs first, then stabilization and lockup outputs.
   Compare by issuer, horizon/event category and field. Classify value changes,
   new missing values, maturity changes and unsupported old values.
3. Preview expansion with `run_pipeline.sh expansion --dry-run --config ...` and
   reconcile against source evidence. Inspect upstream diff and writeback plans;
   the overwrite guard detects clearing/placeholder conflicts, not every wrong
   nonempty value. Do not use `--force-overwrite` merely to bypass a conflict.
4. After resolving the requested changes, write through the normal snapshot/gate
   workflow, export affected cohorts and rebuild master/registry as appropriate.
   Rerun affected analyses under their own sample definition and refresh the
   evidence manifest for the final artifacts.

Completion reports must separate evidence repaired, data recalculated, workbook
cells reconciled and analysis rerun. Tests passing alone completes none of these
data tasks. Do not claim all-data completion when only a default cohort was run.
