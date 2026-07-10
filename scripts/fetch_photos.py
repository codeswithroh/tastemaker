#!/usr/bin/env python3
"""
Fetch real photography — keyless and attribution-free — from Openverse.

Why this is the default photo source:
  - **No API key.** Openverse's public search works anonymously (rate-limited
    to 20/min, 200/day — plenty for build-time asset fetching). Combined with
    Iconify (icons, also keyless) and the ideagram skill (illustrations), this
    makes the whole asset pipeline zero-setup: one prompt, a complete site,
    no accounts to create.
  - **Attribution-free by filter.** By default this fetches only CC0 and
    Public-Domain-Mark images — licenses that legally require *no* attribution
    anywhere. Nothing the end user ever has to see.
  - **Searchable** across 800M+ openly-licensed images (Wikimedia, museums,
    Flickr, rawpixel, StockSnap, …), unlike keyless placeholder services.

"Pay it through the code": even though CC0/PDM require nothing, this writes a
CREDITS block listing each photo's creator + source + license + Openverse link.
Drop it into a code comment (e.g. top of your HTML/CSS) as a voluntary
thank-you to the people whose work you're using — visible to any developer who
reads the source, invisible to the end user. That's the honest middle ground:
generous credit, zero on-page hindrance. (See --credits-format.)

Optional higher-curation upgrade: `--source pixabay` uses Pixabay instead
(needs a free PIXABAY_API_KEY) — also attribution-free, generally more
"stock-polished" imagery, full resolution. Use it when Openverse's more
eclectic pool doesn't have a clean match.

Usage:
    python3 fetch_photos.py "modern office workspace" --count 3 --out design/assets/photos
    python3 fetch_photos.py "storm clouds" --source pixabay --out design/assets/photos
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.parse

OPENVERSE = "https://api.openverse.org/v1/images/"
PIXABAY = "https://pixabay.com/api/"
UA = {"User-Agent": "tastemaker-skill/1.0 (https://github.com/codeswithroh/tastemaker)"}


def http_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode())


def http_bytes(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as resp:
        ctype = resp.headers.get("Content-Type", "")
        data = resp.read()
        return data, ctype


def image_ext(data):
    """Return the correct file extension for the actual image bytes, or None
    if the bytes aren't a recognized image. Naming a WebP file `.jpg` (which
    some sources like rawpixel serve) is a real mismatch that trips strict
    tooling, so we detect format from magic bytes rather than trusting the URL."""
    if data[:3] == b"\xff\xd8\xff":
        return ".jpg"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return ".gif"
    return None


def download_photo(result):
    """Try the full-res source URL first; fall back to Openverse's own image
    proxy when a source blocks hotlinking (some return a 403 HTML page).
    Returns (bytes, extension) or (None, None)."""
    src = result.get("url")
    if src:
        try:
            data, _ = http_bytes(src)
            ext = image_ext(data)
            if ext:
                return data, ext
        except Exception:
            pass
    # Fallback: Openverse thumbnail proxy — always serves a real image, ~600px.
    thumb = f"{OPENVERSE}{result['id']}/thumb/"
    try:
        data, _ = http_bytes(thumb)
        ext = image_ext(data)
        if ext:
            return data, ext
    except Exception:
        pass
    return None, None


def _broadening_queries(query):
    """Openverse (like many search backends) treats a long multi-word query as
    a strict-ish AND, so a natural 3-4 word phrase can return zero even when
    each word has hundreds of hits on its own. Yield the full query first, then
    progressively broader versions (dropping leading words, since the English
    head noun tends to sit at the end) so a fetch rarely comes back empty."""
    words = query.split()
    seen = set()
    # full query, then last-3, last-2, last-1 words
    for start in range(0, len(words)):
        candidate = " ".join(words[start:])
        if candidate and candidate not in seen:
            seen.add(candidate)
            yield candidate


def _openverse_search(query, page_size):
    params = {
        "q": query,
        "license": "cc0,pdm",   # zero-attribution licenses only, by default
        "size": "large",
        "page_size": page_size,
        "mature": "false",
    }
    url = f"{OPENVERSE}?{urllib.parse.urlencode(params)}"
    return http_json(url).get("results", [])


def fetch_openverse(query, count, out):
    page_size = max(count * 3, 6)  # over-fetch: some sources will fail download
    results = []
    try:
        for candidate in _broadening_queries(query):
            results = _openverse_search(candidate, page_size)
            if results:
                if candidate != query:
                    print(f"(broadened '{query}' → '{candidate}' to find CC0 matches)")
                break
    except Exception as e:
        print(f"Openverse request failed: {e}", file=sys.stderr)
        return []

    if not results:
        print(f"No CC0/public-domain results for '{query}' even after broadening. "
              "Try different terms, or --source pixabay for a differently-curated pool.", file=sys.stderr)
        return []

    saved = []
    slug = query.replace(" ", "-").lower()
    for r in results:
        if len(saved) >= count:
            break
        img, ext = download_photo(r)
        if img is None:
            continue
        filename = f"{slug}-{len(saved) + 1}{ext}"
        dest = os.path.join(out, filename)
        with open(dest, "wb") as f:
            f.write(img)
        saved.append({
            "file": filename,
            "title": r.get("title") or "",
            "creator": r.get("creator") or "Unknown",
            "source": r.get("source") or "",
            "license": f"{r.get('license', '')} {r.get('license_version', '')}".strip(),
            "openverse_url": r.get("foreign_landing_url") or r.get("detail_url") or "",
        })
        print(f"[ok] {dest}")
    return saved


def fetch_pixabay(query, count, out):
    key = os.environ.get("PIXABAY_API_KEY")
    if not key:
        print("PIXABAY_API_KEY not set. Get a free key at https://pixabay.com/api/docs/, "
              "or drop --source pixabay to use keyless Openverse instead.", file=sys.stderr)
        return []
    params = {"key": key, "q": query, "image_type": "photo", "safesearch": "true", "per_page": max(3, count)}
    try:
        data = http_json(f"{PIXABAY}?{urllib.parse.urlencode(params)}")
    except Exception as e:
        print(f"Pixabay request failed: {e}", file=sys.stderr)
        return []
    hits = data.get("hits", [])
    saved = []
    slug = query.replace(" ", "-").lower()
    for hit in hits[:count]:
        img_url = hit.get("largeImageURL") or hit.get("webformatURL")
        try:
            img, ctype = http_bytes(img_url)
        except Exception as e:
            print(f"[fail] {img_url} — {e}", file=sys.stderr)
            continue
        filename = f"{slug}-{len(saved) + 1}.jpg"
        dest = os.path.join(out, filename)
        with open(dest, "wb") as f:
            f.write(img)
        saved.append({
            "file": filename, "title": hit.get("tags", ""),
            "creator": hit.get("user", "Unknown"), "source": "pixabay",
            "license": "Pixabay Content License (no attribution required)",
            "openverse_url": hit.get("pageURL", ""),
        })
        print(f"[ok] {dest}")
    return saved


def write_credits(saved, out, fmt):
    if not saved:
        return
    lines = [
        "Photo credits — voluntary courtesy, NOT a license requirement.",
        "All images below are CC0 / Public Domain / attribution-free; none of this",
        "needs to appear on the rendered page. Keep it here in the source as a",
        "thank-you to the creators. Do not surface it as visible on-site attribution.",
        "",
    ]
    for s in saved:
        cred = f"{s['file']}: \"{s['title']}\" by {s['creator']} ({s['source']}, {s['license']})"
        if s["openverse_url"]:
            cred += f" — {s['openverse_url']}"
        lines.append(cred)

    if fmt == "html":
        body = "\n".join(lines)
        text = f"<!--\n{body}\n-->\n"
        path = os.path.join(out, "CREDITS.html.txt")
    elif fmt == "css":
        body = "\n".join("   " + l for l in lines)
        text = f"/*\n{body}\n*/\n"
        path = os.path.join(out, "CREDITS.css.txt")
    else:
        text = "\n".join(lines) + "\n"
        path = os.path.join(out, "CREDITS.txt")

    with open(path, "w") as f:
        f.write(text)
    print(f"\nCredits written to {path} — paste this into a code comment (top of your "
          "HTML/CSS) as a voluntary thank-you. It must NOT appear as visible text on the page.")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("query")
    parser.add_argument("--count", type=int, default=3)
    parser.add_argument("--out", default="design/assets/photos")
    parser.add_argument("--source", choices=["openverse", "pixabay"], default="openverse",
                        help="openverse = keyless + attribution-free (default); pixabay = higher curation, needs key")
    parser.add_argument("--credits-format", choices=["plain", "html", "css"], default="html",
                        help="Comment style for the voluntary credits file (default html)")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    if args.source == "pixabay":
        saved = fetch_pixabay(args.query, args.count, args.out)
    else:
        saved = fetch_openverse(args.query, args.count, args.out)

    if not saved:
        print("\nNo photos fetched. A section needing real photography can use a code-native "
              "placeholder until this resolves — but flag it plainly rather than shipping a "
              "grey box as if it were a real photo.", file=sys.stderr)
        sys.exit(1)

    write_credits(saved, args.out, args.credits_format)


if __name__ == "__main__":
    main()
