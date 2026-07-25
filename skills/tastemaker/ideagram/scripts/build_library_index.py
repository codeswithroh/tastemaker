#!/usr/bin/env python3
"""
Build a searchable index of a local unDraw library so matching a concept to
an illustration is a fast, accurate lookup instead of eyeballing filenames.

Why this exists: unDraw SVGs carry no per-file description (just an
`artist`/`source` attribute) — the filename slug is the only real metadata
(e.g. `undraw_content-team_1p7b.svg` -> "content team"). This script extracts
that slug into keywords, detects whether the file uses a secondary unDraw
accent (green/pink/etc. beyond the main purple) worth remapping too, and
writes both a human-scannable index.md and a machine-readable index.json
into the library folder itself. Re-run it whenever you add new SVGs.

Usage:
    python3 build_library_index.py                      # indexes ~/.ideagram/undraw
    python3 build_library_index.py --library /path/to/svgs
"""

import sys
import os
import re
import json
import argparse

DEFAULT_LIBRARY = os.path.expanduser("~/.ideagram/undraw")

# unDraw's known secondary ACCENT colors worth flagging for --also remapping.
# Deliberately excludes unDraw's skin-tone variants (#9f616a, #a0616a, #ffb6b6,
# #ed9da0, etc.) — those are skin, not a "pop" color, and must never be
# offered as something to recolor.
SECONDARY_ACCENTS = {
    "#8ed16f": "green",
    "#ff6584": "pink",
}


def slug_to_keywords(filename):
    """undraw_content-team_1p7b.svg -> ['content', 'team']"""
    base = os.path.splitext(filename)[0]
    m = re.match(r"^undraw_(.+)_[a-z0-9]+$", base)
    slug = m.group(1) if m else base
    return [w for w in slug.replace("_", "-").split("-") if w]


def detect_secondary_accents(text):
    found = []
    lowered = text.lower()
    for hex_color, name in SECONDARY_ACCENTS.items():
        if hex_color in lowered:
            found.append(f"{name} ({hex_color})")
    return found


def figure_count_estimate(text):
    # unDraw figures are typically the deepest/most path-dense <g> groups;
    # a precise count needs real parsing, so this is a rough proxy only:
    # count top-level <g transform="translate(...)"> groups as a ceiling.
    return len(re.findall(r'<g transform="translate\(', text))


def build_index(library):
    if not os.path.isdir(library):
        print(f"Library folder not found: {library}", file=sys.stderr)
        print("Create it and drop unDraw SVGs in (free from undraw.co/illustrations), "
              "or pass --library /path/to/svgs.", file=sys.stderr)
        sys.exit(1)

    files = sorted(f for f in os.listdir(library) if f.lower().endswith(".svg"))
    if not files:
        print(f"No .svg files in {library} yet. Grab a few from undraw.co/illustrations.", file=sys.stderr)
        sys.exit(1)

    entries = []
    for f in files:
        path = os.path.join(library, f)
        text = open(path, "r", errors="ignore").read()
        entries.append({
            "file": f,
            "keywords": slug_to_keywords(f),
            "secondary_accents": detect_secondary_accents(text),
            "group_count": figure_count_estimate(text),
        })

    # JSON — machine-readable, for the skill to load directly
    json_path = os.path.join(library, "index.json")
    with open(json_path, "w") as jf:
        json.dump({"library": library, "count": len(entries), "illustrations": entries}, jf, indent=2)

    # Markdown — human-scannable table, and hand-editable (add your own keywords)
    md_path = os.path.join(library, "index.md")
    lines = [
        "# unDraw library index",
        "",
        f"{len(entries)} illustrations. Regenerate with `build_library_index.py` after adding new SVGs — "
        "or hand-edit the keywords column below; matching reads whichever is more specific.",
        "",
        "| File | Keywords | Secondary accent |",
        "|---|---|---|",
    ]
    for e in entries:
        accents = ", ".join(e["secondary_accents"]) or "—"
        lines.append(f"| `{e['file']}` | {' '.join(e['keywords'])} | {accents} |")
    with open(md_path, "w") as mf:
        mf.write("\n".join(lines) + "\n")

    print(f"Indexed {len(entries)} illustrations from {library}")
    print(f"  -> {md_path}  (human-readable, hand-editable)")
    print(f"  -> {json_path}  (machine-readable)")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--library", default=DEFAULT_LIBRARY, help=f"Library folder (default: {DEFAULT_LIBRARY})")
    args = p.parse_args()
    build_index(args.library)


if __name__ == "__main__":
    main()
