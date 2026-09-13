import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

from report import generate_report


class ReportTests(unittest.TestCase):
    def test_generate_report_metrics(self):
        stats = generate_report()
        self.assertEqual(stats["n_companies"], 38)
        self.assertGreater(stats["total_net_proceeds_hkd"], 90e9)  # > 90 billion HKD
        self.assertGreater(stats["total_market_cap_hkd"], 1e12)     # > 1 trillion HKD
        self.assertGreater(stats["cornerstone_coverage_pct"], 0.8)  # > 80% coverage
        self.assertEqual(stats["pathways"]["ch18c_specialist_tech"], 6)
        self.assertEqual(stats["pathways"]["ch18a_biotech"], 3)
        self.assertEqual(stats["pathways"]["ah_dual_listing"], 12)
        
        # Verify markdown report exists and has substantial content
        md_file = Path(stats["report_md_path"])
        self.assertTrue(md_file.exists())
        content = md_file.read_text(encoding="utf-8")
        self.assertIn("香港主板 2026 年第一季度 (Q1) IPO 全景学术与市场分析报告", content)
        self.assertIn("38 家", content)
        self.assertIn("資訊科技業", content)


if __name__ == "__main__":
    unittest.main()
