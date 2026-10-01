# ==============================================================================
# HK IPO Pipeline Master Makefile
# ==============================================================================

PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
COHORT_CONFIGS := $(patsubst pipeline/%,%,$(sort $(wildcard pipeline/prospectus_pipeline/config_*.yaml)))
CONFIGS_2026 := $(patsubst pipeline/%,%,$(sort $(wildcard pipeline/prospectus_pipeline/config_2026q*.yaml)))
PYTHON_SOURCES := run.py analysis pipeline/run.py pipeline/prospectus_pipeline/run.py pipeline/prospectus_pipeline/src pipeline/prospectus_pipeline/tools pipeline/prospectus_pipeline/tests

.PHONY: margin-reference refresh-2026 help env status audit cross_check report export registry registry-check master evidence exclusions aftermarket-refresh test test-pipeline test-analysis analysis check check-code lint clean weekly-report

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
	@echo "  make lint          - Compile maintained Python sources and run required static checks"
	@echo "  make refresh-2026  - Refresh 2026 aftermarket bars, clear immature window stats, re-export, refresh A-share references, rebuild master and analysis"
	@echo "  make analysis      - Regenerate statistics and regressions for 2026 listings only"
	@echo "  make check-code    - Run lint, portable/acceptance tests and registry consistency"
	@echo "  make clean         - Remove cached bytecode and temporary compilation files"
	@echo "  make check         - Run complete health inspection (status + audit + cross_check + test + registry-check)"

env:
	@./.agents/skills/hk-ipo-pipeline/scripts/check_env.sh

status:
	@"$(PYTHON)" run.py status

audit:
	@"$(PYTHON)" run.py audit --target all

cross_check:
	@"$(PYTHON)" run.py cross_check

report:
	@"$(PYTHON)" run.py report

weekly-report:
	@"$(PYTHON)" run.py report-weekly

export:
	@"$(PYTHON)" run.py export

registry:
	@"$(PYTHON)" run.py registry

master:
	@"$(PYTHON)" run.py master

evidence:
	@"$(PYTHON)" run.py evidence

exclusions:
	@for cfg in $(COHORT_CONFIGS); do \
		"$(PYTHON)" run.py exclusions --config $$cfg || exit 1; done

aftermarket-refresh:
	@for cfg in $(COHORT_CONFIGS); do \
		"$(PYTHON)" run.py aftermarket --config $$cfg || exit 1; done

test: test-pipeline test-analysis

test-pipeline:
	@"$(PYTHON)" -m unittest discover -s "pipeline/prospectus_pipeline/tests" -v

test-analysis:
	@"$(PYTHON)" -m unittest discover -s "analysis/tests" -v

# Run when new listing windows have matured (e.g. Q2 six-month windows from mid-October 2026). The analysis scripts read
# the refreshed daily bars directly, so Q2 lockup events enter the event studies without the expansion writer.
refresh-2026:
	@for cfg in $(CONFIGS_2026); do \
		PIPELINE_CONFIG="$(CURDIR)/pipeline/$$cfg" "$(PYTHON)" pipeline/prospectus_pipeline/tools/external/market.py || exit 1; \
		"$(PYTHON)" run.py academic --config $$cfg || exit 1; \
		"$(PYTHON)" run.py aftermarket --config $$cfg || exit 1; \
		"$(PYTHON)" pipeline/prospectus_pipeline/tools/blank_immature_window_stats.py --config $$cfg || exit 1; \
		"$(PYTHON)" run.py export --config $$cfg || exit 1; done
	@"$(PYTHON)" run.py master --derive
	@"$(PYTHON)" pipeline/prospectus_pipeline/tools/external/ah_reference.py --refresh
	@$(MAKE) analysis

margin-reference:
	@"$(PYTHON)" pipeline/prospectus_pipeline/tools/external/margin_reference.py

analysis:
	@for script in module_a_stylized_facts module_b_underpricing_regression ir_decomposition_2026 q2_breakdown_2026 monthly_breakdown_2026 testability_screen_2026 extended_analysis_2026 aftermarket_event_time_2026 academic_extensions_2026 ah_anchor_2026 margin_financing_2026 research_frontier_2026; do \
		"$(PYTHON)" analysis/$$script.py || exit 1; done

lint:
	@"$(PYTHON)" -m compileall -q $(PYTHON_SOURCES)
	@"$(PYTHON)" -m flake8 --select=F401,F811,F821,F541 $(PYTHON_SOURCES)
	@echo "✅ All Python files passed syntax compilation!"

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.py[cod]" -delete 2>/dev/null || true
	@rm -rf .pytest_cache
	@echo "✅ Cleaned all temporary caches."

registry-check:
	@"$(PYTHON)" run.py registry --check

check-code: lint test registry-check

check: status audit cross_check check-code
	@echo "=================================================================="
	@echo "✅ Configured pipeline and code checks passed; inspect audit coverage separately."
	@echo "=================================================================="
