"""Describe the observed 2026 IPO sample before selecting a research question.

Run: python3 analysis/basic_statistics_2026.py
Outputs: analysis/out/basic_statistics/ (coverage, summaries, groups, correlations).
No regressions or hypothesis tests; coverage means stored values, not verified evidence.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from research_inputs import C, MASTER, ROOT, load_panel, select_2026
from shared.reporting import to_markdown

OUT = ROOT / "analysis/out/basic_statistics"
AS_OF = pd.Timestamp("2026-09-30")


def markdown(frame: pd.DataFrame) -> str:
    return to_markdown(frame.round(3).set_index(frame.columns[0]), str(frame.columns[0]))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sample = select_2026(load_panel())
    sample = sample[sample.listing_date <= AS_OF].copy()
    registry_path = ROOT / "pipeline/registry/HKIPO_Variable_Registry.yaml"
    registry = yaml.safe_load(registry_path.read_text())
    coverage = []
    for variable in registry["variables"]:
        field = variable["header"]
        values = sample[field]
        row = {"field": field, "dtype": variable["dtype"], "n_population": len(sample),
               "n_present": int(values.notna().sum()), "n_missing": int(values.isna().sum()),
               "n_distinct": int(values.nunique())}
        for cohort, part in sample.groupby("cohort"):
            row[f"{cohort}_present"] = int(part[field].notna().sum())
        coverage.append(row)
    coverage = pd.DataFrame(coverage)
    coverage.to_csv(OUT / "field_coverage.csv", index=False)

    ratio = sample["Final public offer shares"] / sample["Public valid applied shares"].where(sample["Public valid applied shares"] > 0)
    allocation = ratio.where(ratio.gt(0) & ratio.le(1))
    frame = pd.DataFrame({
        "code": sample["Stock Code"], "quarter": sample["cohort"], "month": sample["month"].astype(str),
        "route": sample["route"], "ir_pct": 100 * sample["ir"], "base_proceeds_hkd_mn": sample["base_proceeds"] / 1e6,
        "subscription_x": sample[C["sub"]], "applicants": sample["Public applicants"],
        "age_years": sample[C["age"]], "cornerstone_pct": 100 * sample[C["corner"]],
        "allocation_pct": 100 * allocation, "application_gross_return_pct": 100 * allocation * sample["ir"],
    })
    frame["demand_group"] = pd.qcut(frame["subscription_x"], 3, labels=["Low demand", "Middle demand", "High demand"])
    frame.to_csv(OUT / "sample.csv", index=False)
    units = {"ir_pct": "首日收益（%）", "base_proceeds_hkd_mn": "基础发售金额（百万港元）",
             "subscription_x": "公开认购倍数（倍）", "applicants": "申请人数（人）", "age_years": "企业年龄（年）",
             "cornerstone_pct": "基石份额（%）", "allocation_pct": "发行人平均配售率（%）",
             "application_gross_return_pct": "申请资金毛收益（%，发行人平均配售情景）"}
    summary = frame[list(units)].describe(percentiles=[.25, .5, .75]).T.reset_index(names="variable")
    summary["variable"] = summary["variable"].map(units)
    summary.to_csv(OUT / "summary.csv", index=False)

    tables = []
    for group in ["quarter", "month", "route", "demand_group"]:
        rows = []
        for name, part in frame.groupby(group, observed=True):
            ir = part["ir_pct"].dropna()
            rows.append({"grouping": group, "group": str(name), "issuer_n": len(part), "ir_n": len(ir),
                         "mean_ir_pct": ir.mean(), "median_ir_pct": ir.median(),
                         "break_share_pct": 100 * ir.lt(0).mean(), "median_subscription_x": part["subscription_x"].median(),
                         "median_base_proceeds_hkd_mn": part["base_proceeds_hkd_mn"].median(),
                         "application_return_n": int(part["application_gross_return_pct"].notna().sum()),
                         "mean_application_gross_return_pct": part["application_gross_return_pct"].mean()})
        tables.append(pd.DataFrame(rows))
    groups = pd.concat(tables, ignore_index=True)
    groups.to_csv(OUT / "group_comparisons.csv", index=False)

    correlations = []
    for variable in ["subscription_x", "applicants", "base_proceeds_hkd_mn", "age_years", "cornerstone_pct"]:
        pair = frame[["ir_pct", variable]].replace([np.inf, -np.inf], np.nan).dropna()
        correlations.append({"variable": units[variable], "pair_n": len(pair),
                             "spearman_with_ir": pair["ir_pct"].corr(pair[variable], method="spearman")})
    correlations = pd.DataFrame(correlations)
    correlations.to_csv(OUT / "correlations.csv", index=False)

    core_fields = [C[k] for k in ("ir", "offer", "sub", "age", "corner", "vc", "float", "profit_y1")]
    core_fields += ["Industry classification code", "Public applicants", "Public valid applied shares", "Final public offer shares",
                    "Pricing date", "First trading day turnover (HK$)", "Day-5 BHR from Day-1 close (%)",
                    "Day-20 BHR from Day-1 close (%)", "3-month BHR from Day-1 close (%)", "6-month BHR from Day-1 close (%)"]
    selected = coverage[coverage.field.isin(core_fields)][["field", "n_present", "n_missing"]]
    missing_rows = [{"field": field, "code": row["Stock Code"], "cohort": row["cohort"]}
                    for field in core_fields for _, row in sample.loc[sample[field].isna()].iterrows()]
    pd.DataFrame(missing_rows, columns=["field", "code", "cohort"]).to_csv(OUT / "core_missing_records.csv", index=False)
    report = f"""# 2026 IPO基础统计与数据覆盖

