#!/usr/bin/env python3
"""
Fetch real photography from Pixabay — attribution-free, API-first.

Why Pixabay is the default photo source (over Unsplash):
  - The Pixabay Content License requires NO attribution, anywhere, ever —
    not on the finished site, not in a caption, not in a footer. So a photo
    never becomes a visual hindrance for the end user. (Pixabay's API terms
    only ask for source display if you're building an app that shows Pixabay
    *search results* to your users — a stock-photo browser — which is not
    what a finished website does. A downloaded photo used in a real site
    carries no attribution obligation.)
  - Free official API built for exactly this programmatic use.
  - No download-tracking ping to remember (unlike Unsplash).

The result: a generated site can include real photography with zero
attribution markup and zero manual steps — the whole point of switching.

Requires a free Pixabay API key: https://pixabay.com/api/docs/ (sign in,
the key is shown on that page), then:
    export PIXABAY_API_KEY="your_key_here"

Usage:
    python3 fetch_photos.py "modern office workspace" \\
        --count 3 --out design/assets/photos --orientation horizontal
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.parse

API = "https://pixabay.com/api/"


def api_get(params):
    url = f"{API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "tastemaker-skill/1.0"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode())


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "tastemaker-skill/1.0"})
    with urllib.request.urlopen(req, timeout=45) as resp, open(dest, "wb") as f:
        f.write(resp.read())


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("query")
    parser.add_argument("--count", type=int, default=3)
    parser.add_argument("--out", default="design/assets/photos")
    parser.add_argument("--orientation", choices=["horizontal", "vertical", "all"], default="all")
    args = parser.parse_args()

    key = os.environ.get("PIXABAY_API_KEY")
    if not key:
        print(
            "PIXABAY_API_KEY not set. Get a free key at https://pixabay.com/api/docs/ "
            "(shown on that page once signed in), then:\n"
            "  export PIXABAY_API_KEY=your_key_here\n"
            "No photos fetched. Sections needing real photography can use a code-native "
            "placeholder until the key is set — but the finished site should have real "
            "photos, so flag this rather than silently shipping placeholders.",
            file=sys.stderr,
        )
        sys.exit(1)

    os.makedirs(args.out, exist_ok=True)

    params = {
        "key": key,
        "q": args.query,
        "image_type": "photo",
        "safesearch": "true",
        "per_page": max(3, args.count),
        "orientation": args.orientation,
    }
    try:
        data = api_get(params)
    except Exception as e:
        print(f"Pixabay request failed: {e}", file=sys.stderr)
        sys.exit(1)

    hits = data.get("hits", [])
    if not hits:
        print(f"No results for '{args.query}'. Try broader terms.", file=sys.stderr)
        sys.exit(1)

    for i, hit in enumerate(hits[: args.count]):
        # largeImageURL is the full-res download; fall back to webformatURL.
        img_url = hit.get("largeImageURL") or hit.get("webformatURL")
        filename = f"{args.query.replace(' ', '-').lower()}-{i+1}.jpg"
        dest = os.path.join(args.out, filename)
        try:
            download(img_url, dest)
            print(f"[ok] {dest}")
        except Exception as e:
            print(f"[fail] {filename} — {e}", file=sys.stderr)

    print(
        "\nDone. Pixabay's Content License requires no attribution — these can be used "
        "directly in the site with zero credit markup. No caption, no footer credit, "
        "nothing for the end user to see."
    )


if __name__ == "__main__":
    main()
