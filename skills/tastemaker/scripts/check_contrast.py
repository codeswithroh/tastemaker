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

    # JSON output (stable, machine-readable) -- add --json to any mode
    python3 check_contrast.py --json 050315 fbfbfe
    python3 check_contrast.py --json --palette text=050315 bg=fbfbfe primary=2f27ce
    python3 check_contrast.py --json --matrix text=e6e6ea bg=0b0d12 primary=047857

    # style-lock regression check -- fails if a declared text-safe pairing drops below 4.5:1
    python3 check_contrast.py --check-lock .tastemaker/style-lock.md
    python3 check_contrast.py --json --check-lock .tastemaker/style-lock.md

JSON output (stable, documented):
    --json is additive and does not change the exit-code semantics.
    Without --json the script prints human-readable text exactly as before.

    Pair mode (--json <hex1> <hex2>):
        {"mode": "pair", "passed": true, "pair": {"label": "given pair", "color1": "050315",
         "color2": "fbfbfe", "ratio": 19.56, "floor": 4.5, "passed": true, "status": "PASS",
         "classification": "text-safe"}}

    Palette mode (--json --palette role=hex ...):
        {"mode": "palette", "passed": true, "roles": {"text": "050315", "bg": "fbfbfe"},
         "checks": [{"label": "body text / background", "color1": "050315", "color2": "fbfbfe",
         "ratio": 19.56, "floor": 4.5, "passed": true, "status": "PASS", "classification": "text-safe"}, ...]}

    Matrix mode (--json --matrix role=hex ...):
        {"mode": "matrix", "roles": {"text": "050315", ...},
         "pairs": [{"color1": "text", "color2": "bg", "hex1": "050315", "hex2": "fbfbfe",
         "ratio": 19.56, "class": "text-safe", "class_label": "text-safe (>=4.5)"}, ...],
         "legal_pairings": {"text_safe": ["text/bg"], "ui_safe": [], "decorative": []}}

    Check-lock mode (--json --check-lock <file>):
        {"mode": "check_lock", "file": ".tastemaker/style-lock.md", "passed": true,
         "roles": {"bg": "F4F1EB", ...}, "checks": [...], "violations": []}
        violations is a list of human-readable strings each naming the offending pair.

Exit code:
    --palette and single-pair exit nonzero if any checked pairing fails its floor.
    --matrix is a report and exits 0 (it does not know each pair's intended use, so it
    classifies rather than pass/fails).
    --check-lock exits 1 if any declared text-safe pairing drops below 4.5:1, or if the
    lock file cannot be parsed (fail-closed); 0 otherwise.
