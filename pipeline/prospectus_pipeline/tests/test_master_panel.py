import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]
WS = ROOT.parent

from master_panel import (
    DERIVED_SPECS,
    MASTER_STEM,
    build_master,
    build_registry,
    column_letter,
    compute_derived_columns,
    load_registry,
    parse_codebook_variables,
    parse_date,
    slugify,
)

SYNTH_HEADERS = [
    "Stock Code",
    "Date of Listing (dd/mm/yy)",
    "IPO Subscription Price (HK$)",
    "Sale Shares",
]


def write_cohort_csv(path: Path, rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(SYNTH_HEADERS)
        writer.writerows(rows)


class UnitTests(unittest.TestCase):
    def test_slugify_variants(self):
        self.assertEqual(slugify("IPO Subscription Price (HK$)"), "ipo_subscription_price_hk")
        self.assertEqual(slugify("Pre-IPO VC/PE backing (1=yes; 0=no)"), "pre_ipo_vc_pe_backing")
        self.assertEqual(slugify("Filing price revision (%)"), "filing_price_revision_pct")
        self.assertEqual(slugify("HKEx file# of the year"), "hkex_file_no_of_the_year")
        self.assertEqual(slugify("Date of Listing (dd/mm/yy)"), "date_of_listing")

    def test_column_letter(self):
        self.assertEqual(column_letter(0), "A")
        self.assertEqual(column_letter(25), "Z")
        self.assertEqual(column_letter(26), "AA")
        self.assertEqual(column_letter(201), "GT")

    def test_parse_date_formats(self):
        from datetime import date
        self.assertEqual(parse_date("2026-07-02"), date(2026, 7, 2))
        self.assertEqual(parse_date("02/07/26"), date(2026, 7, 2))
        self.assertEqual(parse_date("02/07/2026"), date(2026, 7, 2))
        self.assertIsNone(parse_date(""))
        self.assertIsNone(parse_date("not a date"))


class SyntheticMasterTests(unittest.TestCase):
    def build(self, tmp: Path, q1_rows, q2_rows, q2_headers=None):
        write_cohort_csv(tmp / "exports" / "HKIPO-MB2025Q1_clean.csv", q1_rows)
        path2 = tmp / "exports" / "HKIPO-MB2025Q2_clean.csv"
        headers = q2_headers or SYNTH_HEADERS
        with path2.open("w", encoding="utf-8-sig", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(headers)
            writer.writerows(q2_rows)
        return build_master(tmp, registry_path=None, out_dir=tmp)

    def test_aligned_cohorts_merge_with_cohort_column(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            summary = self.build(
                tmp,
                [["0001.HK", "2025-01-10", "1.00", "0"]],
                [["0002.HK", "2025-04-02", "2.00", "0"],
                 ["0003.HK", "2025-05-06", "3.00", "0"]],
            )
            self.assertFalse(summary["hard_errors"])
            self.assertTrue(summary["headers_aligned"])
            self.assertEqual(summary["total_rows"], 3)
            master_path = Path(summary["master_csv"])
            with master_path.open(encoding="utf-8-sig", newline="") as fh:
                rows = list(csv.reader(fh))
            self.assertEqual(rows[0][:2], ["cohort", "cross_cohort_duplicate"])
            self.assertEqual(rows[0][2], "Stock Code")
            self.assertEqual([r[0] for r in rows[1:]], ["2025Q1", "2025Q2", "2025Q2"])
            self.assertEqual([r[1] for r in rows[1:]], ["0", "0", "0"])
            self.assertTrue(Path(summary["drift_report"]).exists())

    def test_header_drift_is_hard_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            summary = self.build(
                tmp,
                [["0001.HK", "2025-01-10", "1.00", "0"]],
                [["0002.HK", "2025-04-02", "0"]],
                q2_headers=SYNTH_HEADERS[:3],
            )
            self.assertFalse(summary["headers_aligned"])
            self.assertTrue(summary["hard_errors"])

    def test_cross_cohort_duplicate_code_is_hard_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            summary = self.build(
                tmp,
                [["0001.HK", "2025-01-10", "1.00", "0"]],
                [["0001.HK", "2025-04-02", "2.00", "0"]],
            )
            self.assertIn("0001.HK", summary["cross_cohort_duplicate_codes"])
            self.assertTrue(summary["hard_errors"])

    def test_out_of_quarter_listing_date_is_warning_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            summary = self.build(
                tmp,
                [["0001.HK", "2025-04-10", "1.00", "0"]],
                [["0002.HK", "2025-05-02", "2.00", "0"]],
            )
            self.assertFalse(summary["hard_errors"])
            self.assertTrue(summary["date_violations"]["2025Q1"])
            self.assertFalse(summary["date_violations"]["2025Q2"])


class IdentityAndDerivedTests(unittest.TestCase):
    ID_HEADERS = [
        "Stock Code",
        "Date of Listing (dd/mm/yy)",
        "Total (without option)",
        "Number of offer shares under the capitalization Issue",
        "Number of offer shares under Capitalization Rest",
        "Global Offering (without option)",
        "New shares",
        "Sale Shares",
    ]

    def rows(self, total, cap_n, cap_rest, global_off, new_shares, sale_shares):
        return [["0001.HK", "2025-02-10", str(total), str(cap_n), str(cap_rest),
                 str(global_off), str(new_shares), str(sale_shares)]]

    def build_identity_cohort(self, tmp: Path, rows):
        path = tmp / "exports" / "HKIPO-MB2025Q1_clean.csv"
        path.parent.mkdir(exist_ok=True)
        with path.open("w", encoding="utf-8-sig", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(self.ID_HEADERS)
            writer.writerows(rows)

    def test_identities_pass_on_consistent_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "exports").mkdir(exist_ok=True)
            # 1000 = 900 + 100；1000 = 900 + 100；100 = 100 + 0
            self.build_identity_cohort(tmp, self.rows(1000, 900, 900, 100, 100, 0))
            summary = build_master(tmp, registry_path=None, out_dir=tmp)
            self.assertEqual(summary["identity_violations"], [])
            self.assertEqual(summary["identities_skipped"], [])

    def test_identity_violation_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            # M = 120 但 Q + P = 100，违反 M = Q + P
            self.build_identity_cohort(tmp, self.rows(1100, 1000, 980, 120, 100, 0))
            summary = build_master(tmp, registry_path=None, out_dir=tmp)
            identities = {v["identity"] for v in summary["identity_violations"]}
            self.assertEqual(identities, {"M = Q + P"})
            self.assertEqual(summary["identity_violations"][0]["code"], "0001.HK")

    def test_missing_identity_columns_are_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            write_cohort_csv(tmp / "exports" / "HKIPO-MB2025Q1_clean.csv",
                             [["0001.HK", "2025-02-10", "1.00", "0"]])
            summary = build_master(tmp, registry_path=None, out_dir=tmp)
            self.assertEqual(summary["identity_violations"], [])
            self.assertEqual(len(summary["identities_skipped"]), 3)

    def test_derived_columns_math_and_missing_handling(self):
        headers = ["Stock Code", "total liability in year-1", "total assets in year-1",
                   "Profit for the year in year-1", "Net sales in year-1",
                   "Net sales in year-2", "Total (without option)",
                   "Public Offer shares", "New shares"]
        rows = [
            ["0001.HK", "50", "200", "10", "110", "100", "1000", "10", "100"],
            ["0002.HK", "50", "0", "10", "110", "0", "-5", "10", "100"],
            ["0003.HK", "NaN", "200", "10", "110", "100", "1000", "10", "100"],
        ]
        added, columns, skipped = compute_derived_columns(headers, rows)
        self.assertEqual(skipped, [])  # 所有源列齐全（DERIVED_SPECS 全部可算）
        by_col = dict(zip(added, columns))
        self.assertEqual(len(added), len(DERIVED_SPECS))
        self.assertEqual(by_col["leverage_y1"], ["0.250000", "NaN", "NaN"])
        self.assertEqual(by_col["roa_y1"], ["0.050000", "NaN", "0.050000"])
        self.assertEqual(by_col["sales_growth_y1"], ["0.100000", "NaN", "0.100000"])
        self.assertEqual(by_col["public_offer_fraction"], ["0.100000", "0.100000", "0.100000"])
        # log_proceeds: Total<=0 或缺失 -> NaN
        self.assertEqual(by_col["log_proceeds_hkd"][1], "NaN")

    def test_derive_flag_appends_columns_only_when_sources_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            write_cohort_csv(tmp / "exports" / "HKIPO-MB2025Q1_clean.csv",
                             [["0001.HK", "2025-02-10", "1.00", "0"]])
            summary = build_master(tmp, registry_path=None, out_dir=tmp, derive=True)
            self.assertEqual(summary["derived_columns"], [])
            with Path(summary["master_csv"]).open(encoding="utf-8-sig", newline="") as fh:
                rows = list(csv.reader(fh))
            self.assertEqual(len(rows[0]), 2 + len(SYNTH_HEADERS))


class RealArtifactTests(unittest.TestCase):
    """依赖纳入版本控制的 Codebook 与本地 clean CSV（CSV 缺失时跳过）。"""

    def setUp(self):
        self.codebooks = sorted((WS / "codebooks").glob("HKIPO_*_Codebook.md"))
        self.cohort_csvs = [WS / "exports" / f"HKIPO-MB{tag}_clean.csv"
                            for tag in ("2025Q1", "2025Q2", "2026Q1", "2026Q2", "2026Q3")]

    def test_parse_real_codebook_has_full_variable_set(self):
        latest = self.codebooks[-1]
        variables = parse_codebook_variables(latest)
        self.assertEqual(len(variables), 202)
        self.assertEqual(len(set(variables)), 202)
        self.assertEqual(variables["A"]["header"], "HKEx file# of the year")
        self.assertEqual(variables["K"]["header"], "IPO Subscription Price (HK$)")

    def test_build_registry_from_real_codebooks(self):
        self.assertTrue(self.codebooks)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "registry.yaml"
            registry = build_registry(WS, out_path=out)
            self.assertEqual(registry["meta"]["variable_count"], 202)
            loaded = load_registry(out)
            headers = [v["header"] for v in loaded["variables"]]
            self.assertEqual(len(headers), len(set(headers)))
            slugs = [v["slug"] for v in loaded["variables"]]
            self.assertEqual(len(slugs), len(set(slugs)))

    @unittest.skipUnless(all(p.exists() for p in
                             [WS / "exports" / f"HKIPO-MB{tag}_clean.csv" for tag in
                              ("2025Q1", "2025Q2", "2026Q1", "2026Q2", "2026Q3")]),
                         "local cohort clean CSVs not present")
    def test_build_master_over_real_cohorts(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry_path = Path(tmp) / "registry.yaml"
            build_registry(WS, out_path=registry_path)
            summary = build_master(WS, registry_path=registry_path, out_dir=Path(tmp))
            self.assertTrue(summary["headers_aligned"])
            self.assertTrue(summary["registry_ok"])
            self.assertEqual(summary["variable_count"], 202)
            self.assertEqual(summary["cohort_order"],
                             ["2025Q1", "2025Q2", "2026Q1", "2026Q2", "2026Q3"])
            self.assertEqual(summary["total_rows"], 148)
            # hard error 只能来自重复代码（表头与注册表均已对齐）；
            # 若重复问题修复后，hard_errors 应为 False
            if summary["hard_errors"]:
                self.assertTrue(summary["cross_cohort_duplicate_codes"]
                                or summary["duplicate_codes"])
            with Path(summary["master_csv"]).open(encoding="utf-8-sig", newline="") as fh:
                rows = list(csv.reader(fh))
            self.assertEqual(rows[0][:2], ["cohort", "cross_cohort_duplicate"])
            self.assertEqual(len(rows) - 1, 148)

            # --derive：免汇率派生列应全部可算并追加到 master
            summary_d = build_master(WS, registry_path=registry_path, out_dir=Path(tmp),
                                     derive=True)
            self.assertEqual(len(summary_d["derived_columns"]), len(DERIVED_SPECS))
            with Path(summary_d["master_csv"]).open(encoding="utf-8-sig", newline="") as fh:
                rows_d = list(csv.reader(fh))
            self.assertEqual(len(rows_d[0]), 2 + 202 + len(DERIVED_SPECS))


if __name__ == "__main__":
    unittest.main()
