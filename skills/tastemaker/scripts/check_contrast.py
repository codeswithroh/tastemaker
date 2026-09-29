#!/usr/bin/env python3
"""
WCAG contrast ratio checker for two hex colors, a whole palette, or the full
pairing matrix of a palette.

Why this exists: a palette (whether hand-picked, extracted from a reference
image, or a user-supplied brand color) can look fine as a swatch and still
fail contrast once it's actually used as text-on-background or a button
label. The easiest miss is checking body-text-on-background and stopping
there — a Primary/Accent color can pass that check and still be illegible
as a button fill with white label text. This script checks pairs directly
against the real WCAG math instead of eyeballing it.

The deeper miss is time: a palette that passed for the pairings you enumerated
at authoring time can still fail the moment the model uses two of its colors
in a pairing you never listed. --matrix answers "which of these colors may
legally touch which," so the lock certifies the palette as *usable*, not just
as authored. See the contract described in references/style-lock-format.md.

Usage:
    # single pair
    python3 check_contrast.py 050315 fbfbfe
    python3 check_contrast.py "#050315" "#FBFBFE"

    # a five-role palette: checks the critical pairings and PASS/FAILs
    python3 check_contrast.py --palette text=050315 bg=fbfbfe primary=2f27ce \
        secondary=dedcff accent=433bff

    # the full pairing matrix: every color pair, classified by which floor it
    # clears, plus a legal-pairings summary to record in the style lock.
    # Include a label color (e.g. on-primary=ffffff) to see button-label legality.
    python3 check_contrast.py --matrix text=e6e6ea bg=0b0d12 surface=161a21 \
        primary=047857 accent=34d399 border=232a33 on-primary=ffffff

Machine output: add --json in any mode. The object has a stable `mode`,
`passed`, and `pairs` array. Each pair has `a`, `b`, `ratio` (full precision),
`class` (`text-safe`, `ui-safe`, or `decorative`), `floor`, and `passed`.
Matrix output also has `legal_pairings` with arrays for each class. Pair order
is descending by ratio in matrix mode; palette checks retain their display
order. Use --check-lock PATH to compare the lock's declared Text-safe pairs
with its current palette; it works with or without --json.

Exit code: --palette and single-pair exit nonzero if any checked pairing fails
its floor. --matrix is a report and exits 0 unless --check-lock finds a
declared text-safe pairing below 4.5:1.
"""

import json
import re
import sys
from pathlib import Path

AA_NORMAL = 4.5        # body text on its background
AA_LARGE_OR_UI = 3.0   # large text, UI components, graphical objects (WCAG 1.4.11)


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


def parse_roles(args):
    roles = {}
    for kv in args:
        if "=" not in kv:
            print(f"Bad argument (expected role=hex): {kv}", file=sys.stderr)
            sys.exit(1)
        k, v = kv.split("=", 1)
        roles[k] = v.lstrip("#")
    return roles


def run_matrix(roles):
    names = list(roles.keys())
    pairs = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            pairs.append((a, b, ratio(roles[a], roles[b])))
    pairs.sort(key=lambda p: -p[2])

    text_safe, ui_safe, decorative = [], [], []
    print(f"== Contrast matrix ({len(names)} roles, {len(pairs)} pairs) ==")
    for a, b, r in pairs:
        if r >= AA_NORMAL:
            cls = "text-safe (>=4.5)"
            text_safe.append(f"{a}/{b}")
        elif r >= AA_LARGE_OR_UI:
            cls = "UI-safe  (>=3.0)"
            ui_safe.append(f"{a}/{b}")
        else:
            cls = "decorative (<3.0)"
            decorative.append(f"{a}/{b}")
        print(f"  {a:<12} x {b:<12} {r:6.2f}  {cls}")

    print()
    print("== Legal pairings (record these in the style lock) ==")
    print(f"  Text-safe   (body text, links, button labels on a fill; >=4.5): {', '.join(text_safe) or 'none'}")
    print(f"  UI-safe     (large text, icons, and borders that convey state; >=3.0 and <4.5): {', '.join(ui_safe) or 'none'}")
    print(f"  Decorative  (below 3.0; fine as a subtle hairline, must NOT be the only thing conveying state): {', '.join(decorative) or 'none'}")
    return pairs


