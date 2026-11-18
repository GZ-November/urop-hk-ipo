#!/usr/bin/env python3
"""Read offering-structure and underwriting sections for explicit cornerstone language."""
import csv, json, re, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import fitz
sys.path.insert(0, str(Path(__file__).parent))
from download_historical_financial_sections import fetch, links

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "analysis/out/historical_financial_sources"
OUT = ROOT / "analysis/out/subscription_cornerstone_repair"
WANT = re.compile(r"structure\s+(?:and\s+conditions\s+)?of\s+(?:the\s+)?(?:global\s+|share\s+)?(?:offer|placing)|structure\s+of\s+the\s+(?:global|share)|^\s*underwrit", re.I)
CS = re.compile(r"(?i:corner\s*stone\s+(?:investor|placing|subscription|tranche|investment|shareholder))|\b(?:[Tt]he|[Oo]ur)\s+Corporate\s+(?:Investors?|Placing)\b")


def scan(paths):
    hits, ctx, pages = 0, [], 0
    for p in paths:
        with fitz.open(p) as d:
            pages += d.page_count
            for i, pg in enumerate(d):
                t = re.sub(r"\s+", " ", pg.get_text())
                for m in CS.finditer(t):
                    hits += 1
                    if len(ctx) < 3:
                        ctx.append(f"{Path(p).name} p{i+1}: " + t[max(0, m.start() - 220):m.end() + 260])
    return hits, ctx, pages


def one(e):
    k, b = e["key"], e["batch"]
    rec = {"key": k, "kind": e["kind"], "files": 0, "pages": 0, "hits": 0, "ctx": [], "err": ""}
    d = SRC / b / k
    try:
        if e["kind"] == "pdf":
            ps = sorted(list(d.glob("full.pdf")) + list(d.glob("part_*.pdf")))
        else:
            ps = sorted(d.glob("cs_section_*.pdf"))
            ls = [] if ps else links(fetch(e["url"]).decode("utf8", "ignore"), e["url"])
            for n, (u, label) in enumerate(x for x in ls if WANT.search(x[1])):
                f = d / f"cs_section_{n+1}.pdf"
                if not f.exists():
                    data = fetch(u)
                    if data.startswith(b"%PDF"):
                        f.write_bytes(data)
                        time.sleep(0.15)
                if f.exists():
                    ps.append(f)
            ps += sorted(d.glob("summary_*.pdf"))
        rec["files"] = len(ps)
        rec["hits"], rec["ctx"], rec["pages"] = scan(ps)
    except Exception as x:
        rec["err"] = str(x)[:80]
    return rec


def main():
    st = {r["key"]: r for r in csv.DictReader(open(SRC / "status.csv")) if r["url"]}
    ev = [json.loads(l) for l in open(OUT / "cornerstone_evidence.jsonl")]
    jobs = []
    for e in ev:
        if e["section_hit"] or e["key"] not in st:
            continue
        kind = "pdf" if e["source"] == "pdf" else "index" if e["source"] == "index" and e["sections"] >= 8 else None
        if kind:
            jobs.append({"key": e["key"], "batch": st[e["key"]]["batch"], "url": e["url"], "kind": kind})
    print(len(jobs), flush=True)
    with ThreadPoolExecutor(5) as ex, open(OUT / "cornerstone_sections.jsonl", "w") as f:
        for r in ex.map(one, jobs):
            f.write(json.dumps(r, ensure_ascii=False) + "\n"); f.flush()


main()
