#!/usr/bin/env python3
"""
Recolor local SVG files to match the project's locked palette.

This operates only on SVG files already sitting on disk — files the user
downloaded themselves (e.g. from unDraw's own gallery, or an icon set).
It does not fetch, scrape, or search anything remote. That distinction
matters: unDraw's license explicitly prohibits automated
scraping/downloading of their assets, but recoloring a file the user
already legitimately has on their machine is just local file editing.

Note: unDraw's own site (undraw.co/illustrations) already has a built-in
recolor tool, so illustrations downloaded from there may not need this at
all. This script is most useful for normalizing assets pulled from
*multiple* sources (e.g. a generic icon set that isn't pre-tinted) onto
one consistent accent color.

Usage:
    python3 recolor_svg.py <svg_path_or_dir> --accent "#C9A227" [--preserve-dark]

    --preserve-dark   Leave near-black (#000-#333 range) fills/strokes alone —
                       useful for line-art icons where only the accent fill
                       should change and outlines should stay dark.
"""

import sys
import os
import re
import argparse


HEX_COLOR_RE = re.compile(r'(fill|stroke)="(#[0-9a-fA-F]{3,8})"')


def hex_to_rgb(hexstr):
    hexstr = hexstr.lstrip("#")
    if len(hexstr) == 3:
        hexstr = "".join(c * 2 for c in hexstr)
    return tuple(int(hexstr[i : i + 2], 16) for i in (0, 2, 4))


def is_near_black(hexstr, threshold=60):
    r, g, b = hex_to_rgb(hexstr[:7])
    return max(r, g, b) < threshold


def is_near_white(hexstr, threshold=240):
    r, g, b = hex_to_rgb(hexstr[:7])
    return min(r, g, b) > threshold


def recolor_file(path, accent, preserve_dark):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    def replace(match):
        attr, color = match.group(1), match.group(2)
        if color.lower() in ("#000", "#000000", "#fff", "#ffffff", "none"):
            return match.group(0)  # leave pure black/white/none untouched
        if preserve_dark and is_near_black(color):
            return match.group(0)
        if is_near_white(color):
            return match.group(0)
        return f'{attr}="{accent}"'

    new_text, count = HEX_COLOR_RE.subn(replace, text)
    return new_text, count


def find_svgs(path):
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for f in files:
                if f.lower().endswith(".svg"):
                    yield os.path.join(root, f)
    elif path.lower().endswith(".svg"):
        yield path


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", help="SVG file or directory of SVGs")
    parser.add_argument("--accent", required=True, help='Target hex color, e.g. "#C9A227"')
    parser.add_argument("--preserve-dark", action="store_true", help="Leave near-black fills/strokes untouched")
    parser.add_argument("--dry-run", action="store_true", help="Report what would change without writing")
    args = parser.parse_args()

    files = list(find_svgs(args.path))
    if not files:
        print(f"No SVG files found at {args.path}", file=sys.stderr)
        sys.exit(1)

    for path in files:
        new_text, count = recolor_file(path, args.accent, args.preserve_dark)
        if count == 0:
            print(f"[skip] {path} — no matching fill/stroke colors found")
            continue
        if args.dry_run:
            print(f"[dry-run] {path} — would recolor {count} attribute(s) to {args.accent}")
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_text)
            print(f"[done] {path} — recolored {count} attribute(s) to {args.accent}")


if __name__ == "__main__":
    main()
