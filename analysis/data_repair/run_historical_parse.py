#!/usr/bin/env python3
"""Parse every downloaded issuer and write work packets for what the parser cannot accept."""
import calendar
import argparse, json, re, sys
from multiprocessing import Pool
from pathlib import Path
import fitz
sys.path.insert(0, str(Path(__file__).parent))
import parse_historical_financials as P

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "analysis/out/historical_financial_sources"
OUT = SRC / "work"
HINT = re.compile(r"\b(revenues?|turnover|before\s+(?:income\s+)?tax|total\s+assets|current\s+liabilities|net\s+assets|total\s+equity)\b", re.I)
MONTHS = "january february march april may june july august september october november december".split()
WORD = {"three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11}


def docs(d):
    idx = json.loads((d / "index.json").read_text())
    names = [f["name"] for f in idx]
    ar = [n for n in names if n.startswith(("accountants", "appendix_i"))]
    if ar:
        return [d / f"{n}.pdf" for n in ar], False
    whole = [n for n in names if n == "full" or n.startswith("part_")]
    if whole:
        return [d / f"{n}.pdf" for n in whole], True
    return [], False


def period(path, page):
    with fitz.open(path) as doc:
        ls = layout(doc[page - 1]).splitlines()
    idx = next((i for i, x in enumerate(ls) if re.match(r"\s*(total\s+|net\s+)?(revenues?|turnover|sales)\b", x, re.I)), None)
    if idx is None:
        return None, None
    head = "\n".join(ls[max(0, idx - 8):idx])
    years = re.findall(r"\b((?:19|20)\d\d)\b", head)
    month_rx = "|".join(MONTHS)
    dates = [(m.group(1) or m.group(4), m.group(2) or m.group(3)) for m in
             re.finditer(rf"\b(\d{{1,2}})(?:st|nd|rd|th)?\s+({month_rx})\b|\b({month_rx})\s+(\d{{1,2}})\b(?!\d)", head, re.I)]
    if not years or not dates:
        return None, None
    year = max(years)
    dated = re.findall(rf"\b(\d{{1,2}})(?:st|nd|rd|th)?\s+({month_rx}),?\s+((?:19|20)\d\d)\b", head, re.I)
    if re.search(r"period\s+from|from\s+\d{1,2}", head, re.I):
        # A first column running from incorporation must not be read as the latest period.
        last = [(d, m) for d, m, y in dated if y == year]
        if len(last) == 1 and re.search(r"year\s+ended", head, re.I):
            d, m = last[0]
            return f"{year}-{MONTHS.index(m.lower())+1:02d}-{int(d):02d}", 12
        return None, None
    day, mon = dates[-1]
    stub = re.search(r"\b(three|four|five|six|seven|eight|nine|ten|eleven|\d{1,2})[\s-]+months?\b", head, re.I)
    months = 12
    distinct = {m.lower() for _, m in dates}
    if stub:
        s = stub.group(1).lower()
        months = WORD.get(s) or int(s)
        if len(distinct) == 1 and re.search(r"year\s+ended", head, re.I):
            # Only the fiscal year end is printed; the stub ends that many months after it.
            m = (MONTHS.index(mon.lower()) + months) % 12
            y = int(year)
            return f"{y}-{m+1:02d}-{calendar.monthrange(y, m+1)[1]:02d}", months
    elif len(distinct) > 1:
        # "Year ended 31 December ... Period ended 31 August": stub length from the fiscal year end
        months = (MONTHS.index(mon.lower()) - MONTHS.index(dates[0][1].lower())) % 12 or 12
    return f"{year}-{MONTHS.index(mon.lower())+1:02d}-{int(day):02d}", months


def layout(page):
    out = []
    for lw in P.lines(page):
        s, x = "", 0
        for w in lw:
            gap = int(max(1, (w[0] - x) / 6)) if s else 0
            s += " " * min(gap, 12) + w[4]
            x = w[2]
        out.append(s)
    return "\n".join(out)


def candidates(paths, whole):
    inc, bal = [], []
    n_text = 0
    for p in paths:
        with fitz.open(p) as doc:
            take_next = False
            for i in range(doc.page_count):
                pg = doc[i]
                t = pg.get_text()
                n_text += len(t)
                if whole and not P.in_accountants_report(pg):
                    take_next = False
                    continue
                head = layout(pg)[:900]
                company = re.search(r"of\s+(?:the\s+)?company\b", head, re.I) and not re.search(r"group|consolidated|combined", head, re.I)
                rank = 0 if re.search(r"consolidated|combined", head, re.I) else 1
                item = (rank, p.name, i + 1, layout(pg)[:3800])
                if company:
                    take_next = False
                elif P.BS_T.search(t) and re.search(r"current\s+(assets|liabilities)|total\s+assets", t, re.I):
                    bal.append(item); take_next = True
                elif take_next and re.search(r"liabilities|equity|net\s+assets", t, re.I):
                    bal.append(item); take_next = False
                else:
                    take_next = False
                    if P.IS_T.search(t) and re.search(r"before\s+(?:income\s+)?tax", t, re.I) and re.search(r"revenue|turnover|sales", t, re.I):
                        inc.append(item)
    pick = lambda xs, n: [x[1:] for x in sorted(xs, key=lambda x: x[0])[:n]]
    return pick(inc, 3), sorted(pick(bal, 5), key=lambda x: (x[0], x[1])), n_text


def one(d):
    rec = {"batch": d.parent.name, "key": d.name}
    try:
        paths, whole = docs(d)
        rec["source"] = "full" if whole else "section"
        if not paths:
            rec["state"] = "no_accountants_report"
            return rec, None
        r = P.parse_doc(paths, whole)
        i, b = r["income"], r["balance"]
        if i and b:
            rev, ta = abs(i["revenue"] * i["unit"]), b["ta"] * b["unit"]
            if ta < rev / 100 or (i["ccy"] and b["ccy"] and i["ccy"] != b["ccy"]):
                r["balance"] = None
                r["flags"].append("balance_scale_or_currency_mismatch")
        rec.update(P.values(r))
        rec["flags"] = r["flags"]
        if r["income"]:
            rec["period_end"], rec["period_months"] = period(r["income"]["file"], r["income"]["page"])
        rec["income_ok"], rec["balance_ok"] = bool(r["income"]), bool(r["balance"])
        rec["state"] = "parsed" if r["income"] and r["balance"] else "partial" if r["income"] or r["balance"] else "unparsed"
        pack = None
        if rec["state"] != "parsed":
            inc, bal, n = candidates(paths, whole)
            rec["text_chars"] = n
            if n < 2000:
                rec["state"] = "scanned"
            else:
                pack = {"key": d.name, "batch": d.parent.name, "need_income": not r["income"], "need_balance": not r["balance"],
                        "income_pages": inc if not r["income"] else [], "balance_pages": bal if not r["balance"] else []}
    except Exception as e:
        rec["state"], rec["error"] = "error", str(e)[:150]
        pack = None
    return rec, pack


def refresh_periods():
    rows = [json.loads(x) for x in open(OUT / "parsed.jsonl")]
    n = 0
    for r in rows:
        if r.get("income_ok"):
            try:
                r["period_end"], r["period_months"] = period(r["income_file"], int(r["income_page"]))
            except Exception:
                r["period_end"], r["period_months"] = None, None
            n += r["period_end"] is not None
    with open(OUT / "parsed.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("periods", n, "of", sum(bool(r.get("income_ok")) for r in rows))


def main():
    if "--refresh-periods" in sys.argv:
        return refresh_periods()
    if "--filter-column-order" in sys.argv:
        rows = [json.loads(x) for x in open(OUT / "parsed.jsonl")]
        n = {"income": 0, "balance": 0}
        for r in rows:
            for sec, file_key, page_key, fields in (("income", "income_file", "income_page", ("revenue", "pbt", "np", "tax", "ccy", "period_end", "period_months")), ("balance", "balance_file", "balance_page", ("ta", "tl", "te", "bal_ccy"))):
                if not r.get(sec + "_ok"):
                    continue
                with fitz.open(r[file_key]) as doc:
                    bad = P.latest_period_on_left(doc[int(r[page_key]) - 1])
                if bad:
                    n[sec] += 1
                    r[sec + "_ok"] = False
                    r.setdefault("flags", []).append("latest_period_on_left:" + sec)
                    for f in fields:
                        r.pop(f, None)
        with open(OUT / "parsed.jsonl", "w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("removed", n)
        return
    if "--reparse-full" in sys.argv:
        rows = {json.loads(x)["key"]: json.loads(x) for x in open(OUT / "parsed.jsonl")}
        ds = [SRC / r["batch"] / k for k, r in rows.items() if r.get("source") == "full"]
        with Pool(6) as pool:
            for rec, _ in pool.imap_unordered(one, ds, 4):
                rows[rec["key"]] = rec
        with open(OUT / "parsed.jsonl", "w") as f:
            for r in rows.values():
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("reparsed", len(ds))
        return
    a = argparse.ArgumentParser(); a.add_argument("--workers", type=int, default=6); a.add_argument("--only-new", action="store_true"); a.add_argument("--min-year", type=int, default=2005); a = a.parse_args()
    ds = sorted(p.parent for p in SRC.glob("batch*/*/index.json") if int(p.parent.name[:4]) >= a.min_year)
    OUT.mkdir(exist_ok=True)
    mode = "w"
    if a.only_new:
        seen = {json.loads(x)["key"] for x in open(OUT / "parsed.jsonl")}
        ds = [d for d in ds if d.name not in seen]
        mode = "a"
    packets = OUT / ("packets_new.jsonl" if a.only_new else "packets.jsonl")
    with Pool(a.workers) as pool, open(OUT / "parsed.jsonl", mode) as f, open(packets, "w") as g:
        c = {}
        for rec, pack in pool.imap_unordered(one, ds, 8):
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            c[rec["state"]] = c.get(rec["state"], 0) + 1
            if pack and (pack["income_pages"] or pack["balance_pages"]):
                g.write(json.dumps(pack, ensure_ascii=False) + "\n")
    print(c)


if __name__ == "__main__":
    main()
