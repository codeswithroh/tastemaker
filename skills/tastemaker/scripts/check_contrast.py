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

    # machine-readable JSON (stable, all three modes)
    python3 check_contrast.py --json 050315 fbfbfe
    python3 check_contrast.py --json --palette text=050315 bg=fbfbfe primary=2f27ce
    python3 check_contrast.py --json --matrix text=e6e6ea bg=0b0d12 primary=047857
    # --json emits one JSON object to stdout and suppresses the human-readable
    # text (stderr still carries regressions when --style-lock is used).
    # For --matrix the object contains every pair with its ratio and
    # classification (text-safe / ui-safe / decorative) plus grouped
    # legal-pairings. Stable schema:
    #   pair mode:   {mode:"pair", hex1, hex2, ratio, classification, floor, pass}
    #   palette mode:{mode:"palette", roles, checks:[{label,hex1,hex2,ratio,floor,pass}], pass, regressions?}
    #   matrix mode: {mode:"matrix", roles, pairs:[{a,b,pair,ratio,classification}], groups:{text_safe,ui_safe,decorative}, legal_pairings:{text_safe,ui_safe,decorative}, regressions}
    # ratios are rounded to 2 decimals; classifications are "text-safe" (>=4.5),
    # "ui-safe" (>=3.0 and <4.5), "decorative" (<3.0). Keys are stable.

    # style-lock regression gate (CI): fail if a text-safe pairing recorded in
    # .tastemaker/style-lock.md drops below 4.5:1
    python3 check_contrast.py --matrix text=... bg=... --style-lock .tastemaker/style-lock.md
    python3 check_contrast.py --matrix --json text=... bg=... --style-lock .tastemaker/style-lock.md

