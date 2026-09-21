#!/usr/bin/env python3
"""生成 2026 Q1 Pre-IPO VC/PE 学术研究细分维度全景分析报告。"""
from __future__ import annotations

from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parent.parent
WS = ROOT.parent
out_report = ROOT / "out" / "HKIPO_VC_PE_Research_Report.md"

wb = openpyxl.load_workbook(WS / "HKIPO-MB2026Q1.xlsx", data_only=True)
ws = wb["NLR"]

rows = []
for r in range(2, 40):
    code = ws.cell(r, 2).value
    name = ws.cell(r, 3).value
    name_cn = ws.cell(r, 130).value
    ba = ws.cell(r, 53).value
    vc = ws.cell(r, 54).value
    pe = ws.cell(r, 55).value
    cvc = ws.cell(r, 56).value
    gov = ws.cell(r, 57).value
    top = ws.cell(r, 58).value
    investors = ws.cell(r, 59).value
    stake = ws.cell(r, 60).value
    board = ws.cell(r, 61).value
    round_name = ws.cell(r, 62).value
    duration = ws.cell(r, 63).value
    rows.append({
        "code": code,
        "name": name,
        "name_cn": name_cn,
        "ba": ba,
        "vc": vc,
        "pe": pe,
        "cvc": cvc,
        "gov": gov,
        "top": top,
        "investors": investors,
        "stake": stake,
        "board": board,
        "round": round_name,
        "duration": duration,
    })

total = len(rows)
vc_cnt = sum(1 for r in rows if r["vc"] == 1)
pe_cnt = sum(1 for r in rows if r["pe"] == 1)
cvc_cnt = sum(1 for r in rows if r["cvc"] == 1)
gov_cnt = sum(1 for r in rows if r["gov"] == 1)
top_cnt = sum(1 for r in rows if r["top"] == 1)
board_cnt = sum(1 for r in rows if r["board"] == 1)
backed_cnt = sum(1 for r in rows if r["ba"] == 1)

backed_stakes = [r["stake"] for r in rows if r["ba"] == 1 and isinstance(r["stake"], (int, float))]
avg_stake = sum(backed_stakes) / len(backed_stakes) if backed_stakes else 0.0

backed_durations = [r["duration"] for r in rows if r["ba"] == 1 and isinstance(r["duration"], (int, float))]
avg_duration = sum(backed_durations) / len(backed_durations) if backed_durations else 0.0

md = [
    "# 香港主板 2026 Q1 IPO Pre-IPO VC/PE 学术研究细分维度全景报告",
    "",
    "> **计量数据源**：`HKIPO-MB2026Q1.xlsx` (Sheet: `NLR`, 列 53~63)",
    f"> **样本范围**：2026 年第一季度香港联交所主板新上市企业全集 (N = {total})",
    "> **理论支撑**：Lowry, Michaely, & Volkova (2017) Intermediary Governance; Gompers (1996) Grandstanding; Megginson & Weiss (1991) Certification.",
    "",
    "---",
    "",
    "## 一、核心实证统计量总览 (Executive Summary)",
    "",
    "| 维度指标 | 变量字段 | 覆盖家数 | 样本占比 (%) | 经典文献与实证用途 |",
    "| :--- | :--- | :---: | :---: | :--- |",
    f"| **Pre-IPO 机构总覆盖** | `col_BA` | {backed_cnt} / {total} | {backed_cnt/total*100:.1f}% | 传统基础哑变量（Base VC/PE Dummy） |",
    f"| **早期风险投资 (VC)** | `col_vc_backed` | {vc_cnt} / {total} | {vc_cnt/total*100:.1f}% | 检验早期创业孵化与高成长筛选机制 |",
    f"| **私募股权基金 (PE)** | `col_pe_backed` | {pe_cnt} / {total} | {pe_cnt/total*100:.1f}% | 检验成熟期/并购重组基金的资本赋能与交叉融资 |",
    f"| **产业资本/企业创投 (CVC)** | `col_cvc_backed` | {cvc_cnt} / {total} | {cvc_cnt/total*100:.1f}% | 检验战略协同、生态绑定与上下游订单支持效应 |",
    f"| **国资/产业引导基金 (Gov)** | `col_gov_backed` | {gov_cnt} / {total} | {gov_cnt/total*100:.1f}% | 检验地方政府招商、硬科技政策支持与制度背书 |",
    f"| **顶级机构认证 (Top-tier)** | `col_top_tier_vc` | {top_cnt} / {total} | {top_cnt/total*100:.1f}% | 检验 Megginson & Weiss (1991) 声誉认证假说 |",
    f"| **董事会席位派驻 (Board Seat)** | `col_vc_board_seat` | {board_cnt} / {total} | {board_cnt/total*100:.1f}% | 检验 Sørensen (2007) 积极监控与公司治理赋能 |",
    f"| **上市前机构平均持股比例** | `col_vc_pe_stake` | 均值 {avg_stake*100:.1f}% | - | 衡量投资人股权集中度与信息不对称折价 |",
    f"| **平均持有投资年限 (久期)** | `col_holding_duration` | 均值 {avg_duration:.2f} 年 | - | 检验 Gompers (1996) 基金急迫退出与立名造势假说 |",
    "",
    "---",
    "",
    "## 二、38 家公司 10 大细分维度完整对账清单",
    "",
    "| 股票代码 | 公司名称 (中文) | VC/PE | VC | PE | CVC | 国资 | 顶级 | 董事席位 | 最早轮次 | 持有年限 | 机构持股(%) | 核心机构投资者清单 |",
    "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |",
]

for r in rows:
    stk_str = f"{r['stake']*100:.1f}%" if isinstance(r["stake"], (int, float)) and r["stake"] > 0 else "0.0%"
    dur_str = f"{r['duration']:.2f}" if isinstance(r["duration"], (int, float)) and r["duration"] > 0 else "0.00"
    md.append(
        f"| `{r['code']}` | {r['name_cn']} | {r['ba']} | {r['vc']} | {r['pe']} | {r['cvc']} | {r['gov']} | {r['top']} | {r['board']} | {r['round']} | {dur_str} | {stk_str} | {r['investors']} |"
    )

out_report.write_text("\n".join(md), encoding="utf-8")
print("Successfully generated research report:", out_report)
