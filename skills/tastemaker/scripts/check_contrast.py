#!/usr/bin/env python3
"""
WCAG contrast ratio checker for two hex colors, a whole palette, or the full
pairing matrix of a palette.

Why this exists: a palette (whether hand-picked, extracted from a reference
image, or a user-supplied brand color) can look fine as a swatch and still
fail contrast once it's actually used as text-on-background or a button
label. The easiest miss is checking body-text-on-background and stopping
there -- a Primary/Accent color can pass that check and still be illegible
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

    # machine-readable output (all three modes)
    python3 check_contrast.py --json 050315 fbfbfe
    python3 check_contrast.py --palette --json text=050315 bg=fbfbfe primary=2f27ce
    python3 check_contrast.py --matrix --json text=... bg=...

    # regression gate: fail if a pairing the style lock marks text-safe drops <4.5
    python3 check_contrast.py --matrix text=... bg=... --style-lock .tastemaker/style-lock.md
    python3 check_contrast.py --matrix --json text=... bg=... --style-lock .tastemaker/style-lock.md

Flags:
    --json            Emit stable JSON to stdout instead of human text. The
                      existing text output is unchanged without this flag.
    --style-lock PATH Read PATH as a .tastemaker/style-lock.md file and treat
                      its "Text-safe (>=4.5)" list as the contract. If any
                      listed pair is present in the current palette but now
                      measures <4.5, the script exits non-zero and reports the
                      offending pair(s) (both in text and in JSON under
                      "regressions"). Missing roles in the current palette are
                      ignored. Without --style-lock, --matrix remains a
                      report and exits 0 (or exits 1 only on --palette/pair
                      failures, as before).

JSON schema (stable, additive-only changes will be minor-version):
    Pair mode (--json without --palette/--matrix):
      {
        "mode": "pair",
        "pairs": [{"label": "given pair", "a": null, "b": null,
                   "hex1": "#050315", "hex2": "#fbfbfe",
                   "ratio": 19.73, "floor": 4.5, "pass": true,
                   "class": "text-safe"}],
        "pass": true,
        "regressions": []
      }

    Palette mode (--palette --json):
      {
        "mode": "palette",
        "roles": {"text": "#050315", "bg": "#fbfbfe"},
        "checks": [
          {"label": "body text / background", "a": "text", "b": "bg",
           "hex1": "#050315", "hex2": "#fbfbfe",
           "ratio": 19.73, "floor": 4.5, "pass": true, "class": "text-safe"},
          ...
        ],
        "pass": true,
        "regressions": []
      }

    Matrix mode (--matrix --json):
      {
        "mode": "matrix",
        "roles": {"text": "#e6e6ea", "bg": "#0b0d12"},
        "pairs": [
          {"a": "bg", "b": "on-primary", "hex1": "#0b0d12", "hex2": "#ffffff",
           "ratio": 19.43, "class": "text-safe"},
          ...
        ],
        "groups": {
          "text_safe": ["bg/on-primary"],
          "ui_safe": ["text/primary"],
          "decorative": ["primary/accent"]
        },
        "pass": true,
        "regressions": [
          {"pair": "bg/accent", "ratio": 2.51, "expected": "text-safe"}
        ]
      }
    Notes:
      - ratio is rounded to 2 decimals in JSON (same as text).
      - class is one of "text-safe" (>=4.5), "ui-safe" (>=3.0 and <4.5),
        "decorative" (<3.0).
      - groups.* contain "a/b" strings sorted by descending ratio, matching
        the text summary order.
      - "pass" is true when no check failed and no regressions were found.

Exit code:
    0  all checks passed and no regressions
    1  any --palette/pair check failed, or any --style-lock regression (<4.5)
    2  usage error (bad args, missing roles, unreadable style-lock)
"""

import sys
import json
import re

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


def _class_for(r):
    if r >= AA_NORMAL:
        return "text-safe"
    if r >= AA_LARGE_OR_UI:
        return "ui-safe"
    return "decorative"


def report(label, hex1, hex2, floor=AA_NORMAL):
    r = ratio(hex1, hex2)
    status = "PASS" if r >= floor else "FAIL"
    print(f"[{status}] {label}: {r:.2f}:1 (floor {floor}:1) -- #{hex1.lstrip('#')} vs #{hex2.lstrip('#')}")
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


