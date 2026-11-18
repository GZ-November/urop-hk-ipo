#!/usr/bin/env python3
"""Replace 1994-2024 prospectus financial fields in the master panel.

Only statements that passed an accounting identity in the Accountants' Report are kept.
Every other historical financial value is blanked. 2025-2026 reviewed rows are untouched.
"""
import json, re, shutil, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PANEL = ROOT / "analysis/out/overview_1994_2026/hkipo_33y_master_panel_1994_2026_tier1_complete.csv"
ARCHIVE = PANEL.parent / "archive_pre_financial_repair"
WORK = ROOT / "analysis/out/historical_financial_sources/work"
OUT = ROOT / "analysis/out/historical_financial_sources/verified_financials_1994_2024.csv"
COLS = ["col_Y", "col_AB", "col_AE", "col_AH", "col_AK", "col_AN", "col_AU", "col_AF", "col_AG", "col_AL", "col_AM", "col_AT"]
EXT = ["ext_revenue_yr1", "ext_net_profit_yr1", "ext_pbt_yr1", "ext_total_assets", "ext_total_equity", "ext_total_liabilities", "ext_operating_cashflow"]
CODE = {"HK$": "HKD", "US$": "USD", "RMB": "RMB", "S$": "SGD"}
SGD = lambda y: 5.45 if y <= 1997 else 4.55 if y <= 2005 else 5.35 if y <= 2010 else 6.15 if y <= 2015 else 5.75


def main():
    if not (ARCHIVE / PANEL.name).exists():
        ARCHIVE.mkdir(exist_ok=True)
        shutil.copy2(PANEL, ARCHIVE / PANEL.name)
    p = pd.read_csv(ARCHIVE / PANEL.name, low_memory=False)
    hist = p.batch != "2025-2026"
    p["_key"] = p.file.astype(str).str.replace(".json", "", regex=False)
    d = pd.DataFrame([json.loads(x) for x in open(WORK / "parsed.jsonl")]).drop_duplicates("key", keep="last")
    extra = WORK / "excluded_keys.json"
    excluded = set(json.load(open(extra))) if extra.exists() else set()
    d = d[~d.key.isin(excluded) & (d.key.str[:4].astype(int) >= 2005)].set_index("key")

    rates = p[hist & p.ext_fin_currency.isin(["RMB", "USD"])].groupby(["ext_fin_currency", "cohort_year"]).ext_fx_to_hkd.first().to_dict()
    def fx(c, y):
        if c == "HKD":
            return 1.0
        if c == "SGD":
            return SGD(int(y))
        return rates.get((c, y), np.nan)

    for c in COLS + [x + s for x in ("ext_revenue_yr1", "ext_net_profit_yr1", "ext_pbt_yr1", "ext_total_assets", "ext_total_equity", "ext_total_liabilities", "ext_operating_cashflow") for s in ("", "_hkd")]:
        p[c] = p[c].astype(object) if c == "col_AT" else pd.to_numeric(p[c], errors="coerce")
        p.loc[hist, c] = np.nan
    for c in COLS:
        for s in ("__quote", "__page"):
            if c + s in p:
                p[c + s] = p[c + s].astype(object)
                p.loc[hist, c + s] = np.nan
    new = ["fin_source", "fin_income_page", "fin_balance_page", "fin_period_months", "revenue_orig", "pbt_orig", "np_orig"]
    for c in new:
        p["ext_" + c] = np.nan
        p["ext_" + c] = p["ext_" + c].astype(object)
    rows, reasons = [], {}
    for i, r in p[hist].iterrows():
        k = r["_key"]
        if k not in d.index:
            reasons["no_document"] = reasons.get("no_document", 0) + 1
            continue
        x = d.loc[k]
        y = int(r.cohort_year)
        listed = pd.to_datetime(r.listing_date, format="mixed")
        rec = {"key": k, "listing_date": r.listing_date}
        inc_ok, bal_ok = x.get("income_ok") == True, x.get("balance_ok") == True
        # Later accountants' reports in a prospectus cover acquired or holding entities.
        if inc_ok and re.search(r"accountants_report_[2-9]", str(x.get("income_file"))):
            inc_ok = False; reasons["income_secondary_report"] = reasons.get("income_secondary_report", 0) + 1
        if bal_ok and re.search(r"accountants_report_[2-9]", str(x.get("balance_file"))):
            bal_ok = False; reasons["balance_secondary_report"] = reasons.get("balance_secondary_report", 0) + 1
        ccy = x.get("ccy") if inc_ok else x.get("bal_ccy")
        code = CODE.get(ccy)
        rate = fx(code, y) if code else np.nan
        proceeds = pd.to_numeric(r.funds_raised_total_hkd, errors="coerce")
        # A missed "'000" or "million" caption leaves figures far too small for the offering.
        if inc_ok and proceeds > 0 and max(abs(x.revenue), abs(x.pbt), abs(x.np)) * rate < 0.005 * proceeds:
            inc_ok = False; reasons["income_scale"] = reasons.get("income_scale", 0) + 1
        if bal_ok and proceeds > 0 and x.ta * fx(CODE.get(x.get("bal_ccy")), y) < 0.03 * proceeds:
            bal_ok = False; reasons["balance_scale"] = reasons.get("balance_scale", 0) + 1
        p.at[i, "ext_fin_currency"] = code if code else np.nan
        p.at[i, "ext_fx_to_hkd"] = rate
        if inc_ok:
            end = pd.to_datetime(x.get("period_end"), errors="coerce")
            months = x.get("period_months")
            good = pd.notna(end) and pd.notna(months) and 0 < (listed - end).days <= 548 and 1 <= months <= 12
            if good:
                f = 12.0 / months
                vals = {"col_AH": ("ext_revenue_yr1", x.revenue * f), "col_AK": ("ext_pbt_yr1", x.pbt * f), "col_AN": ("ext_net_profit_yr1", x.np * f)}
                for c, (e, v) in vals.items():
                    p.at[i, c] = v; p.at[i, e] = v; p.at[i, e + "_hkd"] = v * rate
                    p.at[i, c + "__page"] = x.income_page
                p.at[i, "col_AT"] = end.strftime("%Y-%m-%d")
                p.at[i, "ext_fin_period_months"] = months
                p.at[i, "ext_fin_income_page"] = x.income_page
                p.at[i, "ext_revenue_orig"], p.at[i, "ext_pbt_orig"], p.at[i, "ext_np_orig"] = x.revenue, x.pbt, x.np
                rec.update(revenue=x.revenue, pbt=x.pbt, np=x.np, months=months, period_end=end.date(), ccy=code)
            else:
                reasons["income_period_failed"] = reasons.get("income_period_failed", 0) + 1
        if bal_ok and (not inc_ok or x.get("bal_ccy") == x.get("ccy")):
            for c, e, v in (("col_Y", "ext_total_assets", x.ta), ("col_AB", "ext_total_equity", x.te), ("col_AE", "ext_total_liabilities", x.tl)):
                p.at[i, c] = v; p.at[i, e] = v; p.at[i, e + "_hkd"] = v * rate
                p.at[i, c + "__page"] = x.balance_page
            p.at[i, "ext_fin_balance_page"] = x.balance_page
            rec.update(ta=x.ta, tl=x.tl, te=x.te, ccy=code)
        if len(rec) > 2:
            p.at[i, "ext_fin_source"] = "Accountants' Report, identity-checked parser"
            rows.append(rec)
    p.drop(columns="_key").to_csv(PANEL, index=False)
    pd.DataFrame(rows).to_csv(OUT, index=False)
    h = p[hist]
    print("reasons", reasons)
    report(pd.read_csv(ARCHIVE / PANEL.name, low_memory=False), p, d)
    print(h.groupby("batch").agg(n=("file", "size"), rev=("col_AH", "count"), np=("col_AN", "count"), ta=("col_Y", "count"), rev_hkd=("ext_revenue_yr1_hkd", "count")).to_string())


