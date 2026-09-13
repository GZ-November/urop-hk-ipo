#!/usr/bin/env python3
"""Record hash-bound extraction and independent-review workflow states."""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent if Path(__file__).resolve().parent.name == "tools" else Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from run import load_cfg  # noqa: E402
from state import save_record, require  # noqa: E402
from validate import validate_all  # noqa: E402


def current(cfg, code, target):
    report = validate_all(cfg, only=[code], target=target)
    rec = report["records"][0]
    if not rec.get("gate_pass", rec.get("status") in {"pass", "warning_missing"}):
        raise SystemExit(f"{code}: current JSON did not pass deterministic validation")
    return {**rec, "code": code, "target": target, "gate_pass": True}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["extracted", "reviewed"])
    ap.add_argument("--target", choices=["prospectus", "allot"], required=True)
    ap.add_argument("--code", nargs="*", default=None, help="一个或多个股票代码，如 6082.HK")
    ap.add_argument("--all", action="store_true", default=False, help="处理全部公司")
    ap.add_argument("--verdict", choices=["pass", "fail"])
    args = ap.parse_args()
    cfg = load_cfg()

    if args.all:
        from run import read_companies
        codes = [c["code"] for c in read_companies(cfg)]
    elif args.code:
        codes = args.code
    else:
        ap.error("必须指定 --code 或 --all")

    for code in codes:
        rec = current(cfg, code, args.target)
        if args.stage == "extracted":
            save_record(cfg, args.target, code, "extracted", rec)
            print(f"RECORDED extracted {code} {rec['hash']}")
        else:
            require(cfg, args.target, code, rec["hash"], "extracted")
            require(cfg, args.target, code, rec["hash"], "validated")
            passed = args.verdict == "pass"
            save_record(cfg, args.target, code, "reviewed",
                        {**rec, "verdict": args.verdict, "gate_pass": passed})
            print(f"RECORDED reviewed={args.verdict} {code} {rec['hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
