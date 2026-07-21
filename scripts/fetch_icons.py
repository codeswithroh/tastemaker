#!/usr/bin/env python3
"""
Fetch icons from Iconify's public API — attribution-free, no API key.

Why this is the default icon source:
  - No key, no signup, no rate-limit gymnastics: api.iconify.design is a
    free public CDN designed for exactly this kind of programmatic use.
  - 200k+ icons across permissively-licensed open sets (Lucide, Tabler,
    Material Symbols, Phosphor, etc.). None of these require attribution
    on the finished site — so an icon never becomes a visual hindrance
    the way an attribution-required source does.
  - The API applies the color server-side, so an icon comes back already
    tinted to the project's locked accent — one fewer recolor step.

Pick ONE icon set per project and stay in it so every icon shares one
stroke weight and corner style — mixing sets is a fast way to look
unintentional. But "one set per project" does not mean "one set for every
project": every Tastemaker install defaulting to the same Lucide icons
regardless of what's being built is its own kind of sameness. Use --mood
to pick a set that actually matches the project's locked mood instead of
always reaching for the same default:

    premium    -> heroicons   (clean solid/outline, professional)
    warm       -> tabler      (friendly, rounded stroke)
    technical  -> lucide      (crisp, minimal, developer-tool default)
    playful    -> ph          (Phosphor; bold/duotone weights read playful)
    elegant    -> material-symbols  (thin weight reads considered, editorial)

Usage:
    # search to discover the right icon names within a set (mood picks the set)
    python3 fetch_icons.py --search "chart growth analytics" --mood technical

    # fetch specific icons, tinted, into the project
    python3 fetch_icons.py --icons rocket shield mail chart-line \\
        --mood warm --color "#6C5CE7" --out design/assets/icons

    # or name the set explicitly if the mood mapping doesn't fit this project
    python3 fetch_icons.py --icons rocket --set tabler --color "#6C5CE7"
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.parse

API = "https://api.iconify.design"

MOOD_ICON_SETS = {
    "premium": "heroicons",
    "warm": "tabler",
    "technical": "lucide",
    "playful": "ph",
    "elegant": "material-symbols",
}


def http_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "tastemaker-skill/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read()


def _search_one(term, set_prefix, limit):
    params = {"query": term, "limit": limit}
    if set_prefix:
        params["prefix"] = set_prefix
    url = f"{API}/search?{urllib.parse.urlencode(params)}"
    data = json.loads(http_get(url).decode())
    return data.get("icons", [])


def search(query, set_prefix=None, limit=24):
    # Iconify treats a multi-word query as a strict AND, so "chart growth"
    # matches nothing even though "chart" and "growth" each match plenty.
    # Search each word separately and merge, preserving first-seen order,
    # so a natural phrase still surfaces useful candidates.
    seen = []
    for term in query.split():
        for icon in _search_one(term, set_prefix, limit):
            if icon not in seen:
                seen.append(icon)
    return seen[:limit]


def fetch_icon(set_prefix, name, color, width):
    # Iconify serves ready-to-use SVG at /{prefix}/{name}.svg with optional
    # color + width query params applied server-side.
    params = {"width": width}
    if color:
        params["color"] = color
    url = f"{API}/{set_prefix}/{name}.svg?{urllib.parse.urlencode(params)}"
    return http_get(url)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--search", help="Discover icon names matching these terms")
    parser.add_argument("--icons", nargs="+", help="Icon names to fetch (within --set)")
    parser.add_argument("--set", dest="icon_set", default=None,
                         help="Iconify set prefix, e.g. lucide, tabler, ph. Overrides --mood if both are given.")
    parser.add_argument("--mood", choices=list(MOOD_ICON_SETS.keys()),
                         help="Pick the icon set from the project's locked mood instead of naming --set directly "
                              "(see the mapping in this script's module docstring). Recommended over a bare default.")
    parser.add_argument("--color", default=None, help='Hex tint applied server-side, e.g. "#6C5CE7"')
    parser.add_argument("--width", type=int, default=48, help="Icon width in px (default 48)")
    parser.add_argument("--out", default="design/assets/icons", help="Output directory")
    args = parser.parse_args()

    if args.icon_set:
        pass  # explicit --set always wins
    elif args.mood:
        args.icon_set = MOOD_ICON_SETS[args.mood]
    else:
        args.icon_set = "lucide"
        print(
            "No --set or --mood given; defaulting to 'lucide'. This is how every project ends up with the same "
            "icons — pass --mood <premium|warm|technical|playful|elegant> to match this project's locked mood, "
            "or --set to name one directly.",
            file=sys.stderr,
        )

    if args.search:
        try:
            names = search(args.search, set_prefix=args.icon_set)
        except Exception as e:
            print(f"Search failed (network?): {e}", file=sys.stderr)
            sys.exit(1)
        if not names:
            print(f"No icons found for '{args.search}' in set '{args.icon_set}'. Try a broader term or a different --set.")
            return
        print(f"Icons matching '{args.search}' in '{args.icon_set}':")
        for n in names:
            # results come back as "prefix:name" — strip prefix for reuse with --icons
            print(f"  {n.split(':', 1)[-1]}")
        return

    if not args.icons:
        print("Nothing to do. Use --search to discover names, or --icons to fetch.", file=sys.stderr)
        sys.exit(1)

    os.makedirs(args.out, exist_ok=True)
    failed = []
    for name in args.icons:
        try:
            svg = fetch_icon(args.icon_set, name, args.color, args.width)
            # Iconify returns a tiny error SVG (404-ish) for unknown names rather
            # than an HTTP error — detect the empty/placeholder case by size.
            if len(svg) < 60:
                failed.append(name)
                print(f"[miss] {name} — not found in set '{args.icon_set}' (run --search to find the right name)")
                continue
            dest = os.path.join(args.out, f"{name}.svg")
            with open(dest, "wb") as f:
                f.write(svg)
            print(f"[ok]   {dest}")
        except Exception as e:
            failed.append(name)
            print(f"[fail] {name} — {e}", file=sys.stderr)

    if failed:
        print(f"\n{len(failed)} icon(s) not fetched: {', '.join(failed)}. "
              "These are attribution-free open sets, so a miss is just a wrong name — search first.")


if __name__ == "__main__":
    main()
