#!/usr/bin/env python3
"""Blind spot-check packets: the checker sees the cited pages, never the parser's values."""
import json, sys, random
from pathlib import Path
import fitz
sys.path.insert(0, str(Path(__file__).parent))
import run_historical_parse as R
ERAS = [(a, b, int(n)) for a, b, n in (x.split(":") for x in sys.argv[2:])]
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
rows = [json.loads(x) for x in open(R.OUT / "parsed.jsonl")]
used = {json.loads(l)["key"] for f in out.parent.glob("*/packets.jsonl") if f.parent != out for l in open(f)}
rows = [r for r in rows if r["key"] not in used]
random.seed(20261120); packs = []
for a, b, n in ERAS:
    pool = [r for r in rows if a <= r["key"][:4] <= b and (r.get("income_ok") or r.get("balance_ok"))]
    for r in random.sample(pool, min(n, len(pool))):
        p = {"key": r["key"], "batch": r["batch"], "need_income": bool(r.get("income_ok")), "need_balance": bool(r.get("balance_ok")), "income_pages": [], "balance_pages": []}
        if r.get("income_ok"):
            with fitz.open(r["income_file"]) as d:
                pg = int(r["income_page"]); p["income_pages"] = [(Path(r["income_file"]).name, q, R.layout(d[q - 1])[:3800]) for q in (pg, pg + 1) if q <= d.page_count]
        if r.get("balance_ok"):
            with fitz.open(r["balance_file"]) as d:
                pg = int(r["balance_page"]); p["balance_pages"] = [(Path(r["balance_file"]).name, q, R.layout(d[q - 1])[:3800]) for q in (pg, pg + 1) if q <= d.page_count]
        packs.append(p)
with open(out / "packets.jsonl", "w") as f:
    for p in packs:
        f.write(json.dumps(p, ensure_ascii=False) + "\n")
print(len(packs))
