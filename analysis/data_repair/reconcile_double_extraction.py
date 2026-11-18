#!/usr/bin/env python3
"""Accept a blind double extraction only when both passes agree and the accounts tie."""
import glob, json, sys
from pathlib import Path
import fitz
sys.path.insert(0, str(Path(__file__).parent))
import parse_historical_financials as P

INC, BAL = ("revenue", "pbt", "tax", "np"), ("ta", "tl", "te")

def load(d):
    out = {}
    for f in sorted(glob.glob(str(Path(d) / "*.json"))):
        for r in json.load(open(f)):
            out[r["key"]] = r
    return out

def same(a, b):
    return a is not None and b is not None and abs(a - b) <= max(1e-9, 0.0005 * max(abs(a), abs(b)))

def tie(a, b, tol=3):
    return abs(a - b) <= max(tol, 0.002 * max(abs(a), abs(b)))

def check(a, b, fields):
    if not a or not b:
        return None, "missing"
    try:
        sa = {k: float(a[k]) * float(a["unit"]) for k in fields}
        sb = {k: float(b[k]) * float(b["unit"]) for k in fields}
        unit = float(a["unit"])
    except (KeyError, TypeError, ValueError):
        return None, "incomplete"
    if not all(same(sa[k], sb[k]) for k in fields) or a.get("currency") != b.get("currency") or a.get("period_end") != b.get("period_end"):
        return None, "disagree"
    if fields is INC:
        ok = tie(sa["pbt"] - abs(sa["tax"]), sa["np"], 3 * unit) or tie(sa["pbt"] + abs(sa["tax"]), sa["np"], 3 * unit)
    else:
        ok = tie(sa["ta"], sa["tl"] + sa["te"], 3 * unit)
    return (dict(sa, currency=a.get("currency"), period_end=a.get("period_end"), period_months=a.get("period_months"), file=a.get("file"), page=a.get("page")), "accepted") if ok else (None, "identity_failed")

def on_page(sec, resolve, key, fields):
    """Printed values must be the rightmost figure of a row on the cited page."""
    path = resolve(key, sec["file"])
    with fitz.open(path) as doc:
        page = doc[int(sec["page"]) - 1]
        return all(P.rightmost_matches(page, sec[f] / sec["_unit"]) for f in fields)


def reconcile(da, db, resolve=None):
    A, B = load(da), load(db)
    out = {}
    for k in sorted(set(A) | set(B)):
        a, b = A.get(k, {}), B.get(k, {})
        i, si = check(a.get("income"), b.get("income"), INC)
        c, sc = check(a.get("balance"), b.get("balance"), BAL)
        if resolve:
            try:
                if i and not on_page({**i, "_unit": float(a["income"]["unit"])}, resolve, k, ("revenue", "pbt", "np")):
                    i, si = None, "not_rightmost"
                if c and not on_page({**c, "_unit": float(a["balance"]["unit"])}, resolve, k, ("te",)):
                    # equity may sit on the continuation page of the balance sheet
                    if not on_page({**c, "page": int(c["page"]) + 1, "_unit": float(a["balance"]["unit"])}, resolve, k, ("te",)):
                        c, sc = None, "not_rightmost"
            except Exception as e:
                i, c, si, sc = None, None, f"verify_error:{e}"[:60], f"verify_error:{e}"[:60]
        out[k] = {"income": i, "income_status": si, "balance": c, "balance_status": sc}
    return out

if __name__ == "__main__":
    json.dump(reconcile(sys.argv[1], sys.argv[2]), open(sys.argv[3], "w"), ensure_ascii=False, indent=0)
