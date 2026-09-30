#!/usr/bin/env python3
"""Blank "first 6M" daily-window statistics for issuers whose 6-month window has not matured.

Amihud, zero-volume days, daily volatility and maximum drawdown are defined over a matured
Month_6 window (see src/expansion_mapping.py). Older writebacks filled them from a few days of
bars, so they cannot be read as 6-month statistics. The expansion writer cannot repair this: it
regenerates from the Q1-only event tables and refuses to clear curated cells. This tool clears
only these four columns, and only where the issuer's own 6-month BHR cell is empty.

Usage (from pipeline/):
    python3 prospectus_pipeline/tools/blank_immature_window_stats.py --config prospectus_pipeline/config_2026q2.yaml [--dry-run]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from workbook_transaction import workbook_transaction  # noqa: E402

STAT_HEADERS = [
    "Amihud illiquidity (6M mean)",
    "Zero-volume days count (first 6M)",
    "Return volatility (first 6M daily std dev, %)",
    "Maximum drawdown (first 6M, %)",
]
MATURITY_HEADER = "6-month BHR from Day-1 close (%)"


def _norm(value) -> str:
    return " ".join(str(value or "").split()).lower()


def immature_cells(ws) -> list[tuple[int, int]]:
    """(row, column) of stat cells that hold a value although the row's 6-month BHR is empty."""
    header = {_norm(c.value): c.column for c in ws[1] if c.value}
    missing = [h for h in [MATURITY_HEADER, *STAT_HEADERS] if _norm(h) not in header]
    if missing:
        raise ValueError(f"Workbook lacks required headers: {missing}")
    maturity_col = header[_norm(MATURITY_HEADER)]
    stat_cols = [header[_norm(h)] for h in STAT_HEADERS]
    cells = []
    for row in range(2, ws.max_row + 1):
        if ws.cell(row, maturity_col).value not in (None, ""):
            continue
        cells += [(row, col) for col in stat_cols if ws.cell(row, col).value not in (None, "")]
    return cells


def main() -> int:
    from cohort import load_cfg
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    cfg = load_cfg(None, None, None, config_path=args.config)
    with workbook_transaction(cfg["_workbook_path"], operation="blank_immature_window_stats", dry_run=args.dry_run) as wb:
        ws = wb[cfg["sheet"]]
        cells = immature_cells(ws)
        print(f"{len(cells)} stale cell(s) in {Path(cfg['_workbook_path']).name}" + (" (dry run, not written)" if args.dry_run else ""))
        if not args.dry_run:
            for row, col in cells:
                ws.cell(row, col).value = None
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
