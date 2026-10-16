---
name: hk-ipo-collect
description: >-
  Collect Hong Kong IPO data for a listing period end to end: plan quarters,
  install, collect Main Board and GEM, extract, independently review, resume,
  audit and deliver a ZIP. Use when the user names a period to collect or
  update (e.g. "2025Q4", "收集2025年下半年的港股IPO", "采集去年的新股"), asks
  to continue an earlier collection ("继续采集"), or hands over only this
  repository's link.
---

# One-sentence HK IPO collection

The user supplies a period; you deliver the best dataset the official sources
support. **Best** means every official issuer in the period, every supported
field backed by a page and quote, a real independent review of each payload,
and every gap named. Filled cells without evidence make a dataset worse.

Work through the steps in order. Each ends on a **done when** line.

## 1. Find the checkout

Use the current directory if it holds `run.py` and `.agents/skills/hk-ipo-collect/`.
Otherwise this skill's directory resolves through symlinks to
`<checkout>/.agents/skills/hk-ipo-collect`: use that checkout. Otherwise clone
`https://github.com/GZ-November/urop-hk-ipo.git` into a clean directory.
Run every later command from the checkout root.

**Done when** `python3 run.py plan --help` prints usage at the checkout root.

## 2. Pin the scope and plan

Translate the request into period terms. Resolve relative words against
today's date in Hong Kong (UTC+8).

| The user says | Term |
|---|---|
| 2025年第四季度 / 2025 Q4 | `2025Q4` |
| 2025年上半年 / 下半年 | `2025H1` / `2025H2` |
| 2025年 / 2025全年 | `2025` |
| 2025年11月 | `2025-11` |
| 2024年7月到2025年6月 | `2024-07..2025-06` |
| 2025年11月15日到2026年2月10日 | `2025-11-15..2026-02-10` |
| 上个季度, or only the repository link | `latest` |

Boards default to both. 主板 / Main Board only → `--board main`; GEM / 创业板
only → `--board gem`. The observation cutoff defaults to today in Hong Kong
unless the user names one. Ask a question only when the period itself is
ambiguous (for example "最近"); otherwise state your reading and continue.

```bash
python3 run.py plan 2025Q4            # add --board main|gem when restricted
```

Each job is one board × one calendar quarter. Tell the user, in their language,
the resolved interval, boards, cutoff and job list, then continue without
waiting for approval. A request to re-collect a `stored` quarter is the one
case to confirm first, since stored cohorts are canonical research data.

**Done when** the user has seen the plan and you hold its job list.

## 3. Install and verify

```bash
python3 tools/bootstrap.py --profile dev
.venv/bin/python run.py doctor --network
make check-code
```

Bootstrap installs the locked dependencies and links the project skills. If a
step fails, diagnose the cause (network, `venv` support, disk) and fix it;
report the exact failing stage when it is outside your control.

**Done when** doctor passes, or a named blocker is reported to the user.

## 4. Run the jobs, one at a time, in plan order

| Status | Action |
|---|---|
| `stored` | Run the printed audit command; reuse the cohort |
| `complete` | Nothing; it is already bundled |
| `future` | Report it; nothing has listed yet |
| `new`, `prepared`, `started`, `pending-review`, `failed` | Run the printed `python3 run.py start ...` command |

Rerunning the same `start` command resumes its cohort. Read its exit code:

- `0`: the job's cohort is collected, exported and zipped.
- `3`: extraction or independent review is pending. Do step 5, then rerun the
  same command. Repeat until `0`.
- `2`: source coverage or configuration error. An official report that does not
  yet cover the period is a **gap**, never evidence of zero IPOs. Report it,
  keep the requested interval, and move to the next job.
- `1`: read `START_HERE.html` in the job's run directory. Fix environmental
  causes (network, an open Excel file, a stale lock) and rerun once; report the rest.

**Done when** every job is `complete` or `stored`-and-audited, or carries a
named blocker.

## 5. Clear exit 3: extraction, then independent review

Exit 3 prints the cohort config. Drive the work with the scheduler instead of the
raw `work_orders.json`; it decides how many subagents to run, which issuer each
takes, and writes the one brief each subagent reads:

```bash
.venv/bin/python run.py work next --config CONFIG     # claim jobs, print briefs
.venv/bin/python run.py work status --config CONFIG   # read-only progress
```

GEM rules: [GEM pipeline](../../../docs/GEM_PIPELINE.md). Source rules:
[statutory evidence](references/statutory_evidentiary_rules.md).

