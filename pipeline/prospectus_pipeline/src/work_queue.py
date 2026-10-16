"""Lease-based scheduler for parallel extraction and independent-review subagents.

The orchestrating agent no longer decides how many subagents to run or which issuer
each one takes. It loops on ``run.py work next``: each call expires dead leases,
adapts the concurrency limits, claims the next jobs and writes one self-contained brief
per job. Subagents finish with a single command (``work finish-extract`` /
``work finish-review``) that runs every gate in order under the cohort lock.

Issuer phases come from the hash-bound state records, so the queue survives restarts:
  extract  some target has no payload, an unrecorded payload, or a rejected review
  review   every target holds a current extracted credential, some lack a review
  done     every target holds a passing review of its current payload
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess
import sys
import uuid
from pathlib import Path

from boards import normalize_board
from cohort_lock import cohort_lock
from extraction_targets import target_paths
from state import file_hash, read_record, save_record
from storage import atomic_json

ROLES = ("extract", "review")
DEFAULT_LIMITS = {"extract": 4, "review": 4, "total": 6}
CEILINGS = {"extract": 6, "review": 6, "total": 8}
TTL_MINUTES = {"extract": 90, "review": 60}
EXCERPT = 350


# ------------------------------------------------------------------ paths and phases
def targets_for(cfg: dict) -> list[str]:
    gem = normalize_board(cfg.get("dataset", {}).get("board")) == "gem"
    return ["prospectus", "allot", "gem"] if gem else ["prospectus", "allot"]


def _stem(code: str) -> str:
    return "HKIPO-MB" + code.split(".")[0]


def payload_path(cfg: dict, target: str, code: str) -> Path:
    return target_paths(cfg, target)[1] / "extracted" / f"{_stem(code)}.json"


def packet_path(cfg: dict, target: str, code: str) -> Path:
    return Path(target_paths(cfg, target)[2]) / f"{_stem(code)}.md"


def handoff_dir(cfg: dict) -> Path:
    return Path(cfg["paths"]["out"]) / "agent_handoff"


def report_path(cfg: dict, target: str, code: str) -> Path:
    return handoff_dir(cfg) / f"{code}.{target}.review_report.md"


def queue_path(cfg: dict) -> Path:
    return handoff_dir(cfg) / "work_queue.json"


def target_state(cfg: dict, target: str, code: str) -> str:
    """missing | unrecorded | extracted | reviewed | rejected for the current payload bytes."""
    path = payload_path(cfg, target, code)
    if not path.is_file():
        return "missing"
    sha = file_hash(path)
    extracted = read_record(cfg, target, code, "extracted")
    if extracted.get("json_sha256") != sha or extracted.get("gate_pass") is not True:
        return "unrecorded"
    reviewed = read_record(cfg, target, code, "reviewed")
    if reviewed.get("json_sha256") == sha and reviewed.get("hash") == extracted.get("hash"):
        return "reviewed" if reviewed.get("verdict") == "pass" else "rejected"
    return "extracted"


def issuer_phase(states: dict[str, str]) -> str:
    if all(s == "reviewed" for s in states.values()):
        return "done"
    if any(s in {"missing", "unrecorded", "rejected"} for s in states.values()):
        return "extract"
    return "review"


# ------------------------------------------------------------------ queue file
def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _load(cfg: dict) -> dict:
    path = queue_path(cfg)
    queue = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    queue.setdefault("version", 1)
    queue.setdefault("limits", dict(DEFAULT_LIMITS))
    queue.setdefault("streak", {role: 0 for role in ROLES})
    queue.setdefault("leases", {})
    queue.setdefault("history", [])
    return queue


def _save(cfg: dict, queue: dict) -> None:
    queue["history"] = queue["history"][-500:]
    atomic_json(queue_path(cfg), queue)


def _close(queue: dict, lease_id: str, outcome: str, detail: str = "") -> dict:
    lease = queue["leases"].pop(lease_id)
    queue["history"].append({"lease": lease_id, "role": lease["role"], "code": lease["code"],
                             "outcome": outcome, "detail": detail, "at": _now().isoformat()})
    role, limits = lease["role"], queue["limits"]
    if outcome == "done":
        # Grow back one slot after a full window of clean completions.
        queue["streak"][role] = queue["streak"].get(role, 0) + 1
        if queue["streak"][role] >= limits[role]:
            limits[role] = min(CEILINGS[role], limits[role] + 1)
            queue["streak"][role] = 0
    elif outcome == "expired":
        # A silent subagent usually means the runtime is overloaded: halve the role.
        limits[role] = max(1, limits[role] // 2)
        queue["streak"][role] = 0
    elif outcome == "released":
        limits[role] = max(1, limits[role] - 1)
        queue["streak"][role] = 0
    return lease


def _apply_overrides(queue: dict, overrides: dict) -> None:
    for key, value in overrides.items():
        if value:
            queue["limits"][key] = max(1, min(int(value), CEILINGS[key]))


# ------------------------------------------------------------------ dispatch
def snapshot(cfg: dict, companies: list[dict]) -> dict[str, dict]:
    targets = targets_for(cfg)
    result = {}
    for company in companies:
        code = company["code"]
        states = {t: target_state(cfg, t, code) for t in targets}
        result[code] = {"name": company.get("name", ""), "states": states,
                        "phase": issuer_phase(states)}
    return result


def next_jobs(cfg: dict, companies: list[dict], overrides: dict | None = None,
              agent_command: str | None = None) -> dict:
    """Expire dead leases, claim the jobs that fit the limits and write their briefs."""
    claimed = []
    with cohort_lock(cfg):
        queue = _load(cfg)
        now = _now()
        expired = [lid for lid, lease in queue["leases"].items()
                   if dt.datetime.fromisoformat(lease["expires_at"]) <= now]
        for lid in expired:
            _close(queue, lid, "expired", "no finish command before the lease ran out")
        _apply_overrides(queue, overrides or {})
        snap = snapshot(cfg, companies)
        leased = {lease["code"] for lease in queue["leases"].values()}
        active = {role: sum(1 for x in queue["leases"].values() if x["role"] == role)
                  for role in ROLES}
        limits = queue["limits"]
        free_total = limits["total"] - sum(active.values())

        def candidates(phase):
            codes = [c for c, info in snap.items() if info["phase"] == phase and c not in leased]
            if phase == "extract":
                # Longest packets first shortens the cohort's wall-clock time.
                codes.sort(key=lambda c: -_packet_size(cfg, c))
            return codes

        for role, phase in (("review", "review"), ("extract", "extract")):
            room = min(limits[role] - active[role], free_total)
            for code in candidates(phase)[:max(0, room)]:
                lease_id = uuid.uuid4().hex[:10]
                targets = [t for t, s in snap[code]["states"].items()
                           if (s == "extracted" if role == "review" else True)]
                lease = {"role": role, "code": code, "targets": targets,
                         "issued_at": now.isoformat(),
                         "expires_at": (now + dt.timedelta(minutes=TTL_MINUTES[role])).isoformat()}
                queue["leases"][lease_id] = lease
                claimed.append((lease_id, lease))
                free_total -= 1
        _save(cfg, queue)
        active_after = dict(queue["leases"])
        limits_after = dict(queue["limits"])

    command = agent_command or _command(cfg)
    dispatch = []
    for lease_id, lease in claimed:
        writer = write_review_brief if lease["role"] == "review" else write_extract_brief
        brief = writer(cfg, lease_id, lease, snap[lease["code"]], command)
        dispatch.append({"role": lease["role"], "code": lease["code"], "lease": lease_id,
                         "targets": lease["targets"], "brief": str(brief),
                         "expires_at": lease["expires_at"]})
    phases = {p: sum(1 for x in snap.values() if x["phase"] == p) for p in ("extract", "review", "done")}
    done = phases["done"] == len(snap)
    return {"dispatch": dispatch, "expired": expired, "limits": limits_after,
            "active": [{"lease": k, **v} for k, v in active_after.items()],
            "phases": phases, "done": done}


def _packet_size(cfg: dict, code: str) -> int:
    path = packet_path(cfg, "prospectus", code)
    return path.stat().st_size if path.exists() else 0


def _command(cfg: dict) -> str:
    run = Path(cfg["_root"]) / "run.py"
    return f'"{sys.executable}" "{run}" --config "{cfg["_config_path"]}"'


# ------------------------------------------------------------------ finishing jobs
def _lease(queue: dict, lease_id: str, role: str) -> dict:
    lease = queue["leases"].get(lease_id)
    if lease is None:
        raise SystemExit(f"lease {lease_id} is not active (finished, released or expired); "
                         "ask the orchestrator for a new job with `work next`")
    if lease["role"] != role:
        raise SystemExit(f"lease {lease_id} is a {lease['role']} lease, not {role}")
    return lease


def finish_extract(cfg: dict, lease_id: str, derive, log=print) -> int:
    """derive_allot, then validate and record `extracted` for every target, in order."""
    from validate import validate_all
    with cohort_lock(cfg):
        queue = _load(cfg)
        lease = _lease(queue, lease_id, "extract")
        code = lease["code"]
        targets = targets_for(cfg)
        missing = [t for t in targets if not payload_path(cfg, t, code).is_file()]
        if missing:
            log(f"{code}: write these payloads first: "
                + ", ".join(str(payload_path(cfg, t, code)) for t in missing))
            return 1
        derive(code)
        problems, records = [], {}
        for target in targets:  # prospectus first: the allot context reads its col_M
            report = validate_all(cfg, only=[code], target=target, log=lambda *_: None)
            rec = next((r for r in report.get("records", []) if r.get("code") == code), {})
            records[target] = rec
            if rec.get("status") not in {"pass", "warning_missing"}:
                problems += [f"[{target}] {e}" for e in (rec.get("errors") or ["validation failed"])]
        if problems:
            lease["expires_at"] = (_now() + dt.timedelta(minutes=TTL_MINUTES["extract"])).isoformat()
            _save(cfg, queue)
            log(f"{code}: validation errors (lease kept; fix from the source and rerun):")
            for line in problems:
                log("  - " + line)
            return 1
        for target, rec in records.items():
            save_record(cfg, target, code, "extracted",
                        {**rec, "code": code, "target": target, "gate_pass": True})
        _close(queue, lease_id, "done")
        _save(cfg, queue)
    for target, rec in records.items():
        missing_fields = rec.get("fields_missing") or []
        log(f"RECORDED extracted {code} {target} {rec['hash'][:12]} "
            f"(missing {len(missing_fields)}, warnings {len(rec.get('warnings') or [])})")
    log(f"{code}: extraction finished; the orchestrator will dispatch an independent reviewer.")
    return 0


def finish_review(cfg: dict, lease_id: str, verdict: str, reviewer: str, note: str = "",
                  failed_targets: list[str] | None = None, log=print) -> int:
    """Check every report names the current payload sha256, then record the verdicts."""
    from validate import validate_all
    from tools.state import record_review
    if verdict not in {"pass", "fail"}:
        raise SystemExit("--verdict must be pass or fail")
    if not (reviewer or "").strip():
        raise SystemExit("--reviewer must name the actual independent reviewer")
    with cohort_lock(cfg):
        queue = _load(cfg)
        lease = _lease(queue, lease_id, "review")
        code = lease["code"]
        unknown = set(failed_targets or []) - set(lease["targets"])
        if unknown:
            raise SystemExit(f"--failed-targets not under review in this lease: {sorted(unknown)}")
        problems = []
        for target in lease["targets"]:
            report = report_path(cfg, target, code)
            sha = file_hash(payload_path(cfg, target, code))
            if not report.is_file():
                problems.append(f"missing report {report}")
            elif sha not in report.read_text(encoding="utf-8"):
                problems.append(f"{report.name} does not name the current payload sha256 {sha} "
                                "(the payload changed or the report is for another file)")
        if problems:
            for line in problems:
                log("  - " + line)
            return 1
        recorded = []
        for target in lease["targets"]:
            report = validate_all(cfg, only=[code], target=target, log=lambda *_: None)
            rec = next((r for r in report.get("records", []) if r.get("code") == code), {})
            failed = verdict == "fail" and (not failed_targets or target in failed_targets)
            try:
                record_review(cfg, target, code, rec, "fail" if failed else "pass", reviewer,
                              note, str(report_path(cfg, target, code)))
            except ValueError as exc:
                log(f"  - [{target}] {exc}; the payload changed after extraction, so the "
                    "extractor must finish again and a new review is needed")
                return 1
            recorded.append((target, "fail" if failed else "pass"))
        _close(queue, lease_id, "done", "; ".join(f"{t}={v}" for t, v in recorded))
        _save(cfg, queue)
    for target, result in recorded:
        log(f"RECORDED reviewed={result} {code} {target}")
    return 0


def release(cfg: dict, lease_id: str, reason: str = "", log=print) -> int:
    with cohort_lock(cfg):
        queue = _load(cfg)
        if lease_id not in queue["leases"]:
            log(f"lease {lease_id} is not active")
            return 1
        lease = _close(queue, lease_id, "released", reason)
        _save(cfg, queue)
    log(f"released {lease['role']} lease {lease_id} for {lease['code']}; it returns to the queue")
    return 0


# ------------------------------------------------------------------ briefs
PERIOD_RULE = """year-1 is the latest period in the Accountants' Report (the audited Track Record,
per the prospectus's "Track Record Period" definition), a full year or a 3-11 month stub;
col_AT is its end date. year-2/year-3 are the two complete financial years before year-1;
never derive them by subtraction. Unaudited figures outside the Accountants' Report
(appendix quarterly results, Recent Developments) are never year-1. Only net sales,
profit before tax and profit for the period (col_AH/AK/AN) are annualised (x12/months).
Assets, equity, liabilities, cash and interest-bearing debt take year-1-end values;
operating cash flow, R&D, gross profit and capex take year-1 original-period values."""


CONVENTIONS = """- col_AQ (over-allotment option %): when the prospectus has no over-allotment option
  but has an Offer Size Adjustment Option, record that option's size (for example
  0.15). Every stored cohort follows this; 0 only when neither option exists.
