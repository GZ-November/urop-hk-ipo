# Deterministic retail evidence brief

113 corrected one-lot IPOs; cutoff 30 September 2026. No simulation.

Run `.venv/bin/python tools/audit_retail_sources_2026.py` then `.venv/bin/python analysis/retail_evidence_brief_2026.py` from the root. Raw source PDFs must be available at the paths in the source manifest.

[Mentor brief](../../../docs/reports/RETAIL_MENTOR_BRIEF_2026-10-03.md) · [Evidence assessment](../../../docs/reports/RETAIL_EVIDENCE_ASSESSMENT_2026-10-03.md). CSV returns are decimals; covariance columns ending in `_pp` are percentage points. The median after-fee profit is the median across IPO expectations, not a simulated portfolio median.
