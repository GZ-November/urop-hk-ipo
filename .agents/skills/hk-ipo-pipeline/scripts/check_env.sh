#!/usr/bin/env bash
# ==============================================================================
# HK IPO Pipeline 运行环境与依赖自检/自愈脚本
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../.." && pwd)"
PIPELINE_DIR="${REPO_ROOT}/Data Collecting Pipeline/prospectus_pipeline"
REQ_FILE="${PIPELINE_DIR}/requirements.txt"

if [[ -z "${PYTHON_BIN:-}" ]]; then
  if [[ -x "${REPO_ROOT}/.venv/bin/python" ]]; then
    PYTHON_BIN="${REPO_ROOT}/.venv/bin/python"
  elif [[ -x "${REPO_ROOT}/Data Collecting Pipeline/.venv/bin/python" ]]; then
    PYTHON_BIN="${REPO_ROOT}/Data Collecting Pipeline/.venv/bin/python"
  elif command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
  else
    echo "❌ 未检测到 Python，请先安装 Python 3.9 或更高版本。"
    exit 1
  fi
fi

echo "=== [1/2] 检查 Python 解释器 ==="
if [[ ! -x "${PYTHON_BIN}" ]] && ! command -v "${PYTHON_BIN}" &>/dev/null; then
  echo "❌ 未检测到 Python 解释器: ${PYTHON_BIN}"
  exit 1
fi

PY_VER=$("${PYTHON_BIN}" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✓ Python 解释器: ${PYTHON_BIN} (${PY_VER})"

echo "=== [2/2] 检查核心运行依赖 (openpyxl, pyyaml, requests, pymupdf) ==="
if "${PYTHON_BIN}" -c "import openpyxl, yaml, requests, fitz" &>/dev/null; then
  echo "✓ 所有依赖均已安装就绪。"
else
  echo "⚠️  检测到缺失依赖，正在自动自愈安装: ${REQ_FILE} ..."
  "${PYTHON_BIN}" -m pip install -r "${REQ_FILE}"
  "${PYTHON_BIN}" -c "import openpyxl, yaml, requests, fitz"
  echo "✓ 依赖自动补全成功！"
fi

echo "=================================================================="
echo "🎉 HK IPO Pipeline 运行环境准备完毕 (0 Token 确定性引擎就绪)"
echo "=================================================================="