- Pre-IPO fields (col_pre_ipo_investors, col_earliest_round): "None" only when the
  prospectus explicitly states there was no pre-IPO investment; otherwise "NA".
  The shareholding history alone is not such a statement.
- Read each field's `hint` in the schema when the packet's field list is not enough."""


def _search(cfg: dict, *args: str, limit: int = 6000) -> str:
    tool = Path(cfg["_root"]) / "tools" / "search.py"
    env = {**os.environ, "PIPELINE_CONFIG": str(cfg["_config_path"])}
    try:
        out = subprocess.run([sys.executable, str(tool), *args], capture_output=True, text=True,
                             env=env, timeout=300, cwd=str(cfg.get("_ws") or Path(cfg["_root"]).parent))
        text = (out.stdout or out.stderr).strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        text = f"(unavailable: {exc})"
    return text if len(text) <= limit else text[:limit] + "\n... (truncated; run the command for the rest)"


def _brief_path(cfg: dict, code: str, role: str, lease_id: str) -> Path:
    path = handoff_dir(cfg) / "briefs" / f"{code}.{role}.{lease_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def write_extract_brief(cfg: dict, lease_id: str, lease: dict, info: dict, command: str) -> Path:
    code = lease["code"]
    rows = "\n".join(
        f"| {t} | `{packet_path(cfg, t, code)}` | `{payload_path(cfg, t, code)}` | "
        f"`{target_paths(cfg, t)[0]}` |" for t in targets_for(cfg))
    rejected = [t for t, s in info["states"].items() if s == "rejected"]
    feedback = ""
    if rejected:
        feedback = ("\n## Previous review rejected these targets\n"
                    + "\n".join(f"- {t}: read `{report_path(cfg, t, code)}` and correct the payload"
                                for t in rejected) + "\n")
    body = f"""# Extraction brief: {code} {info['name']} (lease {lease_id})

