#!/usr/bin/env python3
"""【在线爬虫】从香港金管局（HKMA）开放 API 实时抓取「银行体系流动性每日数据」。

数据源（官方开放 API，JSON）：
  https://api.hkma.gov.hk/public/market-data-and-statistics/daily-monetary-statistics/daily-figures-interbank-liquidity
  文档：https://apidocs.hkma.gov.hk/documentation/market-data-and-statistics/daily-monetary-statistics/daily-figures-interbank-liquidity/

本脚本拉取两个核心宏观字段：
  hibor_fixing_1m  -> 1 个月 HIBOR 定盘价（百分数，如 2.88387）
  closing_balance  -> 银行体系总结余（百万港元，如 54023）

输出 CSV 格式（供 tools/external/hkma_import.py 离线导入）：
  date,hibor_1m_pct,aggregate_balance_hkd_mn

注意：若所在网络对 api.hkma.gov.hk 超时或拦截，可直接使用本地已校验的
data/manual/hibor_balance.csv 并通过 hkma_import.py 极速离线入表。
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
DEFAULT_OUT = ROOT / "data" / "manual" / "hibor_balance.csv"
BASE = ("https://api.hkma.gov.hk/public/market-data-and-statistics/"
        "daily-monetary-statistics/daily-figures-interbank-liquidity")
FIELDS = "end_of_date,hibor_fixing_1m,closing_balance"
UA = {"User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                     "(KHTML, like Gecko) Chrome/120 Safari/537.36"),
      "Accept": "application/json, text/plain, */*"}


def fetch_page(base: str, frm: str, to: str, offset: int, pagesize: int,
               retries: int, log=print) -> dict:
    params = {"from": frm, "to": to, "offset": offset,
              "pagesize": pagesize, "fields": FIELDS}
    last = None
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(base, params=params, headers=UA, timeout=90)
            if r.status_code != 200:
                last = f"HTTP {r.status_code}"
                log(f"    第 {attempt}/{retries} 次：{last}，{2 ** attempt}s 后重试")
                time.sleep(2 ** attempt)
                continue
            return r.json()
        except Exception as exc:                      # noqa: BLE001
            last = f"{type(exc).__name__}: {exc}"
            log(f"    第 {attempt}/{retries} 次：{last}，{2 ** attempt}s 后重试")
            time.sleep(2 ** attempt)
    raise SystemExit(
        f"\n取数失败（{last}）。\n"
        f"  如果是 HTTP 502 / 连接被重置，多为网络/代理拦截 api.hkma.gov.hk；\n"
        f"  请在能访问 HKMA 的机器上运行本脚本，把生成的 CSV 拷到：\n"
        f"      {DEFAULT_OUT}\n"
        f"  再执行：python3 prospectus_pipeline/tools_import_market_csv.py")


def collect(base: str, frm: str, to: str, pagesize: int, retries: int, log=print) -> list[dict]:
    rows, offset = [], 0
    while True:
        log(f"  请求 offset={offset} pagesize={pagesize} …")
        payload = fetch_page(base, frm, to, offset, pagesize, retries, log)
        header = payload.get("header", {})
        if not header.get("success", False):
            raise SystemExit(f"API 返回失败：{header}")
        result = payload.get("result", {})
        recs = result.get("records", []) or []
        if not recs:
            log("    本页 0 条，已到数据末尾")
            break
        rows.extend(recs)
        oldest = min(str(r.get("end_of_date")) for r in recs if r.get("end_of_date"))
        log(f"    本页 {len(recs)} 条（累计 {len(rows)}），最早 {oldest}")
        # 注：该 API 忽略 from/to，按"最新在前"返回，因此用 offset 往回翻，
        #     直到最早一条已经早于请求起点，或已取不出更多数据。
        if len(recs) < pagesize or oldest <= frm:
            break
        offset += len(recs)
        time.sleep(1.2)
    return rows


def normalise(rows: list[dict], frm: str | None = None,
              to: str | None = None) -> list[tuple[str, float, float]]:
    out = {}
    for r in rows:
        d = str(r.get("end_of_date") or "").strip()
        h = r.get("hibor_fixing_1m")
        b = r.get("closing_balance")
        if not d or h in (None, "") or b in (None, ""):
            continue
        if frm and d < frm:
            continue
        if to and d > to:
            continue
        out[d] = (d, float(str(h).replace(",", "")), float(str(b).replace(",", "")))
    return [out[k] for k in sorted(out)]


def main() -> int:
    ap = argparse.ArgumentParser(description="从 HKMA API 拉取 HIBOR / 银行体系总结余")
    ap.add_argument("--from", dest="frm", default="2025-11-01")
    ap.add_argument("--to", dest="to", default="2026-04-30")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--pagesize", type=int, default=1000,
                    help="每页条数（该 API 忽略 from/to，用大页 + offset 回溯）")
    ap.add_argument("--retries", type=int, default=4)
    ap.add_argument("--base", default=BASE, help="API 地址（默认 HKMA 官方）")
    args = ap.parse_args()

    print(f"HKMA 每日银行体系流动性：{args.frm} ~ {args.to}")
    rows = collect(args.base, args.frm, args.to, args.pagesize, args.retries)
    data = normalise(rows, args.frm, args.to)
    if not data:
        raise SystemExit("API 没有返回可用记录（检查日期区间是否有数据）。")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["date", "hibor_1m_pct", "aggregate_balance_hkd_mn"])
        w.writerows(data)

    print(f"\n已写出 {len(data)} 条 -> {out}")
    print(f"  区间 {data[0][0]} ~ {data[-1][0]}")
    print(f"  样例 HIBOR 1M = {data[0][1]}%（{data[0][0]}）  总结余 = {data[0][2]} 百万港元")
    print("\n下一步：python3 prospectus_pipeline/tools_import_market_csv.py --dry-run")
    return 0


if __name__ == "__main__":
    sys.exit(main())
