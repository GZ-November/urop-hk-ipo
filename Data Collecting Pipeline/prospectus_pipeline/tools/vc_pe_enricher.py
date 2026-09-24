#!/usr/bin/env python3
"""Cohort-neutral VC/PE coverage and evidence audit.

VC/PE values are collected by the normal prospectus workflow from the active
cohort's packets and ``schema/fields.json``. This helper deliberately contains
no issuer-level values and never writes to a workbook. Use ``run.py validate``
and ``run.py write`` for the normal hash-bound validation/write-back gates.

Examples (run from ``Data Collecting Pipeline``)::

    python prospectus_pipeline/tools/vc_pe_enricher.py status
    python prospectus_pipeline/tools/vc_pe_enricher.py validate --only 6656.HK
    python prospectus_pipeline/tools/vc_pe_enricher.py validate --require-complete
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
WS = ROOT.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from run import load_cfg, read_companies  # noqa: E402
from contracts import evidence_issues, normalize_code, strict_load_file  # noqa: E402
from storage import official_files  # noqa: E402

VC_PE_KEYS = (
    "col_vc_backed",
    "col_pe_backed",
    "col_cvc_backed",
    "col_gov_backed",
    "col_top_tier_vc",
    "col_pre_ipo_investors",
    "col_vc_pe_stake",
    "col_vc_board_seat",
    "col_earliest_round",
    "col_holding_duration",
)
MISSING = {None, "", "na", "n/a", "nan", "none", "-"}


def _is_missing(value: Any) -> bool:
    return value is None or (isinstance(value, str) and value.strip().lower() in MISSING)


def _field_value(record: dict, key: str) -> dict:
    fields = record.get("fields", {})
    entry = fields.get(key, {}) if isinstance(fields, dict) else {}
    return entry if isinstance(entry, dict) else {"value": entry}


def _validate_field(key: str, entry: dict) -> list[str]:
    value = entry.get("value")
    if _is_missing(value):
        return []
    issues = []
    if key in {"col_vc_backed", "col_pe_backed", "col_cvc_backed", "col_gov_backed",
               "col_top_tier_vc", "col_vc_board_seat"}:
        if value not in (0, 1, "0", "1"):
            issues.append("expected binary 0/1")
    elif key in {"col_vc_pe_stake", "col_holding_duration"}:
        try:
            number = float(value)
            if not math.isfinite(number):
                raise ValueError
            if key == "col_vc_pe_stake" and not 0 <= number <= 1:
                issues.append("shareholding must be in [0, 1]")
            if key == "col_holding_duration" and number < 0:
                issues.append("holding duration cannot be negative")
        except (TypeError, ValueError):
            issues.append("expected a finite number")
    else:
        if not isinstance(value, str):
            issues.append("expected text")

    quote = entry.get("quote")
    page = entry.get("page")
    source = entry.get("source")
    if not isinstance(quote, str) or not quote.strip():
        issues.append("missing source quote")
    if source != "derived" and (not isinstance(page, int) or isinstance(page, bool) or page < 1):
        issues.append("missing prospectus page")
    return issues


def audit(cfg: dict, only: list[str] | None = None) -> list[dict]:
    companies = read_companies(cfg)
    if only:
        wanted = {code.upper() for code in only}
        companies = [company for company in companies if company["code"].upper() in wanted]
    directory = cfg["paths"]["out"] / "extracted"
    files = official_files(directory, only=[c["code"] for c in companies])
    by_code = {code: path for code, path in files.items()}
    schema = strict_load_file(ROOT / "schema" / "fields.json")
    results = []
    for company in companies:
        code = company["code"]
        path = by_code.get(code)
        if not path:
            results.append({"code": code, "name": company["name"], "missing_file": True,
                            "present": 0, "missing": list(VC_PE_KEYS), "issues": {}})
            continue
        try:
            record = strict_load_file(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            results.append({"code": code, "name": company["name"], "missing_file": False,
                            "present": 0, "missing": list(VC_PE_KEYS),
                            "issues": {"_record": [f"cannot read extraction JSON: {exc}"]}})
            continue
        if not isinstance(record, dict):
            results.append({"code": code, "name": company["name"], "missing_file": False,
                            "present": 0, "missing": list(VC_PE_KEYS),
                            "issues": {"_record": ["extraction root must be a JSON object"]}})
            continue
        if normalize_code(record.get("code", "")) != normalize_code(code):
            results.append({"code": code, "name": company["name"], "missing_file": False,
                            "present": 0, "missing": list(VC_PE_KEYS),
                            "issues": {"_record": [f"record code does not match workbook company {code}"]}})
            continue
        record_fields = record.get("fields")
        if not isinstance(record_fields, dict):
            results.append({"code": code, "name": company["name"], "missing_file": False,
                            "present": 0, "missing": list(VC_PE_KEYS),
                            "issues": {"_record": ["fields must be a JSON object"]}})
            continue
        missing, issues, present = [], {}, 0
        for key in VC_PE_KEYS:
            entry = _field_value(record, key)
            if _is_missing(entry.get("value")):
                missing.append(key)
                continue
            present += 1
            field_issues = _validate_field(key, entry)
            if field_issues:
                issues[key] = field_issues
        pages_path = cfg["paths"]["text"] / f"HKIPO-MB{code.split('.')[0]}.jsonl"
        packet_path = cfg["paths"]["packets"] / f"HKIPO-MB{code.split('.')[0]}.md"
        if pages_path.is_file() and packet_path.is_file():
            page_blocks = []
            try:
                with pages_path.open(encoding="utf-8") as page_file:
                    for line in page_file:
                        page = json.loads(line)
                        page_blocks.append(f"<<<PAGE {int(page['page'])}>>>\n{page['text']}")
                evidence_record = {"code": code, "fields": {
                    key: record_fields.get(key)
                    for key in VC_PE_KEYS
                    if isinstance(record_fields.get(key), dict)
                }}
                evidence_problems = evidence_issues(
                    evidence_record, packet_path, schema,
                    {"prospectus": "\n".join(page_blocks)}, target="prospectus")
                for problem in evidence_problems:
                    key, _, detail = problem.partition(":")
                    issues.setdefault(key if key in VC_PE_KEYS else "_evidence", []).append(detail.strip() or problem)
            except (OSError, ValueError, KeyError, TypeError) as exc:
                issues.setdefault("_evidence", []).append(f"cannot verify cited pages/quotes: {exc}")
        else:
            missing_sources = []
            if not packet_path.is_file():
                missing_sources.append("packet")
            if not pages_path.is_file():
                missing_sources.append("page text")
            issues.setdefault("_evidence", []).append("evidence verification unavailable: missing " + " and ".join(missing_sources))
        results.append({"code": code, "name": company["name"], "missing_file": False,
                        "present": present, "missing": missing, "issues": issues})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="按当前 cohort 检查 Pre-IPO VC/PE 抽取覆盖率与证据")
    parser.add_argument("command", choices=("status", "validate"), nargs="?", default="status")
    parser.add_argument("--only", nargs="*", help="只检查指定公司，如 6656.HK")
    parser.add_argument("--require-complete", action="store_true",
                        help="validate 时将缺失字段也视为失败")
    parser.add_argument("--config", help="cohort config；也可设置 PIPELINE_CONFIG")
    args = parser.parse_args()
    if args.config:
        import os
        os.environ["PIPELINE_CONFIG"] = str(Path(args.config).expanduser().resolve())
    cfg = load_cfg()
    results = audit(cfg, args.only)
    dataset = cfg.get("dataset", {})
    label = dataset.get("id") or dataset.get("cohort") or "active cohort"
    print(f"VC/PE audit — {label}: {len(results)} companies, {len(VC_PE_KEYS)} fields/company")
    invalid = incomplete = 0
    for result in results:
        incomplete += bool(result["missing"] or result["missing_file"])
        invalid += bool(result["issues"])
        state = "MISSING FILE" if result["missing_file"] else f"{result['present']}/10 fields"
        details = []
        if result["missing"]:
            details.append("missing=" + ",".join(result["missing"]))
        if result["issues"]:
            details.append("invalid=" + "; ".join(
                f"{key}: {', '.join(messages)}" for key, messages in result["issues"].items()))
        suffix = " | " + " | ".join(details) if details else ""
        print(f"{result['code']} {result['name']}: {state}{suffix}")
    print(f"Summary: incomplete={incomplete}, evidence/type issues={invalid}")
    if args.command == "validate" and (invalid or (args.require_complete and incomplete)):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
