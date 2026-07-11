#!/usr/bin/env python3
"""
Extract a whole component (a figure, a device, a background panel) from a real
unDraw SVG into a standalone SVG you can reuse and recolor.

Reusing a whole component is the reliable way to build a NEW scene at genuine
unDraw quality (see references/undraw-anatomy.md) — the extracted paths are the
illustrator's real work, untouched.

How it works: unDraw components are `<g transform="translate(...)">` groups. This
finds a group by a substring of its opening tag (usually its translate), lifts it
out with proper brace-matching, and wraps it in a standalone SVG that keeps the
source's root viewBox + any wrapping parent transform, so it renders in exactly
the same place/size as in the original. From there, place it in a composition
with your own `<g transform>` and recolor with recolor_undraw.py.

First, list the groups to find the one you want:
    python3 extract_component.py source.svg --list

Then extract by a match string (e.g. the translate of the figure group):
    python3 extract_component.py source.svg --match "translate(626.584 516.463)" --out figure.svg

Tip: after extracting, render it in a browser and read the group's getBBox()
to set a tight viewBox — nested transforms make eyeballing the bounds wrong.
"""

import sys
import re
import argparse


def root_open_tag(text):
    m = re.search(r"<svg[^>]*>", text)
    return m.group(0) if m else '<svg xmlns="http://www.w3.org/2000/svg">'


def outer_wrapping_transform(text):
    """unDraw usually wraps everything in one <g transform="translate(a b)"> right
    after <svg>. Capturing it keeps extracted children positioned correctly."""
    m = re.search(r"<svg[^>]*>\s*(<g transform=\"[^\"]*\">)", text)
    return m.group(1) if m else None


def list_groups(text):
    for m in re.finditer(r'<g transform="[^"]*">', text):
        # show a short preview of what's inside to help identify it
        start = m.end()
        snippet = re.sub(r"\s+", " ", text[start:start + 90])
        print(f"  {m.group(0)}   …{snippet[:70]}")


def extract(text, match):
    idx = text.find(match)
    if idx == -1:
        return None
    # walk back to the '<g' that opens this tag
    gstart = text.rfind("<g", 0, idx + len(match))
    # brace-match <g>…</g>
    depth = 0
    j = gstart
    while j < len(text):
        ng = text.find("<g", j)
        nc = text.find("</g>", j)
        if ng != -1 and ng < nc:
            depth += 1
            j = ng + 2
        else:
            depth -= 1
            j = nc + 4
            if depth == 0:
                return text[gstart:j]
    return None


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("source")
    p.add_argument("--list", action="store_true", help="List transform groups to pick from")
    p.add_argument("--match", help='Substring of the target group\'s opening tag, e.g. a translate(...)')
    p.add_argument("--out", help="Output standalone SVG path")
    args = p.parse_args()

    text = open(args.source).read()

    if args.list:
        list_groups(text)
        return

    if not args.match:
        print("Give --list to see groups, or --match \"translate(...)\" to extract one.", file=sys.stderr)
        sys.exit(1)

    comp = extract(text, args.match)
    if comp is None:
        print(f"No group matching {args.match!r} found. Try --list.", file=sys.stderr)
        sys.exit(1)

    root = root_open_tag(text)
    wrap = outer_wrapping_transform(text)
    inner = f"{wrap}{comp}</g>" if wrap else comp
    out_svg = f"{root}{inner}</svg>"

    dest = args.out or (args.source.rsplit(".", 1)[0] + "-component.svg")
    open(dest, "w").write(out_svg)
    print(f"[ok] {dest} — extracted. Render it and read getBBox() on the group to set a tight viewBox, "
          "then place it in your composition with a <g transform> and recolor with recolor_undraw.py.")


if __name__ == "__main__":
    main()
