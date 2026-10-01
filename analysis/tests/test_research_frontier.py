"""Economic denominators, confounding algebra and market-information timing."""
from pathlib import Path
import json
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
import statsmodels.api as sm

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import academic_extensions_2026 as ac
import research_frontier_2026 as rf


class ResearchTests(unittest.TestCase):
    def test_high_unweighted_ir_can_coexist_with_negative_allocation_return(self):
        frame = pd.DataFrame({'ir': [1., -.1], 'allocation': [.01, 1.]})
        out = rf.allocation_metrics(frame)
        self.assertAlmostEqual(out['mean_ir'], .45)
        self.assertAlmostEqual(out['allocation_weighted_ir'], -.09 / 1.01)
        self.assertAlmostEqual(out['application_return'], -.045)

    def test_impossible_allocation_is_excluded_instead_of_capped(self):
        out = rf.allocation_metrics(pd.DataFrame({'ir': [1., .5], 'allocation': [2., .1]}))
        self.assertEqual(out['n'], 1)
        self.assertAlmostEqual(out['application_return'], .05)

    def test_ovb_formula_matches_observed_confounder_omission(self):
        rng = np.random.default_rng(7)
        z = rng.normal(size=500)
        d = .8 * z + rng.normal(size=500)
        y = .4 * d + .7 * z + rng.normal(size=500)
        short = sm.OLS(y, pd.DataFrame({'const': 1., 'd': d})).fit()
        full = sm.OLS(y, pd.DataFrame({'const': 1., 'd': d, 'z': z})).fit()
        r2_dz = np.corrcoef(d, z)[0, 1] ** 2
        residual_z = sm.OLS(z, short.model.exog).fit().resid
        r2_yz = np.corrcoef(short.resid, residual_z)[0, 1] ** 2
        self.assertAlmostEqual(rf.ovb_magnitude(short, 'd', r2_yz, r2_dz), abs(short.params.d - full.params.d), places=10)
        rv = rf.point_sensitivity(short, 'd')['rv_to_zero_equal_strength']
        self.assertAlmostEqual(rf.ovb_magnitude(short, 'd', rv, rv), abs(short.params.d), places=10)

    def test_future_stock_bars_and_missing_benchmark_are_not_imputed(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            dates = ['2026-01-05', '2026-01-06', '2026-01-07']
            bars = [{'date': day, 'close': close, 'turnover': 100.} for day, close in zip(dates, [10., 11., 50.])]
            (path / 'hk00001.json').write_text(json.dumps(bars))
            benchmark = pd.Series([100., 102.], index=pd.to_datetime([dates[0], dates[2]]))
            sample = pd.DataFrame({'Stock Code': ['1.HK'], 'listing_date': [pd.Timestamp(dates[0])]})
            with patch.object(ac.et, 'BARS', path), patch.object(ac.et, 'load_bars', return_value=benchmark):
                frames, _ = ac.load_event_frame(sample, '2026-01-06')
            self.assertEqual(len(frames['1.HK']), 2)
            self.assertTrue(np.isnan(frames['1.HK'].ex_hsi.iloc[-1]))


if __name__ == '__main__':
    unittest.main()
