import datetime as dt
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ah_reference", ROOT / "tools" / "external" / "ah_reference.py")
ah = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ah)


def hint(*items):
    return 'v_hint="' + "^".join("~".join(i) for i in items) + '"'


class SymbolLookupTests(unittest.TestCase):
    def test_parse_hint_decodes_unicode_and_skips_no_result(self):
        text = 'v_hint="sh~603501~\\u8c6a\\u5a01\\u96c6\\u56e2~hwjt~GP-A^hk~00501~\\u8c6a\\u5a01\\u96c6\\u56e2~hwjt~GP"'
        records = ah.parse_hint(text)
        self.assertEqual([(r["market"], r["code"], r["name"]) for r in records], [("sh", "603501", "豪威集团"), ("hk", "00501", "豪威集团")])
        self.assertEqual(ah.parse_hint('v_hint="N"'), [])

    def test_unique_short_name_match_including_star_market_and_status_suffix(self):
        def lookup(query):
            if query == "00537":
                return ah.parse_hint(hint(("hk", "00537", "普源精电", "x", "GP")))
            return ah.parse_hint(hint(("sh", "688337", "普源精电", "x", "GP-A-KCB"), ("hk", "00537", "普源精电", "x", "GP")))
        found = ah.find_a_symbol("0537.HK", lookup)
        self.assertEqual(found["symbol"], "sh688337")
        self.assertIn("STAR", found["status"])
        self.assertEqual(ah.normalize_name("迈威生物U"), ah.normalize_name("迈威生物b"))

    def test_ambiguous_or_missing_a_record_is_left_unresolved(self):
        def lookup(query):
            if query == "00001":
                return ah.parse_hint(hint(("hk", "00001", "同名", "x", "GP")))
            return ah.parse_hint(hint(("sh", "600001", "同名", "x", "GP-A"), ("sz", "000001", "同名", "x", "GP-A")))
        self.assertEqual(ah.find_a_symbol("0001.HK", lookup)["symbol"], "")
        self.assertEqual(ah.find_a_symbol("0001.HK", lookup)["status"], "ambiguous")
        self.assertEqual(ah.find_a_symbol("9999.HK", lambda q: [])["status"], "no_h_record")


class AnchorTests(unittest.TestCase):
    bars = [{"date": "2026-01-05", "close": 10.0}, {"date": "2026-01-06", "close": 11.0}, {"date": "2026-01-09", "close": 12.0}]
    fx = [{"date": "2026-01-05", "close": 1.1}, {"date": "2026-01-06", "close": 1.2}, {"date": "2026-01-09", "close": 1.3}]

    def test_anchor_uses_last_bar_on_or_before_and_strictly_before_variant(self):
        a = ah.anchor(self.bars, self.fx, dt.date(2026, 1, 7))
        self.assertEqual(a["a_date"], "2026-01-06")
        self.assertAlmostEqual(a["a_close_hkd"], 11.0 * 1.2)
        self.assertEqual(ah.anchor(self.bars, self.fx, dt.date(2026, 1, 9), strictly_before=True)["a_date"], "2026-01-06")

    def test_stale_or_missing_data_never_becomes_an_anchor(self):
        self.assertIsNone(ah.anchor(self.bars, self.fx, dt.date(2026, 2, 1)))      # last bar is too old
        self.assertIsNone(ah.anchor(self.bars, self.fx, dt.date(2026, 1, 1)))      # nothing yet
        self.assertIsNone(ah.anchor(self.bars, self.fx, None))
        self.assertIsNone(ah.anchor(self.bars, [], dt.date(2026, 1, 7)))           # no exchange rate


if __name__ == "__main__":
    unittest.main()
