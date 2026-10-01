"""master 面板 producer 不得编造缺来源字段。

stabilization_panel 曾在稳价经理人正则未命中时写入
"China International Capital Corporation / Sponsor-OC"，并以上市日 +30 天、
15% 超额配售、全额行使等惯例值代填；relational_tables 曾硬编码 1.0% 酌情奖励费、
2.5% 基础佣金，且把小数费率 (0.015) 与百分点 (1.0) 相加。
这些值经 expansion_mapping 流入工作簿 162-200 列。
"""
import csv
import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

import master_contracts  # noqa: E402
from expansion_mapping import ExpansionValueMapper  # noqa: E402
from relational_tables import RelationalTableEngine, commission_pct, split_sponsors  # noqa: E402
from stabilization_panel import StabilizationPanelEngine, extract_manager  # noqa: E402

CODE = "1234.HK"


def make_cfg(tmp: Path) -> dict:
    return {"paths": {"out": tmp / "out", "allot_out": tmp / "out" / "allot", "data": tmp / "data"}}


def write_text(tmp: Path, text: str, kind: str = "greenshoe") -> None:
    text_dir = tmp / "out" / "allot" / ("greenshoe/text" if kind == "greenshoe" else "text")
    text_dir.mkdir(parents=True, exist_ok=True)
    (text_dir / "HKIPO-MB1234.jsonl").write_text(
        json.dumps({"page": 1, "text": text}, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def run_stabilization(tmp: Path) -> dict:
    engine = StabilizationPanelEngine(cfg=make_cfg(tmp))
    out = engine.run([{"stock_code": CODE, "listing_date": "2026-07-10"}])
    self_check = out.read_text(encoding="utf-8-sig")
    assert "Sponsor-OC" not in self_check, self_check
    rows = master_contracts.load_rows(out, master_contracts.STABILIZATION_EVENTS_COLS)
    assert len(rows) == 1
    return rows[0]


class StabilizingManagerExtractionTests(unittest.TestCase):
    def test_borrowed_by_phrase_with_pdf_line_break(self):
        text = ("Shares borrowed by China International Capital Corporation Hong Kong Securities \n"
                "Limited, the Stabilizing Manager, or its affiliate")
        self.assertEqual(extract_manager(text),
                         "China International Capital Corporation Hong Kong Securities Limited")

    def test_british_spelling_stabilization_manager(self):
        text = "the stabilizing actions undertaken by Haitong International Securities Company Limited, the  Stabilization Manager"
        self.assertEqual(extract_manager(text), "Haitong International Securities Company Limited")

    def test_as_stabilizing_manager_strips_affiliate_parenthetical(self):
        text = ("In connection with the Global Offering, CMB International Capital Limited (or its affiliates or any "
                "person acting for \nit), as the stabilizing manager (the “Stabilizing Manager”)")
        self.assertEqual(extract_manager(text), "CMB International Capital Limited")

    def test_as_stabilizing_manager_keeps_name_parenthetical(self):
        text = ("In connection with the Global Offering, Huatai Financial Holdings (Hong Kong) Limited as "
                "stabilizing manager (the \n“Stabilizing Manager”)")
        self.assertEqual(extract_manager(text), "Huatai Financial Holdings (Hong Kong) Limited")

    def test_unmatched_text_returns_none(self):
        self.assertIsNone(extract_manager("Stabilizing actions were undertaken by the Stabilizing Manager."))


class StabilizationPanelNoFabricationTests(unittest.TestCase):
    def test_no_source_text_leaves_every_parsed_field_blank(self):
        with tempfile.TemporaryDirectory() as tmp:
            row = run_stabilization(Path(tmp))

        self.assertEqual(row["stabilizing_manager"], "")
        self.assertEqual(row["stabilizing_manager_status"], "NO_SOURCE_TEXT")
        # 不得按上市日 +30 天推算稳价结束日
        self.assertEqual(row["stabilization_period_end"], "")
        self.assertEqual(row["announcement_date"], "")
        for col in ("stabilization_purchases_occurred", "over_allocation_pct", "stock_borrowing_arrangement",
                    "option_exercise_date", "shares_issued_under_option", "exercise_pct_of_option",
                    "expired_unexercised", "aggregate_stabilization_shares", "source_url"):
            self.assertEqual(row[col], "", col)
        self.assertIn("stabilizing_manager", row["missing_fields"].split(";"))
        self.assertIn("stabilization_period_end", row["missing_fields"].split(";"))

    def test_manager_regex_miss_is_blank_and_logged(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_text(Path(tmp), "The stabilization period in connection with the Global Offering ended on "
                                  "Friday, August 7, 2026.")
            with self.assertLogs("stabilization_panel", level="WARNING") as logs:
                row = run_stabilization(Path(tmp))

        self.assertEqual(row["stabilizing_manager"], "")
        self.assertEqual(row["stabilizing_manager_status"], "NOT_FOUND")
        self.assertTrue(any(CODE in line and "NOT_FOUND" in line for line in logs.output))
        self.assertEqual(row["stabilization_period_end"], "2026-08-07")
        self.assertEqual(row["announcement_date"], "")

    def test_borrowing_stabilizing_actions_do_not_imply_market_purchases(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_text(Path(tmp), "The stabilizing actions undertaken by Example Securities Limited, the "
                                  "Stabilizing Manager, consisted of borrowing 1,500,000 Offer Shares "
                                  "under the Stock Borrowing Agreement.")
            row = run_stabilization(Path(tmp))

        self.assertEqual(row["stabilization_purchases_occurred"], "")
        self.assertEqual(row["aggregate_stabilization_shares"], "")

    def test_no_manager_appointed_is_flagged_not_filled(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_text(Path(tmp), "No stabilizing manager will be appointed, and it is anticipated that no "
                                  "stabilization will take place.", kind="allot")
            row = run_stabilization(Path(tmp))

        self.assertEqual(row["stabilizing_manager"], "")
        self.assertEqual(row["stabilizing_manager_status"], "NOT_APPOINTED")
        self.assertEqual(row["source_url"], "HKEXnews Allotment Results Announcement")

    def test_over_allocation_without_disclosed_pct_or_exercise_stays_blank(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_text(Path(tmp), "There has been an over-allocation of 1,500,000 Offer Shares in the "
                                  "International Offering.")
            row = run_stabilization(Path(tmp))

        self.assertEqual(row["over_allocation_shares"], "1500000.0")
        self.assertEqual(row["over_allocation_pct"], "")        # 不以 15% 惯例代填
        self.assertEqual(row["shares_issued_under_option"], "")  # 不默认全额行使
        self.assertEqual(row["exercise_pct_of_option"], "")
        self.assertEqual(row["expired_unexercised"], "")
        self.assertEqual(row["stock_borrowing_arrangement"], "")

    def test_disclosed_full_exercise_is_parsed(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_text(Path(tmp), (
                "4,379,640 Shares borrowed by Morgan Stanley Asia Limited, the Stabilizing Manager, under the "
                "Stock Borrowing Agreement. There has been an over-allocation of 4,379,640 Offer Shares. "
                "The Over-allotment Option has been fully exercised on Wednesday, January 28, 2026, in respect "
                "of an aggregate of 4,379,640 Shares. The stabilization period in connection with the Global "
                "Offering ended on Wednesday, January 28, 2026."))
            row = run_stabilization(Path(tmp))

        self.assertEqual(row["stabilizing_manager"], "Morgan Stanley Asia Limited")
        self.assertEqual(row["stabilizing_manager_status"], "PARSED")
        self.assertEqual(row["shares_issued_under_option"], "4379640.0")
        self.assertEqual(row["exercise_pct_of_option"], "100.0")
        self.assertEqual(row["expired_unexercised"], "False")
        self.assertEqual(row["option_exercise_date"], "2026-01-28")
        self.assertEqual(row["stock_borrowing_arrangement"], "Delayed delivery arrangement / Stock borrowing")

    def test_partial_exercise_without_share_count_is_not_assumed_half(self):
        with tempfile.TemporaryDirectory() as tmp:
            write_text(Path(tmp), "There has been an over-allocation of 2,000,000 Offer Shares. "
                                  "The Company announces the partial exercise of the Over-allotment Option.")
            row = run_stabilization(Path(tmp))

        self.assertEqual(row["shares_issued_under_option"], "")
        self.assertEqual(row["exercise_pct_of_option"], "")


class StabilizationEventCoverageTests(unittest.TestCase):
    """A named event window needs its full observed endpoints and zero-volume days."""

    def compute(self, count: int, end_index: int, zero_first_turnover: bool = False) -> dict:
        engine = object.__new__(StabilizationPanelEngine)
        first = dt.date(2026, 1, 1)
        bars = [{"date": first + dt.timedelta(days=i), "close": 100 + i,
                 "turnover": (100 if i <= end_index else 50)} for i in range(count)]
        if zero_first_turnover:
            bars[0]["turnover"] = 0
        engine.daily_bars = {CODE: bars}
        return engine.compute_event_windows({
            "stock_code": CODE,
            "stabilization_period_end": (first + dt.timedelta(days=end_index)).isoformat(),
        })

    def test_cliff_window_requires_both_endpoints(self):
        for count, end_index in ((30, 4), (10, 5)):
            with self.subTest(count=count, end_index=end_index):
                self.assertIsNone(self.compute(count, end_index)["cliff_return_m5_p5"])

    def test_post20_and_volume_decay_wait_for_twenty_post_event_bars(self):
        row = self.compute(25, 5)
        self.assertAlmostEqual(row["cliff_return_m5_p5"], 110 / 100 - 1)
        self.assertIsNone(row["post_stab_return_p20"])
        self.assertIsNone(row["volume_decay_post_stab"])

    def test_complete_windows_include_actual_zero_turnover_in_average(self):
        row = self.compute(26, 5, zero_first_turnover=True)
        self.assertAlmostEqual(row["cliff_return_m5_p5"], 0.1)
        self.assertAlmostEqual(row["post_stab_return_p20"], 125 / 105 - 1, places=6)
        self.assertAlmostEqual(row["volume_decay_post_stab"], 0.6)


class RelationalTablesNoFabricationTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.master = self.tmp / "out" / "master"

    def tearDown(self):
        self._tmp.cleanup()

    def write_extracted(self, fields: dict) -> None:
        path = self.tmp / "out" / "extracted" / "HKIPO-MB1234.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"fields": {k: {"value": v} for k, v in fields.items()}}), encoding="utf-8")

    def write_issuer_master(self, sponsors: str) -> None:
        write_csv(self.master / "issuer_master.csv", [{"stock_code": CODE, "sponsors": sponsors}])

    def write_stab(self, manager: str) -> None:
        write_csv(self.master / master_contracts.STABILIZATION_EVENTS,
                  [{"stock_code": CODE, "stabilizing_manager": manager}])

    def run_engine(self, issuer: dict | None = None) -> list[dict]:
        engine = RelationalTableEngine(cfg=make_cfg(self.tmp))
        _, syn_path = engine.run([issuer or {"stock_code": CODE, "company_name": "Test Co"}])
        # 产出须通过 fail-closed 加载器
        return master_contracts.load_rows(syn_path, master_contracts.UNDERWRITER_RELATIONAL_COLS)

    def investor_rows(self, fields: dict) -> list[dict]:
        self.write_extracted(fields)
        engine = RelationalTableEngine(cfg=make_cfg(self.tmp))
        issuer = {"stock_code": CODE, "company_name": "Test Co", "listing_date": "2026-01-02"}
        return engine.process_investors([issuer])

    def test_unknown_investor_flags_stay_unknown_not_zero(self):
        rows = self.investor_rows({"col_pre_ipo_investors": "Alpha Capital Fund; Beta Ventures Fund",
                                   "col_vc_backed": "NaN", "col_pe_backed": 1, "col_gov_backed": "NaN",
                                   "col_vc_board_seat": "NaN"})
        self.assertEqual(len(rows), 2)
        for row in rows:
            self.assertIsNone(row["board_seat_flag"])
            self.assertIsNone(row["lockup_expiry_date"])  # no generic listing+183 days fabrication
            self.assertEqual(row["investor_category"], "Pre-IPO PE")  # PE flag survives sibling NaN flags

    def test_explicit_board_seat_zero_and_one_are_kept(self):
        for value, expected in ((1, True), (0, False), ("1", True)):
            rows = self.investor_rows({"col_pre_ipo_investors": "Alpha Capital Fund", "col_vc_board_seat": value})
            self.assertIs(rows[0]["board_seat_flag"], expected)

    def test_commission_pct_converts_decimal_to_percent_points(self):
        self.assertEqual(commission_pct(0.015), 1.5)
        self.assertEqual(commission_pct("0.03"), 3.0)
        self.assertIsNone(commission_pct(None))
        self.assertIsNone(commission_pct(""))
        self.assertIsNone(commission_pct("NaN"))
        self.assertIsNone(commission_pct(2.5))  # 单位不明，不猜

    def test_split_sponsors_ignores_pdf_line_breaks(self):
        raw = ("China International Capital Corporation\nHong Kong Securities Limited / \n"
               "Ping An of China Capital \n(Hong Kong) Company Limited / \nBOCI Asia Limited")
        self.assertEqual(split_sponsors(raw), [
            "China International Capital Corporation Hong Kong Securities Limited",
            "Ping An of China Capital (Hong Kong) Company Limited",
            "BOCI Asia Limited",
        ])

    def test_sponsor_rows_from_issuer_master_with_percent_fees_and_blank_incentive(self):
        self.write_issuer_master("China International Capital Corporation\nHong Kong Securities Limited / \n"
                                 "BOCI Asia Limited")
        self.write_stab("Citigroup Global Markets Asia Limited")
        self.write_extracted({"col_AO": 0.015, "col_AP": 0.02})
        rows = self.run_engine()

        roles = [(r["syndicate_role"], r["intermediary_name"]) for r in rows]
        self.assertEqual(roles, [
            ("Joint Sponsor", "China International Capital Corporation Hong Kong Securities Limited"),
            ("Joint Sponsor", "BOCI Asia Limited"),
            ("Stabilizing Manager", "Citigroup Global Markets Asia Limited"),
        ])
        self.assertEqual([r["base_commission_pct"] for r in rows], ["1.5", "1.5", "2.0"])
        for r in rows:
            self.assertEqual(r["discretionary_incentive_fee_pct"], "")
            self.assertEqual(r["total_fee_rate_pct"], "")

    def test_sponsor_that_is_stabilizing_manager_gets_no_duplicate_row(self):
        self.write_issuer_master("Morgan Stanley Asia Limited /\nGF Capital (Hong Kong) Limited")
        self.write_stab("Morgan Stanley Asia \nLimited")
        rows = self.run_engine()

        self.assertEqual([r["syndicate_role"] for r in rows], ["Joint Sponsor", "Joint Sponsor"])
        self.assertEqual([r["is_stabilizing_manager"] for r in rows], ["True", "False"])

    def test_missing_commission_source_is_blank_not_default(self):
        self.write_issuer_master("Huatai Financial Holdings (Hong Kong) Limited")
        rows = self.run_engine()

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["syndicate_role"], "Sole Sponsor")
        self.assertEqual(rows[0]["base_commission_pct"], "")
        self.assertEqual(rows[0]["total_fee_rate_pct"], "")

    def test_out_of_range_commission_is_blank_and_logged(self):
        self.write_issuer_master("Huatai Financial Holdings (Hong Kong) Limited")
        self.write_extracted({"col_AO": 2.5})
        with self.assertLogs("relational_tables", level="WARNING") as logs:
            rows = self.run_engine()

        self.assertEqual(rows[0]["base_commission_pct"], "")
        self.assertTrue(any("col_AO" in line for line in logs.output))

    def test_placeholder_stabilizing_manager_in_stale_csv_is_ignored(self):
        self.write_issuer_master("Huatai Financial Holdings (Hong Kong) Limited")
        self.write_stab("China International Capital Corporation / Sponsor-OC")
        with self.assertLogs("relational_tables", level="WARNING"):
            rows = self.run_engine()

        self.assertEqual([r["syndicate_role"] for r in rows], ["Sole Sponsor"])
        self.assertNotIn("Sponsor-OC", json.dumps(rows))

    def test_issuer_sponsors_key_takes_precedence(self):
        self.write_issuer_master("Other Sponsor Limited")
        rows = self.run_engine({"stock_code": CODE, "sponsors": "Given Sponsor Limited"})
        self.assertEqual([r["intermediary_name"] for r in rows], ["Given Sponsor Limited"])


class ProducerToExpansionUnitTests(unittest.TestCase):
    """producer 输出经 expansion_mapping 后，费率须为正确的 Excel 小数（1.5% → 0.015）。"""

    def test_base_commission_and_manager_reach_workbook_cells_unfabricated(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            master = tmp / "out" / "master"
            write_csv(master / "issuer_master.csv", [{"stock_code": CODE, "sponsors": "BOCI Asia Limited"}])
            extracted = tmp / "out" / "extracted" / "HKIPO-MB1234.json"
            extracted.parent.mkdir(parents=True, exist_ok=True)
            extracted.write_text(json.dumps({"fields": {"col_AO": {"value": 0.015}}}), encoding="utf-8")

            StabilizationPanelEngine(cfg=make_cfg(tmp)).run([{"stock_code": CODE, "listing_date": "2026-07-10"}])
            RelationalTableEngine(cfg=make_cfg(tmp)).run([{"stock_code": CODE}])
            write_csv(master / master_contracts.HORIZON_SUMMARY, [{"stock_code": CODE, "horizon": "Day_1"}])
            write_csv(master / master_contracts.DAILY_MARKET_PANEL, [dict.fromkeys(
                master_contracts.DAILY_MARKET_PANEL_COLS, "")])
            write_csv(master / master_contracts.LOCKUP_EVENTS, [{"stock_code": CODE, "lockup_category": "X"}])

            mapper = ExpansionValueMapper(master)
            mapper.load_sources()

        manager, _ = mapper.value_for(CODE, 162)
        self.assertIn(manager, (None, ""))
        base, fmt = mapper.value_for(CODE, 193)
        self.assertEqual(fmt, "0.00%")
        self.assertAlmostEqual(base, 0.015)


if __name__ == "__main__":
    unittest.main()
