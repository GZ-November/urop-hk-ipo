"""超额配售权（绿鞋）核实：col_CV 的确定性来源。

为什么必须单独查：
  配发结果公告只写「假設超額配售權未行使」的口径，或一句
  "In the event the Over-allotment Option is exercised, an announcement will be made"，
  这**不能**用来推断 col_CV = 0。唯一确定性证据是上市后 30 天内港交所有没有
  发出行使公告：
    - 有行使公告 -> col_CV = 公告里的实际配发股数（含部分行使）
    - 无行使公告且窗口已过 -> col_CV = 0（确定的零，写 0 不写 NaN）
    - 窗口未过 -> col_CV = NaN（还不知道）

输出：
  out/allot/greenshoe.json        每家的公告检索结果
  out/allot/greenshoe_shares.json 已行使公司的股数与原文
  data/allot/greenshoe/{pdf,text}/ 行使公告原文（供证据引用）
"""
from __future__ import annotations

import datetime as dt
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from storage import atomic_json, official_files

from hkex import UA, _search_by_id

WINDOW_DAYS = 45  # 法规窗口为上市后 30 天，多给 15 天覆盖周末与公告延迟
KEYWORDS = ("OVER-ALLOTMENT", "OVER ALLOTMENT", "OVERALLOTMENT",
            "GREENSCHOE", "GREEN SHOE")

NUM = r"\d{1,3}(?:,\d{3})+|\d{4,}"
# 「exercised」与实际股数之间可能隔 100+ 字符（"fully exercised by the Overall
# Coordinators (for themselves and on behalf of the International Underwriters), on
# Saturday, February 7, 2026, in respect of an aggregate of 4,337,300 H Shares"），
# 所以按 over-allotment 锚点开窗，而不是按句子匹配。
# 标的可能是普通股（Shares）或预托证券/存托凭证（HDRs，如 DRS 上市），两者都要认。
UNIT = r"(?:Shares|HDRs)"
PATTERNS = [
    re.compile(rf"in\s+respect\s+of\s+(?:an\s+aggregate\s+of\s+)?({NUM})\s*(?:new\s+)?(?:H\s+|Offer\s+)?{UNIT}", re.I),
    re.compile(rf"over-?allocations?\s+of\s+(?:an\s+aggregate\s+of\s+)?({NUM})\s*(?:H\s+)?{UNIT}", re.I),
    re.compile(rf"allot(?:ted)?\s+and\s+issued\s+(?:by\s+the\s+Company\s+)?(?:an\s+aggregate\s+of\s+)?({NUM})\s*(?:new\s+)?(?:H\s+)?{UNIT}", re.I),
    re.compile(rf"subscri\w+\s+for\s+(?:an\s+aggregate\s+of\s+)?({NUM})\s*(?:new\s+)?(?:H\s+|Offer\s+)?{UNIT}", re.I),
    re.compile(rf"({NUM})\s*(?:new\s+)?(?:H\s+)?{UNIT}\s+(?:will\s+be|have\s+been|were)\s+(?:allotted|issued)", re.I),
]
ANCHOR = re.compile(r"over-?allotment", re.I)
PCT = re.compile(r"representing\s+(?:approximately\s+)?([\d.]+)\s*%\s+of\s+the\s+"
                 r"(?:total\s+number\s+of\s+the\s+)?(?:Offer\s+|H\s+)?Shares\s+"
                 r"(?:initially\s+available|available)", re.I)
WINDOW = 400


def safe(code: str) -> str:
    return "HKIPO-MB" + "".join(ch for ch in str(code) if ch.isdigit())


def parse_date(s) -> dt.date | None:
    s = (s or "").strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def classify(title: str) -> str:
    t = (title or "").upper()
    if "LAPSE" in t or "NOT BE EXERCISED" in t or "NON-EXERCISE" in t:
        return "lapse"
    if "EXERCISE" in t:
        return "exercise"
    return "other"