You are the extractor for this one issuer. Write one JSON payload per target, then run
the finish command. Shell commands below start with: {command}

| target | packet (read this) | write payload to | schema (only to resolve one field) |
|---|---|---|---|
{rows}

Each packet is self-contained: it holds the field list, units, output contract and hard
rules. Read the packet itself; open the schema, `workflows/*_extract.js` or the docs only
when a specific field is unclear. Locate pages with `search pages {code} 120-125` or
`search search {code} "REGEX" --context 3 --max 8` (both via `{command}`).
{feedback}
## Rules
- Extract from this issuer's packets and source pages only. Do not open, copy or start
  from any other payload, earlier extraction, workbook or export, in this cohort or any
  other directory: the review and the credentials certify a fresh reading of the source.
- Each populated field: value, page, short verbatim quote from that page, confidence.
  Unreadable or undisclosed: numeric "NaN", text/date "NA". Zero only when the
  disclosure states zero. Never solve a value so an identity balances.
- {PERIOD_RULE.replace(chr(10), chr(10) + '  ')}
- The workbook columns BC and CN/CO/CP are derived later, not extracted. The allotment
  fields col_CV/CK/CQ/DA are filled deterministically by the finish command.

## Dataset conventions
{CONVENTIONS}

## Precomputed: search periods {code}
```
{_search(cfg, "periods", code)}
```

