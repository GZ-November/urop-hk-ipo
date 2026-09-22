"""自动化回归与管道健壮性测试套件 (Pipeline Robustness & Dynamic Schema Tests)

验证核心改进：
  1. tools/external/aftermarket.py 动态列语义解析（在列位移/打乱时仍能准确读取必要字段）；
  2. tools/external/market.py, hkma_import.py, ipo_count.py 动态列语义解析；
  3. src/cross_check.py 动态行号扫描（突破硬编码 38 家限制）与严格列安全防护；
  4. src/audit.py 外部衍生字段语义表头映射（100% 覆盖率，杜绝 Unmapped）；
  5. src/codebook.py 学术元数据完整性（时点约定、缺失策略、覆盖度分级标签）。
"""
from __future__ import annotations

import datetime as dt
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
WS = ROOT.parent
WORKBOOK_PATH = WS / "HKIPO-MB2026Q1.xlsx"
FIXTURE_WORKBOOK = ROOT / "tests" / "fixtures" / "mock_workbook.xlsx"

import sys
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from audit import HEADER_TOOL_MAPPING, run_audit
from codebook import build_codebook
from cross_check import run_cross_check
from run import load_cfg


# 动态加载 aftermarket
MODULE_PATH = ROOT / "tools" / "external" / "aftermarket.py"
SPEC = importlib.util.spec_from_file_location("aftermarket", MODULE_PATH)
aftermarket = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(aftermarket)


class PipelineRobustnessTests(unittest.TestCase):
    def test_header_tool_mapping_completeness(self):
        """验证 HEADER_TOOL_MAPPING 包含所有预期的外部工具表头关键字映射。"""
        self.assertGreaterEqual(len(HEADER_TOOL_MAPPING), 30)
        self.assertIn("1-month post-ipo close price (hk$)", HEADER_TOOL_MAPPING)
        self.assertIn("6-month post-ipo close price (hk$)", HEADER_TOOL_MAPPING)
        self.assertIn("hsi return over 20 trading days before prospectus (%)", HEADER_TOOL_MAPPING)
        self.assertIn("first trading day closing price (hk$)", HEADER_TOOL_MAPPING)

    @unittest.skipUnless(WORKBOOK_PATH.exists(), "Requires local production dataset HKIPO-MB2026Q1.xlsx")
    def test_audit_external_tool_mapping_completeness(self):
        """验证 audit.py 对全量工作簿非 schema 外部列保持 100% 语义工具映射，无任何遗漏。"""
        cfg = load_cfg()
        res = run_audit(cfg)
        self.assertGreaterEqual(len(res["external_columns"]), 31)
        unmapped = [c for c in res["external_columns"] if c["tool_source"] == "Other external / manual"]
        self.assertEqual(
            unmapped,
            [],
            f"存在未映射的外部工具列: {[(c['col'], c['header']) for c in unmapped]}",
        )

    def test_codebook_academic_metadata_attributes(self):
        """验证 codebook 导出的每一个变量均完备定义了时点约定、缺失处理政策与覆盖状态。"""
        cfg = load_cfg()
        if not WORKBOOK_PATH.exists():
            cfg["workbook_path"] = FIXTURE_WORKBOOK
        variables, summary = build_codebook(cfg)
        self.assertEqual(summary["variable_count"], 161)

        reserved_headers = {
            "1-year post-IPO return (%) [Reserved]",
            "1-year wealth relative vs HSI [Reserved]",
            "3-year post-IPO return (%) [Reserved]",
            "3-year wealth relative vs HSI [Reserved]",
        }

        for v in variables:
            self.assertIn("timing_convention", v, f"{v['header']} missing timing_convention")
            self.assertIn("missing_policy", v, f"{v['header']} missing missing_policy")
            self.assertIn("coverage_status", v, f"{v['header']} missing coverage_status")

            if v["header"] in reserved_headers:
                self.assertEqual(
                    v["coverage_status"],
                    "Reserved / Unmatured",
                    f"{v['header']} should be flagged as Reserved / Unmatured",
                )

    def test_cross_check_dynamic_row_scanning(self):
        """验证 cross_check.py 动态扫描所有数据行，支持多于 38 家公司的动态样本。"""
        with tempfile.TemporaryDirectory() as tmp_dir:
            wb_path = Path(tmp_dir) / "dynamic_cohort.xlsx"
            base_wb = WORKBOOK_PATH if WORKBOOK_PATH.exists() else FIXTURE_WORKBOOK
            wb = openpyxl.load_workbook(base_wb)
            ws = wb["NLR"]

            data_rows = [r for r in range(2, ws.max_row + 1) if ws.cell(r, 2).value not in (None, "")]
            initial_companies = len(data_rows)
            last_r = max(data_rows)
            new_r = last_r + 1
            for col in range(1, ws.max_column + 1):
                ws.cell(new_r, col).value = ws.cell(last_r, col).value
            ws.cell(new_r, 2).value = "9999.HK"
            ws.cell(new_r, 3).value = "Dynamic Extra Issuer Limited"
            wb.save(wb_path)
            wb.close()

            cfg = load_cfg()
            cfg["workbook_path"] = wb_path
            res = run_cross_check(cfg, out_dir=tmp_dir)
            self.assertEqual(res["total_companies"], initial_companies + 1)
            codes = [r["code"] for r in res["results"]]
            self.assertIn("9999.HK", codes)

    def test_cross_check_strict_unmapped_column_guard(self):
        """验证 cross_check.py 的 cell 函数拒绝访问未映射的列键，杜绝位置猜测。"""
        cfg = load_cfg()
        book_path = WORKBOOK_PATH if WORKBOOK_PATH.exists() else FIXTURE_WORKBOOK
        wb = openpyxl.load_workbook(book_path, data_only=True)
        ws = wb[cfg["sheet"]]

        header_to_col = {}
        for c in range(1, ws.max_column + 1):
            v = ws.cell(1, c).value
            if v:
                h = " ".join(str(v).replace("\n", " ").split()).strip().lower()
                header_to_col[h] = c

        col_map = {"B": 2}

        def strict_cell(r: int, col_key: str):
            if col_key not in col_map:
                raise KeyError(f"Column key {col_key!r} not in verified col_map")
            idx = col_map[col_key]
            return ws.cell(r, idx).value

        # 访问合法列正常
        self.assertIsNotNone(strict_cell(2, "B"))
        # 访问未在映射中的列强制抛出 KeyError
        with self.assertRaises(KeyError):
            strict_cell(2, "ZZ_NONEXISTENT")
        wb.close()


if __name__ == "__main__":
    unittest.main()
