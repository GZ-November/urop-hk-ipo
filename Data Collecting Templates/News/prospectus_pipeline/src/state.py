"""Hash-bound extracted -> validated -> reviewed -> written credentials."""
import hashlib
import json
import os
import re
from pathlib import Path

from contracts import normalize_code, strict_load_file
from storage import atomic_json

CONTRACT_VERSION = "2026-09-13-v2"


def digest(rec, schema, evidence):
    blob = json.dumps([CONTRACT_VERSION, rec, schema, evidence], sort_keys=True,
                      ensure_ascii=False, allow_nan=False, default=str).encode()
    return hashlib.sha256(blob).hexdigest()


def file_hash(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


def state_dir(cfg):
    return Path(cfg.get("state_dir") or os.environ.get("PIPELINE_STATE_DIR")
                or cfg["_root"] / ".pipeline_state")


def record_path(cfg, target, code, stage):
    code = normalize_code(code)
    if not re.fullmatch(r"\d{4}\.HK", code):
        raise ValueError("invalid official stock code")
    return state_dir(cfg) / target / stage / (code + ".json")


def save_record(cfg, target, code, stage, record):
    atomic_json(record_path(cfg, target, code, stage), {**record, "stage": stage})


def read_record(cfg, target, code, stage):
    try:
        return strict_load_file(record_path(cfg, target, code, stage))
    except (OSError, ValueError):
        return {}


def require(cfg, target, code, version, stage):
    record = read_record(cfg, target, code, stage)
    ok = (record.get("code") == normalize_code(code) and record.get("target") == target
          and record.get("hash") == version and record.get("gate_pass") is True)
    if not ok:
        raise ValueError(f"{code}: missing/failed {stage} record or hash mismatch")
    return record


def authorized(cfg, code, target, current):
    if current.get("status") not in {"pass", "warning_missing"}:
        raise ValueError(f"{code}: snapshot validation failed: {current.get('errors', [])}")
    for stage in ("extracted", "validated", "reviewed"):
        require(cfg, target, code, current.get("hash"), stage)
