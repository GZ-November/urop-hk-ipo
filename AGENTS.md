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

Collection exit 3 means extraction/independent review pending: read the generated
work orders, complete supported tasks, and resume the same collection command.
Use an independent reviewer with original-source access. A credential requires
a real review of the exact payload; preserve pending review when the runtime
cannot supply an independent reviewer. Do not fabricate a passing sign-off.

Publish results as a ZIP with `run.py bundle`, including coverage and gate reports.
Report actual issuers/dates, missing evidence, unresolved review, immature windows,
source limitations, and absolute artifact paths. Passing tests does not certify
all data. Keep raw sources and rollback snapshots local; preserve uncommitted
research and run cohort jobs sequentially where configs share output directories.
For code changes, follow CONTRIBUTING.md and run `make check-code` before a PR.
