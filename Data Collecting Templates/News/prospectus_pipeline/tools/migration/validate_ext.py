#!/usr/bin/env python3
"""校验扩展 18 列的抽取结果（out_ext/extracted/*.json）。

只做结构契约 + 证据核验（页码真实、引文连续），不做跨字段勾稽
（勾稽在合并后的全量 validate 里做）。

用法：python3 tools_validate_ext.py [--only 6082.HK ...]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from contracts import (  # noqa: E402
    evidence_issues, is_missing, normalize_code, strict_load_file, validate_record,
)

EXT_KEYS = ["col_BA", "col_BB", "col_BC", "col_BD", "col_BE", "col_BF", "col_BG",
            "col_BI", "col_BP", "col_BR", "col_BT", "col_CC", "col_CD", "col_CE",
            "col_CF", "col_CG", "col_CH", "col_CI"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", default=None)
    args = ap.parse_args()

    full = json.loads((ROOT / "schema" / "fields.json").read_text(encoding="utf-8"))
    ext_schema = {"fields": [f for f in full["fields"] if f["key"] in EXT_KEYS]}
    ext_schema["field_count"] = len(ext_schema["fields"])

    ext_dir = ROOT / "out_ext" / "extracted"
    files = {normalize_code(f.stem.replace("HKIPO-MB", "")): f
             for f in ext_dir.glob("*.json")}
    wanted = [normalize_code(x) for x in args.only] if args.only else sorted(files)

    n_err = 0
    for code in wanted:
        fp = files.get(code)
        if fp is None:
            print(f"MISSING          {code}")
            n_err += 1
            continue
        packets_dir = ROOT / "data" / "packets_ext"
        packet = packets_dir / f"HKIPO-MB{code.split('.')[0]}.md"
        try:
            rec = strict_load_file(fp)
            errs = validate_record(rec, ext_schema, code)
            if packet.exists():
                # 扩展包本身带 <<<PAGE>>>（bundle 片段），页码核验用它
                alt = None
                textf = ROOT / "data" / "text" / f"HKIPO-MB{code.split('.')[0]}.jsonl"
                if textf.exists():
                    alt = {"prospectus": "\n".join(
                        f"<<<PAGE {json.loads(x)['page']}>>>\n{json.loads(x)['text']}"
                        for x in textf.open(encoding="utf-8"))}
                errs += evidence_issues(rec, packet, ext_schema, alt)
            else:
                errs.append(f"packet missing: {packet}")
            fields = rec.get("fields") or {}
            missing = [k for k in EXT_KEYS
                       if is_missing((fields.get(k) or {}).get("value"),
                                     next(f.get("kind", "text")
                                          for f in ext_schema["fields"] if f["key"] == k))]
            status = "ERROR" if errs else ("WARNING_MISSING" if missing else "PASS")
            if errs:
                n_err += 1
            print(f"{status:15s} {code:9s} missing={len(missing):2d} errors={len(errs):2d}")
            for e in errs[:6]:
                print(f"    - {e[:150]}")
        except Exception as exc:  # noqa: BLE001
            n_err += 1
            print(f"ERROR           {code:9s} {type(exc).__name__}: {exc}")

    print(f"\n扩展校验：{len(wanted)} 家，{n_err} 家有 ERROR")
    return 1 if n_err else 0


if __name__ == "__main__":
    raise SystemExit(main())
