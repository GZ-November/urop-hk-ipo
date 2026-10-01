#!/usr/bin/env python3
"""Targeted lockup-column writeback for the 2026 cohort workbooks.

Writes only NLR columns 185-189 (controller 6M/12M expiry dates and the three
cornerstone unlock statistics) from the regenerated master panels, leaving every
other curated workbook column untouched. Workbooks are snapshotted first; the
change log is written alongside the other repair provenance. Run from the repo root.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PROSPECTUS = ROOT / "pipeline" / "prospectus_pipeline"
sys.path.insert(0, str(PROSPECTUS / "src"))
sys.path.insert(0, str(PROSPECTUS))

from cohort import load_cfg
from write_back_expansion import WorkbookExpansionWriter

COLUMNS = {185, 186, 187, 188, 189}
SNAPSHOTS = ROOT / "pipeline" / "reports" / "repair_handoff" / "snapshots"
LOG = ROOT / "pipeline" / "reports" / "repair_handoff" / "lockup_writeback_log.json"


def main() -> int:
    log = {}
    for q in ("2026q1", "2026q2", "2026q3"):
        cfg = load_cfg(config_path=PROSPECTUS / f"config_{q}.yaml")
        workbook = Path(cfg["_workbook_path"])
        SNAPSHOTS.mkdir(parents=True, exist_ok=True)
        snapshot = SNAPSHOTS / f"{workbook.name}.before-lockup-writeback"
        if not snapshot.exists():
            shutil.copy2(workbook, snapshot)
        writer = WorkbookExpansionWriter(cfg=cfg)
        changed = writer.write_expansion(columns=COLUMNS, force_overwrite=True, dry_run=False)
        log[q] = {"workbook": workbook.name, "cells_written": changed}
        print(f"{q}: {changed} cells written (columns 185-189)")
    LOG.write_text(json.dumps(log, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
