# Agent readiness, GEM implementation and workspace audit — 12 October 2026

## Scope and conclusion

The published repository baseline was `b743da90884ef99c1cc887b54a1bdde5b65abf34`.
The owner's local checkout also contained substantial unpublished research changes.
The GitHub change is built from the published baseline. Changes were separately
integrated into the local checkout without replacing those existing changes.
Consequently, the published Main Board schema has 202 columns and the local
research schema has 220. The new GEM canonical sheet has 195 columns.

The pipeline now supports automatic locked environment setup, separate Main Board
and GEM discovery and work orders, source-bound validation/review/writeback, and
portable data delivery. This is an executable agent workflow: the agent still
needs terminal/network/document access and a real independent reviewer. A link
cannot provide those capabilities by itself. Passing software checks does not
prove every historical observation correct.

## Repaired failures

| Finding | Repair and practical effect |
|---|---|
| Stale dependency lock omitted matplotlib despite the declared analysis extra | Regenerated lock; bootstrap uses `uv sync --locked` so metadata drift fails visibly. |
| Audit discrepancy and external-stage failures could be reported without failing the command | Nonzero exit status now propagates; collection stops on unresolved reconciliation. |
| Old validation/review flags could be mistaken for current evidence | Collection requires current hash-bound extracted, validated and reviewed state. |
| Report underpricing used filing-range midpoint | Report uses the actual offer price; unsupported return calculations stay missing. |
| Missing turnover was converted to zero | Missing/invalid turnover stays missing; partial windows do not become complete averages; observed zero remains valid. |
| Upper-bound discretionary fee descriptions resembled actual paid fees | Source catalog, codebooks and registry explicitly describe disclosed upper bounds. |
| GEM report assumed Main Board column positions and prospectus dates | Separate report parser and cache, multi-row headers, continuation handling and publication-date discovery/provenance. |
| Main Board admission, reform and lockup assumptions leaked into GEM | Seven fields physically removed; GEM validation avoids Main Board admission-rule inference and contractual-date assumptions. |
| Original GEM workbook had millions of empty formatted cells | Removed formatting outside the original 46 columns after verifying no populated cells were there. |
| Local dashboard snapshot and 202-column assertions drifted from the local 220-column registry | Rebuilt the local snapshot, checked exact registry field order and used digest comparison to avoid expensive HTML assertion diffs. This dashboard repair is local only because the published baseline does not include that dashboard. |

## GEM design and real source smoke test

The original student workbook remains a historical template with examples. Its
first 46 fields and existing cell contents/styles/formulas are preserved. A new
blank template supplies a user-facing `GEM` view, canonical `NLR` data and
`GEM_details` extension/provenance sheet. The extension has 15 independently
extracted fields. The prospectus schema has 69 fields, allotment 18.

Removed concepts: WVR, Chapters 18A/18C, technology commercialization stage,
Main Board 2025 pricing reform regime, and the fixed controller six/twelve-month
expiry fields. Cornerstone investment, public offers, greenshoes and other
issuer-dependent concepts remain available where disclosed. Missing evidence
never becomes zero. See `docs/GEM_PIPELINE.md` for the full original-field map.

A real 2026 Q1 GEM collection discovered BBSB (8610.HK), downloaded its 563-page
prospectus and 16-page allotment/results document, and generated isolated packets
and work orders. It correctly stopped with exit code 3 awaiting extraction and
independent review. The committed initial cohort is explicitly source-only;
this smoke test does not certify its financial extraction. Empty GEM intervals
also have a tested path without inventing an observation.

The advanced Main Board `expansion` event writer remains unavailable for GEM and
returns an explicit error. Common academic/market fields are supported. Built-in
research studies continue to select Main Board 2026 listings; GEM requires a
separate explicit analysis specification.

## Validation evidence

On the isolated published-baseline checkout, `make check-code` passed:

- 325 pipeline tests (two source-PDF acceptance checks skipped because those
  Main Board raw PDFs are intentionally absent from a fresh clone).
- 63 analysis tests and 10 subtests.
- Python compilation, static checks and registry consistency.

In the owner's unpublished local checkout, 332 pipeline tests passed. Analysis
finished with 125 passing tests, 12 passing subtests and three stale historical
snapshot failures. Two depend on the corrected retail brief's recorded
`analysis/research_inputs.py` hash; the return-stage manifest also records an
older master CSV hash. A deterministic brief refresh correctly refused to proceed
because its upstream source-follow-up manifest records a different master CSV.
The original manifests were preserved, not rewritten to claim a new source
review. These older studies require a source reconciliation and deliberate
recomputation before their saved results can be called current. A backup was
made before the attempted refresh; it stopped before writing results.

