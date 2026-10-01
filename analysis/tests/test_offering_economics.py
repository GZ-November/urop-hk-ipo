"""Guard estimands, accounting identities and nonzero-null inference."""
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.special import expit

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import offering_economics_2026 as research


class OfferingEconomicsTests(unittest.TestCase):
    def test_nonzero_null_bootstrap_matches_shifted_outcome(self):
        rng = np.random.default_rng(5)
        size = rng.normal(size=72)
        z = pd.DataFrame({"ln_size": size, "month_id": np.repeat(["a", "b", "c", "d", "e", "f"], 12)})
        z["outcome"] = .4 * size + rng.normal(size=72)
        z["shifted"] = z.outcome - z.ln_size
        nonzero = research.focal_test(z, "outcome", ["ln_size"], "ln_size", 1.)
        zero = research.focal_test(z, "shifted", ["ln_size"], "ln_size", 0.)
        self.assertAlmostEqual(nonzero["Restricted wild p"], zero["Restricted wild p"])
        self.assertAlmostEqual(nonzero["HC3 p"], zero["HC3 p"])
        self.assertAlmostEqual(nonzero["Coefficient"]-1, zero["Coefficient"])

    def test_finite_fractional_contrast_keeps_bounds(self):
        x = np.array([[1., -2.], [1., 0.], [1., 2.]])
        params = np.array([-1., .8])
        expected = 100 * np.mean(expit(x @ params + .8*np.log(2)) - expit(x @ params))
        self.assertAlmostEqual(research.doubling_share(params, x, 1), expected)
        self.assertTrue(0 < expected < 100)

    def test_rank_failure_is_not_silently_estimated(self):
        z = pd.DataFrame({"a": [1., 2., 3., 4.], "b": [2., 4., 6., 8.]})
        with self.assertRaises(ValueError):
            research.design(z, ["a", "b"])

    def test_subscription_identity_and_sample_cutoff(self):
        z = research.prepare()
        self.assertEqual(len(z), 113)
        self.assertEqual(z.code.nunique(), 113)
        self.assertTrue(z.listing_date.le(research.CUTOFF).all())
        np.testing.assert_allclose(z.ln_multiple, z.ln_applicants + z.ln_avg_application - z.ln_initial_public_value, atol=1e-12)
        self.assertFalse(z.coarse_sector.isna().any())
        # The four discrepant reported multiples must not be overwritten.
        self.assertGreater((abs(z.constructed_multiple/z.subscription-1)>.01).sum(), 0)


if __name__ == "__main__":
    unittest.main()
