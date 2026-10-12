#!/usr/bin/env python3
"""Install locked dependencies and managed Python without changing global Python."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parents[1]
UV_VERSION = "0.12.19"


def environment_python(directory: Path) -> Path:
    return directory / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def run(command: list[str]) -> None:
    print("Running:", subprocess.list2cmdline(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("core", "analysis", "dev"), default="dev",
                        help="dev includes collection, analysis and verification dependencies")
    parser.add_argument("--python", default="3.12", help="Managed project Python version")
    parser.add_argument("--check", action="store_true", help="Also run make check-code (requires make)")
    args = parser.parse_args()
    if sys.version_info < (3, 9):
        parser.error("Bootstrap requires an existing Python 3.9+; uv installs project Python afterward.")
    # A separate tools environment prevents uv sync from removing its own installer.
    installer = ROOT / ".bootstrap"
    installer_python = environment_python(installer)
    if not installer_python.exists():
        venv.EnvBuilder(with_pip=True).create(installer)
    result = subprocess.run([str(installer_python), "-m", "uv", "--version"],
                            capture_output=True, text=True)
    if result.returncode or result.stdout.split()[:2] != ["uv", UV_VERSION]:
        run([str(installer_python), "-m", "pip", "install", f"uv=={UV_VERSION}"])
    uv = [str(installer_python), "-m", "uv"]
    # --locked refuses stale metadata; --frozen would silently trust an obsolete lock.
    sync = uv + ["sync", "--locked", "--python", args.python]
    if args.profile in ("analysis", "dev"):
        sync += ["--extra", "analysis"]
    if args.profile == "dev":
        sync += ["--extra", "dev"]
    run(sync)
    python = str(environment_python(ROOT / ".venv"))
    run([python, str(ROOT / "tools/doctor.py"), "--profile", args.profile])
    if args.check:
        if args.profile != "dev":
            parser.error("--check requires --profile dev")
        run(["make", "check-code", f"PYTHON={python}"])
    print("Setup complete. Use:", python, "run.py --help")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (subprocess.CalledProcessError, OSError) as exc:
        print(f"Setup failed: {exc}. Check network, disk space and Python venv support.", file=sys.stderr)
        raise SystemExit(1)
