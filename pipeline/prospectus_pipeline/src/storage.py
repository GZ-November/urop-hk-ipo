from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path

from contracts import normalize_code


def file_sha256(path: Path | str) -> str:
    """计算文件的 SHA-256 哈希值，用于数字证据链溯源与防篡改。"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1 << 16):
            h.update(chunk)
    return h.hexdigest()


def create_http_session(retries: int = 3, backoff_factor: float = 0.5) -> "requests.Session":
    """创建具备指数退避重试机制与状态码容错的 HTTP 会话。"""
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util import Retry

    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


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
