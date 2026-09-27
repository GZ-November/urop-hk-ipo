"""原生结构化表格解析引擎单元测试。"""
from __future__ import annotations

import unittest
from pathlib import Path

from table_parser import (
    extract_all_tables_for_pdf,
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


if __name__ == "__main__":
    unittest.main()
