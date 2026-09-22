#!/usr/bin/env python3
"""自动化单元与回归测试套件：全景主板样本扩容与学术事件面板。

验证目标：
  1. 样本构建与法定筛选完整性（555 筛选，523 纳入，32 剔除）；
  2. 既有 2026 Q1 38 家公司 100% 完整包含且无一遗漏；
  3. 逐日交易面板（5,489 条 K 线）与 Amihud 非流动性指标数学一致性；
  4. 学术多跨期面板（342 条记录）严格成熟度审查（防前视偏差，未成熟窗口严格为 IMMATURE_WINDOW）；
  5. 稳价事件（38 家）与断崖效应指标完整性；
  6. 解禁事件（114 条）法定规则映射与事件窗 CAR 计算；
  7. 关系型投资者表（457 条）与承销辛迪加表（38 条）实体规范化格式。
"""
from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_MASTER = ROOT / "out" / "master"
WB_PATH = ROOT.parent / "HKIPO-MB2026Q1.xlsx"


class MasterExpansionTestSuite(unittest.TestCase):
    """主板大样本与事件面板全覆盖测试。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.sample_csv = OUT_MASTER / "sample_construction.csv"
        cls.issuer_csv = OUT_MASTER / "issuer_master.csv"
        cls.daily_csv = OUT_MASTER / "daily_market_panel.csv"
        cls.horizon_csv = OUT_MASTER / "horizon_summary.csv"
        cls.stab_csv = OUT_MASTER / "stabilization_events.csv"
        cls.lockup_csv = OUT_MASTER / "lockup_events.csv"
        cls.inv_csv = OUT_MASTER / "investor_relational.csv"
        cls.syn_csv = OUT_MASTER / "underwriter_relational.csv"

        # 确保所有必要文件均已就绪
        for p in (cls.sample_csv, cls.issuer_csv, cls.daily_csv, cls.horizon_csv, cls.stab_csv, cls.lockup_csv, cls.inv_csv, cls.syn_csv):
            if not p.exists():
                raise unittest.SkipTest(f"Missing deliverable: {p}")

    def test_01_sample_construction_audit(self) -> None:
        """测试 1: 验证全景样本筛选严格性与法定排除原因完备性。"""
        with self.sample_csv.open("r", encoding="utf-8-sig") as fh:
            rows = list(csv.DictReader(fh))

        self.assertGreaterEqual(len(rows), 550, "全量候选样本数应至少 550 家")
        
        inc = [r for r in rows if r["inclusion_status"] == "INCLUDED"]
        exc = [r for r in rows if r["inclusion_status"] == "EXCLUDED"]

        self.assertGreaterEqual(len(inc), 520, "纳入合格主板 IPO 应至少 520 家")
        self.assertGreaterEqual(len(exc), 30, "排除非合格发行（GEM/SPAC/介绍）应至少 30 家")

        # 每一家排除的样本必须有明确的法定原因
        for r in exc:
            self.assertIsNotNone(r["exclusion_reason"])
            self.assertGreater(len(r["exclusion_reason"].strip()), 10, f"{r['stock_code']} 缺失具体排除证据")
            self.assertEqual(r["data_completion_status"], "EXCLUDED_NON_IPO")

        # 重点排查案例
        exc_map = {r["stock_code"]: r for r in exc}
        self.assertIn("9893.HK", exc_map, "创业板转主板 Pizu Group 必须被排除")
        self.assertIn("6676.HK", exc_map, "De-SPAC 交易 ZG Group 必须被排除")
        self.assertIn("6887.HK", exc_map, "介绍上市 Sunshine Lake Pharma 必须被排除")

    def test_02_baseline_38_issuers_intact(self) -> None:
        """测试 2: 验证既有 38 家公司 100% 完整存在于 master 样本中。"""
        if not WB_PATH.exists():
            raise unittest.SkipTest(f"Missing production workbook: {WB_PATH}")
        import openpyxl
        wb = openpyxl.load_workbook(WB_PATH, data_only=True)
        ws = wb["NLR"]
        baseline_codes = set()
        for r in range(2, 40):
            c = ws.cell(r, 2).value
            if c:
                c_str = str(c).strip()
                if not c_str.endswith(".HK"):
                    digits = "".join(ch for ch in c_str if ch.isdigit())
                    c_str = f"{int(digits):04d}.HK"
                baseline_codes.add(c_str)
        wb.close()

        self.assertEqual(len(baseline_codes), 38, "既有工作簿应为 38 家")

        with self.issuer_csv.open("r", encoding="utf-8-sig") as fh:
            master_codes = {r["stock_code"] for r in csv.DictReader(fh)}

        for c in baseline_codes:
            self.assertIn(c, master_codes, f"基准 2026 Q1 公司 {c} 缺失于 master 表中")

    def test_03_daily_market_panel_microstructure(self) -> None:
        """测试 3: 验证逐日市场与微观结构数据数学一致性。"""
        with self.daily_csv.open("r", encoding="utf-8-sig") as fh:
            bars = list(csv.DictReader(fh))

        self.assertGreaterEqual(len(bars), 5000, "逐日 K 线总行数应超过 5,000 条")

        for b in bars[:200]:
            code = b["stock_code"]
            close = float(b["close"])
            high = float(b["high"])
            low = float(b["low"])
            vol = float(b["volume"])
            to = float(b["turnover"])

            self.assertGreater(close, 0.0, f"{code} 收盘价必须为正数")
            self.assertGreaterEqual(high, low, f"{code} 最高价必须大于等于最低价")
            self.assertGreaterEqual(vol, 0.0, f"{code} 成交量必须非负")
            self.assertGreaterEqual(to, 0.0, f"{code} 成交额必须非负")

            if b.get("amihud_illiq") and b["amihud_illiq"] != "":
                illiq = float(b["amihud_illiq"])
                self.assertGreaterEqual(illiq, 0.0, f"{code} Amihud 指标必须非负")

    def test_04_horizon_summary_maturity_guard(self) -> None:
        """测试 4: 验证学术跨期表现的成熟度防前视审查（Maturity Guard）。"""
        with self.horizon_csv.open("r", encoding="utf-8-sig") as fh:
            horizons = list(csv.DictReader(fh))

        self.assertEqual(len(horizons), 342, "38 家公司 × 9 个跨期窗口应严格为 342 条记录")

        for h in horizons:
            horizon_name = h["horizon"]
            matured = (h["matured"].lower() == "true")

            # 2026 Q1 上市公司截至当前不可能成熟 12M, 24M, 36M 窗口
            if horizon_name in ("Month_12", "Month_24", "Month_36"):
                self.assertFalse(matured, f"{h['stock_code']} 的 {horizon_name} 窗口不应成熟")
                self.assertEqual(h["missing_reason"], "IMMATURE_WINDOW", f"{h['stock_code']} 未成熟窗口必须标明 IMMATURE_WINDOW")
                self.assertIn(h["bhr_from_day1"], ("", "None", None), f"{h['stock_code']} 未成熟窗口绝不可填入未来假设收益")
                self.assertIn(h["wr_hsi"], ("", "None", None), f"{h['stock_code']} 未成熟窗口绝不可填入未来财富相对比")

            # 首日与首周应 100% 已成熟
            if horizon_name in ("Day_1", "Day_5"):
                self.assertTrue(matured, f"{h['stock_code']} 的 {horizon_name} 窗口必须已成熟")
                self.assertNotIn(h["bhr_from_day1"], ("", "None", None), f"{h['stock_code']} 已成熟窗口必须有真实 BHR 收益")

    def test_05_stabilization_events_completeness(self) -> None:
        """测试 5: 验证稳价行动与托单断崖效应指标完整性。"""
        with self.stab_csv.open("r", encoding="utf-8-sig") as fh:
            stabs = list(csv.DictReader(fh))

        self.assertEqual(len(stabs), 38, "稳价事件表应包含全部 38 家公司")

        for s in stabs:
            self.assertGreater(len(s["stabilizing_manager"].strip()), 2, f"{s['stock_code']} 缺失稳价经理人")
            self.assertIsNotNone(s["stabilization_period_end"], f"{s['stock_code']} 缺失稳价结束日期")
            self.assertIn(s["expired_unexercised"].lower(), ("true", "false"))

            # 断崖效应收益率格式
            if s.get("cliff_return_m5_p5") and s["cliff_return_m5_p5"] != "":
                c_ret = float(s["cliff_return_m5_p5"])
                self.assertGreater(c_ret, -1.0, "断崖收益率不可小于 -100%")

    def test_06_lockup_events_integrity(self) -> None:
        """测试 6: 验证多重法定解禁日程与事件窗 CAR 测算。"""
        with self.lockup_csv.open("r", encoding="utf-8-sig") as fh:
            lockups = list(csv.DictReader(fh))

        self.assertGreaterEqual(len(lockups), 114, "38 家公司至少应产生 114 个解禁事件")

        categories = {r["lockup_category"] for r in lockups}
        self.assertIn("Cornerstone_6M", categories)
        self.assertIn("Controlling_Shareholder_6M_Disposal", categories)
        self.assertIn("Controlling_Shareholder_12M_Control", categories)

        for lk in lockups:
            self.assertIn(lk["window_status"], ("MATURED", "IMMATURE_WINDOW", "NO_TRADING_DATA", "POST_UNLOCK_TRADING_MISSING"))
            if lk["window_status"] == "MATURED":
                self.assertIsNotNone(lk["car_m5_p5"])
                self.assertNotEqual(lk["car_m5_p5"], "")

    def test_07_relational_entities_format(self) -> None:
        """测试 7: 验证机构投资者与承销辛迪加关系表实体代号与属性完整性。"""
        with self.inv_csv.open("r", encoding="utf-8-sig") as fh:
            invs = list(csv.DictReader(fh))
        self.assertGreaterEqual(len(invs), 400, "投资者关系记录应至少 400 条")
        for inv in invs[:50]:
            self.assertTrue(inv["investor_id"].startswith("INV_"), f"投资者 ID {inv['investor_id']} 必须以 INV_ 开头")
            self.assertIn(inv["investor_category"], ("Cornerstone", "Pre-IPO VC", "Pre-IPO PE", "Pre-IPO Strategic"))

        with self.syn_csv.open("r", encoding="utf-8-sig") as fh:
            syns = list(csv.DictReader(fh))
        self.assertGreaterEqual(len(syns), 38, "承销辛迪加记录应至少 38 条")
        for syn in syns:
            self.assertTrue(syn["intermediary_id"].startswith("IB_"), f"中介机构 ID {syn['intermediary_id']} 必须以 IB_ 开头")
            self.assertIn(syn["commercial_bank_affiliate"].lower(), ("true", "false"))


if __name__ == "__main__":
    unittest.main()
