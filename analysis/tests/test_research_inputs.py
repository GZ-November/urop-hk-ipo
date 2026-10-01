"""Shared-input isolation, compatibility and issuer alignment contracts."""
from pathlib import Path
import subprocess
import sys
import unittest

import pandas as pd

ANALYSIS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ANALYSIS))
import research_inputs as inputs


class ResearchInputTests(unittest.TestCase):
    def test_import_does_not_load_reporting_or_estimation_modules(self):
        code = """
import sys
import research_inputs
assert not any(name in sys.modules for name in (
    'module_a_stylized_facts', 'module_b_underpricing_regression',
    'extended_analysis_2026', 'academic_extensions_2026',
    'matplotlib', 'statsmodels',
))
"""
        subprocess.run([sys.executable, "-c", code], cwd=ANALYSIS, check=True)

    def test_previous_input_names_are_the_same_implementation(self):
        import module_a_stylized_facts as a
        import module_b_underpricing_regression as b
        import extended_analysis_2026 as extended
        import academic_extensions_2026 as academic

        self.assertIs(a.load_panel, inputs.load_panel)
        self.assertIs(a.select_2026, inputs.select_2026)
        self.assertIs(b.prepare, inputs.prepare_regression)
        self.assertIs(extended.prepare, inputs.prepare_extended)
        self.assertIs(academic.build_frame, inputs.prepare_academic)

    def test_shared_frames_keep_issuer_alignment_after_input_reordering(self):
        if not inputs.MASTER.is_file():
            self.skipTest("Versioned master panel is unavailable")
        panel = inputs.select_2026(inputs.load_panel())
        reordered = panel.sample(frac=1, random_state=7).copy()
        # Nonconsecutive labels expose positional assignments after sorting.
        reordered.index = range(1000, 1000 + len(reordered) * 3, 3)
        for prepare in (inputs.prepare_regression, inputs.prepare_extended,
                        inputs.prepare_academic):
            with self.subTest(prepare=prepare.__name__):
                expected = prepare(panel).set_index("code").sort_index()
                actual = prepare(reordered).set_index("code").sort_index()
                # Reordered rolling means change floating-point summation order.
                pd.testing.assert_frame_equal(expected, actual, check_exact=False,
                                              rtol=1e-12, atol=1e-14)
                self.assertEqual(len(actual), len(panel))


if __name__ == "__main__":
    unittest.main()
