import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]
WS = ROOT.parent
WORKBOOK_PATH = WS / "HKIPO-MB2026Q1.xlsx"
FIXTURE_WORKBOOK = ROOT / "tests" / "fixtures" / "mock_workbook.xlsx"

from report import generate_report
from run import load_cfg

PRODUCTION_COHORT = "2026 Q1"


def pinned_cfg(workbook: Path, cohort: str = PRODUCTION_COHORT) -> dict:
    """Return a config pinned to an explicit workbook and cohort.

    A working checkout's ``config.yaml`` is repointed whenever a new cohort is
    being collected (for example ``HKIPO-MB2026Q2.xlsx``). These tests assert on
    a specific dataset, so they must pin it explicitly rather than inheriting
    whatever cohort the local checkout happens to target.
    """
    cfg = load_cfg()
    cfg["workbook_path"] = workbook
    cfg["dataset"] = {**cfg.get("dataset", {}), "cohort": cohort}
    return cfg


class ReportTests(unittest.TestCase):
    def test_generate_report_with_mock_fixture(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            cfg = pinned_cfg(FIXTURE_WORKBOOK)
            out_md = Path(tmp_dir) / "mock_report.md"
            stats = generate_report(cfg, out_path=out_md)
            self.assertEqual(stats["n_companies"], 2)
            self.assertTrue(out_md.exists())
            content = out_md.read_text(encoding="utf-8")
            self.assertIn("香港主板 2026 Q1 IPO 全景学术与市场分析报告", content)
            self.assertIn("2 家", content)

    @unittest.skipUnless(WORKBOOK_PATH.exists(), "Requires local production dataset HKIPO-MB2026Q1.xlsx")
    def test_generate_report_metrics_production(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_md = Path(tmp_dir) / "prod_report.md"
            stats = generate_report(pinned_cfg(WORKBOOK_PATH), out_path=out_md)
            self.assertEqual(stats["n_companies"], 38)
            self.assertGreater(stats["total_net_proceeds_hkd"], 90e9)  # > 90 billion HKD
            self.assertGreater(stats["total_market_cap_hkd"], 1e12)     # > 1 trillion HKD
            self.assertGreater(stats["cornerstone_coverage_pct"], 0.8)  # > 80% coverage
            self.assertEqual(stats["pathways"]["ch18c_specialist_tech"], 6)
            self.assertEqual(stats["pathways"]["ch18a_biotech"], 3)
            self.assertEqual(stats["pathways"]["ah_dual_listing"], 12)

            # Verify markdown report exists and has substantial content
            self.assertTrue(out_md.exists())
            content = out_md.read_text(encoding="utf-8")
            self.assertIn("香港主板 2026 Q1 IPO 全景学术与市场分析报告", content)
            self.assertIn("38 家", content)
            self.assertIn("資訊科技業", content)


if __name__ == "__main__":
    unittest.main()
