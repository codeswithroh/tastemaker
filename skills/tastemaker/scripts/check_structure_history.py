#!/usr/bin/env python3
"""Flag structural repetition across tastemaker builds — project-local and cross-project.

`.tastemaker/log.json` only prevents a project from repeating itself. Two
*different* projects can still both default to "Feature Stack" every time,
because nothing was ever comparing across projects. This script reads the
global `~/.tastemaker/structure-history.json` (written alongside the project
log after every build) and flags when a macrostructure or archetype is
over-represented in the recent global window, regardless of which project
built it.

This is a mechanical guardrail for Step 2.5 in SKILL.md, the same role
anti_slop_scan.py plays for Step 4: it doesn't replace the model's own
rotation statement, it catches the case where that statement was skipped.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

DEFAULT_GLOBAL_PATH = Path.home() / ".tastemaker" / "structure-history.json"
FIELDS = ("macrostructure", "nav", "hero", "footer")
# an axis is "hot" once it accounts for this fraction of the recent window
HOT_THRESHOLD = 0.6
MIN_WINDOW_FOR_HOT_CHECK = 3


def load_entries(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return data if isinstance(data, list) else []


def check_immediate_repeat(current: dict, previous: dict) -> list[str]:
    """The single-project rotation rule: don't repeat the *very last* build's picks."""
    problems = []
    for field in FIELDS:
        cur_val = current.get(field)
        prev_val = previous.get(field)
        if cur_val and prev_val and cur_val == prev_val:
            problems.append(
                f"{field} repeats the immediately previous build ('{cur_val}') — "
                f"reuse is only OK if you changed a variation knob and said so."
            )
    return problems


def check_hot_axis(current: dict, window: list[dict], window_size: int) -> list[str]:
    """The cross-project rule: don't pick what most recent builds everywhere already picked."""
    problems = []
    if len(window) < MIN_WINDOW_FOR_HOT_CHECK:
        return problems
    for field in FIELDS:
        cur_val = current.get(field)
        if not cur_val:
            continue
        counts = Counter(e.get(field) for e in window if e.get(field))
        total = sum(counts.values())
        if total == 0:
            continue
        share = counts.get(cur_val, 0) / total
        if share >= HOT_THRESHOLD:
            problems.append(
                f"{field} '{cur_val}' made up {counts[cur_val]}/{total} of the last "
                f"{window_size} builds across all projects — it's the hot default right now. "
                f"Only keep it if the brief specifically demands it, and say why."
            )
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check a build's structural picks against project and cross-project history."
    )
    parser.add_argument(
        "--current",
        required=True,
        type=Path,
        help="JSON file with this build's picks: {macrostructure, nav, hero, footer, ...}",
    )
    parser.add_argument(
        "--project-log",
        type=Path,
        default=Path(".tastemaker/log.json"),
        help="Path to this project's log.json (default: .tastemaker/log.json)",
    )
    parser.add_argument(
        "--global-log",
        type=Path,
        default=DEFAULT_GLOBAL_PATH,
        help=f"Path to the cross-project structure history (default: {DEFAULT_GLOBAL_PATH})",
    )
    parser.add_argument(
        "--window",
        type=int,
        default=5,
        help="How many recent global entries count toward the 'hot axis' check (default: 5)",
    )
    args = parser.parse_args()

    if not args.current.exists():
        print(f"error: --current file not found: {args.current}")
        return 2
    try:
        current = json.loads(args.current.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"error: --current is not valid JSON: {exc}")
        return 2

    project_entries = load_entries(args.project_log)
    global_entries = load_entries(args.global_log)

    problems: list[str] = []

    if project_entries:
        problems.extend(check_immediate_repeat(current, project_entries[0]))

    window = global_entries[: args.window]
    problems.extend(check_hot_axis(current, window, len(window)))

    if not problems:
        scope = f"{len(project_entries)} project + {len(global_entries)} global entries"
        print(f"Structure check passed ({scope} checked): pick reads as distinct.")
        return 0

    print("Structural repetition flagged:")
    for problem in problems:
        print(f"  - {problem}")
    print(
        "\nThis is a nudge, not a hard block — a repeat can be the right call if the brief "
        "asks for it. State the reason before shipping it."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
