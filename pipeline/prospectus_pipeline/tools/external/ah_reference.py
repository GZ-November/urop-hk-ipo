#!/usr/bin/env python3
"""Collect A-share reference prices for A+H issuers (H-share offer discount to the A-share price).

For every A+H issuer in the master panel:
  1. find the A-share symbol through Tencent's search endpoint, requiring the same short name as the
     issuer's H-share listing (the endpoint groups A and H listings of one company), and record how it was found;
  2. download raw (unadjusted) A-share daily bars and the CNY/HKD exchange rate (Yahoo daily close);
  3. take the A-share close on the last A trading day on or before the subscription closing date (and, where the
     pricing date is known, on the last trading day before it), convert it to HKD, and compute the offer discount.

Nothing is estimated: an issuer without a unique matching A-share symbol, or without a bar on the anchor
date, is left missing and listed in the output with the reason.

Outputs:
  data/market/ah_reference/a_bars/<symbol>.json   raw A-share bars (date, open, close, high, low, volume)
  data/market/ah_reference/fx_cnyhkd.json         CNY/HKD daily closes
  data/market/ah_reference/csi300.json            CSI 300 daily bars (A-share market benchmark)
  data/market/ah_reference/a_share_map.csv        H code -> A symbol, names, method
  <repo>/pipeline/exports/HKIPO-2026-AH-reference.csv   anchor prices and offer discounts

Usage (from the repository root):
    python3 pipeline/prospectus_pipeline/tools/external/ah_reference.py [--refresh]
"""
from __future__ import annotations

import argparse
import codecs
import csv
import datetime as dt
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parents[1]
CACHE = ROOT / "data" / "market" / "ah_reference"
MASTER = REPO / "pipeline" / "exports" / "HKIPO-MB-MASTER_clean.csv"
OUTPUT = REPO / "pipeline" / "exports" / "HKIPO-2026-AH-reference.csv"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
A_SUFFIX = {"sh": "SH", "sz": "SZ", "bj": "BJ"}


def http_get(url: str, retries: int = 3, timeout: int = 15) -> str:
    last: Exception | None = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as response:
                return response.read().decode("utf-8", errors="replace")
        except Exception as exc:  # network errors are retried, then re-raised
            last = exc
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"GET failed for {url}: {last}")


# ---------------------------------------------------------------- symbol lookup

def parse_hint(text: str) -> list[dict]:
    """Parse Tencent smartbox `v_hint="mkt~code~name~pinyin~type^..."` into records."""
    match = re.search(r'v_hint="(.*)"', text)
    if not match or match.group(1) in {"", "N"}:
        return []
    raw = codecs.decode(match.group(1).encode("ascii", errors="ignore"), "unicode_escape")
    records = []
    for item in raw.split("^"):
        parts = item.split("~")
        if len(parts) >= 5:
            records.append({"market": parts[0], "code": parts[1], "name": parts[2], "kind": parts[4]})
    return records


def smartbox(query: str) -> list[dict]:
    return parse_hint(http_get("https://smartbox.gtimg.cn/s3/?v=2&t=all&q=" + urllib.parse.quote(query)))


# Issuers whose A-share short name differs from the H-share short name, so the name match cannot find them.
# Each entry was checked against the issuer's Chinese company name and, after download, against the A-share
# price (an offer within a plausible band of the converted A-share close; see `plausible` in the output).
MANUAL_OVERRIDES = {
    "2768.HK": ("sz002768", "H short name 国恩科技; A-share short name 国恩股份 (Qingdao Guoen Technology Co., Ltd.)"),
}


def normalize_name(name: str) -> str:
    """Drop listing-status suffixes (U, -U, B, -B, -W, W, -SW) and case so 迈威生物U matches 迈威生物b."""
    return re.sub(r"[-\s]*(u|b|w|sw)$", "", name.strip().lower())