**Reporting periods.** year-1 is the latest period of the audited Track
Record, the periods covered by the Accountants' Report and named in the
prospectus's "Track Record Period" definition. If that period is a stub (3M to
11M), year-1 is the stub: col_AT is the stub end, and balance-sheet fields use
that date. Unaudited figures outside the Track Record are never year-1. That
includes appendix quarterly results, "Recent Developments" and
post-track-record financial information, even when they are later. year-2 and
year-3 are the two complete Track Record years before year-1. Only
col_AH/AK/AN are annualised (×12/months). This follows the teacher's manual
§2.3: use the most recent data and annualise it when it is not a full year.
`run.py search periods CODE` applies this rule and `validate` enforces it.
When the command cannot decide, read the Track Record Period definition;
never derive periods by subtracting years. A justified departure goes in the
col_AT `note`, starting `period-override:` with the page, and the reviewer
confirms it.

**The loop.** Run `work next`. For every job it prints, start one NEW subagent
with fresh context and give it only the brief path; never hand a review to the
subagent that extracted that issuer, and never pass extractor notes to a
reviewer. Whenever a subagent returns, run `work next` again. Stop when it
reports every issuer reviewed, then rerun the step 4 command.

- An extract brief names the packets (self-contained: field list, units and
  rules), the payload paths, and the precomputed `search periods` and
  `search sharecap` results. The extractor writes the payloads and runs
  `work finish-extract --lease L`, which runs derive_allot, validate and
  `state extracted` for every target in order. On errors it fixes the payload
  from the source and reruns it.
- A review brief carries a sheet of every populated field with the text around
  its quote on the cited page. The reviewer checks meaning, units, period and
  consolidation, opens full pages when needed, searches the text for each
  missing field, writes one report per target starting
  `payload sha256: <value>`, and runs `work finish-review --lease L --verdict
  pass|fail [--failed-targets ...] --reviewer "<runtime> <model> review
  subagent, independent of extractor"`. The command refuses reports that do not
  name the current payload sha256. A failed target returns the issuer to
  extraction with the report as feedback, and a new reviewer reviews the
  corrected payload.
- A number must be read or computed from the cited page. Never solve for a
  value so that an identity holds: an unreadable value stays `NaN`.

**Concurrency is the scheduler's job.** Each lease lasts 90 minutes (extract) or
60 minutes (review). It starts at 4 extractors, 4 reviewers and 6 subagents in
total, dispatches reviews first, and takes the longest prospectuses first. A
lease that expires without a finish command halves that role's limit; a full
window of clean finishes adds one slot back, up to 6 per role and 8 in total.
Override with `--max-extract`, `--max-review` and `--max-total` when the
runtime allows fewer. Every mutating `run.py` stage takes a per-cohort lock, so
parallel finish commands queue instead of overwriting shared files. A subagent
that cannot finish runs `work release --lease L --reason "..."`.

A runtime without subagents cannot supply an independent reviewer: leave review
pending and deliver the prepared packets with a pending-review report.

**Partial write-back.** When the user wants reviewed issuers delivered before
every review finishes, add `--write-reviewed` to the `start` or `resume`
command; later resumes remember it. An issuer is written only when every one
of its targets validates and holds a current reviewed credential. Other rows
stay blank and are listed with reasons in `out/partial_writeback.json`. The
command still exits 3 until no issuer is pending, so report the delivery as
review-pending.

`.venv/bin/python run.py work status --config CONFIG` is the progress ledger. Its
phases come from the hash-bound state records, so a new session picks up from it
and long cohorts survive interruptions.

**Done when** `work status` shows every issuer `done` (a current extracted
credential and a real review verdict for every target), or the remaining
issuers are reported as pending review.

## 6. Deliver

For each cohort you collected, run `run.py audit --target all --config CONFIG`
and `run.py cross_check --config CONFIG`. Rerun `python3 run.py plan <terms>`
and execute its **Final delivery** bundle command, which picks an unused ZIP
name. Report in the user's language using the
[delivery report template](references/report_template.md).

**Done when** the ZIP exists and every section of the report template is filled
from audit, status and bundle output.

## Ground rules

- Evidence or missing: each written value has a source page and quote.
  Unsupported numbers stay `NaN`, unsupported text and dates `NA`, and zero
  appears only when the disclosure states zero.
- A review credential records a review that actually happened, of the exact
  current payload.
- Completion follows coverage, audit and review status. Passing tests show the
  code works, not that the data are correct.
- One writer per workbook at any time; jobs run sequentially.
- Raw PDFs, text caches and workbook snapshots stay local. Collection ends at
  delivery: commits, pushes and analysis runs happen only when the user asks.

Full operating manual: [AGENT_INSTRUCTIONS](../../../docs/AGENT_INSTRUCTIONS.md).
