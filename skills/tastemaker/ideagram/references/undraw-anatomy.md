# unDraw anatomy — how the real illustrations are built, and how to reuse them

This is the result of dissecting real unDraw SVGs. The headline finding: **you cannot hand-author illustration at this quality, and you don't need to.** Every unDraw figure is dozens of hand-placed bezier anchors drawn in Illustrator by a professional (Katerina Limpitsouni) — freehand-generating those coordinates produces pictograms, not illustration. The quality is *in the path data*. So the skill's job is to **reuse the real path data** — recolor whole illustrations to a brand, and compose whole real components into new scenes — not to redraw.

## The real palette

Extracted by frequency across a corpus of unDraw SVGs:

| Hex | Role |
|---|---|
| `#090814` | Near-black ink — outlines, hair, trousers, the dominant "dark" |
| `#6c63ff` | **The accent** — the one purple that defines each illustration's "pop" (screens, logos, highlights). This is the ONLY color you swap for a brand. |
| `#e6e6e6` | Light grey — shirts, background panels, the ground-shadow ellipse |
| `#ed9da0` | Skin (also `#9f616a`, `#a0616a`, `#ffb6b6`, `#fbbebe`, `#e8989b` — unDraw uses several skin tones) |
| `#3f3d56` / `#3f3d58` / `#2f2e41` | Dark clothing / hair variants |
| `#d6d6e3` | Light lavender-grey — subtle shading |
| `#8ed16f`, `#ff6584` | Occasional secondary accents (green, pink) |

**Shading technique:** unDraw layers semi-transparent black (`opacity="0.05"`–`0.2"`) over a base fill to create shadow tones, rather than defining a separate darker hex. That's why the shading looks cohesive.

## How a figure is structured

A figure is one `<g transform="translate(x y)">` group. Inside, in rough back-to-front order: back limbs → trousers/legs (`#090814`) → torso/jacket (`#3f3d56`) → shirt (`#e6e6e6` or the `#6c63ff` accent) → arms + hands (skin) → neck → head (a skin `circle`) → hair (one intricate `#090814` bezier path over the head). The hair and hands are the most detailed paths — and the hardest to fake, which is exactly why you reuse them rather than draw them.

## A whole illustration is a SCENE, not a floating figure

This is the biggest thing the old primitive approach got wrong. A real unDraw illustration is layered:
1. **Background** — a large light panel, a big screen, a window, or an abstract shape (`#e6e6e6` / faint accent), often the biggest element.
2. **Midground** — the device/object the scene is about (a phone, monitor, chart), carrying the accent.
3. **Figure(s)** — often *smaller* than you'd expect, positioned relative to the background element, interacting with it.
4. **Decorative bits** — a plant, floating dots, small shapes, a ground shadow.

A figure alone on white reads as unfinished. The background + midground are what make it a designed illustration. When composing, always build the scene, not just the person.

## The two reliable operations (and one fragile one)

**Reliable — recolor a whole illustration to a brand.** Use `scripts/recolor_undraw.py --accent "#hex"`. It swaps only the `#6c63ff` accent family, leaving skin/ink/greys/clothing exactly as drawn. Verified on real multi-figure scenes: perfect. This alone delivers unDraw-quality, on-brand illustration with zero drawing.

**Reliable — transplant a whole component into a new scene.** A whole figure group, or a whole background/device group, lifts cleanly:
1. Find the component's `<g transform="translate(...)">` in the source.
2. Extract it with brace-matching (`<g>`…`</g>` depth counting), keeping any parent `transform` that positions it.
3. Drop it into a fresh `<svg>`, wrapping in a `<g transform="translate()/scale()">` to place and size it. Measure the real bounds with the browser's `getBBox()` on the group rather than guessing the viewBox — nested transforms make eyeballing wrong.
4. Recolor to brand.

**Fragile — recombining sub-parts** (grafting an arm from figure A onto torso B). Each sub-part is drawn in its own coordinate space, angle, and shading direction, so they don't cleanly connect and it looks like a Frankenstein. Avoid unless you're prepared to hand-fix the join. Reuse whole figures instead.

## Why this beats the old "draw from primitives" approach

The old approach hand-built figures from circles + capsules + two colors → pictograms with no finesse, no scene, no depth. This approach reuses the actual illustrator's vector work → genuine unDraw quality, because it *is* unDraw. The skill's value moves from "drawing" (which it's bad at) to "matching + recoloring + composing" (which it's reliable at).
