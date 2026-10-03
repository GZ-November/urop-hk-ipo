"""Build a portable, offline dashboard from canonical IPO exports and registry."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / 'pipeline/exports/HKIPO-MB-MASTER_clean.csv'
REGISTRY = ROOT / 'pipeline/registry/HKIPO_Variable_Registry.yaml'
TEMPLATE = ROOT / 'dashboard/template.html'
OUTPUT = ROOT / 'dashboard/index.html'
DATE = 'Date of Listing (dd/mm/yy)'
CODE = 'Stock Code'
MISSING = {'', 'nan', 'na', 'n/a', 'null'}


def build_payload(master: Path = MASTER, registry: Path = REGISTRY) -> dict:
    """Interpret registry types, preserving unknowns and validating identities."""
    definitions = yaml.safe_load(registry.read_text(encoding='utf-8'))
    fields = [{k: v.get(k) for k in ('header', 'dtype', 'layer', 'timing', 'unit')}
              for v in definitions['variables']]
    numeric = {v['header'] for v in fields if v['dtype'] in {'numeric', 'boolean'}}
    numeric.update({'cross_cohort_duplicate', 'leverage_y1', 'roa_y1',
                    'sales_growth_y1', 'log_proceeds_hkd', 'public_offer_fraction',
                    'sponsor_reputation_tier'})
    rows = []
    identities = set()
    with master.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        missing = {v['header'] for v in fields} - set(headers)
        if missing:
            raise ValueError(f'Master missing registered fields: {sorted(missing)}')
        for raw in reader:
            row = {}
            for key, value in raw.items():
                value = (value or '').strip()
                if value.lower() in MISSING:
                    row[key] = None
                elif key in numeric:
                    number = float(value)
                    row[key] = number if math.isfinite(number) else None
                else:
                    row[key] = value
            listing = date.fromisoformat(row[DATE])
            expected = f'{listing.year}Q{(listing.month - 1) // 3 + 1}'
            if row['cohort'] != expected:
                raise ValueError(f'Cohort/date conflict: {row[CODE]}')
            identity = (listing.year, row[CODE])
            if identity in identities:
                raise ValueError(f'Duplicate issuer: {identity}')
            identities.add(identity)
            rows.append(row)
    sources = {str(p.relative_to(ROOT) if p.is_relative_to(ROOT) else p):
               hashlib.sha256(p.read_bytes()).hexdigest()
               for p in (master, registry)}
    return {'rows': rows, 'fields': fields, 'headers': headers,
            'sources': sources, 'cutoff': '2026-09-30',
            'listingRange': [min(r[DATE] for r in rows), max(r[DATE] for r in rows)]}


def render() -> str:
    """Inline all data, styles and scripts; no web server or CDN is required."""
    payload = json.dumps(build_payload(), ensure_ascii=True, allow_nan=False,
                         separators=(',', ':')).replace('<', '\\u003c')
    return TEMPLATE.read_text(encoding='utf-8').replace('__IPO_DATA__', payload)


def main() -> None:
    """Build the snapshot or check that the checked-in HTML is current."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    html = render()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding='utf-8') != html:
            raise SystemExit('Dashboard snapshot is stale; run make dashboard-build.')
        print('Dashboard snapshot matches canonical data and template.')
    else:
        OUTPUT.write_text(html, encoding='utf-8')
        print(f'Built {OUTPUT}')


if __name__ == '__main__':
    main()