def find_a_symbol(h_code: str, lookup=smartbox) -> dict:
    """Unique A-share (GP-A) record sharing the H-share's short name; otherwise a reasoned failure."""
    if h_code in MANUAL_OVERRIDES:
        symbol, note = MANUAL_OVERRIDES[h_code]
        return {"status": "manual_override: " + note, "name": "", "symbol": symbol}
    h5 = h_code.split(".")[0].zfill(5)
    h_records = [r for r in lookup(h5) if r["market"] == "hk" and r["code"] == h5 and r["kind"].startswith("GP")]
    if not h_records:
        return {"status": "no_h_record", "name": "", "symbol": ""}
    name = h_records[0]["name"]
    candidates = {}
    for query in dict.fromkeys([name, normalize_name(name)]):  # a status suffix on the H name can hide the A record
        for r in lookup(query):
            if r["market"] in A_SUFFIX and r["kind"].startswith("GP-A") and normalize_name(r["name"]) == normalize_name(name):
                candidates[(r["market"], r["code"])] = r
    matches = list(candidates.values())
    if len(matches) == 1:
        m = matches[0]
        return {"status": "matched_by_short_name" + (" (STAR)" if m["kind"] == "GP-A-KCB" else ""), "name": name, "symbol": f"{m['market']}{m['code']}"}
    return {"status": "ambiguous" if matches else "no_a_record", "name": name, "symbol": ""}


# ---------------------------------------------------------------- prices

def fetch_a_bars(symbol: str, start: dt.date, end: dt.date) -> list[dict]:
    """Raw (unadjusted) daily bars from Tencent."""
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={symbol},day,{start},{end},640,"
    payload = json.loads(http_get(url))
    rows = ((payload.get("data") or {}).get(symbol) or {}).get("day") or []
    return [{"date": r[0], "open": float(r[1]), "close": float(r[2]), "high": float(r[3]), "low": float(r[4]), "volume": float(r[5])} for r in rows]


def fetch_fx(start: dt.date, end: dt.date) -> list[dict]:
    """CNY/HKD daily closes from Yahoo (HKD per 1 CNY)."""
    p1 = int(dt.datetime.combine(start, dt.time()).replace(tzinfo=dt.timezone.utc).timestamp())
    p2 = int(dt.datetime.combine(end + dt.timedelta(days=1), dt.time()).replace(tzinfo=dt.timezone.utc).timestamp())
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/CNYHKD=X?period1={p1}&period2={p2}&interval=1d"
    result = json.loads(http_get(url))["chart"]["result"][0]
    closes = result["indicators"]["quote"][0]["close"]
    return [{"date": dt.datetime.fromtimestamp(t, dt.timezone.utc).date().isoformat(), "close": c}
            for t, c in zip(result["timestamp"], closes) if c is not None]


def last_on_or_before(bars: list[dict], day: dt.date, max_gap_days: int = 7) -> dict | None:
    """The last bar dated on or before `day`, only if it is within max_gap_days (a stale bar is not an anchor)."""
    best = None
    for bar in bars:
        d = dt.date.fromisoformat(bar["date"])
        if d <= day:
            best = bar
        else:
            break
    if best is None or (day - dt.date.fromisoformat(best["date"])).days > max_gap_days:
        return None
    return best


def anchor(bars: list[dict], fx: list[dict], day: dt.date | None, strictly_before: bool = False) -> dict | None:
    """A-share close and CNY/HKD rate for the last A trading day on/before `day` (or before it)."""
    if day is None:
        return None
    ref = day - dt.timedelta(days=1) if strictly_before else day
    a = last_on_or_before(bars, ref)
    if a is None:
        return None
    rate = last_on_or_before(fx, dt.date.fromisoformat(a["date"]))
    if rate is None:
        return None
    return {"a_date": a["date"], "a_close_cny": a["close"], "cnyhkd": rate["close"], "a_close_hkd": a["close"] * rate["close"]}


# ---------------------------------------------------------------- main

def to_date(value) -> dt.date | None:
    text = str(value or "")[:10]
    try:
        return dt.date.fromisoformat(text)
    except ValueError:
        return None


