#!/usr/bin/env python3
"""
Fetch real photography from Unsplash's official API for sections that should
read as "real" rather than illustrated (offices, team headshots, product-in-use
shots) — see references/component-patterns.md's "About / company" pattern for
when a section calls for a photo instead of an illustration.

This uses Unsplash's actual public API, not scraping — that's the whole point.
Unsplash's API Guidelines require two things this script does NOT skip:
  1. Attribution (photographer name + Unsplash, both linked) wherever the
     photo is displayed — written out to ATTRIBUTION.md alongside the image.
  2. A "download tracked" ping to photo.links.download_location once a photo
     is actually used (not just browsed) — this script does that at fetch
     time since fetching here means "we're using this."

Requires a free Unsplash API access key: register at
https://unsplash.com/developers, then:
    export UNSPLASH_ACCESS_KEY="your_key_here"

Usage:
    python3 fetch_unsplash.py "modern office interior plants" \
        --count 3 --out design/assets/photos --orientation landscape
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.parse


API_BASE = "https://api.unsplash.com"


def api_get(path, params, access_key):
    url = f"{API_BASE}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Authorization": f"Client-ID {access_key}"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def download(url, dest_path):
    req = urllib.request.Request(url, headers={"User-Agent": "tastemaker-skill/1.0"})
    with urllib.request.urlopen(req) as resp, open(dest_path, "wb") as f:
        f.write(resp.read())


def trigger_download_tracking(download_location, access_key):
    # Required by Unsplash's API Guidelines whenever a photo is actually used,
    # not merely previewed. Fire-and-forget is fine per their docs.
    req = urllib.request.Request(
        download_location, headers={"Authorization": f"Client-ID {access_key}"}
    )
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print(f"  (warning: download-tracking ping failed, non-fatal: {e})", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("query", help="Search query, e.g. 'modern office interior plants'")
    parser.add_argument("--count", type=int, default=3, help="Number of photos to fetch (default 3)")
    parser.add_argument("--out", default="design/assets/photos", help="Output directory")
    parser.add_argument("--orientation", choices=["landscape", "portrait", "squarish"], default=None)
    args = parser.parse_args()

    access_key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not access_key:
        print(
            "UNSPLASH_ACCESS_KEY not set. Register a free app at "
            "https://unsplash.com/developers and run:\n"
            "  export UNSPLASH_ACCESS_KEY=your_key_here",
            file=sys.stderr,
        )
        sys.exit(1)

    os.makedirs(args.out, exist_ok=True)

    params = {"query": args.query, "per_page": args.count}
    if args.orientation:
        params["orientation"] = args.orientation

    results = api_get("/search/photos", params, access_key).get("results", [])
    if not results:
        print(f"No results for query: {args.query}", file=sys.stderr)
        sys.exit(1)

    attribution_lines = []
    for i, photo in enumerate(results[: args.count]):
        img_url = photo["urls"]["regular"]
        filename = f"{args.query.replace(' ', '-').lower()}-{i+1}.jpg"
        dest = os.path.join(args.out, filename)
        download(img_url, dest)
        trigger_download_tracking(photo["links"]["download_location"], access_key)

        photographer = photo["user"]["name"]
        photographer_url = photo["user"]["links"]["html"] + "?utm_source=tastemaker&utm_medium=referral"
        photo_url = photo["links"]["html"] + "?utm_source=tastemaker&utm_medium=referral"
        attribution_lines.append(
            f"- `{filename}` — Photo by [{photographer}]({photographer_url}) on "
            f"[Unsplash]({photo_url})"
        )
        print(f"Saved {dest}")

    attribution_path = os.path.join(args.out, "ATTRIBUTION.md")
    header = [] if not os.path.exists(attribution_path) else None
    with open(attribution_path, "a") as f:
        if header is not None:
            f.write("# Photo attribution (required by Unsplash API Guidelines)\n\n")
        f.write("\n".join(attribution_lines) + "\n")

    print(f"\nAttribution written to {attribution_path} — surface this credit near each photo in the UI (not just in this file). Unsplash's guidelines require the photographer + Unsplash to be credited and linked wherever the photo is actually displayed.")


if __name__ == "__main__":
    main()
