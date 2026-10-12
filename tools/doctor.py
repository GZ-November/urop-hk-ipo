#!/usr/bin/env python3
"""Check runtime imports and collection assets; never install or approve evidence."""
from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PROFILES = {
    "core": ["openpyxl", "yaml", "requests", "fitz", "xlrd"],
    "analysis": ["pandas", "numpy", "scipy", "statsmodels", "matplotlib"],
    "dev": ["pytest", "flake8"],
}
ASSETS = ["uv.lock", "pipeline/templates/HKIPO-MB-template-final.xlsx",
          "pipeline/prospectus_pipeline/config.yaml",
          "pipeline/prospectus_pipeline/schema/fields.json",
          "pipeline/prospectus_pipeline/schema/allot_fields.json",
          "pipeline/templates/HKIPO-GEM-template-final.xlsx",
          "pipeline/prospectus_pipeline/gem_base.yaml",
          "pipeline/prospectus_pipeline/schema/gem_fields.json",
          "pipeline/prospectus_pipeline/schema/gem_prospectus_fields.json"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=tuple(PROFILES), default="dev")
    parser.add_argument("--network", action="store_true", help="Probe HKEX and HKMA with bounded HTTP GETs")
    parser.add_argument("--output", type=Path, help="Save JSON diagnostics")
    args = parser.parse_args()
    checks = [{"name": "Python >= 3.9", "ok": sys.version_info >= (3, 9), "detail": sys.version.split()[0]}]
    modules = PROFILES["core"][:]
    if args.profile != "core":
        modules += PROFILES["analysis"]
    if args.profile == "dev":
        modules += PROFILES["dev"]
    for module in modules:
        try:
            importlib.import_module(module)
            checks.append({"name": module, "ok": True})
        except Exception as exc:
            checks.append({"name": module, "ok": False, "detail": str(exc)})
    checks += [{"name": asset, "ok": (ROOT / asset).is_file()} for asset in ASSETS]
    if args.network:
        for name, url in {
            "HKEX listing reports": "https://www2.hkexnews.hk/New-Listings/New-Listing-Information/Main-Board?sc_lang=en",
            "HKEX issuer search": "https://www1.hkexnews.hk/search/prefix.do?callback=cb&lang=EN&type=A&name=700&market=SEHK",
            "HKMA": "https://api.hkma.gov.hk/public/market-data-and-statistics/daily-monetary-statistics/daily-figures-interbank-liquidity?pagesize=1",
        }.items():
            try:
                request = urllib.request.Request(url, headers={"User-Agent": "HKIPO-research-doctor/1.0"})
                with urllib.request.urlopen(request, timeout=15) as response:
                    ok = response.status == 200 and bool(response.read(256))
                checks.append({"name": name, "ok": ok})
            except Exception as exc:
                checks.append({"name": name, "ok": False, "detail": str(exc)})
    report = {"passed": all(item["ok"] for item in checks), "checks": checks,
              "note": "Import/assets/connectivity checks do not certify source semantics or dataset completeness."}
    for item in checks:
        print(f"{'PASS' if item['ok'] else 'FAIL'} {item['name']} {item.get('detail', '')}")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