All runtime imports/assets and bounded HKEX listing-report, HKEX issuer-search
and HKMA connectivity probes passed on the final locked environment.

Additional tests cover audit/external exit propagation, portable work orders,
GEM source layouts and coverage, original-template mapping and exclusions,
independent GEM extension gates, empty-sample export, actual-price returns,
unknown/zero/partial-window turnover and delivery manifests/nonmutation.

Installation was exercised with the locked development profile and project
Python 3.12. Connectivity diagnostics and provider limitations must be read as
point-in-time availability, not a guarantee of future downloads. Native Windows
and every optional market provider were not exhaustively tested.

## Data quality findings

The stored cohorts contain 156 issuers: Main Board 2025Q1=15, 2025Q2=27,
2026Q1=38, 2026Q2=45, 2026Q3=30, and GEM 2026Q1=1 source-only issuer.

- The two 2025 Main Board cohorts lack formal prospectus/allotment JSON for their
  42 issuers. Existing workbook values cannot be certified from those missing
  artifacts. Keep them identified as legacy/unreviewed.
- On the isolated published checkout, all three 2026 Main Board cohorts reconcile
  Excel with present formal JSON without numeric differences. Some fields are
  missing on both sides, and a fresh clone lacks ignored source-bound review
  credentials. Reconciliation alone is not independent source verification.
- The owner's local 2026Q2 workbook has three evidence gaps for 6106.HK:
  allotment `col_DA`, `col_DB`, `col_DC`. Existing workbook values were preserved;
  no extraction or passing review was fabricated to remove the discrepancy.
- GEM evidence and its 15 extensions remain pending extraction/review. The initial
  source-only workbook is useful for membership and discovery, not regression.
- Existing scripts do not enforce one historical observation cutoff across every
  public market/event stage. Requested cutoff filtering and immature horizons
  must be reported explicitly, as described in the English instructions.

`bundle --require-reviewed` refuses incomplete/unreviewed/mismatched cohorts.
Ordinary bundle delivery includes quality summaries so partial legacy data can
be transported without being mislabeled as complete.

## Full local folder inspection and cleanup

An inventory covered 22,646 files, including environment and Git metadata:
9,549 research/source/code files, 256 regenerated cache files and 12,841
environment/version-control files. Cleanup removed only the 256 untracked
`.DS_Store`, bytecode and pytest-cache files (3,530,615 bytes), plus 20 empty
cache directories. Hashes of all 9,549 protected research/source/code files
remained unchanged during that cleanup. No broken symlinks were found.

The historical GEM workbook shrank from 16,667,417 to 53,068 bytes. All 19,867
surviving in-range XML cell elements were byte-identical. Subsequent authorized
code/template/definition edits are separate from the cache-cleanup hash check.

Structural checks opened/parsed 229 Python files, 4,010 JSON files, 14 YAML files,
260 CSV files, 48 XLSX containers and 493 PDFs, with zero structural issues.
This covers parsability, CSV widths, ZIP integrity and PDF opening; it does not
certify every source statement or financial cell. Raw disclosures, evidence,
research outputs, useful historical templates, environments and existing local
research edits were retained. Tests can recreate disposable caches.

Local detailed inventory, cleanup results, structure results and pre-integration
code backup are under `pipeline/backups/workspace_cleanup_2026-10-12/` and are
intentionally not published. Visual inspection confirmed the new workbook's
header formatting and separate sheets are readable.

## Entry points and delivery

Start with `docs/AGENT_INSTRUCTIONS.md` (English copyable prompt and complete
commands), then `docs/GEM_PIPELINE.md` (design and field applicability).
Use `python3 tools/bootstrap.py --profile dev`, `make check-code`, board-specific
`run.py collect`, actual independent review and `run.py bundle`.

The local delivery ZIP contains selected cohort Excel/CSV files, GEM view and
extensions, dictionaries, formal evidence where present, audit/state summaries,
SHA-256 manifest and both English instruction documents. Packaging works from
copies and does not modify research workbooks. Raw PDFs and environments remain
outside the ZIP and can be downloaded using their source indices.
