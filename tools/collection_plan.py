#!/usr/bin/env python3
"""Turn a requested listing period into an ordered, resumable collection plan.

The plan splits the inclusive interval into calendar-quarter jobs per board,
marks quarters already stored as canonical cohorts or started in earlier runs,
and prints the exact start, audit and bundle commands. It only reads files; it
never downloads, collects, reviews or writes research data. Standard library
only, so it runs before bootstrap.

Period syntax (Hong Kong calendar dates, inclusive):
  2025          a calendar year          2025H2     a half year
  2025Q4        a calendar quarter       2025-11    a month
  2025-11-03    a single day             latest     latest completed quarter
  A..B          from the start of A through the end of B, e.g. 2024Q3..2025Q2
"""
from __future__ import annotations

import argparse
import calendar
import datetime as dt
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PIPE = ROOT / "pipeline" / "prospectus_pipeline"
HK = dt.timezone(dt.timedelta(hours=8))
PREFIX = {"main": "HKIPO-MB", "gem": "HKIPO-GEM"}
RUN_STATUS = {"WORK_PENDING": "pending-review", "ANALYSIS-READY": "complete", "FAILED": "failed"}


def hk_today() -> dt.date:
    return dt.datetime.now(HK).date()


def quarter_bounds(day: dt.date) -> tuple[dt.date, dt.date]:
    first_month = 3 * ((day.month - 1) // 3) + 1
    last_month = first_month + 2
    return (dt.date(day.year, first_month, 1),
            dt.date(day.year, last_month, calendar.monthrange(day.year, last_month)[1]))


def latest_completed_quarter(today: dt.date) -> tuple[dt.date, dt.date]:
    start, _ = quarter_bounds(today)
    return quarter_bounds(start - dt.timedelta(days=1))


def parse_term(term: str, today: dt.date) -> tuple[dt.date, dt.date]:
    """Resolve one period term to its inclusive first and last calendar day."""
    text = term.strip().upper().replace(" ", "")
    if text == "LATEST":
        return latest_completed_quarter(today)
    if re.fullmatch(r"\d{4}", text):
        year = int(text)
        return dt.date(year, 1, 1), dt.date(year, 12, 31)
    match = re.fullmatch(r"(\d{4})-?Q([1-4])", text)
    if match:
        year, quarter = int(match[1]), int(match[2])
        return quarter_bounds(dt.date(year, 3 * quarter, 1))
    match = re.fullmatch(r"(\d{4})-?H([12])", text)
    if match:
        year, half = int(match[1]), int(match[2])
        return (dt.date(year, 1, 1), dt.date(year, 6, 30)) if half == 1 else (dt.date(year, 7, 1), dt.date(year, 12, 31))
    match = re.fullmatch(r"(\d{4})-(\d{2})", text)
    if match:
        year, month = int(match[1]), int(match[2])
        if not 1 <= month <= 12:
            raise ValueError(f"Invalid month in period '{term}'.")
        return dt.date(year, month, 1), dt.date(year, month, calendar.monthrange(year, month)[1])
    try:
        day = dt.date.fromisoformat(text)
    except ValueError:
        raise ValueError(
            f"Unrecognized period '{term}'. Use 2025, 2025H2, 2025Q4, 2025-11, "
            "2025-11-03, latest, or A..B."
        ) from None
    return day, day


def parse_period(spec: str, today: dt.date) -> tuple[dt.date, dt.date]:
    """Resolve a period term or an A..B range to one inclusive interval."""
    if ".." in spec:
        left, _, right = spec.partition("..")
        start, end = parse_term(left, today)[0], parse_term(right, today)[1]
    else:
        start, end = parse_term(spec, today)
    if start > end:
        raise ValueError(f"Period '{spec}' starts after it ends.")
    return start, end


def merge_intervals(intervals: list[tuple[dt.date, dt.date]]) -> list[tuple[dt.date, dt.date]]:
    merged: list[tuple[dt.date, dt.date]] = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1] + dt.timedelta(days=1):
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def quarter_chunks(start: dt.date, end: dt.date) -> list[tuple[dt.date, dt.date]]:
    """Split an inclusive interval at calendar-quarter boundaries."""
    chunks = []
    cursor = start
    while cursor <= end:
        _, quarter_end = quarter_bounds(cursor)
        chunks.append((cursor, min(end, quarter_end)))
        cursor = quarter_end + dt.timedelta(days=1)
    return chunks


