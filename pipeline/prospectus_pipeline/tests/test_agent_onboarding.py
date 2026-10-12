"""Period planning, skill installation and skill metadata for one-sentence collection."""
from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import unittest

PIPE = Path(__file__).resolve().parents[1]
REPO = PIPE.parents[1]
sys.path.insert(0, str(REPO / "tools"))

from collection_plan import build_plan, parse_period, quarter_chunks  # noqa: E402
import install_skills  # noqa: E402

D = dt.date
TODAY = D(2026, 10, 12)


class PeriodParsingTests(unittest.TestCase):
    def test_period_terms_resolve_to_inclusive_intervals(self):
        cases = {
            "2025": (D(2025, 1, 1), D(2025, 12, 31)),
            "2025q4": (D(2025, 10, 1), D(2025, 12, 31)),
            "2025-Q1": (D(2025, 1, 1), D(2025, 3, 31)),
            "2024H1": (D(2024, 1, 1), D(2024, 6, 30)),
            "2025H2": (D(2025, 7, 1), D(2025, 12, 31)),
            "2024-02": (D(2024, 2, 1), D(2024, 2, 29)),
            "2025-11-03": (D(2025, 11, 3), D(2025, 11, 3)),
            "2024Q3..2025Q2": (D(2024, 7, 1), D(2025, 6, 30)),
            "2025-11-15..2026-02-10": (D(2025, 11, 15), D(2026, 2, 10)),
            "latest": (D(2026, 7, 1), D(2026, 9, 30)),
        }
        for spec, expected in cases.items():
            with self.subTest(spec=spec):
                self.assertEqual(parse_period(spec, TODAY), expected)

    def test_invalid_or_inverted_periods_fail(self):
        for spec in ("last autumn", "2025Q5", "2025-13", "2025Q4..2025Q1"):
            with self.subTest(spec=spec), self.assertRaises(ValueError):
                parse_period(spec, TODAY)

    def test_intervals_split_at_calendar_quarters(self):
        self.assertEqual(quarter_chunks(D(2025, 11, 15), D(2026, 4, 2)), [
            (D(2025, 11, 15), D(2025, 12, 31)),
            (D(2026, 1, 1), D(2026, 3, 31)),
            (D(2026, 4, 1), D(2026, 4, 2)),
        ])


class CollectionPlanTests(unittest.TestCase):
    def test_new_quarters_get_one_start_command_per_board(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "pipeline/prospectus_pipeline").mkdir(parents=True)
            plan = build_plan(["2025Q4"], ["main", "gem"], TODAY, root)
            self.assertEqual([(job["board"], job["status"]) for job in plan["jobs"]],
                             [("main", "new"), ("gem", "new")])
            self.assertEqual(plan["jobs"][0]["command"], "python3 run.py start --board main "
                             "--period-start 2025-10-01 --period-end 2025-12-31")
            self.assertIsNone(plan["bundle_command"])
            self.assertIn("rerun this plan after collection", plan["notes"][-1])

            config = Path(plan["jobs"][1]["cohort_config"])
            config.parent.mkdir(parents=True)
            config.write_text("dataset:\n  board: GEM\n", encoding="utf-8")
            (root / "deliverables").mkdir()
            (root / "deliverables/hkipo_2025-10-01_2025-12-31_20261012.zip").write_bytes(b"")
            plan = build_plan(["2025Q4"], ["main", "gem"], TODAY, root)
        self.assertEqual(plan["jobs"][1]["status"], "prepared")
        self.assertIn("--config pipeline/prospectus_pipeline/datasets/HKIPO_2025-10-01_2025-12-31_HKIPO-GEM/cohort.yaml",
                      plan["bundle_command"])
        self.assertNotIn("HKIPO-MB/", plan["bundle_command"])
        self.assertIn("--output deliverables/hkipo_2025-10-01_2025-12-31_20261012-2.zip", plan["bundle_command"])

    def test_stored_cohorts_are_reused_and_partial_quarters_collected(self):
        plan = build_plan(["2026-03-15..2026-12-31"], ["main"], TODAY)
        statuses = [(job["period_start"], job["status"]) for job in plan["jobs"]]
        self.assertEqual(statuses, [("2026-03-15", "stored"), ("2026-04-01", "stored"),
                                    ("2026-07-01", "stored"), ("2026-10-01", "new")])
        self.assertIn("select rows by listing date", plan["jobs"][0]["note"])
        self.assertIn("config_2026q1.yaml", plan["jobs"][0]["command"])
        self.assertIn("has not ended", plan["jobs"][-1]["note"])
        self.assertEqual(plan["bundle_command"].count("--config"), 3)

    def test_future_quarters_have_no_command_and_runs_report_progress(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "pipeline/prospectus_pipeline").mkdir(parents=True)
            run_dir = root / "deliverables/run_main_2025-10-01_2025-12-31"
            run_dir.mkdir(parents=True)
            (run_dir / "run_state.json").write_text(json.dumps({"status": "WORK_PENDING"}), encoding="utf-8")
            plan = build_plan(["2025Q4", "2027Q1"], ["main"], TODAY, root)
        self.assertEqual([job["status"] for job in plan["jobs"]], ["pending-review", "future"])
        self.assertIn("resumes", plan["jobs"][0]["note"])
        self.assertIsNone(plan["jobs"][1]["command"])
        self.assertIsNone(plan["bundle_command"])


