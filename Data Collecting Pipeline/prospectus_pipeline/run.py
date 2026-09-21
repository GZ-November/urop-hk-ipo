#!/usr/bin/env python3
"""招股书自动采集流水线 CLI。

用法：
  python3 prospectus_pipeline/run.py find          # 定位招股书 PDF 链接
  python3 prospectus_pipeline/run.py download      # 下载 PDF
  python3 prospectus_pipeline/run.py prepare       # 抽文本 + 分组切片 + 生成 AI 抽取包
  python3 prospectus_pipeline/run.py validate      # 校验 AI 抽取结果
  python3 prospectus_pipeline/run.py write         # 写回模板（仅浅蓝列）
  python3 prospectus_pipeline/run.py all           # find + download + prepare
加 --limit N 只处理前 N 家，--only 6082.HK 只处理指定公司。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent          # prospectus_pipeline/
WS = ROOT.parent                                # 工作簿所在目录
sys.path.insert(0, str(ROOT / "src"))


def load_cfg(workbook_override: str | None = None) -> dict:
    with open(ROOT / "config.yaml") as f:
        cfg = yaml.safe_load(f)
    if workbook_override:
        cfg["workbook"] = workbook_override
    cfg["_root"] = ROOT
    cfg["_ws"] = WS
    for k, v in cfg["paths"].items():
        p = WS / v
        p.mkdir(parents=True, exist_ok=True)
        cfg["paths"][k] = p
    return cfg


def _to_date(v):
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    return None


def read_companies(cfg: dict) -> list[dict]:
    import openpyxl
    wb = openpyxl.load_workbook(WS / cfg["workbook"], read_only=True, data_only=True)
    ws = wb[cfg["sheet"]]
    ic = cfg["id_columns"]
    companies = []
    from openpyxl.utils import column_index_from_string
    positions = {k: column_index_from_string(v) - 1 for k, v in ic.items()}
    for r, values in enumerate(ws.iter_rows(min_row=cfg["data_start_row"],
                                           max_col=max(positions.values()) + 1,
                                           values_only=True), cfg["data_start_row"]):
        code = values[positions["stock_code"]]
        if code in (None, ""):
            continue
        companies.append({
            "row": r,
            "file_no": values[positions["file_no"]],
            "code": str(code).strip(),
            "name": str(values[positions["name"]] or "").strip(),
            "prospectus_date": _to_date(values[positions["prospectus_date"]]),
            "listing_date": _to_date(values[positions["listing_date"]]),
        })
    wb.close()
    return companies


def cmd_find(cfg, args, companies):
    from hkex import find_all
    from storage import merge_index
    found = find_all(cfg["hkex"], companies)
    payload = [f.__dict__ for f in found]
    out = cfg["paths"]["out"] / "found.json"
    merge_index(out, payload)
    ok = sum(1 for f in found if f.status == "ok")
    print(f"\n定位完成：{ok}/{len(found)} 找到招股书 -> {out}")
    for f in found:
        if f.status != "ok":
            print(f"   未找到：{f.code} {f.name[:40]} | {f.note}")
    return payload


def cmd_download(cfg, args, companies):
    from pdfprep import download_all
    found = json.loads((cfg["paths"]["out"] / "found.json").read_text())
    if args.only:
        found = [f for f in found if f["code"] in args.only]
    if args.limit:
        found = found[: args.limit]
    return download_all(cfg, found)


def cmd_prepare(cfg, args, companies):
    from pdfprep import prepare_all
    src = cfg["paths"]["out"] / "downloaded.json"
    if not src.exists():
        src = cfg["paths"]["out"] / "found.json"
    found = json.loads(src.read_text())
    for rec in found:                     # 兜底：补齐本地 PDF 路径
        if not rec.get("pdf") and rec.get("status") == "ok":
            p = cfg["paths"]["pdf"] / f"HKIPO-MB{''.join(c for c in rec['code'] if c.isdigit())}.pdf"
            rec["pdf"] = str(p) if p.exists() else None
    if args.only:
        found = [f for f in found if f["code"] in args.only]
    if args.limit:
        found = found[: args.limit]
    with_topics = not getattr(args, "no_topics", False)
    return prepare_all(cfg, found, with_topics=with_topics)


def cmd_allot(cfg, args, companies):
    """配发结果公告：下载 PDF + 抽全文 + 生成抽取包（整篇，不切片）。"""
    from allotprep import download_all, prepare_all
    index = json.loads((cfg["paths"]["out"] / "allotment_index.json").read_text())
    # 公司名取自 found.json（allotment_index 只存了代码/时间/链接）
    names = {}
    found_path = cfg["paths"]["out"] / "found.json"
    if found_path.exists():
        for rec in json.loads(found_path.read_text()):
            names[rec.get("code")] = rec.get("name", "")
    wanted = {c["code"] for c in companies}
    index = [r for r in index if r["code"] in wanted]
    for r in index:
        r.setdefault("name", names.get(r["code"], ""))
        r.setdefault("title", "ANNOUNCEMENT OF (FINAL) OFFER PRICE AND ALLOTMENT RESULTS")
    if args.only:
        index = [r for r in index if r["code"] in args.only]
    if args.limit:
        index = index[: args.limit]
    print(f"配发结果公告：{len(index)} 家")
    dl = download_all(cfg, index)
    return prepare_all(cfg, dl)


def cmd_greenshoe(cfg, args, companies):
    """绿鞋核实：检索行使公告 -> 取实际配发股数 -> 确定性回填 col_CV。"""
    from greenshoe import apply_cv, fetch_index, fetch_shares
    found_path = cfg["paths"]["out"] / "found.json"
    found = json.loads(found_path.read_text())
    wanted = {c["code"] for c in companies}
    found = [r for r in found if r["code"] in wanted]
    index = fetch_index(cfg, found, only=args.only)
    fetch_shares(cfg, index, only=args.only)
    apply_cv(cfg, only=args.only)


def cmd_cornerstone(cfg, args, companies):
    """基石核实：确认「无基石投资者」的公司把 col_CK 写成 0。"""
    from cornerstone import apply_ck, scan
    scan(cfg, only=args.only)
    apply_ck(cfg, only=args.only)


def cmd_validate(cfg, args, companies):
    from validate import validate_all
    return validate_all(cfg, only=args.only, limit=args.limit, target=args.target)


def cmd_derive_allot(cfg, args, companies):
    """Explicit mutating stage for deterministic allotment fields."""
    from greenshoe import apply_cv
    from cornerstone import apply_ck
    from pricing_date import apply_cq
    from validate import apply_da
    apply_cv(cfg, only=args.only)
    apply_ck(cfg, only=args.only)
    apply_cq(cfg, only=args.only)
    apply_da(cfg, only=args.only)
    return 0


def cmd_validate_ext(cfg, args, companies):
    import subprocess
    cmd = [sys.executable, str(ROOT / "tools" / "validate_ext.py")]
    if args.only:
        cmd.extend(["--only", *args.only])
    return subprocess.call(cmd, cwd=WS)


def cmd_write(cfg, args, companies):
    from write_back import write_all
    return write_all(cfg, fill_missing=args.fill_missing, only=args.only,
                     limit=args.limit, target=args.target)


def cmd_audit(cfg, args, companies):
    from audit import run_audit
    only = [c["code"] for c in companies] if args.only else None
    target = args.target if args.target in ("prospectus", "allot") else "all"
    run_audit(cfg, only=only, target=target)
    return 0


def cmd_cross_check(cfg, args, companies):
    from cross_check import run_cross_check
    only = [c["code"] for c in companies] if args.only else None
    res = run_cross_check(cfg, only=only)
    print("\n" + "=" * 70)
    print(f"HK IPO 宏观业务逻辑与跨字段一致性审计完成 (共 {res['total_companies']} 家公司)")
    print("=" * 70)
    print(f"100% 完美达标公司: {res['clean_companies']} / {res['total_companies']}")
    print(f"异常或业务预警项: {res['total_anomalies']} 项")
    print("报告已输出至: out/cross_check_report.md & out/cross_check_report.json\n")
    return 1 if any(r["status"] == "ERROR" for r in res["results"]) else 0


def cmd_report(cfg, args, companies):
    from report import generate_report, print_summary
    stats = generate_report(cfg)
    print_summary(stats)
    return 0


def cmd_export(cfg, args, companies):
    from codebook import export_all
    export_all(cfg)
    return 0


def cmd_codebook(cfg, args, companies):
    from codebook import export_all
    export_all(cfg)
    return 0


def cmd_status(cfg, args, companies):
    from auto_fill import inventory, print_status
    print_status(inventory())
    return 0


def cmd_search(cfg, args, companies):
    import subprocess
    cmd = [sys.executable, str(ROOT / "tools" / "search.py")] + sys.argv[2:]
    return subprocess.call(cmd, cwd=WS)


def cmd_state(cfg, args, companies):
    import subprocess
    cmd = [sys.executable, str(ROOT / "tools" / "state.py")] + sys.argv[2:]
    return subprocess.call(cmd, cwd=WS)


def cmd_external(cfg, args, companies):
    """Orchestrate external data collection tools."""
    import subprocess
    external_scripts = [
        ("market", ROOT / "tools" / "external" / "market.py"),
        ("hkma_import", ROOT / "tools" / "external" / "hkma_import.py"),
        ("ipo_count", ROOT / "tools" / "external" / "ipo_count.py"),
        ("flags", ROOT / "tools" / "external" / "flags.py"),
        ("rules", ROOT / "tools" / "external" / "rules.py"),
        ("hsic_codes", ROOT / "tools" / "external" / "hsic_codes.py"),
    ]
    for name, script in external_scripts:
        if script.exists():
            print(f"\n--- 执行外部工具: {name} ---")
            cmd = [sys.executable, str(script)]
            subprocess.run(cmd, cwd=WS, check=False)
def cmd_merge_topics(cfg, args, companies):
    """将 4 个主题分片合并为完整招股书抽取 JSON。"""
    from merge_topics import merge_topics_for_code
    codes = [c["code"] for c in companies] if companies else (args.only or [])
    if not codes:
        print("请指定要合并的公司代码，例如 --only 6082.HK")
        return 1
    success = 0
    for code in codes:
        dest = merge_topics_for_code(cfg, code)
        if dest:
            success += 1
    print(f"\n主题分片合并完成：{success}/{len(codes)} 家")
    return 0 if success == len(codes) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="招股书 / 配发公告自动采集流水线")
    ap.add_argument("stage", choices=["find", "download", "prepare", "allot", "greenshoe", "cornerstone",
                                     "derive_allot", "validate", "validate_ext", "write", "audit", "cross_check",
                                     "report", "codebook", "export", "status", "external", "search", "state",
                                     "merge_topics", "all"])
    ap.add_argument("extra", nargs="*", default=[], help="传递给 search/state 的额外参数")
    ap.add_argument("--no-topics", action="store_true", help="跳过生成 4 个主题分片包")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", nargs="*", default=None, help="只处理这些股票代码，如 6082.HK")
    ap.add_argument("--target", choices=["prospectus", "allot", "all"], default="prospectus",
                    help="validate/write/audit 作用于哪套字段（默认 prospectus，audit 支持 all）")
    ap.add_argument("--fill-missing", action="store_true",
                    help="write 阶段：按手册把缺失写成 NaN（数值）或 NA（文本/日期）")
    ap.add_argument("--workbook", default=None,
                    help="指定/覆盖目标工作簿文件名，例如 HKIPO-MB2026Q1.xlsx")
    args, extra = ap.parse_known_args()
    args.extra = (args.extra or []) + extra

    if args.stage in ("search", "state"):
        return globals()[f"cmd_{args.stage}"](None, args, None)

    cfg = load_cfg(workbook_override=args.workbook)
    companies = read_companies(cfg)
    print(f"工作簿 {cfg['workbook']} 共 {len(companies)} 家公司")
    if args.only:
        companies = [c for c in companies if c["code"] in args.only]
    if args.limit:
        companies = companies[: args.limit]

    stages = ["find", "download", "prepare"] if args.stage == "all" else [args.stage]
    rc = 0
    for s in stages:
        print(f"\n=== {s} ===")
        result = globals()[f"cmd_{s}"](cfg, args, companies)
        if s == "validate" and isinstance(result, dict) and result.get("errors"):
            rc = 1
        elif s == "validate_ext" and isinstance(result, int):
            rc = result
        elif s in {"find", "download", "prepare", "allot"} and isinstance(result, list):
            if not result or any(not (r.get("pdf") or r.get("packet_path") or r.get("status") == "ok") for r in result):
                rc = 1
        if rc:
            break
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
