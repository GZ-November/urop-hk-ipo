"""Apply only independently reviewed supplementary cells, with frozen hash guards."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "pipeline/prospectus_pipeline/src"))
from workbook_transaction import workbook_transaction


def main():
    review = json.loads((HERE / "final_review.json").read_text())
    assert review["gate_pass"] and review["allowed_formal_write"]
    bound = {
        "payload_sha256": ROOT / "pipeline/prospectus_pipeline/out/extracted/HKIPO-MB6872.json",
        "supplemental_sha256": HERE / "supplemental_fields.json",
        "supporting_evidence_sha256": HERE / "supporting_evidence.json",
        "investor_crosscheck_sha256": HERE / "investor_crosscheck.json",
        "source_text_sha256": ROOT / "pipeline/prospectus_pipeline/data/text/HKIPO-MB6872.jsonl",
    }
    for key, path in bound.items():
        assert hashlib.sha256(path.read_bytes()).hexdigest() == review[key], key
    payload = json.loads((HERE / "supplemental_fields.json").read_text())
    approved = {
        "Underwriting base commission rate (%)": 0.03,
        "Underwriting discretionary incentive fee rate (%)": 0.01,
        "Total underwriting fee rate (%)": 0.04,
        "Year-1 net sales (original, pre-annualization)": 0,
    }
    assert {x["header"]: x["value"] for x in payload["entries"]} == approved
    assert review["allowed_supplemental_write"]
    book = ROOT / "pipeline/cohorts/HKIPO-MB2026Q2.xlsx"
    receipt = []
    with workbook_transaction(book, operation="6872-reviewed-supplement") as wb:
        ws = wb["NLR"]
        rows = [r for r in range(2, ws.max_row + 1) if ws.cell(r, 2).value == "6872.HK"]
        assert len(rows) == 1
        for header, value in approved.items():
            cols = [c for c in range(1, ws.max_column + 1) if ws.cell(1, c).value == header]
            assert len(cols) == 1, header
            cell = ws.cell(rows[0], cols[0])
            receipt.append({"header": header, "cell": cell.coordinate, "before": cell.value, "after": value})
            cell.value = value
    (HERE / "supplement_write_receipt.json").write_text(json.dumps({"review": "final_review.json", "payload_sha256": review["payload_sha256"], "changes": receipt}, indent=2) + "\n")
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == "__main__":
    main()
