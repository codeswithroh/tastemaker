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

    # a five-role palette: checks the critical pairings and PASS/FAILs
    python3 check_contrast.py --palette text=050315 bg=fbfbfe primary=2f27ce \
        secondary=dedcff accent=433bff

    # the full pairing matrix: every color pair, classified by which floor it
    # clears, plus a legal-pairings summary to record in the style lock.
    python3 check_contrast.py --matrix text=e6e6ea bg=0b0d12 surface=161a21 \
        primary=047857 accent=34d399 border=232a33 on-primary=ffffff

    # CI: read palette and text-safe pairings from the style lock and fail if
    # any text-safe pairing drops below 4.5:1
    python3 check_contrast.py --ci --style-lock .tastemaker/style-lock.md

    # CI with explicit palette overriding the style lock palette
    python3 check_contrast.py --palette text=050315 bg=fbfbfe primary=2f27ce \
        --style-lock .tastemaker/style-lock.md

--json output:
    Any mode accepts --json. When present, the script emits a single JSON
    document to stdout instead of human-readable text. The shapes are:

      pair:
        {"mode": "pair",
         "results": [{label, hex1, hex2, ratio, floor, pass}],
         "all_pass": bool}

      palette:
        {"mode": "palette",
         "results": [...],
         "all_pass": bool,
         "style_lock_failures": [{a, b, reason, ratio?}]}

      matrix:
        {"mode": "matrix",
         "roles": {name: hex, ...},
         "pairs": [{a, b, ratio, class}],
         "legal_pairings": {"text_safe": [...], "ui_safe": [...], "decorative": [...]}}

      ci:
        {"mode": "ci",
         "style_lock": "<path>",
         "palette": {name: hex, ...},
         "results": [{a, b, ratio, pass, reason}],
         "failures": [{a, b, reason, ratio?}],
         "all_pass": bool}

    `class` is one of text-safe (>=4.5), ui-safe (>=3.0 and <4.5), decorative
    (<3.0). `ratio` is the raw WCAG ratio rounded to 4 decimal places.

Exit codes:
    - single-pair:   0 on pass, 1 on fail.
    - --palette:     0 if every checked pairing passes its floor, 1 otherwise.
    - --matrix:      0 always (report, not a gate).
    - --ci:          0 if every text-safe pairing from the style lock is
                     >=4.5:1, 1 if any falls below or a role in the lock is
                     missing from the palette.