def run_matrix(roles, json_mode=False):
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
        cls = _class_for(r)
        if cls == "text-safe":
            text_safe.append(f"{a}/{b}")
        elif cls == "ui-safe":
            ui_safe.append(f"{a}/{b}")
        else:
            decorative.append(f"{a}/{b}")
        structured_pairs.append((a, b, r, cls))

    if json_mode:
        return {
            "pairs": structured_pairs,
            "groups": {"text_safe": text_safe, "ui_safe": ui_safe, "decorative": decorative},
        }

    print(f"== Contrast matrix ({len(names)} roles, {len(pairs)} pairs) ==")
    for a, b, r, cls in structured_pairs:
        if cls == "text-safe":
            label = "text-safe (>=4.5)"
        elif cls == "ui-safe":
            label = "UI-safe  (>=3.0)"
        else:
            label = "decorative (<3.0)"
        print(f"  {a:<12} x {b:<12} {r:6.2f}  {label}")

    print()
    print("== Legal pairings (record these in the style lock) ==")
    print(f"  Text-safe   (body text, links, button labels on a fill; >=4.5): {', '.join(text_safe) or 'none'}")
    print(f"  UI-safe     (large text, icons, and borders that convey state; >=3.0 and <4.5): {', '.join(ui_safe) or 'none'}")
    print(f"  Decorative  (below 3.0; fine as a subtle hairline, must NOT be the only thing conveying state): {', '.join(decorative) or 'none'}")
    return {"pairs": structured_pairs, "groups": {"text_safe": text_safe, "ui_safe": ui_safe, "decorative": decorative}}


def parse_style_lock_text_safe(path):
    try:
        text = open(path, encoding="utf-8").read()
    except Exception as e:
        print(f"Failed to read style-lock {path}: {e}", file=sys.stderr)
        sys.exit(2)
    m = re.search(r"Text-safe\s*\(>=4\.5\)\s*:\s*(.*)", text)
    if not m:
        return set()
    line = m.group(1).strip()
    pairs = set()
    for part in line.split(","):
        part = part.strip()
        if not part or part.lower() == "none":
            continue
        token = re.split(r"\s|\(", part, maxsplit=1)[0].strip()
        if "/" in token:
            pairs.add(token.strip())
    return pairs
def compute_regressions(roles, text_safe_pairs):
    regressions = []
    if not text_safe_pairs:
        return regressions
    for pair in sorted(text_safe_pairs):
        if "/" not in pair:
            continue
        a, b = pair.split("/", 1)
        a = a.strip()
        b = b.strip()
        if a not in roles or b not in roles:
            continue
        try:
            r = ratio(roles[a], roles[b])
        except Exception:
            continue
        if r < AA_NORMAL:
            regressions.append({"pair": pair, "ratio": round(r, 2), "expected": "text-safe"})
    regressions.sort(key=lambda x: x["pair"])
    return regressions