def report(old, new, parsed):
    """Coverage and old-versus-new audit by listing era."""
    hist = new.batch != "2025-2026"
    o, n = old[hist].copy(), new[hist].copy()
    keys = n["_key"]
    state = keys.map(parsed.state) if "state" in parsed else pd.Series(index=keys.index, dtype=object)
    out = []
    pairs = [("revenue", "col_AH"), ("pbt", "col_AK"), ("net_profit", "col_AN"), ("total_assets", "col_Y"), ("total_equity", "col_AB"), ("total_liabilities", "col_AE")]
    y = pd.to_numeric(n.cohort_year)
    eras = {"1994-2004 (out of scope)": y <= 2004, "2005-2007": y.between(2005, 2007), "2008-2017": y.between(2008, 2017), "2018-2024": y.between(2018, 2024), "All 2005-2024": y >= 2005}
    for era, mask in eras.items():
        idx = n.index[mask]
        s = state.loc[idx]
        row = {"era": era, "ipos": len(idx), "no_prospectus_found": int(s.isna().sum()),
               "document_but_no_accountants_report_or_scan": int(s.isin(["no_accountants_report", "scanned", "error"]).sum()),
               "income_verified": int(n.loc[idx, "col_AN"].notna().sum()), "balance_verified": int(n.loc[idx, "col_Y"].notna().sum()),
               "neither_verified": int((n.loc[idx, "col_AN"].isna() & n.loc[idx, "col_Y"].isna()).sum())}
        for name, c in pairs:
            a, b = pd.to_numeric(o.loc[idx, c], errors="coerce"), pd.to_numeric(n.loc[idx, c], errors="coerce")
            both = a.notna() & b.notna()
            bad = (a[both] - b[both]).abs() > 0.01 * b[both].abs().clip(lower=1)
            row[f"old_{name}_nonblank"] = int(a.notna().sum())
            row[f"old_{name}_checked"] = int(both.sum())
            row[f"old_{name}_wrong"] = int(bad.sum())
            row[f"old_{name}_unverifiable"] = int((a.notna() & b.isna()).sum())
        out.append(row)
    r = pd.DataFrame(out)
    r.to_csv(OUT.parent / "financial_repair_audit_by_era.csv", index=False)
    print(r.T.to_string())


if __name__ == "__main__":
    main()