## Precomputed: search sharecap {code}
```
{_search(cfg, "sharecap", code, limit=4000)}
```

## Finish
Run `{command} work finish-extract --lease {lease_id}`. It runs derive_allot, validates
every target and records the extracted credentials in the required order under the
cohort lock. If it prints errors, correct the payload from the source and run it again.
Do not run validate, state or derive_allot yourself; do not review your own payloads,
write the workbook or commit. If you cannot finish, run
`{command} work release --lease {lease_id} --reason "..."`.

Reply in at most 150 words: targets finished, fields left NaN/NA and why, and any
value whose reading was a judgement call.
"""
    path = _brief_path(cfg, code, "extract", lease_id)
    path.write_text(body, encoding="utf-8")
    return path


def _pages(path: Path) -> dict[int, str]:
    pages: dict[int, str] = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                pages[int(row["page"])] = row.get("text", "")
    return pages


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def excerpt(page_text: str, quote: str, width: int = EXCERPT) -> str | None:
    """Text around the quote on its page, whitespace-normalised, or None if not found."""
    text, q = _norm(page_text), _norm(quote)
    if not text or not q:
        return None
    pos = text.lower().find(q.lower()[:80])
    if pos < 0:
        return None
    start, end = max(0, pos - width), min(len(text), pos + len(q) + width)
    return ("..." if start else "") + text[start:end] + ("..." if end < len(text) else "")


def _warnings(cfg: dict, target: str, code: str) -> list:
    path = target_paths(cfg, target)[1] / "validation.json"
    if not path.exists():
        return []
    report = json.loads(path.read_text(encoding="utf-8"))
    rec = next((r for r in report.get("records", []) if r.get("code") == code), {})
    return rec.get("warnings") or []


def review_sheet(cfg: dict, code: str, targets: list[str]) -> str:
    stem = _stem(code)
    sources = {"prospectus": _pages(Path(cfg["paths"]["text"]) / f"{stem}.jsonl"),
               "allot": _pages(Path(cfg["paths"]["allot_text"]) / f"{stem}.jsonl")}
    out = []
    for target in targets:
        path = payload_path(cfg, target, code)
        schema = json.loads(Path(target_paths(cfg, target)[0]).read_text(encoding="utf-8"))
        headers = {f["key"]: f.get("header", "") for f in schema.get("fields", [])}
        fields = json.loads(path.read_text(encoding="utf-8")).get("fields", {})
        pages = sources["allot" if target == "allot" else "prospectus"]
        out.append(f"### {target}: payload sha256 {file_hash(path)}\n")
        warnings = _warnings(cfg, target, code)
        if warnings:
            out.append("Validation warnings to recompute and explain:\n```\n"
                       + json.dumps(warnings, ensure_ascii=False, indent=1)[:4000] + "\n```\n")
        missing = []
        for key in headers:
            entry = fields.get(key) if isinstance(fields.get(key), dict) else {}
            value = entry.get("value")
            if value in (None, "", "NaN", "NA"):
                missing.append(f"{key} {headers[key]}")
                continue
            source = entry.get("source")
            line = (f"- **{key}** {headers[key]} = `{value}` (p{entry.get('page')}, "
                    f"{entry.get('confidence', '?')})\n  quote: \"{_norm(entry.get('quote', ''))[:220]}\"")
            page = entry.get("page")
            if source == "greenshoe":
                line += f"\n  source: over-allotment exercise announcement ({_norm(entry.get('note', ''))[:160]})"
            elif source:
                line += f"\n  deterministic ({source}): {_norm(entry.get('note', ''))[:220]}"
            else:
                text = pages.get(int(page)) if str(page).isdigit() else None
                found = excerpt(text or "", entry.get("quote", ""))
                where = "allotment announcement" if target == "allot" else f"search pages {code} {page}-{page}"
                line += (f"\n  page text: {found}" if found else
                         f"\n  page text: (not located verbatim; open the page: {where})")
            out.append(line)
        if missing:
            out.append("\nMissing (confirm each is genuinely undisclosed by searching the full text):\n"
                       + "\n".join(f"- {m}" for m in missing))
        out.append("")
    return "\n".join(out)


def write_review_brief(cfg: dict, lease_id: str, lease: dict, info: dict, command: str) -> Path:
    code, targets = lease["code"], lease["targets"]
    stem = _stem(code)
    reports = "\n".join(f"- `{report_path(cfg, t, code)}`" for t in targets)
    body = f"""# Independent review brief: {code} {info['name']} (lease {lease_id})

