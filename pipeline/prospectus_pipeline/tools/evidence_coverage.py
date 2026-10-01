#!/usr/bin/env python3
"""Report what the gate credentials and extraction files do and do not establish.

Outputs (written to --out-dir, default pipeline/reports/repair_handoff):
  review_provenance.csv  one row per cohort x target x issuer: credential status and who reviewed
  evidence_matrix.csv    one row per issuer x research-relevant field: evidence status
  evidence_coverage_summary.md  counts by cohort and target

Review provenance classes:
  named_reviewer    the reviewed record names a reviewer and is bound to the current payload bytes
  bulk_stamp        a pass record exists but names no reviewer (e.g. imported in one batch seconds after
                    the extraction record); it proves a gate was opened, not that anyone reviewed it
  stale             a record names the payload hash of an older file version
  absent            no reviewed record
Nothing here verifies semantics; it classifies the available evidence.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from offer_units import QUANTITY_FIELDS_ALLOT, QUANTITY_FIELDS_PROSPECTUS, quote_unit_conflict  # noqa: E402

COHORTS = {"2026Q1": ("config_2026q1.yaml", ""), "2026Q2": ("config_2026q2.yaml", "HKIPO-MB2026Q2"),
           "2026Q3": ("config_2026q3.yaml", "HKIPO-MB2026Q3")}
STATE = ROOT / ".pipeline_state"
MISSING = {"", "nan", "na", "n/a", "none", "null"}

# Fields used by the research scripts and the repair scope (prices, quantities, allocations, cornerstones,
# VC/PE, mechanism and timing). Keys resolve against schema/fields.json and schema/allot_fields.json.
PROSPECTUS_KEYS = ["col_L", "col_M", "col_N", "col_O", "col_P", "col_Q", "col_R", "col_S", "col_T", "col_U", "col_AO",
                   "col_AP", "col_AQ", "col_AS", "col_BA", "col_vc_backed", "col_pe_backed", "col_cvc_backed",
                   "col_gov_backed", "col_top_tier_vc", "col_vc_board_seat", "col_vc_pe_stake", "col_pre_ipo_investors",
                   "col_BC", "col_BD", "col_CC", "col_CD", "col_CE", "col_CI", "col_CJ"]
ALLOT_KEYS = ["col_CK", "col_CM", "col_CN", "col_CO", "col_CQ", "col_CR", "col_CS", "col_CT", "col_CU", "col_CV",
              "col_CW", "col_CX", "col_CY", "col_CZ", "col_DA", "col_DC"]


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def sha256(path: Path) -> str:
    import hashlib
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def is_missing(value) -> bool:
    return value is None or (isinstance(value, str) and value.strip().lower() in MISSING)


def classify_review(reviewed: dict, extracted: dict, validated: dict, payload_sha: str):
    if not reviewed:
        return "absent", ""
    if not reviewed.get("gate_pass"):
        return "failed", reviewed.get("reviewer", "")
    current = validated.get("json_sha256") == payload_sha and reviewed.get("hash") == validated.get("hash")
    if not current:
        return "stale", reviewed.get("reviewer", "")
    if (reviewed.get("reviewer") or "").strip():
        return "named_reviewer", reviewed["reviewer"].strip()
    return "bulk_stamp", ""


def cohort_codes(cohort: str):
    path = REPO / "pipeline" / "exports" / "HKIPO-MB-MASTER_clean.csv"
    with path.open(encoding="utf-8-sig") as fh:
        return [r["Stock Code"] for r in csv.DictReader(fh) if r["cohort"] == cohort]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", default=str(REPO / "pipeline" / "reports" / "repair_handoff"))
    args = ap.parse_args(argv)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    prov_rows, matrix_rows = [], []
    for cohort, (_, state_sub) in COHORTS.items():
        base = STATE / state_sub if state_sub else STATE
        for code in cohort_codes(cohort):
            digits = code.split(".")[0]
            for target, ext_dir, keys in (("prospectus", ROOT / "out" / "extracted", PROSPECTUS_KEYS),
                                          ("allot", ROOT / "out" / "allot" / "extracted", ALLOT_KEYS)):
                path = ext_dir / f"HKIPO-MB{digits}.json"
                record = read_json(path) if path.exists() else None
                states = {st: (read_json(base / target / st / f"{code}.json") or {}) for st in
                          ("extracted", "validated", "reviewed", "written")}
                payload_sha = sha256(path) if path.exists() else ""
                review_class, reviewer = classify_review(states["reviewed"], states["extracted"], states["validated"],
                                                         payload_sha)
                prov_rows.append({
                    "cohort": cohort, "target": target, "code": code, "json_present": int(record is not None),
                    "extracted": int(bool(states["extracted"].get("gate_pass"))),
                    "validated": int(bool(states["validated"].get("gate_pass"))),
                    "review_class": review_class, "reviewer": reviewer,
                    "review_scope": ("field_scoped" if str(states["reviewed"].get("review_note", "")).startswith("Scope:")
                                     else ("whole_payload_unspecified" if review_class == "named_reviewer" else "")),
                    "review_note": states["reviewed"].get("review_note", ""),
                    "reviewed_at": states["reviewed"].get("recorded_at", ""),
                    "written": int(bool(states["written"].get("gate_pass")))})
                fields = (record or {}).get("fields", {})
                quantity_keys = set(QUANTITY_FIELDS_PROSPECTUS if target == "prospectus" else QUANTITY_FIELDS_ALLOT)
                for key in keys:
                    entry = fields.get(key)
                    if record is None:
                        status = "json_absent"
                    elif not isinstance(entry, dict):
                        status = "field_absent"
                    elif is_missing(entry.get("value")):
                        status = "unknown"
                    elif entry.get("source") in {"da_formula", "greenshoe_lapse", "greenshoe_search", "cornerstone_absence"}:
                        status = "derived_rule"
                    elif not (entry.get("quote") or "").strip():
                        status = "value_without_quote"
                    elif key in quantity_keys and quote_unit_conflict(entry.get("value"), entry.get("quote", "")):
                        status = "unit_conflict_with_quote"
                    else:
                        status = "value_with_quote"
                    matrix_rows.append({"cohort": cohort, "code": code, "target": target, "field": key,
                                        "status": status, "page": (entry or {}).get("page", "") if isinstance(entry, dict) else "",
                                        "confidence": (entry or {}).get("confidence", "") if isinstance(entry, dict) else "",
                                        "review_class": review_class})

    def write(name, rows):
        with (out_dir / name).open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    write("review_provenance.csv", prov_rows)
    write("evidence_matrix.csv", matrix_rows)

    from collections import Counter
    lines = [f"# Evidence coverage summary\n\nGenerated {dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).isoformat(timespec='seconds')} HKT "
             "from the extraction JSON files and local gate credentials. Classification only; no semantic verification.\n",
             "## Review provenance (issuers per cohort x target)\n", "| cohort | target | n | named_reviewer | bulk_stamp | stale | absent | failed |",
             "|---|---|---:|---:|---:|---:|---:|---:|"]
    for cohort in COHORTS:
        for target in ("prospectus", "allot"):
            sub = [r for r in prov_rows if r["cohort"] == cohort and r["target"] == target]
            c = Counter(r["review_class"] for r in sub)
            lines.append(f"| {cohort} | {target} | {len(sub)} | {c['named_reviewer']} | {c['bulk_stamp']} | {c['stale']} | {c['absent']} | {c['failed']} |")
    lines += ["", "## Research-field evidence status (issuer x field cells)\n",
              "| cohort | target | cells | value_with_quote | derived_rule | unknown | value_without_quote | unit_conflict_with_quote | field_absent | json_absent |",
              "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for cohort in COHORTS:
        for target in ("prospectus", "allot"):
            sub = [r for r in matrix_rows if r["cohort"] == cohort and r["target"] == target]
            c = Counter(r["status"] for r in sub)
            lines.append(f"| {cohort} | {target} | {len(sub)} | {c['value_with_quote']} | {c['derived_rule']} | {c['unknown']} | "
                         f"{c['value_without_quote']} | {c['unit_conflict_with_quote']} | {c['field_absent']} | {c['json_absent']} |")
    lines += ["", "`named_reviewer` means a record names a reviewer and matches the current file bytes (see `review_scope`: "
              "this repair's reviews cover only the stated fields, not the whole payload); `bulk_stamp` is a pass record "
              "with no reviewer identity. A quote that contains the value is not a semantic review.\n"]
    (out_dir / "evidence_coverage_summary.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
