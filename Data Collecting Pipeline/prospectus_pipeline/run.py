#!/usr/bin/env python3
"""招股书自动采集流水线 CLI。

用法：
  python3 prospectus_pipeline/run.py find          # 定位招股书 PDF 链接
  python3 prospectus_pipeline/run.py download      # 下载 PDF
  python3 prospectus_pipeline/run.py prepare       # 抽文本 + 分组切片 + 生成 AI 抽取包
  python3 prospectus_pipeline/run.py validate      # 校验 AI 抽取结果
  python3 prospectus_pipeline/run.py write         # 写回模板（仅浅蓝列）
  python3 prospectus_pipeline/run.py all           # find + download + prepare
  python3 prospectus_pipeline/run.py collect --period-start YYYY-MM-DD --period-end YYYY-MM-DD
                                                 # 按上市日期建立并推进普通主板 IPO cohort
加 --limit N 只处理前 N 家，--only 6082.HK 只处理指定公司。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent          # prospectus_pipeline/
WS = ROOT.parent                                # 工作簿所在目录
sys.path.insert(0, str(ROOT / "src"))
from cohort import build_cohort_workbook, load_cfg, read_companies, write_cohort_config


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
    codes = [c["code"] for c in companies]
    index = fetch_index(cfg, found, only=codes)
    fetch_shares(cfg, index, only=codes)
    apply_cv(cfg, only=codes)
    return 0


def cmd_cornerstone(cfg, args, companies):
    """基石核实：确认「无基石投资者」的公司把 col_CK 写成 0。"""
    from cornerstone import apply_ck, scan
    codes = [c["code"] for c in companies]
    scan(cfg, only=codes)
    apply_ck(cfg, only=codes)
    return 0


def cmd_validate(cfg, args, companies):
    from validate import validate_all
    return validate_all(cfg, only=[c["code"] for c in companies], limit=0, target=args.target)


def cmd_derive_allot(cfg, args, companies):
    """Explicit mutating stage for deterministic allotment fields."""
    from greenshoe import apply_cv
    from cornerstone import apply_ck
    from pricing_date import apply_cq
    from validate import apply_da
    codes = [c["code"] for c in companies]
    apply_cv(cfg, only=codes)
    apply_ck(cfg, only=codes)
    apply_cq(cfg, only=codes)
    apply_da(cfg, only=codes)
    return 0


def cmd_validate_ext(cfg, args, companies):
    import subprocess
    cmd = [sys.executable, str(ROOT / "tools" / "validate_ext.py")]
    codes = [c["code"] for c in companies]
    if codes:
        cmd.extend(["--only", *codes])
    return subprocess.call(cmd, cwd=WS)


def cmd_write(cfg, args, companies):
    from write_back import write_all
    write_all(cfg, fill_missing=args.fill_missing, only=[c["code"] for c in companies],
              limit=0, target=args.target)
    return 0


def cmd_audit(cfg, args, companies):
    from audit import run_audit
    only = [c["code"] for c in companies]
    target = args.target if args.target in ("prospectus", "allot") else "all"
    run_audit(cfg, only=only, target=target)
    return 0


def cmd_cross_check(cfg, args, companies):
    from cross_check import run_cross_check
    only = [c["code"] for c in companies]
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
    print_status(inventory(cfg))
    return 0


def cmd_search(cfg, args, companies):
    import subprocess
    env = os.environ.copy()
    cmd = [sys.executable, str(ROOT / "tools" / "search.py"), *args.extra]
    return subprocess.call(cmd, cwd=WS, env=env)


def cmd_state(cfg, args, companies):
    import subprocess
    cmd = [sys.executable, str(ROOT / "tools" / "state.py"), *args.extra,
           "--target", args.target]
    return subprocess.call(cmd, cwd=WS)


def cmd_aftermarket(cfg, args, companies):
    """采集与计算港股新股二级市场跨期表现与流动性衰减指标 (Col 139-161)。"""
    import subprocess
    script = ROOT / "tools" / "external" / "aftermarket.py"
    cmd = [sys.executable, str(script)]
    if getattr(args, "dry_run", False):
        cmd.append("--dry-run")
    codes = [c["code"] for c in companies]
    if codes:
        cmd.extend(["--only"] + codes)
    cmd.extend(["--book", str(cfg["_workbook_path"])])
    return subprocess.call(cmd, cwd=WS)


def cmd_allot_index(cfg, args, companies):
    """Build allotment index for the selected cohort."""
    import subprocess
    cmd = [sys.executable, str(ROOT / "tools" / "build_allotment_index.py")]
    return subprocess.call(cmd, cwd=WS)


def cmd_expansion(cfg, args, companies):
    """Write back academic expansion fields."""
    import subprocess
    cmd = [sys.executable, str(ROOT / "src" / "write_back_expansion.py"), "--workbook", str(cfg["_workbook_path"])]
    return subprocess.call(cmd, cwd=WS)


def cmd_disclosure_notes(cfg, args, companies):
    """Derive the 10 disclosure note columns."""
    import subprocess
    cmd = [sys.executable, str(ROOT / "tools" / "derive_disclosure_notes.py"), "--book", str(cfg["_workbook_path"])]
    if args.only:
        cmd.extend(["--only", *args.only])
    return subprocess.call(cmd, cwd=WS)


def _ipo_count_reports(cfg, args, companies):
    """Resolve every official report needed for the prospectus 90-day windows."""
    from datetime import timedelta
    from listing_reports import reports_for_interval

    prospectus_dates = [c["prospectus_date"] for c in companies if c.get("prospectus_date")]
    if len(prospectus_dates) != len(companies):
        raise ValueError("至少一家发行人缺少招股书日期，无法计算上市前 90 天 IPO 数。")
    source_dir = Path(
        getattr(args, "source_dir", None)
        or cfg["dataset"].get("report_source_dir")
        or WS / "sources"
    ).expanduser().resolve()
    return reports_for_interval(
        min(prospectus_dates) - timedelta(days=90),
        max(prospectus_dates) - timedelta(days=1),
        source_dir,
    )


def cmd_external(cfg, args, companies):
    """Orchestrate external data collection tools with fail-closed execution."""
    import subprocess
    from datetime import timedelta

    try:
        nlr_reports = _ipo_count_reports(cfg, args, companies)
    except (OSError, ValueError) as exc:
        print(f"错误: 90 天 IPO 统计缺少官方年度报告: {exc}", file=sys.stderr)
        return 1
    prospectus_dates = [c["prospectus_date"] for c in companies]
    external_scripts = [
        ("market", ROOT / "tools" / "external" / "market.py", True, True),
        ("hkma", ROOT / "tools" / "external" / "hkma.py", False, False),
        ("hkma_import", ROOT / "tools" / "external" / "hkma_import.py", True, True),
        ("ipo_count", ROOT / "tools" / "external" / "ipo_count.py", True, True),
        ("flags", ROOT / "tools" / "external" / "flags.py", True, True),
        ("rules", ROOT / "tools" / "external" / "rules.py", True, True),
        ("hsic", ROOT / "tools" / "external" / "hsic.py", False, False),
        ("hsic_codes", ROOT / "tools" / "external" / "hsic_codes.py", True, True),
        ("aftermarket", ROOT / "tools" / "external" / "aftermarket.py", True, True),
    ]
    book_target = str(cfg["_workbook_path"])
    for name, script, wants_book, wants_only in external_scripts:
        if not script.exists():
            print(f"错误: 外部脚本不存在: {script}")
            return 1
        print(f"\n--- 执行外部工具: {name} ---")
        cmd = [sys.executable, str(script)]
        if name == "hkma":
            start = min(prospectus_dates) - timedelta(days=7)
            cmd.extend(["--from", start.isoformat(), "--to", cfg["dataset"]["period_end"],
                        "--out", str(cfg["paths"]["data"] / "manual" / "hibor_balance.csv")])
        if name == "hkma_import":
            cmd.extend(["--csv", str(cfg["paths"]["data"] / "manual" / "hibor_balance.csv")])
        if name == "ipo_count":
            cmd.extend(["--nlr", *(str(path) for path in nlr_reports)])
        if getattr(args, "dry_run", False) and wants_book:
            cmd.append("--dry-run")
        codes = [c["code"] for c in companies]
        if codes and wants_only:
            cmd.extend(["--only"] + codes)
        if wants_book:
            cmd.extend(["--book", book_target])
        proc = subprocess.run(cmd, cwd=WS)
        if proc.returncode != 0:
            print(f"错误: 外部工具 {name} 执行失败 (退出码 {proc.returncode})，终止后续流程。")
            return proc.returncode
    return 0


def cmd_collect(cfg, args, companies):
    """Prepare a date-selected cohort, then resume through the review gates."""
    from contracts import normalize_code
    from state import read_record

    wanted = {normalize_code(c["code"]) for c in companies}

    def index_covers(path: Path, packet_dir: Path) -> bool:
        if not path.is_file():
            return False
        try:
            records = json.loads(path.read_text(encoding="utf-8"))
            indexed = {normalize_code(item["code"]) for item in records}
            return wanted <= indexed and all(
                (packet_dir / f"HKIPO-MB{code.split('.')[0]}.md").is_file()
                for code in wanted
            )
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
            return False

    out = cfg["paths"]["out"]
    allot_out = cfg["paths"]["allot_out"]
    if not index_covers(out / "packets.json", cfg["paths"]["packets"]):
        for stage in (cmd_find, cmd_download, cmd_prepare):
            result = stage(cfg, args, companies)
            if not result or any(rec.get("status") == "error" for rec in result):
                return 1
        if not index_covers(out / "packets.json", cfg["paths"]["packets"]):
            print("Prospectus preparation did not cover every issuer in the cohort.", file=sys.stderr)
            return 1
    if not index_covers(allot_out / "packets.json", cfg["paths"]["allot_packets"]):
        if cmd_allot_index(cfg, args, companies):
            return 1
        result = cmd_allot(cfg, args, companies)
        if not result:
            return 1
        if not index_covers(allot_out / "packets.json", cfg["paths"]["allot_packets"]):
            print("Allotment preparation did not cover every issuer in the cohort.", file=sys.stderr)
            return 1

    def missing_extractions(directory: Path) -> list[str]:
        return [
            code for code in sorted(wanted)
            if not (directory / f"HKIPO-MB{code.split('.')[0]}.json").is_file()
        ]

    missing_prospectus = missing_extractions(out / "extracted")
    missing_allot = missing_extractions(allot_out / "extracted")
    if missing_prospectus or missing_allot:
        print("Cohort workbook and document packets are ready. Extraction is still required.")
        print("  Cohort config:", cfg["_config_path"])
        if missing_prospectus:
            print("  Prospectus:", ", ".join(missing_prospectus))
            print("  Workflow:", ROOT / "workflows" / "prospectus_extract.js")
        if missing_allot:
            print("  Allotment:", ", ".join(missing_allot))
            print("  Workflow:", ROOT / "workflows" / "allot_extract.js")
        print("After extraction and independent review, rerun the same collect command.")
        return 3

    for target in ("prospectus", "allot"):
        result = cmd_validate(cfg, argparse.Namespace(target=target), companies)
        if result.get("errors") or result.get("missing_files") or not result.get("gate_pass"):
            return 1
    unreviewed = [
        f"{code} {target}" for code in sorted(wanted) for target in ("prospectus", "allot")
        if not read_record(cfg, target, code, "reviewed").get("gate_pass")
    ]
    if unreviewed:
        print("Independent review is required before write-back:", ", ".join(unreviewed))
        print("  Cohort config:", cfg["_config_path"])
        return 3

    try:
        _ipo_count_reports(cfg, args, companies)
    except (OSError, ValueError) as exc:
        print(f"错误: 90 天 IPO 统计缺少官方年度报告: {exc}", file=sys.stderr)
        return 1

    for target in ("prospectus", "allot"):
        if cmd_write(cfg, argparse.Namespace(target=target, fill_missing=True), companies):
            return 1
    if cmd_external(cfg, args, companies):
        return 1
    cmd_audit(cfg, argparse.Namespace(target="all"), companies)
    return cmd_cross_check(cfg, args, companies)


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
    ap.add_argument("stage", choices=["find", "download", "prepare", "allot_index", "allot", "greenshoe", "cornerstone",
                                     "derive_allot", "validate", "validate_ext", "write", "audit", "cross_check",
                                     "report", "codebook", "export", "status", "external", "aftermarket", "expansion",
                                     "disclosure_notes", "search", "state",
                                     "merge_topics", "all", "collect"])
    ap.add_argument("extra", nargs="*", default=[], help="传递给 search/state 的额外参数")
    ap.add_argument("--dry-run", action="store_true", help="演练模式，不写回工作簿")
    ap.add_argument("--no-topics", action="store_true", help="跳过生成 4 个主题分片包")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", nargs="*", default=None, help="只处理这些股票代码，如 6082.HK")
    ap.add_argument("--target", choices=["prospectus", "allot", "all"], default="prospectus",
                    help="validate/write/audit 作用于哪套字段（默认 prospectus，audit 支持 all）")
    ap.add_argument("--fill-missing", action="store_true",
                    help="write 阶段：按手册把缺失写成 NaN（数值）或 NA（文本/日期）")
    ap.add_argument("--workbook", default=None,
                    help="指定目标工作簿路径（可为相对路径或绝对路径）")
    ap.add_argument("--config", default=None,
                    help="指定 cohort 配置文件；也可用 PIPELINE_CONFIG 环境变量")
    ap.add_argument("--period-start", default=None, help="纳入样本的起始日期，格式 YYYY-MM-DD")
    ap.add_argument("--period-end", default=None, help="纳入样本的截止日期，格式 YYYY-MM-DD")
    ap.add_argument("--source-dir", default=None, help="官方年度新上市报告的本地缓存目录（collect）")
    args, extra = ap.parse_known_args()
    args.extra = (args.extra or []) + extra

    if args.stage == "collect" and args.dry_run:
        ap.error("collect does not support --dry-run; use individual stages to preview writes")

    generated_cohort = args.stage == "collect" and not args.workbook
    runtime_override = bool(
        args.workbook or args.period_start or args.period_end
        or os.environ.get("HKIPO_WORKBOOK")
        or os.environ.get("HKIPO_PERIOD_START")
        or os.environ.get("HKIPO_PERIOD_END")
    )
    if generated_cohort:
        if not args.period_start or not args.period_end:
            ap.error("date-only collect requires --period-start and --period-end")
        try:
            from datetime import date
            start = date.fromisoformat(args.period_start)
            end = date.fromisoformat(args.period_end)
            workbook = build_cohort_workbook(
                start, end,
                source_dir=Path(args.source_dir) if args.source_dir else None,
            )
            args.config = str(write_cohort_config(
                start, end, workbook,
                base_config=Path(args.config) if args.config else None,
                source_dir=Path(args.source_dir) if args.source_dir else None,
            ))
            args.period_start = None
            args.period_end = None
            for name in ("HKIPO_WORKBOOK", "HKIPO_PERIOD_START", "HKIPO_PERIOD_END"):
                os.environ.pop(name, None)
        except (OSError, ValueError) as exc:
            ap.error(str(exc))

    try:
        cfg = load_cfg(args.workbook, args.period_start, args.period_end, config_path=args.config)
    except (ValueError, KeyError) as exc:
        ap.error(str(exc))
    os.environ["PIPELINE_CONFIG"] = str(cfg["_config_path"])
    if runtime_override and not generated_cohort:
        os.environ["HKIPO_WORKBOOK"] = str(cfg["_workbook_path"])
        os.environ["HKIPO_PERIOD_START"] = cfg["dataset"]["period_start"]
        os.environ["HKIPO_PERIOD_END"] = cfg["dataset"]["period_end"]
    else:
        for name in ("HKIPO_WORKBOOK", "HKIPO_PERIOD_START", "HKIPO_PERIOD_END"):
            os.environ.pop(name, None)
    if args.stage in ("search", "state"):
        return globals()[f"cmd_{args.stage}"](cfg, args, None)
    companies = read_companies(cfg)
    cfg["dataset"]["expected_companies"] = len(companies)
    print(f"工作簿 {cfg['workbook']} 共 {len(companies)} 家公司")
    if args.only:
        companies = [c for c in companies if c["code"] in args.only]
    if args.limit:
        companies = companies[: args.limit]
    cfg["_selected_codes"] = [c["code"] for c in companies]
    if not companies:
        print("错误: 工作簿中没有符合日期范围的发行人记录。请检查日期范围和工作簿内容。", file=sys.stderr)
        return 1

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
        elif isinstance(result, int):
            rc = result
        if rc:
            break
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