def read_a_plus_h() -> list[dict]:
    with MASTER.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    out = []
    for r in rows:
        ld = to_date(r.get("Date of Listing (dd/mm/yy)"))
        if not ld or ld.year != 2026 or str(r.get("A+H issuer flag")) not in {"1", "1.0"}:
            continue
        out.append({"code": r["Stock Code"], "name_cn": r.get("Company Chinese Name", ""), "listing": ld,
                    "sub_close": to_date(r.get("Subscription closing date")), "pricing": to_date(r.get("Pricing date")),
                    "offer": float(r["IPO Subscription Price (HK$)"]), "close1": float(r["First trading day closing price (HK$)"])})
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--refresh", action="store_true", help="ignore cached A-share bars and FX")
    args = parser.parse_args()
    issuers = read_a_plus_h()
    (CACHE / "a_bars").mkdir(parents=True, exist_ok=True)
    start = min(i["sub_close"] for i in issuers) - dt.timedelta(days=45)
    end = dt.date.today()
    fx_path = CACHE / "fx_cnyhkd.json"
    if args.refresh or not fx_path.exists():
        fx_path.write_text(json.dumps(fetch_fx(start, end), indent=1), encoding="utf-8")
    fx = json.loads(fx_path.read_text(encoding="utf-8"))
    csi_path = CACHE / "csi300.json"  # A-share market benchmark for the A-share reaction study
    if args.refresh or not csi_path.exists():
        csi_path.write_text(json.dumps(fetch_a_bars("sh000300", start, end), indent=1), encoding="utf-8")

    map_rows, out_rows = [], []
    for i in issuers:
        found = find_a_symbol(i["code"])
        map_rows.append({"h_code": i["code"], "a_symbol": found["symbol"], "short_name": found["name"], "status": found["status"], "company_cn": i["name_cn"]})
        row = {"h_code": i["code"], "a_symbol": found["symbol"], "status": found["status"], "listing_date": i["listing"], "subscription_close": i["sub_close"],
               "pricing_date": i["pricing"] or "", "offer_hkd": i["offer"], "h_day1_close_hkd": i["close1"]}
        if found["symbol"]:
            path = CACHE / "a_bars" / f"{found['symbol']}.json"
            if args.refresh or not path.exists():
                path.write_text(json.dumps(fetch_a_bars(found["symbol"], start, end), indent=1), encoding="utf-8")
                time.sleep(0.3)
            bars = json.loads(path.read_text(encoding="utf-8"))
            for label, day, strict in (("close", i["sub_close"], False), ("pricing", i["pricing"], True)):
                a = anchor(bars, fx, day, strictly_before=strict)
                if a:
                    row.update({f"a_date_{label}": a["a_date"], f"a_close_cny_{label}": a["a_close_cny"], f"cnyhkd_{label}": round(a["cnyhkd"], 5),
                                f"a_close_hkd_{label}": round(a["a_close_hkd"], 4), f"offer_vs_a_{label}": round(i["offer"] / a["a_close_hkd"] - 1, 6)})
            offer_vs = row.get("offer_vs_a_close")
            row["plausible"] = "" if offer_vs is None else int(-0.6 < offer_vs < 0.6)
            listing_bar = last_on_or_before(bars, i["listing"])
            if listing_bar and listing_bar["date"] == i["listing"].isoformat():
                rate = last_on_or_before(fx, i["listing"])
                if rate:
                    row["a_close_hkd_listing"] = round(listing_bar["close"] * rate["close"], 4)
                    row["h_day1_close_vs_a"] = round(i["close1"] / (listing_bar["close"] * rate["close"]) - 1, 6)
        out_rows.append(row)

    with (CACHE / "a_share_map.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(map_rows[0]))
        writer.writeheader()
        writer.writerows(map_rows)
    fields = list(dict.fromkeys(k for r in out_rows for k in r))
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out_rows)
    matched = sum(1 for r in out_rows if r.get("offer_vs_a_close") is not None)
    print(f"{len(issuers)} A+H issuers: {sum(1 for r in map_rows if r['a_symbol'])} A-share symbols found, {matched} with an offer-vs-A anchor -> {OUTPUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
