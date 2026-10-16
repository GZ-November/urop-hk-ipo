"""Cohort lock and lease scheduler for parallel extraction/review subagents."""
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

import work_queue as wq  # noqa: E402
from cohort_lock import ENV, cohort_lock  # noqa: E402
from state import file_hash, save_record  # noqa: E402


def make_cfg(tmp: Path, board="Main Board") -> dict:
    out = tmp / "out"
    paths = {"out": out, "allot_out": out / "allot", "packets": tmp / "packets",
             "allot_packets": tmp / "allot_packets", "text": tmp / "text",
             "allot_text": tmp / "allot_text", "pdf": tmp / "pdf", "allot_pdf": tmp / "allot_pdf"}
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return {"_root": ROOT, "_ws": tmp, "_config_path": tmp / "cohort.yaml",
            "state_dir": str(tmp / "state"), "dataset": {"board": board, "id": "T"},
            "paths": paths}


def companies(*codes):
    return [{"code": c, "name": f"Issuer {c}"} for c in codes]


def write_payload(cfg, target, code, fields=None):
    path = wq.payload_path(cfg, target, code)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"code": code, "fields": fields or {}}), encoding="utf-8")
    return path


def record(cfg, target, code, stage, verdict=None, digest="h1"):
    rec = {"code": code, "target": target, "hash": digest, "gate_pass": True,
           "json_sha256": file_hash(wq.payload_path(cfg, target, code))}
    if verdict:
        rec["verdict"] = verdict
    save_record(cfg, target, code, stage, rec)


class CohortLockTests(unittest.TestCase):
    def test_second_process_waits_until_the_holder_releases(self):
        with tempfile.TemporaryDirectory() as raw:
            cfg = make_cfg(Path(raw))
            script = textwrap.dedent(f"""
                import sys, time
                sys.path[:0] = [{str(ROOT / 'src')!r}]
                from pathlib import Path
                from cohort_lock import cohort_lock
                cfg = {{"paths": {{"out": Path({str(cfg['paths']['out'])!r})}}}}
                start = time.monotonic()
                with cohort_lock(cfg, log=lambda *a: None):
                    print(round(time.monotonic() - start, 2))
            """)
            env = {k: v for k, v in os.environ.items() if k != ENV}
            with cohort_lock(cfg):
                child = subprocess.Popen([sys.executable, "-c", script], stdout=subprocess.PIPE,
                                         text=True, env=env)
                time.sleep(1.0)
            waited = float(child.communicate(timeout=30)[0].strip())
            self.assertGreaterEqual(waited, 0.8)

    def test_child_of_the_holder_does_not_deadlock(self):
        with tempfile.TemporaryDirectory() as raw:
            cfg = make_cfg(Path(raw))
            script = textwrap.dedent(f"""
                import sys
                sys.path[:0] = [{str(ROOT / 'src')!r}]
                from pathlib import Path
                from cohort_lock import cohort_lock
                with cohort_lock({{"paths": {{"out": Path({str(cfg['paths']['out'])!r})}}}}, timeout=3):
                    print("ok")
            """)
            with cohort_lock(cfg):
                out = subprocess.run([sys.executable, "-c", script], capture_output=True,
                                     text=True, timeout=30)
            self.assertEqual(out.stdout.strip(), "ok")


class PhaseTests(unittest.TestCase):
    def test_phases_follow_the_hash_bound_records(self):
        with tempfile.TemporaryDirectory() as raw:
            cfg = make_cfg(Path(raw))
            code = "0001.HK"
            self.assertEqual(wq.snapshot(cfg, companies(code))[code]["phase"], "extract")
            for target in ("prospectus", "allot"):
                write_payload(cfg, target, code)
                record(cfg, target, code, "extracted")
            self.assertEqual(wq.snapshot(cfg, companies(code))[code]["phase"], "review")
            record(cfg, "prospectus", code, "reviewed", "pass")
            record(cfg, "allot", code, "reviewed", "fail")
            snap = wq.snapshot(cfg, companies(code))[code]
            self.assertEqual(snap["states"], {"prospectus": "reviewed", "allot": "rejected"})
            self.assertEqual(snap["phase"], "extract")
            record(cfg, "allot", code, "reviewed", "pass")
            self.assertEqual(wq.snapshot(cfg, companies(code))[code]["phase"], "done")

    def test_editing_a_reviewed_payload_reopens_it(self):
        with tempfile.TemporaryDirectory() as raw:
            cfg = make_cfg(Path(raw))
            code = "0001.HK"
            for target in ("prospectus", "allot"):
                write_payload(cfg, target, code)
                record(cfg, target, code, "extracted")
                record(cfg, target, code, "reviewed", "pass")
            write_payload(cfg, "allot", code, {"col_CS": {"value": 1}})
            self.assertEqual(wq.snapshot(cfg, companies(code))[code]["states"]["allot"], "unrecorded")

    def test_gem_cohorts_add_the_extension_target(self):
        with tempfile.TemporaryDirectory() as raw:
            self.assertEqual(wq.targets_for(make_cfg(Path(raw), board="GEM")),
                             ["prospectus", "allot", "gem"])


