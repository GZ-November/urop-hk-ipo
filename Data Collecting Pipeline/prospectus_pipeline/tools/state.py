#!/usr/bin/env python3
"""Record hash-bound extraction and independent-review workflow states."""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent if Path(__file__).resolve().parent.name == "tools" else Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from cohort import load_cfg  # noqa: E402
from state import save_record, require  # noqa: E402
from validate import validate_all  # noqa: E402


def get_records_by_code(cfg, codes, target):
    report = validate_all(cfg, only=codes if codes else None, target=target)
    by_code = {}
    for r in report.get("records", []):
        c = r.get("code")
        if c:
            by_code[c] = r
    return by_code


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["extracted", "reviewed"])
    ap.add_argument("--target", choices=["prospectus", "allot"], required=True)
    ap.add_argument("--code", nargs="*", default=None, help="一个或多个股票代码，如 6082.HK")
    ap.add_argument("--all", action="store_true", default=False, help="处理全部公司")
    ap.add_argument("--verdict", choices=["pass", "fail"])
    ap.add_argument("--workbook", help="目标工作簿路径")
    ap.add_argument("--period-start", help="纳入样本起始日期 YYYY-MM-DD")
    ap.add_argument("--period-end", help="纳入样本截止日期 YYYY-MM-DD")
    args = ap.parse_args()
    cfg = load_cfg(args.workbook, args.period_start, args.period_end)

    if args.all:
        from cohort import read_companies
        codes = [c["code"] for c in read_companies(cfg)]
        target_codes = None
    elif args.code:
        codes = args.code
        target_codes = codes
    else:
        ap.error("必须指定 --code 或 --all")

    records_map = get_records_by_code(cfg, target_codes, args.target)

    for code in codes:
        rec = records_map.get(code)
        if not rec:
            raise SystemExit(f"{code}: record not found in validation output")
        if not rec.get("gate_pass", rec.get("status") in {"pass", "warning_missing"}):
            raise SystemExit(f"{code}: current JSON did not pass deterministic validation")
        payload = {**rec, "code": code, "target": args.target, "gate_pass": True}

        if args.stage == "extracted":
            save_record(cfg, args.target, code, "extracted", payload)
            print(f"RECORDED extracted {code} {rec['hash']}")
        else:
            require(cfg, args.target, code, rec["hash"], "extracted")
            require(cfg, args.target, code, rec["hash"], "validated")
            passed = args.verdict == "pass"
            save_record(cfg, args.target, code, "reviewed",
                        {**payload, "verdict": args.verdict, "gate_pass": passed})
            print(f"RECORDED reviewed={args.verdict} {code} {rec['hash']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
