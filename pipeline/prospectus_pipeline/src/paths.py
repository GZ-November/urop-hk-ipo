#!/usr/bin/env python3
"""pipeline 布局的唯一事实来源（layout adapter）。

子目录名、工件文件名、根路径引导只在本 module 定义一次；
其他 module 一律 import，不得自行拼写目录字符串。
本周的目录重组（b1acb92/94a4ba0）曾因布局知识散在 6+ 个文件而连改两轮，
本 module 即那次教训的固化。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent   # prospectus_pipeline/
WS = ROOT.parent                                 # pipeline/（工作簿与工件根目录）

# 工件子目录
COHORTS = "cohorts"        # 工作簿（版本控制）
EXPORTS = "exports"        # clean CSV + master 面板（本地）
CODEBOOKS = "codebooks"    # 季度变量代码本（版本控制）
REGISTRY = "registry"      # 变量注册表（版本控制）
REPORTS = "reports"        # 漂移报告、筛选日志、诊断/复核、证据清单（版本控制）
SOURCES = "sources"        # 官方 NLR 年报缓存（本地）

# 工件文件名
MASTER_STEM = "HKIPO-MB-MASTER"
REGISTRY_NAME = "HKIPO_Variable_Registry.yaml"
EVIDENCE_NAME = "HKIPO-Evidence_SHA256.txt"


def cohorts_dir(ws: Path = WS) -> Path:
    return ws / COHORTS


def exports_dir(ws: Path = WS) -> Path:
    return ws / EXPORTS


def codebooks_dir(ws: Path = WS) -> Path:
    return ws / CODEBOOKS


def reports_dir(ws: Path = WS) -> Path:
    return ws / REPORTS


def sources_dir(ws: Path = WS) -> Path:
    return ws / SOURCES


def registry_path(ws: Path = WS) -> Path:
    return ws / REGISTRY / REGISTRY_NAME


def cohort_csv_path(ws: Path, tag: str) -> Path:
    """exports/HKIPO-MB{tag}_clean.csv"""
    return ws / EXPORTS / f"HKIPO-MB{tag}_clean.csv"


def codebook_md_path(ws: Path, tag: str) -> Path:
    """codebooks/HKIPO_{tag}_Codebook.md"""
    return ws / CODEBOOKS / f"HKIPO_{tag}_Codebook.md"


def master_csv_path(ws: Path = WS, stem: str = MASTER_STEM) -> Path:
    return ws / EXPORTS / f"{stem}_clean.csv"


def drift_report_path(ws: Path = WS, stem: str = MASTER_STEM) -> Path:
    return ws / REPORTS / f"{stem}_Drift_Report.md"


def exclusions_path(ws: Path, tag: str) -> Path:
    """reports/HKIPO_{tag}_Exclusions.md（tag 形如 2026Q3）"""
    return ws / REPORTS / f"HKIPO_{tag}_Exclusions.md"


def evidence_path(ws: Path = WS) -> Path:
    return ws / REPORTS / EVIDENCE_NAME
