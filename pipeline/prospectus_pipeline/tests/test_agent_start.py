# ==============================================================================
# Tests for Generic-Agent Start Entry Point, Bundling, and Quality Gates
# ==============================================================================
from __future__ import annotations

import argparse
from dataclasses import dataclass
import datetime as dt
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

PIPE = Path(__file__).resolve().parents[1]
REPO = PIPE.parents[1]
sys.path[:0] = [str(PIPE / "src"), str(REPO / "tools")]

from agent_start import (
    latest_completed_hk_quarter,
    validate_date_range,
    RunLock,
    start_collection,
    resume_collection,
    main as agent_start_main,
)
from delivery_index import (
    generate_delivery_readme,
    generate_index_json,
    generate_start_here_html,
)
from bundle_data import build_bundle, sheet_csv


@dataclass
class DummyProcess:
    returncode: int = 0
    stdout: str = ""
    stderr: str = ""


class AgentStartTests(unittest.TestCase):
    """Test suite for stdlib-only agent entry point, auto-quarter, and safe resume."""

    def test_default_quarter_across_year_boundaries(self):
        """Verify Hong Kong quarter calculation across year and quarter boundaries."""
        # 1. Q4 in Hong Kong (e.g. October 2026) -> latest completed is Q3
        start, end, label = latest_completed_hk_quarter(dt.date(2026, 10, 12))
        self.assertEqual(start, dt.date(2026, 7, 1))
        self.assertEqual(end, dt.date(2026, 9, 30))
        self.assertEqual(label, "2026Q3")

        # 2. Q1 across year boundary (e.g. January 5, 2027) -> latest completed is 2026 Q4
        start, end, label = latest_completed_hk_quarter(dt.date(2027, 1, 5))
        self.assertEqual(start, dt.date(2026, 10, 1))
        self.assertEqual(end, dt.date(2026, 12, 31))
        self.assertEqual(label, "2026Q4")

        # 3. Q2 (e.g. April 1, 2026) -> latest completed is 2026 Q1
        start, end, label = latest_completed_hk_quarter(dt.date(2026, 4, 1))
        self.assertEqual(start, dt.date(2026, 1, 1))
        self.assertEqual(end, dt.date(2026, 3, 31))
        self.assertEqual(label, "2026Q1")

        # 4. Q3 (e.g. July 1, 2026) -> latest completed is 2026 Q2
        start, end, label = latest_completed_hk_quarter(dt.date(2026, 7, 1))
        self.assertEqual(start, dt.date(2026, 4, 1))
        self.assertEqual(end, dt.date(2026, 6, 30))
        self.assertEqual(label, "2026Q2")

        # 5. Boundary dates: Dec 31 -> Q3 of same year
        start, end, label = latest_completed_hk_quarter(dt.date(2026, 12, 31))
        self.assertEqual(start, dt.date(2026, 7, 1))
        self.assertEqual(end, dt.date(2026, 9, 30))
        self.assertEqual(label, "2026Q3")

        # 6. Default call without reference_date runs without error
        now_start, now_end, now_label = latest_completed_hk_quarter()
        self.assertIsInstance(now_start, dt.date)
        self.assertIsInstance(now_end, dt.date)
        self.assertTrue(now_start <= now_end)

    def test_explicit_range_validation(self):
        """Test explicit range validation for valid, inverted, and malformed inputs."""
        # Valid range
        s, e = validate_date_range("2026-01-01", "2026-03-31")
        self.assertEqual(s, dt.date(2026, 1, 1))
        self.assertEqual(e, dt.date(2026, 3, 31))

        # Inverted range
        with self.assertRaises(ValueError) as ctx:
            validate_date_range("2026-04-01", "2026-01-01")
        self.assertIn("must be on or before end date", str(ctx.exception))

        # Incomplete range
        with self.assertRaises(ValueError) as ctx:
            validate_date_range("2026-01-01", None)
        self.assertIn("Both --period-start and --period-end must be provided together", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            validate_date_range(None, "2026-03-31")
        self.assertIn("Both --period-start and --period-end must be provided together", str(ctx.exception))

        # Malformed date string
        with self.assertRaises(ValueError) as ctx:
            validate_date_range("not-a-date", "2026-03-31")
        self.assertIn("Invalid --period-start date format", str(ctx.exception))

    def test_run_lock_concurrency_fails_safely(self):
        """Verify directory lock fails safely on concurrent access and cleans up."""
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir) / "run_test"

            # 1. First lock acquisition succeeds
            with RunLock(run_dir):
                self.assertTrue((run_dir / "run.lock").is_file())

                # 2. Second lock attempt on active process must raise RuntimeError
                with self.assertRaises(RuntimeError) as ctx:
                    with RunLock(run_dir):
                        pass
                self.assertIn("Concurrency collision", str(ctx.exception))

            # 3. Exiting first lock cleans up lock file
            self.assertFalse((run_dir / "run.lock").exists())

            # 4. Stale lock recovery (simulating dead PID 999999)
            lock_file = run_dir / "run.lock"
            lock_file.write_text(json.dumps({"pid": 999999, "created_at": "test"}), encoding="utf-8")
            self.assertTrue(lock_file.is_file())

            # Acquiring must prune stale lock and succeed
            with RunLock(run_dir):
                self.assertTrue(lock_file.is_file())
            self.assertFalse(lock_file.exists())

    def test_config_reuse_and_resume_workflow(self):
        """Test one-command execution returning exit code 3 (work pending), then resuming to 0."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_dir = root / "run_output"

            # Simulated cohort structure
            cohort_dir = root / "pipeline/prospectus_pipeline/datasets/HKIPO_2026-01-01_2026-03-31_HKIPO-MB"
            cohort_dir.mkdir(parents=True)
            cohort_config = cohort_dir / "cohort.yaml"
            cohort_config.write_text("dataset:\n  board: Main Board\n", encoding="utf-8")
            handoff_dir = cohort_dir / "out/agent_handoff"
            handoff_dir.mkdir(parents=True)
            (handoff_dir / "work_orders.json").write_text(json.dumps({"jobs": []}), encoding="utf-8")

            executed_commands = []

            def mock_runner_stage1(cmd, **kwargs):
                executed_commands.append(list(cmd))
                # Return 3 to simulate extraction/review pending
                return DummyProcess(returncode=3)

            # Step 1: Initial invocation
            import argparse
            args = argparse.Namespace(
                board="main",
                period_start="2026-01-01",
                period_end="2026-03-31",
                run_dir=str(run_dir),
                profile="core",
                no_bootstrap=True,
                resume=False,
            )
            # Seed project python check so no real venv required
            os.environ["HKIPO_PYTHON"] = sys.executable

            rc1 = start_collection(args, root=root, runner=mock_runner_stage1)
            self.assertEqual(rc1, 3)

            # Check artifacts generated for work pending
            state_file = run_dir / "run_state.json"
            self.assertTrue(state_file.is_file())
            state1 = json.loads(state_file.read_text(encoding="utf-8"))
            self.assertEqual(state1["status"], "WORK_PENDING")
            self.assertFalse(state1["is_analysis_ready"])
            self.assertEqual(state1["cohort_config"], str(cohort_config))
            self.assertIn("resume --run-dir", state1["resume_command"])

            html_file = run_dir / "START_HERE.html"
            self.assertTrue(html_file.is_file())
            html_text = html_file.read_text(encoding="utf-8")
            self.assertIn("WORK PENDING", html_text)
            self.assertIn("NOT ANALYSIS-READY", html_text)
            self.assertIn("Exact Resume Command", html_text)

            index_file = run_dir / "index.json"
            self.assertTrue(index_file.is_file())
            index_data = json.loads(index_file.read_text(encoding="utf-8"))
            self.assertFalse(index_data["is_analysis_ready"])

            # Step 2: Resume invocation
            def mock_runner_stage2(cmd, **kwargs):
                executed_commands.append(list(cmd))
                # Return 0 to simulate completion
                return DummyProcess(returncode=0)

            resume_args = argparse.Namespace(
                run_dir=str(run_dir),
                profile="core",
                no_bootstrap=True,
            )
            rc2 = resume_collection(resume_args, root=root, runner=mock_runner_stage2)
            self.assertEqual(rc2, 0)

            # Check that resume updated state to analysis-ready
            state2 = json.loads(state_file.read_text(encoding="utf-8"))
            self.assertEqual(state2["status"], "ANALYSIS-READY")
            self.assertTrue(state2["is_analysis_ready"])

            html_text2 = html_file.read_text(encoding="utf-8")
            self.assertIn("ANALYSIS-READY", html_text2)

    def test_rerunning_same_start_command_resumes_saved_main_board_run(self):
        """The saved display board "Main Board" must not block the identical start command."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_dir = root / "run_main"
            cohort_dir = root / "pipeline/prospectus_pipeline/datasets/HKIPO_2026-01-01_2026-03-31_HKIPO-MB"
            cohort_dir.mkdir(parents=True)
            (cohort_dir / "cohort.yaml").write_text("dataset:\n  board: Main Board\n", encoding="utf-8")
            os.environ["HKIPO_PYTHON"] = sys.executable
            args = argparse.Namespace(
                board="main", period_start="2026-01-01", period_end="2026-03-31",
                run_dir=str(run_dir), profile="core", no_bootstrap=True, resume=False,
            )
            self.assertEqual(start_collection(args, root=root, runner=lambda cmd, **kw: DummyProcess(3)), 3)
            commands = []

            def finish(cmd, **kwargs):
                commands.append(list(cmd))
                return DummyProcess(0)

            self.assertEqual(start_collection(args, root=root, runner=finish), 0)
            self.assertIn("--config", commands[0])
            state = json.loads((run_dir / "run_state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["board"], "Main Board")
            self.assertEqual(state["status"], "ANALYSIS-READY")

    def test_failure_propagation_no_stale_success(self):
        """Verify pipeline failure is propagated with exit code and no fake success."""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_dir = root / "run_fail"

            def mock_runner_fail(cmd, **kwargs):
                return DummyProcess(returncode=2, stderr="Official coverage gap")

            os.environ["HKIPO_PYTHON"] = sys.executable
            args = argparse.Namespace(
                board="main",
                period_start="2026-01-01",
                period_end="2026-03-31",
                run_dir=str(run_dir),
                profile="core",
                no_bootstrap=True,
                resume=False,
            )

            rc = start_collection(args, root=root, runner=mock_runner_fail)
            self.assertEqual(rc, 2)

            state = json.loads((run_dir / "run_state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["status"], "FAILED")
            self.assertFalse(state["is_analysis_ready"])

            html_text = (run_dir / "START_HERE.html").read_text(encoding="utf-8")
            self.assertIn("FAILED", html_text)
            self.assertIn("NOT ANALYSIS-READY", html_text)
            self.assertNotIn("COLLECTION COMPLETE", html_text)

    def test_relative_output_links_and_html_escaping(self):
        """Verify strict HTML escaping of malicious scripts/formula prefixes and relative links."""
        cohort_mock = {
            "id": "HKIPO_2026Q1",
            "board": "Main Board",
            "period": ["2026-01-01", "2026-03-31"],
            "issuers": 1,
            "is_analysis_ready": False,
            "workbook": "cohorts/HKIPO_2026Q1/HKIPO-MB.xlsx",
            "csv": "cohorts/HKIPO_2026Q1/HKIPO-MB_clean.csv",
            "codebook_md": "cohorts/HKIPO_2026Q1/codebook.md",
            "codebook_json": "cohorts/HKIPO_2026Q1/codebook.json",
            "audit_md": "cohorts/HKIPO_2026Q1/audit.md",
            "status_json": "cohorts/HKIPO_2026Q1/status.json",
            "evidence_dir": "cohorts/HKIPO_2026Q1/evidence",
            "companies": [
                {
                    "code": "6082.HK",
                    "name": '<script>alert("XSS")</script> & "Dangerous=Formula"',
                    "listing_date": "2026-01-15",
                    "prospectus_status": "Pending",
                    "allot_status": "Pending",
                }
            ],
        }

        html_out = generate_start_here_html(
            title="Test Escaping",
            status="WORK_PENDING",
            is_analysis_ready=False,
            cohorts=[cohort_mock],
            is_bundle=True,
        )

        # Ensure no unescaped script tag exists
        self.assertNotIn('<script>alert("XSS")</script>', html_out)
        self.assertIn('&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;', html_out)
        self.assertIn('&amp;', html_out)
        self.assertIn('&quot;Dangerous=Formula&quot;', html_out)

        # Ensure all hrefs are relative (no machine-specific absolute paths)
        import re
        hrefs = re.findall(r'href="([^"]+)"', html_out)
        for h in hrefs:
            if h != "#":
                self.assertFalse(h.startswith("/"), f"Absolute link found: {h}")
                self.assertNotIn("Users", h, f"User directory found in link: {h}")
                self.assertNotIn("tmp", h, f"Tmp directory found in link: {h}")

    def test_quality_labels_and_missing_versus_zero_explanation(self):
        """Verify complete/pending/legacy labels and missing vs observed zero explanation."""
        html_out = generate_start_here_html(
            title="Quality Labels Test",
            status="ANALYSIS-READY",
            is_analysis_ready=True,
            cohorts=[],
            is_bundle=True,
        )
        self.assertIn("ANALYSIS-READY", html_out)
        self.assertIn("Missing Data Policy vs. Observed Zero", html_out)
        self.assertIn("never substituted with zero", html_out)
        self.assertIn("Empirically Observed Zero", html_out)

        readme_out = generate_delivery_readme(
            title="README Quality Test",
            status="ANALYSIS-READY",
            is_analysis_ready=True,
            cohorts=[],
            is_bundle=True,
        )
        self.assertIn("never substituted with zero", readme_out)
        self.assertIn("Standard Folder Layout", readme_out)

        index_out = generate_index_json(
            title="Index Quality Test",
            status="ANALYSIS-READY",
            is_analysis_ready=True,
            cohorts=[],
        )
        self.assertTrue(index_out["is_analysis_ready"])
        self.assertIn("folder_layout", index_out)

    def test_cli_entry_point_help_or_defaults(self):
        """Test agent_start_main with argument parsing."""
        with self.assertRaises(SystemExit) as ctx:
            agent_start_main(["--help"])
        self.assertEqual(ctx.exception.code, 0)

    def test_sheet_csv_sanitizes_formula_prefixes(self):
        """Verify sheet_csv neutralizes spreadsheet formula injection (=, +, -, @)."""
        import openpyxl
        with tempfile.TemporaryDirectory() as temp_dir:
            wb_path = Path(temp_dir) / "test_book.xlsx"
            csv_path = Path(temp_dir) / "test_out.csv"

            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "TestSheet"
            ws.append(["Header1", "Header2", "Header3"])
            ws.append(["=CMD|' /C calc'!A0", "+12345", "@SUM(A1:A2)"])
            wb.save(wb_path)
            wb.close()

            wb_read = openpyxl.load_workbook(wb_path)
            sheet_csv(wb_read, "TestSheet", csv_path)
            wb_read.close()

            csv_text = csv_path.read_text(encoding="utf-8-sig")
            # Should be prefixed with a single quote to prevent execution in Excel
            self.assertIn("'=CMD", csv_text)
            self.assertIn("'+12345", csv_text)
            self.assertIn("'@SUM", csv_text)

    def test_selected_only_bundle_delivery(self):
        """Verify bundle packages only requested cohorts, not unrelated canonical cohorts."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            out_zip = temp_root / "delivery.zip"

            # Create mock cohort configs
            pipe_dir = temp_root / "pipeline/prospectus_pipeline"
            pipe_dir.mkdir(parents=True)

            # We will test build_bundle with canonical 2026Q1 config from repo
            repo_cfg = Path(__file__).resolve().parents[1] / "config_2026q1.yaml"
            if not repo_cfg.is_file():
                self.skipTest("config_2026q1.yaml not present")

            summary = build_bundle(configs=[repo_cfg], output=out_zip, require_reviewed=False)
            self.assertTrue(out_zip.is_file())
            self.assertEqual(len(summary["cohorts"]), 1)

            # Inspect zip contents
            with zipfile.ZipFile(out_zip, "r") as zf:
                namelist = zf.namelist()
                # Must contain START_HERE.html, index.json, README.md, quality_summary.json, manifest.json
                self.assertIn("START_HERE.html", namelist)
                self.assertIn("index.json", namelist)
                self.assertIn("README.md", namelist)
                self.assertIn("quality_summary.json", namelist)
                self.assertIn("manifest.json", namelist)

                # Must contain HKIPO-MB2026Q1 cohort
                self.assertTrue(any("cohorts/HKIPO-MB2026Q1/" in name for name in namelist))
                # Must NOT contain unselected cohorts (e.g. 2026Q2, 2026Q3, GEM)
                self.assertFalse(any("cohorts/HKIPO-MB2026Q2/" in name for name in namelist))
                self.assertFalse(any("cohorts/HKIPO-MB2026Q3/" in name for name in namelist))

            # Verify no-overwrite guarantee
            with self.assertRaises(ValueError) as ctx:
                build_bundle(configs=[repo_cfg], output=out_zip, require_reviewed=False)
            self.assertIn("Delivery already exists", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
