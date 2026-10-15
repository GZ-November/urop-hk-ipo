"""derive_allot must not crash on a cohort that has not run the greenshoe search."""
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]

import run  # noqa: E402


class DeriveAllotPrerequisiteTests(unittest.TestCase):
    def _run(self, index_exists: bool):
        with tempfile.TemporaryDirectory() as tmp:
            allot_out = Path(tmp)
            if index_exists:
                (allot_out / "greenshoe.json").write_text("{}", encoding="utf-8")
            cfg = {"paths": {"allot_out": allot_out}}
            calls = []

            def fake_greenshoe(*_args):
                calls.append("greenshoe")
                (allot_out / "greenshoe.json").write_text("{}", encoding="utf-8")

            with patch.object(run, "cmd_greenshoe", fake_greenshoe), \
                    patch("greenshoe.apply_cv", lambda *a, **k: calls.append("cv")), \
                    patch("cornerstone.apply_ck", lambda *a, **k: calls.append("ck")), \
                    patch("pricing_date.apply_cq", lambda *a, **k: calls.append("cq")), \
                    patch("validate.apply_da", lambda *a, **k: calls.append("da")):
                run.cmd_derive_allot(cfg, Namespace(), [{"code": "8610.HK"}])
            return calls

    def test_missing_greenshoe_index_triggers_the_search_before_apply_cv(self):
        self.assertEqual(self._run(False), ["greenshoe", "cv", "ck", "cq", "da"])

    def test_existing_greenshoe_index_is_not_searched_again(self):
        self.assertEqual(self._run(True), ["cv", "ck", "cq", "da"])


if __name__ == "__main__":
    unittest.main()
