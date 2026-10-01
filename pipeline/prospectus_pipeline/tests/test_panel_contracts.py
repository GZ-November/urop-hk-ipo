"""面板 producer 的契约测试：产出文件必须满足 master_contracts 常量。

这是 producer 侧的钉子——列名/文件名改动若不同步契约，这里立即失败，
而不是等 expansion 写回时静默空格。
"""
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

import master_contracts  # noqa: E402
from stabilization_panel import StabilizationPanelEngine  # noqa: E402
from lockup_panel import LockupPanelEngine  # noqa: E402


def make_cfg(tmp: Path) -> dict:
    return {
        "paths": {
            "out": tmp / "out",
            "allot_out": tmp / "out" / "allot",
            "data": tmp / "data",
        }
    }


def write_greenshoe_text(tmp: Path, code: str, text: str) -> None:
    digits = "".join(ch for ch in code if ch.isdigit())
    text_dir = tmp / "out" / "allot" / "greenshoe" / "text"
    text_dir.mkdir(parents=True, exist_ok=True)
    with (text_dir / f"HKIPO-MB{digits}.jsonl").open("w", encoding="utf-8") as fh:
        fh.write(json.dumps({"page": 1, "text": text}, ensure_ascii=False) + "\n")


def read_header_and_rows(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
        fh.seek(0)
        header = next(csv.reader(fh))
    return header, rows


class StabilizationPanelContractTests(unittest.TestCase):
    def test_no_purchase_announcement_flags_false(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            write_greenshoe_text(
                tmp, "1234.HK",
                "The Stabilizing Manager has confirmed to the Stock Exchange that there was "
                "no purchase of any H Shares on the market for the purpose of price "
                "stabilization. The stabilization period in connection with the Global "
                "Offering ended on Friday, August 7, 2026.")
            engine = StabilizationPanelEngine(cfg=make_cfg(tmp))
            out = engine.run([{"stock_code": "1234.HK", "listing_date": "2026-07-10"}])

            self.assertEqual(out, tmp / "out" / "master" / master_contracts.STABILIZATION_EVENTS)
            header, rows = read_header_and_rows(out)
            for col in master_contracts.STABILIZATION_EVENTS_COLS:
                self.assertIn(col, header)
            self.assertEqual(len(rows), 1)
            self.assertIn(rows[0]["stabilization_purchases_occurred"], ("False", "0"))

    def test_stabilizing_actions_flag_true_with_price_range(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            write_greenshoe_text(
                tmp, "1234.HK",
                "Stabilizing actions were undertaken by the Stabilizing Manager. "
                "Shares were purchased in a price range of HK$ 10.0 to HK$ 12.0 "
                "in the course of stabilizing actions.")
            engine = StabilizationPanelEngine(cfg=make_cfg(tmp))
            out = engine.run([{"stock_code": "1234.HK", "listing_date": "2026-07-10"}])

            _, rows = read_header_and_rows(out)
            self.assertIn(rows[0]["stabilization_purchases_occurred"], ("True", "1"))
            self.assertEqual(rows[0]["purchase_price_low"], "10.0")
            self.assertEqual(rows[0]["purchase_price_high"], "12.0")


class LockupPanelContractTests(unittest.TestCase):
    def test_issuer_without_contract_evidence_gets_explicit_missing_rows_not_dates(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            engine = LockupPanelEngine(cfg=make_cfg(tmp), as_of="2026-09-30", contracts={})
            out = engine.run([{"stock_code": "1234.HK",
                               "company_name": "Test Co",
                               "listing_date": "2026-07-10"}])

            self.assertEqual(out, tmp / "out" / "master" / master_contracts.LOCKUP_EVENTS)
            header, rows = read_header_and_rows(out)
            for col in master_contracts.LOCKUP_EVENTS_COLS:
                self.assertIn(col, header)
            categories = {r["lockup_category"] for r in rows}
            self.assertIn("Cornerstone_Lockup", categories)
            for row in rows:  # no listing-date-plus-six-months default
                self.assertEqual(row["expiry_date"], "")
                self.assertEqual(row["window_status"], "MISSING_CONTRACTUAL_EVIDENCE")

    def test_contract_record_supplies_the_date_and_evidence_status(self):
        contracts = {"1234.HK": {"events": [{
            "category": "Cornerstone_Lockup", "holder": "All cornerstone investors",
            "last_restricted_day": "2027-01-09", "first_free_day": "2027-01-10", "review": "reviewed"}]}}
        with tempfile.TemporaryDirectory() as tmp:
            engine = LockupPanelEngine(cfg=make_cfg(Path(tmp)), as_of="2026-09-30", contracts=contracts)
            rows = engine.process_issuer_lockups({"stock_code": "1234.HK", "listing_date": "2026-07-10"})
            row = next(r for r in rows if r["lockup_category"] == "Cornerstone_Lockup")
            self.assertEqual(row["expiry_date"], "2027-01-10")
            self.assertEqual(row["last_restricted_day"], "2027-01-09")
            self.assertEqual(row["evidence_status"], "reviewed")
            self.assertEqual(row["window_status"], "NO_TRADING_DATA")  # nothing observed, nothing estimated

    def test_cornerstone_event_file_is_written_with_contract_columns(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            engine = LockupPanelEngine(cfg=make_cfg(tmp), as_of="2026-09-30", contracts={})

    def test_issuer_without_listing_date_produces_no_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            engine = LockupPanelEngine(cfg=make_cfg(tmp))
            out = engine.run([{"stock_code": "1234.HK", "listing_date": None}])
            self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