You are an independent reviewer. You have not seen the extraction and must not look for
the extractor's notes or reasoning: judge the payloads only against the original
disclosures. Shell commands below start with: {command}

Original sources: prospectus PDF `{Path(cfg['paths']['pdf']) / (stem + '.pdf')}` (page text via
`search pages {code} N-M`), allotment announcement PDF in `{cfg['paths']['allot_pdf']}`.
Targets to review: {', '.join(targets)}.

The sheet below lists every populated field with the text around its quote on the cited
page; the pipeline already checked that each quote occurs in the source text. Your job:
is each value the right number for the field (meaning, units and multipliers, period,
consolidated not parent-only, initial versus final terms, net versus gross), and is each
missing field genuinely undisclosed (search the full text with
`search search {code} "REGEX"`)? Open the full page whenever an excerpt is not enough,
and report a discrepancy only after opening the cited page yourself.

Period standard: {PERIOD_RULE}

Dataset conventions (a value that breaks one is a discrepancy):
{CONVENTIONS}

## Reports (one per target)
{reports}
Each report starts with the line `payload sha256: <value shown in the sheet>`, then the
verdict, the fields you checked, every discrepancy (page and what the page says), the
arithmetic for each validation warning, and the judgement calls you accepted.

## Finish
`{command} work finish-review --lease {lease_id} --verdict pass --reviewer "<runtime> <model> review subagent, independent of extractor" --note "<one-line summary>"`
Use `--verdict fail --failed-targets <targets>` when any value is wrong; the issuer then
returns to extraction with your report. The command refuses unless every report exists
and names the current payload sha256. Do not edit payloads, write the workbook or commit.

