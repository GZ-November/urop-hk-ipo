#!/usr/bin/env python3
"""核实每家公司上市后有没有「行使超额配售权」（绿鞋）公告。

为什么必须单独查：配发结果公告只写「假設超額配售權未行使」的口径，或写一句
"In the event the Over-allotment Option is exercised, an announcement will be made"，
这**不能**用来推断 col_CV=0。唯一确定性证据是上市后 30 天内（法规窗口）港交所
有没有发出行使公告：
  - 有行使公告  -> col_CV = 公告里的实际配发股数
  - 无行使公告且窗口已过 -> col_CV = 0（确定的零，写 0 不写 NaN）

输出 out/allot/greenshoe.json：
  {code: {exercised: bool, window: [from, to], window_closed: bool,
          matches: [{title, datetime, file}], status: ok|error}}

用法：
  python3 tools_greenshoe.py                 # 全部 38 家
  python3 tools_greenshoe.py --only 2649.HK  # 指定
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

import yaml  # noqa: E402
import requests  # noqa: E402
from hkex import UA, lookup_stock_id, _search_by_id  # noqa: E402

WINDOW_DAYS = 45          # 绿鞋窗口为上市后 30 天；多给 15 天覆盖公告与周末
KEYWORDS = ("OVER-ALLOTMENT", "OVER ALLOTMENT", "OVERALLOTMENT",
            "GREENSCHOE", "GREEN SHOE")
# 排除「不行使/失效」类标题里同样含 OVER-ALLOTMENT 但并非行使的文档：
# 实际港交所标题形如 "FULL EXERCISE OF THE OVER-ALLOTMENT OPTION" /
# "PARTIAL EXERCISE OF THE OVER-ALLOTMENT OPTION" / "LAPSE OF THE OVER-ALLOTMENT OPTION"。


def parse_date(s: str) -> dt.date | None:
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    cfg = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    cfg["_root"] = ROOT
    out_dir = (ROOT.parent / cfg["paths"]["allot_out"]).resolve()
    out_path = Path(args.out).resolve() if args.out else out_dir / "greenshoe.json"

    found = json.loads((ROOT / "out" / "found.json").read_text(encoding="utf-8"))
    want = set(args.only) if args.only else None
    today = dt.date.today()

    sess = requests.Session()
    result: dict[str, dict] = {}
    if out_path.exists() and not args.only:
        result = json.loads(out_path.read_text(encoding="utf-8"))

    for rec in found:
        code = rec["code"]
        if want and code not in want:
            continue
        ld = parse_date(rec.get("listing_date"))
        sid = rec.get("stock_id")
        if not ld or not sid:
            result[code] = {"status": "error", "note": "缺上市日期或 stock_id"}
            print(f"ERROR  {code} 缺上市日期/stock_id")
            continue
        frm, to = ld, ld + dt.timedelta(days=WINDOW_DAYS)
        try:
            rows = _search_by_id(sess, cfg["hkex"], int(sid),
                                 frm.strftime("%Y%m%d"), to.strftime("%Y%m%d"))
        except Exception as exc:                       # noqa: BLE001
            result[code] = {"status": "error", "note": f"{type(exc).__name__}: {exc}"}
            print(f"ERROR  {code} 检索失败 {type(exc).__name__}: {exc}")
            time.sleep(cfg["hkex"].get("sleep_sec", 0.4))
            continue
        matches = []
        for r in rows:
            title = (r.get("TITLE") or "").upper()
            if any(k in title for k in KEYWORDS):
                matches.append({"kind": classify(r.get("TITLE") or ""),
                                "title": r.get("TITLE"),
                                "datetime": r.get("DATE_TIME") or r.get("DateTime"),
                                "file": r.get("FILE_LINK"),
                                "short": (r.get("SHORT_TEXT") or "").strip()[:120]})
        exercised = any(m["kind"] == "exercise" for m in matches)
        result[code] = {
            "status": "ok",
            "exercised": exercised,
            "window": [str(frm), str(to)],
            "window_closed": today > to,
            "listing_date": str(ld),
            "announcements_scanned": len(rows),
            "matches": matches,
        }
        flag = "EXERCISED" if exercised else ("not-exercised" if today > to else "WINDOW-OPEN")
        print(f"OK     {code}  扫描 {len(rows):3d} 条公告，命中 {len(matches)} 条 -> {flag}")
        for m in matches:
            print(f"         [{m['kind']}] {m['datetime']}  {m['title']}")
        time.sleep(cfg["hkex"].get("sleep_sec", 0.4))

    if args.only and out_path.exists():
        old = json.loads(out_path.read_text(encoding="utf-8"))
        old.update(result)
        result = old
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    n_ex = sum(1 for v in result.values() if v.get("exercised"))
    n_err = sum(1 for v in result.values() if v.get("status") != "ok")
    print(f"\n绿鞋核实完成：{len(result)} 家，行使 {n_ex} 家，失败 {n_err} 家 -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
