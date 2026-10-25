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
    python3 check_contrast.py --palette text=050315 bg=fbfbfe primary=2f27ce \\
        secondary=dedcff accent=433bff

    # the full pairing matrix: every color pair, classified by which floor it
    # clears, plus a legal-pairings summary to record in the style lock.
    # Include a label color (e.g. on-primary=ffffff) to see button-label legality.
    python3 check_contrast.py --matrix text=e6e6ea bg=0b0d12 surface=161a21 \\
        primary=047857 accent=34d399 border=232a33 on-primary=ffffff

    # machine-readable output: --json works in all three modes and replaces
    # the human-readable text on stdout (diagnostics still go to stderr).
    # The JSON is deterministic: same inputs always produce the same bytes,
    # so a downstream tool can diff it or fail CI on it.
    python3 check_contrast.py --json 050315 fbfbfe
    python3 check_contrast.py --palette --json text=050315 bg=fbfbfe
    python3 check_contrast.py --matrix --json text=e6e6ea bg=0b0d12

JSON shapes (ratios rounded to two decimals, pairs sorted by ratio desc):
    pair:    {"mode": "pair", "checks": [{"label", "color1", "color2",
               "ratio", "floor", "pass"}], "pass": bool}
    palette: {"mode": "palette", "checks": [...same check objects...],
               "note": str (only when neither label color is readable on
               primary), "pass": bool}
    matrix:  {"mode": "matrix", "roles": {"role": "#hex", ...},
               "pairs": [{"color1", "color2", "ratio",
               "class": "text-safe" | "ui-safe" | "decorative"}],
               "legal_pairings": {"text_safe": ["a/b", ...],
               "ui_safe": [...], "decorative": [...]}}
    lock:    matrix shape plus "lock": path and "gate": {"checked":
               ["a/b", ...recorded text-safe pairings...],
               "offenders": [{"pair", "ratio" | null, "reason"}],
               "pass": bool}

Style-lock regression gate:
    A palette change that lowers a pairing the style lock records as
    text-safe below 4.5:1 must fail CI, with the offending pair named.
    --lock PATH (with --matrix) and --from-lock PATH both read the lock's
    Palette section and its "Text-safe" contract list, recompute every
    recorded text-safe pairing against the current palette, and exit
    nonzero naming each offender (a recorded pair whose roles are missing
    from the palette counts as an offender too — removing a color a
    text-safe pairing depends on is a regression, not a silent pass).

    --from-lock reads the palette itself from the lock, so the CI action
    needs no hand-maintained role list:
        python3 check_contrast.py --from-lock .tastemaker/style-lock.md

    Lock parsing rules (documented because the lock is prose, not config):
    - Palette section: lines "- Name: #RRGGBB (...)" under "## Palette".
      Names map to roles: Background->bg, Surface->surface,
      Dark surface->dark, Primary->primary, Accent->accent,
      Text primary->text, Text muted->muted, On-dark text->on-dark,
      Button label color->on-primary. Non-hex entries (e.g. rgba borders)
      are skipped; any other hex entry keeps a slugified name.
    - Contract section: lines "- Text-safe (>=4.5): a/b (r), c/d (r), ..."
      under "## Color contract". Only the pair names are used; the
      recorded ratios are recomputed, never trusted.

