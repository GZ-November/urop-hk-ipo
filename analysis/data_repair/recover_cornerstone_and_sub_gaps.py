#!/usr/bin/env python3
"""Recover missing 2002-2024 cornerstone statuses from final prospectuses and
2005-2024 bloomberg_only subscription multiples from HKEXnews allotment announcements."""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin

import fitz
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import parse_allotment_subscription as SUBP

ROOT = Path(__file__).resolve().parents[2]
PANEL_PATH = ROOT / "analysis/out/overview_1994_2026/hkipo_33y_master_panel_1994_2026_tier1_complete.csv"
SRC_DIR = ROOT / "analysis/out/historical_financial_sources"
OUT_DIR = ROOT / "analysis/out/subscription_cornerstone_repair"
GAP_PDF_DIR = OUT_DIR / "gap_recovery_pdfs"
GAP_PDF_DIR.mkdir(parents=True, exist_ok=True)

HOST = "https://www1.hkexnews.hk"
SEARCH_URL = HOST + "/search/titleSearchServlet.do"

BATCH_MAP = {
    "1994-2001": "batch4_1994_2001",
    "2002-2007": "batch3_2002_2007",
    "2008-2017": "batch2_2008_2017",
    "2018-2024": "batch1_2018_2024",
}

BAD_PROS = re.compile(
    r"allot|result|supplement|formal\s*notice|application\s*form|new\s*listing|"
    r"price\s*determination|stabili[sz]|phip|post\s*hearing|application\s*proof|web\s*proof|wpip",
    re.I,
)
WANT_SEC = re.compile(
    r"corner\s*stone|corporate\s*(?:investor|placing)|structure\s+(?:and\s+conditions\s+)?of\s+(?:the\s+)?(?:global|share|public)?\s*(?:offer|placing)|"
    r"^\s*underwrit|\bsummary\b|history.*structure",
    re.I,
)
CS_RE = re.compile(
    r"(?i:corner\s*stone\s+(?:investor|placing|subscription|tranche|investment|shareholder|agreement)s?)|"
    r"\b(?:the|our)\s+corporate\s+(?:investors?|placing)\b|"
    r"\bcorporate\s+placing\b",
    re.I,
)
BOILER_RE = re.compile(
    r"(authorised\s+representative\s+of\s+a\s+corporate\s+investor|"
    r"investment\s+commitments?\s+by\s+any|"
    r"commitments?\s+(?:of|by)\s+(?:any\s+)?(?:the\s+)?corner\s*stone|"
    r"no\s+corner\s*stone|not\s+(?:have|has|had)\s+(?:any\s+)?corner\s*stone|"
    r"without\s+(?:any\s+)?corner\s*stone|"
    r"(?:any|if)\s+corner\s*stone|"
    r"other\s+than\s+(?:the\s+)?corner\s*stone\s+investors?\s*,?\s+if)",
    re.I,
)
BAD_ALLOT = re.compile(
    r"over-?allotment|stabili[sz]|exercise\s+of\s+(?:the\s+)?over-?allotment|"
    r"supplement|clarification|prospectus|formal\s*notice|wpip|phip|application\s*proof",
    re.I,
)
GOOD_ALLOT = re.compile(
    r"allot|results?\s+of|final\s+offer\s+price|offer\s+price\s+and\s+allot|"
    r"announcement\s+of\s+(?:offer\s+price|final\s+allocations)|public\s+offer",
    re.I,
)


def fetch(url: str, retries: int = 2) -> bytes:
    last_err: Exception | None = None
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.read()
        except Exception as e:
            last_err = e
            time.sleep(0.4 * (i + 1))
    raise last_err  # type: ignore[misc]


def load_stock_ids() -> dict[str, list[int]]:
    out: dict[str, list[int]] = {}
    for fn in ("activestock_sehk_e", "inactivestock_sehk_e"):
        rows = json.loads((ROOT / f"analysis/out/batch4_1994_2001_raw/{fn}.json").read_text())
        for r in rows:
            out.setdefault(str(r["c"]).zfill(5), []).append(r["i"])
    return out


