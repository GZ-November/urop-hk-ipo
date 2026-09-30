"""Margin-financing (孖展) demand during the subscription period, when a data file is available.

No public, machine-readable history of daily margin totals exists, so this repository does not ship one. Put a file at
    pipeline/exports/HKIPO-2026-margin-daily.csv
with the columns of pipeline/templates/HKIPO-2026-margin-daily.template.csv (one row per issuer and day of the subscription
period; margin_total_hkd = cumulative margin loans applied for, margin_multiple = margin total / public tranche, source = where each
figure came from). Then run this script. It validates the file, and relates the margin path to the final subscription ratio and to the
first-day return. Without the file it writes a short note and exits; nothing is estimated.

Output (analysis/out/margin/): margin.md.

Usage:
    python3 analysis/margin_financing_2026.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

import extended_analysis_2026 as ext
from module_a_stylized_facts import ROOT, load_panel, select_2026, to_markdown

OUT = ROOT / "analysis" / "out" / "margin"
DATA = ROOT / "pipeline" / "exports" / "HKIPO-2026-margin-daily.csv"
REQUIRED = ["stock_code", "date", "margin_total_hkd", "margin_multiple", "source"]


def validate(margin: pd.DataFrame, sample: pd.DataFrame) -> pd.DataFrame:
    """Return the cleaned frame or raise ValueError describing the first problem found."""
    missing = [c for c in REQUIRED if c not in margin.columns]
    if missing:
        raise ValueError(f"Margin file lacks columns: {missing}")
    frame = margin.dropna(subset=["stock_code", "date"]).copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    if frame["date"].isna().any():
        raise ValueError("Unparseable dates in the margin file")
    unknown = set(frame["stock_code"]) - set(sample["Stock Code"])
    if unknown:
        raise ValueError(f"Issuers outside the 2026 sample: {sorted(unknown)}")
    window = sample.set_index("Stock Code")[["Subscription opening date", "Subscription closing date"]].apply(pd.to_datetime)
    outside = frame[(frame["date"] < frame["stock_code"].map(window["Subscription opening date"]))
                    | (frame["date"] > frame["stock_code"].map(window["Subscription closing date"]))]
    if len(outside):
        raise ValueError(f"{len(outside)} rows fall outside the issuer's subscription period")
    frame = frame.sort_values(["stock_code", "date"])
    for col in ("margin_total_hkd", "margin_multiple"):
        values = pd.to_numeric(frame[col], errors="coerce")
        if (values < 0).any():
            raise ValueError(f"Negative {col}")
        frame[col] = values
    falling = frame.groupby("stock_code")["margin_total_hkd"].apply(lambda s: (s.dropna().diff().dropna() < 0).any())
    if falling.any():
        raise ValueError(f"Cumulative margin totals decrease for: {sorted(falling[falling].index)}")
    return frame


def per_issuer(margin: pd.DataFrame) -> pd.DataFrame:
    """Final and first observed margin multiple and the number of observed days per issuer."""
    g = margin.dropna(subset=["margin_multiple"]).groupby("stock_code")
    return pd.DataFrame({"final_multiple": g["margin_multiple"].last(), "first_multiple": g["margin_multiple"].first(), "days": g["date"].nunique()})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if not DATA.exists():
        (OUT / "margin.md").write_text(
            "# Margin financing, 2026\n\nNo data file found. Add `pipeline/exports/HKIPO-2026-margin-daily.csv` (columns in "
            "`pipeline/templates/HKIPO-2026-margin-daily.template.csv`) and rerun `python3 analysis/margin_financing_2026.py`.\n"
            "Nothing is estimated in the absence of data.\n", encoding="utf-8")
        print("No margin data file; wrote a note to", (OUT / "margin.md").relative_to(ROOT))
        return
    y26 = select_2026(load_panel())
    margin = validate(pd.read_csv(DATA), y26)
    d = ext.prepare(y26).merge(per_issuer(margin), left_on="code", right_index=True, how="inner")
    d["lfinal"] = np.log(d["final_multiple"].where(d["final_multiple"] > 0))
    rho = stats.spearmanr(d["lfinal"], d["ir"], nan_policy="omit")
    rows = []
    for label, xs in [("ln final margin multiple", ["lfinal"]), ("+ April-June window", ["lfinal", "hot"]), ("+ window + ln size", ["lfinal", "hot", "lproc"])]:
        r = ext.ols_focus(d, "y", xs, "lfinal")
        rows.append([label, f"{r['b']:.3f}{ext.stars(r['p'])} ({r['se']:.3f})", f"{r['p']:.3f}", "—" if np.isnan(r["p_wild"]) else f"{r['p_wild']:.3f}", str(r["n"])])
    tab = pd.DataFrame(rows, columns=["Specification", "Coefficient (HC3 s.e.)", "HC3 p", "Wild cluster p", "N"])
    (OUT / "margin.md").write_text(
        f"# Margin financing, 2026 (N = {len(d)} issuers with data)\n\nRank correlation of the final margin multiple with IR: rho = {rho.statistic:.2f} (p = {rho.pvalue:.3f}).\n\n"
        + to_markdown(tab.set_index("Specification"), "Specification") + "\n", encoding="utf-8")
    print("Margin analysis written to", (OUT / "margin.md").relative_to(ROOT))


if __name__ == "__main__":
    main()
