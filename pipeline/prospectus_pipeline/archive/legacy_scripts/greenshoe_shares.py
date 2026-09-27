#!/usr/bin/env python3
"""从「行使超额配售权」公告里取出实际配发股数，用于填 col_CV。

输入 out/allot/greenshoe.json 中 exercised=true 的公司与其公告链接。
输出 out/allot/greenshoe_shares.json：
  {code: {shares, pct_of_option, quote, page, doc_title, datetime, file, status}}

用法：
  python3 tools_greenshoe_shares.py                # 下载+抽取全部已行使公司
  python3 tools_greenshoe_shares.py --dump 0501.HK # 打印候选句，人工核对用
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

import yaml  # noqa: E402
import requests  # noqa: E402
from hkex import UA  # noqa: E402

G_DIR = ROOT / "data" / "allot" / "greenshoe"


def safe(code: str) -> str:
    return "HKIPO-MB" + "".join(ch for ch in str(code) if ch.isdigit())


def load_cfg():
    cfg = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    cfg["_root"] = ROOT
    return cfg


def download(cfg: dict, rec: dict) -> dict:
    (G_DIR / "pdf").mkdir(parents=True, exist_ok=True)
    dest = G_DIR / "pdf" / f"{safe(rec['code'])}.pdf"
    url = cfg["hkex"]["base_url"] + rec["file"]
    if dest.exists() and dest.stat().st_size > 20_000:
        return {**rec, "pdf": str(dest), "bytes": dest.stat().st_size, "download": "cached"}
    try:
        r = requests.get(url, timeout=180, headers={"User-Agent": UA}, stream=True)
        r.raise_for_status()
        tmp = dest.with_suffix(".part")
        with open(tmp, "wb") as fh:
            for chunk in r.iter_content(1 << 16):
                fh.write(chunk)
        tmp.rename(dest)
        return {**rec, "pdf": str(dest), "bytes": dest.stat().st_size, "download": "ok"}
    except Exception as exc:  # noqa: BLE001
        return {**rec, "pdf": None, "bytes": 0, "download": f"error: {type(exc).__name__}: {exc}"}


def to_pages(code: str) -> list[dict]:
    import fitz
    (G_DIR / "text").mkdir(parents=True, exist_ok=True)
    dest = G_DIR / "text" / f"{safe(code)}.jsonl"
    if dest.exists() and dest.stat().st_size > 0:
        return [json.loads(x) for x in dest.open(encoding="utf-8")]
    doc = fitz.open(G_DIR / "pdf" / f"{safe(code)}.pdf")
    with dest.open("w", encoding="utf-8") as fh:
        for i, page in enumerate(doc, 1):
            fh.write(json.dumps({"page": i, "text": page.get_text()}, ensure_ascii=False) + "\n")
    doc.close()
    return [json.loads(x) for x in dest.open(encoding="utf-8")]


# 数字：1,234,567 或 1234567
NUM = r"\d{1,3}(?:,\d{3})+|\d{4,}"
# 不能只靠单句正则：实际行文是
#   "... has been fully exercised by the Overall Coordinators (for themselves and on
#    behalf of the International Underwriters), on Saturday, February 7, 2026,
#    in respect of an aggregate of 4,337,300 H Shares (the "Over-allotment Shares") ..."
# 「exercised」与数字之间隔了 100+ 字符，因此改为**窗口锚定**：先定位每处
# over-allotment，再在 ±400 字符窗口里套下列数字句式。
PATTERNS = [
    re.compile(rf"in\s+respect\s+of\s+(?:an\s+aggregate\s+of\s+)?({NUM})\s*(?:new\s+)?(?:H\s+|Offer\s+)?Shares", re.I),
    re.compile(rf"over-?allocations?\s+of\s+(?:an\s+aggregate\s+of\s+)?({NUM})\s*(?:H\s+)?Shares", re.I),
    re.compile(rf"allot(?:ted)?\s+and\s+issued\s+(?:by\s+the\s+Company\s+)?(?:an\s+aggregate\s+of\s+)?({NUM})\s*(?:new\s+)?(?:H\s+)?Shares", re.I),
    re.compile(rf"subscri\w+\s+for\s+(?:an\s+aggregate\s+of\s+)?({NUM})\s*(?:new\s+)?(?:H\s+|Offer\s+)?Shares", re.I),
    re.compile(rf"({NUM})\s*(?:new\s+)?(?:H\s+)?Shares\s+(?:will\s+be|have\s+been|were)\s+(?:allotted|issued)", re.I),
]
ANCHOR = re.compile(r"over-?allotment", re.I)
WINDOW = 400
# "representing approximately 15.0% of the total number of the Offer Shares available
#  under the Global Offering (before any exercise of the Over-Allotment Option)"
PCT = re.compile(rf"representing\s+(?:approximately\s+)?([\d.]+)\s*%\s+of\s+the\s+(?:total\s+number\s+of\s+the\s+)?"
                 rf"(?:Offer\s+|H\s+)?Shares\s+(?:initially\s+available|available)", re.I)


def int_of(s: str) -> int:
    return int(s.replace(",", ""))


def extract(code: str) -> dict:
    pages = to_pages(code)
    cands: list[dict] = []
    for p in pages:
        flat = re.sub(r"\s+", " ", p["text"])
        for a in ANCHOR.finditer(flat):
            lo, hi = max(0, a.start() - WINDOW), min(len(flat), a.end() + WINDOW)
            win = flat[lo:hi]
            for pat in PATTERNS:
                for m in pat.finditer(win):
                    cands.append({"page": p["page"], "shares": int_of(m.group(1)),
                                  "quote": win[max(0, m.start() - 120):m.end() + 40].strip()})
    pcts = []
    for p in pages:
        for m in PCT.finditer(re.sub(r"\s+", " ", p["text"])):
            pcts.append({"page": p["page"], "pct": float(m.group(1))})
    # 去重 + 取众数（同一数字会在正文/表格/中文段重复出现）
    tally: dict[int, list[dict]] = {}
    for c in cands:
        tally.setdefault(c["shares"], []).append(c)
    best, best_n = None, 0
    for sh, items in tally.items():
        if len(items) > best_n or (len(items) == best_n and best is not None and sh > best):
            best, best_n = sh, len(items)
    return {
        "code": code,
        "status": "ok" if best is not None else "no_match",
        "shares": best,
        "hits": {str(k): len(v) for k, v in sorted(tally.items())},
        "candidates": cands,
        "pct_of_option": pcts[0] if pcts else None,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--dump", nargs="*", default=None, help="只打印候选句不做判定")
    args = ap.parse_args()

    cfg = load_cfg()
    g = json.loads((ROOT / "out" / "allot" / "greenshoe.json").read_text(encoding="utf-8"))
    exercised = [c for c, v in sorted(g.items()) if v.get("exercised")]
    if args.only:
        exercised = [c for c in exercised if c in set(args.only)]

    if args.dump:
        for c in args.dump:
            r = extract(c)
            print(f"===== {c} shares={r['shares']} hits={r['hits']} pct={r['pct_of_option']}")
            for cand in r["candidates"]:
                print(f"   p{cand['page']} {cand['shares']:>12,}  {cand['quote'][:230]}")
        return 0

    recs = []
    for c in exercised:
        m = next((x for x in g[c]["matches"] if x["kind"] == "exercise"), None)
        recs.append({"code": c, "file": m["file"], "doc_title": m["title"], "datetime": m["datetime"]})
    print(f"下载 {len(recs)} 份行使公告 ...")
    dl = []
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(download, cfg, r): r for r in recs}
        for i, fut in enumerate(as_completed(futs), 1):
            res = fut.result()
            dl.append(res)
            print(f"  [{i}/{len(recs)}] {res['code']:9s} {res['bytes']/1e6:5.2f}MB  {res['download']}")

    out = {}
    for r in sorted(dl, key=lambda x: x["code"]):
        if not r["pdf"]:
            out[r["code"]] = {"status": "error", "note": r["download"]}
            continue
        res = extract(r["code"])
        res.update({"doc_title": r["doc_title"], "datetime": r["datetime"], "file": r["file"]})
        out[r["code"]] = res
        print(f"  {r['code']:9s} CV={str(res['shares']):>12s}  hits={res['hits']}  pct={res['pct_of_option']}")

    dest = ROOT / "out" / "allot" / "greenshoe_shares.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    ok = sum(1 for v in out.values() if v.get("status") == "ok")
    print(f"\n行使股数抽取完成：{ok}/{len(out)} -> {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
