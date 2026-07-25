#!/usr/bin/env python3
"""
Deterministic color extraction from reference images.

Why this exists: asking an LLM to "describe the colors in this image" and
regenerating from that description loses most of what makes a reference feel
specific. This script pulls real dominant colors, contrast ratios, and
lightness/saturation stats directly from the pixels, so the design brief is
anchored to something measured rather than paraphrased.

Usage:
    python3 extract_palette.py image1.png [image2.jpg ...]

Output: JSON to stdout. Degrades gracefully (prints a clear error to stderr
and exits nonzero) if Pillow isn't installed, so the skill can fall back to
a vision-based read instead of crashing silently.
"""

import sys
import json
import colorsys


def fail(msg):
    print(json.dumps({"error": msg}), file=sys.stderr)
    sys.exit(1)


try:
    from PIL import Image
except ImportError:
    fail(
        "Pillow not installed. Run `pip install Pillow`, or skip this script "
        "and do a visual (non-deterministic) read of the reference instead."
    )


def relative_luminance(r, g, b):
    def chan(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def contrast_ratio(rgb1, rgb2):
    l1 = relative_luminance(*rgb1) + 0.05
    l2 = relative_luminance(*rgb2) + 0.05
    return round(max(l1, l2) / min(l1, l2), 2)


def extract_dominant_colors(path, num_colors=6, sample_size=150):
    img = Image.open(path).convert("RGB")
    img.thumbnail((sample_size, sample_size))

    # Quantize with a wide adaptive palette, then read back the palette's
    # actual population-weighted colors. This is deterministic (no RNG),
    # unlike naive k-means with a random seed.
    quantized = img.quantize(colors=num_colors, method=Image.MEDIANCUT)
    palette = quantized.getpalette()
    color_counts = quantized.getcolors()  # [(count, palette_index), ...]
    color_counts.sort(reverse=True, key=lambda x: x[0])

    total_pixels = sum(c for c, _ in color_counts)
    results = []
    for count, idx in color_counts:
        r, g, b = palette[idx * 3 : idx * 3 + 3]
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        results.append(
            {
                "hex": "#{:02x}{:02x}{:02x}".format(r, g, b),
                "rgb": [r, g, b],
                "share": round(count / total_pixels, 3),
                "hue_deg": round(h * 360, 1),
                "saturation": round(s, 2),
                "value": round(v, 2),
            }
        )
    return results


def summarize_mood(colors):
    avg_sat = sum(c["saturation"] for c in colors) / len(colors)
    avg_val = sum(c["value"] for c in colors) / len(colors)
    notes = []
    notes.append("muted/desaturated" if avg_sat < 0.35 else ("vivid/saturated" if avg_sat > 0.65 else "moderately saturated"))
    notes.append("dark-leaning" if avg_val < 0.4 else ("light-leaning" if avg_val > 0.75 else "mid-tone"))
    return notes


def analyze_image(path):
    colors = extract_dominant_colors(path)
    lightest = max(colors, key=lambda c: c["value"])
    darkest = min(colors, key=lambda c: c["value"])
    return {
        "file": path,
        "dominant_colors": colors,
        "likely_background": lightest["hex"],
        "likely_foreground_text": darkest["hex"],
        "background_text_contrast_ratio": contrast_ratio(
            lightest["rgb"], darkest["rgb"]
        ),
        "wcag_aa_normal_text_pass": contrast_ratio(lightest["rgb"], darkest["rgb"]) >= 4.5,
        "mood_notes": summarize_mood(colors),
    }


def main():
    if len(sys.argv) < 2:
        fail("Usage: python3 extract_palette.py <image_path> [image_path ...]")

    results = []
    for path in sys.argv[1:]:
        try:
            results.append(analyze_image(path))
        except Exception as e:
            results.append({"file": path, "error": str(e)})

    print(json.dumps({"images": results}, indent=2))


if __name__ == "__main__":
    main()
