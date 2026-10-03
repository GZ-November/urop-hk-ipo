"""Prepare and apply a narrowly reviewed col_CO repair; never writes workbooks."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

import pandas as pd
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
PIPE = ROOT / "pipeline/prospectus_pipeline"
sys.path[:0] = [str(PIPE / "src"), str(PIPE)]
from cohort import load_cfg  # noqa: E402
from contracts import evidence_issues, validate_record  # noqa: E402
from storage import atomic_json  # noqa: E402
from validate import validate_all  # noqa: E402

FOLLOWUP = ROOT / "pipeline/reports/data_gap_collection/source_followup_2026-10-03"
OUT = FOLLOWUP / "formal_json_repair"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare():
    OUT.mkdir(exist_ok=True)
    for name in ["before", "extracted", "evidence", "pre_repair_followup"]:
        (OUT / name).mkdir(exist_ok=True)
    ledger = pd.read_csv(FOLLOWUP / "nineteen_applied_totals.csv")
    assert len(ledger) == 19 and ledger.code.nunique() == 19
    schema = json.loads((PIPE / "schema/allot_fields.json").read_text())
    field_schema = {**schema, "fields": [x for x in schema["fields"] if x["key"] == "col_CO"], "field_count": 1}
    # Preserve the previous assessment's exact input and output bytes once.
    for source in [*FOLLOWUP.glob("*.csv"), FOLLOWUP / "source_manifest.json"]:
        target = OUT / "pre_repair_followup" / source.name
        if not target.exists():
            shutil.copyfile(source, target)
    records = []
    for row in ledger.to_dict("records"):
        code = row["code"]
        name = "HKIPO-MB" + code.split(".")[0]
        canonical = PIPE / "out/allot/extracted" / (name + ".json")
        before = OUT / "before" / canonical.name
        if not before.exists():
            assert sha(canonical) == row["formal_sha256"], code
            shutil.copyfile(canonical, before)
        payload = json.loads(before.read_text())
        pdf = PIPE / "data/allot/pdf" / (name + ".pdf")
        source_text = PIPE / "data/allot/text" / (name + ".jsonl")
        packet = PIPE / "data/allot/packets" / (name + ".md")
        assert sha(pdf) == row["pdf_sha256"]
        pages = [int(x) for x in row["pdf_pages"].split(";")]
        operands, raw_pages = [], []
        with pymupdf.open(pdf) as document:
            for page in pages:
                text = document[page - 1].get_text(sort=True)
                raw_pages.append({"pdf_page": page, "layout_text": text})
                pattern = r"(?m)^\s*([\d,]+)\s+([\d,]+)\s+(?:\D|(?=[\d,]+\s+(?:out\s+of|(?:H\s+)?Shares)))"
                for match in re.finditer(pattern, text):
                    applied, applicants = [int(x.replace(",", "")) for x in match.groups()]
                    operands.append({"pdf_page": page, "applied_shares": applied, "applicants": applicants,
                                     "product": applied * applicants})
        assert len(operands) == row["tiers"]
        assert len({x["applied_shares"] for x in operands}) == len(operands)
        exact = sum(x["product"] for x in operands)
        applicant_sum = sum(x["applicants"] for x in operands)
        assert exact == row["exact_pdf_tier_sum"]
        assert applicant_sum == payload["fields"]["col_CN"]["value"]
        originals = {json.loads(s)["page"]: json.loads(s)["text"] for s in source_text.read_text().splitlines()}
        first_page = pages[0]
        # A real header excerpt identifies the table; the complete sum is in note/evidence.
        original = originals[first_page]
        start = original.upper().find("BASIS OF ALLOCATION")
        if start < 0:
            start = original.upper().find("NO. OF")
        if start < 0:
            start = 0
        quote = original[start:start + 195].strip()
        proof = OUT / "evidence" / (name + ".json")
        evidence = {"code": code, "field": "col_CO", "definition": "ordinary public valid applied shares",
                    "derivation": "sum(applied_shares * valid_applications) across each disclosed ordinary public tier once",
                    "source_pdf": str(pdf.relative_to(ROOT)), "official_pdf_url": row["source_url"],
                    "pdf_sha256": sha(pdf), "source_text": str(source_text.relative_to(ROOT)),
                    "source_text_sha256": sha(source_text), "packet_sha256": sha(packet),
                    "physical_pdf_pages": pages, "operands": operands, "raw_pages": raw_pages,
                    "total_applied_shares": exact, "total_applicants": applicant_sum,
                    "unit": "shares", "old_field": payload["fields"]["col_CO"],
                    "old_origin_assessment": row["cause_status"]}
        atomic_json(proof, evidence)
        candidate = deepcopy(payload)
        candidate["fields"]["col_CO"] = {
            "value": exact, "page": first_page, "quote": quote, "confidence": "high",
            "note": (f"Derived exact integer sum of applied shares × valid applications across {len(operands)} ordinary-public tiers "
                     f"on physical PDF pages {', '.join(map(str, pages))}: {exact:,} shares; applicant sum {applicant_sum:,}. "
                     f"This is a tier sum, not a directly printed aggregate or a product of the rounded subscription multiple. "
                     f"Evidence: {proof.relative_to(ROOT)}; source PDF SHA-256 {sha(pdf)}.")}
        assert {k for k in candidate["fields"] if candidate["fields"][k] != payload["fields"][k]} == {"col_CO"}
        isolated = {"code": code, "fields": {"col_CO": candidate["fields"]["col_CO"]}}
        errors = validate_record(isolated, field_schema, code, "allot") + evidence_issues(isolated, packet, field_schema, target="allot")
        assert not errors, (code, errors)
        target = OUT / "extracted" / canonical.name
        atomic_json(target, candidate)
        records.append({"code": code, "field": "col_CO", "before": str(before.relative_to(ROOT)),
                        "before_sha256": sha(before), "candidate": str(target.relative_to(ROOT)), "candidate_sha256": sha(target),
                        "canonical": str(canonical.relative_to(ROOT)), "evidence": str(proof.relative_to(ROOT)),
                        "evidence_sha256": sha(proof), "source_pdf": str(pdf.relative_to(ROOT)), "source_pdf_sha256": sha(pdf),
                        "old_value": payload["fields"]["col_CO"]["value"], "new_value": exact,
                        "field_validation_errors": errors})
    # Full deterministic checks are retained separately from scoped semantic review.
    validation = {}
    for quarter in ["q2", "q3"]:
        cfg = load_cfg(config_path=PIPE / f"config_2026{quarter}.yaml")
        cohort_codes = {x["code"] for x in __import__("cohort").read_companies(cfg)}
        codes = [r["code"] for r in records if r["code"] in cohort_codes]
        staging = OUT / "validation_scope" / quarter
        (staging / "extracted").mkdir(parents=True, exist_ok=True)
        for code in codes:
            name = "HKIPO-MB" + code.split(".")[0] + ".json"
            shutil.copyfile(OUT / "extracted" / name, staging / "extracted" / name)
        for name in ["greenshoe.json", "greenshoe_shares.json", "cornerstone_absence.json"]:
            source = PIPE / "out/allot" / name
            if source.exists():
                shutil.copyfile(source, staging / name)
        # A candidate-only validation does not pretend to cover other cohort issuers.
        (staging / "validation.json").unlink(missing_ok=True)
        cfg["paths"]["allot_out"] = staging
        cfg["state_dir"] = OUT / ".pipeline_state" / quarter
        report = validate_all(cfg, only=codes, target="allot", log=lambda _: None)
        atomic_json(OUT / f"candidate_validation_{quarter}.json", report)
        validation[quarter] = {"issuers": len(codes), "gate_pass": report["gate_pass"], "errors": report["errors"]}
    atomic_json(OUT / "repair_manifest.json", {"scope": "col_CO only, 19 issuers; no workbook write", "records": records,
                                              "candidate_validation": validation, "schema_sha256": sha(PIPE / "schema/allot_fields.json")})
    print(json.dumps(validation, indent=2))


def apply():
    manifest = json.loads((OUT / "repair_manifest.json").read_text())
    review = json.loads((OUT / "independent_review.json").read_text())
    assert review["verdict"] == "pass_for_col_CO_only" and review["reviewer_id"].startswith("independent-agent:")
    assert review["whole_payload_review"] is False
    assert all(r["gate_pass"] and not r["errors"] for r in manifest["candidate_validation"].values())
    expected = {r["code"]: r for r in manifest["records"]}
    assessed = {r["code"]: r for r in review["records"]}
    assert set(expected) == set(assessed) and len(expected) == 19
    for code, row in expected.items():
        decision = assessed[code]
        assert decision["verdict"] == "pass" and decision["field"] == "col_CO"
        assert decision["candidate_sha256"] == row["candidate_sha256"]
        assert decision["evidence_sha256"] == row["evidence_sha256"]
        assert decision["source_pdf_sha256"] == row["source_pdf_sha256"]
        assert decision["independently_computed_total"] == row["new_value"]
        for path_key, hash_key in [("candidate", "candidate_sha256"), ("before", "before_sha256"),
                                   ("evidence", "evidence_sha256"), ("source_pdf", "source_pdf_sha256")]:
            assert sha(ROOT / row[path_key]) == row[hash_key], (code, path_key)
        assert sha(ROOT / row["canonical"]) == row["before_sha256"], f"Canonical changed since preparation: {code}"
    written = []
    try:
        for row in expected.values():
            target = ROOT / row["canonical"]
            candidate = ROOT / row["candidate"]
            temporary = target.with_suffix(".repair-tmp")
            shutil.copyfile(candidate, temporary)
            temporary.replace(target)
            written.append(row)
    except Exception:
        for row in written:
            shutil.copyfile(ROOT / row["before"], ROOT / row["canonical"])
        raise
    atomic_json(OUT / "applied.json", {"status": "19_col_CO_repairs_applied", "review_sha256": sha(OUT / "independent_review.json"),
                                      "workbooks_written": False, "whole_payload_review_renewed": False,
                                      "records": [{"code": r["code"], "json_sha256": sha(ROOT / r["canonical"])} for r in written]})
    print("Applied 19 source-reviewed col_CO repairs; no workbook changes; no whole-payload review approval created.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["prepare", "apply"])
    action = parser.parse_args().stage
    prepare() if action == "prepare" else apply()
