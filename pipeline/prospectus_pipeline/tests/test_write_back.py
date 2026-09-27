"""write_back.py 的纯函数与 fail-closed 行为测试。"""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from paths import WS  # noqa: E402
from write_back import coerce, parse_date, write_all  # noqa: E402


class ParseDateTests(unittest.TestCase):
    def test_accepts_pipeline_formats(self):
        from datetime import date, datetime
        self.assertEqual(parse_date(datetime(2026, 7, 2, 10, 0)), date(2026, 7, 2))
        self.assertEqual(parse_date("02/07/26"), date(2026, 7, 2))
        self.assertEqual(parse_date("2026-07-02"), date(2026, 7, 2))
        self.assertEqual(parse_date("2 July 2026"), date(2026, 7, 2))

    def test_unparseable_raises(self):
        with self.assertRaises(ValueError):
            parse_date("not a date")


class CoerceTests(unittest.TestCase):
    def test_missing_uses_manual_sentinels(self):
        # 抽取契约：缺失以哨兵字符串标注（NA / NaN），coerce 原样透传为写入值
        self.assertEqual(coerce({"value": "NA"}, {"key": "k", "kind": "text"}), "NA")
        self.assertEqual(coerce({"value": "NA"}, {"key": "k", "kind": "date"}), "NA")
        self.assertEqual(coerce({"value": "NaN"}, {"key": "k", "kind": "number"}), "NaN")

    def test_kinds_are_converted(self):
        self.assertEqual(coerce({"value": "12.4"}, {"key": "k", "kind": "integer"}), 12)
        self.assertEqual(coerce({"value": "12.4"}, {"key": "k", "kind": "number"}), 12.4)
        self.assertEqual(coerce({"value": "2026-07-02"}, {"key": "k", "kind": "date"}),
                         parse_date("2026-07-02"))
        self.assertEqual(coerce({"value": "  China Infotech "}, {"key": "k", "kind": "text"}),
                         "China Infotech")


class WriteAllFailClosedTests(unittest.TestCase):
    """写回前的拒绝路径：缺抽取 JSON / 工作簿无对应行都必须整体拒绝。"""

    def make_cfg(self, tmp: Path) -> dict:
        return {
            "_root": ROOT,
            "_ws": WS,
            "workbook": "cohorts/HKIPO-MB2026Q1.xlsx",
            "sheet": "NLR",
            "data_start_row": 2,
            "id_columns": {
                "file_no": "A", "stock_code": "B", "name": "C",
                "prospectus_date": "D", "listing_date": "E", "offer_price": "K",
            },
            "paths": {"out": tmp / "out", "allot_out": tmp / "out" / "allot"},
        }

    def test_missing_extraction_json_rejects_whole_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            cfg = self.make_cfg(tmp)
            with self.assertRaises(SystemExit) as ctx:
                write_all(cfg, only=["6656.HK"])  # 2026Q1 的真实发行人，但无抽取 JSON
            self.assertIn("缺少抽取 JSON", str(ctx.exception))

    def test_unknown_code_rejects_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            cfg = self.make_cfg(tmp)
            with self.assertRaises(SystemExit) as ctx:
                write_all(cfg, only=["9999.HK"])  # 工作簿不存在该代码
            self.assertIn("工作簿无对应行", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
