"""Centralized, ACID-compliant, concurrency-safe Workbook Transaction Manager.

Features:
  1. Exclusive file locking via fcntl.flock to serialize all workbook writers.
  2. Collision-resistant timestamped backup snapshots before mutation.
  3. Atomic file replacement via temporary file on same filesystem + os.replace.
  4. Post-write integrity check (verifies valid ZIP / openpyxl readable structure).
  5. Automatic rollback on exception (temporary file discarded, locks released).
"""
from __future__ import annotations

import contextlib
import datetime as dt
import fcntl
import os
import shutil
import tempfile
import time
import uuid
import zipfile
from pathlib import Path
from typing import Generator

import openpyxl

from storage import file_sha256


class WorkbookLockError(Exception):
    """Raised when the workbook lock cannot be acquired."""


class WorkbookIntegrityError(Exception):
    """Raised when the written workbook fails post-write validation."""


def _acquire_lock(lock_path: Path, timeout: float = 30.0) -> int:
    """Acquire an exclusive lock on lock_path with timeout."""
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(str(lock_path), os.O_CREAT | os.O_RDWR)
    deadline = time.time() + timeout
    while True:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return fd
        except (BlockingIOError, OSError):
            if time.time() >= deadline:
                os.close(fd)
                raise WorkbookLockError(
                    f"Timed out waiting for workbook lock: {lock_path} ({timeout}s)"
                )
            time.sleep(0.1)


def _release_lock(fd: int, lock_path: Path) -> None:
    try:
        fcntl.flock(fd, fcntl.LOCK_UN)
    finally:
        os.close(fd)


def create_snapshot_backup(book_path: Path, operation: str = "backup") -> Path:
    """Create a collision-resistant timestamped backup snapshot."""
    snapshots_dir = book_path.parent / "backups" / "excel_snapshots"
    snapshots_dir.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    rand_suffix = uuid.uuid4().hex[:6]
    backup_name = f"{book_path.stem}.backup-{operation}-{ts}-{rand_suffix}.xlsx"
    backup_path = snapshots_dir / backup_name
    shutil.copy2(book_path, backup_path)
    return backup_path


def verify_workbook_file(file_path: Path) -> None:
    """Verify that file is a non-empty, valid, readable openpyxl/zip archive."""
    if not file_path.exists() or file_path.stat().st_size == 0:
        raise WorkbookIntegrityError(f"Workbook file is empty or missing: {file_path}")
    if not zipfile.is_zipfile(file_path):
        raise WorkbookIntegrityError(f"Workbook file is corrupted (not valid zip): {file_path}")
    # Quick open check
    try:
        wb = openpyxl.load_workbook(file_path, read_only=True)
        wb.close()
    except Exception as exc:
        raise WorkbookIntegrityError(f"Workbook failed openpyxl structure validation: {exc}") from exc


@contextlib.contextmanager
def workbook_transaction(
    book_path: Path,
    operation: str = "write",
    dry_run: bool = False,
    timeout: float = 30.0,
) -> Generator[openpyxl.Workbook, None, None]:
    """Exclusive, transactional context manager for mutating openpyxl workbooks.

    Usage:
        with workbook_transaction(book_path, operation="market") as wb:
            ws = wb["NLR"]
            ws.cell(row, col).value = val
            # Changes are automatically committed atomically on exit!
    """
    book_path = Path(book_path).resolve()
    if not book_path.exists():
        raise FileNotFoundError(f"Workbook not found: {book_path}")

    lock_file = book_path.with_name(f".{book_path.name}.lock")
    lock_fd = _acquire_lock(lock_file, timeout=timeout)

    backup_path: Path | None = None
    wb: openpyxl.Workbook | None = None
    tmp_path: Path | None = None

    try:
        if not dry_run:
            backup_path = create_snapshot_backup(book_path, operation=operation)

        wb = openpyxl.load_workbook(book_path)
        yield wb

        if dry_run:
            wb.close()
            return

        # Atomic commit: save to tmp in same dir, verify, replace
        rand_id = uuid.uuid4().hex[:8]
        tmp_path = book_path.parent / f".{book_path.stem}.tmp-{rand_id}.xlsx"
        wb.save(tmp_path)
        wb.close()
        wb = None

        # Verify integrity of the newly written file before replacement
        verify_workbook_file(tmp_path)

        # Atomic swap
        os.replace(tmp_path, book_path)
        tmp_path = None

    except Exception:
        if wb:
            wb.close()
        if tmp_path and tmp_path.exists():
            with contextlib.suppress(OSError):
                tmp_path.unlink()
        raise

    finally:
        _release_lock(lock_fd, lock_file)


def commit_prepared_workbook(
    book_path: Path,
    workbook: openpyxl.Workbook,
    expected_source_sha256: str,
    operation: str = "write",
    timeout: float = 30.0,
) -> Path:
    """Commit a workbook prepared outside the lock using optimistic concurrency.

    Legacy enrichment tools do substantial in-memory transformations.  They may
    prepare those changes without holding the lock, but commit is rejected if
    another writer changed the source workbook in the meantime.
    """
    book_path = Path(book_path).resolve()
    lock_path = book_path.with_name(f".{book_path.name}.lock")
    lock_fd = _acquire_lock(lock_path, timeout=timeout)
    tmp_path: Path | None = None
    try:
        actual_hash = file_sha256(book_path)
        if actual_hash != expected_source_sha256:
            raise WorkbookLockError(
                f"Workbook changed while {operation} was preparing: {book_path}"
            )
        create_snapshot_backup(book_path, operation=operation)
        tmp_path = book_path.parent / f".{book_path.stem}.tmp-{uuid.uuid4().hex[:8]}.xlsx"
        workbook.save(tmp_path)
        workbook.close()
        verify_workbook_file(tmp_path)
        os.replace(tmp_path, book_path)
        tmp_path = None
        return book_path
    except Exception:
        with contextlib.suppress(Exception):
            workbook.close()
        if tmp_path and tmp_path.exists():
            with contextlib.suppress(OSError):
                tmp_path.unlink()
        raise
    finally:
        _release_lock(lock_fd, lock_path)