def main():
    raw_args = sys.argv[1:]
    if not raw_args:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    json_mode = False
    style_lock_path = None
    args = []
    i = 0
    while i < len(raw_args):
        tok = raw_args[i]
        if tok == "--json":
            json_mode = True
        elif tok == "--style-lock":
            if i + 1 >= len(raw_args):
                print("--style-lock requires a path", file=sys.stderr)
                sys.exit(2)
            style_lock_path = raw_args[i + 1]
            i += 1
        elif tok.startswith("--style-lock="):
            style_lock_path = tok.split("=", 1)[1]
        else:
            args.append(tok)
        i += 1

    if not args:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    if args[0] == "--matrix":
        roles = parse_roles(args[1:])
        if len(roles) < 2:
            print("--matrix needs at least two role=hex colors.", file=sys.stderr)
            sys.exit(2)
        data = run_matrix(roles, json_mode=json_mode)
        regressions = []
        if style_lock_path:
            text_safe = parse_style_lock_text_safe(style_lock_path)
            regressions = compute_regressions(roles, text_safe)
        if json_mode:
            pairs_json = []
            for a, b, r, cls in data["pairs"]:
                pairs_json.append({
                    "a": a, "b": b,
                    "hex1": f"#{roles[a].lstrip('#')}",
                    "hex2": f"#{roles[b].lstrip('#')}",
                    "ratio": round(r, 2),
                    "class": cls,
                })
            out = {
                "mode": "matrix",
                "roles": {k: f"#{v.lstrip('#')}" for k, v in roles.items()},
                "pairs": pairs_json,
                "groups": data["groups"],
                "pass": len(regressions) == 0,
            }
            if style_lock_path is not None:
                out["regressions"] = regressions
                out["style_lock"] = style_lock_path
            print(json.dumps(out, indent=2))
            if regressions:
                for reg in regressions:
                    print(f"Regression: {reg['pair']} is {reg['ratio']}:1, expected >=4.5 (text-safe per {style_lock_path})", file=sys.stderr)
                sys.exit(1)
            sys.exit(0)
        else:
            if regressions:
                print()
                print("== Regression check (against style-lock) ==")
                for reg in regressions:
                    print(f"  FAIL  {reg['pair']}: {reg['ratio']:.2f}:1 -- expected text-safe >=4.5 (from {style_lock_path})")
                print("", file=sys.stderr)
                print("== Regression check (against style-lock) ==", file=sys.stderr)
                for reg in regressions:
                    print(f"  FAIL  {reg['pair']}: {reg['ratio']:.2f}:1 -- expected text-safe >=4.5 (from {style_lock_path})", file=sys.stderr)
                sys.exit(1)
            sys.exit(0)

    all_pass = True
    regressions = []

    if args[0] == "--palette":
        roles = parse_roles(args[1:])
        missing = {"text", "bg"} - roles.keys()
        if missing:
            print(f"--palette requires at least text= and bg=; missing {missing}", file=sys.stderr)
            sys.exit(2)
        checks = []

        def _check(label, hex1, hex2, floor, a_name=None, b_name=None):
            r = ratio(hex1, hex2)
            ok = r >= floor
            cls = _class_for(r)
            checks.append({
                "label": label, "a": a_name, "b": b_name,
                "hex1": f"#{hex1.lstrip('#')}", "hex2": f"#{hex2.lstrip('#')}",
                "ratio": round(r, 2), "floor": floor, "pass": ok, "class": cls,
            })
            if not json_mode:
                status = "PASS" if ok else "FAIL"
                print(f"[{status}] {label}: {r:.2f}:1 (floor {floor}:1) -- #{hex1.lstrip('#')} vs #{hex2.lstrip('#')}")
            return ok

        p1 = _check("body text / background", roles["text"], roles["bg"], AA_NORMAL, "text", "bg")
        all_pass &= p1

        if "primary" in roles:
            r_white = ratio("ffffff", roles["primary"])
            r_dark = ratio(roles["text"], roles["primary"])
            white_ok = r_white >= AA_NORMAL
            dark_ok = r_dark >= AA_NORMAL
            _check("white label / primary fill", "ffffff", roles["primary"], AA_NORMAL, "on-primary", "primary")
            _check(f"dark text ({roles['text']}) / primary fill", roles["text"], roles["primary"], AA_NORMAL, "text", "primary")
            if not json_mode and not (white_ok or dark_ok):
                print(f"  -> NEITHER white nor {roles['text']} text is readable on primary #{roles['primary']} -- darken/lighten primary, don't just pick a label color and hope.")
            all_pass &= (white_ok or dark_ok)
            p2 = _check("primary / background (visibility, UI-component floor)", roles["primary"], roles["bg"], AA_LARGE_OR_UI, "primary", "bg")
            all_pass &= p2

        if "accent" in roles:
            p3 = _check("accent / background (visibility + hyperlink-text floor)", roles["accent"], roles["bg"], AA_LARGE_OR_UI, "accent", "bg")
            all_pass &= p3

        if style_lock_path:
            text_safe = parse_style_lock_text_safe(style_lock_path)
            regressions = compute_regressions(roles, text_safe)
            if regressions:
                all_pass = False

        if json_mode:
            roles_json = {k: f"#{v.lstrip('#')}" for k, v in roles.items()}
            out = {
                "mode": "palette",
                "roles": roles_json,
                "checks": checks,
                "pass": bool(all_pass and not regressions),
            }
            if style_lock_path is not None:
                out["regressions"] = regressions
                out["style_lock"] = style_lock_path
            print(json.dumps(out, indent=2))
            if regressions:
                for reg in regressions:
                    print(f"Regression: {reg['pair']} is {reg['ratio']}:1, expected >=4.5 (text-safe per {style_lock_path})", file=sys.stderr)
            sys.exit(0 if all_pass and not regressions else 1)
        else:
            if regressions:
                print()
                print("== Regression check (against style-lock) ==")
                for reg in regressions:
                    print(f"  FAIL  {reg['pair']}: {reg['ratio']:.2f}:1 -- expected text-safe >=4.5 (from {style_lock_path})")
                print("", file=sys.stderr)
                print("== Regression check (against style-lock) ==", file=sys.stderr)
                for reg in regressions:
                    print(f"  FAIL  {reg['pair']}: {reg['ratio']:.2f}:1 -- expected text-safe >=4.5 (from {style_lock_path})", file=sys.stderr)
            sys.exit(0 if all_pass and not regressions else 1)

    else:
        if len(args) != 2:
            print("Usage: check_contrast.py <hex1> <hex2>  OR  --palette role=hex ...  OR  --matrix role=hex ...", file=sys.stderr)
            print("       Add --json for machine-readable output, --style-lock PATH to gate regressions.", file=sys.stderr)
            sys.exit(2)
        hex1, hex2 = args[0], args[1]
        r = ratio(hex1, hex2)
        ok = r >= AA_NORMAL
        cls = _class_for(r)
        all_pass = ok
        if json_mode:
            out = {
                "mode": "pair",
                "pairs": [{
                    "label": "given pair",
                    "a": None, "b": None,
                    "hex1": f"#{hex1.lstrip('#')}",
                    "hex2": f"#{hex2.lstrip('#')}",
                    "ratio": round(r, 2),
                    "floor": AA_NORMAL,
                    "pass": ok,
                    "class": cls,
                }],
                "pass": bool(ok),
            }
            if style_lock_path is not None:
                out["regressions"] = []
                out["style_lock"] = style_lock_path
            print(json.dumps(out, indent=2))
            sys.exit(0 if ok else 1)
        else:
            report("given pair", hex1, hex2, AA_NORMAL)
            sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

