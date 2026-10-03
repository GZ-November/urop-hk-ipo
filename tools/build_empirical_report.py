"""Build the focused, data-driven retail report; uses no hardcoded empirical claims."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

if __name__ == '__main__':
    raise SystemExit(subprocess.call([sys.executable, str(ROOT / 'analysis/retail_profit_distribution_2026.py')], cwd=ROOT))
