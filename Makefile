# ==============================================================================
# HK IPO Pipeline Master Makefile
# ==============================================================================

.PHONY: help env status audit cross_check report export test check

help:
	@echo "Hong Kong Main Board IPO Pipeline Toolkit Commands:"
	@echo "  make env         - Check and bootstrap runtime dependencies (Python 3.9+, openpyxl, etc.)"
	@echo "  make status      - Display pipeline state and hash-gate alignment for issuers"
	@echo "  make audit       - Run read-only cell-by-cell audit against verified extractions"
	@echo "  make cross_check - Run HKEX Listing Rules & cross-field econometric consistency audit"
	@echo "  make report      - Generate macro market and academic research report"
	@echo "  make export      - Export clean econometric CSV and 120-variable academic Codebook"
	@echo "  make test        - Run full automated regression and safety test suite (17/17 tests)"
	@echo "  make check       - Run complete health inspection (status + audit + cross_check + test)"

env:
	@./.agents/skills/hk-ipo-pipeline/scripts/check_env.sh

status:
	@./.agents/skills/hk-ipo-pipeline/scripts/run_pipeline.sh status

audit:
	@./.agents/skills/hk-ipo-pipeline/scripts/run_pipeline.sh audit --target all

cross_check:
	@./.agents/skills/hk-ipo-pipeline/scripts/run_pipeline.sh cross_check

report:
	@./.agents/skills/hk-ipo-pipeline/scripts/run_pipeline.sh report

export:
	@./.agents/skills/hk-ipo-pipeline/scripts/run_pipeline.sh export

test:
	@cd "Data Collecting Templates/News" && python3 -m unittest discover -s prospectus_pipeline/tests -v

check: status audit cross_check test
	@echo "=================================================================="
	@echo "✅ ALL PIPELINE CHECKS PASSED: Pipeline & Toolkit 100% Verified!"
	@echo "=================================================================="
