# Ideagram

A Claude Code / Cursor / Windsurf skill that turns a concept, feature description, or pitch into **one beautiful, on-brand illustration** — by matching it to a real unDraw illustration and recoloring it to your brand. Genuine illustrator quality, not an AI-drawn approximation.

## The idea in one paragraph

An LLM cannot hand-draw illustration at unDraw's quality — those figures are dozens of hand-placed bezier anchors from a professional illustrator, and generating path coordinates blind produces crude pictograms, not art. The quality lives in the real path data. So this skill doesn't draw: it **matches** a concept to the right real unDraw illustration, **recolors** only its purple accent to your brand (skin, hair, and clothing stay exactly as drawn), and **composes** whole real components into a new scene on the rare occasion nothing in the library fits. The output is genuinely illustrator-grade because it *is* the illustrator's work — just made yours.

## Quick start

```bash
# 1. Grab a handful of illustrations covering common themes
#    (undraw.co/illustrations — free, no attribution, unlimited)
mkdir -p ~/.ideagram/undraw
#    ...download a few dozen .svg files into that folder...

# 2. Build the match index
python3 scripts/build_library_index.py

# 3. Ask for an illustration (in Claude Code: /ideagram <your brief>)
#    It matches a library illustration to your concept and asks for
#    (or infers) a brand accent to recolor it to.
```

A library of 20–30 illustrations spanning teams, devices, data, growth, communication, security, and travel covers most requests well. Add more over time; re-run the indexer whenever you do.

## How it works

1. **Distill** the brief to one concept.
2. **Match** it against `~/.ideagram/undraw/index.md` — a keyword index built from the library's filenames (unDraw's only real per-file metadata), matched on *scene*, not just literal word overlap.
3. **Recolor** the match's accent to your brand with `scripts/recolor_undraw.py` — swaps only unDraw's `#6c63ff` family, verified to leave every skin tone and garment untouched.
4. **Compose** (rarely needed) — lift whole real components with `scripts/extract_component.py` and assemble a new scene when no single illustration fits.
5. **Validate and deliver** — `scripts/validate_assets.py` catches malformed SVG before it ships; `scripts/export_png.py` flattens to PNG for platforms that need raster.

See `SKILL.md` for the full step-by-step workflow.

## Sourcing and licensing

unDraw illustrations are free to use commercially with no attribution — but their license bars *compiling their assets into a redistributed collection*. So this skill **does not bundle unDraw's files**. It reads them from a local library you maintain (`~/.ideagram/undraw/` by default), populated by downloading from [undraw.co/illustrations](https://undraw.co/illustrations) yourself. You get full unDraw quality on your own sites; this public repo stays clean of redistributed art — its `.gitignore` blocks `undraw_*.svg` as a guardrail.

## Install

Drop the `ideagram/` folder into your skills directory. Requires Python 3 only — no keys, no accounts, no hosted service. Optional PNG export needs `cairosvg` + the system cairo library (the export script tells you exactly what's missing if either isn't installed).

## Structure

```
ideagram/
├── SKILL.md                          — the workflow, read first
├── references/
│   ├── undraw-anatomy.md             — dissection of real unDraw files: palette, structure, the reuse technique
│   ├── style-contract.md             — fallback only (generated primitives, no library)
│   └── metaphor-library.md           — fallback only
├── scripts/
│   ├── build_library_index.py        — index a local unDraw library for fast, accurate matching
│   ├── recolor_undraw.py             — recolor a real unDraw illustration's accent to a brand color (the workhorse)
│   ├── extract_component.py          — lift a whole figure/device/panel out for composing a new scene
│   ├── validate_assets.py            — SVG well-formedness check
│   └── export_png.py                 — flatten to PNG at standard sizes
└── assets/primitives/                — generated-primitive kit, kept only as a last-resort fallback
```

## What this is, honestly

At its best — recoloring a real unDraw illustration to your brand — the output is indistinguishable from unDraw, because it is unDraw. That's the whole point, and it's a night-and-day improvement over hand-drawn primitives. The fallback path (generating from geometric primitives when there's no library) produces simple pictograms and is clearly labeled as such whenever it's used. This skill's value is matching, recoloring, and composing real art reliably — not out-drawing a human illustrator.

## License

MIT for the skill code, scripts, and docs (all original). Does not include or redistribute unDraw's illustrations — those you download yourself, free, from undraw.co.
