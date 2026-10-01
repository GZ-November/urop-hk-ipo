"""Quarterly cohort configs must carry the full extract budget set.

Packets are hash-bound to extraction and review credentials.  Re-running
`prepare` under a config whose extract budgets differ from config.yaml silently
regenerates different packet bytes and breaks the hash alignment of every
already-reviewed issuer in that cohort.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class ExtractConfigParityTests(unittest.TestCase):
    def test_quarterly_configs_carry_full_extract_budgets(self):
        base = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))["extract"]
        for name in sorted(ROOT.glob("config_2026q*.yaml")):
            extract = yaml.safe_load(name.read_text(encoding="utf-8")).get("extract") or {}
            missing = [key for key, value in base.items() if extract.get(key) != value]
            self.assertEqual(
                [], missing,
                f"{name.name} extract budgets drift from config.yaml: {missing}; "
                "preparing under it would invalidate existing hash-bound reviews",
            )


if __name__ == "__main__":
    unittest.main()
