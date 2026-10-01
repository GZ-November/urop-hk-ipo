"""Testability screen for the 2026 sample (2026Q1-Q3, Main Board ordinary IPOs).

For every variable the research ideas rely on, report how many 2026 issuers have
a value, how many distinct values it takes, and the share held by the modal value.
A variable that is constant or almost constant cannot carry a hypothesis.

Usage:
    python3 analysis/testability_screen_2026.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from research_inputs import load_panel as load_panel, select_2026 as select_2026

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "pipeline" / "exports" / "HKIPO-MB-MASTER_clean.csv"

VARS = [
    "First-day return / Underpricing (%)",
    "Money left on the table (HK$)",
    "Subscription Ratio (times)",
    "Pricing position in filing range",
    "Filing range width (%)",
    "Filing price revision (%)",
    "Offer mechanism",
    "A+H issuer flag",
    "Chapter 18A flag",
    "Chapter 18C flag",
    "WVR flag",
    "Pre-IPO VC/PE backing (1=yes; 0=no)",
    "Top-tier VC/PE backing (1=yes; 0=no)",
    "Pre-IPO State/Gov backing (1=yes; 0=no)",
    "Pre-IPO holding duration (years)",
    "Pre-IPO investor board seat (1=yes; 0=no)",
    "Final cornerstone allocation (% of base offer)",
    "Cornerstone state-owned presence flag",
    "Crossover fund presence flag",
    "Unrestricted public shareholding at listing (%)",
    "Sale Shares",
    "Debt repayment (% of planned net IPO proceeds)",
    "Greenshoe exercise rate (%)",
    "Stabilization purchases occurred",
    "Underwriting discretionary incentive fee rate (%)",
    "Sponsor commercial bank affiliate flag",
    "Top 5 customers (% of year-1 revenue)",
    "First-day flipping ratio (%)",
    "Post-stabilization cliff return [-5, +5] (%)",
    "1-month BHR from Day-1 close (%)",
    "3-month BHR from Day-1 close (%)",
    "6-month BHR from Day-1 close (%)",
    "Cornerstone unlock CAR [-5, +5] (%)",
    "FINI digital settlement regime",
    "2025 pricing reform regime",
]


def screen(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for v in VARS:
        s = df[v]
        n = int(s.notna().sum())
        share = s.value_counts(normalize=True).iloc[0] if n else float("nan")
        rows.append({"variable": v, "non-null": n, "distinct": s.nunique(), "modal share": round(share, 2)})
    return pd.DataFrame(rows)


def main() -> None:
    df = select_2026(load_panel(MASTER))
    print(f"2026 sample: N = {len(df)}  ({df['cohort'].value_counts().sort_index().to_dict()})\n")
    print(screen(df).to_string(index=False))


if __name__ == "__main__":
    main()
