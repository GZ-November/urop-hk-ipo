#!/usr/bin/env python3
"""Download the financial sections of historical HK IPO prospectuses from HKEXnews.

Resumable. Writes PDFs and a status log under analysis/out/historical_financial_sources/.
Stops cleanly when the size budget is reached.
"""
import argparse, csv, json, re, threading, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis/out/historical_financial_sources"
HOST = "https://www1.hkexnews.hk"
BATCHES = [("batch1_2018_2024", 1), ("batch2_2008_2017", 2), ("batch3_2002_2007", 3)]
SECTIONS = [
    ("summary", re.compile(r"^\s*summary\b(?!.*(principal|constitution|articles|company law))", re.I)),
    ("financial_information", re.compile(r"^\s*financial\s+information\b", re.I)),
    ("accountants_report", re.compile(r"accountant", re.I)),
]
lock = threading.Lock()
total = {"bytes": 0}


def fetch(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (academic research)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as exc:
            if getattr(exc, "code", None) == 404 or i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def save(url, path, budget):
    if path.exists() and path.stat().st_size > 0:
        return path.stat().st_size
    with lock:
        if total["bytes"] >= budget:
            raise RuntimeError("budget")
    data = fetch(url)
    if not data.startswith(b"%PDF"):
        raise ValueError("not a PDF")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".part")
    tmp.write_bytes(data)
    tmp.rename(path)
    with lock:
        total["bytes"] += len(data)
    time.sleep(0.2)
    return len(data)


def links(html, base):
    out = []
    for href, text in re.findall(r"""<a\b[^>]*href=["']?([^"' >]+\.pdf)["']?[^>]*>(.*?)</a>""", html, re.I | re.S):
        label = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)).strip()
        out.append((urllib.parse.urljoin(base, href), label))
    return out


def work(job, budget):
    batch, key, url, fmt = job
    d = OUT / batch / key
    rec = {"batch": batch, "key": key, "url": url, "format": fmt, "status": "", "files": "", "bytes": 0, "note": ""}
    try:
        got = []
        if url.lower().endswith(".pdf"):
            got.append(("full", url, "single PDF"))
        else:
            html = fetch(url).decode("utf8", "ignore")
            ls = links(html, url)
            for name, rx in SECTIONS:
                hits = [(u, t) for u, t in ls if rx.search(t)]
                for i, (u, t) in enumerate(hits):
                    got.append((f"{name}_{i+1}", u, t))
            if not ls:
                got.append(("full", url[:-4] + ".pdf", "same-stem PDF"))
            elif not any(n.startswith("accountants") for n, _, _ in got):
                rec["note"] = "no accountants-report link; labels: " + " | ".join(t for _, t in ls)[:400]
                for u, t in ls:
                    if re.match(r"(?i)\s*appendix\s*(i|1|one|ia)\b", t):
                        got.append(("appendix_i", u, t))
                if not any(n.startswith("appendix") for n, _, _ in got):
                    got = [(f"part_{i+1}", u, t) for i, (u, t) in enumerate(ls)]
        files = []
        for name, u, t in got:
            n = save(u, d / f"{name}.pdf", budget)
            files.append({"name": name, "url": u, "label": t, "bytes": n})
            rec["bytes"] += n
        (d).mkdir(parents=True, exist_ok=True)
        (d / "index.json").write_text(json.dumps(files, ensure_ascii=False, indent=1))
        rec["files"] = ";".join(f["name"] for f in files)
        rec["status"] = "ok" if any(f["name"].startswith(("accountants", "full", "appendix", "part_")) for f in files) else "no_financial_section"
    except Exception as exc:
        rec["status"] = "budget" if str(exc) == "budget" else "error"
        rec["note"] = str(exc)[:200]
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int)
    ap.add_argument("--budget-gb", type=float, default=12)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    jobs = []
    for b, i in BATCHES:
        with open(ROOT / f"analysis/out/{b}_packets/batch{i}_packet_manifest.csv", newline="") as f:
            for r in csv.DictReader(f):
                u = (r.get("prospectus_url") or "").strip()
                if not u or u.lower() == "nan" or not (u.startswith("http") or u.startswith("/")):
                    continue
                u = u if u.startswith("http") else HOST + u
                jobs.append((b, Path(r["packet_path"]).stem, u, r.get("prospectus_format", "")))
    if a.limit:
        step = max(len(jobs) // a.limit, 1)
        jobs = jobs[::step][: a.limit]
    OUT.mkdir(parents=True, exist_ok=True)
    existing = sum(p.stat().st_size for p in OUT.rglob("*.pdf"))
    total["bytes"] = existing
    budget = a.budget_gb * 1e9
    rows = []
    with ThreadPoolExecutor(a.workers) as ex:
        for n, rec in enumerate(ex.map(lambda j: work(j, budget), jobs), 1):
            rows.append(rec)
            if n % 100 == 0:
                print(n, len(jobs), round(total["bytes"] / 1e9, 2), "GB", flush=True)
    with open(OUT / ("status_sample.csv" if a.limit else "status.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    c = {}
    for r in rows:
        c[r["status"]] = c.get(r["status"], 0) + 1
    print("done", c, round(total["bytes"] / 1e9, 2), "GB")


if __name__ == "__main__":
    main()