def classify(r):
    return "text-safe" if r >= AA_NORMAL else "ui-safe" if r >= AA_LARGE_OR_UI else "decorative"


def pair_data(a, b, color_a, color_b, floor):
    r = ratio(color_a, color_b)
    return {"a": a, "b": b, "ratio": r, "class": classify(r),
            "floor": floor, "passed": r >= floor}


def read_lock(path):
    """Read the Palette and Legal pairings sections from a style lock."""
    contents = Path(path).read_text(encoding="utf-8")
    palette_section = re.search(r"(?ms)^## Palette\s*$\n(.*?)(?=^## |\Z)", contents)
    contract_section = re.search(r"(?ms)^## Color contract\s*$\n(.*?)(?=^## |\Z)", contents)
    if not palette_section or not contract_section:
        raise ValueError("style lock needs Palette and Color contract sections")
    roles = {}
    names = {"background": "bg", "text primary": "text", "text muted": "text-muted",
             "button label color": "on-primary"}
    for label, value in re.findall(r"(?mi)^\s*-\s*([^:\n]+):\s*(#[0-9a-fA-F]{6})\b", palette_section.group(1)):
        roles[names.get(label.strip().lower(), label.strip().lower().replace(" ", "-"))] = value[1:]
    # A white label is often specified by name, rather than as a hex value.
    if re.search(r"(?mi)^\s*-\s*Button label color:\s*white\b", palette_section.group(1)):
        roles["on-primary"] = "ffffff"
    elif re.search(r"(?mi)^\s*-\s*Button label color:\s*text primary\b", palette_section.group(1)) and "text" in roles:
        roles["on-primary"] = roles["text"]
    declared = re.search(r"(?mi)^\s*-\s*Text-safe\s*(?:\(.*?\))?\s*:\s*(.*)$", contract_section.group(1))
    if not declared:
        raise ValueError("style lock needs a Text-safe legal pairings line")
    pairs = re.findall(r"([\w-]+)\s*/\s*([\w-]+)", declared.group(1))
    if not pairs:
        raise ValueError("style lock has no declared Text-safe pairs")
    for a, b in pairs:
        if a not in roles or b not in roles:
            raise ValueError(f"text-safe pair {a}/{b} references a missing palette role")
    return roles, pairs


def json_output(mode, pairs, passed):
    result = {"mode": mode, "passed": passed, "pairs": pairs}
    if mode == "matrix":
        result["legal_pairings"] = {cls: [f"{p['a']}/{p['b']}" for p in pairs if p["class"] == cls]
                                    for cls in ("text-safe", "ui-safe", "decorative")}
    print(json.dumps(result, indent=2))


