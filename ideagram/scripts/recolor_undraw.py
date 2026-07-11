#!/usr/bin/env python3
"""
Recolor an unDraw-style illustration's ACCENT to a brand color, leaving the
character (skin, hair, clothing) and neutrals exactly as the illustrator drew
them.

This is the linchpin of using real unDraw art on-brand. unDraw draws every
illustration around one accent hue (`#6c63ff`, a purple) plus a fixed set of
neutrals and skin tones. To put an illustration on a brand, you swap ONLY the
accent — not skin, not the dark ink, not the greys. A naive "recolor every
non-black fill" (see recolor_svg.py) would tint skin and shadows too and ruin
it; this targets the accent family specifically.

What it swaps by default (the unDraw accent family):
    #6c63ff  (primary accent)         -> brand
    #6c63ff at any opacity            -> brand
    a couple of near-variants unDraw uses for accent shading

What it preserves (never touched):
    #090814 ink, #2f2e41/#3f3d56/#3f3d58 dark clothing, #e6e6e6/#d6d6e3 greys,
    #ed9da0 and other skin tones, white — the whole rest of the illustration.

Usage:
    python3 recolor_undraw.py illo.svg --accent "#0FB5A8"
    python3 recolor_undraw.py illo.svg --accent "#0FB5A8" --also "#8ed16f:#F59E0B"
        (also remap a secondary accent, e.g. unDraw's green -> amber)
    python3 recolor_undraw.py illo.svg --accent "#0FB5A8" --out branded.svg
"""

import sys
import os
import re
import argparse
import colorsys

# unDraw's accent family — the purple that defines each illustration's "pop".
# Case-insensitive; matched anywhere (fill=, stroke=, stop-color=, gradients).
UNDRAW_ACCENTS = ["#6c63ff", "#6c63fe", "#5c53ef", "#4e46c9"]


def shade(hex_color, factor):
    """Return hex_color lightened(>1)/darkened(<1) in HLS space, for deriving
    unDraw's accent-shade variants from a single brand color so gradients/shading
    on the accent stay coherent."""
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = max(0, min(1, l * factor))
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#{:02x}{:02x}{:02x}".format(round(r * 255), round(g * 255), round(b * 255))


def build_map(brand, extras):
    m = {}
    # Primary accent -> brand. The near-variants (unDraw's darker accent shades)
    # map to a proportionally darker version of the brand so shaded accent areas
    # still read as the same colour family.
    shade_factors = {"#6c63ff": 1.0, "#6c63fe": 1.0, "#5c53ef": 0.85, "#4e46c9": 0.72}
    for accent in UNDRAW_ACCENTS:
        m[accent] = brand if shade_factors[accent] == 1.0 else shade(brand, shade_factors[accent])
    for pair in extras:
        frm, to = pair.split(":")
        m[frm.lower()] = to
    return m


def recolor(text, cmap):
    def repl(match):
        val = match.group(0).lower()
        return cmap.get(val, match.group(0))
    # Replace any 6-hex occurrence that's in our map, case-insensitively.
    pattern = re.compile(r"#[0-9a-fA-F]{6}")
    return pattern.sub(repl, text)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("svg")
    p.add_argument("--accent", required=True, help='Brand accent hex, e.g. "#0FB5A8"')
    p.add_argument("--also", nargs="*", default=[], help='Extra "from:to" hex remaps, e.g. "#8ed16f:#F59E0B"')
    p.add_argument("--out", help="Output path (default: overwrite input)")
    args = p.parse_args()

    if not os.path.exists(args.svg):
        print(f"File not found: {args.svg}", file=sys.stderr)
        sys.exit(1)
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", args.accent):
        print(f"--accent must be a 6-digit hex like #0FB5A8, got {args.accent}", file=sys.stderr)
        sys.exit(1)

    text = open(args.svg).read()
    cmap = build_map(args.accent.lower(), args.also)

    # Count what we'll change for an honest report.
    before = {k: len(re.findall(re.escape(k), text, re.I)) for k in cmap}
    new_text = recolor(text, cmap)
    changed = sum(v for v in before.values())

    if changed == 0:
        print("No unDraw accent colors found. Is this actually an unDraw-style SVG? "
              "(expected the accent family " + ", ".join(UNDRAW_ACCENTS[:1]) + "…). "
              "Nothing written.", file=sys.stderr)
        sys.exit(1)

    out = args.out or args.svg
    open(out, "w").write(new_text)
    print(f"[ok] {out} — swapped {changed} accent occurrence(s) to {args.accent}; "
          "skin, hair, clothing and neutrals left untouched.")


if __name__ == "__main__":
    main()
