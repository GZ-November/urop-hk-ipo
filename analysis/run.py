#!/usr/bin/env python3
"""Run one or more 2026 studies in a stable order, stopping at the first failure.

Run scripts in separate processes to isolate plotting and study state. Listing
studies imports no econometrics code and does not read or write research data.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Study:
    name: str
    script: str
    output: str | None
    description: str
    run_by_default: bool = True


STUDIES = (
    Study("basic", "basic_statistics_2026", "basic_statistics", "Coverage and basic statistics", False),
    Study("descriptive", "module_a_stylized_facts", "module_a", "Descriptive statistics"),
    Study("underpricing", "module_b_underpricing_regression", "module_b", "First-day return regressions"),
    Study("decomposition", "ir_decomposition_2026", "ir_decomposition", "Return decomposition"),
    Study("q2", "q2_breakdown_2026", "q2_breakdown", "Second-quarter analysis"),
    Study("monthly", "monthly_breakdown_2026", "monthly_breakdown", "Monthly patterns"),
    Study("coverage", "testability_screen_2026", None, "Variable coverage screen"),
    Study("extended", "extended_analysis_2026", "extended", "Mechanisms and robustness"),
    Study("aftermarket", "aftermarket_event_time_2026", "event_time", "Aftermarket returns"),
    Study("academic", "academic_extensions_2026", "academic", "Lockups and academic extensions"),
    Study("ah", "ah_anchor_2026", "ah_anchor", "A+H price anchors"),
    Study("margin", "margin_financing_2026", "margin", "Margin financing"),
    Study("retail", "research_frontier_2026", "research_frontier", "Retail returns and cornerstone sensitivity"),
    Study("demand", "subscription_heat_2026", "subscription_heat", "Subscription demand and first-day return / break rate"),
    Study("allocation_profit", "retail_allocation_profit_2026", "retail_profit", "Retail allocation rates, expected allocation and profit"),
    Study("retail_distribution", "retail_profit_distribution_2026", "retail_distribution", "Retail profit distributions and fee frontiers", False),
)


def run_studies(studies: list[Study], root: Path = ROOT) -> int:
    """Run registered studies with this interpreter and return the first failure."""
    for study in studies:
        script = root / "analysis" / f"{study.script}.py"
        if not script.is_file():
            raise ValueError(f"Missing study script: {script}")
    for study in studies:
        print(f"Running {study.name}: {study.description}", flush=True)
        result = subprocess.run([sys.executable, str(root / "analysis" / f"{study.script}.py")], cwd=root)
        if result.returncode:
            return result.returncode
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="List studies without running analysis")
    parser.add_argument("--study", action="append", choices=[s.name for s in STUDIES], help="Select studies; repeat to select more than one")
    args = parser.parse_args(argv)
    if args.list:
        for study in STUDIES:
            output = f"analysis/out/{study.output}" if study.output else "console"
            print(f"{study.name:14} {study.description:40} {output}")
        return 0
    selected = [s for s in STUDIES if (s.name in args.study if args.study else s.run_by_default)]
    try:
        return run_studies(selected)
    except ValueError as exc:
        parser.error(str(exc))
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
