import csv
import datetime as dt
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from expansion_mapping import EXPANSION_COLUMNS, ExpansionValueMapper


class ExpansionMappingTests(unittest.TestCase):
    def test_catalog_covers_all_41_expansion_columns(self):
        self.assertEqual(len(EXPANSION_COLUMNS), 41)
        self.assertEqual([column[0] for column in EXPANSION_COLUMNS], list(range(162, 203)))
        mapper = ExpansionValueMapper(Path("unused"))
        for column, _, expected_format, _ in EXPANSION_COLUMNS:
            self.assertEqual(mapper.value_for("missing.HK", column, "2026-01-10")[1], expected_format)

    def test_mapper_resolves_values_from_master_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_master = Path(tmp)
            with (out_master / "horizon_summary.csv").open("w", newline="", encoding="utf-8-sig") as stream:
                writer = csv.DictWriter(stream, fieldnames=["stock_code", "horizon", "bhr_from_day1", "wr_hsi"])
                writer.writeheader()
                writer.writerow({"stock_code": "1234.HK", "horizon": "Day_5", "bhr_from_day1": "0.125", "wr_hsi": "1.2"})
            with (out_master / "stabilization_events.csv").open("w", newline="", encoding="utf-8-sig") as stream:
                writer = csv.DictWriter(stream, fieldnames=["stock_code", "stabilizing_manager", "stabilization_period_end"])
                writer.writeheader()
                writer.writerow({"stock_code": "1234.HK", "stabilizing_manager": "Example Sponsor", "stabilization_period_end": "2026-02-01"})

            with (out_master / "daily_market_panel.csv").open("w", newline="", encoding="utf-8-sig") as stream:
                csv.DictWriter(stream, fieldnames=["stock_code", "amihud_illiq", "zero_volume_flag", "daily_return", "max_drawdown"]).writeheader()
            with (out_master / "lockup_events.csv").open("w", newline="", encoding="utf-8-sig") as stream:
                csv.DictWriter(stream, fieldnames=["stock_code", "lockup_category"]).writeheader()

            mapper = ExpansionValueMapper(out_master)
            mapper.load_sources()

        self.assertEqual(mapper.value_for("1234.HK", 162), ("Example Sponsor", "@"))
        self.assertEqual(mapper.value_for("1234.HK", 173), (0.125, "0.00%"))
        self.assertEqual(mapper.value_for("1234.HK", 174), (1.2, "0.000"))
        self.assertEqual(mapper.value_for("missing.HK", 173), (None, "0.00%"))

    def test_cornerstone_count_is_never_invented(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_master = Path(tmp)
            for name, fields in {
                "horizon_summary.csv": ["stock_code", "horizon"],
                "stabilization_events.csv": ["stock_code"],
                "daily_market_panel.csv": ["stock_code", "amihud_illiq", "zero_volume_flag", "daily_return", "max_drawdown"],
                "lockup_events.csv": ["stock_code", "lockup_category"],
                "investor_relational.csv": ["stock_code", "cornerstone_flag", "state_owned_flag"],
            }.items():
                with (out_master / name).open("w", newline="", encoding="utf-8-sig") as stream:
                    writer = csv.DictWriter(stream, fieldnames=fields)
                    writer.writeheader()
                    if name == "investor_relational.csv":
                        for _ in range(3):
                            writer.writerow({"stock_code": "1111.HK", "cornerstone_flag": "True",
                                             "state_owned_flag": "False"})
            mapper = ExpansionValueMapper(out_master, no_cornerstone={"2222.HK"})
            mapper.load_sources()

        # counted from investor rows
        self.assertEqual(mapper.value_for("1111.HK", 196), (3, "0"))
        # confirmed no cornerstones -> definite 0
        self.assertEqual(mapper.value_for("2222.HK", 196), (0, "0"))
        # no investor rows and not confirmed absent -> unknown, not a made-up number
        self.assertEqual(mapper.value_for("3333.HK", 196), (None, "0"))


CURATED_COLUMNS = range(162, 201)  # 201-202 由 regime 逻辑负责，不在此测试范围


def _write_csv(path, fieldnames, rows=()):
    with path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _load(out_master, stab=(), horizon=(), daily=(), lockup=(), investor=None, underwriter=None):
    _write_csv(out_master / "stabilization_events.csv",
               ["stock_code", "stabilizing_manager", "stabilization_period_end",
                "stabilization_purchases_occurred", "over_allocation_pct", "option_exercise_date",
                "exercise_pct_of_option", "expired_unexercised"], stab)
    _write_csv(out_master / "horizon_summary.csv",
               ["stock_code", "horizon", "bhr_from_day1", "wr_hsi", "matured", "missing_reason", "actual_date"], horizon)
    _write_csv(out_master / "daily_market_panel.csv",
               ["stock_code", "trade_date", "amihud_illiq", "zero_volume_flag", "daily_return", "max_drawdown"], daily)
    _write_csv(out_master / "lockup_events.csv", ["stock_code", "lockup_category", "expiry_date"], lockup)
    if investor is not None:
        _write_csv(out_master / "investor_relational.csv",
                   ["stock_code", "cornerstone_flag", "pre_ipo_flag", "state_owned_flag", "crossover_flag"], investor)
    if underwriter is not None:
        _write_csv(out_master / "underwriter_relational.csv",
                   ["stock_code", "intermediary_name", "syndicate_role", "commercial_bank_affiliate",
                    "base_commission_pct", "discretionary_incentive_fee_pct", "total_fee_rate_pct"], underwriter)
    mapper = ExpansionValueMapper(out_master)
    mapper.load_sources()
    return mapper


class MissingSourceTests(unittest.TestCase):
    """缺来源 → None；绝不返回历史默认值（CICC / 2 / 2.5 / 1.0 / 3.5 / 4 / 6 / 0.15 ...）。"""

    def test_unloaded_mapper_returns_none_for_all_curated_columns(self):
        mapper = ExpansionValueMapper(Path("unused"))
        for column in CURATED_COLUMNS:
            with self.subTest(column=column):
                self.assertIsNone(mapper.value_for("missing.HK", column)[0])

    def test_issuer_absent_from_every_loaded_source_gets_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            mapper = _load(
                Path(tmp),
                stab=[{"stock_code": "1234.HK", "stabilizing_manager": "Real Manager",
                       "stabilization_period_end": "2025-02-01", "expired_unexercised": "False"}],
                horizon=[{"stock_code": "1234.HK", "horizon": "Day_5", "bhr_from_day1": "0.1"}],
                daily=[{"stock_code": "1234.HK", "amihud_illiq": "0.5", "zero_volume_flag": "False",
                        "daily_return": "0.01", "max_drawdown": "-0.2"}],
                investor=[{"stock_code": "1234.HK", "cornerstone_flag": "True", "pre_ipo_flag": "False"}],
                underwriter=[{"stock_code": "1234.HK", "intermediary_name": "Real Sponsor",
                              "syndicate_role": "Sole Sponsor", "base_commission_pct": "2.0"}],
            )
        for column in CURATED_COLUMNS:
            with self.subTest(column=column):
                self.assertIsNone(mapper.value_for("9999.HK", column)[0])

    def test_partial_stabilization_row_does_not_impute(self):
        with tempfile.TemporaryDirectory() as tmp:
            mapper = _load(Path(tmp), stab=[{
                "stock_code": "1234.HK", "stabilizing_manager": "",
                "stabilization_period_end": "2025-02-01", "expired_unexercised": "False",
            }])
        self.assertIsNone(mapper.value_for("1234.HK", 162)[0])   # 不代填 CICC
        self.assertIsNone(mapper.value_for("1234.HK", 164)[0])   # 不把空值当 0
        self.assertIsNone(mapper.value_for("1234.HK", 166)[0])   # 不代填 15%
        self.assertIsNone(mapper.value_for("1234.HK", 167)[0])   # 不以稳价期结束日代填行使日
        self.assertIsNone(mapper.value_for("1234.HK", 169)[0])   # "False" 字符串不应推出 100%/0%
        self.assertEqual(mapper.value_for("1234.HK", 163)[0], "2025-02-01")

    def test_expired_unexercised_option_is_zero_percent(self):
        with tempfile.TemporaryDirectory() as tmp:
            mapper = _load(Path(tmp), stab=[{"stock_code": "1234.HK", "expired_unexercised": "True"}])
        self.assertEqual(mapper.value_for("1234.HK", 169), (0.0, "0.00%"))

    def test_stabilizing_manager_rows_are_not_sponsors(self):
        with tempfile.TemporaryDirectory() as tmp:
            mapper = _load(Path(tmp), underwriter=[{
                "stock_code": "1234.HK", "intermediary_name": "Stab Co", "syndicate_role": "Stabilizing Manager",
                "commercial_bank_affiliate": "False", "base_commission_pct": "", "total_fee_rate_pct": "",
            }])
        for column in (190, 191, 192, 193, 194, 195):
            with self.subTest(column=column):
                self.assertIsNone(mapper.value_for("1234.HK", column)[0])

    def test_sponsor_rows_resolve_from_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            mapper = _load(Path(tmp), underwriter=[
                {"stock_code": "1234.HK", "intermediary_name": "Bank Sponsor", "syndicate_role": "Joint Sponsor",
                 "commercial_bank_affiliate": "True", "base_commission_pct": "2.0",
                 "discretionary_incentive_fee_pct": "", "total_fee_rate_pct": "2.0"},
                {"stock_code": "1234.HK", "intermediary_name": "Other Sponsor", "syndicate_role": "Joint Sponsor",
                 "commercial_bank_affiliate": "False"},
            ])
        self.assertEqual(mapper.value_for("1234.HK", 190), ("Bank Sponsor", "@"))
        self.assertEqual(mapper.value_for("1234.HK", 191), (2, "0"))
        self.assertEqual(mapper.value_for("1234.HK", 192), (1, "0"))
        self.assertEqual(mapper.value_for("1234.HK", 193), (0.02, "0.00%"))
        self.assertIsNone(mapper.value_for("1234.HK", 194)[0])
        self.assertEqual(mapper.value_for("1234.HK", 195), (0.02, "0.00%"))

    def test_daily_stats_without_observations_are_none_but_real_zero_survives(self):
        with tempfile.TemporaryDirectory() as tmp:
            mapper = _load(Path(tmp), horizon=[
                {"stock_code": code, "horizon": "Month_6", "matured": "True", "missing_reason": "",
                 "actual_date": "2026-07-01"} for code in ("1234.HK", "5678.HK")
            ], daily=[
                {"stock_code": "1234.HK", "trade_date": "2026-01-01", "amihud_illiq": "", "zero_volume_flag": "", "daily_return": "", "max_drawdown": ""},
                {"stock_code": "5678.HK", "trade_date": "2026-01-01", "amihud_illiq": "0.0", "zero_volume_flag": "False", "daily_return": "0.01", "max_drawdown": "0"},
                {"stock_code": "5678.HK", "trade_date": "2026-01-02", "amihud_illiq": "0.0", "zero_volume_flag": "False", "daily_return": "0.01", "max_drawdown": "0"},
            ])
        for column in (181, 182, 183, 184):
            with self.subTest(column=column):
                self.assertIsNone(mapper.value_for("1234.HK", column)[0])
                self.assertEqual(mapper.value_for("5678.HK", column)[0], 0)

    def test_six_month_stats_require_matured_horizon_without_missing_reason(self):
        for horizon in ([],
                        [{"horizon": "Month_6", "matured": "False", "actual_date": "2026-07-01"}],
                        [{"horizon": "Month_6", "matured": "True", "missing_reason": "benchmark unavailable",
                          "actual_date": "2026-07-01"}]):
            with self.subTest(horizon=horizon), tempfile.TemporaryDirectory() as tmp:
                mapper = _load(Path(tmp), horizon=[{"stock_code": "1234.HK", **row} for row in horizon], daily=[
                    {"stock_code": "1234.HK", "trade_date": "2026-01-01", "amihud_illiq": "1",
                     "zero_volume_flag": "False", "daily_return": "0.01", "max_drawdown": "0.2"},
                ])
                for column in (181, 182, 183, 184):
                    self.assertIsNone(mapper.value_for("1234.HK", column)[0], column)

    def test_six_month_calendar_window_uses_all_observed_days_through_actual_date(self):
        first, cutoff = dt.date(2026, 1, 1), dt.date(2026, 6, 30)
        dates = [first + dt.timedelta(days=i) for i in range((cutoff - first).days + 1)
                 if (first + dt.timedelta(days=i)).weekday() < 5]
        self.assertGreater(len(dates), 126)
        daily = [{"stock_code": "1234.HK", "trade_date": date.isoformat(), "amihud_illiq": str(i + 1),
                  "zero_volume_flag": "True", "daily_return": "0.01", "max_drawdown": "0.2"}
                 for i, date in enumerate(dates)]
        daily.append({"stock_code": "1234.HK", "trade_date": "2026-07-01", "amihud_illiq": "100000",
                      "zero_volume_flag": "True", "daily_return": "3", "max_drawdown": "0.9"})
        with tempfile.TemporaryDirectory() as tmp:
            mapper = _load(Path(tmp), horizon=[{
                "stock_code": "1234.HK", "horizon": "Month_6", "matured": "True",
                "missing_reason": "", "actual_date": cutoff.isoformat(),
            }], daily=list(reversed(daily)))
        self.assertAlmostEqual(mapper.value_for("1234.HK", 181)[0], (len(dates) + 1) / 2)
        self.assertEqual(mapper.value_for("1234.HK", 182)[0], len(dates))
        self.assertEqual(mapper.value_for("1234.HK", 183)[0], 0)
        self.assertEqual(mapper.value_for("1234.HK", 184)[0], 0.2)

    def test_missing_window_dates_leave_six_month_stats_blank(self):
        for actual_date, trade_date in (("", "2026-01-01"), ("2026-07-01", "")):
            with self.subTest(actual_date=actual_date, trade_date=trade_date), tempfile.TemporaryDirectory() as tmp:
                mapper = _load(Path(tmp), horizon=[{
                    "stock_code": "1234.HK", "horizon": "Month_6", "matured": "True",
                    "missing_reason": "", "actual_date": actual_date,
                }], daily=[{"stock_code": "1234.HK", "trade_date": trade_date, "amihud_illiq": "1",
                           "zero_volume_flag": "False", "daily_return": "0.01", "max_drawdown": "0.2"}])
                for column in (181, 182, 183, 184):
                    self.assertIsNone(mapper.value_for("1234.HK", column)[0], column)

    def test_malformed_window_dates_fail_closed(self):
        for actual_date, trade_date in (("bad-date", "2026-01-01"), ("2026-07-01", "bad-date")):
            with self.subTest(actual_date=actual_date, trade_date=trade_date), tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(ValueError):
                    _load(Path(tmp), horizon=[{
                        "stock_code": "1234.HK", "horizon": "Month_6", "matured": "True",
                        "missing_reason": "", "actual_date": actual_date,
                    }], daily=[{"stock_code": "1234.HK", "trade_date": trade_date, "amihud_illiq": "1",
                               "zero_volume_flag": "False", "daily_return": "0.01", "max_drawdown": "0.2"}])

    def test_investor_rows_give_real_counts_including_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            mapper = _load(Path(tmp), investor=[
                {"stock_code": "1234.HK", "cornerstone_flag": "False", "pre_ipo_flag": "True", "state_owned_flag": "True"},
            ])
        self.assertEqual(mapper.value_for("1234.HK", 196), (0, "0"))
        self.assertEqual(mapper.value_for("1234.HK", 197), (0, "0"))
        self.assertEqual(mapper.value_for("1234.HK", 199), (1, "0"))
        self.assertEqual(mapper.value_for("1234.HK", 200), (1, "0"))

if __name__ == "__main__":
    unittest.main()