Exit code: --palette and single-pair exit nonzero if any checked pairing fails
its floor. --matrix is a report and exits 0 (it does not know each pair's
intended use, so it classifies rather than pass/fails) — unless
--style-lock is given: then any locked text-safe pairing that now measures
below 4.5:1 causes a non-zero exit and the offending pair is named in the
output (and in the JSON `regressions` array when --json is used).
"""

import sys
import json
import re
import pathlib

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


def classification_for(r):
    if r >= AA_NORMAL:
        return "text-safe"
    if r >= AA_LARGE_OR_UI:
        return "ui-safe"
    return "decorative"


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


def _matrix_data(roles):
    """Return structured matrix data without printing."""
    names = list(roles.keys())
    pairs = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            r = ratio(roles[a], roles[b])
            pairs.append((a, b, r))
    pairs.sort(key=lambda p: -p[2])
    text_safe, ui_safe, decorative = [], [], []
    pair_objs = []
    for a, b, r in pairs:
        cls = classification_for(r)
        pair_objs.append({"a": a, "b": b, "pair": f"{a}/{b}", "ratio": round(r, 2), "classification": cls})
        if cls == "text-safe":
            text_safe.append(f"{a}/{b}")
        elif cls == "ui-safe":
            ui_safe.append(f"{a}/{b}")
        else:
            decorative.append(f"{a}/{b}")
    return pairs, pair_objs, text_safe, ui_safe, decorative


def parse_style_lock_text_safe_pairs(path):
    """Parse .tastemaker/style-lock.md and return list of 'a/b' strings from Text-safe line."""
    try:
        text = pathlib.Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Style lock not found: {path}", file=sys.stderr)
        sys.exit(2)
    pairs = []
    for line in text.splitlines():
        if re.search(r"Text-safe", line, re.IGNORECASE):
            m = re.search(r"Text-safe[^:]*:\s*(.+)", line, re.IGNORECASE)
            if m:
                content = m.group(1).strip()
                if content.lower() == "none" or not content:
                    continue
                for part in content.split(","):
                    part = part.strip()
                    if not part:
                        continue
                    token = part.split()[0]
                    if "/" in token:
                        pairs.append(token.strip())
            break
    return pairs


def check_regressions(roles, style_lock_path):
    """Return list of regression dicts for locked text-safe pairs that now fail."""
    locked = parse_style_lock_text_safe_pairs(style_lock_path)
    regressions = []
    for pair in locked:
        if "/" not in pair:
            continue
        a, b = pair.split("/", 1)
        a = a.strip()
        b = b.strip()
        if a not in roles or b not in roles:
            continue
        r = ratio(roles[a], roles[b])
        if r < AA_NORMAL:
            regressions.append({"pair": f"{a}/{b}", "ratio": round(r, 2), "floor": AA_NORMAL})
    return regressions


def main():
    raw_args = sys.argv[1:]
    if not raw_args:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    # Extract global flags: --json and --style-lock
    json_mode = False
    style_lock_path = None
    filtered = []
    i = 0
    while i < len(raw_args):
        arg = raw_args[i]
        if arg == "--json":
            json_mode = True
        elif arg == "--style-lock":
            if i + 1 < len(raw_args) and not raw_args[i + 1].startswith("--"):
                style_lock_path = raw_args[i + 1]
                i += 1
            else:
                style_lock_path = ".tastemaker/style-lock.md"
        elif arg.startswith("--style-lock="):
            style_lock_path = arg.split("=", 1)[1]
        else:
            filtered.append(arg)
        i += 1

    args = filtered
    if not args:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    # --matrix
    if args[0] == "--matrix":
        roles = parse_roles(args[1:])
        if len(roles) < 2:
            print("--matrix needs at least two role=hex colors.", file=sys.stderr)
            sys.exit(1)

        if json_mode:
            pairs, pair_objs, text_safe, ui_safe, decorative = _matrix_data(roles)
            regressions = []
            if style_lock_path:
                regressions = check_regressions(roles, style_lock_path)
            out = {
                "mode": "matrix",
                "roles": roles,
                "pairs": pair_objs,
                "groups": {
                    "text_safe": text_safe,
                    "ui_safe": ui_safe,
                    "decorative": decorative,
                },
                "legal_pairings": {
                    "text_safe": text_safe,
                    "ui_safe": ui_safe,
                    "decorative": decorative,
                },
                "regressions": regressions,
            }
            json.dump(out, sys.stdout, indent=2)
            sys.stdout.write("\n")
            if regressions:
                for reg in regressions:
                    print(f"Regression: {reg['pair']} is {reg['ratio']}:1 below text-safe floor {reg['floor']}:1 (locked as text-safe)", file=sys.stderr)
                sys.exit(1)
            sys.exit(0)
        else:
            pairs = run_matrix(roles)
            if style_lock_path:
                regressions = check_regressions(roles, style_lock_path)
                if regressions:
                    for reg in regressions:
                        print(f"Regression: {reg['pair']} is {reg['ratio']}:1 below text-safe floor {reg['floor']}:1 (locked as text-safe)", file=sys.stderr)
                    sys.exit(1)
            sys.exit(0)

    all_pass = True
    checks = []

    if args[0] == "--palette":
        roles = parse_roles(args[1:])

        missing = {"text", "bg"} - roles.keys()
        if missing:
            print(f"--palette requires at least text= and bg=; missing {missing}", file=sys.stderr)
            sys.exit(1)

        def do_report(label, hex1, hex2, floor=AA_NORMAL):
            r = ratio(hex1, hex2)
            passed = r >= floor
            checks.append({"label": label, "hex1": hex1.lstrip("#"), "hex2": hex2.lstrip("#"), "ratio": round(r, 2), "floor": floor, "pass": passed})
            if not json_mode:
                status = "PASS" if passed else "FAIL"
                print(f"[{status}] {label}: {r:.2f}:1 (floor {floor}:1) — #{hex1.lstrip('#')} vs #{hex2.lstrip('#')}")
            return passed

        all_pass &= do_report("body text / background", roles["text"], roles["bg"], AA_NORMAL)

        if "primary" in roles:
            white_r = ratio("ffffff", roles["primary"])
            dark_r = ratio(roles["text"], roles["primary"])
            white_ok = white_r >= AA_NORMAL
            dark_ok = dark_r >= AA_NORMAL
            checks.append({"label": "white label / primary fill", "hex1": "ffffff", "hex2": roles["primary"], "ratio": round(white_r, 2), "floor": AA_NORMAL, "pass": white_ok})
            checks.append({"label": f"dark text ({roles['text']}) / primary fill", "hex1": roles["text"], "hex2": roles["primary"], "ratio": round(dark_r, 2), "floor": AA_NORMAL, "pass": dark_ok})
            if not json_mode:
                for c in checks[-2:]:
                    status = "PASS" if c["pass"] else "FAIL"
                    print(f"[{status}] {c['label']}: {c['ratio']:.2f}:1 (floor {c['floor']}:1) — #{c['hex1']} vs #{c['hex2']}")
                if not (white_ok or dark_ok):
                    print(f"  -> NEITHER white nor {roles['text']} text is readable on primary #{roles['primary']} — darken/lighten primary, don't just pick a label color and hope.")
            all_pass &= (white_ok or dark_ok)
            all_pass &= do_report("primary / background (visibility, UI-component floor)", roles["primary"], roles["bg"], AA_LARGE_OR_UI)

        if "accent" in roles:
            all_pass &= do_report("accent / background (visibility + hyperlink-text floor)", roles["accent"], roles["bg"], AA_LARGE_OR_UI)

        regressions = []
        if style_lock_path:
            regs = check_regressions(roles, style_lock_path)
            regressions = regs
            if regressions:
                all_pass = False
                if not json_mode:
                    for reg in regressions:
                        print(f"Regression: {reg['pair']} is {reg['ratio']}:1 below text-safe floor {reg['floor']}:1 (locked as text-safe)", file=sys.stderr)

        if json_mode:
            out = {"mode": "palette", "roles": roles, "checks": checks, "pass": bool(all_pass)}
            if style_lock_path:
                out["regressions"] = regressions
            json.dump(out, sys.stdout, indent=2)
            sys.stdout.write("\n")
            sys.exit(0 if all_pass else 1)
        else:
            if regressions:
                sys.exit(1)
            sys.exit(0 if all_pass else 1)
    else:
        if len(args) != 2:
            print("Usage: check_contrast.py <hex1> <hex2>  OR  --palette role=hex ...  OR  --matrix role=hex ...", file=sys.stderr)
            sys.exit(1)
        hex1, hex2 = args[0], args[1]
        r = ratio(hex1, hex2)
        passed = r >= AA_NORMAL
        if json_mode:
            out = {
                "mode": "pair",
                "hex1": hex1.lstrip("#"),
                "hex2": hex2.lstrip("#"),
                "ratio": round(r, 2),
                "classification": classification_for(r),
                "floor": AA_NORMAL,
                "pass": passed,
            }
            if style_lock_path:
                locked = parse_style_lock_text_safe_pairs(style_lock_path)
                out["regressions"] = []
                # If pair corresponds to a locked pair by hex correlation we cannot know role mapping, so empty
                _ = locked
            json.dump(out, sys.stdout, indent=2)
            sys.stdout.write("\n")
            sys.exit(0 if passed else 1)
        else:
            all_pass = report("given pair", hex1, hex2, AA_NORMAL)
            sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