# ------------------------------------------------------------------ 1) 检索
def fetch_index(cfg: dict, found: list[dict], only=None, log=print) -> dict:
    g_dir = cfg["paths"]["allot_out"]
    out_path = g_dir / "greenshoe.json"
    result = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
    today = dt.date.today()
    sess = requests.Session()
    for rec in found:
        code = rec["code"]
        if only and code not in set(only):
            continue
        ld = parse_date(rec.get("listing_date"))
        sid = rec.get("stock_id")
        if not ld or not sid:
            result[code] = {"status": "error", "note": "缺上市日期或 stock_id"}
            log(f"  ERROR {code} 缺上市日期/stock_id")
            continue
        frm, to = ld, ld + dt.timedelta(days=WINDOW_DAYS)
        try:
            rows = _search_by_id(sess, cfg["hkex"], int(sid),
                                 frm.strftime("%Y%m%d"), to.strftime("%Y%m%d"))
        except Exception as exc:  # noqa: BLE001
            result[code] = {"status": "error", "note": f"{type(exc).__name__}: {exc}"}
            log(f"  ERROR {code} 检索失败 {type(exc).__name__}")
            continue
        matches = [{"kind": classify(r.get("TITLE")),
                    "title": r.get("TITLE"),
                    "datetime": r.get("DATE_TIME") or r.get("DateTime"),
                    "file": r.get("FILE_LINK")}
                   for r in rows
                   if any(k in (r.get("TITLE") or "").upper() for k in KEYWORDS)]
        exercised = any(m["kind"] == "exercise" for m in matches)
        result[code] = {"status": "ok", "exercised": exercised,
                        "window": [str(frm), str(to)], "window_closed": today > to,
                        "listing_date": str(ld), "announcements_scanned": len(rows),
                        "matches": matches}
        log(f"  {code:9s} 扫描 {len(rows):3d} 条 -> "
            f"{'行使' if exercised else ('未行使' if today > to else '窗口未过')}"
            f"（命中 {len(matches)} 条）")
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    n_ex = sum(1 for v in result.values() if v.get("exercised"))
    log(f"绿鞋检索：{len(result)} 家，行使 {n_ex} 家 -> {out_path}")
    return result


# ------------------------------------------------------------------ 2) 取股数
def _download(cfg: dict, rec: dict) -> dict:
    d = cfg["_root"] / "data" / "allot" / "greenshoe" / "pdf"
    d.mkdir(parents=True, exist_ok=True)
    dest = d / f"{safe(rec['code'])}.pdf"
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


def _pages(cfg: dict, code: str) -> list[dict]:
    import fitz
    dest = cfg["_root"] / "data" / "allot" / "greenshoe" / "text" / f"{safe(code)}.jsonl"
    if dest.exists() and dest.stat().st_size > 0:
        return [json.loads(x) for x in dest.open(encoding="utf-8")]
    doc = fitz.open(cfg["_root"] / "data" / "allot" / "greenshoe" / "pdf" / f"{safe(code)}.pdf")
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open("w", encoding="utf-8") as fh:
        for i, page in enumerate(doc, 1):
            fh.write(json.dumps({"page": i, "text": page.get_text()}, ensure_ascii=False) + "\n")
    doc.close()
    return [json.loads(x) for x in dest.open(encoding="utf-8")]


def extract_shares(cfg: dict, code: str) -> dict:
    """取众数（同一数字在正文/中文段/股权表重复出现）；返回原文供证据引用。"""
    tally: dict[int, list[dict]] = {}
    pcts = []
    for p in _pages(cfg, code):
        flat = re.sub(r"\s+", " ", p["text"])
        for a in ANCHOR.finditer(flat):
            lo, hi = max(0, a.start() - WINDOW), min(len(flat), a.end() + WINDOW)
            win = flat[lo:hi]
            for pat in PATTERNS:
                for m in pat.finditer(win):
                    # 契约要求 quote <= 200 字符，且必须仍是原文未改动的片段。
                    q = win[max(0, m.start() - 150):m.end() + 30].strip()
                    tally.setdefault(int(m.group(1).replace(",", "")), []).append(
                        {"page": p["page"], "quote": q[:200]})
        for m in PCT.finditer(flat):
            pcts.append({"page": p["page"], "pct": float(m.group(1))})
    best, best_n = None, 0
    for sh, items in tally.items():
        if len(items) > best_n:
            best, best_n = sh, len(items)
    q = tally[best][0] if best is not None else None
    return {"status": "ok" if best is not None else "no_match", "shares": best,
            "hits": {str(k): len(v) for k, v in sorted(tally.items())},
            "page": q["page"] if q else None, "quote": q["quote"] if q else "",
            "pct_of_option": pcts[0] if pcts else None}


