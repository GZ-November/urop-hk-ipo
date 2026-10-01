#!/usr/bin/env python3
"""Regenerate the 2026 master panels with the evidence-bound lockup contracts.

Runs Market/Stabilization/Lockup engines over all 106 stored 2026 issuers into an
isolated scratch directory, diffs the result against out/master, and — only with
--commit — replaces the production master CSVs. The market and stabilization
regeneration must reproduce the already-reviewed scratch recalculation; the lockup
panel is the only one expected to differ materially (document-derived dates).
"""
from __future__ import annotations

import csv
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PROSPECTUS = ROOT / "pipeline" / "prospectus_pipeline"
sys.path.insert(0, str(PROSPECTUS / "src"))
sys.path.insert(0, str(PROSPECTUS))

from cohort import load_cfg
from lockup_panel import LockupPanelEngine
from market_panel import MarketPanelEngine, load_issuers
from stabilization_panel import StabilizationPanelEngine

SCRATCH = ROOT / "pipeline" / "scratch" / "regen_2026"
OUT_MASTER = PROSPECTUS / "out" / "master"
COMMIT = "--commit" in sys.argv


def load_csv(path: Path) -> dict:
    with path.open(encoding="utf-8-sig") as fh:
        return {(r.get("stock_code"), r.get("lockup_category") or r.get("horizon") or ""): r
                for r in csv.DictReader(fh)}


def diff_csv(name: str, changed_fields: list[str]) -> None:
    old = load_csv(OUT_MASTER / name)
    new = load_csv(SCRATCH / "master" / name)
    changes = 0
    samples = []
    for key, new_r in new.items():
        old_r = old.get(key)
        if old_r is None:
            changes += 1
            if len(samples) < 5:
                samples.append(("new_row", key))
            continue
        for f in changed_fields:
            if (old_r.get(f) or "") != (new_r.get(f) or ""):
                changes += 1
                if len(samples) < 5:
                    samples.append((key, f, old_r.get(f), new_r.get(f)))
                break
    print(f"{name}: {changes} changed rows/cells (of {len(new)})")
    for s in samples:
        print("   ", s)


def main() -> int:
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    (SCRATCH / "master").mkdir(parents=True)

    issuers = []
    for q in ("2026q1", "2026q2", "2026q3"):
        issuers.extend(load_issuers(cfg=load_cfg(config_path=PROSPECTUS / f"config_{q}.yaml")))
    print(f"{len(issuers)} issuers")

    base = load_cfg(config_path=PROSPECTUS / "config_2026q1.yaml")
    cfg = {**base, "paths": {**base["paths"], "out": SCRATCH,
                             "data": PROSPECTUS / "data",
                             "allot_out": PROSPECTUS / "out" / "allot"}}

    print("market ...")
    MarketPanelEngine(cfg=cfg).run(issuers)
    print("stabilization ...")
    StabilizationPanelEngine(cfg=cfg).run(issuers)
    print("lockup ...")
    LockupPanelEngine(cfg=cfg).run(issuers)

    for f in ("investor_relational.csv", "underwriter_relational.csv", "issuer_master.csv"):
        if (OUT_MASTER / f).exists():
            shutil.copy2(OUT_MASTER / f, SCRATCH / "master" / f)

    print("\n--- diffs vs production out/master ---")
    diff_csv("lockup_events.csv", ["expiry_date", "last_restricted_day", "evidence_status",
                                   "window_status", "car_m5_p5", "car_m20_p20", "car_0_p60",
                                   "volume_shock_ratio"])
    diff_csv("stabilization_events.csv", ["stabilization_purchases_occurred", "cliff_return_m5_p5"])
    diff_csv("horizon_summary.csv", ["actual_date", "bhr_from_day1", "matured"])

    if COMMIT:
        for f in ("lockup_events.csv", "stabilization_events.csv", "horizon_summary.csv",
                  "daily_market_panel.csv"):
            shutil.copy2(SCRATCH / "master" / f, OUT_MASTER / f)
        print("committed to out/master")
    return 0


if __name__ == "__main__":
    sys.exit(main())
