# Repository Organization and Maintenance

## Artifact Placement

| Artifact | Location | Maintenance rule |
|---|---|---|
| Pipeline code and CLI | `run.py`, `pipeline/prospectus_pipeline/src/`, `tools/` | Follow the shared path and field contracts |
| Research code and tests | `analysis/`, `analysis/tests/` | One clear entry point per study; update the analysis index |
| Workbooks, exports and evidence | `pipeline/cohorts/`, `exports/`, `prospectus_pipeline/data/`, `out/` | Preserve provenance and review gates; generated exports remain traceable |
| Tables, figures and research reports | `analysis/out/<module>/` | Generate from code; retain samples, diagnostics and manifests |
| Methods and research navigation | `docs/` | Link reports and state sample, cutoff and exploratory status |
| Superseded narratives | `docs/archive/<reason>/` | Preserve original content with a dated status note |
| Source reconciliation and repair records | `pipeline/reports/` | Retain evidence references and observation dates |
| Unverified candidates | Explicit `UNVERIFIED` artifacts | Keep separate from accepted research inputs |
| Project skills | `.agents/skills/` | Version project instructions and their supporting resources |
| Temporary scripts, logs and caches | Ignored locations such as `pipeline/scratch/` | Promote only reviewed, maintained work to the canonical tree |

Public-disclosure CSVs, JSON extraction evidence, workbooks and reports are intentional research artifacts. Do not delete files by extension to make the repository smaller. Original PDFs, full-text packets, isolated collection workspaces and workbook backups follow `.gitignore` and the contribution guide.

## Current Research Snapshot

The latest offering studies use 113 issuers through 30 September 2026. Their reports and table headings are English; verbatim source categories remain unchanged. The master can retain historical cohorts, while each study explicitly selects its population. Model-level complete cases do not change the overall population count.

Dated source reviews and earlier research designs may refer to 106 issuers or earlier repairs. Preserve that historical scope and link current output rather than silently rewriting evidence history. A manifest verifies file bytes, not the semantic correctness of every observation.

## Checkouts and Branches

Inspect the current checkout before integrating changes:

```bash
pwd
git status --short
git log -1 --oneline
git worktree list
```

Use a `codex/` topic branch for reviewable changes. Reuse a suitable checkout; do not copy or discard another checkout's uncommitted work. Workbooks should have one active writer per checkout. Keep old worktrees and research branches until their contents have been intentionally preserved or archived.

## Verification and Cleanup

- Check documentation links and run `git diff --check`.
- Run `make check-code` for maintained code, tests and registry consistency.
- Regenerate the affected analysis module when its behavior changes.
- Keep source refresh, source audits and code tests distinct in completion claims.
- Stage intentional files and inspect the staged summary before committing.
- Remove only regenerable runtime caches during routine cleanup. Preserve canonical datasets, evidence, sample logs, bootstrap diagnostics and historical outputs.

New research commits should contain code, design, generated results and sample records together. Cite the source literature in the methods note and describe final behavior in the pull request, rather than recounting the chat history.
