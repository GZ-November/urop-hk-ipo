#!/usr/bin/env python3
"""Replace public-offer subscription multiples and cornerstone flags with filing-checked values."""
import glob, json, shutil
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PANEL = ROOT / "analysis/out/overview_1994_2026/hkipo_33y_master_panel_1994_2026_tier1_complete.csv"
ARCH = PANEL.parent / "archive_pre_subscription_cornerstone_repair"
R = ROOT / "analysis/out/subscription_cornerstone_repair"
near = lambda a, b, t=.02: pd.notna(a) and pd.notna(b) and abs(a - b) <= t * max(abs(b), 1e-9)


def reviews(folder):
    out = {}
    for f in glob.glob(str(R / folder / "A/*.json")):
        for x in json.load(open(f)):
            out[x["key"]] = x
    return out


def subscription(p):
    d = pd.read_csv(R / "parsed_subscription.csv").set_index("key")
    r1, r2 = reviews("review"), reviews("review2")
    val, src = {}, {}
    for i, r in p[p.batch != "2025-2026"].iterrows():
        k = r["_key"]; b = r.retail_sub_ratio_clean
        v, s = np.nan, "not_available"
        if k in d.index:
            x = d.loc[k]; y = x.parsed; how = x.how
            h = next((pd.to_numeric(q.get("multiple"), errors="coerce") for q in (r2.get(k), r1.get(k)) if q and q.get("status") == "value"), np.nan)
            ratio = np.nan
            for q in (r2.get(k), r1.get(k)):
                if q and q.get("applied_shares") and q.get("offer_shares"):
                    ratio = float(q["applied_shares"]) / float(q["offer_shares"]); break
            no_pub = any(q and q.get("status") == "no_public_offer" for q in (r1.get(k), r2.get(k)))
            placing = x.placing_only == True and not (r.funds_raised_public_hkd > 0)
            if how == "conflict":
                v, s = (y, "allotment_and_bloomberg") if near(y, b) else (b, "allotment_and_bloomberg") if near(x.get("sentence_value"), b) else (x.get("sentence_value"), "allotment_headline")
            elif how == "arithmetic_ok" and (pd.isna(h) or near(h, y)):
                v, s = y, "allotment_arithmetic"
            elif pd.notna(h) and (near(h, y) or near(h, b) or near(h, ratio)):
                v, s = h, "allotment_reviewed"
            elif pd.notna(y) and near(y, b, .01):
                v, s = y, "allotment_and_bloomberg"
            elif how == "arithmetic_ok":
                v, s = y if pd.isna(h) else h, "allotment_reviewed"
            elif no_pub or placing:
                s = "no_public_tranche"
        if s == "not_available" and pd.notna(b):
            v, s = b, "bloomberg_only"
        val[i], src[i] = v, s
    return pd.Series(val), pd.Series(src)


def cornerstone(p):
    d = pd.read_csv(R / "cornerstone_status.csv").set_index("key")
    d.loc["2007_0390.HK", "status"] = "yes"  # prospectus section "Our Corporate Investors"
    h = p.batch != "2025-2026"
    old, pct = pd.to_numeric(p.ext_has_cornerstone, errors="coerce"), pd.to_numeric(p.ext_cornerstone_pct, errors="coerce")
    st = p["_key"].map(d.status)
    keep_old = (st == "no_allotment_only") & (old == 1)
    new = pd.Series(np.nan, index=p.index)
    new[(st == "yes") | keep_old] = 1.0
    new[st == "no"] = 0.0
    src = st.map({"yes": "filing_text", "no": "prospectus_and_allotment_silent"}).astype(object)
    src[keep_old] = "earlier_allotment_quote"
    np_pct = pct.where((new == 1) & (old == 1) & (pct > 0))
    np_pct[new == 0] = 0.0
    tab = pd.crosstab(p.batch[h], new[h].map({1.0: "yes", 0.0: "no"}).fillna("blank"), margins=True)
    print(tab.to_string()); tab.to_csv(R / "cornerstone_status_by_era.csv")
    print("old 0 to yes", int(((old == 0) & (new == 1) & h).sum()), "old 0 to blank", int(((old == 0) & new.isna() & h).sum()), "old 1 to blank", int(((old == 1) & new.isna() & h).sum()), "old 1 to no", int(((old == 1) & (new == 0) & h).sum()))
    p.loc[h, "ext_has_cornerstone"] = new[h]
    p.loc[h, "ext_cornerstone_pct"] = np_pct[h]
    p.loc[h, "ext_cornerstone_shares"] = np_pct[h]
    p["ext_cornerstone_source"] = None
    p.loc[h, "ext_cornerstone_source"] = src[h]
    p.loc[~h, "ext_cornerstone_source"] = "reviewed_2025_2026"


def main():
    if not (ARCH / PANEL.name).exists():
        ARCH.mkdir(exist_ok=True); shutil.copy2(PANEL, ARCH / PANEL.name)
    p = pd.read_csv(ARCH / PANEL.name, low_memory=False).copy()
    p["_key"] = p.file.astype(str).str.replace(".json", "", regex=False)
    old_b, old_e = p.retail_sub_ratio_clean.copy(), p.ext_retail_sub_ratio.copy()
    v, s = subscription(p)
    # The clawback design needs a checked final public allocation; those fields exist for this set.
    p["pn18_allocation_sample"] = old_b.notna().astype(int)
    p["ext_retail_sub_source"] = None
    p.loc[s.index, "ext_retail_sub_source"] = s
    p.loc[p.batch == "2025-2026", "ext_retail_sub_source"] = "reviewed_2025_2026"
    for c in ("retail_sub_ratio_clean", "ext_retail_sub_ratio"):
        p.loc[v.index, c] = v
    t = p[p.batch != "2025-2026"]
    y = pd.to_numeric(t.cohort_year)
    era = pd.cut(y, [1993, 2001, 2004, 2007, 2017, 2024], labels=["1994-2001", "2002-2004", "2005-2007", "2008-2017", "2018-2024"])
    tab = pd.crosstab(era, t.ext_retail_sub_source, margins=True)
    filed = t.ext_retail_sub_source.str.startswith("allotment")
    for name, o in (("old_bloomberg", old_b), ("old_panel", old_e)):
        o = o[t.index]; both = filed & o.notna() & t.retail_sub_ratio_clean.notna()
        bad = (o - t.retail_sub_ratio_clean).abs() > .05 * t.retail_sub_ratio_clean.abs().clip(lower=1e-6)
        print(name, "checked", int(both.sum()), "off_by_more_than_5pct", int((both & bad).sum()), "blanked_or_unavailable", int((o.notna() & t.retail_sub_ratio_clean.isna()).sum()))
    print(tab.to_string()); tab.to_csv(R / "subscription_source_by_era.csv")
    cornerstone(p)
    p.drop(columns="_key").to_csv(PANEL, index=False)


if __name__ == "__main__":
    main()