def main():
    args = sys.argv[1:]
    as_json = "--json" in args
    args = [arg for arg in args if arg != "--json"]
    lock_path = None
    if "--check-lock" in args:
        index = args.index("--check-lock")
        if index + 1 >= len(args):
            print("--check-lock needs a path", file=sys.stderr)
            sys.exit(1)
        lock_path = args[index + 1]
        del args[index:index + 2]
    if lock_path:
        try:
            lock_roles, declared = read_lock(lock_path)
        except (OSError, ValueError) as exc:
            print(f"Invalid style lock: {exc}", file=sys.stderr)
            sys.exit(1)
        if not args:
            args = ["--matrix", *(f"{k}={v}" for k, v in lock_roles.items())]
    if not args:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    if args[0] == "--matrix":
        roles = parse_roles(args[1:])
        if len(roles) < 2:
            print("--matrix needs at least two role=hex colors.", file=sys.stderr)
            sys.exit(1)
        if as_json:
            names = list(roles)
            pairs = sorted((pair_data(a, b, roles[a], roles[b], AA_NORMAL)
                            for i, a in enumerate(names) for b in names[i + 1:]),
                           key=lambda p: -p["ratio"])
        else:
            run_matrix(roles)
        failures = []
        if lock_path:
            for a, b in declared:
                r = ratio(lock_roles[a], lock_roles[b])
                if r < AA_NORMAL:
                    failures.append(f"{a}/{b}: {r:.2f}:1 (floor 4.5:1)")
        if as_json:
            json_output("matrix", pairs, not failures)
        for failure in failures:
            print(f"[FAIL] Text-safe regression: {failure}", file=sys.stderr)
        sys.exit(1 if failures else 0)

    all_pass = True

    if args[0] == "--palette":
        roles = parse_roles(args[1:])

        missing = {"text", "bg"} - roles.keys()
        if missing:
            print(f"--palette requires at least text= and bg=; missing {missing}", file=sys.stderr)
            sys.exit(1)

        checks = [("body text / background", "text", "bg", AA_NORMAL)]
        if not as_json:
            all_pass &= report("body text / background", roles["text"], roles["bg"], AA_NORMAL)

        # Primary is treated as a solid CTA fill (role definition: "main CTAs"),
        # so it needs a label color that's actually readable on it. Whichever
        # of white/dark-text passes is the one to use for button labels.
        if "primary" in roles:
            checks.extend([("white label / primary fill", "white", "primary", AA_NORMAL),
                           (f"dark text ({roles['text']}) / primary fill", "text", "primary", AA_NORMAL)])
            white_ok = ratio("ffffff", roles["primary"]) >= AA_NORMAL if as_json else report("white label / primary fill", "ffffff", roles["primary"], AA_NORMAL)
            dark_ok = ratio(roles["text"], roles["primary"]) >= AA_NORMAL if as_json else report(f"dark text ({roles['text']}) / primary fill", roles["text"], roles["primary"], AA_NORMAL)
            if not (white_ok or dark_ok):
                if not as_json:
                    print(f"  -> NEITHER white nor {roles['text']} text is readable on primary #{roles['primary']} — darken/lighten primary, don't just pick a label color and hope.")
            all_pass &= (white_ok or dark_ok)
            checks.append(("primary / background (visibility, UI-component floor)", "primary", "bg", AA_LARGE_OR_UI))

        # Accent's own role (hyperlinks, highlights, small pops — not a solid
        # button fill) only needs the lighter UI-component/large-text floor
        # against the background, not full text-on-fill contrast.
        if "accent" in roles:
            checks.append(("accent / background (visibility + hyperlink-text floor)", "accent", "bg", AA_LARGE_OR_UI))
        output_pairs = []
        for label, a, b, floor in checks:
            ca, cb = ("ffffff" if a == "white" else roles[a]), roles[b]
            output_pairs.append(pair_data(a, b, ca, cb, floor))
            if not as_json and a not in ("white", "text"):
                all_pass &= report(label, ca, cb, floor)
        all_pass &= output_pairs[0]["passed"]
        if "primary" in roles:
            all_pass &= output_pairs[3]["passed"]
        if "accent" in roles:
            all_pass &= output_pairs[-1]["passed"]
    else:
        if len(args) != 2:
            print("Usage: check_contrast.py <hex1> <hex2>  OR  --palette role=hex ...  OR  --matrix role=hex ...", file=sys.stderr)
            sys.exit(1)
        output_pairs = [pair_data("foreground", "background", args[0], args[1], AA_NORMAL)]
        all_pass = output_pairs[0]["passed"] if as_json else report("given pair", args[0], args[1], AA_NORMAL)

    if as_json:
        json_output("palette" if args[0] == "--palette" else "pair", output_pairs, all_pass)

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
