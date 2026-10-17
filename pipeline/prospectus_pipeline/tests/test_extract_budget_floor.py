"""Main Board extract budgets must keep every page the stored reviewed packets carried.

Stored payloads cite pages of the packets they were extracted from. When a group cap falls
below the slice a stored packet carried, `prepare` silently drops cited pages (2026-10:
config parity set ownership/offering to 50000/20000 while the 2026 packets had been built
under the 60000 default, dropping share-capital, pre-IPO and HOW TO APPLY pages for 45
issuers). Re-check with tools/packet_coverage.py before lowering a cap.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

import pdfprep  # noqa: E402

# Largest per-group slice, in packet characters up to its last carried page, over the stored
# packets of 2026Q1-Q3 (113 issuers), 2025Q1 (30) and 2025Q2 (77), measured 2026-10-16.
GROUP_FLOOR = {
    "share_structure": 44973, "price": 24972, "financials": 94331, "underwriting": 45000,
    "business": 44954, "cornerstone": 79994, "extra_financial": 109972, "chinese_name": 9979,
    "ownership": 59960, "offering": 47131,
}
TOTAL_FLOOR = 455570  # largest distinct-page packet among the same issuers

# 9980.HK text lengths: ownership = HISTORY AND DEVELOPMENT run then the share-capital /
# substantial-shareholder run (374 is cited by col_L/N-Q/BI); offering = EXPECTED TIMETABLE
# then HOW TO APPLY (406-410 cited by col_CE).
OWNERSHIP_9980 = {150: 1873, 151: 2201, 152: 1636, 153: 1593, 154: 2771, 155: 2230, 156: 1398,
                  157: 2595, 158: 1405, 159: 3190, 160: 2251, 161: 2144, 162: 3183, 163: 2797,
                  164: 3146, 165: 2854, 166: 3038, 167: 2779, 168: 3162, 373: 1878, 374: 1556,
                  375: 2781, 376: 1681, 377: 504, 378: 1939, 379: 2634}
OFFERING_9980 = {8: 1850, 9: 2629, 10: 2107, 11: 641, 12: 3422, 13: 2421, 14: 2776, 15: 2687,
                 406: 1490, 407: 1803, 408: 2830, 409: 2008, 410: 1900}


def main_board_configs() -> list[Path]:
    return [ROOT / "config.yaml"] + sorted(
        p for p in ROOT.glob("config_20*.yaml") if "gem" not in p.name)


class ExtractBudgetFloorTests(unittest.TestCase):
    def test_caps_cover_the_slices_of_stored_packets(self):
        for path in main_board_configs():
            extract = yaml.safe_load(path.read_text(encoding="utf-8"))["extract"]
            default = int(extract.get("max_chars_per_group", 60000))
            caps = {g: int(extract.get("group_caps", {}).get(g, default)) for g in pdfprep.GROUP_WINDOWS}
            short = {g: (caps[g], floor) for g, floor in GROUP_FLOOR.items() if caps[g] < floor}
            self.assertEqual({}, short, f"{path.name}: group caps below stored packet slices")
            self.assertGreaterEqual(int(extract.get("max_chars_total", 900000)), TOTAL_FLOOR, path.name)

    def test_cited_ownership_and_offering_pages_fit_the_budget(self):
        extract = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))["extract"]
        pages = {**OWNERSHIP_9980, **OFFERING_9980}
        with tempfile.TemporaryDirectory() as raw:
            text = Path(raw)
            (text / "HKIPO-MB9980.jsonl").write_text("".join(
                json.dumps({"page": pg, "text": "x" * n}) + "\n" for pg, n in sorted(pages.items())),
                encoding="utf-8")
            cfg = {"paths": {"text": text}, "extract": extract}
            loc = {"ownership": list(OWNERSHIP_9980), "offering": list(OFFERING_9980)}
            kept, omitted = pdfprep.select_pages(cfg, "9980.HK", loc)
        self.assertEqual({}, omitted)
        self.assertIn(374, kept["ownership"])
        self.assertEqual([406, 407, 408, 409, 410], kept["offering"][-5:])


if __name__ == "__main__":
    unittest.main()
