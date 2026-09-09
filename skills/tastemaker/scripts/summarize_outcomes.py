#!/usr/bin/env python3
"""Summarize kept/rejected rates from cross-project structure and copy history.

Rotation (check_structure_history.py, check_copy_diversity.py) enforces
*variety* — never repeat the last pick — but has no opinion about *quality*.
This script reads the outcome field that references/diversification.md and
references/copy-voice.md ask Step 5 to patch in after a design pass resolves
to kept/rejected, and reports which archetypes and copy angles actually tend
to get kept across projects.

Use it as a tie-break among already-rotation-legal candidates at Step 2.5 —
never to justify repeating the immediately previous build's pick, and never
trust a bucket with too few resolved entries to mean anything.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

DEFAULT_STRUCTURE_LOG = Path.home() / ".tastemaker" / "structure-history.json"
DEFAULT_COPY_LOG = Path.home() / ".tastemaker" / "copy-history.json"
STRUCTURE_FIELDS = ("macrostructure", "nav", "hero", "footer")
COPY_FIELDS = ("angle",)
MIN_RESOLVED_FOR_SIGNAL = 4


def load_entries(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return data if isinstance(data, list) else []


def summarize(entries: list[dict], fields: tuple[str, ...]) -> dict[str, dict[str, dict[str, int]]]:
    """field -> value -> {kept, rejected, pending} counts."""
    counts: dict[str, dict[str, dict[str, int]]] = {f: defaultdict(lambda: defaultdict(int)) for f in fields}
    for entry in entries:
        outcome = entry.get("outcome", "pending")
        for field in fields:
            value = entry.get(field)
            if not value:
                continue
            counts[field][value][outcome] += 1
    return counts


def print_summary(title: str, counts: dict[str, dict[str, dict[str, int]]]) -> None:
    print(f"\n{title}")
    print("=" * len(title))
    for field, values in counts.items():
        print(f"\n{field}:")
        rows = []
        for value, outcomes in values.items():
            kept = outcomes.get("kept", 0)
            rejected = outcomes.get("rejected", 0)
            pending = outcomes.get("pending", 0)
            resolved = kept + rejected
            if resolved == 0:
                rate = "n/a"
            else:
                rate = f"{kept / resolved:.0%}"
            confidence = "low-confidence (n<4)" if resolved < MIN_RESOLVED_FOR_SIGNAL else ""
            rows.append((value, kept, rejected, pending, rate, confidence))
        rows.sort(key=lambda r: (-r[1], r[0]))
        if not rows:
            print("  (no entries)")
            continue
        for value, kept, rejected, pending, rate, confidence in rows:
            note = f"  {confidence}" if confidence else ""
            print(f"  {value:<24} kept {kept:>2}  rejected {rejected:>2}  pending {pending:>2}  keep-rate {rate:>5}{note}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize kept/rejected rates from cross-project structure and copy history.")
    parser.add_argument("--structure-log", type=Path, default=DEFAULT_STRUCTURE_LOG)
    parser.add_argument("--copy-log", type=Path, default=DEFAULT_COPY_LOG)
    args = parser.parse_args()

    structure_entries = load_entries(args.structure_log)
    copy_entries = load_entries(args.copy_log)

    if not structure_entries and not copy_entries:
        print("No history found — no ~/.tastemaker/structure-history.json or copy-history.json entries yet.")
        print("This is normal on early runs: outcome data accumulates as Step 5 resolves decisions.")
        return 0

    print_summary(f"Structure outcomes ({len(structure_entries)} entries, {args.structure_log})", summarize(structure_entries, STRUCTURE_FIELDS))
    print_summary(f"Copy angle outcomes ({len(copy_entries)} entries, {args.copy_log})", summarize(copy_entries, COPY_FIELDS))

    print(
        "\nUse this as a tie-break among candidates that already pass the rotation rule "
        "(diversification.md) — never to justify repeating the last build's pick, and never "
        "for a bucket marked low-confidence."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
