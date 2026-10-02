"""Project orchestration and shared-module isolation contracts."""
from pathlib import Path
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
ANALYSIS = ROOT / "analysis"
sys.path.insert(0, str(ANALYSIS))


def load_script(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


runner = load_script("analysis_runner", ANALYSIS / "run.py")
workspace = load_script("workspace_manager", ROOT / "tools/research_workspace.py")


class ProjectArchitectureTests(unittest.TestCase):
    def test_inference_does_not_import_reports_or_plotting(self):
        code = """
import sys
from shared.inference import wild_cluster_p
from specifications.underpricing import estimation_sample
assert not any(name in sys.modules for name in (
 'module_a_stylized_facts', 'module_b_underpricing_regression',
 'extended_analysis_2026', 'matplotlib', 'statsmodels'))
"""
        subprocess.run([sys.executable, "-c", code], cwd=ANALYSIS, check=True)

    def test_legacy_names_share_the_same_implementations(self):
        import module_a_stylized_facts as a
        import module_b_underpricing_regression as b
        from shared import reporting, inference
        from specifications import underpricing
        self.assertIs(a.to_markdown, reporting.to_markdown)
        self.assertIs(b.wild_cluster_p, inference.wild_cluster_p)
        self.assertIs(b.estimation_sample, underpricing.estimation_sample)
        self.assertIs(b.MODELS, underpricing.MODELS)
        import extended_analysis_2026 as extended
        from shared import estimation
        self.assertIs(extended.ols_focus, estimation.ols_focus)
        self.assertIs(extended.bh_family, estimation.bh_family)

    def test_analysis_stops_at_failed_study(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "analysis").mkdir()
            studies = list(runner.STUDIES[:3])
            for study in studies:
                (root / "analysis" / f"{study.script}.py").touch()
            with patch.object(runner.subprocess, "run") as run:
                run.side_effect = [subprocess.CompletedProcess([], 0), subprocess.CompletedProcess([], 7)]
                self.assertEqual(runner.run_studies(studies, root), 7)
                self.assertEqual(run.call_count, 2)
                self.assertEqual(run.call_args.kwargs["cwd"], root)

    def test_list_studies_does_not_read_data_or_run_reports(self):
        result = subprocess.run([sys.executable, str(ROOT / "run.py"), "analysis", "--list"],
                                cwd=ROOT, check=True, capture_output=True, text=True)
        self.assertIn("underpricing", result.stdout)
        self.assertIn("retail", result.stdout)
        self.assertEqual(len(result.stdout.splitlines()), len(runner.STUDIES))

    def test_workspace_conflict_preflight_preserves_all_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.csv").write_text("canonical")
            (root / "index").mkdir()
            existing = root / "index/user.csv"
            existing.write_text("user edit")
            catalog = {"version": 1, "directory": "index", "entries": [
                {"name": "new.csv", "source": "source.csv"},
                {"name": "user.csv", "source": "source.csv"},
            ]}
            with self.assertRaisesRegex(ValueError, "Existing file preserved"):
                workspace.synchronize(root, catalog)
            self.assertFalse((root / "index/new.csv").exists())
            self.assertEqual(existing.read_text(), "user edit")

    def test_workspace_relative_links_remain_valid_after_project_move(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "before"
            root.mkdir()
            (root / "source.csv").write_text("canonical")
            catalog = {"version": 1, "directory": "index", "entries": [
                {"name": "inputs/data.csv", "source": "source.csv"},
            ]}
            workspace.synchronize(root, catalog)
            moved = root.with_name("after")
            root.rename(moved)
            self.assertEqual(workspace.synchronize(moved, catalog, check=True), 1)
            self.assertEqual((moved / "index/inputs/data.csv").read_text(), "canonical")

    def test_workspace_rejects_missing_source_before_any_write(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog = {"version": 1, "directory": "index", "entries": [
                {"name": "data.csv", "source": "missing.csv"},
            ]}
            with self.assertRaisesRegex(ValueError, "Missing source"):
                workspace.synchronize(root, catalog)
            self.assertFalse((root / "index").exists())


if __name__ == "__main__":
    unittest.main()
