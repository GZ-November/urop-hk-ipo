# ==============================================================================
# HK IPO One-Command Generic-Agent Orchestrator
# ==============================================================================
"""One-command collection entry point, automatic bootstrapping, and safe resume."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from delivery_index import (  # noqa: E402
    generate_delivery_readme,
    generate_index_json,
    generate_start_here_html,
)


def latest_completed_hk_quarter(reference_date: dt.date | None = None) -> tuple[dt.date, dt.date, str]:
    """Calculate the latest completed calendar quarter in Hong Kong time (UTC+8).

    Across year boundaries:
      Q1 (Jan-Mar) -> previous year Q4 (Oct 1 - Dec 31)
      Q2 (Apr-Jun) -> same year Q1 (Jan 1 - Mar 31)
      Q3 (Jul-Sep) -> same year Q2 (Apr 1 - Jun 30)
      Q4 (Oct-Dec) -> same year Q3 (Jul 1 - Sep 30)
    """
    if reference_date is None:
        tz_hk = dt.timezone(dt.timedelta(hours=8))
        reference_date = dt.datetime.now(tz_hk).date()

    year = reference_date.year
    month = reference_date.month
    current_q = (month - 1) // 3 + 1

    if current_q == 1:
        prev_year = year - 1
        return dt.date(prev_year, 10, 1), dt.date(prev_year, 12, 31), f"{prev_year}Q4"
    elif current_q == 2:
        return dt.date(year, 1, 1), dt.date(year, 3, 31), f"{year}Q1"
    elif current_q == 3:
        return dt.date(year, 4, 1), dt.date(year, 6, 30), f"{year}Q2"
    else:  # current_q == 4
        return dt.date(year, 7, 1), dt.date(year, 9, 30), f"{year}Q3"


def validate_date_range(start_str: str | None, end_str: str | None) -> tuple[dt.date, dt.date]:
    """Validate explicit inclusive date range strings."""
    if start_str is None and end_str is None:
        raise ValueError("Both dates omitted; use latest_completed_hk_quarter instead.")
    if start_str is None or end_str is None:
        raise ValueError("Both --period-start and --period-end must be provided together.")

    try:
        start_date = dt.date.fromisoformat(start_str.strip())
    except ValueError:
        raise ValueError(f"Invalid --period-start date format '{start_str}'. Expected YYYY-MM-DD.")

    try:
        end_date = dt.date.fromisoformat(end_str.strip())
    except ValueError:
        raise ValueError(f"Invalid --period-end date format '{end_str}'. Expected YYYY-MM-DD.")

    if start_date > end_date:
        raise ValueError(
            f"Invalid date range: start date ({start_date.isoformat()}) "
            f"must be on or before end date ({end_date.isoformat()})."
        )

    return start_date, end_date


def board_choice(value: str | None) -> str:
    """Map CLI values and saved display names ("Main Board", "GEM") to main, gem or both."""
    text = (value or "both").strip().lower()
    if text == "both":
        return text
    return "gem" if "gem" in text else "main"


class RunLock:
    """Safe directory file-lock to prevent concurrent mutations using atomic O_CREAT | O_EXCL."""

    def __init__(self, run_dir: Path):
        self.run_dir = run_dir
        self.lock_file = run_dir / "run.lock"
        self.acquired = False

    def __enter__(self) -> "RunLock":
        self.run_dir.mkdir(parents=True, exist_ok=True)
        lock_data = json.dumps({
            "pid": os.getpid(),
            "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        }, indent=2) + "\n"

        for _ in range(2):
            try:
                fd = os.open(str(self.lock_file), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                with open(fd, "w", encoding="utf-8") as f:
                    f.write(lock_data)
                self.acquired = True
                return self
            except FileExistsError:
                existing_pid = 0
                try:
                    data = json.loads(self.lock_file.read_text(encoding="utf-8"))
                    existing_pid = int(data.get("pid", 0))
                except (ValueError, OSError):
                    pass

                if existing_pid > 0 and self._is_pid_alive(existing_pid):
                    raise RuntimeError(
                        f"Concurrency collision: run directory '{self.run_dir}' is currently "
                        f"locked by active process PID {existing_pid}."
                    )
                try:
                    self.lock_file.unlink(missing_ok=True)
                except OSError:
                    pass
        raise RuntimeError(f"Unable to acquire lock on '{self.run_dir}'.")

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self.acquired:
            self.lock_file.unlink(missing_ok=True)
            self.acquired = False

    @staticmethod
    def _is_pid_alive(pid: int) -> bool:
        if pid <= 0:
            return False
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False


def find_project_python(root: Path = ROOT) -> Path | None:
    """Locate an operational project Python virtual environment."""
    candidates = []
    if "HKIPO_PYTHON" in os.environ:
        candidates.append(Path(os.environ["HKIPO_PYTHON"]))
    candidates.append(root / (".venv/Scripts/python.exe" if os.name == "nt" else ".venv/bin/python"))
    if sys.executable:
        candidates.append(Path(sys.executable))

    for candidate in candidates:
        if candidate.is_file():
            try:
                res = subprocess.run(
                    [str(candidate), "-c", "import openpyxl, yaml, requests"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if res.returncode == 0:
                    return candidate
            except (subprocess.SubprocessError, OSError):
                continue
    return None


def ensure_bootstrap(
    root: Path = ROOT,
    profile: str = "core",
    runner: Callable[..., Any] = subprocess.run,
) -> Path:
    """Ensure locked dependencies are installed without modifying global Python."""
    existing = find_project_python(root)
    if existing:
        return existing

    bootstrap_script = root / "tools" / "bootstrap.py"
    if not bootstrap_script.is_file():
        raise RuntimeError(f"Bootstrap script missing at {bootstrap_script}")

    print(f"[*] Bootstrapping project environment with profile '{profile}'...", flush=True)
    res = runner(
        [sys.executable, str(bootstrap_script), "--profile", profile],
        cwd=root,
    )
    returncode = getattr(res, "returncode", 0)
    if returncode != 0:
        raise RuntimeError(f"tools/bootstrap.py failed with exit code {returncode}.")

    resolved = find_project_python(root)
    if not resolved:
        raise RuntimeError("Bootstrap succeeded but operational virtual environment was not detected.")
    return resolved


def resolve_cohort_paths(
    start: dt.date,
    end: dt.date,
    board: str = "main",
    root: Path = ROOT,
) -> tuple[Path, Path]:
    """Resolve standard cohort directory and config path."""
    board_clean = board.strip().lower()
    prefix = "HKIPO-GEM" if board_clean == "gem" else "HKIPO-MB"
    period_id = f"{start.isoformat()}_{end.isoformat()}"
    cohort_dir = root / "pipeline/prospectus_pipeline/datasets" / f"HKIPO_{period_id}_{prefix}"
    config_path = cohort_dir / "cohort.yaml"
    workbook_path = cohort_dir / f"{prefix}.xlsx"
    return workbook_path, config_path


def read_run_state(run_dir: Path) -> dict[str, Any] | None:
    """Load run_state.json if present."""
    state_file = run_dir / "run_state.json"
    if not state_file.is_file():
        return None
    try:
        return json.loads(state_file.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return None


def write_run_state(run_dir: Path, state: dict[str, Any]) -> None:
    """Save run_state.json atomically."""
    state_file = run_dir / "run_state.json"
    temp_file = run_dir / f"run_state.tmp.{os.getpid()}"
    state["updated_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    temp_file.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    temp_file.replace(state_file)


def render_run_artifacts(
    run_dir: Path,
    state: dict[str, Any],
    error_message: str | None = None,
) -> None:
    """Write START_HERE.html, index.json, and README.md into the run directory."""
    status = state.get("status", "WORK_PENDING")
    is_ready = bool(state.get("is_analysis_ready", False))
    cohort_id = state.get("cohort_id", "Requested_Cohort")
    board = state.get("board", "Main Board")
    start_str = state.get("period_start", "")
    end_str = state.get("period_end", "")
    issuers = state.get("issuers", 0)
    config_path = state.get("cohort_config")
    workbook_path = state.get("workbook_path")
    work_orders_path = state.get("work_orders_path")
    bundle_path = state.get("bundle_zip_path")
    resume_cmd = state.get("resume_command")

    # Build cohort descriptor for index generator
    cohort_desc = {
        "id": cohort_id,
        "board": board,
        "requested_period": [start_str, end_str],
        "issuers": issuers,
        "is_analysis_ready": is_ready,
        "workbook": workbook_path,
        "csv": state.get("clean_csv_path"),
        "codebook_md": state.get("codebook_md_path"),
        "codebook_json": state.get("codebook_json_path"),
        "audit_md": state.get("audit_md_path"),
        "status_json": state.get("status_json_path"),
        "evidence_dir": state.get("evidence_dir_path"),
        "audit_stats": state.get("audit_stats", {}),
        "companies": state.get("companies", []),
    }

    # Generate HTML
    html_content = generate_start_here_html(
        title=f"HK IPO Collection Run Status: {board} ({start_str} to {end_str})",
        status=status,
        is_analysis_ready=is_ready,
        cohorts=[cohort_desc],
        resume_command=resume_cmd,
        work_orders_path=work_orders_path,
        bundle_zip_path=bundle_path,
        error_message=error_message,
        is_bundle=False,
        base_dir=run_dir,
    )
    (run_dir / "START_HERE.html").write_text(html_content, encoding="utf-8")

    # Generate index.json
    index_dict = generate_index_json(
        title=f"HK IPO Collection Run Index: {board} ({start_str} to {end_str})",
        status=status,
        is_analysis_ready=is_ready,
        cohorts=[cohort_desc],
        base_dir=run_dir,
    )
    index_dict["run_metadata"] = {
        "cohort_config": str(config_path) if config_path else None,
        "work_orders_path": str(work_orders_path) if work_orders_path else None,
        "resume_command": resume_cmd,
    }
    (run_dir / "index.json").write_text(json.dumps(index_dict, indent=2) + "\n", encoding="utf-8")

    # Generate README.md
    readme_content = generate_delivery_readme(
        title=f"HK IPO Collection Run: {board} ({start_str} to {end_str})",
        status=status,
        is_analysis_ready=is_ready,
        cohorts=[cohort_desc],
        is_bundle=False,
        base_dir=run_dir,
    )
    (run_dir / "README.md").write_text(readme_content, encoding="utf-8")


def start_collection(
    args: argparse.Namespace,
    root: Path = ROOT,
    runner: Callable[..., Any] = subprocess.run,
) -> int:
    """Execute one-command collection workflow."""
    # 1. Resolve board
    board = board_choice(args.board)

    if board == "both":
        print("[*] Starting dual-board collection (Main Board + GEM)...", flush=True)
        import copy
        base_run_dir = Path(args.run_dir).resolve() if args.run_dir else None

        args_main = copy.copy(args)
        args_main.board = "main"
        if base_run_dir:
            args_main.run_dir = str(base_run_dir / "main")
        rc_main = start_collection(args_main, root=root, runner=runner)

        args_gem = copy.copy(args)
        args_gem.board = "gem"
        if base_run_dir:
            args_gem.run_dir = str(base_run_dir / "gem")
        rc_gem = start_collection(args_gem, root=root, runner=runner)

        if rc_main != 0 and rc_main != 3:
            return rc_main
        if rc_gem != 0 and rc_gem != 3:
            return rc_gem
        if rc_main == 3 or rc_gem == 3:
            return 3
        return 0

    # 2. Resolve listing-date interval
    if args.period_start or args.period_end:
        start_date, end_date = validate_date_range(args.period_start, args.period_end)
        quarter_label = f"{start_date.isoformat()} to {end_date.isoformat()}"
    else:
        start_date, end_date, quarter_label = latest_completed_hk_quarter()
        print(
            f"[*] Dates omitted: defaulting to latest completed Hong Kong calendar quarter: "
            f"{quarter_label} ({start_date.isoformat()} to {end_date.isoformat()}) on {board.upper()}.",
            flush=True,
        )

    # 3. Resolve run directory
    period_id = f"{start_date.isoformat()}_{end_date.isoformat()}"
    prefix = "HKIPO-GEM" if board == "gem" else "HKIPO-MB"
    default_run_dir = root / "deliverables" / f"run_{board}_{period_id}"
    run_dir = Path(args.run_dir or default_run_dir).resolve()
    run_dir.mkdir(parents=True, exist_ok=True)

    # 4. Acquire file lock
    with RunLock(run_dir):
        # 5. Check existing state for reuse/mismatch
        existing_state = read_run_state(run_dir)
        workbook_path, cohort_config = resolve_cohort_paths(start_date, end_date, board, root)

        if existing_state:
            prev_board = board_choice(existing_state["board"]) if existing_state.get("board") else ""
            prev_start = existing_state.get("period_start", "")
            prev_end = existing_state.get("period_end", "")
            if (prev_board and prev_board != board) or (
                prev_start and prev_start != start_date.isoformat()
            ) or (prev_end and prev_end != end_date.isoformat()):
                raise ValueError(
                    f"Run directory '{run_dir}' is already configured for cohort "
                    f"[{prev_board}] {prev_start} to {prev_end}. "
                    "Cannot overwrite with a different cohort. Choose another --run-dir."
                )

        # 6. Ensure project python
        if not getattr(args, "no_bootstrap", False):
            py = ensure_bootstrap(root=root, profile=args.profile or "core", runner=runner)
        else:
            py = find_project_python(root)
            if not py:
                raise RuntimeError("Auto-bootstrap disabled (--no-bootstrap) and project python not found.")

        # 7. Execute collection stage
        collect_cmd = [str(py), str(root / "run.py"), "collect"]
        if cohort_config.is_file() and workbook_path.is_file():
            collect_cmd.extend(["--config", str(cohort_config), "--workbook", str(workbook_path)])
        elif cohort_config.is_file():
            collect_cmd.extend([
                "--config", str(cohort_config),
                "--period-start", start_date.isoformat(),
                "--period-end", end_date.isoformat(),
            ])
        else:
            collect_cmd.extend([
                "--board", board,
                "--period-start", start_date.isoformat(),
                "--period-end", end_date.isoformat(),
            ])

        write_reviewed = bool(getattr(args, "write_reviewed", False) or (existing_state or {}).get("write_reviewed"))
        if write_reviewed:
            collect_cmd.append("--write-reviewed")

        print(f"[*] Executing pipeline collection: {' '.join(collect_cmd)}", flush=True)
        collect_proc = runner(collect_cmd, cwd=root)
        rc = getattr(collect_proc, "returncode", 1)

        cohort_id = f"HKIPO_{period_id}_{prefix}"
        cohort_dir = root / "pipeline/prospectus_pipeline/datasets" / cohort_id

        # Resolve work orders file dynamically from cohort config or candidate paths
        work_orders_file = None
        if cohort_config.is_file():
            try:
                import yaml
                cfg_data = yaml.safe_load(cohort_config.read_text(encoding="utf-8"))
                out_rel = cfg_data.get("paths", {}).get("out", "out")
                candidate_wo = (cohort_config.parent / out_rel / "agent_handoff" / "work_orders.json").resolve()
                if candidate_wo.is_file():
                    work_orders_file = candidate_wo
            except Exception:
                pass
        if not work_orders_file:
            for candidate in [
                cohort_dir / "out" / "agent_handoff" / "work_orders.json",
                cohort_dir / "gem" / "out" / "agent_handoff" / "work_orders.json",
                root / "pipeline/prospectus_pipeline/out/agent_handoff" / "work_orders.json",
            ]:
                if candidate.is_file():
                    work_orders_file = candidate
                    break
        if not work_orders_file:
            work_orders_file = cohort_dir / "out" / "agent_handoff" / "work_orders.json"
        resume_cmd = f"python3 run.py resume --run-dir {run_dir}"

        # Initialize or update state dictionary
        state = existing_state or {}
        state.update({
            "cohort_id": cohort_id,
            "board": "GEM" if board == "gem" else "Main Board",
            "period_start": start_date.isoformat(),
            "period_end": end_date.isoformat(),
            "cohort_config": str(cohort_config),
            "workbook_path": str(workbook_path),
            "work_orders_path": str(work_orders_file) if work_orders_file.exists() else None,
            "resume_command": resume_cmd,
            "exit_code": rc,
            "write_reviewed": write_reviewed,
        })
        partial_manifest = (work_orders_file.parent.parent / "partial_writeback.json"
                            if work_orders_file else None)
        if write_reviewed and partial_manifest is not None and partial_manifest.is_file():
            try:
                partial = json.loads(partial_manifest.read_text(encoding="utf-8"))
                state["partial_writeback"] = {"manifest": str(partial_manifest),
                                              "written": len(partial.get("written", [])),
                                              "pending": len(partial.get("pending", {}))}
            except (OSError, ValueError):
                pass

        if rc == 3:
            # Work pending: formal extraction or independent review required
            state["status"] = "WORK_PENDING"
            state["is_analysis_ready"] = False
            write_run_state(run_dir, state)
            render_run_artifacts(run_dir, state)

            print("\n" + "=" * 70)
            print(">>> [WORK PENDING] Extraction and independent review are required.")
            print("=" * 70)
            print(f"Cohort config: {cohort_config}")
            if work_orders_file.exists():
                print(f"Work orders:   {work_orders_file}")
            print(f"Status report: {run_dir / 'START_HERE.html'}")
            if state.get("partial_writeback"):
                info = state["partial_writeback"]
                print(f"Partial write-back: {info['written']} reviewed issuer(s) written, "
                      f"{info['pending']} pending -> {info['manifest']}")
                print("  A review-pending snapshot can be exported and bundled now; pending rows stay blank.")
            work_cmd = f'{shlex.quote(sys.executable)} run.py work next --config {shlex.quote(str(cohort_config))}'
            print("\nAgent next steps:")
            print("  1. Loop on the scheduler; it says how many subagents to start and gives each a brief:")
            print(f"     {work_cmd}")
            print("  2. Start one NEW subagent per dispatched job with its brief; each finishes with")
            print("     `work finish-extract` or `work finish-review`. Rerun `work next` whenever one returns.")
            print("  3. When `work next` reports every issuer reviewed, resume with the exact command:")
            print(f"     {resume_cmd}")
            print("=" * 70 + "\n")
            return 3

        elif rc == 0:
            # Collection complete: export clean CSV and bundle deliverables
            print("[*] Collection gates passed. Exporting cohort deliverables...", flush=True)
            export_proc = runner(
                [str(py), str(root / "run.py"), "export", "--config", str(cohort_config)],
                cwd=root,
            )
            export_rc = getattr(export_proc, "returncode", 1)
            if export_rc != 0:
                state["status"] = "FAILED"
                state["is_analysis_ready"] = False
                write_run_state(run_dir, state)
                render_run_artifacts(run_dir, state, error_message=f"Export failed with exit code {export_rc}")
                return export_rc

            bundle_zip = run_dir / f"hkipo_{board}_{period_id}.zip"
            if bundle_zip.exists():
                bundle_zip.unlink()

            print(f"[*] Packaging delivery archive into {bundle_zip}...", flush=True)
            bundle_proc = runner(
                [
                    str(py), str(root / "tools" / "bundle_data.py"),
                    "--config", str(cohort_config),
                    "--output", str(bundle_zip),
                ],
                cwd=root,
            )
            bundle_rc = getattr(bundle_proc, "returncode", 1)
            if bundle_rc != 0:
                state["status"] = "FAILED"
                state["is_analysis_ready"] = False
                write_run_state(run_dir, state)
                render_run_artifacts(run_dir, state, error_message=f"Bundle failed with exit code {bundle_rc}")
                return bundle_rc

            state["status"] = "ANALYSIS-READY"
            state["is_analysis_ready"] = True
            state["bundle_zip_path"] = str(bundle_zip)
            write_run_state(run_dir, state)
            render_run_artifacts(run_dir, state)

            print("\n" + "=" * 70)
            print(">>> [COLLECTION COMPLETE] Dataset verified and analysis-ready.")
            print("=" * 70)
            print(f"Delivery ZIP:  {bundle_zip}")
            print(f"Status report: {run_dir / 'START_HERE.html'}")
            print("=" * 70 + "\n")
            return 0

        else:
            # Hard error or official coverage failure
            state["status"] = "FAILED"
            state["is_analysis_ready"] = False
            write_run_state(run_dir, state)
            render_run_artifacts(run_dir, state, error_message=f"Pipeline collect stage failed with exit code {rc}")
            print(f"\n[!] Pipeline collection failed with exit code {rc}. No fake success produced.", file=sys.stderr)
            return rc


def resume_collection(
    args: argparse.Namespace,
    root: Path = ROOT,
    runner: Callable[..., Any] = subprocess.run,
) -> int:
    """Resume a previous collection run after extraction/review completion."""
    run_dir = Path(args.run_dir).resolve() if args.run_dir else None
    if not run_dir:
        # Search for latest run_dir under deliverables
        deliv = root / "deliverables"
        if deliv.is_dir():
            candidates = sorted(deliv.glob("run_*"), key=os.path.getmtime, reverse=True)
            if candidates:
                run_dir = candidates[0].resolve()

    if not run_dir or not run_dir.is_dir():
        raise ValueError("No valid --run-dir found to resume. Specify --run-dir explicitly.")

    state = read_run_state(run_dir)
    if not state or not state.get("cohort_config"):
        raise ValueError(f"No usable run_state.json found in {run_dir}.")

    cohort_config = Path(state["cohort_config"])
    if not cohort_config.is_file():
        raise FileNotFoundError(f"Preserved cohort configuration missing at {cohort_config}")

    # Re-run collection using start_collection with preserved config parameters
    args.board = state.get("board", "main")
    args.period_start = state.get("period_start")
    args.period_end = state.get("period_end")
    args.run_dir = str(run_dir)
    return start_collection(args, root=root, runner=runner)


def build_parser() -> argparse.ArgumentParser:
    """Build unified argument parser for start and resume commands."""
    parser = argparse.ArgumentParser(
        prog="python run.py",
        description="One-command HK IPO collection entry point for tool-capable agents.",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Command mode")

    # 'start' command parser
    p_start = subparsers.add_parser("start", help="Bootstrap and start Main Board/GEM collection")
    p_start.add_argument("--board", choices=["main", "gem", "both"], default="both",
                         help="Listing board (main, gem, or both; default: both)")
    p_start.add_argument("--period-start", default=None,
                         help="Inclusive start listing date (YYYY-MM-DD)")
    p_start.add_argument("--period-end", default=None,
                         help="Inclusive end listing date (YYYY-MM-DD)")
    p_start.add_argument("--run-dir", default=None,
                         help="Reusable run and output directory")
    p_start.add_argument("--profile", choices=["core", "analysis", "dev"], default="core",
                         help="Dependency installation profile (default: core)")
    p_start.add_argument("--write-reviewed", action="store_true",
                          help="Write back issuers whose every target passed independent review; "
                               "keep the rest blank and pending (remembered for later resumes)")
    p_start.add_argument("--no-bootstrap", action="store_true",
                         help="Skip automatic bootstrapping")
    p_start.add_argument("--resume", action="store_true",
                         help="Resume from previous run state in --run-dir")

    # 'resume' command parser
    p_resume = subparsers.add_parser("resume", help="Resume collection after extraction/review")
    p_resume.add_argument("--run-dir", default=None,
                          help="Reusable run directory containing run_state.json")
    p_resume.add_argument("--profile", choices=["core", "analysis", "dev"], default="core",
                          help="Dependency installation profile")
    p_resume.add_argument("--write-reviewed", action="store_true",
                          help="Write back issuers whose every target passed independent review; "
                               "keep the rest blank and pending (remembered for later resumes)")
    p_resume.add_argument("--no-bootstrap", action="store_true")

    return parser


def main(argv: list[str] | None = None, runner: Callable[..., Any] = subprocess.run) -> int:
    """CLI entry point callable before any project dependencies exist."""
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()
    # Normalize command invocation: 'start' or 'resume' as first argument
    if not argv:
        argv = ["start"]
    elif argv[0] not in ("start", "resume"):
        argv = ["start", *argv]

    args = parser.parse_args(argv)

    try:
        if args.subcommand == "resume" or getattr(args, "resume", False):
            return resume_collection(args, runner=runner)
        return start_collection(args, runner=runner)
    except (ValueError, FileNotFoundError, RuntimeError) as exc:
        print(f"[!] Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
