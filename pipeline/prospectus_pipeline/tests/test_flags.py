"""tools/external/flags.py 的上市途径文本 → 法定标记推导。"""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]
MODULE_PATH = ROOT / "tools" / "external" / "flags.py"
SPEC = importlib.util.spec_from_file_location("flags", MODULE_PATH)
flags = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(flags)


class APlusHFlagTests(unittest.TestCase):
    def test_route_wordings_seen_for_a_plus_h_issuers(self):
        # 2025–2026 cohort 抽取的实际措辞
        for text in [
            "A+H dual listing: H Shares on the Main Board of the HKEX (A Shares already listed on ChiNext of SZSE)",
            "A+H share listing on the Main Board of the Stock Exchange (PRC joint stock company already listed on the SZSE main board)",
            "Main Board; Chapter 19A PRC issuer with other listed shares (A+H)",
            "Main Board; Rule 8.05(3) (market capitalization/revenue test); Chapter 19A PRC issuer (A+H)",
            # 2026Q2/Q3 漏标的写法（2476.HK、3308.HK 等）
            "Main Board - Chapter 19A of the Listing Rules (PRC issuer with other listed shares)",
            "Chapter 19A of the Listing Rules (PRC issuer with other listed shares)",
            "Chapter 19A (PRC issuer with other listed shares), Main Board",
            "Main Board — Chapter 19A of the Listing Rules (PRC issuer with other listed shares); "
            "market capitalisation/revenue test under Rule 8.05(3)",
            # 1081.HK
            "Chapter 19A of the Main Board Listing Rules (PRC issuer with A Shares listed on the Shenzhen Stock Exchange)",
            "H-share listing of a company already listed on the Shanghai Stock Exchange",
            "PRC issuer with A-shares on the STAR Market",
            "主板 A+H 两地上市",
            "主板；A股已于深交所上市",
        ]:
            with self.subTest(text=text):
                self.assertTrue(flags.is_a_plus_h(text))

    def test_h_share_only_and_other_routes_are_not_a_plus_h(self):
        for text in [
            "Main Board (Chapter 19A PRC issuer)",
            "Chapter 19A of the Listing Rules (H Share issuer)",
            "Main Board of the Stock Exchange (H Shares of a PRC issuer, Chapter 19A)",
            "Main Board — PRC issuer (Chapter 19A) with WVR structure (Chapter 8A); eligibility under Rule 8.05/8A.06",
            "Hong Kong Main Board H-share listing (Listing Rules, PRC issuer, Stock Code 2596)",
            "Main Board of the Stock Exchange (standard H-share listing)",
            "Main Board (H shares)",
            "Chapter 18A of the Listing Rules",
            "Main Board",
            "",
        ]:
            with self.subTest(text=text):
                self.assertFalse(flags.is_a_plus_h(text))

    def test_negated_mentions_are_not_a_plus_h(self):
        for text in [
            "Chapter 19A PRC issuer (not an A+H issuer)",
            "Chapter 19A PRC issuer without other listed shares",
            "H Share issuer; no A Shares listed",
            "H 股发行人，非A+H",
        ]:
            with self.subTest(text=text):
                self.assertFalse(flags.is_a_plus_h(text))

    def test_cites_chapter_still_ignores_negation(self):
        self.assertFalse(flags.cites_chapter("Main Board standard listing (not Chapter 18C / 18A)", "18C"))
        self.assertTrue(flags.cites_chapter("Chapter 18C of the Listing Rules", "18C"))


