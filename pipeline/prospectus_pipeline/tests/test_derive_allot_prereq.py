"""derive_allot must not crash or silently skip issuers missing from the greenshoe search."""
import json
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
    def _run(self, index):
        """Run derive_allot for 8610.HK with ``index`` as greenshoe.json (None = absent)."""
        with tempfile.TemporaryDirectory() as tmp:
            allot_out = Path(tmp)
            if index is not None:
                (allot_out / "greenshoe.json").write_text(json.dumps(index), encoding="utf-8")
            cfg = {"paths": {"allot_out": allot_out}}
            calls = []

            def fake_greenshoe(_cfg, _args, companies):
                calls.append("greenshoe:" + ",".join(c["code"] for c in companies))

            with patch.object(run, "cmd_greenshoe", fake_greenshoe), \
                    patch("greenshoe.apply_cv", lambda *a, **k: calls.append("cv")), \
                    patch("cornerstone.apply_ck", lambda *a, **k: calls.append("ck")), \
                    patch("pricing_date.apply_cq", lambda *a, **k: calls.append("cq")), \
                    patch("validate.apply_da", lambda *a, **k: calls.append("da")):
                run.cmd_derive_allot(cfg, Namespace(), [{"code": "8610.HK"}])
            return calls

    def test_missing_greenshoe_index_triggers_the_search_before_apply_cv(self):
        self.assertEqual(self._run(None), ["greenshoe:8610.HK", "cv", "ck", "cq", "da"])

    def test_index_without_this_issuer_searches_only_this_issuer(self):
        # A parallel extractor already searched another issuer of the same cohort.
        self.assertEqual(self._run({"0001.HK": {"status": "ok"}}),
                         ["greenshoe:8610.HK", "cv", "ck", "cq", "da"])

    def test_issuer_already_searched_is_not_searched_again(self):
        self.assertEqual(self._run({"8610.HK": {"status": "ok"}}), ["cv", "ck", "cq", "da"])


if __name__ == "__main__":
    unittest.main()