def hkex_search(sid: int, frm: str, to: str) -> list[dict]:
    out: list[dict] = []
    for cat in ("0", "1"):
        q = urllib.parse.urlencode({
            "sortDir": "0", "sortByOptions": "DateTime", "category": cat, "market": "SEHK",
            "stockId": sid, "documentType": "-1", "fromDate": frm, "toDate": to,
            "title": "", "searchType": "0", "t1code": "-2", "t2Gcode": "-2", "t2code": "-2",
            "rowRange": "200", "lang": "EN",
        })
        try:
            res = json.loads(json.loads(fetch(f"{SEARCH_URL}?{q}")).get("result") or "[]")
            out.extend(res)
            time.sleep(0.15)
        except Exception:
            pass
        if out:
            break
    return out


def extract_links(html: str, base: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    for m in re.finditer(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.I | re.S):
        lbl = re.sub(r"<[^>]+>|\s+", " ", m.group(2)).strip()
        out.append((urljoin(base, m.group(1)), lbl))
    return out


def scan_pdf_bytes_or_path(src: Path | bytes, label: str = "") -> tuple[int, int, int, list[str], str]:
    """Return (pages, cs_hits_nonboiler, corp_hits_nonboiler, excerpts, text_sample)."""
    doc = fitz.open(src) if isinstance(src, Path) else fitz.open(stream=src, filetype="pdf")
    pages = doc.page_count
    cs_hits = 0
    corp_hits = 0
    excerpts: list[str] = []
    total_chars = 0
    try:
        for i, pg in enumerate(doc):
            raw = pg.get_text()
            total_chars += len(raw.strip())
            t = re.sub(r"\s+", " ", raw)
            for m in CS_RE.finditer(t):
                win = t[max(0, m.start() - 100):m.end() + 120]
                if BOILER_RE.search(win):
                    continue
                matched = m.group(0).lower()
                if "corner" in matched:
                    cs_hits += 1
                else:
                    corp_hits += 1
                if len(excerpts) < 5:
                    excerpts.append(f"{label}p{i+1}: " + t[max(0, m.start() - 180):m.end() + 260])
    finally:
        doc.close()
    return pages, cs_hits, corp_hits, excerpts, ("scanned" if pages > 0 and total_chars < 200 else "text")


def pick_best_prospectus(rows: list[dict]) -> dict | None:
    cands = []
    for x in rows:
        t, lt = x.get("TITLE", ""), x.get("LONG_TEXT", "")
        if BAD_PROS.search(t) or "supplement" in lt.lower() or "phip" in lt.lower() or "application proof" in lt.lower():
            continue
        if re.search(r"prospectus|global\s+offering|share\s+offer|public\s+offer|placing|new\s+issue|offer\s+for\s+subscription", t, re.I) or "Listing Documents" in lt:
            cands.append(x)
    if not cands:
        return None
    def score(x: dict) -> tuple:
        t, lt, fl = x.get("TITLE", ""), x.get("LONG_TEXT", ""), x.get("FILE_LINK", "").lower()
        return (
            not re.match(r"^\s*prospectuses?\s*$", t, re.I),
            "Listing Documents" not in lt,
            not re.search(r"prospectus|global\s+offering", t, re.I),
            not fl.endswith(".pdf"),
        )
    cands.sort(key=score)
    return cands[0]


def process_cs_row(job: dict, idmap: dict[str, list[int]]) -> dict:
    k = job["key"]
    rec: dict = {
        "key": k,
        "cohort_year": job["cohort_year"],
        "board": job["board"],
        "pros_url": "",
        "pros_kind": "",
        "pages": 0,
        "text_layer": "",
        "cs_hits": 0,
        "corp_hits": 0,
        "sec_labels": [],
        "excerpts": [],
        "candidate": "unresolved",
        "err": "",
    }
    try:
        # 1. Check if full.pdf or part_*.pdf already exists locally
        local_dir = SRC_DIR / BATCH_MAP[job["batch"]] / k
        whole = sorted(list(local_dir.glob("full.pdf")) + list(local_dir.glob("part_*.pdf"))) if local_dir.exists() else []
        if (local_dir / "full.pdf").exists() or len(whole) >= 8:
            pgs = cs = corp = 0
            ex: list[str] = []
            layers = set()
            for wp in whole:
                p_cnt, c1, c2, e1, lyr = scan_pdf_bytes_or_path(wp, label=f"{wp.name} ")
                pgs += p_cnt; cs += c1; corp += c2; layers.add(lyr)
                for item in e1:
                    if len(ex) < 5:
                        ex.append(item)
            rec.update(
                pros_url="local", pros_kind="local_full", pages=pgs,
                text_layer="scanned" if layers == {"scanned"} else "text",
                cs_hits=cs, corp_hits=corp, excerpts=ex,
            )
            if rec["text_layer"] == "scanned":
                rec["candidate"] = "scanned_pdf"
            elif cs > 0:
                rec["candidate"] = "yes_cs"
            elif corp > 0:
                rec["candidate"] = "yes_corp_review"
            else:
                rec["candidate"] = "clean_no"
            return rec

        # 2. Query HKEXnews for final prospectus
        code = re.sub(r"\D", "", str(job["stock_code"])).zfill(5)[-5:]
        d = pd.to_datetime(job["listing_date"])
        frm, to = (d - dt.timedelta(days=45)).strftime("%Y%m%d"), (d + dt.timedelta(days=3)).strftime("%Y%m%d")
        cand = None
        for sid in idmap.get(code, []):
            rows = hkex_search(sid, frm, to)
            cand = pick_best_prospectus(rows)
            if cand:
                break
        if not cand:
            rec["candidate"] = "not_found_hkex"
            return rec

        u = HOST + cand["FILE_LINK"]
        rec["pros_url"] = u
        if u.lower().endswith((".htm", ".html")):
            rec["pros_kind"] = "index"
            html = fetch(u).decode("utf8", "ignore")
            ls = extract_links(html, u)
            sec_cs = [lbl for _, lbl in ls if re.search(r"corner\s*stone|corporate\s*(?:investor|placing)", lbl, re.I)]
            rec["sec_labels"] = sec_cs[:10]
            want = [(href, lbl) for href, lbl in ls if WANT_SEC.search(lbl) and href.lower().endswith(".pdf")]
            if not want:
                # Fallback: grab first 5 pdfs
                want = [(href, lbl) for href, lbl in ls if href.lower().endswith(".pdf")][:6]
            pgs = cs = corp = 0
            ex: list[str] = []
            layers = set()
            for href, lbl in want[:8]:
                data = fetch(href)
                if not data.startswith(b"%PDF"):
                    continue
                p_cnt, c1, c2, e1, lyr = scan_pdf_bytes_or_path(data, label=f"[{lbl[:30]}] ")
                pgs += p_cnt; cs += c1; corp += c2; layers.add(lyr)
                for item in e1:
                    if len(ex) < 5:
                        ex.append(item)
                time.sleep(0.08)
            rec.update(pages=pgs, text_layer="scanned" if layers == {"scanned"} else "text", cs_hits=cs, corp_hits=corp, excerpts=ex)
        else:
            rec["pros_kind"] = "pdf"
            pdf_path = GAP_PDF_DIR / f"{k}_pros.pdf"
            if not pdf_path.exists():
                data = fetch(u)
                if not data.startswith(b"%PDF"):
                    rec["candidate"] = "non_pdf_response"
                    return rec
                pdf_path.write_bytes(data)
            pgs, cs, corp, ex, lyr = scan_pdf_bytes_or_path(pdf_path, label="pros ")
            rec.update(pages=pgs, text_layer=lyr, cs_hits=cs, corp_hits=corp, excerpts=ex)

        if rec["text_layer"] == "scanned":
            rec["candidate"] = "scanned_pdf"
        elif rec["cs_hits"] > 0 or any("corner" in s.lower() or "corporate placing" in s.lower() for s in rec["sec_labels"]):
            rec["candidate"] = "yes_cs"
        elif rec["corp_hits"] > 0 or rec["sec_labels"]:
            rec["candidate"] = "yes_corp_review"
        elif rec["pages"] > 0:
            rec["candidate"] = "clean_no"
        else:
            rec["candidate"] = "empty_pdf"
    except Exception as e:
        rec["err"] = str(e)[:150]
        rec["candidate"] = "error"
    return rec


def process_sub_row(job: dict, idmap: dict[str, list[int]]) -> dict:
    k = job["key"]
    rec: dict = {
        "key": k,
        "cohort_year": job["cohort_year"],
        "board": job["board"],
        "bbg_val": job["bbg_val"],
        "allot_url": "",
        "parsed": None,
        "how": "",
        "calc": None,
        "sentence_value": None,
        "quote": "",
        "status": "not_found",
        "err": "",
    }
    try:
        code = re.sub(r"\D", "", str(job["stock_code"])).zfill(5)[-5:]
        d = pd.to_datetime(job["listing_date"])
        frm, to = (d - dt.timedelta(days=12)).strftime("%Y%m%d"), (d + dt.timedelta(days=5)).strftime("%Y%m%d")
        cands = []
        for sid in idmap.get(code, []):
            for x in hkex_search(sid, frm, to):
                t, lt = x.get("TITLE", ""), x.get("LONG_TEXT", "")
                if BAD_ALLOT.search(t) or "supplement" in lt.lower():
                    continue
                if GOOD_ALLOT.search(t) or "Allotment Results" in lt:
                    cands.append(x)
            if cands:
                break
        if not cands:
            return rec
        cands.sort(key=lambda x: ("allot" not in x.get("TITLE", "").lower(), "Allotment" not in x.get("LONG_TEXT", ""), not x.get("FILE_LINK", "").lower().endswith(".pdf")))
        u = HOST + cands[0]["FILE_LINK"]
        rec["allot_url"] = u

        text_chunks: list[str] = []
        if u.lower().endswith((".htm", ".html")):
            html = fetch(u).decode("utf8", "ignore")
            ls = extract_links(html, u)
            pdfs = [(href, lbl) for href, lbl in ls if href.lower().endswith(".pdf") and any(w in lbl.lower() for w in ["summary", "cover", "allot", "offer", "application", "result"])]
            if not pdfs:
                pdfs = [(href, lbl) for href, lbl in ls if href.lower().endswith(".pdf")][:3]
            for href, _ in pdfs[:3]:
                data = fetch(href)
                if data.startswith(b"%PDF"):
                    doc = fitz.open(stream=data, filetype="pdf")
                    for pg in doc[:10]:
                        text_chunks.append(pg.get_text())
                    doc.close()
        else:
            data = fetch(u)
            if data.startswith(b"%PDF"):
                doc = fitz.open(stream=data, filetype="pdf")
                for pg in doc[:12]:
                    text_chunks.append(pg.get_text())
                doc.close()

        full_text = re.sub(r"\s+", " ", " ".join(text_chunks))
        if len(full_text) < 200:
            rec["status"] = "empty_or_scanned"
            return rec
        v, q, n = SUBP.parse(full_text)
        bp = SUBP.block_parse(full_text)
        lv = SUBP.level_parse(full_text)
        placing_only = not re.search(SUBP.PUB, full_text, re.I) and bool(re.search(r"\bplacing\b", full_text, re.I))
        val, how, calc = v, "sentence" if v is not None else "", None
        if lv is not None:
            val, how = lv, "subscription_level"
        if bp:
            calc = bp[1]
            if bp[2] or val is None:
                val = bp[0]
                how = "arithmetic_ok" if bp[2] else "valid_applications"
                q = bp[3]
                if bp[2] and v is not None and abs(v - bp[0]) > 0.02 * max(abs(bp[0]), 0.01):
                    how = "conflict"
        rec.update(
            parsed=val, how=how, calc=calc, sentence_value=v,
            quote=(q or "")[:350],
            status="placing_only" if (val is None and placing_only) else ("parsed" if val is not None else "unparsed"),
        )
    except Exception as e:
        rec["err"] = str(e)[:150]
        rec["status"] = "error"
    return rec


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    p = pd.read_csv(PANEL_PATH, low_memory=False)
    p["key"] = p["file"].str.replace(".json", "", regex=False)
    idmap = load_stock_ids()

    if mode in ("all", "cs"):
        bl = p[(p["cohort_year"].between(2002, 2024)) & (p["ext_has_cornerstone"].isna())].copy()
        jobs = [
            {
                "key": r["key"], "batch": r["batch"], "cohort_year": int(r["cohort_year"]),
                "board": r["board"], "stock_code": r["stock_code"], "listing_date": r["listing_date"],
            }
            for _, r in bl.iterrows()
        ]
        out_cs = OUT_DIR / "gap_recovery_prospectus_cs.jsonl"
        done: dict[str, dict] = {}
        if out_cs.exists():
            for ln in out_cs.open():
                if ln.strip():
                    d = json.loads(ln)
                    if d.get("candidate") != "error":
                        done[d["key"]] = d
        todo = [j for j in jobs if j["key"] not in done]
        print(f"[CS recovery] total={len(jobs)}, cached={len(done)}, todo={len(todo)}", flush=True)
        with ThreadPoolExecutor(6) as ex, out_cs.open("a") as f:
            for i, res in enumerate(ex.map(lambda j: process_cs_row(j, idmap), todo), 1):
                f.write(json.dumps(res, ensure_ascii=False) + "\n")
                f.flush()
                if i % 25 == 0 or i == len(todo):
                    print(f"  [CS] {i}/{len(todo)}", flush=True)

    if mode in ("all", "sub"):
        bsub = p[(p["ext_retail_sub_source"] == "bloomberg_only") & (p["cohort_year"].between(2005, 2024))].copy()
        jobs_s = [
            {
                "key": r["key"], "cohort_year": int(r["cohort_year"]), "board": r["board"],
                "stock_code": r["stock_code"], "listing_date": r["listing_date"],
                "bbg_val": float(r["retail_sub_ratio_clean"]) if pd.notna(r["retail_sub_ratio_clean"]) else None,
            }
            for _, r in bsub.iterrows()
        ]
        out_sub = OUT_DIR / "gap_recovery_allot_sub.jsonl"
        done_s: dict[str, dict] = {}
        if out_sub.exists():
            for ln in out_sub.open():
                if ln.strip():
                    d = json.loads(ln)
                    if d.get("status") != "error":
                        done_s[d["key"]] = d
        todo_s = [j for j in jobs_s if j["key"] not in done_s]
        print(f"[SUB recovery] total={len(jobs_s)}, cached={len(done_s)}, todo={len(todo_s)}", flush=True)
        with ThreadPoolExecutor(6) as ex, out_sub.open("a") as f:
            for i, res in enumerate(ex.map(lambda j: process_sub_row(j, idmap), todo_s), 1):
                f.write(json.dumps(res, ensure_ascii=False) + "\n")
                f.flush()
                if i % 25 == 0 or i == len(todo_s):
                    print(f"  [SUB] {i}/{len(todo_s)}", flush=True)


if __name__ == "__main__":
    main()