class SkillInstallTests(unittest.TestCase):
    def make_skill(self, root: Path, name: str = "demo") -> Path:
        skill = root / ".agents/skills" / name
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: demo\n---\n", encoding="utf-8")
        return skill

    def test_project_install_links_relatively_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = self.make_skill(root)
            directory = root / ".claude/skills"
            self.assertIn(install_skills.install(skill, directory, root), ("linked", "copied (rerun after editing the skill)"))
            destination = directory / "demo"
            self.assertTrue((destination / "SKILL.md").is_file())
            if destination.is_symlink():
                self.assertFalse(Path(os.readlink(destination)).is_absolute())
                self.assertEqual(install_skills.install(skill, directory, root), "already linked")

    def test_existing_foreign_skill_is_kept(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            skill = self.make_skill(root)
            foreign = root / "home/.claude/skills/demo"
            foreign.mkdir(parents=True)
            (foreign / "SKILL.md").write_text("user's own skill", encoding="utf-8")
            self.assertEqual(install_skills.inspect(skill, foreign), "foreign")
            self.assertIn("kept existing", install_skills.install(skill, foreign.parent, root))
            self.assertEqual((foreign / "SKILL.md").read_text(encoding="utf-8"), "user's own skill")

    def test_user_scope_targets_claude_and_shared_agent_directories(self):
        home = Path("/home/example")
        self.assertEqual(install_skills.destinations("user", REPO, home),
                         [home / ".claude/skills", home / ".agents/skills"])
        self.assertEqual(install_skills.destinations("none", REPO, home), [])


class SkillMetadataTests(unittest.TestCase):
    def test_every_repository_skill_has_matching_name_and_description(self):
        skills = install_skills.available_skills()
        self.assertIn("hk-ipo-collect", [skill.name for skill in skills])
        for skill in skills:
            text = (skill / "SKILL.md").read_text(encoding="utf-8")
            front = re.match(r"^---\n(.*?)\n---\n", text, re.S)
            with self.subTest(skill=skill.name):
                self.assertIsNotNone(front)
                self.assertRegex(front[1], rf"(?m)^name: {re.escape(skill.name)}$")
                self.assertRegex(front[1], r"(?m)^description:")

    def test_collect_skill_points_at_existing_repository_files(self):
        text = (REPO / ".agents/skills/hk-ipo-collect/SKILL.md").read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)#]+)\)", text):
            if not target.startswith("http"):
                with self.subTest(target=target):
                    self.assertTrue((REPO / ".agents/skills/hk-ipo-collect" / target).resolve().exists())


if __name__ == "__main__":
    unittest.main()
