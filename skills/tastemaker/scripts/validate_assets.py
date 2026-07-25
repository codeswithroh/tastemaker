#!/usr/bin/env python3
"""
Validate generated/curated SVG assets before they ship.

Why this exists: SVGs are XML, and a generated file can look fine when read
as text but still be malformed in ways that break strict renderers — most
commonly a descriptive comment that happens to contain "--" (illegal inside
an XML comment per spec), which several browsers render as a broken image
instead of silently ignoring. This is invisible unless you actually parse
the file or view it rendered — catching it here is cheaper than catching it
in a screenshot review.

Usage:
    python3 validate_assets.py <file_or_directory> [...]

Exits nonzero if any file fails to parse. Prints one line per file.
"""

import sys
import os
import xml.etree.ElementTree as ET


def find_svgs(paths):
    for path in paths:
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for f in files:
                    if f.lower().endswith(".svg"):
                        yield os.path.join(root, f)
        elif path.lower().endswith(".svg"):
            yield path


def check_double_hyphen_in_comments(text):
    # A quick, specific check for the most common real-world failure mode:
    # a "--" inside a <!-- --> comment, which is illegal XML and trips up
    # strict parsers even though the rest of the file is fine.
    import re

    for match in re.finditer(r"<!--(.*?)-->", text, re.DOTALL):
        if "--" in match.group(1):
            return True
    return False


def validate(path):
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    if check_double_hyphen_in_comments(text):
        return False, "double-hyphen ('--') inside an XML comment — illegal, breaks strict SVG rendering"

    try:
        ET.fromstring(text)
    except ET.ParseError as e:
        return False, f"XML parse error: {e}"

    return True, "ok"


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_assets.py <file_or_directory> [...]", file=sys.stderr)
        sys.exit(1)

    files = list(find_svgs(sys.argv[1:]))
    if not files:
        print("No .svg files found under given paths.")
        sys.exit(0)

    any_failed = False
    for path in files:
        ok, msg = validate(path)
        status = "OK  " if ok else "FAIL"
        print(f"[{status}] {path} — {msg}")
        if not ok:
            any_failed = True

    sys.exit(1 if any_failed else 0)


if __name__ == "__main__":
    main()
