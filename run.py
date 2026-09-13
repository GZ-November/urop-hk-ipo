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
NEWS_DIR = ROOT / "Data Collecting Templates" / "News"
PIPELINE_RUN = NEWS_DIR / "prospectus_pipeline" / "run.py"


def main() -> None:
    if not PIPELINE_RUN.exists():
        sys.stderr.write(f"Error: Pipeline runner not found at {PIPELINE_RUN}\n")
        sys.exit(1)

    cmd = [sys.executable, str(PIPELINE_RUN)] + sys.argv[1:]
    try:
        res = subprocess.run(cmd, cwd=NEWS_DIR)
        sys.exit(res.returncode)
    except KeyboardInterrupt:
        sys.stderr.write("\nProcess interrupted by user.\n")
        sys.exit(130)


if __name__ == "__main__":
    main()