Exit code: --palette and single-pair exit nonzero if any checked pairing fails
its floor. --matrix is a report and exits 0 (it does not know each pair's
intended use, so it classifies rather than pass/fails) — unless --lock is
given, in which case it exits nonzero on gate offenders. --from-lock exits
nonzero on gate offenders.
"""

import json
import re
import sys

AA_NORMAL = 4.5        # body text on its background
AA_LARGE_OR_UI = 3.0   # large text, UI components, graphical objects (WCAG 1.4.11)

# Human palette names in .tastemaker/style-lock.md -> short role names used
# by the contract's pair lists (and by --matrix/--palette callers).
LOCK_ROLE_MAP = {
    "background": "bg",
    "surface": "surface",
    "dark surface": "dark",
    "primary": "primary",
    "accent": "accent",
    "text primary": "text",
    "text muted": "muted",
    "on-dark text": "on-dark",
    "button label color": "on-primary",
}


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


def _class_of(r):
    if r >= AA_NORMAL:
        return "text-safe"
    if r >= AA_LARGE_OR_UI:
        return "ui-safe"
    return "decorative"


def check_pair(label, hex1, hex2, floor=AA_NORMAL):
    """One contrast check as data; report() is the text rendering of it."""
    r = ratio(hex1, hex2)
    return {
        "label": label,
        "color1": "#" + hex1.lstrip("#"),
        "color2": "#" + hex2.lstrip("#"),
        "ratio": round(r, 2),
        "floor": floor,
        "pass": r >= floor,
    }


def report(label, hex1, hex2, floor=AA_NORMAL):
    c = check_pair(label, hex1, hex2, floor)
    status = "PASS" if c["pass"] else "FAIL"
    print(f"[{status}] {label}: {c['ratio']:.2f}:1 (floor {floor}:1) — #{hex1.lstrip('#')} vs #{hex2.lstrip('#')}")
    return c["pass"]


def parse_roles(args):
    roles = {}
    for kv in args:
        if "=" not in kv:
            print(f"Bad argument (expected role=hex): {kv}", file=sys.stderr)
            sys.exit(1)
        k, v = kv.split("=", 1)
        roles[k] = v.lstrip("#")
    return roles


def compute_matrix(roles):
    """All unordered pairs, sorted by ratio desc, plus grouped legal pairings."""
    names = list(roles.keys())
    pairs = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            r = ratio(roles[a], roles[b])
            pairs.append({"color1": a, "color2": b, "ratio": round(r, 2), "class": _class_of(r)})
    pairs.sort(key=lambda p: -p["ratio"])
    groups = {"text_safe": [], "ui_safe": [], "decorative": []}
    for p in pairs:
        groups[p["class"].replace("-", "_")].append(f"{p['color1']}/{p['color2']}")
    return pairs, groups


def run_matrix(roles, json_mode=False):
    pairs, groups = compute_matrix(roles)
    if json_mode:
        print(json.dumps({
            "mode": "matrix",
            "roles": {k: "#" + v for k, v in roles.items()},
            "pairs": pairs,
            "legal_pairings": groups,
        }, indent=2, sort_keys=False))
        return pairs, groups
    print(f"== Contrast matrix ({len(roles)} roles, {len(pairs)} pairs) ==")
    for p in pairs:
        cls = {"text-safe": "text-safe (>=4.5)", "ui-safe": "UI-safe  (>=3.0)",
               "decorative": "decorative (<3.0)"}[p["class"]]
        print(f"  {p['color1']:<12} x {p['color2']:<12} {p['ratio']:6.2f}  {cls}")

    print()
    print("== Legal pairings (record these in the style lock) ==")
    print(f"  Text-safe   (body text, links, button labels on a fill; >=4.5): {', '.join(groups['text_safe']) or 'none'}")
    print(f"  UI-safe     (large text, icons, and borders that convey state; >=3.0 and <4.5): {', '.join(groups['ui_safe']) or 'none'}")
    print(f"  Decorative  (below 3.0; fine as a subtle hairline, must NOT be the only thing conveying state): {', '.join(groups['decorative']) or 'none'}")
    return pairs, groups


def _slug(name):
    return re.sub(r"\s+", "-", name.strip().lower())


def parse_lock(path):
    """Return (roles, contract) from a style-lock markdown file.

    roles: short role name -> hex (no '#'). contract: class key ->
    list of "a/b" pair names. Raises FileNotFoundError / ValueError
    with a human-readable message on a missing or unusable lock.
    """
    try:
        with open(path) as f:
            text = f.read()
    except OSError as e:
        raise ValueError(f"cannot read style lock {path!r}: {e.strerror}") from e
    roles = {}
    in_palette = False
    for line in text.splitlines():
        if line.startswith("## Palette"):
            in_palette = True
            continue
        if in_palette and line.startswith("## "):
            break
        if in_palette:
            m = re.match(r"-\s+(.+?):\s+#([0-9a-fA-F]{6})\b", line)
            if m:
                role = LOCK_ROLE_MAP.get(m.group(1).strip().lower(), _slug(m.group(1)))
                roles[role] = m.group(2).lower()
    if len(roles) < 2:
        raise ValueError(f"no usable palette found in style lock {path!r} "
                         "(expected '- Name: #RRGGBB' lines under '## Palette')")
    contract = {"text_safe": [], "ui_safe": [], "decorative": []}
    key_of = {"Text-safe": "text_safe", "UI-safe": "ui_safe", "Decorative": "decorative"}
    for line in text.splitlines():
        m = re.match(r"-\s+(Text-safe|UI-safe|Decorative)\s+\(", line)
        if m and ":" in line:
            for entry in line.split(":", 1)[1].split(","):
                pm = re.match(r"\s*([A-Za-z0-9_-]+)/([A-Za-z0-9_-]+)", entry)
                if pm:
                    contract[key_of[m.group(1)]].append(f"{pm.group(1)}/{pm.group(2)}")
    return roles, contract


def check_lock_gate(roles, contract):
    """Recorded text-safe pairings recomputed against the current palette.

    Returns a list of offenders: {"pair", "ratio" (null when a role is
    missing from the palette), "reason"}. Empty list means the gate passes.
    """
    offenders = []
    for pair in contract["text_safe"]:
        a, b = pair.split("/")
        if a not in roles or b not in roles:
            offenders.append({"pair": pair, "ratio": None,
                              "reason": "role missing from palette"})
        else:
            r = ratio(roles[a], roles[b])
            if r < AA_NORMAL:
                offenders.append({"pair": pair, "ratio": round(r, 2),
                                  "reason": "below 4.5:1"})
    return offenders


def print_gate(offenders, checked):
    print()
    print("== Style-lock gate (recorded text-safe pairings must stay >=4.5) ==")
    if not offenders:
        print(f"  OK: all {len(checked)} recorded text-safe pairings still clear 4.5:1.")
        return
    for o in offenders:
        if o["ratio"] is None:
            print(f"  FAIL {o['pair']}: {o['reason']}")
        else:
            print(f"  FAIL {o['pair']}: {o['ratio']:.2f}:1 ({o['reason']})")
    print(f"  {len(offenders)} recorded text-safe pairing(s) regressed below 4.5:1.")


def run_palette_checks(roles):
    """The --palette checks as data, in the same order as the text report."""
    checks = []
    checks.append(check_pair("body text / background", roles["text"], roles["bg"], AA_NORMAL))
    note = None
    if "primary" in roles:
        white = check_pair("white label / primary fill", "ffffff", roles["primary"], AA_NORMAL)
        dark = check_pair(f"dark text ({roles['text']}) / primary fill", roles["text"], roles["primary"], AA_NORMAL)
        checks.extend([white, dark])
        if not (white["pass"] or dark["pass"]):
            note = (f"NEITHER white nor {roles['text']} text is readable on primary "
                    f"#{roles['primary']} — darken/lighten primary, don't just pick "
                    "a label color and hope.")
        checks.append(check_pair("primary / background (visibility, UI-component floor)",
                                 roles["primary"], roles["bg"], AA_LARGE_OR_UI))
    if "accent" in roles:
        checks.append(check_pair("accent / background (visibility + hyperlink-text floor)",
                                 roles["accent"], roles["bg"], AA_LARGE_OR_UI))
    return checks, note


def main():
    raw = sys.argv[1:]
    json_mode = "--json" in raw
    args = [a for a in raw if a != "--json"]
    if not args:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    if args[0] == "--from-lock":
        if len(args) != 2:
            print("Usage: check_contrast.py --from-lock <style-lock.md>", file=sys.stderr)
            sys.exit(1)
        lock_path = args[1]
        try:
            roles, contract = parse_lock(lock_path)
        except ValueError as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)
        offenders = check_lock_gate(roles, contract)
        if json_mode:
            pairs, groups = compute_matrix(roles)
            print(json.dumps({
                "mode": "lock",
                "lock": lock_path,
                "roles": {k: "#" + v for k, v in roles.items()},
                "pairs": pairs,
                "legal_pairings": groups,
                "gate": {"checked": contract["text_safe"], "offenders": offenders,
                         "pass": not offenders},
            }, indent=2))
        else:
            run_matrix(roles)
            print_gate(offenders, contract["text_safe"])
        sys.exit(0 if not offenders else 1)

    if args[0] == "--matrix":
        rest = args[1:]
        lock_path = None
        if "--lock" in rest:
            i = rest.index("--lock")
            if i + 1 >= len(rest):
                print("Usage: check_contrast.py --matrix [--lock <style-lock.md>] role=hex ...",
                      file=sys.stderr)
                sys.exit(1)
            lock_path = rest[i + 1]
            rest = rest[:i] + rest[i + 2:]
        roles = parse_roles(rest)
        if len(roles) < 2:
            print("--matrix needs at least two role=hex colors.", file=sys.stderr)
            sys.exit(1)
        if lock_path is None:
            run_matrix(roles, json_mode)
            sys.exit(0)
        try:
            _, contract = parse_lock(lock_path)
        except ValueError as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)
        offenders = check_lock_gate(roles, contract)
        if json_mode:
            pairs, groups = compute_matrix(roles)
            print(json.dumps({
                "mode": "matrix",
                "roles": {k: "#" + v for k, v in roles.items()},
                "pairs": pairs,
                "legal_pairings": groups,
                "gate": {"checked": contract["text_safe"], "offenders": offenders,
                         "pass": not offenders},
            }, indent=2))
        else:
            run_matrix(roles)
            print_gate(offenders, contract["text_safe"])
        sys.exit(0 if not offenders else 1)

    if args[0] == "--palette":
        roles = parse_roles(args[1:])
        missing = {"text", "bg"} - roles.keys()
        if missing:
            print(f"--palette requires at least text= and bg=; missing {missing}", file=sys.stderr)
            sys.exit(1)
        checks, note = run_palette_checks(roles)
        # Primary's label readability is an either/or: the palette passes
        # if at least one of white/dark text reads on the primary fill.
        if "primary" in roles:
            white_ok = checks[1]["pass"]
            dark_ok = checks[2]["pass"]
            label_ok = white_ok or dark_ok
            all_pass = checks[0]["pass"] and label_ok and all(c["pass"] for c in checks[3:])
        else:
            all_pass = all(c["pass"] for c in checks)
        if json_mode:
            out = {"mode": "palette", "checks": checks, "pass": all_pass}
            if note:
                out["note"] = note
            print(json.dumps(out, indent=2))
        else:
            for c in checks:
                status = "PASS" if c["pass"] else "FAIL"
                print(f"[{status}] {c['label']}: {c['ratio']:.2f}:1 (floor {c['floor']}:1) — {c['color1']} vs {c['color2']}")
            if note:
                print(f"  -> {note}")
        sys.exit(0 if all_pass else 1)

    if len(args) != 2:
        print("Usage: check_contrast.py <hex1> <hex2>  OR  --palette role=hex ...  OR  --matrix role=hex ...", file=sys.stderr)
        sys.exit(1)
    check = check_pair("given pair", args[0], args[1], AA_NORMAL)
    if json_mode:
        print(json.dumps({"mode": "pair", "checks": [check], "pass": check["pass"]}, indent=2))
    else:
        report("given pair", args[0], args[1], AA_NORMAL)
    sys.exit(0 if check["pass"] else 1)


if __name__ == "__main__":
    main()
