#!/usr/bin/env python3
"""腾讯港股日线 → DD（恒指 20 日回报）+ DH–DM（上市首日 OHLC/量/额）。

接口：https://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get
  param=hk06082,day,<from>,<to>,<n>,qfq
  恒指代码 hkHSI。

K 线字段顺序（实测）：date, open, close, high, low, volume, {}, ?, turnover_万元, ...
口径：
  DD  t = 招股书日前最后一个恒指交易日，P(t)/P(t−20)−1，用收盘。
  DH–DK 上市日（或其后第一个有 bar 的交易日）的 收/开/高/低。
  DL 成交量（股）；DM 成交额（HK$）= 接口第 9 列 × 10,000。

只赋值，不改样式。缓存落到 data/market/。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import sys
import time
import urllib.request
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2] if Path(__file__).resolve().parent.name == "external" else Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))
from market_fetcher import get_market_fetcher
from run import load_cfg

WS = ROOT.parent
_cfg = load_cfg()
_configured_book = Path(_cfg["workbook"])
BOOK = _configured_book if _configured_book.is_absolute() else WS / _configured_book
CACHE = ROOT / "data" / "market"
SHEET = _cfg.get("sheet", "NLR")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

HEADERS = {
    "DD": "HSI return over 20 trading days before prospectus (%)",
    "DH": "First trading day closing price (HK$)",
    "DI": "First trading day opening price (HK$)",
    "DJ": "First trading day high (HK$)",
    "DK": "First trading day low (HK$)",
    "DL": "First trading day volume (shares)",
    "DM": "First trading day turnover (HK$)",
}


def norm(s) -> str:
    return " ".join(str(s or "").replace("\n", " ").split()).strip().lower()


def to_date(v) -> dt.date | None:
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    return None


def hk_symbol(code: str) -> str:
    d = "".join(ch for ch in str(code) if ch.isdigit())
    return f"hk{int(d):05d}"


def fetch(symbol: str, frm: str, to: str, n: int = 120, retries: int = 4) -> list[list]:
    """兼容旧接口的后备抓取函数。"""
    fetcher = get_market_fetcher()
    bars, _, _ = fetcher.fetch_bars_resilient(symbol, frm, to, n_bars=n)
    return bars


def parse_bar(item: Any) -> dict:
    if isinstance(item, dict):
        d = item["date"]
        if isinstance(d, str):
            d = dt.datetime.strptime(d[:10], "%Y-%m-%d").date()
        return {
            "date": d,
            "open": float(item["open"]),
            "close": float(item["close"]),
            "high": float(item["high"]),
            "low": float(item["low"]),
            "volume": float(item["volume"]),
            "turnover": float(item["turnover"]) if item.get("turnover") is not None else None,
            "turnover_estimated": bool(item.get("turnover_estimated", False)),
        }
    # date, open, close, high, low, volume, {}, ?, turnover_万元
    row = item
    turnover = None
    if len(row) > 8 and row[8] not in (None, "", "{}", {}):
        try:
            turnover = float(row[8]) * 10_000
        except (TypeError, ValueError):
            turnover = None
    return {
        "date": dt.datetime.strptime(str(row[0])[:10], "%Y-%m-%d").date(),
        "open": float(row[1]),
        "close": float(row[2]),
        "high": float(row[3]),
        "low": float(row[4]),
        "volume": float(row[5]),
        "turnover": turnover,
        "turnover_estimated": False,
    }


def last_before(bars: list[dict], d: dt.date) -> int | None:
    idx = None
    for i, b in enumerate(bars):
        if b["date"] < d:
            idx = i
        else:
            break
    return idx


def first_on_or_after(bars: list[dict], d: dt.date) -> dict | None:
    for b in bars:
        if b["date"] >= d:
            return b
    return None


def companies(ws) -> list[tuple[int, str, dt.date, dt.date]]:
    col_code, col_pd, col_ld = 2, 4, 5
    for c in range(1, ws.max_column + 1):
        v = norm(ws.cell(1, c).value)
        if "stock code" in v:
            col_code = c
        elif "date of prospectus" in v:
            col_pd = c
        elif "date of listing" in v:
            col_ld = c
    out = []
    for r in range(2, ws.max_row + 1):
        code = ws.cell(r, col_code).value
        if code in (None, ""):
            continue
        pd, ld = to_date(ws.cell(r, col_pd).value), to_date(ws.cell(r, col_ld).value)
        if not pd or not ld:
            continue
        out.append((r, str(code).strip(), pd, ld))
    return out



def resolve_cols(ws) -> dict[str, int]:
    col_of = {}
    for c in range(1, ws.max_column + 1):
        v = ws.cell(1, c).value
        if v in (None, ""):
            continue
        n = norm(v)
        for key, header in HEADERS.items():
            if n == norm(header):
                col_of[key] = c
    missing = [k for k in HEADERS if k not in col_of]
    if missing:
        raise SystemExit(f"工作簿缺列 {missing}")
    return col_of


def main() -> int:
    ap = argparse.ArgumentParser(description="抓取恒指与港股上市首日市场行情数据 (DD, DH-DM)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--book", default=str(BOOK))
    ap.add_argument("--only", nargs="*", default=None, help="只处理指定股票代码")
    ap.add_argument(
        "--provider",
        choices=["auto", "tencent", "yahoo"],
        default="auto",
        help="市场数据提供商偏好 (auto=腾讯优先并自动降级至雅虎财经, tencent, yahoo)",
    )
    args = ap.parse_args()
    book = Path(args.book)
    CACHE.mkdir(parents=True, exist_ok=True)
    fetcher = get_market_fetcher()

    wb = openpyxl.load_workbook(book)
    ws = wb[SHEET]
    col_of = resolve_cols(ws)
    rows = companies(ws)
    if args.only:
        targets = set()
        for x in args.only:
            s = str(x).strip().upper()
            targets.add(s)
            targets.add(s.replace(".HK", ""))
            d = "".join(ch for ch in s if ch.isdigit())
            if d:
                targets.add(f"{int(d):04d}.HK")
                targets.add(f"{int(d):05d}")
                targets.add(str(int(d)))
        rows = [r for r in rows if r[1].upper() in targets or r[1].upper().replace(".HK", "") in targets]
    print(f"工作簿 {len(rows)} 家 (数据源策略: {args.provider})")

    # 恒指：覆盖最早招股书日前 40 个交易日
    hsi_from = (min(p for _, _, p, _ in rows) - dt.timedelta(days=80)).isoformat()
    hsi_to = (max(p for _, _, p, _ in rows) + dt.timedelta(days=5)).isoformat()
    hsi_raw, hsi_prov, hsi_errs = fetcher.fetch_bars_resilient(
        "hkHSI", hsi_from, hsi_to, n_bars=200, preferred_provider=args.provider
    )
    (CACHE / "hsi.json").write_text(json.dumps(hsi_raw, ensure_ascii=False, default=str), encoding="utf-8")
    hsi = [parse_bar(x) for x in hsi_raw]
    print(f"HSI ({hsi_prov}) {len(hsi)} 条 {hsi[0]['date']} ~ {hsi[-1]['date']}")
    if hsi_errs:
        print(f"   [HSI 降级警报] 经历过以下重试/失败: {hsi_errs}")

    results = []
    for r, code, pd, ld in rows:
        rec = {
            "code": code,
            "row": r,
            "prospectus": str(pd),
            "listing": str(ld),
            "hsi_provider": hsi_prov,
        }
        i = last_before(hsi, pd)
        if i is None or i < 20:
            rec["DD"] = None
            rec["DD_note"] = f"恒指序列不够：i={i}"
        else:
            rec["DD"] = hsi[i]["close"] / hsi[i - 20]["close"] - 1
            rec["DD_t"] = str(hsi[i]["date"])
            rec["DD_t20"] = str(hsi[i - 20]["date"])
        sym = hk_symbol(code)
        frm = (ld - dt.timedelta(days=3)).isoformat()
        to = (ld + dt.timedelta(days=10)).isoformat()
        try:
            bars, prov_stock, errs_stock = fetcher.fetch_bars_resilient(
                code, frm, to, n_bars=20, preferred_provider=args.provider
            )
            (CACHE / f"{sym}.json").write_text(
                json.dumps(bars, ensure_ascii=False, default=str), encoding="utf-8"
            )
            rec["provider"] = prov_stock
            if errs_stock:
                rec["fallback_errors"] = errs_stock
            bar = first_on_or_after(bars, ld)
            if bar is None:
                rec["first"] = None
                rec["first_note"] = "无上市日及之后的 K 线"
            else:
                rec["first"] = bar
                if bar.get("turnover_estimated"):
                    rec["turnover_note"] = "Turnover estimated via Yahoo typical price proxy"
                if bar["date"] != ld:
                    rec["first_note"] = f"上市日 {ld} 无 K 线，改用 {bar['date']}"
        except Exception as exc:  # noqa: BLE001
            rec["first"] = None
            rec["first_note"] = str(exc)
        results.append(rec)
        time.sleep(0.15)

    (CACHE / "computed.json").write_text(json.dumps(results, ensure_ascii=False, indent=2, default=str) + "\n",
                                         encoding="utf-8")

    print(f"\n{'code':9s} {'招股书':12s} {'DD%':8s} {'上市日':12s} {'收':>8s} {'开':>8s} {'量':>14s}")
    n_ok = 0
    for rec in results:
        first = rec.get("first") or {}
        dd = rec.get("DD")
        print(f"{rec['code']:9s} {rec['prospectus']:12s} "
              f"{(f'{dd*100:7.3f}' if dd is not None else '   NaN ')} "
              f"{rec['listing']:12s} "
              f"{first.get('close', float('nan')):8.3f} {first.get('open', float('nan')):8.3f} "
              f"{first.get('volume', float('nan')):14,.0f}"
              f"{'  ' + rec.get('first_note','') if rec.get('first_note') else ''}"
              f"{'  ' + rec.get('DD_note','') if rec.get('DD_note') else ''}")
        if dd is not None and first:
            n_ok += 1
    print(f"\n完整 {n_ok}/{len(results)}")

    if args.dry_run:
        wb.close()
        print("--dry-run：未写回")
        return 0

    wb.close()
    sys.path.insert(0, str(ROOT / "src"))
    from workbook_transaction import workbook_transaction

    with workbook_transaction(book, operation="market") as wb:
        ws = wb[SHEET]
        col_of = resolve_cols(ws)
        for rec in results:
            r = rec["row"]
            dd = rec.get("DD")
            ws.cell(r, col_of["DD"]).value = round(dd, 8) if dd is not None else "NaN"
            first = rec.get("first")
            if not first:
                for k in ("DH", "DI", "DJ", "DK", "DL", "DM"):
                    ws.cell(r, col_of[k]).value = "NaN"
                continue
            ws.cell(r, col_of["DH"]).value = first["close"]
            ws.cell(r, col_of["DI"]).value = first["open"]
            ws.cell(r, col_of["DJ"]).value = first["high"]
            ws.cell(r, col_of["DK"]).value = first["low"]
            ws.cell(r, col_of["DL"]).value = int(round(first["volume"]))
            ws.cell(r, col_of["DM"]).value = (round(first["turnover"], 2)
                                              if first.get("turnover") is not None else "NaN")
    print(f"\n已写回 DD, DH–DM（{n_ok} 家完整） -> {book.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
