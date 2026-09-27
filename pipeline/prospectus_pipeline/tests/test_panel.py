import sys
import tempfile
import unittest
from pathlib import Path

import yaml

try:
    import pandas as pd
except ImportError:  # 分析 extras 未安装时跳过加载器测试
    pd = None

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]
WS = ROOT.parent

from master_panel import MASTER_STEM, REGISTRY_NAME  # noqa: E402

FIXTURE_REGISTRY = {
    "meta": {"variable_count": 4},
    "variables": [
        {"slug": "stock_code", "header": "Stock Code", "dtype": "string"},
        {"slug": "date_of_listing", "header": "Date of Listing (dd/mm/yy)", "dtype": "date"},
        {"slug": "ipo_subscription_price_hk", "header": "IPO Subscription Price (HK$)", "dtype": "numeric"},
        {"slug": "pre_ipo_vc_backing", "header": "Pre-IPO VC backing (1=yes; 0=no)", "dtype": "boolean"},
    ],
}
FIXTURE_MASTER_ROWS = [
    ["cohort", "cross_cohort_duplicate", "Stock Code", "Date of Listing (dd/mm/yy)",
     "IPO Subscription Price (HK$)", "Pre-IPO VC backing (1=yes; 0=no)"],
    ["2025Q1", "0", "0001.HK", "2025-02-10", "1.50", "1"],
    ["2025Q1", "0", "0002.HK", "2025-03-11", "garbage", "0"],
]


def write_fixture(tmp: Path) -> None:
    (tmp / "registry").mkdir(exist_ok=True)
    (tmp / "exports").mkdir(exist_ok=True)
    (tmp / "registry" / REGISTRY_NAME).write_text(
        yaml.safe_dump(FIXTURE_REGISTRY, allow_unicode=True, sort_keys=False), encoding="utf-8")
    with (tmp / "exports" / f"{MASTER_STEM}_clean.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        for row in FIXTURE_MASTER_ROWS:
            fh.write(",".join(row) + "\n")


@unittest.skipUnless(pd is not None, "pandas not installed")
class PanelLoaderTests(unittest.TestCase):
    def test_rename_and_dtype_coercion(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            write_fixture(tmp)
            sys.path.insert(0, str(ROOT / "src"))
            import panel
            frame = panel.load_master(ws=tmp)
            self.assertEqual(list(frame.columns)[:3], ["cohort", "cross_cohort_duplicate", "stock_code"])
            self.assertIn("ipo_subscription_price_hk", frame.columns)
            self.assertTrue(str(frame["date_of_listing"].dtype).startswith("datetime64"))
            values = frame["ipo_subscription_price_hk"].tolist()
            self.assertEqual(values[0], 1.5)
            self.assertTrue(pd.isna(values[1]))
            self.assertEqual(frame["pre_ipo_vc_backing"].tolist(), [1.0, 0.0])

    def test_slug_subset_keeps_identity_columns(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            write_fixture(tmp)
            import panel
            frame = panel.load_master(ws=tmp, slugs=["ipo_subscription_price_hk"])
            self.assertEqual(
                list(frame.columns),
                ["cohort", "cross_cohort_duplicate", "stock_code", "ipo_subscription_price_hk"])

    def test_unknown_slug_lists_available_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            write_fixture(tmp)
            import panel
            with self.assertRaises(ValueError) as ctx:
                panel.load_master(ws=tmp, slugs=["not_a_real_slug"])
            self.assertIn("not_a_real_slug", str(ctx.exception))

    def test_missing_master_points_to_build_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            (tmp / "registry").mkdir(exist_ok=True)
            (tmp / "registry" / REGISTRY_NAME).write_text("meta: {}\nvariables: []\n", encoding="utf-8")
            import panel
            with self.assertRaises(FileNotFoundError):
                panel.load_master(ws=tmp)

    def test_available_slugs(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            write_fixture(tmp)
            import panel
            rows = panel.available_slugs(ws=tmp)
            self.assertEqual([r["slug"] for r in rows],
                             ["stock_code", "date_of_listing",
                              "ipo_subscription_price_hk", "pre_ipo_vc_backing"])


@unittest.skipUnless(pd is not None, "pandas not installed")
class RealPanelTests(unittest.TestCase):
    def setUp(self):
        self.master = WS / "exports" / f"{MASTER_STEM}_clean.csv"
        self.registry = WS / "registry" / REGISTRY_NAME

    @unittest.skipUnless((WS / "exports" / f"{MASTER_STEM}_clean.csv").is_file()
                         and (WS / "registry" / REGISTRY_NAME).is_file(),
                         "local master panel or registry not present")
    def test_load_full_real_panel(self):
        import panel
        frame = panel.load_master()
        # 204 = 2 标识列 + 202 变量；--derive 生成的 master 再多 5 个派生列
        self.assertGreaterEqual(len(frame.columns), 204)
        self.assertEqual(len(frame), 148)
        self.assertTrue(str(frame["date_of_listing"].dtype).startswith("datetime64"))
        self.assertTrue(frame["ipo_subscription_price_hk"].dtype.kind == "f")
        if "leverage_y1" in frame.columns:
            self.assertTrue(frame["leverage_y1"].dtype.kind == "f")
        self.assertEqual(frame["cohort"].nunique(), 5)

    @unittest.skipUnless((WS / "exports" / f"{MASTER_STEM}_clean.csv").is_file()
                         and (WS / "registry" / REGISTRY_NAME).is_file(),
                         "local master panel or registry not present")
    def test_load_real_panel_subset(self):
        import panel
        frame = panel.load_master(slugs=["ipo_subscription_price_hk", "date_of_listing"])
        self.assertEqual(
            list(frame.columns),
            ["cohort", "cross_cohort_duplicate", "stock_code",
             "ipo_subscription_price_hk", "date_of_listing"])


if __name__ == "__main__":
    unittest.main()
