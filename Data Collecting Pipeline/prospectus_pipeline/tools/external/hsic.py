#!/usr/bin/env python3
"""【在线爬虫】从港交所报价接口实时抓取每家公司的恒生行业分类（HSIC）英文名。

接口：https://www1.hkex.com.hk/hkexwidget/data/getequityquote
  ?sym=<4位代码>&token=<页面 token>&lang=eng&qid=<ts>&callback=cb
token 从港交所证券行情页面内联脚本动态解析取得。

返回字段（与 BN/BO 相关）：
  hsic_ind_classification         "Information Technology - Semiconductors"（行业 - 业务类别）
  hsic_sub_sector_classification  "Semiconductors"（业务子类别，对应 HSICS 6 位码）
  incorpin                        注册地（可与 BQ 交叉验证）
  listing_category                上市类别（Primary / Secondary）

输出：out/hsic.json
注意：需联网访问港交所接口；抓取后由离线入表工具 tools/external/hsic_codes.py 负责映射并写入工作簿。
"""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2] if Path(__file__).resolve().parent.name == "external" else Path(__file__).resolve().parent
WS = ROOT.parent
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")
PAGE = "https://www.hkex.com.hk/Market-Data/Securities-Prices/Equities/Equities-Quote"
WIDGET = "https://www1.hkex.com.hk/hkexwidget/data/getequityquote"
TOKEN_RE = re.compile(r'return\s+"([A-Za-z0-9+/=%._-]{40,})"')


def fresh_token(sess: requests.Session, log=print) -> str:
    r = sess.get(PAGE, params={"sym": "1", "sc_lang": "en"},
                 headers={"User-Agent": UA}, timeout=30)
    r.raise_for_status()
    m = TOKEN_RE.search(r.text)
    if not m:
        raise RuntimeError("页面里找不到 token")
    log(f"token 已刷新（{len(m.group(1))} 字符）")
    return m.group(1)


def fetch_one(sess: requests.Session, code: str, token: str) -> dict:
    digits = "".join(c for c in str(code) if c.isdigit())
    # 接口要的是去前导零的形式（100 而非 0100），否则 "Invalid Input"
    digits = str(int(digits)) if digits else digits
    # token 本身已 URL 编码（含 %2f/%2b），必须原样拼进 query，
    # 交给 requests 的 params 会被二次编码成 %252f 导致 403。
    url = (f"{WIDGET}?sym={digits}&token={token}&lang=eng"
           f"&qid={int(time.time() * 1000)}&callback=cb")
    r = sess.get(url, headers={"User-Agent": UA,
                               "Referer": "https://www.hkex.com.hk/"}, timeout=30)
    r.raise_for_status()
    txt = r.text
    if txt.startswith("cb("):
        txt = txt[3:txt.rfind(")")]
    d = json.loads(txt)
    q = ((d.get("data") or {}).get("quote")) or {}
    return q


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "out" / "hsic.json"))
    args = ap.parse_args()

    cfg = json.loads((ROOT / "out" / "packets.json").read_text(encoding="utf-8"))
    codes = [x["code"] for x in cfg]

    sess = requests.Session()
    token = fresh_token(sess)
    out, n_tok = {}, 0
    for i, code in enumerate(codes, 1):
        for attempt in (1, 2):
            try:
                q = fetch_one(sess, code, token)
                break
            except Exception as exc:  # noqa: BLE001
                if attempt == 2:
                    print(f"ERR  {code}: {type(exc).__name__}: {exc}")
                    q = {}
                else:
                    token = fresh_token(sess)
                    n_tok += 1
        out[code] = {
            "hsic_ind": q.get("hsic_ind_classification"),
            "hsic_sub": q.get("hsic_sub_sector_classification"),
            "incorp": q.get("incorpin"),
            "listing_category": q.get("listing_category"),
            "listing_date": q.get("listing_date"),
            "board": q.get("primaryexch"),
            "name": q.get("issuer_name"),
        }
        print(f"[{i:2d}/{len(codes)}] {code:9s} {str(q.get('hsic_ind_classification'))[:34]:36s} "
              f"| {str(q.get('hsic_sub_sector_classification'))[:26]:28s} | {q.get('incorpin')}")
        time.sleep(0.35)

    Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                              encoding="utf-8")
    ok = sum(1 for v in out.values() if v["hsic_sub"])
    print(f"\n成功 {ok}/{len(out)}（token 刷新 {n_tok} 次）-> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
