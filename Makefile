# ==============================================================================
# HK IPO Pipeline Master Makefile
# ==============================================================================

.PHONY: help env status audit cross_check report export test check lint clean weekly-report

help:
	@echo "Hong Kong Main Board IPO Pipeline Toolkit Commands:"
	@echo "  make env           - Check and bootstrap runtime dependencies (Python 3.9+, openpyxl, etc.)"
	@echo "  make status        - Display pipeline state and hash-gate alignment for issuers"
	@echo "  make audit         - Run read-only cell-by-cell audit against verified extractions"
	@echo "  make cross_check   - Run HKEX Listing Rules & cross-field econometric consistency audit"
	@echo "  make report        - Generate macro market and academic research report"
	@echo "  make weekly-report - Compile official Faculty Progress Word Report (DOCX)"
	@echo "  make export        - Export clean econometric CSV and 120-variable academic Codebook"
	@echo "  make test          - Run full automated regression and safety test suite (20/20 tests)"
	@echo "  make lint          - Verify Python syntax and bytecode compilation"
	@echo "  make clean         - Remove cached bytecode and temporary compilation files"
	@echo "  make check         - Run complete health inspection (status + audit + cross_check + test)"

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

test:
	@python3 -m unittest discover -s "Data Collecting Pipeline/prospectus_pipeline/tests" -v

lint:
	@python3 -m py_compile run.py
	@find "Data Collecting Pipeline/prospectus_pipeline/src" -name "*.py" -exec python3 -m py_compile {} +
	@find "Data Collecting Pipeline/prospectus_pipeline/tools" -name "*.py" -exec python3 -m py_compile {} +
	@find "Data Collecting Pipeline/reports" -name "*.py" -exec python3 -m py_compile {} +
	@echo "✅ All Python files passed syntax compilation!"

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.py[cod]" -delete 2>/dev/null || true
	@rm -rf .pytest_cache
	@echo "✅ Cleaned all temporary caches."

check: status audit cross_check test
	@echo "=================================================================="
	@echo "✅ ALL PIPELINE CHECKS PASSED: Pipeline & Toolkit 100% Verified!"
	@echo "=================================================================="
