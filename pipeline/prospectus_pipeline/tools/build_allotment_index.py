#!/usr/bin/env python3
"""构建配发结果公告索引（out/allotment_index.json）。

背景：`run.py allot` 与 `allotprep.download_all` 都需要读取
`out/allotment_index.json`，但仓库中没有任何代码生成该文件。本工具补上这一环。

逐家检索 HKEXnews，定位「ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS」
（配发结果公告通常在上市日前 1–3 日刊发），输出 allotprep 需要的记录结构：

    [{"code": "6656.HK", "file": "/listedco/listconews/sehk/2026/0415/xxx.pdf",
      "datetime": "15/04/2026 22:31", "title": "..."}]

其中 `file` 是相对 `hkex.base_url` 的路径，`datetime` 用于 validate 的
`announce_date`。

用法：
    python prospectus_pipeline/tools/build_allotment_index.py
    python prospectus_pipeline/tools/build_allotment_index.py --only 6656.HK 2476.HK
    python prospectus_pipeline/tools/build_allotment_index.py --before-days 4 --after-days 2
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from hkex import _search_by_id, lookup_stock_id  # noqa: E402
from run import load_cfg, read_companies  # noqa: E402
from storage import atomic_json, create_http_session  # noqa: E402

# 配发结果公告的标题/摘要关键词（大小写不敏感）
KEYWORDS = ("allotment results", "allotment result")


def _text(rec: dict) -> str:
    return " ".join(str(rec.get(k) or "") for k in ("TITLE", "LONG_TEXT", "SHORT_TEXT")).lower()


def _is_allotment(rec: dict) -> bool:
    """是否为配发结果公告 PDF。"""
    link = str(rec.get("FILE_LINK") or "")
    if not link.lower().endswith(".pdf"):
        return False
    text = _text(rec)
    return any(k in text for k in KEYWORDS)


def _pick(rows: list[dict]) -> dict | None:
    """从窗口内的全部文档中挑出配发结果公告；优先摘要直接命中者，同分取最新。"""
    hits = [r for r in rows if _is_allotment(r)]
    if not hits:
        return None
    hits.sort(
        key=lambda r: (
            "allotment results" in str(r.get("SHORT_TEXT") or "").lower(),
            str(r.get("DATE_TIME") or ""),
        ),
        reverse=True,
    )
    return hits[0]


def build(cfg: dict, companies: list[dict], before_days: int, after_days: int, log=print) -> list[dict]:
    # hkex 的检索函数接收扁平的 hkex 子配置（与 run.cmd_find 的调用方式一致）
    hkex_cfg = cfg["hkex"]
    session = create_http_session()
    out: list[dict] = []
    for i, co in enumerate(companies, 1):
        code = co["code"]
        anchor = co.get("listing_date") or co.get("prospectus_date")
        if anchor is None:
            log(f"[{i}/{len(companies)}] !! {code:9s} 缺少上市/招股书日期，跳过")
            continue
        try:
            sid, _short = lookup_stock_id(session, hkex_cfg, code)
        except Exception as exc:  # noqa: BLE001
            log(f"[{i}/{len(companies)}] !! {code:9s} prefix.do 失败: {type(exc).__name__}")
            continue
        if sid is None:
            log(f"[{i}/{len(companies)}] !! {code:9s} 未解析出 stockId")
            continue
        frm = (anchor - dt.timedelta(days=before_days)).strftime("%Y%m%d")
        to = (anchor + dt.timedelta(days=after_days)).strftime("%Y%m%d")
        try:
            rows = _search_by_id(session, hkex_cfg, sid, frm, to)
        except Exception as exc:  # noqa: BLE001
            log(f"[{i}/{len(companies)}] !! {code:9s} titleSearchServlet 失败: {type(exc).__name__}")
            continue
        hit = _pick(rows)
        if hit is None:
            log(f"[{i}/{len(companies)}] !! {code:9s} 窗口 {frm}-{to} 共 {len(rows)} 条，无配发结果公告")
            continue
        out.append({
            "code": code,
            "file": hit["FILE_LINK"],
            "datetime": hit.get("DATE_TIME"),
            "title": hit.get("TITLE"),
            "url": hkex_cfg["base_url"] + hit["FILE_LINK"],
        })
        log(f"[{i}/{len(companies)}] OK {code:9s} {str(hit.get('DATE_TIME')):16s} -> {str(hit.get('TITLE'))[:48]}")
        time.sleep(float(hkex_cfg.get("sleep_sec", 0.4)))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="构建配发结果公告索引")
    ap.add_argument("--only", nargs="*", default=None, help="只处理这些股票代码")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--before-days", type=int, default=4, help="上市日前检索天数")
    ap.add_argument("--after-days", type=int, default=2, help="上市日后检索天数")
    args = ap.parse_args()

    cfg = load_cfg()
    companies = read_companies(cfg)
    if args.only:
        companies = [c for c in companies if c["code"] in args.only]
    if args.limit:
        companies = companies[: args.limit]

    print(f"配发结果公告索引：目标 {len(companies)} 家")
    index = build(cfg, companies, args.before_days, args.after_days)
    dest = cfg["paths"]["out"] / "allotment_index.json"

    if args.only or args.limit:
        # 局部重建：与既有索引合并，避免 --only/--limit 把未处理的条目一并丢掉
        existing = []
        if dest.exists():
            try:
                existing = json.loads(dest.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                existing = []
        by_code = {r.get("code"): r for r in existing if isinstance(r, dict)}
        for r in index:
            by_code[r["code"]] = r
        index = sorted(by_code.values(), key=lambda r: str(r.get("code") or ""))
        print(f"（局部重建：与既有 {len(existing)} 条合并后共 {len(index)} 条）")

    atomic_json(dest, index)
    print(f"\n索引生成完成：本次解析 {len(companies)} 家，索引共 {len(index)} 条 -> {dest}")
    return 0 if len(index) >= len(companies) else 1


if __name__ == "__main__":
    raise SystemExit(main())
