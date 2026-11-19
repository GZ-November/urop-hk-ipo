#!/usr/bin/env python3
"""Turn parser work packets into small batch files for blind double extraction."""
import argparse, json
from pathlib import Path

def block(p):
    out = [f"\n## ISSUER {p['key']}", f"need_income={str(p['need_income']).lower()} need_balance={str(p['need_balance']).lower()}"]
    for kind, pages in (("INCOME", p["income_pages"]), ("BALANCE", p["balance_pages"])):
        for f, n, text in pages:
            out += [f"\n### {kind} CANDIDATE file={f} page={n}", "```", text, "```"]
    return "\n".join(out)

def main():
    a = argparse.ArgumentParser(); a.add_argument("packets"); a.add_argument("outdir"); a.add_argument("--size", type=int, default=20)
    a = a.parse_args(); out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
    P = [json.loads(x) for x in open(a.packets)]
    P.sort(key=lambda p: p["key"])
    for i in range(0, len(P), a.size):
        (out / f"batch_{i//a.size+1:03d}.md").write_text("\n".join(block(p) for p in P[i:i+a.size]))
    print(len(P), "issuers", (len(P)+a.size-1)//a.size, "batches")
main()
