"""The allot validation context must not change when the prospectus is written back."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from validate import _allot_context  # noqa: E402

CODE = "8610.HK"


def make_cfg(tmp: Path, sheet_offer, payload_offer):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "NLR"
    ws.append(["file", "Stock Code", "Name", "", "", "", "", "", "", "",
               "IPO Subscription Price (HK$)", "", "Global Offering (without option)"])
    ws.append([1, CODE, "Issuer", None, None, None, None, None, None, None, 0.6, None, sheet_offer])
    wb.save(tmp / "cohort.xlsx")
    out = tmp / "out"
    (out / "extracted").mkdir(parents=True)
    if payload_offer is not None:
        payload = {"code": CODE, "fields": {"col_M": {"value": payload_offer, "page": 1, "quote": "q"}}}
        (out / "extracted" / "HKIPO-MB8610.json").write_text(json.dumps(payload), encoding="utf-8")
    return {"_ws": tmp, "_root": tmp, "workbook": "cohort.xlsx", "sheet": "NLR",
            "id_columns": {"stock_code": "B"}, "data_start_row": 2,
            "dataset": {"board": "gem"}, "paths": {"out": out, "allot_out": tmp / "allot_out"}}


class AllotContextStabilityTests(unittest.TestCase):
    def context_for(self, sheet_offer, payload_offer):
        with tempfile.TemporaryDirectory() as raw:
            return _allot_context(make_cfg(Path(raw), sheet_offer, payload_offer))

    def test_initial_offer_is_identical_before_and_after_prospectus_write_back(self):
        before = self.context_for(None, 125_000_000)
        after = self.context_for(125_000_000.0, 125_000_000)
        self.assertEqual(before, after)
        self.assertEqual(before[CODE]["initial_offer"], 125_000_000)

    def test_workbook_value_is_used_when_no_prospectus_payload_exists(self):
        self.assertEqual(self.context_for(90_000_000, None)[CODE]["initial_offer"], 90_000_000)

    def test_unusable_payload_value_falls_back_to_the_workbook(self):
        self.assertEqual(self.context_for(90_000_000, "NaN")[CODE]["initial_offer"], 90_000_000)


if __name__ == "__main__":
    unittest.main()
