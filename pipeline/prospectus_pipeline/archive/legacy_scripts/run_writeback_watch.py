#!/usr/bin/env python3
"""自动写回看门狗：只要有 JSON 已齐但还没进 Excel，就自动 validate + write。

每 60 秒轮询一次 auto_fill.py status；发现「待写回Excel > 0」就跑 write-ready。
这一步纯 Python，不花 token。
"""
from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUTO = ROOT / "prospectus_pipeline" / "auto_fill.py"
LOGF = ROOT / "prospectus_pipeline" / "out" / "agy_logs" / "_writeback_watch.log"


def log(msg: str) -> None:
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    with LOGF.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def status() -> str:
    r = subprocess.run([sys.executable, str(AUTO), "status"],
                       cwd=ROOT, capture_output=True, text=True, timeout=180)
    return (r.stdout or "") + (r.stderr or "")


def ready_count(text: str) -> int:
    for line in text.splitlines():
        if "待写回Excel" in line:
            m = re.search(r"待写回Excel\s+(\d+)", line)
            if m:
                return int(m.group(1))
        if "JSON已齐、尚未写进 Excel" in line:
            return 1
    return 0


def main() -> int:
    log("writeback watcher 启动")
    idle = 0
    while True:
        try:
            text = status()
            n = ready_count(text)
            if n:
                log(f"发现 {n} 家待写回，执行 write-ready")
                r = subprocess.run([sys.executable, str(AUTO), "write-ready"],
                                   cwd=ROOT, capture_output=True, text=True, timeout=600)
                tail = (r.stdout or "").strip().splitlines()[-3:]
                log("write-ready: " + " | ".join(tail))
                idle = 0
            else:
                idle += 1
                if idle % 10 == 1:
                    done = re.search(r"招股书进表\s+(\d+)/(\d+)", text)
                    log(f"无待写回；进表 {done.group(0) if done else '?'}")
        except Exception as exc:  # noqa: BLE001
            log(f"watcher 异常：{type(exc).__name__}: {exc}")
        time.sleep(60)


if __name__ == "__main__":
    raise SystemExit(main())