def board_key(value: str | None) -> str:
    return "gem" if "GEM" in str(value or "").upper() else "main"


def read_dataset_block(path: Path) -> dict[str, str]:
    """Read the flat `dataset:` mapping of a cohort config without requiring PyYAML."""
    values: dict[str, str] = {}
    inside = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^dataset:\s*(#.*)?$", line):
            inside = True
            continue
        if inside and line and not line[0].isspace() and not line.startswith("#"):
            break
        match = re.match(r"^\s+(\w+):\s*['\"]?([^'\"#]*?)['\"]?\s*(#.*)?$", line) if inside else None
        if match:
            values[match[1]] = match[2].strip()
    return values


def stored_cohorts(root: Path = ROOT) -> list[dict]:
    """List canonical cohort configs with their board and covered listing period."""
    cohorts = []
    for config in sorted((root / "pipeline" / "prospectus_pipeline").glob("config_*.yaml")):
        dataset = read_dataset_block(config)
        try:
            start = dt.date.fromisoformat(dataset["period_start"])
            end = dt.date.fromisoformat(dataset["period_end"])
        except (KeyError, ValueError):
            continue
        cohorts.append({"id": dataset.get("id", config.stem), "board": board_key(dataset.get("board")),
                        "period_start": start, "period_end": end, "config": config})
    return cohorts


def plan_job(board: str, start: dt.date, end: dt.date, today: dt.date,
             stored: list[dict], root: Path = ROOT) -> dict:
    """Classify one board/quarter job and choose its next command."""
    period_id = f"{start.isoformat()}_{end.isoformat()}"
    run_dir = root / "deliverables" / f"run_{board}_{period_id}"
    cohort_config = (root / "pipeline/prospectus_pipeline/datasets"
                     / f"HKIPO_{period_id}_{PREFIX[board]}" / "cohort.yaml")
    start_command = (f"python3 run.py start --board {board} "
                     f"--period-start {start.isoformat()} --period-end {end.isoformat()}")
    job = {"board": board, "period_start": start.isoformat(), "period_end": end.isoformat(),
           "run_dir": str(run_dir), "cohort_config": str(cohort_config), "command": start_command}
    covering = next((c for c in stored if c["board"] == board
                     and c["period_start"] <= start and end <= c["period_end"]), None)
    if start > today:
        job.update(status="future", command=None, cohort_config=None,
                   note="Starts after today in Hong Kong; nothing has listed yet.")
        return job
    if covering:
        config = covering["config"]
        wider = (covering["period_start"], covering["period_end"]) != (start, end)
        job.update(status="stored", cohort_config=str(config),
                   command=f".venv/bin/python run.py audit --target all --config {config.relative_to(root / 'pipeline').as_posix()}",
                   note=f"Reuse canonical cohort {covering['id']} "
                        f"({covering['period_start']}..{covering['period_end']})"
                        + ("; it is wider than requested, so select rows by listing date." if wider else "."))
        return job
    state_file = run_dir / "run_state.json"
    status = "new"
    if state_file.is_file():
        try:
            status = RUN_STATUS.get(json.loads(state_file.read_text(encoding="utf-8")).get("status"), "started")
        except (OSError, ValueError):
            status = "started"
    elif cohort_config.is_file():
        status = "prepared"
    job["status"] = status
    if status == "complete":
        job.update(command=None, note="Collection finished; included in the final bundle.")
    elif status == "failed":
        job["note"] = f"Read {run_dir / 'START_HERE.html'} and fix the cause before rerunning."
    elif status in ("pending-review", "prepared", "started"):
        job["note"] = "Rerunning the same start command resumes this cohort."
    if end >= today:
        job["note"] = (job.get("note", "") + " Period has not ended in Hong Kong; official listing reports "
                       "may not cover it yet, and a coverage failure is a gap, not zero IPOs.").strip()
    return job


def free_bundle_path(root: Path, label: str, today: dt.date) -> Path:
    base = root / "deliverables" / f"hkipo_{label}_{today.strftime('%Y%m%d')}"
    candidate = base.with_suffix(".zip")
    counter = 2
    while candidate.exists():
        candidate = base.parent / f"{base.name}-{counter}.zip"
        counter += 1
    return candidate


def build_plan(specs: list[str], boards: list[str], today: dt.date, root: Path = ROOT) -> dict:
    """Build the ordered job list, bundle command and maturity notes."""
    intervals = merge_intervals([parse_period(spec, today) for spec in specs])
    stored = stored_cohorts(root)
    jobs = [plan_job(board, start, end, today, stored, root)
            for interval in intervals for start, end in quarter_chunks(*interval) for board in boards]
    # Bundle only cohorts that exist; rerun the plan after collection to include new ones.
    bundle_configs = []
    for job in jobs:
        config = job.get("cohort_config")
        if config and Path(config).is_file() and config not in bundle_configs:
            bundle_configs.append(config)
    uncollected = [job for job in jobs if job.get("cohort_config") and not Path(job["cohort_config"]).is_file()]
    label = f"{intervals[0][0].isoformat()}_{intervals[-1][1].isoformat()}"
    bundle_path = free_bundle_path(root, label, today)

    def relative(path: str | Path) -> str:
        return Path(path).relative_to(root).as_posix()

    bundle_command = " ".join([".venv/bin/python run.py bundle",
                               *[f"--config {relative(config)}" for config in bundle_configs],
                               f"--output {relative(bundle_path)}"]) if bundle_configs else None
    six_months_ago = today - dt.timedelta(days=183)
    notes = [
        "Run jobs one at a time in the listed order; never run two writers on one workbook.",
        "Exit 3 means extraction or independent review is pending: complete the work orders, "
        "then rerun the same start command.",
        f"Observation cutoff defaults to {today.isoformat()} (today in Hong Kong). Return windows "
        "that have not elapsed stay missing; six-month windows are mature only for listings on or "
        f"before about {six_months_ago.isoformat()}.",
    ]
    if uncollected:
        notes.append(f"{len(uncollected)} job(s) have no cohort yet; rerun this plan after collection "
                     "to get the bundle command that includes them.")
    return {"today": today.isoformat(), "boards": boards,
            "intervals": [[s.isoformat(), e.isoformat()] for s, e in intervals],
            "jobs": jobs, "bundle_command": bundle_command, "notes": notes}


def render_text(plan: dict) -> str:
    intervals = ", ".join(f"{s}..{e}" for s, e in plan["intervals"])
    lines = [f"Collection plan for {intervals} | boards: {', '.join(plan['boards'])} | "
             f"Hong Kong today: {plan['today']}", ""]
    for number, job in enumerate(plan["jobs"], 1):
        lines.append(f"{number:>2}. [{job['status']}] {job['board']:<4} "
                     f"{job['period_start']}..{job['period_end']}")
        if job.get("command"):
            lines.append(f"      {job['command']}")
        if job.get("note"):
            lines.append(f"      {job['note']}")
    lines += ["", "Final delivery:", f"  {plan['bundle_command'] or 'nothing to bundle yet'}", "", "Notes:"]
    lines += [f"  - {note}" for note in plan["notes"]]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python3 run.py plan", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("period", nargs="*", help="One or more period terms; default: latest")
    parser.add_argument("--board", choices=("main", "gem", "both"), default="both")
    parser.add_argument("--today", help="Override Hong Kong today (YYYY-MM-DD) for reproducible plans")
    parser.add_argument("--json", action="store_true", help="Print the plan as JSON")
    args = parser.parse_args(argv)
    try:
        today = dt.date.fromisoformat(args.today) if args.today else hk_today()
        boards = ["main", "gem"] if args.board == "both" else [args.board]
        plan = build_plan(args.period or ["latest"], boards, today)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(plan, indent=2) if args.json else render_text(plan))
    return 0


if __name__ == "__main__":
    sys.exit(main())
