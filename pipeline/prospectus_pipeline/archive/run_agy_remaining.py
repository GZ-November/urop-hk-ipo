#!/usr/bin/env python3
"""[DEPRECATED] 历史 42 字段旧版 agy runner，已由现代化 run.py 与 workflows/ 替代。

用 agy + gemini-3.8-flash-high 抽剩下的浅蓝 42 字段。
- 默认 2 并发（8 并发上次只连 API 不写文件）
- quota / RESOURCE_EXHAUSTED / rate limit → 睡 5 小时再试
- 某家 JSON 写出且 validate 不是 ERROR 才算完成
- 全部完成后打印写回命令（不自动 write，除非 --write）
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIPE = ROOT / "prospectus_pipeline"
LOGDIR = PIPE / "out" / "agy_logs"
EXT = PIPE / "out" / "extracted"
TPL = (PIPE / "prompts" / "agy_extract.md").read_text(encoding="utf-8")
MODEL = "gemini-3.8-flash-high"
SLEEP_SEC = 5 * 3600
QUOTA_RE = re.compile(
    r"RESOURCE_EXHAUSTED|quota[-_ ]?exceeded|rate[-_ ]?limit|"
    r"(?:tokens?|quota).{0,40}(?:limit|exhausted)|"
    r"\b429\b",
    re.I,
)
# agy 会给出真实恢复时间："Resets in 2h33m16s"。优先按它睡，别死等 5 小时。
RESET_RE = re.compile(r"Resets? in\s*(?:(\d+)\s*h)?\s*(?:(\d+)\s*m)?\s*(?:(\d+)\s*s)?", re.I)


def quota_sleep(text: str) -> int:
    m = RESET_RE.search(text)
    if not m or not any(m.groups()):
        return SLEEP_SEC
    h, mi, s = (int(x or 0) for x in m.groups())
    return max(120, h * 3600 + mi * 60 + s + 90)


def preflight_quota_wait(max_age: int = 2 * 3600) -> int:
    """启动前预检：最近失败日志里若还有未到期的 quota 重置，先睡到那时再动手，
    免得每家都白跑一遍 agy 的 8 次退避重试（约 10 分钟）。"""
    now = time.time()
    best = 0.0
    for p in LOGDIR.glob("*.stdout.log"):
        try:
            st = p.stat()
        except OSError:
            continue
        if now - st.st_mtime > max_age:
            continue
        txt = p.read_text(encoding="utf-8", errors="replace")
        m = RESET_RE.search(txt)
        if not m or not any(m.groups()):
            continue
        h, mi, s = (int(x or 0) for x in m.groups())
        reset_at = st.st_mtime + h * 3600 + mi * 60 + s
        if reset_at > now:
            best = max(best, reset_at)
    return int(best - now) if best else 0


def remaining() -> list[dict]:
    pk = json.loads((PIPE / "out" / "packets.json").read_text(encoding="utf-8"))
    have = set()
    for p in EXT.glob("HKIPO-MB*.json"):
        if not re.fullmatch(r"HKIPO-MB\d{4}\.json", p.name):
            continue
        try:
            rec = json.loads(p.read_text(encoding="utf-8"))
            if set(rec) != {"code", "fields"} or not isinstance(rec["fields"], dict):
                continue
        except (OSError, UnicodeError, json.JSONDecodeError):
            continue
        d = p.stem.replace("HKIPO-MB", "")
        have.add(f"{d}.HK")
    rest = [x for x in pk if x["code"] not in have]
    # 刚失败过的（有 agy log 但没 JSON）放到队尾，避免反复卡住同一家
    def failed_first(rec):
        d = "".join(c for c in rec["code"] if c.isdigit())
        json_ok = (EXT / f"HKIPO-MB{d}.json").exists()
        log = LOGDIR / f"{d}.agy.log"
        return 1 if (not json_ok and log.exists() and log.stat().st_size > 1000) else 0
    rest.sort(key=failed_first)
    return rest


def digits(code: str) -> str:
    return "".join(c for c in code if c.isdigit())


def prompt_for(rec: dict) -> str:
    return (TPL.replace("{{CODE}}", rec["code"])
               .replace("{{NAME}}", rec.get("name") or "")
               .replace("{{PACKET}}", rec["packet_path"])
               .replace("{{OUT}}", rec["out_path"]))


def validate_ok(code: str) -> tuple[bool, str]:
    r = subprocess.run(
        [sys.executable, str(PIPE / "run.py"), "validate", "--only", code],
        cwd=ROOT, capture_output=True, text=True, timeout=180,
    )
    out = (r.stdout or "") + (r.stderr or "")
    if "errors= 0" in out or "errors=0" in out:
        return True, out[-400:]
    return False, out[-800:]


def _mtime(paths) -> float:
    best = 0.0
    for p in paths:
        try:
            best = max(best, p.stat().st_mtime)
        except OSError:
            pass
    return best


def _safe_wait(proc, timeout: int = 15) -> bool:
    try:
        proc.wait(timeout=timeout)
        return True
    except subprocess.TimeoutExpired:
        return False


def _wait_with_watchdog(proc, code: str, logs, stall_sec: int = 240,
                        hard_sec: int = 30 * 60) -> int:
    """agy 的 SSE 流会静默挂住，--print-timeout 拦不住。
    日志 stall_sec 秒没有新活动即判卡死，杀掉换下一家。"""
    start = time.time()
    last = _mtime(logs) or start
    while True:
        rc = proc.poll()
        if rc is not None:
            return rc
        time.sleep(10)
        m = _mtime(logs)
        now = time.time()
        if now - start > hard_sec:
            print(f"TIMEOUT {code}: 超过 {hard_sec // 60} 分钟，杀掉", flush=True)
            proc.kill()
            _safe_wait(proc)
            return -9
        if m > last:
            last = m
            continue
        if now - last > stall_sec:
            print(f"STALL {code}: 日志 {int(now - last)}s 无活动，判卡死，杀掉", flush=True)
            proc.kill()
            _safe_wait(proc)
            return -9


def run_one(rec: dict) -> dict:
    code = rec["code"]
    d = digits(code)
    LOGDIR.mkdir(parents=True, exist_ok=True)
    prompt_path = LOGDIR / f"{d}.prompt.md"
    prompt_path.write_text(prompt_for(rec), encoding="utf-8")
    stdout_path = LOGDIR / f"{d}.stdout.log"
    agy_log = LOGDIR / f"{d}.agy.log"
    out_json = Path(rec["out_path"])

    cmd = [
        "agy",
        "--print-timeout", "45m",
        "--dangerously-skip-permissions",
        "--add-dir", str(ROOT),
        "--model", MODEL,
        "--log-file", str(agy_log),
        "-p", prompt_path.read_text(encoding="utf-8"),
    ]
    print(f"LAUNCH {code}", flush=True)
    with stdout_path.open("w", encoding="utf-8") as fh:
        proc = subprocess.Popen(
            cmd, cwd=ROOT, stdout=fh, stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        rc = _wait_with_watchdog(proc, code, [agy_log, stdout_path])
    text = ""
    for p in (stdout_path, agy_log):
        if p.exists():
            text += p.read_text(encoding="utf-8", errors="replace")
    quota = bool(QUOTA_RE.search(text))
    written = out_json.exists() and out_json.stat().st_size > 200
    ok, vnote = (False, "no json")
    if written:
        ok, vnote = validate_ok(code)
    wait = quota_sleep(text) if quota else SLEEP_SEC
    print(f"DONE {code} rc={rc} json={written} validate_ok={ok} quota={quota}"
          + (f" reset_in={wait}s" if quota else ""), flush=True)
    return {"code": code, "rc": rc, "written": written, "ok": ok,
            "quota": quota, "note": vnote, "sleep": wait}


def main() -> int:
    write_after = "--write" in sys.argv
    jobs = remaining()
    print(f"remaining {len(jobs)}", flush=True)
    if not jobs:
        print("nothing to extract")
        if write_after:
            subprocess.check_call(
                [sys.executable, str(PIPE / "run.py"), "validate"], cwd=ROOT)
            subprocess.check_call(
                [sys.executable, str(PIPE / "run.py"), "write", "--fill-missing"],
                cwd=ROOT)
        return 0

    pending = list(jobs)
    attempts: dict[str, int] = {}
    permanently_failed = []
    while pending:
        rec = pending.pop(0)
        # skip if another process already wrote it
        if Path(rec["out_path"]).exists() and Path(rec["out_path"]).stat().st_size > 200:
            ok, _ = validate_ok(rec["code"])
            if ok:
                print(f"SKIP already ok {rec['code']}", flush=True)
                continue
        res = run_one(rec)
        attempts[rec["code"]] = attempts.get(rec["code"], 0) + 1
        if res["ok"]:
            continue
        if res["quota"]:
            wait = res.get("sleep", SLEEP_SEC)
            print(f"TOKEN/QUOTA hit on {rec['code']}; sleep {wait}s "
                  f"({wait / 3600:.2f}h，按 agy 报的重置时间)", flush=True)
            pending.insert(0, rec)
            time.sleep(wait)
            continue
        if attempts[rec["code"]] >= 3:
            print(f"GIVE UP after 3 attempts {rec['code']}: {res['note'][:200]}", flush=True)
            permanently_failed.append(rec["code"])
            continue
        print(f"RETRY later {rec['code']}: {res['note'][:200]}", flush=True)
        code = rec["code"]
        if sum(1 for x in pending if x["code"] == code) < 1:
            pending.append(rec)

    left = remaining()
    print(f"still missing {len(left)}: {[x['code'] for x in left]}", flush=True)
    print("\nNext:\n  python3 prospectus_pipeline/run.py validate\n"
          "  python3 prospectus_pipeline/run.py write --fill-missing", flush=True)
    if write_after and not left:
        subprocess.check_call(
            [sys.executable, str(PIPE / "run.py"), "validate"], cwd=ROOT)
        subprocess.check_call(
            [sys.executable, str(PIPE / "run.py"), "write", "--fill-missing"],
            cwd=ROOT)
    return 0 if not left and not permanently_failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
