"""tools/external/flags.py 的上市途径文本 → 法定标记推导。"""
import importlib.util
import sys
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
