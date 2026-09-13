# Contributing to UROP HK IPO Pipeline

Thank you for contributing to the HK IPO automated pipeline and econometric research toolkit!

This document provides technical guidelines for teammates, researchers, and developers.

---

## 1. Development Principles

1. **Zero Data in Git**:
   - **Never commit `.xlsx`, `.csv`, `.pdf`, `.docx`, or extracted company JSONs** to version control.
   - All collected data, intermediate results, and local snapshots are strictly ignored by `.gitignore`.
2. **Deterministic-First**:
   - Computations, formulas, and table parsers must be deterministic Python (0 LLM Token cost).
   - Reserve AI Agent models strictly for unstructured text extraction and semantic verification.
3. **Fail-Closed Gatekeeping**:
   - Never bypass hash signatures or schema validation contracts (`schema/fields.json`, `schema/allot_fields.json`).
4. **Non-Destructive Write-Back**:
   - When modifying Excel write-back logic, never alter workbook styling, fonts, or cell formats.
   - Always ensure automated backups in `backups/excel_snapshots/` are triggered prior to saving.

---

## 2. Environment Setup

```bash
# Clone the repository
git clone https://github.com/GZ-November/urop-hk-ipo.git
cd urop-hk-ipo

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 3. Standard Development Workflow

1. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Run Tests Locally**:
   Before submitting changes, ensure all unit tests and safety checks pass:
   ```bash
   make test
   # Or directly:
   python3 -m unittest discover -s "Data Collecting Templates/News/prospectus_pipeline/tests" -v
   ```

3. **Check Code Quality**:
   - Format according to `.editorconfig` (4-space indent, UTF-8, LF).
   - Ensure all public functions and CLI subcommands have informative docstrings and type hints.

4. **Verify Pipeline State**:
   ```bash
   python run.py status
   ```

5. **Submit a Pull Request**:
   - Open a PR against `main`.
   - Ensure CI tests pass across all Python versions.

---

## 4. Adding New Listing Rules or Fields

- **To add new Listing Rules cross-checks**:
  Modify [`src/cross_check.py`](file:///Data%20Collecting%20Templates/News/prospectus_pipeline/src/cross_check.py) and add corresponding unit test cases in [`tests/test_cross_check.py`](file:///Data%20Collecting%20Templates/News/prospectus_pipeline/tests/test_cross_check.py).
- **To update field schemas**:
  Update [`schema/fields.json`](file:///Data%20Collecting%20Templates/News/prospectus_pipeline/schema/fields.json) or [`schema/allot_fields.json`](file:///Data%20Collecting%20Templates/News/prospectus_pipeline/schema/allot_fields.json).
