#!/usr/bin/env python3
"""
Generate a fresh, on-brand color palette that passes the contrast contract by
construction, instead of picking one of a handful of fixed presets.

Why this exists: a fixed set of presets means two similar prompts produce
near-identical output, which is just a new monoculture. This generates a new
palette every run: a base hue chosen within the mood's range, a color-harmony
rule (analogous / complementary / triadic / split / mono) for the accent, and
per-role lightness solved so the required WCAG pairings clear their floors.
The freshness comes from the hue and harmony; the safety comes from solving
lightness against a target ratio, the same idea Adobe Leonardo uses. Work is
done in OKLCH (perceptually uniform, predictable contrast), then gamut-mapped
to sRGB by reducing chroma until the color is displayable.

No dependencies. Reuses the WCAG math in check_contrast.py.

Usage:
    python3 generate_palette.py --mood technical
    python3 generate_palette.py --mood warm --mode light --seed 42
    python3 generate_palette.py --mood playful --mode dark

Moods: premium, warm, technical, playful, elegant (see the mood table in
references/style-tokens.md). --seed makes a run reproducible; omit it for a
new palette each time. Prints the roles as hex, a realtimecolors preview URL,
and the contrast matrix so the legal pairings can go straight into the lock.
"""

import sys
import math
import random
import argparse

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from check_contrast import ratio, run_matrix  # noqa: E402


# ---------- sRGB <-> OKLab <-> OKLCH ----------

def _srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def _linear_rgb_to_oklab(r, g, b):
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = l ** (1 / 3) if l > 0 else 0, m ** (1 / 3) if m > 0 else 0, s ** (1 / 3) if s > 0 else 0
    return (
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    )


