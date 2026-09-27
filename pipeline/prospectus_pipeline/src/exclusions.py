#!/usr/bin/env python3
"""样本筛选日志：持久化每个 cohort 的发行人纳入/剔除法定原因。

学术规范要求样本构建可复现：官方 NLR 名单中每个未进入工作簿的发行人，
都要有法定排除原因（GEM 转板 / SPAC / 介绍上市等，见 sample_builder.audit_candidate）；
每个 INCLUDED 但缺失于工作簿的发行人是采集缺口警告。

产出 `HKIPO_{tag}_Exclusions.md`（版本控制），由 `python3 run.py exclusions
--config prospectus_pipeline/config_YYYYqN.yaml` 按 cohort 生成。
"""
from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
WS = ROOT.parent
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from cohort import _membership_date  # noqa: E402
from listing_reports import reports_for_interval  # noqa: E402
from sample_builder import audit_candidate, load_nlr_candidates  # noqa: E402


def _official_candidates(cfg: dict, start: dt.date, end: dt.date) -> list[dict[str, Any]]:
    """从本地缓存的官方 NLR 报告加载区间内的候选发行人并做法定审计。"""
    from paths import sources_dir as layout_sources_dir
    source_dir = Path(cfg["dataset"].get("report_source_dir") or layout_sources_dir(WS))
    candidates: list[dict[str, Any]] = []
    for report in reports_for_interval(start, end, source_dir):
        match = re.search(r"(?:NLR)?(19\d{2}|20\d{2})", report.stem, re.I)
        if not match:
            raise ValueError(f"Cannot identify annual report year: {report.name}")
        for candidate in load_nlr_candidates(report, int(match.group(1))):
            candidates.append(audit_candidate(candidate))
    return candidates


def _workbook_codes(cfg: dict) -> set[str]:
    import openpyxl

    workbook_path = Path(cfg["_workbook_path"])
    workbook = openpyxl.load_workbook(workbook_path, read_only=True, data_only=True)
    try:
        rows = workbook[cfg["sheet"]].iter_rows(min_row=2, min_col=2, max_col=2, values_only=True)
        return {str(row[0]).strip() for row in rows if row[0] not in (None, "")}
    finally:
        workbook.close()


def build_exclusion_log(
    cfg: dict,
    candidates: list[dict[str, Any]] | None = None,
    out_path: Path | None = None,
) -> tuple[Path, dict[str, Any]]:
    """生成单个 cohort 的样本筛选日志；返回 (md 路径, 摘要统计)。"""
    start = dt.date.fromisoformat(cfg["dataset"]["period_start"])
    end = dt.date.fromisoformat(cfg["dataset"]["period_end"])
    tag = str(cfg["dataset"].get("cohort", "cohort")).replace(" ", "")
    if candidates is None:
        candidates = _official_candidates(cfg, start, end)

    included: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    for cand in candidates:
        membership = _membership_date(cand)
        if isinstance(membership, dt.datetime):
            membership = membership.date()
        if membership is None or not isinstance(membership, dt.date):
            continue
        if not (start <= membership <= end):
            continue
        if cand.get("inclusion_status") == "INCLUDED":
            included.append(cand)
        else:
            excluded.append(cand)

    codes = _workbook_codes(cfg)
    included_codes = [c["stock_code"] for c in included]
    missing_from_workbook = sorted(set(included_codes) - codes)
    unexpected_in_workbook = sorted(codes - set(included_codes))

    def _date(value: Any) -> str:
        if isinstance(value, dt.datetime):
            return value.date().isoformat()
        if isinstance(value, dt.date):
            return value.isoformat()
        return str(value or "未知")

    lines = [f"# {tag} 样本筛选日志（Sample Selection Log）", ""]
    lines.append(f"- **生成时间**：{dt.datetime.now().isoformat(timespec='seconds')} | "
                 f"**区间**：{start.isoformat()} ~ {end.isoformat()} | "
                 f"**官方候选**：{len(included) + len(excluded)} 家")
    lines.append(f"- **复现命令**：`python3 run.py exclusions --config prospectus_pipeline/config_{tag.lower()}.yaml`")
    lines.append(f"- **纳入**：{len(included)} 家 | **剔除**：{len(excluded)} 家 | "
                 f"**工作簿**：{len(codes)} 家")
    lines.append("")

    lines.append("## 1. 纳入样本（Ordinary Main Board IPO）")
    lines.append("")
    lines.append("| 股票代码 | 公司名称 | 上市日期 | 是否在工作簿 |")
    lines.append("|---|---|---|---|")
    for cand in included:
        in_book = "✅" if cand["stock_code"] in codes else "❌ 缺失"
        lines.append(f"| {cand['stock_code']} | {cand['company_name']} | "
                     f"{_date(cand.get('listing_date'))} | {in_book} |")
    lines.append("")

    lines.append("## 2. 剔除样本及法定原因")
    lines.append("")
    if excluded:
        lines.append("| 股票代码 | 公司名称 | 上市日期 | 上市路径 | 剔除原因 |")
        lines.append("|---|---|---|---|---|")
        for cand in excluded:
            lines.append(f"| {cand['stock_code']} | {cand['company_name']} | "
                         f"{_date(cand.get('listing_date'))} | {cand.get('listing_route', '未知')} | "
                         f"{cand.get('exclusion_reason', '未知')} |")
    else:
        lines.append("本区间无剔除发行人。")
    lines.append("")

    lines.append("## 3. 一致性警告")
    lines.append("")
    if missing_from_workbook:
        lines.append(f"- **❌ 官方名单判定纳入、但工作簿缺失**：{', '.join(missing_from_workbook)}")
    else:
        lines.append("- ✅ 官方名单判定的纳入样本与工作簿一致。")
    if unexpected_in_workbook:
        lines.append(f"- **⚠️ 工作簿中有、但官方名单未判定纳入**：{', '.join(unexpected_in_workbook)}")
    lines.append("")

    summary = {
        "cohort": tag,
        "included": len(included),
        "excluded": len(excluded),
        "workbook": len(codes),
        "missing_from_workbook": missing_from_workbook,
        "unexpected_in_workbook": unexpected_in_workbook,
    }
    if out_path is None:
        from paths import exclusions_path as layout_exclusions_path
        out_path = layout_exclusions_path(WS, tag)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path, summary
