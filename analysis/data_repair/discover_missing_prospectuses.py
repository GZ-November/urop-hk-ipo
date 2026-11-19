#!/usr/bin/env python3
"""Find listing documents on HKEXnews for issuers the first download could not resolve."""
import json, re, sys, time, datetime as dt, urllib.parse, urllib.request
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
import download_historical_financial_sections as D

ROOT = D.ROOT
URL = "https://www1.hkexnews.hk/search/titleSearchServlet.do"
BATCH = {"1994-2001": "batch4_1994_2001", "2002-2007": "batch3_2002_2007", "2008-2017": "batch2_2008_2017", "2018-2024": "batch1_2018_2024"}
GOOD = re.compile(r"prospectus|global offering|share offer|public offer|new issue|placing|offer for subscription|listing document|introduction", re.I)
BAD = re.compile(r"allot|result|supplement|formal notice|application form|new listing|price determination|stabili[sz]", re.I)


def ids():
    out = {}
    for f in ("activestock_sehk_e", "inactivestock_sehk_e"):
        for r in json.load(open(ROOT / f"analysis/out/batch4_1994_2001_raw/{f}.json")):
            out.setdefault(str(r["c"]).zfill(5), []).append(r["i"])
    return out


def search(sid, frm, to):
    for cat in ("0", "1"):
        q = urllib.parse.urlencode({"sortDir": "0", "sortByOptions": "DateTime", "category": cat, "market": "SEHK", "stockId": sid,
                                    "documentType": "-1", "fromDate": frm, "toDate": to, "title": "", "searchType": "0",
                                    "t1code": "-2", "t2Gcode": "-2", "t2code": "-2", "rowRange": "200", "lang": "EN"})
        rows = json.loads(json.loads(D.fetch(f"{URL}?{q}")).get("result") or "[]")
        time.sleep(0.25)
        if rows:
            return rows
    return []


def rank(x):
    t, l = x.get("TITLE", ""), x.get("LONG_TEXT", "")
    return (not re.match(r"\s*prospectus", t, re.I), "Listing Documents" not in l, not re.search("prospectus|global offering", t, re.I))


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    st = pd.read_csv(D.OUT / "status.csv")
    ok = set(st[st.status == "ok"].key)
    p = pd.read_csv(ROOT / "analysis/out/overview_1994_2026/hkipo_33y_master_panel_1994_2026_tier1_complete.csv", dtype=str, low_memory=False)
    p = p[p.batch != "2025-2026"].copy()
    p["key"] = p.file.astype(str).map(lambda s: Path(s).stem)
    todo = p[~p.key.isin(ok)]
    if limit:
        todo = pd.concat([g.sample(min(limit, len(g)), random_state=5) for _, g in todo.groupby("batch")])
    print("to discover", len(todo), flush=True)
    idmap, rows = ids(), []
    for n, r in enumerate(todo.itertuples(), 1):
        rec = {"batch": BATCH[r.batch], "key": r.key, "url": "", "format": "discovered", "status": "not_found", "files": "", "bytes": 0, "note": ""}
        try:
            code = re.sub(r"\D", "", str(r.stock_code)).zfill(5)[-5:]
            d = pd.to_datetime(r.listing_date, format="mixed")
            frm, to = (d - dt.timedelta(days=45)).strftime("%Y%m%d"), (d + dt.timedelta(days=3)).strftime("%Y%m%d")
            cand = []
            for sid in idmap.get(code, []):
                for x in search(sid, frm, to):
                    title, long_text = x.get("TITLE", ""), x.get("LONG_TEXT", "")
                    if re.match(r"\s*prospectus", title, re.I) or "Listing Documents" in long_text:
                        if not BAD.search(title) and "Supplement" not in long_text:
                            cand.append(x)
            cand.sort(key=rank)
            if cand:
                u = D.HOST + cand[0]["FILE_LINK"]
                rec = D.work((BATCH[r.batch], r.key, u, "discovered"), 15e9)
                rec["note"] = (rec["note"] + " title=" + cand[0].get("TITLE", ""))[:300]
        except Exception as e:
            rec["status"], rec["note"] = "error", str(e)[:200]
        rows.append(rec)
        if n % 50 == 0:
            print(n, len(todo), flush=True)
    pd.DataFrame(rows).to_csv(D.OUT / ("status_discovered_sample.csv" if limit else "status_discovered.csv"), index=False)
    print(pd.DataFrame(rows).groupby(["batch", "status"]).size())


if __name__ == "__main__":
    main()