def fetch_shares(cfg: dict, index: dict, only=None, log=print) -> dict:
    out_path = cfg["paths"]["allot_out"] / "greenshoe_shares.json"
    out = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
    codes = [c for c, v in sorted(index.items()) if v.get("exercised")]
    if only:
        codes = [c for c in codes if c in set(only)]
    recs = []
    for c in codes:
        m = next((x for x in index[c]["matches"] if x["kind"] == "exercise"), None)
        recs.append({"code": c, "file": m["file"], "doc_title": m["title"], "datetime": m["datetime"]})
    with ThreadPoolExecutor(max_workers=5) as ex:
        futs = {ex.submit(_download, cfg, r): r for r in recs}
        for fut in as_completed(futs):
            r = fut.result()
            if not r["pdf"]:
                out[r["code"]] = {"status": "error", "note": r["download"]}
                continue
            res = extract_shares(cfg, r["code"])
            res.update({"doc_title": r["doc_title"], "datetime": r["datetime"],
                        "file": r["file"], "pdf": r["pdf"]})
            out[r["code"]] = res
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    log(f"行使股数：{sum(1 for v in out.values() if v.get('status') == 'ok')}/{len(out)} -> {out_path}")
    return out


# ------------------------------------------------------------------ 3) 回填 CV
def apply_cv(cfg: dict, only=None, log=print) -> int:
    """把 col_CV 写成确定性结果（覆盖 agent 的推断），并给出可核验的证据。"""
    out_dir = cfg["paths"]["allot_out"]
    gi = json.loads((out_dir / "greenshoe.json").read_text(encoding="utf-8"))
    gs_path = out_dir / "greenshoe_shares.json"
    gs = json.loads(gs_path.read_text(encoding="utf-8")) if gs_path.exists() else {}
    ext = out_dir / "extracted"
    n = 0
    for code, fp in official_files(ext, only=only).items():
        g = gi.get(code) or gi.get(fp.stem.replace("HKIPO-MB", ""))
        if not g or g.get("status") != "ok":
            continue
        rec = json.loads(fp.read_text(encoding="utf-8"))
        fields = rec.setdefault("fields", {})
        lapse = next((m for m in g["matches"] if m["kind"] == "lapse"), None)
        if g["exercised"]:
            s = gs.get(code)
            if not s or s.get("status") != "ok":
                continue
            fields["col_CV"] = {
                "value": s["shares"], "page": s["page"], "quote": s["quote"],
                "source": "greenshoe", "confidence": "high",
                "note": f"{s['doc_title']} ({s['datetime']})",
            }
        elif lapse:
            fields["col_CV"] = {
                "value": 0, "page": None,
                "quote": f"港交所公告：{lapse['title']}（{lapse['datetime']}）",
                "source": "greenshoe_lapse", "confidence": "high",
                "note": lapse["title"],
            }
        elif g.get("window_closed"):
            fields["col_CV"] = {
                "value": 0, "page": None,
                "quote": (f"港交所公告检索：{g['listing_date']} 起 {WINDOW_DAYS} 天内共 "
                          f"{g['announcements_scanned']} 条公告，无任何 OVER-ALLOTMENT 行使公告，"
                          f"绿鞋窗口已于 {g['window'][1]} 期满未行使"),
                "source": "greenshoe_search", "confidence": "high",
            }
        else:
            fields["col_CV"] = {"value": "NaN", "page": None,
                                "quote": "绿鞋窗口尚未结束，无法确定", "source": "greenshoe",
                                "confidence": "high"}
        atomic_json(fp, rec)
        n += 1
    log(f"col_CV 回填：{n} 家")
    return n
