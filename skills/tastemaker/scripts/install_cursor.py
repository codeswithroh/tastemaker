#!/usr/bin/env python3
"""
Install a project-local Cursor rule (.cursor/rules/tastemaker.mdc) and copy
supporting skill bundles (references, scripts, assets, ideagram) into .tastemaker/skill/
while rewriting internal relative links so Cursor agents resolve paths seamlessly.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
from pathlib import Path

SKILL_DIRS = ("references", "scripts", "assets", "ideagram")
MDC_HEADER = """---
description: Tastemaker UI design system, anti-slop rules, palette generator and typography
globs: *
---

"""


def find_skill_root(start: Path) -> Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / "skills" / "tastemaker" / "SKILL.md").is_file():
            return parent / "skills" / "tastemaker"
        if (parent / "SKILL.md").is_file() and any((parent / d).is_dir() for d in SKILL_DIRS):
            return parent
    raise FileNotFoundError("Could not find tastemaker SKILL.md and supporting directories")


def rewrite_paths(content: str) -> str:
    # Rewrite references/, scripts/, assets/, and ideagram/ to .tastemaker/skill/<dir>
    for dir_name in SKILL_DIRS:
        pattern = rf"(?<!\.tastemaker/skill/)(?<![a-zA-Z0-9_\-\./])({dir_name}/)"
        content = re.sub(pattern, rf".tastemaker/skill/", content)
    return content


def install(target_project: Path, skill_root: Path) -> None:
    target_project = target_project.resolve()
    skill_root = skill_root.resolve()

    target_skill_dir = target_project / ".tastemaker" / "skill"
    rules_dir = target_project / ".cursor" / "rules"

    target_skill_dir.mkdir(parents=True, exist_ok=True)
    rules_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copy supporting directories
    for dir_name in SKILL_DIRS:
        src = skill_root / dir_name
        dst = target_skill_dir / dir_name
        if src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)

    # 2. Convert and install SKILL.md -> tastemaker.mdc
    skill_file = skill_root / "SKILL.md"
    if not skill_file.is_file():
        raise FileNotFoundError(f"Missing {skill_file}")

    raw_content = skill_file.read_text(encoding="utf-8")
    rewritten_content = rewrite_paths(raw_content)

    mdc_file = rules_dir / "tastemaker.mdc"
    mdc_file.write_text(MDC_HEADER + rewritten_content, encoding="utf-8")

    print(f"✓ Installed Cursor rule: {mdc_file}")
    print(f"✓ Preserved supporting skill directories in: {target_skill_dir}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Tastemaker in Cursor projects.")
    parser.add_argument("target", nargs="?", default=".", help="Target project directory (default: current directory)")
    args = parser.parse_args()

    try:
        skill_root = find_skill_root(Path(__file__).parent)
        install(Path(args.target), skill_root)
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
