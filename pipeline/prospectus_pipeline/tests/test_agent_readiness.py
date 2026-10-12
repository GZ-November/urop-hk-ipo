"""Regression checks for CLI failure signals and portable data delivery."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

PIPE = Path(__file__).resolve().parents[1]
REPO = PIPE.parents[1]
sys.path[:0] = [str(PIPE / 'src'), str(REPO / 'tools')]
spec = importlib.util.spec_from_file_location('pipeline_agent_cli', PIPE / 'run.py')
cli = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = cli
spec.loader.exec_module(cli)

from agent_handoff import build_handoff  # noqa: E402
from bundle_data import build_bundle, digest  # noqa: E402


class AgentReadinessTests(unittest.TestCase):
    def test_audit_returns_failure_for_missing_source_or_mismatched_values(self):
        cfg = {'dataset': {}, 'paths': {}}
        for key in ('value_mismatch', 'json_missing', 'excel_missing', 'json_files_absent'):
            with self.subTest(key=key), patch('audit.run_audit', return_value={'stats': {'prospectus': {key: 1}}}):
                self.assertEqual(cli.cmd_audit(cfg, argparse.Namespace(target='all'), [{'code': '0001.HK'}]), 1)
        with patch('audit.run_audit', return_value={'stats': {'prospectus': {'both_missing': 10}}}):
            self.assertEqual(cli.cmd_audit(cfg, argparse.Namespace(target='all'), [{'code': '0001.HK'}]), 0)

    def test_external_nonzero_exit_is_not_ignored_by_stage_protocol(self):
        cfg = {'_config_path': PIPE / 'config.yaml', 'dataset': {'id': 'test'}, 'workbook': 'test.xlsx'}
        with patch.dict(os.environ, {}, clear=True), patch.object(sys, 'argv', ['run.py', 'external']), \
                patch.object(cli, 'load_cfg', return_value=cfg), patch.object(cli, 'read_companies', return_value=[{'code': '0001.HK'}]), \
                patch.object(cli, 'cmd_external', return_value=7):
            self.assertEqual(cli.main(), 7)

    def test_portable_handoff_uses_exact_config_and_actual_schema(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            paths = {key: root / key for key in ('out', 'packets', 'allot_out', 'allot_packets')}
            cfg = {'_root': PIPE, '_config_path': root / 'cohort.yaml', 'dataset': {'board': 'GEM'}, 'paths': paths}
            jobs = json.loads(build_handoff(cfg, [{'code': '8549.HK'}]).read_text())['jobs']
            self.assertEqual(len(jobs), 3)
            self.assertIn('gem_prospectus_fields.json', Path(jobs[0]['extract_instruction']).read_text())
            self.assertIn('--reviewer', Path(jobs[0]['review_instruction']).read_text())
            self.assertIn(str(cfg['_config_path']), Path(jobs[0]['extract_instruction']).read_text())
            self.assertFalse(any(job['packet_ready'] for job in jobs))

    def test_delivery_manifest_matches_files_and_does_not_change_workbook(self):
        config = PIPE / 'config_2026q1.yaml'
        book = REPO / 'pipeline/cohorts/HKIPO-MB2026Q1.xlsx'
        before = digest(book)
        with tempfile.TemporaryDirectory() as temporary:
            archive_path = Path(temporary) / 'data.zip'
            report = build_bundle([config], archive_path)
            self.assertEqual(report['cohorts'][0]['issuers'], 38)
            with zipfile.ZipFile(archive_path) as archive:
                manifest = json.loads(archive.read('manifest.json'))
                import hashlib
                for item in manifest:
                    self.assertEqual(hashlib.sha256(archive.read(item['path'])).hexdigest(), item['sha256'])
                self.assertFalse(any(name.endswith('.pdf') for name in archive.namelist()))
            self.assertEqual(digest(book), before)
            with self.assertRaisesRegex(ValueError, 'already exists'):
                build_bundle([config], archive_path)


if __name__ == '__main__':
    unittest.main()
