#!/usr/bin/env python3
"""Install this repository's agent skills where Claude Code and Codex discover them.

`.agents/skills/` is the single source. Project scope links each skill into
`.claude/skills/` (Codex already reads `.agents/skills/` in a checkout). User
scope links them into `~/.claude/skills/` and `~/.agents/skills/` so the agent
finds them from any directory. Links follow later edits; where symbolic links
are unavailable, a marked copy is made and refreshed on the next install.
Directories or links this tool did not create are reported and kept.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".agents" / "skills"
MARKER = ".installed-from"


def available_skills(source: Path = SOURCE) -> list[Path]:
    return sorted(path for path in source.iterdir() if (path / "SKILL.md").is_file())


def destinations(scope: str, root: Path = ROOT, home: Path | None = None) -> list[Path]:
    home = home or Path.home()
    project = [root / ".claude" / "skills"]
    user = [home / ".claude" / "skills", home / ".agents" / "skills"]
    return {"project": project, "user": user, "both": project + user, "none": []}[scope]


def link_target(skill: Path, directory: Path, root: Path) -> str:
    """Relative inside the checkout so a moved clone keeps working; absolute elsewhere."""
    if directory.resolve().is_relative_to(root.resolve()):
        return os.path.relpath(skill.resolve(), directory.resolve())
    return str(skill.resolve())


def inspect(skill: Path, destination: Path) -> str:
    """Classify a destination as linked, copied, broken, missing or foreign."""
    if destination.is_symlink():
        if not destination.exists():
            # A dangling link left by a moved or deleted checkout of this repository.
            ours = Path(os.readlink(destination)).parts[-3:] == (".agents", "skills", skill.name)
            return "broken" if ours else "foreign"
        return "linked" if destination.resolve() == skill.resolve() else "foreign"
    if destination.is_dir():
        marker = destination / MARKER
        if marker.is_file() and marker.read_text(encoding="utf-8").strip() == str(skill.resolve()):
            return "copied"
        return "foreign"
    return "foreign" if destination.exists() else "missing"


def install(skill: Path, directory: Path, root: Path = ROOT) -> str:
    """Link (or copy) one skill; replace only broken links and this tool's own copies."""
    destination = directory / skill.name
    state = inspect(skill, destination)
    if state == "linked":
        return "already linked"
    if state == "foreign":
        return "kept existing entry not created by this tool"
    directory.mkdir(parents=True, exist_ok=True)
    if destination.is_symlink():
        destination.unlink()
    elif destination.is_dir():
        shutil.rmtree(destination)
    try:
        destination.symlink_to(link_target(skill, directory, root), target_is_directory=True)
        return "linked"
    except OSError:
        shutil.copytree(skill, destination)
        (destination / MARKER).write_text(str(skill.resolve()) + "\n", encoding="utf-8")
        return "copied (rerun after editing the skill)"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--scope", choices=("project", "user", "both", "none"), default="project")
    parser.add_argument("--skill", action="append", help="Install only this skill name (repeatable)")
    parser.add_argument("--check", action="store_true", help="Report without changing anything")
    args = parser.parse_args(argv)
    skills = available_skills()
    if args.skill:
        unknown = set(args.skill) - {skill.name for skill in skills}
        if unknown:
            parser.error(f"Unknown skill(s): {', '.join(sorted(unknown))}")
        skills = [skill for skill in skills if skill.name in args.skill]
    complete = True
    for directory in destinations(args.scope):
        for skill in skills:
            if args.check:
                state = inspect(skill, directory / skill.name)
                complete &= state in ("linked", "copied")
            else:
                state = install(skill, directory)
            print(f"{skill.name:<24} {directory / skill.name}: {state}")
    return 0 if complete or not args.check else 1


if __name__ == "__main__":
    sys.exit(main())
