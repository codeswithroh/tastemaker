---
name: ideagram
description: Turn a concept, feature description, blog post, or pitch into a single beautiful, on-brand illustration by matching it to a real unDraw illustration in a local library and recoloring it to the brand accent — genuine illustrator quality, not an AI-drawn approximation. Use whenever the user asks to "make an illustration," "create a graphic," "visualize this concept," "explain this visually," wants something "unDraw-style" or "Storyset-style," needs a hero/feature/blog illustration, or says an idea needs a picture. Trigger even if they don't name a style — "make something to explain X" or "I need a graphic for this tweet" both qualify.
---

# Ideagram

## The core idea

Produce **one** beautiful, on-brand illustration for a concept by matching it to a real unDraw illustration and recoloring it to the brand — never by hand-drawing. unDraw's figures are dozens of hand-placed bezier anchors from a professional illustrator; freehand-generating path coordinates produces crude pictograms, not art. The quality lives in the real path data, so this skill reuses it: match → recolor → (compose, if needed) → deliver. The output is genuinely illustrator-grade because it *is* the illustrator's work, just made on-brand.

Read `references/undraw-anatomy.md` once — it's the dissection of how these files are built and why this reuse approach works.

## Setup: a local unDraw library

This skill reads real unDraw SVGs from a **local library folder** — it does not bundle or redistribute unDraw's files (their license bars compiling their assets into a redistributed collection; downloading them for your own use is free and needs no attribution).

- Default library location: `~/.ideagram/undraw/`.
- Populate it by downloading illustrations from [undraw.co/illustrations](https://undraw.co/illustrations) (free, no attribution, unlimited) — 20-30 illustrations spanning common themes (teams, devices, data, growth, communication, security, travel) covers most requests well.
- After adding SVGs, (re)build the index: `python3 scripts/build_library_index.py`. This writes `index.md` (human-scannable) and `index.json` (machine-readable) into the library folder — read `index.md` first for matching instead of guessing from filenames cold.
- If **no library exists yet**, say so plainly and point the user at undraw.co (30 seconds to grab a few). Only fall back to the crude generated-primitive path (`references/style-contract.md`) if they genuinely can't, and be upfront that it's a large quality drop from real unDraw art.

## Workflow

### Step 1 — Distill the concept

Reduce the input to one sentence — "this is fundamentally about ___" — plus a few keywords. If the content genuinely holds two ideas, that's two illustrations, not one crowded brief.

### Step 2 — Match to the best illustration in the library

Read `~/.ideagram/undraw/index.md` (run `scripts/build_library_index.py` first if it doesn't exist or the library changed). Match the concept's keywords against each entry's keyword list — prefer a match on the *scene*, not just a loose word overlap: a dashboard/analytics concept wants an illustration with a screen or chart; a teamwork concept wants one with multiple figures. If several are close, pick the one whose scene most literally embodies the concept (see the worked example below). If nothing in the library is a real fit, say so and either ask the user to grab a closer one from undraw.co or fall back (Step 5) — don't force a bad match.

**Worked example:** "an AI creative director composing a whole design system from one prompt" → not literally "AI" or "design system" in any filename, but `mobile-site-builder` (a person actively laying out screen components) is the closest *scene* match — the visual metaphor matters more than exact keyword overlap.

### Step 3 — Recolor to the brand

```
python3 scripts/recolor_undraw.py <matched>.svg --accent "#<brand-hex>" --out design/<name>.svg
```

This swaps only unDraw's `#6c63ff` accent family for the brand color, leaving every skin tone, hair, clothing, and neutral exactly as drawn — verified on real multi-figure scenes. Check the matched illustration's `index.md` row for a flagged secondary accent (green/pink); if present and it should also change, add `--also "#8ed16f:#<hex>"`. If the user gives no brand color, unDraw's default purple is a fine, deliberate choice — don't invent one.

**If you need to redo a color** (the user asks for a different one), re-copy the *original* unDraw source into the output path first, then recolor — `recolor_undraw.py` only remaps `#6c63ff` outward, so recoloring an already-recolored file does nothing (the purple it looks for is gone). Never edit a previously-branded file's colors by hand to "fix" this.

### Step 4 — (Optional) Compose a custom scene from real components

Only when no single library illustration fits and a custom scene is worth the extra effort:

- List a source's components with `scripts/extract_component.py source.svg --list`, then lift one with `--match "translate(...)" --out part.svg`.
- Assemble whole components into one `<svg>` as a real **scene** — a background element, the concept's midground device, then the figure interacting with it, plus a ground shadow — not a floating figure. This is what separates a designed illustration from a subject stranded on white.
- Place each with `<g transform="translate() scale()">`; render and read `getBBox()` to size/position accurately rather than guessing coordinates from nested transforms.
- Reuse *whole* components. Recombining sub-limbs (an arm from one figure onto another's torso) is fragile — different coordinate spaces and shading directions rarely join cleanly.
- Recolor the finished composition (Step 3).

### Step 5 — Fallback only if there's no usable library

If the user genuinely has no unDraw library and won't create one, `references/style-contract.md` + `assets/primitives/` still exist — but they produce simple flat pictograms, not illustrator-grade art. Use only as a last resort, and say plainly that a couple of real unDraw SVGs would look dramatically better for the same effort.

### Step 6 — Validate and deliver

- `python3 scripts/validate_assets.py <final>.svg` — catches malformed SVG (e.g. a `--` inside a comment) that renders as a broken image in strict browsers, invisible unless actually parsed.
- Deliver the SVG directly for web use — smallest, crispest, infinitely recolorable. For social/raster: `scripts/export_png.py <final>.svg --out design/export/` (needs `cairosvg` + system cairo; degrades honestly if either is missing, and the SVG stays fully usable regardless).

## Reference files

| File | Read when |
|---|---|
| `references/undraw-anatomy.md` | Always, first — the palette, structure, and the reuse technique this skill is built on |
| `~/.ideagram/undraw/index.md` | Step 2 — matching a concept to the right illustration |
| `references/style-contract.md`, `references/metaphor-library.md` | Only for the Step 5 fallback (no library, generated primitives) |

## Scripts

| Script | Purpose |
|---|---|
| `scripts/build_library_index.py` | Index a local unDraw library into `index.md`/`index.json` for fast, accurate matching. Run after adding new SVGs. |
| `scripts/recolor_undraw.py` | Recolor a real unDraw illustration's accent to a brand color, preserving skin/ink/clothing/neutrals. The workhorse. |
| `scripts/extract_component.py` | Lift a whole figure/device/panel out of a source unDraw SVG for composing a new scene. |
| `scripts/validate_assets.py` | Verify the finished SVG is well-formed before delivering. |
| `scripts/export_png.py` | Export flattened PNGs at standard social/presentation sizes (needs cairosvg + system cairo). |

## Honesty

Say what actually happened: which illustration was matched and why, whether it was recolored, and if you fell back to generated primitives because there was no library, say that plainly and note the quality gap rather than presenting it as equal. Respect the sourcing model — reuse real unDraw art from the user's local library for their own sites; never redistribute unDraw's files into a public repo.

## A note on image generation

An alternative, higher-ceiling approach exists — *generating* an original illustration with an image model, steered by a rigorous style system (`references/style-dna.md`, `composition-patterns.md`, `prompt-template.md`, `qa-checklist.md`) — for the rare case a session has a genuine image-generation tool available and the library has no good match. Most Claude sessions don't have one, so this isn't part of the default workflow above; only reach for it if such a tool is actually present, and say so.
