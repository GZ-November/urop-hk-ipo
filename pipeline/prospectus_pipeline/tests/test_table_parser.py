"""原生结构化表格解析引擎单元测试。"""
from __future__ import annotations

import datetime as dt
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT), str(ROOT / "src"), str(ROOT / "tools")]

import cross_check
import periods
import stabilization_panel
from table_parser import (
    _build_subtable_columns,
    _extract_rows_for_subtable,
    _is_year_header_line,
    extract_cornerstone_table,
    extract_share_capital_table,
    format_markdown_table,
)
import fitz


class TableParserTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parent.parent
        self.pdf_path = root / "data" / "pdf" / "HKIPO-MB6082.pdf"

    def test_format_markdown_table(self):
        """测试 Markdown 表格对齐与转义格式化。"""
        headers = ["Col A", "Col B"]
        rows = [["Val 1", "100"], ["Val 2 | special", "200"]]
        md = format_markdown_table(headers, rows)
        self.assertIn("| Col A", md)
        self.assertIn("| Col B", md)
        self.assertIn("Val 2 &#124; special", md)
        lines = md.strip().splitlines()
        self.assertEqual(len(lines), 4)

    def test_extract_share_capital_table(self):
        """测试从真实 PDF 抽取股本结构表。"""
        if not self.pdf_path.exists():
            self.skipTest(f"PDF {self.pdf_path} 不存在，跳过测试")

        doc = fitz.open(self.pdf_path)
        tables = extract_share_capital_table(doc)
        doc.close()

        self.assertGreaterEqual(len(tables), 1)
        t = tables[0]
        self.assertEqual(t.name, "share_capital")
        self.assertEqual(t.page, 333)
        self.assertIn("1,238,013,076", t.markdown)
        self.assertIn("2,358,977,900", t.markdown)

    def test_extract_cornerstone_table(self):
        """测试从真实 PDF 抽取基石投资者名单表。"""
        if not self.pdf_path.exists():
            self.skipTest(f"PDF {self.pdf_path} 不存在，跳过测试")

        doc = fitz.open(self.pdf_path)
        tables = extract_cornerstone_table(doc)
        doc.close()

        self.assertGreaterEqual(len(tables), 1)
        found_fullgoal = any("Fullgoal" in t.markdown for t in tables)
        self.assertTrue(found_fullgoal, "应在基石表中检测到 Fullgoal")

    def test_financial_5col_stub_and_pct_not_truncated(self):
        """测试 5 列（3 个完整年度 + 去年同期未审计对比期 + 最新 Stub 期间）及穿插 % 列时，
        真实期间表头按 X 坐标精确还原，且第 5 列（真正 year-1）绝不被 nums[:4] 截断或被 % 列挤占。"""
        # 模拟典型 5 列损益摘要表（含穿插 % 列与 (unaudited) 标记）
        # word 元组: (x0, y0, x1, y1, text, block_no, line_no, word_no)
        lines = [
            [
                (235.0, 100.0, 315.0, 110.0, "Year ended December 31,", 0, 0, 0),
                (410.0, 100.0, 499.0, 110.0, "Four months ended April 30,", 0, 0, 1),
            ],
            [
                (196.0, 115.0, 210.0, 125.0, "2022", 0, 1, 0),
                (268.0, 115.0, 282.0, 125.0, "2023", 0, 1, 1),
                (340.0, 115.0, 354.0, 125.0, "2024", 0, 1, 2),
                (412.0, 115.0, 426.0, 125.0, "2024", 0, 1, 3),
                (483.0, 115.0, 498.0, 125.0, "2025", 0, 1, 4),
            ],
            [
                (176.0, 130.0, 205.0, 140.0, "RMB’000", 0, 2, 0),
                (231.0, 130.0, 238.0, 140.0, "%", 0, 2, 1),
                (248.0, 130.0, 277.0, 140.0, "RMB’000", 0, 2, 2),
                (303.0, 130.0, 309.0, 140.0, "%", 0, 2, 3),
                (320.0, 130.0, 349.0, 140.0, "RMB’000", 0, 2, 4),
                (374.0, 130.0, 381.0, 140.0, "%", 0, 2, 5),
                (391.0, 130.0, 421.0, 140.0, "RMB’000", 0, 2, 6),
                (446.0, 130.0, 453.0, 140.0, "%", 0, 2, 7),
                (463.0, 130.0, 493.0, 140.0, "RMB’000", 0, 2, 8),
                (518.0, 130.0, 525.0, 140.0, "%", 0, 2, 9),
            ],
            [
                (400.0, 142.0, 437.0, 152.0, "(unaudited)", 0, 3, 0),
            ],
            [
                (95.0, 160.0, 127.0, 170.0, "Revenue", 0, 4, 0),
                (180.0, 160.0, 205.0, 170.0, "254,188", 0, 4, 1),
                (230.0, 160.0, 239.0, 170.0, "100.0", 0, 4, 2),
                (252.0, 160.0, 277.0, 170.0, "300,156", 0, 4, 3),
                (302.0, 160.0, 310.0, 170.0, "100.0", 0, 4, 4),
                (324.0, 160.0, 349.0, 170.0, "450,720", 0, 4, 5),
                (373.0, 160.0, 382.0, 170.0, "100.0", 0, 4, 6),
                (395.0, 160.0, 421.0, 170.0, "125,753", 0, 4, 7),
                (445.0, 160.0, 454.0, 170.0, "100.0", 0, 4, 8),
                (467.0, 160.0, 493.0, 170.0, "184,741", 0, 4, 9),
                (517.0, 160.0, 526.0, 170.0, "100.0", 0, 4, 10),
            ],
        ]
        yw = _is_year_header_line(lines[1])
        self.assertEqual(len(yw), 5)
        vcols, pct_xs = _build_subtable_columns(lines, 1, yw)
        self.assertEqual(len(vcols), 5)
        self.assertEqual(len(pct_xs), 5)

        headers = ["Financial Metric"] + [c["header"] for c in vcols]
        # 不得出现硬编码的 Year-3 / Year-2 / Year-1
        for fake in ("Year-3", "Year-2", "Year-1"):
            self.assertNotIn(fake, headers)
        self.assertIn("Year ended December 31 2022 [RMB’000]", headers[1])
        self.assertIn("Four months ended April 30 2024 (unaudited) [RMB’000]", headers[4])
        self.assertIn("Four months ended April 30 2025 [RMB’000]", headers[5])

        rows = _extract_rows_for_subtable(lines, 2, len(lines), vcols, pct_xs)
        self.assertEqual(len(rows), 1)
        # 5 个期间列数值全部保留，且 100.0% 占比列被准确过滤，第 5 列 184,741 完好保留
        self.assertEqual(
            rows[0],
            ["Revenue", "254,188", "300,156", "450,720", "125,753", "184,741"],
        )

    def test_historical_periods_parse_and_resolve(self):
        """测试 2 位年份解析为 1990 年代及 2000 年 IPO 三年业绩期和 COMBINED 报表解析。"""
        d = periods.parse_date("31/12/99")
        self.assertEqual(d, dt.date(1999, 12, 31))

        pages = [
            {
                "page": 1,
                "text": (
                    '"Track Record Period" the three years ended 31 December 1997, 1998 and 1999\n'
                    "COMBINED PROFIT AND LOSS ACCOUNTS"
                ),
            }
        ]
        tr = periods.resolve_from_pages(pages)
        self.assertEqual(tr.status, "ok")
        self.assertIsNotNone(tr.year1)
        self.assertIsNotNone(tr.year2)
        self.assertIsNotNone(tr.year3)
        self.assertEqual(tr.year1.end, dt.date(1999, 12, 31))
        self.assertEqual(tr.year2.end, dt.date(1998, 12, 31))
        self.assertEqual(tr.year3.end, dt.date(1997, 12, 31))

    def test_historical_stabilization_dates(self):
        """测试历史稳价公告不同日期格式解析与 RE_END_STAB 正则匹配。"""
        s1 = "The stabilization period in connection with the Global Offering ended on 15 July 2004"
        m1 = stabilization_panel.RE_END_STAB.search(s1)
        self.assertIsNotNone(m1)
        self.assertEqual(m1.group(1), "15 July 2004")
        self.assertEqual(stabilization_panel.parse_date_str(m1.group(1)), dt.date(2004, 7, 15))

        s2 = (
            "The stabilization period in connection with the Global Offering ended on "
            "Wednesday, January 28, 2026"
        )
        m2 = stabilization_panel.RE_END_STAB.search(s2)
        self.assertIsNotNone(m2)
        self.assertEqual(m2.group(1), "Wednesday, January 28, 2026")
        self.assertEqual(
            stabilization_panel.parse_date_str(m2.group(1)),
            dt.date(2026, 1, 28),
        )

    def test_main_board_market_cap_rules(self):
        """测试 2000–2026 港交所主板最低市值阶梯门槛（1亿/2亿/5亿港元）。"""
        # 2002: HK$150M passes (>= 100M threshold)
        res_2002 = cross_check.check_company(row_b={"col_F": "2002-05-01"}, mcap=150e6)
        self.assertFalse(any(c["check"] == "Main Board Market Cap" for c in res_2002))

        # 2010: HK$150M fails, HK$250M passes (200M threshold)
        res_2010_fail = cross_check.check_company(row_b={"col_F": "2010-05-01"}, mcap=150e6)
        self.assertTrue(any(c["check"] == "Main Board Market Cap" for c in res_2010_fail))
        res_2010_pass = cross_check.check_company(row_b={"col_F": "2010-05-01"}, mcap=250e6)
        self.assertFalse(any(c["check"] == "Main Board Market Cap" for c in res_2010_pass))

        # 2020: HK$250M fails, HK$600M passes (500M threshold)
        res_2020_fail = cross_check.check_company(row_b={"col_F": "2020-05-01"}, mcap=250e6)
        self.assertTrue(any(c["check"] == "Main Board Market Cap" for c in res_2020_fail))
        res_2020_pass = cross_check.check_company(row_b={"col_F": "2020-05-01"}, mcap=600e6)
        self.assertFalse(any(c["check"] == "Main Board Market Cap" for c in res_2020_pass))


if __name__ == "__main__":
    unittest.main()
