#!/usr/bin/env bash
# ==============================================================================
# HK IPO Pipeline 运行环境与依赖自检/自愈脚本
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../.." && pwd)"
PIPELINE_DIR="${REPO_ROOT}/Data Collecting Pipeline/prospectus_pipeline"
REQ_FILE="${PIPELINE_DIR}/requirements.txt"

echo "=== [1/2] 检查 Python 解释器 ==="
if ! command -v python3 &>/dev/null; then
  echo "❌ 未检测到 python3，请先安装 Python 3.9 或更高版本。"
  exit 1
fi

PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✓ Python 版本: ${PY_VER}"

echo "=== [2/2] 检查核心运行依赖 (openpyxl, pyyaml, requests, pymupdf) ==="
if python3 -c "import openpyxl, yaml, requests, fitz" &>/dev/null; then
  echo "✓ 所有依赖均已安装就绪。"
else
  echo "⚠️  检测到缺失依赖，正在自动自愈安装: ${REQ_FILE} ..."
  if command -v uv &>/dev/null; then
    uv pip install -r "${REQ_FILE}"
  else
    python3 -m pip install -r "${REQ_FILE}"
  fi
  python3 -c "import openpyxl, yaml, requests, fitz"
  echo "✓ 依赖自动补全成功！"
fi

echo "=================================================================="
echo "🎉 HK IPO Pipeline 运行环境准备完毕 (0 Token 确定性引擎就绪)"
echo "=================================================================="