"""

import json
import os
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


def classify_ratio(r):
    if r >= AA_NORMAL:
        return "text-safe"
    if r >= AA_LARGE_OR_UI:
        return "ui-safe"
    return "decorative"


def report(label, hex1, hex2, floor=AA_NORMAL, as_json=False):
    r = ratio(hex1, hex2)
    passed = r >= floor
    status = "PASS" if passed else "FAIL"
    if not as_json:
        print(f"[{status}] {label}: {r:.2f}:1 (floor {floor}:1) — #{hex1.lstrip('#')} vs #{hex2.lstrip('#')}")
    return {
        "label": label,
        "color1": hex1.lstrip("#"),
        "color2": hex2.lstrip("#"),
        "ratio": round(r, 2),
        "floor": floor,
        "passed": passed,
        "status": status,
        "classification": classify_ratio(r),
    }


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
    pairs_raw = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            pairs_raw.append((a, b, ratio(roles[a], roles[b])))
    pairs_raw.sort(key=lambda p: -p[2])

    text_safe, ui_safe, decorative = [], [], []
    pair_details = []
    for a, b, r in pairs_raw:
        cls = classify_ratio(r)
        if cls == "text-safe":
            cls_label = "text-safe (>=4.5)"
            text_safe.append(f"{a}/{b}")
        elif cls == "ui-safe":
            cls_label = "UI-safe  (>=3.0)"
            ui_safe.append(f"{a}/{b}")
        else:
            cls_label = "decorative (<3.0)"
            decorative.append(f"{a}/{b}")
        pair_details.append({
            "color1": a,
            "color2": b,
            "hex1": roles[a],
            "hex2": roles[b],
            "ratio": round(r, 2),
            "class": cls,
            "class_label": cls_label,
        })

    if as_json:
        return {
            "mode": "matrix",
            "roles": roles,
            "pairs": pair_details,
            "legal_pairings": {
                "text_safe": text_safe,
                "ui_safe": ui_safe,
                "decorative": decorative,
            },
        }

    print(f"== Contrast matrix ({len(names)} roles, {len(pairs_raw)} pairs) ==")
    for p in pair_details:
        print(f"  {p['color1']:<12} x {p['color2']:<12} {p['ratio']:6.2f}  {p['class_label']}")

    print()
    print("== Legal pairings (record these in the style lock) ==")
    print(f"  Text-safe   (body text, links, button labels on a fill; >=4.5): {', '.join(text_safe) or 'none'}")
    print(f"  UI-safe     (large text, icons, and borders that convey state; >=3.0 and <4.5): {', '.join(ui_safe) or 'none'}")
    print(f"  Decorative  (below 3.0; fine as a subtle hairline, must NOT be the only thing conveying state): {', '.join(decorative) or 'none'}")
    return pair_details


def _parse_style_lock(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Style lock file not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    patterns = {
        "bg": r"Background:\s*#([0-9a-fA-F]{6})",
        "surface": r"Surface:\s*#([0-9a-fA-F]{6})",
        "dark": r"Dark surface:\s*#([0-9a-fA-F]{6})",
        "primary": r"Primary:\s*#([0-9a-fA-F]{6})",
        "accent": r"Accent:\s*#([0-9a-fA-F]{6})",
        "text": r"Text primary:\s*#([0-9a-fA-F]{6})",
        "muted": r"Text muted:\s*#([0-9a-fA-F]{6})",
        "on-dark": r"On-dark text:\s*#([0-9a-fA-F]{6})",
        "on-primary": r"Button label.*?:\s*#([0-9a-fA-F]{6})",
    }
    import re as _re
    roles = {}
    for key, pat in patterns.items():
        m = _re.search(pat, content)
        if m:
            roles[key] = m.group(1)
    declared = []
    m = _re.search(r"Text-safe\s*(?:\([^)]*\))?\s*:\s*(.+)", content, _re.IGNORECASE)
    if m:
        line = m.group(1).strip()
        for part in line.split(","):
            part = part.strip()
            if not part or part.lower() == "none":
                continue
            token = part.split()[0].strip()
            if "/" in token:
                declared.append(token)
    return roles, declared


def check_lock_file(file_path, as_json=False):
    roles, declared_text_safe = _parse_style_lock(file_path)
    if not roles.get("text") or not roles.get("bg"):
        raise ValueError(f"Style lock at {file_path} missing essential text/bg tokens; found {list(roles.keys())}")
    checks = []
    violations = []
    c = report("body text / background", roles["text"], roles["bg"], AA_NORMAL, as_json=as_json)
    checks.append(c)
    if not c["passed"]:
        violations.append(f"body text / background (text/bg) ratio {c['ratio']}:1 < 4.5 -- #{roles['text']} vs #{roles['bg']}")
    if "surface" in roles:
        c2 = report("body text / surface (text/surface)", roles["text"], roles["surface"], AA_NORMAL, as_json=as_json)
        checks.append(c2)
    if "primary" in roles:
        w = report("white label / primary fill", "ffffff", roles["primary"], AA_NORMAL, as_json=as_json)
        d = report(f"dark text ({roles['text']}) / primary fill", roles["text"], roles["primary"], AA_NORMAL, as_json=as_json)
        checks.extend([w, d])
        if not (w["passed"] or d["passed"]):
            violations.append(f"primary label contrast: neither white nor text #{roles['text']} >=4.5 on primary #{roles['primary']} (white {w['ratio']}:1, text {d['ratio']}:1)")
    for pair_str in declared_text_safe:
        parts = pair_str.split("/")
        if len(parts) != 2:
            continue
        a, b = parts[0].strip(), parts[1].strip()
        if a not in roles or b not in roles:
            violations.append(f"Declared text-safe pairing {pair_str} references unknown role (available: {', '.join(sorted(roles.keys()))})")
            continue
        cr = report(f"declared text-safe ({pair_str})", roles[a], roles[b], AA_NORMAL, as_json=as_json)
        checks.append(cr)
        if not cr["passed"]:
            violations.append(f"Declared text-safe pairing {pair_str} dropped below 4.5:1 (actual: {cr['ratio']}:1) -- #{roles[a]} vs #{roles[b]}")
    all_pass = len(violations) == 0
    result = {
        "mode": "check_lock",
        "file": file_path,
        "passed": all_pass,
        "roles": roles,
        "checks": checks,
        "violations": violations,
        "declared_text_safe": declared_text_safe,
    }
    return result, all_pass


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    as_json = False
    if "--json" in args:
        as_json = True
        args = [a for a in args if a != "--json"]
        if not args:
            print("Error: --json requires a mode (pair, --palette, --matrix, or --check-lock).", file=sys.stderr)
            sys.exit(1)

    if args[0] == "--check-lock":
        if len(args) < 2:
            print("Error: --check-lock requires a file path (e.g. .tastemaker/style-lock.md)", file=sys.stderr)
            sys.exit(1)
        file_path = args[1]
        try:
            res, all_pass = check_lock_file(file_path, as_json=as_json)
            if as_json:
                print(json.dumps(res, indent=2))
            else:
                if not all_pass:
                    print(f"[FAIL] Contrast regressions found in {file_path}:", file=sys.stderr)
                    for v in res["violations"]:
                        print(f"  - {v}", file=sys.stderr)
                else:
                    print(f"[PASS] All declared text-safe pairings in {file_path} still meet 4.5:1.")
            sys.exit(0 if all_pass else 1)
        except Exception as e:
            if as_json:
                print(json.dumps({"mode": "check_lock", "file": file_path, "passed": False, "error": str(e), "violations": [str(e)]}, indent=2))
            else:
                print(f"Error checking style lock: {e}", file=sys.stderr)
            sys.exit(1)

    if args[0] == "--matrix":
        roles = parse_roles(args[1:])
        if len(roles) < 2:
            print("--matrix needs at least two role=hex colors.", file=sys.stderr)
            sys.exit(1)
        res = run_matrix(roles, as_json=as_json)
        if as_json:
            print(json.dumps(res, indent=2))
        sys.exit(0)

    all_pass = True
    checks = []

    if args[0] == "--palette":
        roles = parse_roles(args[1:])

        missing = {"text", "bg"} - roles.keys()
        if missing:
            print(f"--palette requires at least text= and bg=; missing {missing}", file=sys.stderr)
            sys.exit(1)

        c1 = report("body text / background", roles["text"], roles["bg"], AA_NORMAL, as_json=as_json)
        checks.append(c1)
        all_pass &= c1["passed"]

        if "primary" in roles:
            white_ok = report("white label / primary fill", "ffffff", roles["primary"], AA_NORMAL, as_json=as_json)
            dark_ok = report(f"dark text ({roles['text']}) / primary fill", roles["text"], roles["primary"], AA_NORMAL, as_json=as_json)
            checks.extend([white_ok, dark_ok])
            if not (white_ok["passed"] or dark_ok["passed"]):
                if not as_json:
                    print(f"  -> NEITHER white nor {roles['text']} text is readable on primary #{roles['primary']} -- darken/lighten primary, don't just pick a label color and hope.")
            all_pass &= (white_ok["passed"] or dark_ok["passed"])
            c2 = report("primary / background (visibility, UI-component floor)", roles["primary"], roles["bg"], AA_LARGE_OR_UI, as_json=as_json)
            checks.append(c2)
            all_pass &= c2["passed"]

        if "accent" in roles:
            c3 = report("accent / background (visibility + hyperlink-text floor)", roles["accent"], roles["bg"], AA_LARGE_OR_UI, as_json=as_json)
            checks.append(c3)
            all_pass &= c3["passed"]

        if as_json:
            print(json.dumps({
                "mode": "palette",
                "passed": bool(all_pass),
                "roles": roles,
                "checks": checks,
            }, indent=2))

    else:
        if len(args) != 2:
            print("Usage: check_contrast.py [--json] <hex1> <hex2>  OR  [--json] --palette role=hex ...  OR  [--json] --matrix role=hex ...  OR  [--json] --check-lock <file>", file=sys.stderr)
            sys.exit(1)
        r = report("given pair", args[0], args[1], AA_NORMAL, as_json=as_json)
        all_pass = r["passed"]
        checks = [r]
        if as_json:
            print(json.dumps({
                "mode": "pair",
                "passed": bool(all_pass),
                "pair": r,
                "roles": {},
                "checks": checks,
            }, indent=2))

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
