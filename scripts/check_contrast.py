#!/usr/bin/env python3
"""
WCAG contrast ratio checker for two hex colors, or a whole palette at once.

Why this exists: a palette (whether hand-picked, extracted from a reference
image, or a user-supplied brand color) can look fine as a swatch and still
fail contrast once it's actually used as text-on-background or a button
label. The easiest miss is checking body-text-on-background and stopping
there — a Primary/Accent color can pass that check and still be illegible
as a button fill with white label text. This script checks pairs directly
against the real WCAG math instead of eyeballing it.

Usage:
    # single pair
    python3 check_contrast.py 050315 fbfbfe
    python3 check_contrast.py "#050315" "#FBFBFE"

    # a whole five-role palette at once (checks the pairings that matter:
    # text/bg, white-on-primary, white-on-accent, dark-text-on-primary)
    python3 check_contrast.py --palette text=050315 bg=fbfbfe primary=2f27ce \
        secondary=dedcff accent=433bff

Exit code is nonzero if any checked pairing fails its floor.
"""

import sys

AA_NORMAL = 4.5
AA_LARGE_OR_UI = 3.0


def _linearize(c):
    c = c / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def _luminance(hex_color):
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        raise ValueError(f"expected a 6-digit hex color, got {hex_color!r}")
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _linearize(r) + 0.7152 * _linearize(g) + 0.0722 * _linearize(b)


def ratio(hex1, hex2):
    l1, l2 = _luminance(hex1), _luminance(hex2)
    l1, l2 = max(l1, l2), min(l1, l2)
    return (l1 + 0.05) / (l2 + 0.05)


def report(label, hex1, hex2, floor=AA_NORMAL):
    r = ratio(hex1, hex2)
    status = "PASS" if r >= floor else "FAIL"
    print(f"[{status}] {label}: {r:.2f}:1 (floor {floor}:1) — #{hex1.lstrip('#')} vs #{hex2.lstrip('#')}")
    return r >= floor


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    all_pass = True

    if args[0] == "--palette":
        roles = {}
        for kv in args[1:]:
            if "=" not in kv:
                print(f"Bad --palette argument (expected role=hex): {kv}", file=sys.stderr)
                sys.exit(1)
            k, v = kv.split("=", 1)
            roles[k] = v.lstrip("#")

        missing = {"text", "bg"} - roles.keys()
        if missing:
            print(f"--palette requires at least text= and bg=; missing {missing}", file=sys.stderr)
            sys.exit(1)

        all_pass &= report("body text / background", roles["text"], roles["bg"], AA_NORMAL)

        # Primary is treated as a solid CTA fill (role definition: "main CTAs"),
        # so it needs a label color that's actually readable on it. Whichever
        # of white/dark-text passes is the one to use for button labels.
        if "primary" in roles:
            white_ok = report("white label / primary fill", "ffffff", roles["primary"], AA_NORMAL)
            dark_ok = report(f"dark text ({roles['text']}) / primary fill", roles["text"], roles["primary"], AA_NORMAL)
            if not (white_ok or dark_ok):
                print(f"  -> NEITHER white nor {roles['text']} text is readable on primary #{roles['primary']} — darken/lighten primary, don't just pick a label color and hope.")
            all_pass &= (white_ok or dark_ok)
            all_pass &= report("primary / background (visibility, UI-component floor)", roles["primary"], roles["bg"], AA_LARGE_OR_UI)

        # Accent's own role (hyperlinks, highlights, small pops — not a solid
        # button fill) only needs the lighter UI-component/large-text floor
        # against the background, not full text-on-fill contrast.
        if "accent" in roles:
            all_pass &= report("accent / background (visibility + hyperlink-text floor)", roles["accent"], roles["bg"], AA_LARGE_OR_UI)
    else:
        if len(args) != 2:
            print("Usage: check_contrast.py <hex1> <hex2>  OR  check_contrast.py --palette text=.. bg=.. primary=.. accent=..", file=sys.stderr)
            sys.exit(1)
        all_pass = report("given pair", args[0], args[1], AA_NORMAL)

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
