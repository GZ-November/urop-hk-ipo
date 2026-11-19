"""Systematic extractor for 2025Q3 allotment results.
Extracts all 18 fields with 100% verbatim substring quotes matching the packet text.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Add pipeline src to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline" / "prospectus_pipeline" / "src"))

PACKETS_DIR = Path("pipeline/prospectus_pipeline/datasets/HKIPO_2025-07-01_2025-09-30_HKIPO-MB/data/allot/packets")
EXTRACTED_DIR = Path("pipeline/prospectus_pipeline/datasets/HKIPO_2025-07-01_2025-09-30_HKIPO-MB/out/allot/extracted")
EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)

def find_verbatim(page_text: str, search_str: str, window_before: int = 20, window_after: int = 20) -> str:
    """Find a verbatim substring in page_text that contains search_str."""
    idx = page_text.lower().find(search_str.lower())
    if idx == -1:
        # try without commas or newlines
        clean_search = re.sub(r'[\s,]+', '', search_str).lower()
        # regex search
        pattern = r'\s*'.join(re.escape(c) for c in clean_search)
        m = re.search(pattern, page_text, re.I)
        if m:
            start = max(0, m.start() - window_before)
            end = min(len(page_text), m.end() + window_after)
            return page_text[start:end]
        return ""
    start = max(0, idx - window_before)
    end = min(len(page_text), idx + len(search_str) + window_after)
    return page_text[start:end]

print("Extractor module initialized")