class DispatchTests(unittest.TestCase):
    def setUp(self):
        patcher = patch.object(wq, "_search", lambda *a, **k: "")
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_limits_cap_extract_and_total_and_leases_block_reclaiming(self):
        with tempfile.TemporaryDirectory() as raw:
            cfg = make_cfg(Path(raw))
            codes = [f"{i:04d}.HK" for i in range(1, 9)]
            first = wq.next_jobs(cfg, companies(*codes), {"extract": 3, "total": 4})
            self.assertEqual([j["role"] for j in first["dispatch"]], ["extract"] * 3)
            self.assertTrue(all(Path(j["brief"]).is_file() for j in first["dispatch"]))
            again = wq.next_jobs(cfg, companies(*codes))
            self.assertEqual(again["dispatch"], [])
            self.assertEqual(len(again["active"]), 3)

    def test_reviews_are_dispatched_before_new_extractions(self):
        with tempfile.TemporaryDirectory() as raw:
            cfg = make_cfg(Path(raw))
            ready = "0009.HK"
            for target in ("prospectus", "allot"):
                write_payload(cfg, target, ready)
                record(cfg, target, ready, "extracted")
            result = wq.next_jobs(cfg, companies("0001.HK", ready), {"total": 1})
            self.assertEqual([(j["role"], j["code"]) for j in result["dispatch"]], [("review", ready)])
            brief = Path(result["dispatch"][0]["brief"]).read_text(encoding="utf-8")
            self.assertIn(file_hash(wq.payload_path(cfg, "allot", ready)), brief)

    def test_expired_lease_halves_the_role_limit_and_requeues_the_issuer(self):
        with tempfile.TemporaryDirectory() as raw:
            cfg = make_cfg(Path(raw))
            first = wq.next_jobs(cfg, companies("0001.HK"), {"extract": 4})
            queue = wq._load(cfg)
            past = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=1)).isoformat()
            for lease in queue["leases"].values():
                lease["expires_at"] = past
            wq._save(cfg, queue)
            second = wq.next_jobs(cfg, companies("0001.HK"))
            self.assertEqual(second["expired"], [first["dispatch"][0]["lease"]])
            self.assertEqual(second["limits"]["extract"], 2)
            self.assertEqual([j["code"] for j in second["dispatch"]], ["0001.HK"])

    def test_clean_completions_grow_the_limit_back(self):
        queue = {"limits": {"extract": 2, "review": 4, "total": 6}, "streak": {"extract": 0},
                 "leases": {"a": {"role": "extract", "code": "1"}, "b": {"role": "extract", "code": "2"}},
                 "history": []}
        wq._close(queue, "a", "done")
        self.assertEqual(queue["limits"]["extract"], 2)
        wq._close(queue, "b", "done")
        self.assertEqual(queue["limits"]["extract"], 3)


class FinishReviewTests(unittest.TestCase):
    def test_review_is_refused_until_each_report_names_the_current_payload(self):
        with tempfile.TemporaryDirectory() as raw:
            cfg = make_cfg(Path(raw))
            code = "0001.HK"
            for target in ("prospectus", "allot"):
                write_payload(cfg, target, code)
                record(cfg, target, code, "extracted")
            with patch.object(wq, "_search", lambda *a, **k: ""):
                lease = wq.next_jobs(cfg, companies(code))["dispatch"][0]["lease"]
            wq.report_path(cfg, "prospectus", code).write_text(
                f"payload sha256: {file_hash(wq.payload_path(cfg, 'prospectus', code))}\nPASS",
                encoding="utf-8")
            wq.report_path(cfg, "allot", code).write_text("payload sha256: deadbeef\nPASS",
                                                          encoding="utf-8")
            lines = []
            rc = wq.finish_review(cfg, lease, "pass", "reviewer", log=lines.append)
            self.assertEqual(rc, 1)
            self.assertTrue(any("does not name the current payload" in x for x in lines))
            self.assertIn(lease, wq._load(cfg)["leases"])  # still claimed by the reviewer


class ExcerptTests(unittest.TestCase):
    def test_excerpt_finds_the_quote_across_line_breaks(self):
        page = "STATEMENT\nRevenue  6\n76,757 133,002\nCost of services (65,767)"
        self.assertIn("Revenue 6 76,757 133,002", wq.excerpt(page, "Revenue 6 76,757 133,002"))
        self.assertIsNone(wq.excerpt(page, "not on this page"))


if __name__ == "__main__":
    unittest.main()
