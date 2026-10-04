"""Guard missing-price semantics, information timing and price-stage accounting."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pricing_adjustment_2026 as study  # noqa: E402


@pytest.fixture(scope='module')
def sample():
    return study.build_sample()


def test_missing_lower_endpoint_is_not_fixed_or_zero_revision(sample):
    missing = sample.range_low.isna()
    assert missing.sum() == 31
    assert sample.loc[missing,'price_status'].eq('undisclosed_lower_bound').all()
    assert sample.loc[missing,['midpoint','revision','range_position']].isna().all().all()
    equal = sample.price_status.eq('equal_endpoints')
    assert equal.sum() == 39 and sample.loc[equal,'revision'].isna().all()


def test_price_stage_coefficients_add_on_independent_least_squares(sample):
    s = sample[sample.price_status.eq('two_sided_range')]
    x = np.column_stack([np.ones(len(s)),s.revision,s.q2,s.q3])
    b = {k:np.linalg.lstsq(x,s[k],rcond=None)[0]
         for k in ['log_close','log_opening','log_intraday']}
    assert np.allclose(b['log_close'],b['log_opening']+b['log_intraday'],atol=1e-12)


def test_temporal_forecast_never_uses_unavailable_labels(sample,monkeypatch,tmp_path):
    monkeypatch.setattr(study,'OUT',tmp_path)
    study.rolling_assessment(sample)
    p = pd.read_csv(tmp_path/'rolling_predictions.csv')
    s = sample.set_index('code')
    for _,row in p.iterrows():
        ids = row.training_codes.split(';')
        assert len(ids)==row.training_n and row.training_n>=40
        assert row.code not in ids
        assert s.loc[ids,'listing_date'].lt(pd.Timestamp(row.cutoff)).all()
    # Changing a later payoff cannot change the earliest forecast.
    altered = sample.copy()
    first = p.iloc[0]
    future = altered.listing_date.ge(pd.Timestamp(first.cutoff))
    altered.loc[future,'ceiling_principal_return'] += 1000
    study.rolling_assessment(altered)
    second = pd.read_csv(tmp_path/'rolling_predictions.csv').iloc[0]
    assert second.launch_size_and_ah == pytest.approx(first.launch_size_and_ah)
    assert second.expanding_mean == pytest.approx(first.expanding_mean)


def test_ceiling_principal_return_uses_requested_maximum_not_final_proceeds(sample):
    expected = sample.allocation_rate*(sample.first_day_close-sample.offer_price)/sample.range_high
    assert np.allclose(expected,sample.ceiling_principal_return,atol=1e-12)
