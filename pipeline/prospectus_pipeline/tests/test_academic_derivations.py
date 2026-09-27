"""学术衍生变量纯函数与边界计算单元测试套件。

严格验证依据 Lowry et al. (2017) 规范的 8 个核心衍生变量计算逻辑。
"""
from __future__ import annotations

import datetime as dt
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from academic_derivations import (
    derive_firm_age,
    derive_greenshoe_rate,
    derive_pricing_dynamics,
    derive_day1_trading,
)


class AcademicDerivationTests(unittest.TestCase):
    def test_derive_firm_age_standard(self):
        # 2019-09-09 到 2026-01-02 (2307 天 / 365.25 ≈ 6.32 年)
        l_date = dt.date(2026, 1, 2)
        i_date = dt.date(2019, 9, 9)
        age = derive_firm_age(l_date, i_date)
        self.assertEqual(age, 6.32)

    def test_derive_firm_age_strings_and_formats(self):
        age1 = derive_firm_age("2026-01-02", "2019-09-09")
        self.assertEqual(age1, 6.32)

        age2 = derive_firm_age("02/01/2026", "09/09/2019")
        self.assertEqual(age2, 6.32)

    def test_derive_firm_age_invalid_or_missing(self):
        self.assertIsNone(derive_firm_age(None, dt.date(2020, 1, 1)))
        self.assertIsNone(derive_firm_age(dt.date(2020, 1, 1), None))
        self.assertIsNone(derive_firm_age("NA", "2020-01-01"))
        # 成立日晚于上市日
        self.assertIsNone(derive_firm_age(dt.date(2020, 1, 1), dt.date(2025, 1, 1)))

    def test_derive_pricing_dynamics_at_high(self):
        # 壁仞科技真实数据: offer=19.60, max=19.60, min=17.00
        # mid = 18.30, revision = (19.6 - 18.3) / 18.3 ≈ 0.071038
        # width = (19.6 - 17.0) / 18.3 ≈ 0.142077
        rev, width, pos = derive_pricing_dynamics(19.60, 19.60, 17.00)
        self.assertAlmostEqual(rev, 0.071038, places=4)
        self.assertAlmostEqual(width, 0.142077, places=4)
        self.assertEqual(pos, "At high")

    def test_derive_pricing_dynamics_midpoint(self):
        rev, width, pos = derive_pricing_dynamics(18.30, 19.60, 17.00)
        self.assertAlmostEqual(rev, 0.0, places=4)
        self.assertEqual(pos, "Midpoint")

    def test_derive_pricing_dynamics_at_low(self):
        rev, width, pos = derive_pricing_dynamics(17.00, 19.60, 17.00)
        self.assertAlmostEqual(rev, -0.071038, places=4)
        self.assertEqual(pos, "At low")

    def test_derive_pricing_dynamics_fixed_price(self):
        # 智谱华章 / 天数智芯固定价格: min 为 None 或 min == max
        rev, width, pos = derive_pricing_dynamics(116.20, 116.20, None)
        self.assertEqual(rev, 0.0)
        self.assertEqual(width, 0.0)
        self.assertEqual(pos, "Fixed price")

        rev2, width2, pos2 = derive_pricing_dynamics(116.20, 116.20, 116.20)
        self.assertEqual(rev2, 0.0)
        self.assertEqual(width2, 0.0)
        self.assertEqual(pos2, "Fixed price")

    def test_derive_day1_trading_positive_return(self):
        # close = 34.46, offer = 19.60, vol = 150709945, shares = 284846600
        ir, money_left, flip = derive_day1_trading(34.46, 19.60, 150709945, 284846600)
        # ir = (34.46 - 19.60) / 19.60 = 0.758163
        self.assertAlmostEqual(ir, 0.758163, places=4)
        # money_left = (34.46 - 19.60) * 284846600 = 4232820476.0
        self.assertAlmostEqual(money_left, 4232820476.0, places=1)
        # flip = 150709945 / 284846600 = 0.529092
        self.assertAlmostEqual(flip, 0.529092, places=4)

    def test_derive_day1_trading_negative_return(self):
        ir, money_left, flip = derive_day1_trading(8.00, 10.00, 1000, 10000)
        self.assertAlmostEqual(ir, -0.20, places=4)
        self.assertAlmostEqual(money_left, -20000.0, places=1)
        self.assertAlmostEqual(flip, 0.10, places=4)

    def test_derive_greenshoe_rate(self):
        # 全额行使: 42726800 / (284846600 * 0.15) = 1.0
        rate = derive_greenshoe_rate(42726800, 284846600, 0.15)
        self.assertEqual(rate, 1.0)

        # 未行使
        rate_zero = derive_greenshoe_rate(0, 284846600, 0.15)
        self.assertEqual(rate_zero, 0.0)

        # 无绿鞋
        rate_no_opt = derive_greenshoe_rate(0, 284846600, 0.0)
        self.assertEqual(rate_no_opt, 0.0)


if __name__ == "__main__":
    unittest.main()
