#!/usr/bin/env python3
import json, sys, glob
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
C = Path(sys.argv[1]); W = C.parents[1] / "work"
P = {json.loads(l)["key"]: json.loads(l) for l in open(C / "packets.jsonl")}
D = {json.loads(l)["key"]: json.loads(l) for l in open(W / "parsed.jsonl")}
A = {}
for f in sorted(glob.glob(str(C / "A/*.json"))):
    for r in json.load(open(f)):
        A[r["key"]] = r
print("packets", len(P), "returned", len(A), "missing", sorted(set(P) - set(A))[:20])
rows = []
for k, p in P.items():
    a, d = A.get(k), D.get(k)
    if not a or not d:
        continue
    for sec, need, fs in (("income", "need_income", ("revenue", "pbt", "np")), ("balance", "need_balance", ("ta", "tl", "te"))):
        if not p[need]:
            continue
        s = a.get(sec)
        for f in fs:
            v = None
            try:
                v = float(s[f]) * float(s["unit"])
            except Exception:
                pass
            x = d.get(f)
            if x is None:
                rows.append(dict(key=k, era=k[:4], sec=sec, f=f, parser=None, checker=v, st="parser_now_blank", note=""))
                continue
            st = "checker_blank" if v is None else "match" if abs(v - x) <= 0.005 * max(abs(x), 1) else "DIFF"
            rows.append(dict(key=k, era=k[:4], sec=sec, f=f, parser=x, checker=v, st=st, note=(a.get("note") or "")[:110]))
        if sec == "income" and s and d.get("income_ok"):
            rows.append(dict(key=k, era=k[:4], sec="period", f="end", parser=d.get("period_end"), checker=s.get("period_end"), st="match" if d.get("period_end") == s.get("period_end") else "DIFF", note=""))
            rows.append(dict(key=k, era=k[:4], sec="period", f="months", parser=d.get("period_months"), checker=s.get("period_months"), st="match" if d.get("period_months") == s.get("period_months") else "DIFF", note=""))
r = pd.DataFrame(rows); r.to_csv(C / "comparison.csv", index=False)
print(pd.crosstab([r.sec, r.f], r.st).to_string())
print(r[r.st == "DIFF"].to_string(max_colwidth=70))
print(r[r.st == "checker_blank"].drop_duplicates(["key", "sec"])[["key", "sec", "note"]].to_string(max_colwidth=100))
