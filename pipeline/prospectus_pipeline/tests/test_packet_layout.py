"""The extraction packet carries each source page once, ordered, with an index of who needs it."""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

import pdfprep  # noqa: E402

CODE = "8888.HK"
FIELDS = [{"key": "col_L", "header": "Shares", "group": "share_structure", "kind": "number", "unit": "shares"},
          {"key": "col_T", "header": "Price", "group": "price", "kind": "number", "unit": "HKD"},
          {"key": "col_DP", "header": "Chinese name", "group": "chinese_name", "kind": "text", "unit": "text"}]
REC = {"code": CODE, "name": "Test", "pdf_url": "x", "doc_type": "", "doc_title": "", "doc_datetime": "",
       "prospectus_date": "", "listing_date": ""}


def make_cfg(tmp: Path, **extract) -> dict:
    (tmp / "text").mkdir()
    (tmp / "packets").mkdir()
    rows = [{"page": i, "text": f"page {i} body " + "x" * 200} for i in range(1, 9)]
    (tmp / "text" / "HKIPO-MB8888.jsonl").write_text(
        "\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return {"paths": {"text": tmp / "text", "packets": tmp / "packets"},
            "extract": {"cover_pages": 3, "max_chars_per_group": 60000, **extract}}


class PacketLayoutTests(unittest.TestCase):
    def test_shared_pages_are_written_once_in_page_order(self):
        with tempfile.TemporaryDirectory() as raw:
            cfg = make_cfg(Path(raw))
            loc = {"price": [1, 2, 3], "chinese_name": [1, 2, 3], "share_structure": [7, 5, 3]}
            kept, omitted = pdfprep.select_pages(cfg, CODE, loc)
            page_text = {p["page"]: p["text"] for p in pdfprep._pages(cfg, CODE)}
            path = pdfprep.build_packet(cfg, REC, FIELDS, kept, omitted, page_text)
            text = path.read_text(encoding="utf-8")
            marks = [int(x) for x in re.findall(r"<<<PAGE (\d+)>>>", text)]
            self.assertEqual(marks, [1, 2, 3, 5, 7])
            self.assertIn("第 1-3 页", text)
            self.assertIn("第 3, 5, 7 页", text)
            self.assertEqual(text.count("`col_L`"), 1)
            # slices used for audit files keep one block per group
            slices = pdfprep.build_slices(cfg, CODE, loc)
            self.assertEqual(slices["price"].count("<<<PAGE"), 3)
            self.assertEqual(slices["chinese_name"].count("<<<PAGE"), 3)

    def test_group_cap_counts_shared_pages_but_total_cap_counts_them_once(self):
        with tempfile.TemporaryDirectory() as raw:
            one_page = len("\n<<<PAGE 1>>>\n" + "page 1 body " + "x" * 200)
            cfg = make_cfg(Path(raw), group_caps={"price": one_page * 2 + 5, "chinese_name": one_page * 2 + 5},
                           max_chars_total=one_page * 2 + 5)
            loc = {"price": [1, 2, 3], "chinese_name": [1, 2, 3]}
            kept, omitted = pdfprep.select_pages(cfg, CODE, loc)
            self.assertEqual(kept["price"], [1, 2])
            self.assertEqual(kept["chinese_name"], [1, 2])  # shared pages add nothing to the total
            self.assertEqual(omitted, {"price": 3, "chinese_name": 3})
            page_text = {p["page"]: p["text"] for p in pdfprep._pages(cfg, CODE)}
            text = pdfprep.build_packet(cfg, REC, FIELDS, kept, omitted, page_text).read_text(encoding="utf-8")
            self.assertIn("第 3 页起因超出字符上限省略", text)
            self.assertNotIn("<<<PAGE 3>>>", text)


if __name__ == "__main__":
    unittest.main()
