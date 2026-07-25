#!/usr/bin/env python3
"""
Export a generated SVG illustration to PNG at common social/web dimensions.

SVG is the right source format (crisp, tiny, infinitely recolorable/scalable),
but most social platforms and many CMSes want a raster file to upload. This
renders flattened PNGs at standard sizes so the same illustration is ready
for a tweet, an OG/link-preview image, or a square Instagram-style post
without the user having to figure out dimensions themselves.

Requires cairosvg (pip install cairosvg). If it's not installed, this exits
with clear instructions rather than failing silently — the illustration
itself (the SVG) is still fully usable directly in any browser/HTML context
without this step.

Usage:
    python3 export_png.py illustration.svg --out design/export/
"""

import sys
import os
import argparse

SIZES = {
    "social-square": (1080, 1080),      # Instagram/LinkedIn square post
    "social-landscape": (1200, 630),    # Twitter/X card, OG image, link previews
    "presentation": (1920, 1080),       # slide/full-width use
}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("svg_path")
    parser.add_argument("--out", default="design/export", help="Output directory")
    parser.add_argument(
        "--sizes",
        nargs="+",
        choices=list(SIZES.keys()) + ["all"],
        default=["all"],
        help="Which preset sizes to export (default: all)",
    )
    args = parser.parse_args()

    try:
        import cairosvg
    except ImportError:
        print(
            "cairosvg not installed. Run `pip install cairosvg` to enable PNG export.\n"
            "Until then, the SVG itself is still fully usable directly — most modern "
            "social platforms and every browser/CMS accept SVG natively.",
            file=sys.stderr,
        )
        sys.exit(1)
    except OSError as e:
        # The common real-world failure: the cairosvg *Python* package is
        # installed, but its underlying native cairo library isn't — pip
        # can't install that part, it's a system package.
        print(
            f"cairosvg is installed but couldn't load the native cairo library ({e}).\n"
            "Install it at the system level, then retry:\n"
            "  macOS:          brew install cairo\n"
            "  Debian/Ubuntu:  sudo apt install libcairo2\n"
            "Until then, the SVG itself is still fully usable directly — most modern "
            "social platforms and every browser/CMS accept SVG natively.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        from PIL import Image
    except ImportError:
        print("Pillow not installed. Run `pip install Pillow` (needed to center the illustration on each canvas size without distorting it).", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.svg_path):
        print(f"File not found: {args.svg_path}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.out, exist_ok=True)
    basename = os.path.splitext(os.path.basename(args.svg_path))[0]

    sizes_to_export = SIZES if "all" in args.sizes else {k: SIZES[k] for k in args.sizes}

    for label, (w, h) in sizes_to_export.items():
        dest = os.path.join(args.out, f"{basename}-{label}.png")

        # Render at a scale that fits *within* the target box, preserving
        # aspect ratio, then paste centered onto a transparent canvas of the
        # exact target size — passing output_width/output_height straight to
        # cairosvg would stretch a square illustration into whatever aspect
        # ratio the target happens to be, which is exactly the distortion
        # this is meant to avoid.
        temp_png = os.path.join(args.out, f".{basename}-{label}-render.png")
        cairosvg.svg2png(url=args.svg_path, write_to=temp_png, output_width=w * 2, output_height=h * 2)
        rendered = Image.open(temp_png).convert("RGBA")
        scale = min(w / rendered.width, h / rendered.height)
        new_size = (max(1, int(rendered.width * scale)), max(1, int(rendered.height * scale)))
        rendered = rendered.resize(new_size, Image.LANCZOS)

        canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        offset = ((w - new_size[0]) // 2, (h - new_size[1]) // 2)
        canvas.paste(rendered, offset, rendered)
        canvas.save(dest)
        os.remove(temp_png)

        print(f"Exported {dest} ({w}x{h})")


if __name__ == "__main__":
    main()
