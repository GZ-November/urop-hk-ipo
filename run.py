#!/usr/bin/env python3
"""HK IPO Pipeline - Unified Root CLI Entry Point.

Provides a clean, direct command-line interface to the entire pipeline
without requiring callers to navigate deep into subdirectories.

Usage Examples:
    python run.py status
    python run.py audit --target all
    python run.py cross_check
    python run.py report
    python run.py export
    python run.py find --only 6082.HK
    python run.py --help
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PIPELINE_DIR = ROOT / "Data Collecting Pipeline"
PIPELINE_RUN = PIPELINE_DIR / "prospectus_pipeline" / "run.py"
WEEKLY_REPORT_SCRIPT = PIPELINE_DIR / "reports" / "build_weekly_report.py"


def main() -> None:
    args = sys.argv[1:]

    # Dedicated target for building the research progress Word document
    if args and args[0] in ("report-weekly", "weekly-report"):
        if not WEEKLY_REPORT_SCRIPT.exists():
            sys.stderr.write(f"Error: Weekly report script not found at {WEEKLY_REPORT_SCRIPT}\n")
            sys.exit(1)
        res = subprocess.run([sys.executable, str(WEEKLY_REPORT_SCRIPT)] + args[1:], cwd=PIPELINE_DIR)
        sys.exit(res.returncode)

    if not PIPELINE_RUN.exists():
        sys.stderr.write(f"Error: Pipeline runner not found at {PIPELINE_RUN}\n")
        sys.exit(1)

    cmd = [sys.executable, str(PIPELINE_RUN)] + args
    try:
        res = subprocess.run(cmd, cwd=PIPELINE_DIR)
        sys.exit(res.returncode)
    except KeyboardInterrupt:
        sys.stderr.write("\nProcess interrupted by user.\n")
        sys.exit(130)


if __name__ == "__main__":
    main()
