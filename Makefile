# ==============================================================================
# HK IPO Pipeline Master Makefile
# ==============================================================================

.PHONY: help env status audit cross_check report export registry master evidence exclusions aftermarket-refresh test check lint clean weekly-report

help:
	@echo "Hong Kong Main Board IPO Pipeline Toolkit Commands:"
	@echo "  make env           - Check and bootstrap runtime dependencies (Python 3.9+, openpyxl, etc.)"
	@echo "  make status        - Display pipeline state and hash-gate alignment for issuers"
	@echo "  make audit         - Run read-only cell-by-cell audit against verified extractions"
	@echo "  make cross_check   - Run HKEX Listing Rules & cross-field econometric consistency audit"
	@echo "  make report        - Generate macro market and academic research report"
	@echo "  make weekly-report - Compile official Faculty Progress Word Report (DOCX)"
	@echo "  make export        - Export clean econometric CSV and live-schema academic Codebook"
	@echo "  make registry      - Merge quarterly Codebooks into the machine-readable variable registry (YAML)"
	@echo "  make master        - Merge all cohort clean CSVs into the master panel + drift report"
	@echo "  make evidence      - Freeze SHA-256 evidence manifest of all research data artifacts"
	@echo "  make exclusions    - Generate per-cohort sample selection logs (inclusion/exclusion reasons)"
	@echo "  make aftermarket-refresh - Refresh aftermarket columns for every cohort config"
	@echo "  make test          - Run full automated regression and safety test suite"
	@echo "  make lint          - Verify Python syntax and bytecode compilation"
	@echo "  make clean         - Remove cached bytecode and temporary compilation files"
	@echo "  make check         - Run complete health inspection (status + audit + cross_check + test + registry-check)"

env:
	@./.agents/skills/hk-ipo-pipeline/scripts/check_env.sh

status:
	@python3 run.py status

audit:
	@python3 run.py audit --target all

cross_check:
	@python3 run.py cross_check

report:
	@python3 run.py report

weekly-report:
	@python3 run.py report-weekly

export:
	@python3 run.py export

registry:
	@python3 run.py registry

master:
	@python3 run.py master

evidence:
	@python3 run.py evidence

exclusions:
	@for cfg in prospectus_pipeline/config_2025q1.yaml prospectus_pipeline/config_2025q2.yaml \
	            prospectus_pipeline/config_2026q1.yaml prospectus_pipeline/config_2026q2.yaml \
	            prospectus_pipeline/config_2026q3.yaml; do \
		echo "=== exclusions: $$cfg ==="; python3 run.py exclusions --config $$cfg || exit 1; done

aftermarket-refresh:
	@for cfg in prospectus_pipeline/config_2025q1.yaml prospectus_pipeline/config_2026q1.yaml \
	            prospectus_pipeline/config_2026q2.yaml prospectus_pipeline/config_2026q3.yaml; do \
		echo "=== aftermarket: $$cfg ==="; python3 run.py aftermarket --config $$cfg || exit 1; done

test:
	@python3 -m unittest discover -s "pipeline/prospectus_pipeline/tests" -v

lint:
	@python3 -m py_compile run.py
	@find "pipeline/prospectus_pipeline/src" -name "*.py" -exec python3 -m py_compile {} +
	@find "pipeline/prospectus_pipeline/tools" -name "*.py" -exec python3 -m py_compile {} +
	@find "pipeline/prospectus_pipeline/tools" -name "*.py" -exec python3 -m py_compile {} +
	@echo "✅ All Python files passed syntax compilation!"

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.py[cod]" -delete 2>/dev/null || true
	@rm -rf .pytest_cache
	@echo "✅ Cleaned all temporary caches."

registry-check:
	@python3 run.py registry --check

check: status audit cross_check test registry-check
	@echo "=================================================================="
	@echo "✅ ALL PIPELINE CHECKS PASSED: Pipeline & Toolkit 100% Verified!"
	@echo "=================================================================="
