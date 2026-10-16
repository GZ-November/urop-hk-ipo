"""One writer per cohort output directory, across processes and parallel agents.

Gate commands (validate, state, derive_allot, greenshoe, write, ...) update shared
cohort files such as validation.json, greenshoe.json and cornerstone_absence.json with
read-modify-write cycles. Parallel extraction/review subagents call those commands at
the same time, so every mutating stage runs under this lock. Cohorts that share an
``out/`` directory share the lock. The lock is re-entrant for child processes: the
holder exports HKIPO_COHORT_LOCK so a subprocess it starts (``state`` runs
tools/state.py) does not wait on its own parent.
"""
from __future__ import annotations

import contextlib
import fcntl
import os
import time
from pathlib import Path

ENV = "HKIPO_COHORT_LOCK"


def lock_path(cfg: dict) -> Path:
    return Path(cfg["paths"]["out"]) / ".cohort.lock"


@contextlib.contextmanager
def cohort_lock(cfg: dict, timeout: float = 3600.0, poll: float = 0.25, log=print):
    if not (cfg.get("paths") or {}).get("out"):
        yield None  # no cohort output directory, so no shared cohort files to protect
        return
    path = lock_path(cfg)
    if os.environ.get(ENV) == str(path):
        yield path
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+") as handle:
        start = time.monotonic()
        announced = False
        while True:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                waited = time.monotonic() - start
                if waited >= timeout:
                    raise TimeoutError(f"cohort lock {path} still held after {timeout:.0f}s")
                if not announced and waited >= 2:
                    log(f"Waiting for another pipeline command on this cohort ({path.name})...")
                    announced = True
                time.sleep(poll)
        previous = os.environ.get(ENV)
        os.environ[ENV] = str(path)
        try:
            yield path
        finally:
            if previous is None:
                os.environ.pop(ENV, None)
            else:
                os.environ[ENV] = previous
            fcntl.flock(handle, fcntl.LOCK_UN)
