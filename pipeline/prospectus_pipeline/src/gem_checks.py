"""GEM consistency checks; dated eligibility/waivers require independent source review."""
from __future__ import annotations

import json
import math
from pathlib import Path

import openpyxl

from contracts import strict_load_file
from workbook_reader import resolve_columns


def run_gem_cross_check(cfg: dict, companies: list[dict]) -> int:
    workbook = openpyxl.load_workbook(cfg["_workbook_path"], data_only=True)
    try:
        sheet = workbook[cfg["sheet"]]
        mapping, issues = resolve_columns(sheet, strict_load_file(cfg["_root"] / "schema/gem_prospectus_fields.json"))
        if issues:
            raise ValueError(f"GEM headers do not resolve: {issues}")
        results = []
        for company in companies:
            row, code = company["row"], company["code"]
            def number(key):
                value = sheet[f"{mapping[key]}{row}"].value
                return float(value) if isinstance(value, (int, float)) and math.isfinite(float(value)) else None
            checks = []
            for title, left, right_a, right_b in (
                ("Offer = placing + public", "col_M", "col_R", "col_S"),
                ("Offer = new + sale", "col_M", "col_Q", "col_P"),
            ):
                values = [number(k) for k in (left, right_a, right_b)]
                if all(v is not None for v in values) and abs(values[0] - values[1] - values[2]) > 1:
                    checks.append({"check": title, "severity": "ERROR", "values": values})
            lower, upper = number("col_U"), number("col_T")
            if lower is not None and upper is not None and lower > upper:
                checks.append({"check": "Filing range inverted", "severity": "ERROR"})
            checks.append({"check": "GEM eligibility, public float, offering terms and waivers",
                           "severity": "REVIEW", "detail": "Use the issuer's dated GEM rules and extension evidence. Main Board admission checks are not applied."})
            results.append({"code": code, "checks": checks})
    finally:
        workbook.close()
    errors = sum(c["severity"] == "ERROR" for r in results for c in r["checks"])
    report = {"board": "GEM", "total_companies": len(results), "errors": errors,
              "scope": "Share identities and filing range only; not a legal eligibility certification.", "results": results}
    output = Path(cfg["paths"]["out"]) / "cross_check_report.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    output.with_suffix(".md").write_text(
        f"# GEM consistency report\n\nIssuers: {len(results)}. Errors: {errors}.\n\n{report['scope']}\n\n"
        "Issuer-specific GEM requirements and waivers remain subject to independent source review.\n", encoding="utf-8")
    print(f"GEM consistency: {len(results)} issuers, {errors} errors; eligibility source review required. {output}")
    return int(bool(errors))


def generate_gem_report(cfg: dict) -> Path:
    from codebook import build_codebook
    variables, summary = build_codebook(cfg)
    path = Path(cfg["paths"]["out"]) / "GEM_research_readiness.md"
    lines = ["# GEM research readiness", "", f"Issuers: {summary['sample_size']}. Common fields: {summary['variable_count']}.",
             "", "Main Board-only pathways and fixed controller-lockup dates are absent. GEM eligibility and waivers require source review.",
             "", "| Field | Nonmissing | Missing |", "|---|---:|---:|"]
    for variable in variables:
        values = variable.get("values", [])
        missing = sum(value in (None, "", "NA", "NaN") for value in values)
        lines.append(f"| {variable['header']} | {len(values)-missing} | {missing} |")
    lines += ["", "This is descriptive field coverage, not independent review or legal certification. Use audit/status and the GEM extension evidence separately."]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