"""

import json
import re
import sys

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


def _classify(r):
    if r >= AA_NORMAL:
        return "text-safe"
    if r >= AA_LARGE_OR_UI:
        return "ui-safe"
    return "decorative"


def _make_result(label, hex1, hex2, floor=AA_NORMAL):
    r = ratio(hex1, hex2)
    return {
        "label": label,
        "hex1": "#" + hex1.lstrip("#"),
        "hex2": "#" + hex2.lstrip("#"),
        "ratio": round(r, 4),
        "floor": floor,
        "pass": r >= floor,
    }


def report(label, hex1, hex2, floor=AA_NORMAL, as_json=False):
    result = _make_result(label, hex1, hex2, floor)
    if not as_json:
        status = "PASS" if result["pass"] else "FAIL"
        print(f"[{status}] {label}: {result['ratio']:.2f}:1 (floor {floor}:1) — "
              f"{result['hex1']} vs {result['hex2']}")
    return result


def parse_roles(args):
    roles = {}
    for kv in args:
        if "=" not in kv:
            print(f"Bad argument (expected role=hex): {kv}", file=sys.stderr)
            sys.exit(1)
        k, v = kv.split("=", 1)
        roles[k] = v.lstrip("#")
    return roles


def run_matrix(roles, as_json=False):
    names = list(roles.keys())
    pairs = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            pairs.append((a, b, ratio(roles[a], roles[b])))
    pairs.sort(key=lambda p: -p[2])

    text_safe, ui_safe, decorative = [], [], []
    structured_pairs = []
    for a, b, r in pairs:
        cls = _classify(r)
        structured_pairs.append({"a": a, "b": b, "ratio": round(r, 4), "class": cls})
        if cls == "text-safe":
            text_safe.append(f"{a}/{b}")
        elif cls == "ui-safe":
            ui_safe.append(f"{a}/{b}")
        else:
            decorative.append(f"{a}/{b}")

    if as_json:
        print(json.dumps({
            "mode": "matrix",
            "roles": roles,
            "pairs": structured_pairs,
            "legal_pairings": {
                "text_safe": text_safe,
                "ui_safe": ui_safe,
                "decorative": decorative,
            },
        }, indent=2))
        return

    print(f"== Contrast matrix ({len(names)} roles, {len(pairs)} pairs) ==")
    class_display = {
        "text-safe": "text-safe (>=4.5)",
        "ui-safe": "UI-safe  (>=3.0)",
        "decorative": "decorative (<3.0)",
    }
    for p in structured_pairs:
        print(f"  {p['a']:<12} x {p['b']:<12} {p['ratio']:6.2f}  {class_display[p['class']]}")
    print()
    print("== Legal pairings (record these in the style lock) ==")
    print(f"  Text-safe   (body text, links, button labels on a fill; >=4.5): {', '.join(text_safe) or 'none'}")
    print(f"  UI-safe     (large text, icons, and borders that convey state; >=3.0 and <4.5): {', '.join(ui_safe) or 'none'}")
    print(f"  Decorative  (below 3.0; fine as a subtle hairline, must NOT be the only thing conveying state): {', '.join(decorative) or 'none'}")


def _parse_style_lock(path):
    try:
        text = open(path, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"[style-lock] {path} not found, ignoring", file=sys.stderr)
        return {"palette": {}, "text_safe_pairs": []}

    palette = {}
    for m in re.finditer(
        r"^\s*[-*|]?\s*([a-z][a-z0-9_-]*)\s*[:=|]\s*`?#?([0-9a-fA-F]{6})`?",
        text, re.MULTILINE,
    ):
        palette[m.group(1).lower()] = m.group(2).lower()

    text_safe_pairs = []
    m = re.search(
        r"[Tt]ext-safe[^:\n]*:\s*([^\n]*(?:\n\s*[-*][^\n]+)*)",
        text,
    )
    if m:
        for piece in re.split(r"[,;\n]\s*", m.group(1)):
            piece = piece.strip().lstrip("-*` ").rstrip("` ")
            if "/" in piece and piece.lower() != "none":
                a, b = (s.strip().lower() for s in piece.split("/", 1))
                if re.fullmatch(r"[a-z][a-z0-9_-]*", a) and re.fullmatch(r"[a-z][a-z0-9_-]*", b):
                    text_safe_pairs.append((a, b))

    return {"palette": palette, "text_safe_pairs": text_safe_pairs}


def _extract_arg(args, flag):
    for i, a in enumerate(args):
        if a == flag:
            if i + 1 >= len(args):
                print(f"{flag} needs a value", file=sys.stderr)
                sys.exit(1)
            val = args[i + 1]
            del args[i:i + 2]
            return val
    return None


def _run_ci(roles, pairs, as_json=False, style_lock_path=None):
    results = []
    failures = []
    for a, b in pairs:
        if a not in roles or b not in roles:
            rec = {"a": a, "b": b, "reason": "missing_role"}
            results.append(rec)
            failures.append(rec)
            continue
        r = ratio(roles[a], roles[b])
        rec = {
            "a": a, "b": b, "ratio": round(r, 4),
            "pass": r >= AA_NORMAL,
            "reason": "ok" if r >= AA_NORMAL else "below_text_safe_floor",
        }
        results.append(rec)
        if not rec["pass"]:
            failures.append(rec)

    if as_json:
        print(json.dumps({
            "mode": "ci",
            "style_lock": style_lock_path,
            "palette": roles,
            "results": results,
            "failures": failures,
            "all_pass": not failures,
        }, indent=2))
    else:
        for rec in results:
            if rec.get("reason") == "missing_role":
                print(f"[FAIL] {rec['a']}/{rec['b']}: role missing from palette")
            else:
                status = "PASS" if rec["pass"] else "FAIL"
                print(f"[{status}] {rec['a']}/{rec['b']}: {rec['ratio']:.2f}:1 (floor {AA_NORMAL}:1)")
        if failures:
            print()
            print(f"== {len(failures)} text-safe pair(s) below {AA_NORMAL}:1 ==")
            for rec in failures:
                ratio_str = f"{rec['ratio']:.2f}:1" if "ratio" in rec else "n/a"
                print(f"  {rec['a']}/{rec['b']}: {ratio_str} ({rec['reason']})")
    sys.exit(0 if not failures else 1)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    as_json = "--json" in args
    if as_json:
        args = [a for a in args if a != "--json"]
    style_lock = _extract_arg(args, "--style-lock")

    if not args:
        print("No mode specified (need --matrix, --palette, --ci, or two hex colors).",
              file=sys.stderr)
        sys.exit(1)

    if args[0] == "--ci":
        if not style_lock:
            print("--ci requires --style-lock <path>", file=sys.stderr)
            sys.exit(1)
        lock = _parse_style_lock(style_lock)
        if not lock["palette"]:
            print(f"No palette entries found in {style_lock}", file=sys.stderr)
            sys.exit(1)
        if not lock["text_safe_pairs"]:
            print(f"No 'Text-safe ...:' pairings found in {style_lock}", file=sys.stderr)
            sys.exit(1)
        _run_ci(lock["palette"], lock["text_safe_pairs"], as_json, style_lock)
        return

    if args[0] == "--matrix":
        roles = parse_roles(args[1:])
        if len(roles) < 2:
            print("--matrix needs at least two role=hex colors.", file=sys.stderr)
            sys.exit(1)
        run_matrix(roles, as_json=as_json)
        sys.exit(0)

    if args[0] == "--palette":
        roles = parse_roles(args[1:])
        missing = {"text", "bg"} - roles.keys()
        if missing:
            print(f"--palette requires at least text= and bg=; missing {missing}",
                  file=sys.stderr)
            sys.exit(1)

        results = []
        all_pass = True

        r = report("body text / background", roles["text"], roles["bg"], AA_NORMAL, as_json)
        results.append(r); all_pass &= r["pass"]

        if "primary" in roles:
            white_r = report("white label / primary fill", "ffffff", roles["primary"], AA_NORMAL, as_json)
            dark_r  = report(f"dark text ({roles['text']}) / primary fill", roles["text"], roles["primary"], AA_NORMAL, as_json)
            results.extend([white_r, dark_r])
            label_ok = white_r["pass"] or dark_r["pass"]
            if not label_ok and not as_json:
                print(f"  -> NEITHER white nor {roles['text']} text is readable on primary "
                      f"#{roles['primary']} — darken/lighten primary, don't just pick a label "
                      f"color and hope.")
            all_pass &= label_ok

            prim_bg_r = report("primary / background (visibility, UI-component floor)",
                               roles["primary"], roles["bg"], AA_LARGE_OR_UI, as_json)
            results.append(prim_bg_r); all_pass &= prim_bg_r["pass"]

        if "accent" in roles:
            acc_r = report("accent / background (visibility + hyperlink-text floor)",
                           roles["accent"], roles["bg"], AA_LARGE_OR_UI, as_json)
            results.append(acc_r); all_pass &= acc_r["pass"]

        style_lock_failures = []
        if style_lock:
            lock = _parse_style_lock(style_lock)
            for a, b in lock["text_safe_pairs"]:
                if a not in roles or b not in roles:
                    style_lock_failures.append({"a": a, "b": b, "reason": "missing_role"})
                    continue
                rr = ratio(roles[a], roles[b])
                if rr < AA_NORMAL:
                    style_lock_failures.append({
                        "a": a, "b": b, "ratio": round(rr, 4),
                        "reason": "below_text_safe_floor",
                    })
            if style_lock_failures:
                all_pass = False

        if as_json:
            print(json.dumps({
                "mode": "palette",
                "results": results,
                "all_pass": all_pass,
                "style_lock_failures": style_lock_failures,
            }, indent=2))
        elif style_lock_failures:
            print()
            print(f"== Style lock failures ({style_lock}) ==")
            for f in style_lock_failures:
                ratio_str = f"{f['ratio']:.2f}:1" if "ratio" in f else "n/a"
                print(f"  {f['a']}/{f['b']}: {ratio_str} ({f['reason']})")

        sys.exit(0 if all_pass else 1)

    if len(args) != 2:
        print("Usage: check_contrast.py <hex1> <hex2>  OR  --palette role=hex ...  "
              "OR  --matrix role=hex ...  OR  --ci --style-lock <path>",
              file=sys.stderr)
        sys.exit(1)
    result = report("given pair", args[0], args[1], AA_NORMAL, as_json)
    if as_json:
        print(json.dumps({
            "mode": "pair",
            "results": [result],
            "all_pass": result["pass"],
        }, indent=2))
    sys.exit(0 if result["pass"] else 1)


if __name__ == "__main__":
    main()
