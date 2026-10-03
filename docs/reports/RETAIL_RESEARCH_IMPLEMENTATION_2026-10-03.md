# Retail Research Implementation — 3 October 2026

Observation cutoff: 30 September 2026. The work was implemented in the latest Desktop checkout.

## Completed work

1. Separated arithmetic reconciliation from independent semantic approval. Read-time gates bind the reviewed candidates, coverage and source text to their recorded hashes. Re-extraction creates pending candidates only. Existing frozen inputs retain their prior review; no new approval was fabricated.
2. Distinguished 112 strict one-lot IPOs from the 113-IPO one-lot/minimum-tier sample. For 2649, the current record shows a 200-security trading lot and a 500-security minimum application tier; the mismatch remains a source follow-up. Guaranteed and additional ballot quantities are modeled separately.
3. Computed single-application outcomes and repeated-participation distributions using 100,000 independent-ballot simulations. Added listing-month sampling sensitivity, winner-concentration diagnostics and an exclusion check for 3355. Original and inferred 3355 quantities are retained separately.
4. Decomposed allocation-weighted application returns into the product of means and allocation/return covariance, with quarter, A+H and population-size groups.
5. Produced handling-fee frontiers, complete application-size schedules and financing scenarios. Added demand-regression influence checks and matched five/twenty-day market-relative returns for 100 IPOs.
6. Converted current reports and their generators to English, placed the consolidated report in `docs/reports/`, and cataloged the reports and study outputs in the research workspace.

## Reproduction

```bash
python run.py analysis --study basic --study demand --study allocation_profit --study retail_distribution
python tools/build_empirical_report.py
make check-code
make workspace-check
```

See [the consolidated report](EMPIRICAL_RESEARCH_REPORT_2026.md) and [the generated result directory](../../analysis/out/retail_distribution/).

## Validation and limitations

The prior implementation passed 406 pytest tests and 179 subtests; its final gate changes passed 19 focused tests and two subtests. The English publication edition passed `make check-code`: 313 pipeline tests and 93 analysis tests (406 total), plus 12 analysis subtests. Workspace validation verifies 50 links. Source/static checks and registry consistency use `make check-code`; workspace links use `make workspace-check`.

The study conditions on observed prices and independent ballots. HK$88 is hypothetical; current channel quotes do not establish historical account fees. Costs exclude allotted-security subscription brokerage/levies, sale costs and opportunity cost. Principal budgets pay fees separately and do not enforce overlapping cash constraints. Results are not annualized or causal. No source field was changed during this research implementation; the 19 master corrections in the submitted baseline predate it.
