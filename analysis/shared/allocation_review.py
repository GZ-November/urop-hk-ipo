"""Read-only review gate for frozen retail tier evidence; never creates approval."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def reviewed_tiers(root):
    directory = Path(root) / 'pipeline/reports/data_gap_collection'
    review = json.loads((directory / 'allocation_review.json').read_text())
    if review.get('gate_pass') is not True or review.get('verdict') != 'pass_for_all_113_issuers_reconciled':
        raise ValueError('Independent allocation review does not authorize this dataset')
    if review.get('source_and_rule_failures'):
        raise ValueError('Review contains unresolved source/rule failures')
    for key, name in [('candidate_sha256', 'allocation_tiers_candidates.csv'),
                      ('coverage_sha256', 'allocation_coverage.csv')]:
        if review.get(key) != digest(directory / name):
            raise ValueError('Independent review hash mismatch: ' + name)
    candidate = pd.read_csv(directory / 'allocation_tiers_candidates.csv')
    clean = pd.read_csv(directory / 'allocation_tiers_clean.csv')
    if len(candidate) != review.get('rows_checked') or candidate.code.nunique() != review.get('issuers_checked'):
        raise ValueError('Review scope does not match candidate rows/issuers')
    keys = ['code', 'pool', 'applied_shares']
    columns = ['applicants', 'guaranteed_shares', 'ballot_winners', 'ballot_denominator',
               'ballot_extra_shares', 'expected_shares', 'allocated_shares', 'source_text',
               'source_sha256', 'pdf_page', 'board_lot_units', 'board_lot_unit',
               'source_quote', 'rule_original', 'rule_encoding', 'continuation_page', 'printed_allocation_pct']
    if candidate.duplicated(keys).any() or clean.duplicated(keys).any() or len(clean) != len(candidate):
        raise ValueError('Clean/candidate identity or cardinality mismatch')
    joined = candidate.merge(clean, on=keys, suffixes=('_candidate', '_clean'), validate='one_to_one')
    if len(joined) != len(candidate):
        raise ValueError('Clean table missing candidate identities')
    for col in columns:
        a, b = joined[col + '_candidate'], joined[col + '_clean']
        if not (a.eq(b) | (a.isna() & b.isna())).all():
            raise ValueError('Clean table differs from reviewed candidate: ' + col)
    if not clean.semantic_review.eq('pass').all():
        raise ValueError('Clean rows are not marked as independently reviewed')
    if not candidate.ballot_denominator.eq(candidate.applicants).all():
        raise ValueError('Ballot denominator differs from applicant count')
    if not candidate.errors.isna().all():
        raise ValueError('Candidate has unresolved parse errors')
    for path, group in candidate.groupby('source_text'):
        target = (Path(root) / path).resolve()
        if not target.is_relative_to(Path(root).resolve()):
            raise ValueError('Source path outside repository')
        if not target.exists() or not group.source_sha256.eq(digest(target)).all():
            raise ValueError('Reviewed source changed: ' + path)
    probability = candidate.ballot_winners / candidate.applicants
    if not np.isfinite(probability).all() or not probability.between(0, 1).all():
        raise ValueError('Invalid ballot probability')
    expected = candidate.guaranteed_shares + probability * candidate.ballot_extra_shares
    if not np.allclose(expected, candidate.expected_shares):
        raise ValueError('Invalid expected allocation')
    return clean
