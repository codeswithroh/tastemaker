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

    # machine-readable JSON output (all three modes, --json is order-agnostic)
    python3 check_contrast.py --json 050315 fbfbfe
    python3 check_contrast.py --json --palette text=050315 bg=fbfbfe primary=2f27ce
    python3 check_contrast.py --palette --json text=050315 bg=fbfbfe primary=2f27ce
    python3 check_contrast.py --matrix --json text=e6e6ea bg=0b0d12 primary=047857
    python3 check_contrast.py --json --matrix text=e6e6ea bg=0b0d12 primary=047857

    # regression gate: fail when a pairing the style lock marks text-safe drops below 4.5:1
    python3 check_contrast.py --check-lock .tastemaker/style-lock.md
    python3 check_contrast.py --style-lock .tastemaker/style-lock.md
    python3 check_contrast.py --json --check-lock .tastemaker/style-lock.md
    python3 check_contrast.py --matrix text=... bg=... --check-lock .tastemaker/style-lock.md
    python3 check_contrast.py --matrix --json text=... bg=... --check-lock .tastemaker/style-lock.md

Flags:
    --json              Emit stable JSON to stdout instead of human text. The
                        existing text output is unchanged without this flag.
    --check-lock PATH   Read PATH as a .tastemaker/style-lock.md file and treat
                        its "Text-safe (>=4.5)" list as the contract. If any
                        listed pair is present in the current palette but now
                        measures <4.5, the script exits non-zero and reports the
                        offending pair(s) (both on stderr in text mode and under
                        "regressions" in JSON). Missing roles in the current
                        palette are ignored. If --check-lock is given without an
                        explicit palette/matrix/pair, the palette is read from
                        the lock file itself (self-check).
    --style-lock PATH   Alias for --check-lock.

JSON schema (stable, additive-only changes will be minor-version):
    Pair mode (--json <hex1> <hex2> [--check-lock PATH]):
      {
        "mode": "pair",
        "pairs": [{"label": "given pair", "a": null, "b": null,
                   "hex1": "#050315", "hex2": "#fbfbfe",
                   "ratio": 19.73, "floor": 4.5, "pass": true,
                   "class": "text-safe"}],
        "pass": true,
        "passed": true,
        "regressions": []                 // only when --check-lock/--style-lock given
      }

    Palette mode (--palette --json ... [--check-lock PATH]):
      {
        "mode": "palette",
        "roles": {"text": "#050315", "bg": "#fbfbfe", "primary": "#2f27ce"},
        "checks": [
          {"label": "body text / background", "a": "text", "b": "bg",
           "hex1": "#050315", "hex2": "#fbfbfe",
           "ratio": 19.73, "floor": 4.5, "pass": true, "class": "text-safe"},
          ...
        ],
        "pass": true,
        "passed": true,
        "regressions": []                 // only with --check-lock/--style-lock
      }
      checks are in display order (body text/bg first, then primary label
      checks, primary/bg, accent/bg).

    Matrix mode (--matrix --json ... [--check-lock PATH]):
      {
        "mode": "matrix",
        "roles": {"text": "#e6e6ea", "bg": "#0b0d12", ...},
        "pairs": [
          {"a": "text", "b": "bg", "hex1": "#e6e6ea", "hex2": "#0b0d12",
           "ratio": 15.12, "class": "text-safe"},
          ...
        ],
        "groups": {
          "text_safe": ["text/bg", ...],
          "ui_safe": ["text/primary", ...],
          "decorative": ["primary/accent", ...]
        },
        "legal_pairings": {               // alias for groups, same content
          "text_safe": [...], "ui_safe": [...], "decorative": [...]
        },
        "pass": true,
        "passed": true,
        "regressions": [                  // only with --check-lock/--style-lock
          {"pair": "bg/accent", "ratio": 2.51, "expected": "text-safe"}
        ],
        "style_lock": ".tastemaker/style-lock.md"  // only with --check-lock/--style-lock
      }
    Notes:
      - ratio is rounded to 2 decimals in JSON (same as text).
      - class is one of "text-safe" (>=4.5), "ui-safe" (>=3.0 and <4.5),
        "decorative" (<3.0).
      - groups and legal_pairings contain "a/b" strings sorted by descending
        ratio, matching the text summary order.
      - "pass"/"passed" is true when no check failed and no regressions were found.
      - When --check-lock/--style-lock is given without explicit roles, roles
        are read from the lock's Palette section and checked against its own
        Text-safe list (self-check).

Exit code:
    0  all checks passed and no regressions
    1  any --palette/pair check failed, or any --check-lock/--style-lock regression
       (<4.5) for a declared text-safe pairing, or invalid lock when fail-closed
       is required
    2  usage error (bad args, missing roles, unreadable lock file path)
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


def _class_for(r):
    if r >= AA_NORMAL:
        return "text-safe"
    if r >= AA_LARGE_OR_UI:
        return "ui-safe"
    return "decorative"


