#!/usr/bin/env python3
"""Classify how old 2005-2024 financial values differ from the verified values."""
from pathlib import Path
import numpy as np, pandas as pd, warnings
warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
D = ROOT / "analysis/out/overview_1994_2026"
OUT = ROOT / "analysis/out/historical_financial_sources/old_value_error_types_2005_2024.csv"
old = pd.read_csv(D / "archive_pre_financial_repair" / "hkipo_33y_master_panel_1994_2026_tier1_complete.csv", low_memory=False)
new = pd.read_csv(D / "hkipo_33y_master_panel_1994_2026_tier1_complete.csv", low_memory=False)
m = (new.batch != "2025-2026") & (pd.to_numeric(new.cohort_year) >= 2005)
near = lambda a, b: np.abs(a - b) <= 0.01 * np.abs(b).clip(lower=1)
rows = []
for name, c, orig in (("revenue", "col_AH", "ext_revenue_orig"), ("pre-tax profit", "col_AK", "ext_pbt_orig"), ("net profit", "col_AN", "ext_np_orig"),
                      ("total assets", "col_Y", None), ("total equity", "col_AB", None), ("total liabilities", "col_AE", None)):
    a, b = pd.to_numeric(old[c], errors="coerce")[m], pd.to_numeric(new[c], errors="coerce")[m]
    o = pd.to_numeric(new[orig], errors="coerce")[m] if orig else b
    k = a.notna() & b.notna() & (b != 0)
    a, b, o = a[k], b[k], o[k]
    t = pd.Series("different number", index=a.index)
    scale = pd.Series(False, index=a.index)
    for f in (1e-6, 1e-3, 1e3, 1e6):
        scale |= near(a, b * f) | near(a, o * f)
    t[scale] = "unit only (thousand/million)"
    t[near(a.abs(), b.abs()) & (np.sign(a) != np.sign(b))] = "sign flipped"
    t[near(a, o) & ~near(a, b)] = "not annualised"
    if orig:
        t[(a.between(1990, 2030)) & ~near(a, b)] = "year stored as value"
    t[near(a, b)] = "correct"
    v = t.value_counts()
    rows.append({"field": name, "checked": len(t), **v.to_dict()})
r = pd.DataFrame(rows).fillna(0).set_index("field").astype(int)
r["wrong_after_ignoring_units_and_annualisation"] = r.get("different number", 0) + r.get("sign flipped", 0) + r.get("year stored as value", 0)
r.to_csv(OUT); print(r.T.to_string())
