"""Economic quantity and evidence-gate tests, independent of empirical signs."""
import json
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import retail_profit_distribution_2026 as study
from shared.allocation_review import reviewed_tiers


def fixture():
    return pd.DataFrame({'applicants':[10], 'ballot_winners':[2],
                         'guaranteed_shares':[100], 'ballot_extra_shares':[100],
                         'applied_shares':[500], 'p0':[2.0], 'p1':[3.0]})


def test_guarantees_and_exact_break_even_are_separate_states():
    z=study.outcome_metrics(fixture(),100)
    assert z.net_low.iloc[0]==0
    assert z.net_high.iloc[0]==100
    assert z.expected_net.iloc[0]==20
    assert z.p_loss.iloc[0]==0
    assert z.p_zero_net.iloc[0]==.8
    assert z.p_profit.iloc[0]==.2
    assert z.p_no_shares.iloc[0]==0


def test_zero_guarantee_and_minimum_tier_outcome():
    f=fixture();f['guaranteed_shares']=0;f['ballot_extra_shares']=500
    z=study.outcome_metrics(f,88)
    assert z.net_low.iloc[0]==-88
    assert z.net_high.iloc[0]==412
    assert np.isclose(z.expected_net.iloc[0],12)
    assert z.p_loss.iloc[0]==.8
    assert np.allclose(z.p_loss+z.p_zero_net+z.p_profit,1)


def test_invalid_probabilities_and_financing_rejected():
    f=fixture();f['ballot_winners']=11
    with pytest.raises(ValueError): study.outcome_metrics(f)
    with pytest.raises(ValueError): study.outcome_metrics(fixture(),borrowed_fraction=1)


def test_deterministic_portfolio_and_reproducible_seed():
    f=fixture();f['ballot_winners']=10
    z=study.outcome_metrics(f,88)
    assert np.all(study.simulate_portfolio(z,20)==112)
    z=study.outcome_metrics(fixture(),88)
    assert np.array_equal(study.simulate_portfolio(z,30),study.simulate_portfolio(z,30))


def test_covariance_identity_including_negative_returns():
    d=study.decomposition(pd.DataFrame({'alloc_rate':[.1,.9], 'ir':[1.0,-.5]}))
    assert np.isclose(d['mean_product'],d['product_of_means']+d['covariance'])
    assert np.isclose(d['mean_product'],-.175)


def gate_copy(tmp_path):
    target=tmp_path/'pipeline/reports/data_gap_collection';target.mkdir(parents=True)
    source=study.ROOT/'pipeline/reports/data_gap_collection'
    for name in ['allocation_review.json','allocation_tiers_candidates.csv','allocation_coverage.csv','allocation_tiers_clean.csv']:
        shutil.copy2(source/name,target/name)
    return target


def test_changed_candidate_invalidates_review(tmp_path):
    target=gate_copy(tmp_path)
    with (target/'allocation_tiers_candidates.csv').open('a') as f:f.write('\n')
    with pytest.raises(ValueError,match='hash mismatch'):reviewed_tiers(tmp_path)


def test_clean_table_cannot_change_reviewed_amounts(tmp_path):
    target=gate_copy(tmp_path)
    p=target/'allocation_tiers_clean.csv';data=pd.read_csv(p)
    data.loc[0,'guaranteed_shares']+=100;data.to_csv(p,index=False)
    with pytest.raises(ValueError,match='differs'):reviewed_tiers(tmp_path)


def test_failed_review_cannot_be_used(tmp_path):
    target=gate_copy(tmp_path);p=target/'allocation_review.json'
    j=json.loads(p.read_text());j['gate_pass']=False;p.write_text(json.dumps(j))
    with pytest.raises(ValueError,match='does not authorize'):reviewed_tiers(tmp_path)