def _compute_matrix_data(roles):
    names = list(roles.keys())
    pairs = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            pairs.append((a, b, ratio(roles[a], roles[b])))
    pairs.sort(key=lambda p: -p[2])
    text_safe, ui_safe, decorative = [], [], []
    structured = []
    for a, b, r in pairs:
        cls = _class_for(r)
        if cls == "text-safe":
            text_safe.append(f"{a}/{b}")
        elif cls == "ui-safe":
            ui_safe.append(f"{a}/{b}")
        else:
            decorative.append(f"{a}/{b}")
        structured.append((a, b, r, cls))
    groups = {"text_safe": text_safe, "ui_safe": ui_safe, "decorative": decorative}
    return structured, groups


def parse_style_lock_text_safe(path):
    try:
        txt = pathlib.Path(path).read_text(encoding="utf-8")
    except Exception as e:
        print(f"Failed to read style-lock {path}: {e}", file=sys.stderr)
        sys.exit(2)
    m = re.search(r"Text-safe\s*\(>=4\.5\)\s*:\s*(.*)", txt)
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


def parse_style_lock_palette(path):
    try:
        txt = pathlib.Path(path).read_text(encoding="utf-8")
    except Exception as e:
        print(f"Failed to read style-lock {path}: {e}", file=sys.stderr)
        sys.exit(2)
    m = re.search(r"## Palette(.*?)(?:\n## |\Z)", txt, re.S)
    section = m.group(1) if m else txt
    mapping = {
        "button label color": "on-primary",
        "on-dark text": "on-dark",
        "text primary": "text",
        "text muted": "muted",
        "dark surface": "dark",
        "background": "bg",
        "surface": "surface",
        "primary": "primary",
        "accent": "accent",
        "on-dark": "on-dark",
        "on-primary": "on-primary",
        "border": "border",
        "text": "text",
        "muted": "muted",
        "dark": "dark",
        "bg": "bg",
    }
    roles = {}
    sorted_keys = sorted(mapping, key=lambda k: -len(k))
    for line in section.splitlines():
        hm = re.search(r"#([0-9a-fA-F]{6})", line)
        if not hm:
            continue
        hv = hm.group(1).lower()
        lm = re.search(r"-\s*([^:]+):", line)
        if not lm:
            continue
        lb = lm.group(1).strip().lower()
        lb = re.sub(r"^[^a-z]+", "", lb)
        key = mapping.get(lb)
        if not key:
            for k in sorted_keys:
                if k in lb:
                    key = mapping[k]
                    break
        if key and key not in roles:
            roles[key] = hv
    if "on-primary" not in roles:
        if re.search(r"button label color:\s*white\b", section, re.I):
            roles["on-primary"] = "ffffff"
        elif re.search(r"button label color:\s*text primary\b", section, re.I) and "text" in roles:
            roles["on-primary"] = roles["text"]
    return roles


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
        elif tok == "--check-lock" or tok == "--style-lock":
            if i + 1 >= len(raw_args):
                print(f"{tok} requires a path", file=sys.stderr)
                sys.exit(2)
            style_lock_path = raw_args[i + 1]
            i += 1
        elif tok.startswith("--check-lock="):
            style_lock_path = tok.split("=", 1)[1]
        elif tok.startswith("--style-lock="):
            style_lock_path = tok.split("=", 1)[1]
        else:
            args.append(tok)
        i += 1

    if style_lock_path is not None and not args:
        roles = parse_style_lock_palette(style_lock_path)
        if len(roles) < 2:
            print(f"Failed to extract palette from {style_lock_path} (found {roles})", file=sys.stderr)
            sys.exit(2)
        text_safe = parse_style_lock_text_safe(style_lock_path)
        if not text_safe:
            print(f"Style lock {style_lock_path} has no Text-safe list to check", file=sys.stderr)
            sys.exit(2)
        regressions = compute_regressions(roles, text_safe)
        structured, groups = _compute_matrix_data(roles)
        if json_mode:
            pairs_json = []
            for a, b, r, cls in structured:
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
                "groups": groups,
                "legal_pairings": groups,
                "pass": len(regressions) == 0,
                "passed": len(regressions) == 0,
                "regressions": regressions,
                "style_lock": style_lock_path,
            }
            print(json.dumps(out, indent=2))
            if regressions:
                for reg in regressions:
                    print(f"Regression: {reg['pair']} is {reg['ratio']}:1, expected >=4.5 (text-safe per {style_lock_path})", file=sys.stderr)
                sys.exit(1)
            sys.exit(0)
        else:
            run_matrix(roles)
            if regressions:
                print()
                print("== Regression check (against style-lock) ==")
                for reg in regressions:
                    print(f"  FAIL  {reg['pair']}: {reg['ratio']:.2f}:1 -- expected text-safe >=4.5 (from {style_lock_path})")
                print("", file=sys.stderr)
                print(f"[FAIL] Contrast regressions found in {style_lock_path}:", file=sys.stderr)
                for reg in regressions:
                    print(f"  FAIL  {reg['pair']}: {reg['ratio']:.2f}:1 -- expected text-safe >=4.5 (from {style_lock_path})", file=sys.stderr)
                sys.exit(1)
            else:
                print()
                print(f"[PASS] All declared text-safe pairings in {style_lock_path} still meet 4.5:1.")
            sys.exit(0)

    if not args:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    if args[0] == "--matrix":
        roles = parse_roles(args[1:])
        if len(roles) < 2:
            print("--matrix needs at least two role=hex colors.", file=sys.stderr)
            sys.exit(2 if json_mode else 1)
        structured, groups = _compute_matrix_data(roles)
        regressions = []
        if style_lock_path is not None:
            text_safe = parse_style_lock_text_safe(style_lock_path)
            regressions = compute_regressions(roles, text_safe)
        if json_mode:
            pairs_json = []
            for a, b, r, cls in structured:
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
                "groups": groups,
                "legal_pairings": groups,
                "pass": len(regressions) == 0,
                "passed": len(regressions) == 0,
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
            run_matrix(roles)
            if regressions:
                print()
                print("== Regression check (against style-lock) ==")
                for reg in regressions:
                    print(f"  FAIL  {reg['pair']}: {reg['ratio']:.2f}:1 -- expected text-safe >=4.5 (from {style_lock_path})")
                print("", file=sys.stderr)
                print(f"[FAIL] Contrast regressions found in {style_lock_path}:", file=sys.stderr)
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
            sys.exit(2 if json_mode else 1)

        checks = []

        def _check(label, hex1, hex2, floor, a_name=None, b_name=None):
            r = ratio(hex1, hex2)
            ok = r >= floor
            cls = _class_for(r)
            checks.append({
                "label": label, "a": a_name, "b": b_name,
                "hex1": f"#{hex1.lstrip('#')}", "hex2": f"#{hex2.lstrip('#')}",
                "ratio": round(r, 2), "floor": floor, "pass": ok, "passed": ok, "class": cls,
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
            _check("white label / primary fill", "ffffff", roles["primary"], AA_NORMAL, "white", "primary")
            _check(f"dark text ({roles['text']}) / primary fill", roles["text"], roles["primary"], AA_NORMAL, "text", "primary")
            if not json_mode and not (white_ok or dark_ok):
                print(f"  -> NEITHER white nor {roles['text']} text is readable on primary #{roles['primary']} -- darken/lighten primary, don't just pick a label color and hope.")
            all_pass &= (white_ok or dark_ok)
            p2 = _check("primary / background (visibility, UI-component floor)", roles["primary"], roles["bg"], AA_LARGE_OR_UI, "primary", "bg")
            all_pass &= p2

        if "accent" in roles:
            p3 = _check("accent / background (visibility + hyperlink-text floor)", roles["accent"], roles["bg"], AA_LARGE_OR_UI, "accent", "bg")
            all_pass &= p3

        if style_lock_path is not None:
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
                "pairs": checks,
                "pass": bool(all_pass and not regressions),
                "passed": bool(all_pass and not regressions),
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
                print(f"[FAIL] Contrast regressions found in {style_lock_path}:", file=sys.stderr)
                for reg in regressions:
                    print(f"  FAIL  {reg['pair']}: {reg['ratio']:.2f}:1 -- expected text-safe >=4.5 (from {style_lock_path})", file=sys.stderr)
            sys.exit(0 if all_pass and not regressions else 1)

    else:
        if len(args) != 2:
            print("Usage: check_contrast.py <hex1> <hex2>  OR  --palette role=hex ...  OR  --matrix role=hex ...", file=sys.stderr)
            if json_mode:
                print("       Add --json for machine-readable output, --check-lock/--style-lock PATH to gate regressions.", file=sys.stderr)
            sys.exit(2 if json_mode else 1)
        hex1, hex2 = args[0], args[1]
        r = ratio(hex1, hex2)
        ok = r >= AA_NORMAL
        cls = _class_for(r)
        all_pass = ok
        if style_lock_path is not None:
            regressions = []
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
                    "passed": ok,
                    "class": cls,
                }],
                "checks": [{
                    "label": "given pair",
                    "a": None, "b": None,
                    "hex1": f"#{hex1.lstrip('#')}",
                    "hex2": f"#{hex2.lstrip('#')}",
                    "ratio": round(r, 2),
                    "floor": AA_NORMAL,
                    "pass": ok,
                    "passed": ok,
                    "class": cls,
                }],
                "pass": bool(ok),
                "passed": bool(ok),
            }
            if style_lock_path is not None:
                out["regressions"] = regressions
                out["style_lock"] = style_lock_path
            print(json.dumps(out, indent=2))
            sys.exit(0 if ok else 1)
        else:
            report("given pair", hex1, hex2, AA_NORMAL)
            sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
