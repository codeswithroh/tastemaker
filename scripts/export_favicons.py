#!/usr/bin/env python3
"""
Export a project's logo mark to standard favicon and OG-card sizes.

Why this exists: `ideagram/scripts/export_png.py` covers illustration export
at social/presentation sizes, but a logo mark (the output of
`references/logo-sourcing.md`) needs a different, smaller set of sizes —
favicon.ico, apple-touch-icon, and a manifest icon — that no other script in
this skill produces. Skipping this step is what leaves a generated site with
a browser-default blank-page icon even though a real logo mark exists on disk.

Requires cairosvg (pip install cairosvg) + Pillow, same as export_png.py.
Degrades the same way: if either is missing, this says so plainly and exits
nonzero rather than silently producing nothing — the source SVG remains
usable directly in an <img> tag regardless.

Usage:
    python3 export_favicons.py logo-mark.svg --out design/assets/favicons/

Produces:
    favicon-16.png, favicon-32.png, favicon-48.png   (browser tab icon)
    apple-touch-icon.png (180x180)                    (iOS home screen)
    icon-192.png, icon-512.png                        (PWA manifest icons)
    favicon.ico                                       (multi-size, legacy browsers)
    og-card.png (1200x630)                             (link preview / social share)
"""

import sys
import os
import argparse

SQUARE_SIZES = {
    "favicon-16": 16,
    "favicon-32": 32,
    "favicon-48": 48,
    "apple-touch-icon": 180,
    "icon-192": 192,
    "icon-512": 512,
}
OG_SIZE = (1200, 630)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("svg_path")
    parser.add_argument("--out", default="design/assets/favicons", help="Output directory")
    parser.add_argument("--skip-og", action="store_true", help="Skip the 1200x630 OG-card render (favicon sizes only)")
    args = parser.parse_args()

    try:
        import cairosvg
    except ImportError:
        print(
            "cairosvg not installed. Run `pip install cairosvg` to enable favicon export.\n"
            "Until then, the SVG itself still works directly as a favicon in modern "
            "browsers via <link rel=\"icon\" type=\"image/svg+xml\" href=\"...\">, just "
            "without the legacy .ico/apple-touch-icon/manifest sizes.",
            file=sys.stderr,
        )
        sys.exit(1)
    except OSError as e:
        print(
            f"cairosvg is installed but couldn't load the native cairo library ({e}).\n"
            "Install it at the system level, then retry:\n"
            "  macOS:          brew install cairo\n"
            "  Debian/Ubuntu:  sudo apt install libcairo2",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        from PIL import Image
    except ImportError:
        print("Pillow not installed. Run `pip install Pillow` (needed for centering + writing the multi-size .ico).", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.svg_path):
        print(f"File not found: {args.svg_path}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.out, exist_ok=True)

    def render_square(size):
        temp_png = os.path.join(args.out, f".render-{size}.png")
        cairosvg.svg2png(url=args.svg_path, write_to=temp_png, output_width=size * 2, output_height=size * 2)
        img = Image.open(temp_png).convert("RGBA")
        scale = min(size / img.width, size / img.height)
        new_size = (max(1, int(img.width * scale)), max(1, int(img.height * scale)))
        img = img.resize(new_size, Image.LANCZOS)
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        canvas.paste(img, ((size - new_size[0]) // 2, (size - new_size[1]) // 2), img)
        os.remove(temp_png)
        return canvas

    rendered = {}
    for label, size in SQUARE_SIZES.items():
        img = render_square(size)
        dest = os.path.join(args.out, f"{label}.png")
        img.save(dest)
        rendered[size] = img
        print(f"Exported {dest} ({size}x{size})")

    ico_dest = os.path.join(args.out, "favicon.ico")
    ico_sizes = [s for s in (16, 32, 48) if s in rendered]
    rendered[ico_sizes[0]].save(
        ico_dest,
        format="ICO",
        sizes=[(s, s) for s in ico_sizes],
    )
    print(f"Exported {ico_dest} (multi-size: {ico_sizes})")

    if not args.skip_og:
        w, h = OG_SIZE
        temp_png = os.path.join(args.out, ".render-og.png")
        cairosvg.svg2png(url=args.svg_path, write_to=temp_png, output_width=w, output_height=h)
        img = Image.open(temp_png).convert("RGBA")
        scale = min(w / img.width, h / img.height) * 0.6  # logo mark shouldn't fill the whole OG card
        new_size = (max(1, int(img.width * scale)), max(1, int(img.height * scale)))
        img = img.resize(new_size, Image.LANCZOS)
        canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        canvas.paste(img, ((w - new_size[0]) // 2, (h - new_size[1]) // 2), img)
        os.remove(temp_png)
        dest = os.path.join(args.out, "og-card.png")
        canvas.save(dest)
        print(f"Exported {dest} ({w}x{h}) — a bare centered mark; if the OG card needs a wordmark/background too, compose that in code rather than relying on this alone.")


if __name__ == "__main__":
    main()
