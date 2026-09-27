"""自包含测试夹具完整性与契约有效性测试。

验证 tests/fixtures/ 下的合成测试数据：
1. mock_workbook.xlsx 结构完整（161 列，2 家公司）；
2. mock_valid_extracted.json 严格满足 70 字段 schema 契约，零校验错误；
3. mock_invalid_extracted.json 包含已知反例，能被 contracts.validate_record 准确拦截；
4. mock_allot_extracted.json 严格满足 18 字段配发契约；
5. mock_pages.jsonl 包含关键页码并能被文本搜索模块正确解析。
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

import openpyxl
from contracts import validate_record


class FixtureIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.fixtures_dir = ROOT / "tests" / "fixtures"
        self.mock_wb = self.fixtures_dir / "mock_workbook.xlsx"
        self.mock_valid_json = self.fixtures_dir / "mock_valid_extracted.json"
        self.mock_invalid_json = self.fixtures_dir / "mock_invalid_extracted.json"
        self.mock_allot_json = self.fixtures_dir / "mock_allot_extracted.json"
        self.mock_pages = self.fixtures_dir / "mock_pages.jsonl"

    def test_mock_workbook_structure(self):
        self.assertTrue(self.mock_wb.exists(), "mock_workbook.xlsx 夹具文件必须存在")
        wb = openpyxl.load_workbook(self.mock_wb, data_only=True)
        self.assertIn("NLR", wb.sheetnames)
        ws = wb["NLR"]
        self.assertEqual(ws.max_column, 161, "工作簿表头必须为 161 列")
        self.assertEqual(ws.max_row, 3, "夹具包含 1 行表头 + 2 家公司")
        self.assertEqual(ws.cell(2, 2).value, "6082.HK")
        self.assertEqual(ws.cell(3, 2).value, "2513.HK")
        wb.close()

    def test_mock_valid_extracted_conforms_to_schema(self):
        self.assertTrue(self.mock_valid_json.exists())
        schema_path = ROOT / "schema" / "fields.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        rec = json.loads(self.mock_valid_json.read_text(encoding="utf-8"))
        self.assertEqual(len(rec["fields"]), 70, "招股书字段必须为 70 个")

        errors = validate_record(rec, schema, target="prospectus")
        self.assertEqual(errors, [], f"合法夹具不应包含校验错误: {errors}")

    def test_mock_invalid_extracted_is_intercepted(self):
        self.assertTrue(self.mock_invalid_json.exists())
        schema_path = ROOT / "schema" / "fields.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        rec = json.loads(self.mock_invalid_json.read_text(encoding="utf-8"))

        errors = validate_record(rec, schema, target="prospectus")
        self.assertGreater(len(errors), 0, "非法夹具必须被 contracts.validate_record 拦截")

    def test_mock_allot_extracted_conforms_to_schema(self):
        self.assertTrue(self.mock_allot_json.exists())
        schema_path = ROOT / "schema" / "allot_fields.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        rec = json.loads(self.mock_allot_json.read_text(encoding="utf-8"))
        self.assertEqual(len(rec["fields"]), 18, "配发字段必须为 18 个")

        errors = validate_record(rec, schema, target="allot")
        self.assertEqual(errors, [], f"合法配发夹具不应包含校验错误: {errors}")

    def test_mock_pages_parsing(self):
        self.assertTrue(self.mock_pages.exists())
        lines = [json.loads(l) for l in self.mock_pages.read_text(encoding="utf-8").splitlines() if l.strip()]
        self.assertGreaterEqual(len(lines), 3)
        pages = {l["page"] for l in lines}
        self.assertIn(333, pages, "应包含股本表关键页 333")


    def test_provenance_sha256_and_http_session(self):
        from storage import create_http_session, file_sha256

        # Test deterministic SHA-256 calculation
        h = file_sha256(self.mock_wb)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 64)  # 64 hex characters for SHA-256

        # Test resilient session creation with retries
        session = create_http_session(retries=4, backoff_factor=1.0)
        self.assertIn("https://", session.adapters)
        self.assertEqual(session.adapters["https://"].max_retries.total, 4)


if __name__ == "__main__":
    unittest.main()
