#!/usr/bin/env bash
# ==============================================================================
# HK IPO Pipeline 通用命令行转发入口（任意目录均可直接调用）
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../.." && pwd)"
PIPELINE_DIR="${REPO_ROOT}/Data Collecting Pipeline"

cd "${PIPELINE_DIR}"
exec python3 prospectus_pipeline/run.py "$@"