Reply in at most 150 words: verdict per target and any discrepancies or judgement calls.

## Review sheet
{review_sheet(cfg, code, targets)}
"""
    path = _brief_path(cfg, code, "review", lease_id)
    path.write_text(body, encoding="utf-8")
    return path


# ------------------------------------------------------------------ status text
def describe(result: dict) -> str:
    lines = [f"phases: extract {result['phases']['extract']} | review {result['phases']['review']}"
             f" | done {result['phases']['done']}   limits: extract {result['limits']['extract']},"
             f" review {result['limits']['review']}, total {result['limits']['total']}"]
    if result.get("expired"):
        lines.append(f"expired leases (limits reduced): {', '.join(result['expired'])}")
    if result["dispatch"]:
        lines.append("Spawn one NEW subagent per job (fresh context; reviewers never reuse an extractor):")
        for job in result["dispatch"]:
            lines.append(f"  {job['role']:7s} {job['code']}  lease {job['lease']}  brief {job['brief']}")
    active = [a for a in result["active"] if a["lease"] not in {j["lease"] for j in result["dispatch"]}]
    if active:
        lines.append("Still running: " + ", ".join(f"{a['role']} {a['code']}" for a in active))
    if result["done"]:
        lines.append("All issuers reviewed. Rerun the same start/resume command to write back.")
    elif not result["dispatch"]:
        lines.append("Nothing to dispatch now: wait for a running subagent to finish, then run `work next` again.")
    return "\n".join(lines)
