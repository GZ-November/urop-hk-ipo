#!/usr/bin/env python3
"""Create or verify the English research index from its artifact catalog.

Preflight every source and destination before changing links. Existing files
are never replaced. Canonical data and analysis outputs stay with their producer.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "config/research_workspace.json"


def _inside(root: Path, value: str) -> Path:
    path = root / value
    if Path(value).is_absolute() or ".." in Path(value).parts:
        raise ValueError(f"Catalog paths must be relative: {value}")
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Catalog path leaves project: {value}")
    return path


def workspace_links(root: Path, catalog: dict) -> list[tuple[Path, Path]]:
    """Resolve a complete catalog, rejecting missing sources and unsafe conflicts."""
    if catalog.get("version") != 1:
        raise ValueError("Unsupported workspace catalog version")
    directory = _inside(root, catalog["directory"])
    links = []
    destinations = set()
    for entry in catalog["entries"]:
        destination = _inside(root, str(directory.relative_to(root) / entry["name"]))
        source = _inside(root, entry["source"])
        if destination in destinations:
            raise ValueError(f"Duplicate workspace destination: {destination}")
        destinations.add(destination)
        if not source.exists():
            raise ValueError(f"Missing source: {source}")
        if destination.is_symlink():
            if destination.resolve() != source.resolve():
                raise ValueError(f"Conflicting link preserved: {destination}")
        elif destination.exists():
            raise ValueError(f"Existing file preserved: {destination}")
        links.append((destination, source))
    return links


def synchronize(root: Path, catalog: dict, *, check: bool = False) -> int:
    """Create missing links, or fail if the index is incomplete in check mode."""
    links = workspace_links(root, catalog)
    missing = [(destination, source) for destination, source in links if not destination.is_symlink()]
    if check and missing:
        raise ValueError(f"Missing workspace links: {len(missing)}; run workspace without --check")
    for destination, source in missing:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.symlink_to(os.path.relpath(source, destination.parent), target_is_directory=source.is_dir())
    return len(links)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check links without changing files")
    args = parser.parse_args(argv)
    try:
        count = synchronize(ROOT, json.loads(CATALOG.read_text(encoding="utf-8")), check=args.check)
    except (OSError, ValueError, KeyError) as exc:
        parser.error(str(exc))
    print(f"Research workspace: {count} links verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
