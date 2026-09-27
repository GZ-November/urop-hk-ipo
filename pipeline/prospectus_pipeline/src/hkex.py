"""HKEXnews 招股书定位器（两段式，服务端按股票过滤）。

港交所 titleSearchServlet 的 stockId 是内部 ID，直接传股票代码会返回空。
可靠做法分两步：
  1) prefix.do 自动补全接口：股票代码 -> stockId（同时校验 5 位代码精确匹配）
  2) titleSearchServlet.do 带 stockId + 日期窗 -> 该公司全部文档，本地挑招股书
招股书在列表里的大类是 "Listing Documents"，子类为 [Offer for Subscription]
或 [Offer for Placing]，标题通常是 "GLOBAL OFFERING" / "Global Offering"。
"""
from __future__ import annotations

import datetime as dt
import json
import time
from dataclasses import dataclass
from typing import Iterable

import requests
from storage import create_http_session

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")
PREFIX_URL = "https://www1.hkexnews.hk/search/prefix.do"


@dataclass
class Found:
    code: str
    name: str
    prospectus_date: str | None
    listing_date: str | None
    stock_id: int | None
    pdf_url: str | None
    doc_title: str | None
    doc_type: str | None
    doc_datetime: str | None
    candidates: int
    status: str          # ok | not_found | error
    note: str = ""


def _digits(code: str) -> str:
    return "".join(ch for ch in str(code) if ch.isdigit())


def lookup_stock_id(session: requests.Session, cfg: dict, code: str) -> tuple[int | None, str | None]:
    """股票代码 -> (内部 stockId, 港交所简称)。"""
    d = _digits(code)
    if not d:
        return None, None
    r = session.get(PREFIX_URL, params={"callback": "cb", "lang": "EN", "type": "A",
                                        "name": d, "market": "SEHK"},
                    timeout=cfg.get("timeout_sec", 40), headers={"User-Agent": UA})
    r.raise_for_status()
    txt = r.text
    if "(" not in txt:
        return None, None
    try:
        js = json.loads(txt[txt.find("(") + 1: txt.rfind(")")])
    except json.JSONDecodeError:
        return None, None
    want = f"{int(d):05d}"
    for s in js.get("stockInfo", []):
        if str(s.get("code")) == want:
            return int(s["stockId"]), s.get("name")
    return None, None


def _search_by_id(session: requests.Session, cfg: dict, stock_id: int,
                  frm: str, to: str) -> list[dict]:
    p = {
        "sortDir": "0", "sortByOptions": "DateTime", "category": "0", "market": "SEHK",
        "stockId": str(stock_id), "documentType": "-1", "fromDate": frm, "toDate": to,
        "title": "", "searchType": "1", "t1code": "-2", "t2Gcode": "-2", "t2code": "-2",
        "rowRange": str(cfg.get("row_range", 1000)), "lang": "EN",
    }
    r = session.get(cfg["search_url"], params=p, timeout=cfg.get("timeout_sec", 40),
                    headers={"User-Agent": UA})
    r.raise_for_status()
    try:
        return json.loads(r.json().get("result") or "[]")
    except json.JSONDecodeError:
        return []


def _score(rec: dict, cfg: dict) -> int:
    """给候选文档打分，招股书优先；非招股书返回 -1。"""
    long_text = rec.get("LONG_TEXT", "") or ""
    text = f"{long_text} {rec.get('TITLE','')} {rec.get('SHORT_TEXT','')}"
    if cfg["listing_doc_prefix"] not in long_text:
        return -1
    for bad in cfg["exclude_substrings"]:
        if bad.lower() in text.lower():
            return -1
    score = 0
    for good in cfg["include_substrings"]:
        if good.lower() in text.lower():
            score += 10
    title = (rec.get("TITLE") or "").upper()
    if "GLOBAL OFFERING" in title:
        score += 20
    if "PROSPECTUS" in title:
        score += 20
    if (rec.get("FILE_LINK") or "").lower().endswith(".pdf"):
        score += 1
    return score


def find_one(session: requests.Session, cfg: dict, code: str, name: str,
             prospectus_date: dt.date | None, listing_date: dt.date | None) -> Found:
    base = Found(code, name, str(prospectus_date), str(listing_date),
                 None, None, None, None, None, 0, "error", "")
    anchor = prospectus_date or listing_date
    if anchor is None:
        base.note = "缺少招股书/上市日期"
        return base

    try:
        sid, _short = lookup_stock_id(session, cfg, code)
    except Exception as exc:  # noqa: BLE001
        base.note = f"prefix.do 失败: {type(exc).__name__}: {exc}"
        return base
    if sid is None:
        base.note = "prefix.do 未找到该股票代码"
        return base
    base.stock_id = sid

    win = int(cfg.get("day_window", 10))
    frm = (anchor - dt.timedelta(days=win)).strftime("%Y%m%d")
    to = ((listing_date or anchor) + dt.timedelta(days=win)).strftime("%Y%m%d")
    try:
        rows = _search_by_id(session, cfg, sid, frm, to)
    except Exception as exc:  # noqa: BLE001
        base.note = f"titleSearchServlet 失败: {type(exc).__name__}: {exc}"
        return base

    base.candidates = len(rows)
    scored = sorted(((_score(r, cfg), r) for r in rows), key=lambda x: -x[0])
    best = [r for s, r in scored if s > 0]
    if not best:
        base.status = "not_found"
        base.note = f"stockId={sid} 窗口 {frm}-{to} 共 {len(rows)} 条，无招股书类文档"
        return base

    top = best[0]
    base.status = "ok"
    base.pdf_url = cfg["base_url"] + top["FILE_LINK"]
    base.doc_title = top.get("TITLE")
    base.doc_type = top.get("LONG_TEXT")
    base.doc_datetime = top.get("DATE_TIME")
    base.note = f"候选 {len(best)} 条"
    return base


def find_all(cfg: dict, companies: Iterable[dict], log=print) -> list[Found]:
    """companies: [{code, name, prospectus_date, listing_date}, ...]"""
    companies = list(companies)
    session = create_http_session()
    out: list[Found] = []
    for i, co in enumerate(companies, 1):
        f = find_one(session, cfg, co["code"], co["name"],
                     co.get("prospectus_date"), co.get("listing_date"))
        out.append(f)
        flag = "OK " if f.status == "ok" else "!! "
        log(f"[{i}/{len(companies)}] {flag}{f.code} {f.name[:30]:30s} -> "
            f"{str(f.doc_type or f.note)[:52]}")
        time.sleep(float(cfg.get("sleep_sec", 0.4)))
    return out
