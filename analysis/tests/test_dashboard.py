"""Data contracts for the portable dashboard, without altering source artifacts."""
import csv
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('build_dashboard', ROOT / 'tools/build_dashboard.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def test_snapshot_matches_sources():
    assert builder.OUTPUT.read_text(encoding='utf-8') == builder.render()
    payload = builder.build_payload()
    assert len(payload['fields']) == 202
    research = [r for r in payload['rows'] if r[builder.DATE].startswith('2026-')]
    assert len(research) == 113
    assert {c: sum(r['cohort'] == c for r in research)
            for c in ('2026Q1', '2026Q2', '2026Q3')} == {'2026Q1': 38, '2026Q2': 45, '2026Q3': 30}
    assert any(r['Final cornerstone allocation (% of base offer)'] == 0 for r in research)
    assert any(r['6-month BHR from Day-1 close (%)'] is None for r in research)
    html = builder.render()
    assert '<script src=' not in html
    embedded = html.split('<script id="ipo-data" type="application/json">')[1].split('</script>')[0]
    assert json.loads(embedded) == payload


def write_master(path, rows, headers):
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


@pytest.mark.parametrize('violation', ['duplicate', 'cohort', 'number', 'header'])
def test_invalid_data_rejected(tmp_path, violation):
    with builder.MASTER.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        rows, headers = list(reader), reader.fieldnames
    rows = [rows[0].copy()]
    if violation == 'duplicate':
        rows.append(rows[0].copy())
    elif violation == 'cohort':
        rows[0]['cohort'] = '2026Q1'
    elif violation == 'number':
        rows[0]['IPO Subscription Price (HK$)'] = 'not a number'
    else:
        headers.remove('Stock Code')
        rows[0].pop('Stock Code')
    path = tmp_path / f'dashboard-{violation}.csv'
    try:
        write_master(path, rows, headers)
        with pytest.raises(ValueError):
            builder.build_payload(path)
    finally:
        path.unlink()


def test_script_terminator_is_escaped(monkeypatch):
    monkeypatch.setattr(builder, 'build_payload', lambda: {'name': '</script><script>alert(1)</script>'})
    html = builder.render()
    embedded = html.split('<script id="ipo-data" type="application/json">')[1].split('</script>')[0]
    assert '<' not in embedded
    assert json.loads(embedded)['name'] == '</script><script>alert(1)</script>'
