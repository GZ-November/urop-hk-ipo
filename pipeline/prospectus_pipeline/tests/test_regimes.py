"""制度分期 (Col 201 FINI / Col 202 2025 pricing reform) 按上市日期推导且 fail-closed。

回归：2025Q1/Q2 共 42 家（上市 2025-01-08 至 2025-06-30）曾因改革分界点误设为
2025-01-01 被标为 POST_2025_REFORM；实际改革生效日为 2025-08-04。
"""
import csv
import datetime as dt
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import master_contracts
from expansion_mapping import ExpansionValueMapper
from regimes import FINI_CUTOFF_DATE, REFORM_2025_DATE, fini_regime, pricing_reform_regime
from sample_builder import audit_candidate


def _candidate(listing_date):
    return {
        "stock_code": "1234.HK",
        "company_name": "Example Holdings Limited",
        "raw_price_str": "10.00",
        "raw_funds_str": "1,000,000,000",
        "funds_raised_public_hkd": 1.0e9,
        "funds_raised_int_hkd": None,
        "offer_price_hkd": 10.0,
        "listing_date": listing_date,
        "sponsors": "Example Capital",
    }


class RegimeCutoffTests(unittest.TestCase):
    def test_cutoff_dates(self):
        self.assertEqual(FINI_CUTOFF_DATE, dt.date(2023, 11, 22))
        self.assertEqual(REFORM_2025_DATE, dt.date(2025, 8, 4))

    def test_boundaries(self):
        self.assertEqual(fini_regime(dt.date(2023, 11, 21)), "PRE_FINI")
        self.assertEqual(fini_regime(dt.date(2023, 11, 22)), "POST_FINI")
        self.assertEqual(pricing_reform_regime(dt.date(2025, 8, 1)), "PRE_2025_REFORM")
        self.assertEqual(pricing_reform_regime(dt.date(2025, 8, 4)), "POST_2025_REFORM")

    def test_2025_h1_listings_are_post_fini_pre_reform(self):
        for listing in (dt.date(2025, 1, 8), dt.datetime(2025, 3, 31), "2025-06-30"):
            self.assertEqual(fini_regime(listing), "POST_FINI")
            self.assertEqual(pricing_reform_regime(listing), "PRE_2025_REFORM")

    def test_missing_or_invalid_listing_date_fails_closed(self):
        for bad in (None, "", "NA", "30/06/25"):
            with self.assertRaises(ValueError):
                fini_regime(bad, "1234.HK")
            with self.assertRaises(ValueError):
                pricing_reform_regime(bad, "1234.HK")


class SampleBuilderRegimeTests(unittest.TestCase):
    def test_included_candidate_regimes_follow_listing_date(self):
        cand = audit_candidate(_candidate(dt.date(2025, 1, 8)))
        self.assertEqual(cand["inclusion_status"], "INCLUDED")
        self.assertEqual(cand["fini_regime"], "POST_FINI")
        self.assertEqual(cand["pricing_reform_regime"], "PRE_2025_REFORM")

    def test_included_candidate_without_listing_date_fails_closed(self):
        with self.assertRaises(ValueError):
            audit_candidate(_candidate(None))


class ExpansionMapperRegimeTests(unittest.TestCase):
    def _mapper(self, master_row):
        with tempfile.TemporaryDirectory() as tmp:
            out_master = Path(tmp)
            for name, fields in (
                (master_contracts.STABILIZATION_EVENTS, master_contracts.STABILIZATION_EVENTS_COLS),
                (master_contracts.HORIZON_SUMMARY, master_contracts.HORIZON_SUMMARY_COLS),
                (master_contracts.DAILY_MARKET_PANEL, master_contracts.DAILY_MARKET_PANEL_COLS),
                (master_contracts.LOCKUP_EVENTS, master_contracts.LOCKUP_EVENTS_COLS),
            ):
                with (out_master / name).open("w", newline="", encoding="utf-8-sig") as stream:
                    csv.DictWriter(stream, fieldnames=fields).writeheader()
            with (out_master / "issuer_master.csv").open("w", newline="", encoding="utf-8-sig") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(master_row))
                writer.writeheader()
                writer.writerow(master_row)
            mapper = ExpansionValueMapper(out_master)
            mapper.load_sources()
        return mapper

    def test_workbook_listing_date_overrides_stale_master_regime(self):
        mapper = self._mapper({
            "stock_code": "1234.HK", "listing_date": "2025-01-08",
            "fini_regime": "PRE_FINI", "pricing_reform_regime": "POST_2025_REFORM",
        })
        self.assertEqual(mapper.value_for("1234.HK", 201, dt.date(2025, 1, 8)), ("POST_FINI", "@"))
        self.assertEqual(mapper.value_for("1234.HK", 202, dt.date(2025, 1, 8)), ("PRE_2025_REFORM", "@"))

    def test_falls_back_to_master_listing_date(self):
        mapper = self._mapper({"stock_code": "1234.HK", "listing_date": "2025-09-01"})
        self.assertEqual(mapper.value_for("1234.HK", 202), ("POST_2025_REFORM", "@"))

    def test_no_listing_date_anywhere_fails_closed(self):
        mapper = ExpansionValueMapper(Path("unused"))
        for column in (201, 202):
            with self.assertRaises(ValueError):
                mapper.value_for("missing.HK", column)


if __name__ == "__main__":
    unittest.main()
