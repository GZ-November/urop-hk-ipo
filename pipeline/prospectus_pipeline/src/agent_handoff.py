"""Generate portable extraction/review work orders for any tool-capable agent."""
from __future__ import annotations

import json
from pathlib import Path
import shlex
import sys


def build_handoff(cfg: dict, companies: list[dict]) -> Path:
    destination = cfg["paths"]["out"] / "agent_handoff"
    destination.mkdir(parents=True, exist_ok=True)
    run = Path(cfg["_root"]) / "run.py"
    command = shlex.join([sys.executable, str(run), "--config", str(cfg["_config_path"])])
    jobs = []
    targets = [("prospectus", "packets", "out", "gem_prospectus_fields.json" if str(cfg.get("dataset", {}).get("board", "")).upper() == "GEM" else "fields.json"),
               ("allot", "allot_packets", "allot_out", "allot_fields.json")]
    if str(cfg.get("dataset", {}).get("board", "")).upper() == "GEM":
        targets.append(("gem", "packets", "out", "gem_fields.json"))
    for company in companies:
        code = company["code"]
        stem = "HKIPO-MB" + code.split(".")[0]  # legacy artifact key, isolated by cohort paths
        for target, packet_key, output_key, schema_name in targets:
            packet = cfg["paths"][packet_key] / f"{stem}.md"
            payload = (cfg["paths"][output_key] / "gem" if target == "gem" else cfg["paths"][output_key]) / "extracted" / f"{stem}.json"
            schema = cfg["_root"] / "schema" / schema_name
            extract_path = destination / f"{code}.{target}.extract.md"
            review_path = destination / f"{code}.{target}.review.md"
            common = f"""Company: {code} {company.get('name', '')}
Board: {cfg.get('dataset', {}).get('board', 'Main Board')}
Config: {cfg['_config_path']}
Packet: {packet}
Schema: {schema}
Extraction output: {payload}
Run commands with the supplied config. Keep monetary units, share units, source
page numbers and reporting periods explicit. Use issuer-specific consolidated
financial statements. Treat missing evidence as missing, and disclosed zero as zero.
The config board comes from the official listing-report source. Read docs/GEM_PIPELINE.md for applicability: classify structural absence separately
from undisclosed/unknown/immature fields in a source-backed review report. For GEM, apply
GEM-specific issuer terms and dated rules; Main Board admission/Chapter 18A/18C
checks do not determine GEM compliance. Historical filenames beginning HKIPO-MB
are internal compatibility keys, not board classifications.
"""
            extract = f"""# Extract {target} evidence
{common}
Read the entire field contract in the packet/schema. Write exactly the keys and
entry structure required by that contract: code/fields, with value/page/quote/
confidence per field. Use NaN for missing numeric values and NA for missing text
or dates, as strings. Each nonmissing value needs a supporting source quote.
For prospectus work use these search commands to examine actual disclosure pages:
```
{command} search sharecap {code}
{command} search periods {code}
{command} search bundle {code}
{command} search pages {code} 1-3
{command} search search {code} "YOUR_REGEX" --context 3 --max 8
```
Read pipeline/prospectus_pipeline/workflows/{'allot' if target == 'allot' else 'prospectus'}_extract.js
for the domain extraction rules; it is a DSH runtime adapter, not a Node command.
For allotment, read the whole packet and distinguish final offer shares from greenshoe.
After writing allotment JSON, run `{command} derive_allot --only {code}` BEFORE
recording any final extraction or review credential (it can modify the payload).
Reporting periods: `search periods` is authoritative and validate enforces it.
year-1 is the latest Track Record period; a stub (3M to 11M) is year-1 itself,
col_AT is its end date, and balance-sheet fields use that date. year-2 and year-3
are the two complete years before it. Only col_AH/AK/AN are annualised
(×12/months). Read or compute every number from the cited page. Never solve for
a value to make an identity hold: leave it NaN and report the identity.
Validate and correct unsupported values against source text until validation passes:
```
{command} validate --target {target} --only {code}
{command} state extracted --target {target} --code {code}
```
Save a short extraction note naming missing/uncertain fields. Hand the payload to
an independent reviewer. Completion here is a valid extraction plus extracted
credential; a review pass belongs to the independent reviewer.
"""
            review = f"""# Independently review {target} evidence
{common}
Read the original packet and supporting pages independently of the extracting
agent's reasoning. Verify every populated field's meaning, units, period, page and
quote. Pay particular attention to consolidated versus parent-only accounts,
annualization, share-capital denominators, VC/PE classification, cornerstone
allocations, net versus gross proceeds, and initial versus final offering terms.
Record the payload's sha256 at the top of the report. Report a discrepancy only
after opening the cited page yourself. Check the period anchor: year-1 is the
latest Track Record period (a stub, if there is one), and year-2/year-3 are the
two complete years before it. For every value this code lists under `warnings`
in the target's validation.json, recompute it from the cited page and write the
arithmetic down. Never propose a value that only satisfies an identity.
Write a review report identifying checked fields, missing fields, corrections and
source pages. Keep the actual reviewer identity and the report path in the record.
If corrections change the payload, the extractor must validate and record extracted
again, followed by another independent review of the changed payload.
Only after the independent review succeeds, run (replace placeholders):
```
{command} state reviewed --target {target} --code {code} --verdict pass --reviewer "ACTUAL_INDEPENDENT_REVIEWER" --evidence-ref "ACTUAL_REVIEW_REPORT_PATH" --review-note "ACTUAL_REVIEW_SUMMARY"
```
Use --verdict fail for an unsuccessful review. A named record is provenance, not
proof that the review occurred. If no independent reviewer is available, report
review pending and leave writeback blocked. Completion is a source-supported
report and a credential for the exact current payload, with no invented sign-off.
"""
            extract_path.write_text(extract, encoding="utf-8")
            review_path.write_text(review, encoding="utf-8")
            jobs.append({"code": code, "target": target, "packet": str(packet),
                         "packet_ready": packet.is_file(), "output": str(payload),
                         "extraction_exists": payload.is_file(),
                         "extract_instruction": str(extract_path), "review_instruction": str(review_path)})
    path = destination / "work_orders.json"
    path.write_text(json.dumps({"config": str(cfg["_config_path"]), "jobs": jobs}, indent=2) + "\n", encoding="utf-8")
    return path
