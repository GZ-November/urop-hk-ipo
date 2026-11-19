#!/usr/bin/env python3
"""Build and probe 48-issuer stratified pilot sample (1994-2024).

Task C implementation:
1. Stratified 48-issuer selection: 4 batches x 12 issuers (9 MB + 3 GEM = 48).
   - Fully reproducible with fixed seed.
   - Comprehensive constraint checking.
2. Lightweight, non-destructive source availability probe:
   - Local repo PDF/packet checks.
   - HKEXnews live title search query with polite rate limiting (0.3s delay).
   - Archival alternative identifiers for pre-1999 cutoff and missing filings.
3. Save CSVs and Markdown report.
"""
from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PANEL_CSV = ROOT / "analysis" / "out" / "overview_1994_2026" / "clean_33y_hkipo_panel_1994_2026.csv"
OUT_DIR = ROOT / "analysis" / "out" / "overview_1994_2026"
SAMPLE_CSV = OUT_DIR / "pilot_48_stratified_sample.csv"
PROBE_CSV = OUT_DIR / "pilot_48_source_probe.csv"
REPORT_MD = OUT_DIR / "pilot_48_design_and_probe_report.md"

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
HKEX_BASE = "https://www1.hkexnews.hk"
HKEX_SEARCH_URL = "https://www1.hkexnews.hk/search/titleSearchServlet.do"
ACTIVE_URL = "https://www1.hkexnews.hk/ncms/script/eds/activestock_sehk_e.json"
INACTIVE_URL = "https://www1.hkexnews.hk/ncms/script/eds/inactivestock_sehk_e.json"

SEED = 20261112

print("Script template created")