生成样本：{len(sample)}家，上市日期{sample.listing_date.min().date()}至{sample.listing_date.max().date()}；截至{AS_OF.date()}。仅使用2026主板普通IPO。
此报告只做描述和相关性，不运行回归或显著性检验。原始价格和当前单位修复沿用现有研究输入。

## 1. 核心字段覆盖

{markdown(selected)}

覆盖表示master中有值，不证明原始披露已独立核实。完整202字段清单见field_coverage.csv；核心字段缺失发行人见core_missing_records.csv。
固定价格发售不适用区间修价；未成熟收益、未披露、未采集和不适用必须分别判断，不能将缺失全部补0。
基础发售金额=P0×基础发售证券数量，单位沿用当前发行股份／HDR修复；不等同于含绿鞋募资或发行人净所得。

## 2. 描述统计

{markdown(summary)}

申请资金毛收益=发行人平均配售率×首日收益；这是比例获配情景，不是一手中签率、实际账户收益或扣费净收益。
超过1或非正的配售率保留缺失，不截为1。用均值与中位数共同观察极端值，不能只报平均收益。

## 3. 季度与上市路径

{markdown(groups.loc[groups.grouping.isin(['quarter', 'route']), ['group', 'ir_n', 'mean_ir_pct', 'median_ir_pct', 'break_share_pct']])}

路径按18A、18C、A+H、普通路径互斥归类；独立A+H标记可以与18C重叠。月份完整表见group_comparisons.csv。
每个单元格的收益样本数单列；很小的组只描述，不据此概括总体。

## 4. 认购热度三等分

{markdown(groups.loc[groups.grouping.eq('demand_group'), ['group', 'ir_n', 'mean_ir_pct', 'median_ir_pct', 'break_share_pct', 'mean_application_gross_return_pct']])}

三组由当前样本的认购倍数分位点划分，不是外部制度阈值。差异可能同时来自规模、上市月份及上市路径。

## 5. 与首日收益的简单秩相关

{markdown(correlations)}

Spearman系数只表示排名关系，不能解释为因果效应。每对变量使用自身有限样本，不与回归共同样本混用。

## 6. 下一步

先检查分布、分组和异常发行人，再深入认购热度与零售获配收益。A+H锚专题可作为独立的小样本方向。
缺什么数据、哪些公开可得及近期不做的选题见docs/RESEARCH_PLAN_2026.md；具体采集表见docs/DATA_GAPS_2026.md。
"""
    (OUT / "basic_statistics.md").write_text(report, encoding="utf-8")
    manifest = {"as_of": str(AS_OF.date()), "sample_n": len(sample), "registered_fields": len(coverage),
                "inputs": {str(MASTER.relative_to(ROOT)): hashlib.sha256(MASTER.read_bytes()).hexdigest(),
                           "analysis/basic_statistics_2026.py": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                           str(registry_path.relative_to(ROOT)): hashlib.sha256(registry_path.read_bytes()).hexdigest()},
                "pandas_version": pd.__version__}
    (OUT / "run_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n")
    print(f"Basic statistics written: {len(sample)} issuers, {len(coverage)} registered fields")


if __name__ == "__main__":
    main()
