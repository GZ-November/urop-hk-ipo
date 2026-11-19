"""Audit / provenance script for Sections 6-8 of the HK IPO overview manuscript.

Reproduces the cells in Table 8 (pricing regimes with missing ranges separated),
the pre/post 4-Aug-2025 rows of Table 9 and the robustness rows of Table 12.
Run from the repository root: python3 analysis/audit_overview_sec6_8.py
"""
import contextlib
import io
import os
import runpy

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "overview_1994_2026")

# ---- Table 8: reuse the exact sample construction of run_deep_part2_econometrics.py
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(os.path.join(HERE, "run_deep_part2_econometrics.py"))
m = g["m"].copy()
m["p_type2"] = np.where(m["Minimum Offer Price"].isna(), "Range not captured", m["p_type"])
m["gs"] = m["Greenshoe exercise rate (%)"]
agg = dict(N=("ir_pct", "size"), mean_ir=("ir_pct", "mean"), med_ir=("ir_pct", "median"),
           break_pct=("ir_pct", lambda s: (s < 0).mean() * 100),
           med_sub=("Subscription Ratio (times)", "median"), gs_mean=("gs", "mean"))
print("TABLE 8 — pricing regimes (N=%d)" % len(m))
print(m.groupby("p_type2").agg(**agg).round(2).to_string())
print("All:", m.agg({"ir_pct": ["mean", "median"]}).round(2).to_dict(),
      "break", round((m.ir_pct < 0).mean() * 100, 2), "gs", round(m.gs.mean(), 3))
print("Listing months present:", sorted(m.listing_ym.dropna().unique()))

# ---- Table 9 pre/post rows and Table 12 robustness on the complete 226 panel
d = pd.read_csv(os.path.join(OUT, "hkipo_2025Q1_2026Q3_complete_226.csv"))
d["post"] = pd.to_datetime(d["Date of Listing"]) >= "2025-08-04"
d["ml_bn"] = d.gross_proceeds_hkd_m * d.initial_return_pct / 100 / 1000
d["r"] = d.public_offer_fraction_pct / 100
d["c"] = d.cornerstone_pct_of_offering.fillna(0) / 100
d["i"] = 1 - d.r - d.c
print("\nTABLE 9 / 12 — complete panel by 4-Aug-2025")
for k, s in d.groupby("post"):
    tot = s.ml_bn.sum()
    print(("post" if k else "pre"), "N", len(s),
          "meanIR %.2f medIR %.2f break %.1f medsub %.1f pub %.2f cs %.2f" % (
              s.initial_return_pct.mean(), s.initial_return_pct.median(),
              (s.initial_return_pct < 0).mean() * 100, s["Subscription Ratio (times)"].median(),
              s.public_offer_fraction_pct.mean(), s.cornerstone_pct_of_offering.mean()),
          "| ML %.2fbn retail %.2f corner %.2f other %.2f" % (
              tot, (s.ml_bn * s.r).sum() / tot * 100, (s.ml_bn * s.c).sum() / tot * 100,
              (s.ml_bn * s.i).sum() / tot * 100))
post = d[d.post]
print("Top-5 share of post-reform ML: %.1f%%" % (post.ml_bn.nlargest(5).sum() / post.ml_bn.sum() * 100))
print("Negative-IR contribution to ML: %.2fbn" % d.loc[d.ml_bn < 0, "ml_bn"].sum())
