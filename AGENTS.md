# Agent entry point

When the user names a listing period to collect, asks to continue a collection,
or gives only this repository link, follow
[the hk-ipo-collect skill](.agents/skills/hk-ipo-collect/SKILL.md); it starts with
`python3 run.py plan <period>`. Rerunning the same `run.py start` command resumes.

For installation, new Main Board/GEM collection, review, resume or data delivery,
read [the English operating instructions](docs/AGENT_INSTRUCTIONS.md) and follow
its ordered workflow. For GEM, also read [the template and board adapter](docs/GEM_PIPELINE.md).
Use the repository's `tools/bootstrap.py`; the lockfile and project metadata are
one dependency contract. Run `run.py` from the source checkout.

Resolve board, inclusive listing-date interval and observation cutoff from the
request. When a collection request supplies only this repository link, use the
latest completed calendar quarter in Hong Kong for both boards, state that
assumption and attempt official source discovery. Coverage failures remain
explicit gaps; an unavailable report is not evidence of zero IPOs. Large ranges
should be split into nonoverlapping calendar quarters. Existing studies select
Main Board 2026 listings; GEM needs a separate sample and research specification.

## Fixed financial-period standard (teacher's manual §2.3, confirmed 2026-10-14)

Every extraction, review and repair uses this rule; do not reinterpret it.

- **year-1** is the latest period in the prospectus's Accountants' Report (the
  audited Track Record, per its "Track Record Period" definition), whether a
  full year or a 3–11 month stub. col_AT is its end date.
- **year-2 / year-3** are the two complete financial years before year-1.
  Never derive them by subtraction.
- Unaudited figures outside the Accountants' Report are never year-1. That
  includes appendix quarterly results and "Recent Developments" numbers.
- Only net sales, profit before tax and profit for the period (col_AH/AK/AN)
  are annualised (×12/months). The workbook columns BC (= months/12) and
  CN/CO/CP (originals) are derived by `run.py disclosure_notes`, not extracted;
  they are not the payload key `col_BC`.
- Assets, equity, liabilities, cash and interest-bearing debt take the year-1
  end values.
- Operating cash flow, R&D expense, gross profit and capital expenditure take
  year-1's original-period values, not annualised.
- `run.py search periods CODE` applies the rule and `validate` rejects a wrong
  anchor or annualisation.

Collection exit 3 means extraction/independent review pending: loop on
`run.py work next --config CONFIG`, start one new subagent per dispatched brief
(the scheduler sets concurrency), and resume the same collection command.
Use an independent reviewer with original-source access. A credential requires
a real review of the exact payload; preserve pending review when the runtime
cannot supply an independent reviewer. Do not fabricate a passing sign-off.

## Token & API cost optimization rules (mandatory for batch collection)

1. **Issuer-level bundling (`work next`)**: Never spawn separate extractor subagents
   for `prospectus`, `allot` and `gem` of the same issuer. Always dispatch via
   `run.py work next --config CONFIG` so one extractor subagent completes all
   targets of one issuer in a single context (reading shared company/share/cornerstone
   context once).
2. **Zero-token deterministic fields**: Do not spend subagent tool calls searching
   for fields filled or derived deterministically by `work finish-extract` /
   `derive_allot` (`col_CV` greenshoe, `col_CK` when cornerstone is absent,
   `col_CQ` pricing date, `col_DA/DB/DC` free float, and `col_CR` announcement
   datetime pre-injected in the brief) or later stages (`BC`, `CN/CO/CP`, market,
   HKMA, HSIC, aftermarket, academic variables).
3. **Single-pass reading & batched search**:
   - **Extractors**: Read the brief (which already embeds `search periods`,
     `search sharecap` and `col_CR`) and the deduplicated packet (which already
     embeds `<!-- TABLE_START -->` structured Markdown tables) first. For any
     remaining fields not found in the packet, batch-query candidates in **one**
     call using `run.py search bundle CODE --fields col_X,col_Y,col_Z` instead of
     running multiple per-field regex searches.
   - **Reviewers**: Verify populated fields directly against the 700-char page
     excerpts in the review brief's `Review sheet`; open full pages (`search pages`)
     or run `search search` only when an excerpt is truncated, a validation warning
     is present, or a field is marked missing (`NaN`/`NA`).
4. **No redundant topic packets**: Use `--no-topics` when running standalone
   `prepare` stages; `work next` uses the single deduplicated packet `HKIPO-MBxxxx.md`.
5. **Rate-limit-safe concurrency**: If the model runtime has tight RPM/TPM quotas,
   cap active leases with `run.py work next --config CONFIG --max-extract 3 --max-review 3 --max-total 4`
   to avoid lease timeouts and wasted tokens.

Publish results as a ZIP with `run.py bundle`, including coverage and gate reports.
Report actual issuers/dates, missing evidence, unresolved review, immature windows,
source limitations, and absolute artifact paths. Passing tests does not certify
all data. Keep raw sources and rollback snapshots local; preserve uncommitted
research and run cohort jobs sequentially where configs share output directories.
For code changes, follow CONTRIBUTING.md and run `make check-code` before a PR.
