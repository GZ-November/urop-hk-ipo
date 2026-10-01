# Start or Reproduce a Study

The current offering-research population is **113 Hong Kong Main Board IPOs listed through 30 September 2026**, with Q1/Q2/Q3 counts of 38/45/30. Start with the [English facts report](../analysis/out/offer_facts/facts.md), [advanced offering results](../analysis/out/offering_economics/analysis.md) and [literature review](IPO_LITERATURE_METHODS_2026.md).

Earlier source reviews used a 106-issuer population. Their evidence scope is historical and does not certify the later 113-issuer sample. Superseded numerical narratives remain in the [archive](archive/README.md).

## Reproduce Existing Results

After installing the root dependency profiles:

```bash
make check-code
make offer-facts
make offering-economics

# All maintained studies, including first-day and aftermarket analyses
make analysis
```

The offering modules use the committed master, verify the September cutoff and 113-issuer population, and record input hashes. They do not collect new evidence or market data. Full model samples range from 110 to 112 observations; each outcome has its own common-sample log.

## Inputs and Outputs

| Layer | Location | Use |
|---|---|---|
| Canonical workbooks | [pipeline/cohorts/](../pipeline/cohorts/) | Update through validated, reviewed transactional writeback |
| Definitions | [Registry](../pipeline/registry/HKIPO_Variable_Registry.yaml), [codebooks](../pipeline/codebooks/) | Resolve units, timing and missing-value semantics |
| Disclosure evidence | [Data](../pipeline/prospectus_pipeline/data/), [pipeline outputs](../pipeline/prospectus_pipeline/out/) | Source references, extraction/review state and cached observations; some raw materials are local |
| Main study input | [Master CSV](../pipeline/exports/HKIPO-MB-MASTER_clean.csv) | Select actual 2026 listing dates; historical rows remain stored |
| A+H references | [2026 panel](../pipeline/exports/HKIPO-2026-AH-reference.csv), [cross-year panel](../pipeline/exports/HKIPO-MASTER-AH-reference.csv) | Reference coverage does not automatically expand estimation samples |
| Margin financing | [Source ledger](../pipeline/prospectus_pipeline/data/margin/reported_snapshots.json), [observations](../pipeline/exports/HKIPO-2026-margin-daily.csv) | Preserve dates, links and survey scope; do not interpolate missing days |
| Research modules | [Analysis index](../analysis/README.md) | Implementations, model scope and output directories |
| Generated results | [analysis/out/](../analysis/out/) | Reports, tables, figures, sample records and diagnostics |
| Evidence reviews | [Source review artifacts](../pipeline/reports/margin_review/), [readiness notes](../pipeline/reports/research_readiness/README.md) | Dated repair history and unresolved or previously resolved evidence gaps |

## Start a New Question

Use the project [IPO empirical research skill](../.agents/skills/ipo-empirical-research/SKILL.md) for theory, definitions, estimation and inference. Use the [pipeline skill](../.agents/skills/hk-ipo-pipeline/SKILL.md) for collection, validation and refresh. Project variable and date contracts take precedence over generic defaults.

A useful study request is:

```text
Study [question] using this repository's IPO empirical research skill.
Read the research guide, applicable design and relevant skill references.
Confirm the sample, units, timing and evidence coverage in the current master.
Write the estimand, controls, common-sample rules and inference approach before
running new models. Keep the analysis exploratory if results have already been
examined. Reuse shared inputs and helpers, save all reported specifications,
and generate numbers from code with explicit N, cutoff and limitations.
```

For the latest offering models, see the [design record](OFFERING_ECONOMICS_DESIGN_2026.md). Older frontier questions and their original sample scope are in [RESEARCH_DESIGN_2026.md](RESEARCH_DESIGN_2026.md).

## Updating the Snapshot

`python run.py master --derive` merges existing cohort exports; it does not export changed workbooks. Export every changed cohort with `python run.py export --config prospectus_pipeline/config_2026qN.yaml` before rebuilding the master and running studies.

`make refresh-2026` deliberately fetches raw first-day and aftermarket observations, refreshes academic fields and A-share references, and rewrites workbooks, exports and reports. Run it when source updates or mature event windows are needed. Shared-path cohort jobs must run sequentially and preserve their individual audit reports.

Existing candidate fields and dated repairs need source-specific interpretation. Unknown backing, unsupported governance classifications, sparse financing snapshots and immature event windows are not zero. Mechanism choice, cornerstone allocation and retail demand are selected together; extra controls or matching cannot create missing identification or common support.

See the [repository guide](REPOSITORY_GUIDE.md) for artifact placement and cleanup, and the [research plan](RESEARCH_PLAN_2026.md) for study priorities.