class AShareListingStatementTests(unittest.TestCase):
    """招股书全文兜底：col_AS 未提及 A 股时，扫发行人自述的 A 股上市句。"""

    def scan(self, *pages):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "HKIPO-MB1234.jsonl"
            path.write_text(
                "".join(json.dumps({"page": i, "text": t}) + "\n" for i, t in enumerate(pages, 1)),
                encoding="utf-8",
            )
            return flags.a_share_listing_statement("1234.HK", Path(tmp))

    def test_issuer_statements_seen_in_prospectuses(self):
        # 2025–2026 cohort 招股书原句（1276、2865、2701、3296、2493、0537、6951、2249、6693）
        for text in [
            "RISK FACTORS Our A Shares are listed on the Shanghai Stock Exchange, and the characteristics may differ",
            "Our A Shares are listed and traded on the Shanghai Stock Exchange",
            "we completed our initial public offering of 30,000,000 A Shares, and our A Shares became "
            "listed on the Shenzhen Stock Exchange (stock code: 002865)",
            "Our A Shares are currently listed on the ChiNext Market of the Shenzhen Stock Exchange",
            "Since August 2023, our Company’s A Shares have been listed on the main board of Shanghai Stock Exchange",
            "The A Shares of our Company have been listed on the Shanghai Stock Exchange STAR Market (stock code: 688062)",
            "Since April 8, 2022, our A Shares have been listed on the Shanghai Stock Exchange’s STAR Market",
            "In December 2014, the A Shares of the Company were listed on the ChiNext of the Shenzhen Stock Exchange",
            "Our A Shares are listed on the STAR Market of the Shanghai Stock Exchange",
            "Our A Shares were listed and traded on the Shanghai Stock Exchange in 2004",
            "as our Group’s A shares are listed on the SSE, our principal books are kept in the PRC",
        ]:
            with self.subTest(text=text):
                hit = self.scan("cover page", text)
                self.assertIsNotNone(hit)
                self.assertEqual(hit["page"], 2)
                self.assertEqual(hit["hits"], 1)
                self.assertIn("A", hit["quote"])

    def test_statements_about_other_companies_or_share_classes_are_ignored(self):
        for text in [
            # 控股股东 / 可比公司 / 定义条目里别家公司的 A 股
            "Our Controlling Shareholder’s A Shares are listed on the Shanghai Stock Exchange",
            "XYZ Group, a company the A Shares of which are listed on the Shenzhen Stock Exchange",
            "Comparable companies whose A Shares are listed on the Shanghai Stock Exchange include ABC",
            "the A Shares of our parent company are listed on the Shanghai Stock Exchange",
            # 同股不同权 / 融资轮次（6810、0625、6658）
            "each Class A Share shall entitle the holder to exercise ten votes",
            "our Class A Shares are listed on no exchange; the Class B Shares will be listed on the Stock Exchange",
            "Beijing Sequoia subscribed for Series A Shares at a consideration of RMB135,000,000",
            # A 股在香港以外、非 A 股交易所
            "Our H Shares are listed on the Stock Exchange",
        ]:
            with self.subTest(text=text):
                self.assertIsNone(self.scan(text))

    def test_negated_and_hypothetical_statements_are_ignored(self):
        for text in [
            "Our A Shares are not listed on any stock exchange",
            "our A Shares have not been listed on the Shanghai Stock Exchange",
            "There is no assurance that our A Shares are listed on the STAR Market of the Shanghai Stock Exchange",
            "If our A Shares are listed on the Shanghai Stock Exchange, we will be subject to dual regulation",
            "after our A Shares are listed on the STAR Market of the Shanghai Stock Exchange, prices may diverge",
            "Our A Shares will be listed on the Shenzhen Stock Exchange upon approval",
            "we propose that our A Shares be listed on the Beijing Stock Exchange",
        ]:
            with self.subTest(text=text):
                self.assertIsNone(self.scan(text))

    def test_first_affirmative_page_is_recorded_and_all_hits_counted(self):
        hit = self.scan(
            "If our A Shares are listed on the Shanghai Stock Exchange, ...",
            "nothing here",
            "Our A Shares are listed on the Shanghai Stock Exchange",
            "Our A Shares are listed and traded on the Shanghai Stock Exchange",
        )
        self.assertEqual(hit["page"], 3)
        self.assertEqual(hit["hits"], 2)

    def test_missing_text_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(flags.a_share_listing_statement("1234.HK", Path(tmp)), {"missing_text": True})


class CellStrTests(unittest.TestCase):
    def test_workbook_values_normalise_to_derived_strings(self):
        import datetime as dt
        self.assertEqual(flags.cell_str(1), "1")
        self.assertEqual(flags.cell_str(0.0), "0")
        self.assertEqual(flags.cell_str(dt.datetime(2026, 3, 1)), "2026-03-01")
        self.assertEqual(flags.cell_str("NA"), "NA")
        self.assertEqual(flags.cell_str(None), "")


class ConfirmedAbsentCornerstoneTests(unittest.TestCase):
    def test_absence_comes_from_verdict_or_zero_allocation(self):
        import json
        import tempfile
        from cornerstone import confirmed_absent

        with tempfile.TemporaryDirectory() as tmp:
            allot_out = Path(tmp)
            (allot_out / "extracted").mkdir()
            (allot_out / "cornerstone_absence.json").write_text(json.dumps({
                "0901.HK": {"verdict": "absent"},
                "0100.HK": {"verdict": "present"},
                "0200.HK": {"verdict": "none"},  # legacy label
            }), encoding="utf-8")
            for code, value in {"1392": 0, "2272": 0.0, "3333": 0.31, "4444": None}.items():
                (allot_out / "extracted" / f"HKIPO-MB{code}.json").write_text(
                    json.dumps({"code": f"{code}.HK", "fields": {"col_CK": {"value": value}}}),
                    encoding="utf-8")
            absent = confirmed_absent({"paths": {"allot_out": allot_out}})

        self.assertEqual(absent, {"0901.HK", "0200.HK", "1392.HK", "2272.HK"})


if __name__ == "__main__":
    unittest.main()
