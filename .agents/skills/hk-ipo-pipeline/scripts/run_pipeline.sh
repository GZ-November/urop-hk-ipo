#!/usr/bin/env bash
# ==============================================================================
# HK IPO Pipeline 通用命令行转发入口（任意目录均可直接调用）
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../.." && pwd)"
PIPELINE_DIR="${REPO_ROOT}/Data Collecting Pipeline"

if [[ -z "${PYTHON_BIN:-}" ]]; then
  if [[ -x "${REPO_ROOT}/.venv/bin/python" ]]; then
    PYTHON_BIN="${REPO_ROOT}/.venv/bin/python"
  elif [[ -x "${PIPELINE_DIR}/.venv/bin/python" ]]; then
    PYTHON_BIN="${PIPELINE_DIR}/.venv/bin/python"
  else
    PYTHON_BIN="python3"
  fi
fi

cd "${PIPELINE_DIR}"
exec "${PYTHON_BIN}" prospectus_pipeline/run.py "$@"
