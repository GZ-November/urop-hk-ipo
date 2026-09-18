"""Atomic JSON storage and strict extraction filename discovery."""
import fcntl
import json
import os
import re
import tempfile
from pathlib import Path

from contracts import normalize_code


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix="." + path.name, dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(value, fh, ensure_ascii=False, indent=2, allow_nan=False)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def official_files(directory, only=None, limit=0):
    wanted = {normalize_code(c) for c in only} if only is not None else None
    result = {}
    for path in sorted(Path(directory).glob("*.json")):
        match = re.fullmatch(r"HKIPO-MB(\d{4})\.json", path.name)
        if match:
            code = match.group(1) + ".HK"
            if wanted is None or code in wanted:
                result[code] = path
    return dict(list(result.items())[:limit]) if limit else result


def merge_index(path, updates):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.with_suffix(path.suffix + ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
        rows = {normalize_code(row["code"]): row for row in old}
        rows.update({normalize_code(row["code"]): row for row in updates})
        atomic_json(path, list(rows.values()))
