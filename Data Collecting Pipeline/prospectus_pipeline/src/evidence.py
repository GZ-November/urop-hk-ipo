#!/usr/bin/env python3
"""审计凭证归档：为研究数据工件生成 SHA-256 证据清单。

对 WS 根目录的 cohort 工作簿、clean CSV、Codebook、变量注册表、master 面板
与漂移报告逐一计算 SHA-256，写入 HKIPO-Evidence_SHA256.txt（版本控制）。

用法：cohort 关闭（采集 + 复核 + 导出完成）后运行 `python3 run.py evidence`，
把当时的清单快照提交版本控制；此后任何工件被改动都会导致清单失配，
保证每个单元格可追溯到采集时点的原始 PDF 与复核凭证。
"""
from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WS = ROOT.parent
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

from storage import file_sha256  # noqa: E402

EVIDENCE_NAME = "HKIPO-Evidence_SHA256.txt"

# 覆盖顺序：工作簿 -> 导出物 -> 注册表 -> master 面板与漂移报告
PATTERNS = [
    "HKIPO-MB[0-9]*.xlsx",
    "HKIPO-MB[0-9]*_clean.csv",
    "HKIPO_*_Codebook.md",
    "HKIPO_Variable_Registry.yaml",
    "HKIPO-MB-MASTER_clean.csv",
    "HKIPO-MB-MASTER_Drift_Report.md",
    "HKIPO_*_Exclusions.md",
]


def build_evidence_manifest(ws: Path | None = None) -> tuple[Path, list[tuple[str, str]]]:
    """计算全部数据工件哈希并写入清单文件；返回 (清单路径, 条目列表)。"""
    ws = Path(ws) if ws else WS
    seen: set[Path] = set()
    entries: list[tuple[str, str]] = []
    for pattern in PATTERNS:
        for path in sorted(ws.glob(pattern)):
            if path in seen or not path.is_file():
                continue
            seen.add(path)
            entries.append((path.name, file_sha256(path)))
    entries.sort(key=lambda e: e[0])

    out_path = ws / EVIDENCE_NAME
    lines = [
        "# HK IPO 研究数据 SHA-256 证据清单",
        f"# 生成时间: {dt.datetime.now().isoformat(timespec='seconds')}",
        f"# 文件数: {len(entries)}",
        "# 复现命令: python3 run.py evidence",
        "#",
        "# 用途: cohort 关闭后冻结凭证快照并纳入版本控制；",
        "#       之后工件一旦被改动，哈希即失配，用于保证数据可追溯到采集时点。",
        *[f"{digest}  {name}" for name, digest in entries],
    ]
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out_path, entries
