#!/usr/bin/env python3
"""6228.HK: express offer quantities in the quoted offer unit (HDR).

The baseline stored CS/CT/CU and prospectus M/P/R/S/CE as underlying shares (HDR x 10)
while price, applications (CO), greenshoe (CV) and market volume are per HDR. Each corrected
value equals a number in its own quote. Share-capital fields (L, N, O, CZ, DC) stay in underlying
shares; comparisons use data/manual/offer_units.json. Run from the repository root.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PRO = ROOT / "pipeline/prospectus_pipeline/out/extracted/HKIPO-MB6228.json"
ALL = ROOT / "pipeline/prospectus_pipeline/out/allot/extracted/HKIPO-MB6228.json"
UNIT = "Quoted offer unit is the HDR (1 HDR = 10 underlying Shares, prospectus PDF p.24 / printed p.15)."


def patch(path, updates):
    rec = json.loads(path.read_text(encoding="utf-8"))
    for key, (value, note) in updates.items():
        entry = rec["fields"][key]
        entry["value"] = value
        entry["note"] = note
    path.write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


patch(PRO, {
    "col_M": (89668600, f"Offer HDRs (base, before over-allotment). {UNIT} = 896,686,000 underlying Shares."),
    "col_P": (89668600, f"Offer for Sale: all offer HDRs are Sale HDRs. {UNIT}"),
    "col_R": (80701700, f"International Offer HDRs before reallocation. {UNIT}"),
    "col_S": (8966900, f"Hong Kong Offer HDRs before reallocation. {UNIT}"),
    "col_O": (13834680060, "Shares (underlying) after capitalisation: O = L - 10 x M (M is in HDRs; 10 underlying Shares per HDR)."),
    "col_CE": (89668600, f"HDRs listed at listing (89,668,600 issued HDRs upon Listing per allotment announcement). {UNIT}"),
})
patch(ALL, {
    "col_CS": (89668600, f"Final Offer HDRs before over-allotment. {UNIT}"),
    "col_CT": (8966900, f"Final Hong Kong Offer HDRs (no clawback). {UNIT}"),
    "col_CU": (80701700, f"Final International Offer HDRs (no reallocation). {UNIT}"),
    "col_CO": (39645800, "HDRs applied for = sum over Pool A and Pool B tiers of (HDRs applied for x valid applications) "
                         "= 21,562,400 + 18,083,400 (independent recomputation from the basis-of-allocation table, pdf p.15)."),
})

# Refresh the free-float formula evidence text (value unchanged: 0.0305) so it states the unit conversion.
rec = json.loads(ALL.read_text(encoding="utf-8"))
f = rec["fields"]
cs, ck, cz = f["col_CS"]["value"], f["col_CK"]["value"], f["col_CZ"]["value"]
ratio = 10
expected = cs * ratio * (1 - ck) / cz
assert round(expected, 4) == f["col_DA"]["value"] == 0.0305, expected
quote = (f"公式：((col_CS {cs:,.0f} − col_CK {ck:.4f}×col_CS) × {ratio} 股/HDR) ÷ col_CZ {cz:,.0f}"
         f" = {expected:.4f}；DC = CZ")
for key in ("col_DA", "col_DB", "col_DC"):
    f[key]["quote"] = quote
ALL.write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