def _oklab_to_linear_rgb(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (
        4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


def _in_gamut(lr, lg, lb):
    return all(-1e-4 <= c <= 1 + 1e-4 for c in (lr, lg, lb))


def oklch_to_hex(L, C, H):
    """OKLCH -> hex, gamut-mapped by reducing chroma until displayable."""
    hr = math.radians(H)
    c = C
    for _ in range(40):
        a, b = c * math.cos(hr), c * math.sin(hr)
        lr, lg, lb = _oklab_to_linear_rgb(L, a, b)
        if _in_gamut(lr, lg, lb):
            break
        c *= 0.92
    lr, lg, lb = (min(1.0, max(0.0, v)) for v in (lr, lg, lb))
    r, g, b = (round(_linear_to_srgb(v) * 255) for v in (lr, lg, lb))
    return f"{r:02x}{g:02x}{b:02x}"


# ---------- contrast-targeted lightness ----------

def _best_l(hue, chroma, bg, want, floor, prefer_l):
    """Scan OKLCH lightness for a color at (hue, chroma) whose contrast vs bg
    clears `floor` for the pairing described by `want`, choosing the candidate
    closest to prefer_l. `want` is a function(candidate_hex)->bool."""
    best = None
    L = 0.02
    while L <= 0.99:
        hx = oklch_to_hex(L, chroma, hue)
        if ratio(hx, bg) >= floor and want(hx):
            if best is None or abs(L - prefer_l) < abs(best[0] - prefer_l):
                best = (L, hx)
        L += 0.01
    return best


def solve_fill(hue, chroma, bg, text, prefer_l):
    """A solid fill (Primary/Accent-as-button): visible vs bg (>=3) and carrying
    a readable label (white or the text color, >=4.5). Reduce chroma if no
    lightness satisfies both."""
    c = chroma
    for _ in range(8):
        got = _best_l(
            hue, c, bg,
            want=lambda hx: max(ratio("ffffff", hx), ratio(text, hx)) >= 4.5,
            floor=3.0, prefer_l=prefer_l,
        )
        if got:
            _, hx = got
            label = "ffffff" if ratio("ffffff", hx) >= ratio(text, hx) else text
            return hx, label
        c *= 0.85
    # Fallback: give up on chroma, return a safe mid color
    hx = oklch_to_hex(prefer_l, 0.02, hue)
    return hx, ("ffffff" if ratio("ffffff", hx) >= ratio(text, hx) else text)


def solve_link(hue, chroma, bg, prefer_l):
    """Accent used as a link/highlight: aim for text-legible vs bg (>=4.5);
    accept the UI floor (>=3) if the hue can't reach 4.5 at a reasonable L."""
    c = chroma
    for target in (4.5, 3.0):
        for _ in range(6):
            got = _best_l(hue, c, bg, want=lambda hx: True, floor=target, prefer_l=prefer_l)
            if got:
                return got[1], target
            c *= 0.9
        c = chroma
    return oklch_to_hex(prefer_l, chroma * 0.5, hue), 3.0


# ---------- mood + harmony ----------

MOODS = {
    "premium":   {"hues": [(245, 285)], "chroma": (0.11, 0.17), "mode": "light"},
    "warm":      {"hues": [(20, 60)],   "chroma": (0.08, 0.14), "mode": "light"},
    "technical": {"hues": [(150, 200), (210, 255)], "chroma": (0.10, 0.15), "mode": "dark"},
    "playful":   {"hues": [(0, 360)],   "chroma": (0.15, 0.24), "mode": "light"},
    "elegant":   {"hues": [(20, 55), (70, 90)], "chroma": (0.05, 0.10), "mode": "light"},
}

HARMONIES = {
    "analogous":          lambda h: ((h + 32) % 360, (h - 32) % 360),
    "complementary":      lambda h: ((h + 180) % 360, (h + 150) % 360),
    "split-complementary": lambda h: ((h + 150) % 360, (h + 210) % 360),
    "triadic":            lambda h: ((h + 120) % 360, (h + 240) % 360),
    "monochromatic":      lambda h: (h, h),
}


def generate(mood, mode, rng):
    cfg = MOODS[mood]
    if mode is None:
        mode = cfg["mode"]
    dark = mode == "dark"

    lo, hi = rng.choice(cfg["hues"])
    base_h = rng.uniform(lo, hi)
    harmony = rng.choice(list(HARMONIES.keys()))
    accent_h, _ = HARMONIES[harmony](base_h)
    primary_chroma = rng.uniform(*cfg["chroma"])

    # Neutrals: a whisper of the base hue keeps the whole thing cohesive.
    neutral_c = 0.012
    bg_L = rng.uniform(0.14, 0.19) if dark else rng.uniform(0.975, 0.99)
    surface_L = bg_L + (0.05 if dark else -0.03)
    bg = oklch_to_hex(bg_L, neutral_c, base_h)
    surface = oklch_to_hex(surface_L, neutral_c, base_h)

    # Text: strong, comfortable contrast (aim well past the 4.5 floor).
    text_prefer = 0.96 if dark else 0.22
    text = _best_l(base_h, neutral_c * 1.5, bg, want=lambda hx: True, floor=8.0, prefer_l=text_prefer)
    text = text[1] if text else oklch_to_hex(text_prefer, neutral_c, base_h)

    primary_prefer = 0.62 if dark else 0.55
    primary, on_primary = solve_fill(base_h, primary_chroma, bg, text, primary_prefer)

    accent, accent_floor = solve_link(accent_h, primary_chroma, bg, 0.70 if dark else 0.58)

    # Secondary: a soft tint of the PRIMARY hue (not a third harmony hue) for
    # pills and secondary surfaces. Keeping it in the primary family is what
    # holds the palette together as "one family plus one accent pop," the
    # structure that reads as designed rather than as three competing colors.
    secondary = oklch_to_hex(0.30 if dark else 0.90, primary_chroma * 0.35, base_h)

    # Border: subtle separation, decorative by default.
    border = oklch_to_hex(bg_L + (0.10 if dark else -0.08), neutral_c, base_h)

    return {
        "mood": mood, "mode": mode, "harmony": harmony,
        "base_hue": round(base_h, 1), "accent_hue": round(accent_h, 1),
        "roles": {
            "text": text, "bg": bg, "surface": surface,
            "primary": primary, "on-primary": on_primary,
            "secondary": secondary, "accent": accent, "border": border,
        },
        "accent_floor": accent_floor,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mood", required=True, choices=list(MOODS.keys()))
    ap.add_argument("--mode", choices=["light", "dark"], default=None, help="Override the mood's default light/dark.")
    ap.add_argument("--seed", type=int, default=None, help="Reproducible run; omit for a fresh palette each time.")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    p = generate(args.mood, args.mode, rng)
    r = p["roles"]

    print(f"# Generated palette — {p['mood']} / {p['mode']} / {p['harmony']} harmony "
          f"(base hue {p['base_hue']}, accent hue {p['accent_hue']})")
    print()
    for name in ("text", "bg", "surface", "primary", "on-primary", "secondary", "accent", "border"):
        print(f"  {name:<11} #{r[name]}")
    print()
    order = "text-bg-primary-secondary-accent"
    vals = "-".join(r[k] for k in ("text", "bg", "primary", "secondary", "accent"))
    print(f"Preview: realtimecolors.com/?colors={vals}")
    print(f"  (accent is legible to a floor of {p['accent_floor']}:1 vs the background)")
    print()
    run_matrix({k: r[k] for k in ("text", "bg", "surface", "primary", "accent", "border", "on-primary")})


if __name__ == "__main__":
    main()
