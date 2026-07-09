# Tastemaker

A Claude Code / Cursor / Windsurf skill for building UI that doesn't look AI-generated.

Ask an LLM to build a UI and you get the same handful of defaults every time: indigo-to-purple gradients, the same soft-shadow rounded card, a generic hero. That's not a prompting problem — it's what happens when a model has to invent visual taste from scratch, with no grounding and no memory of what you actually like.

Tastemaker fixes this with three ideas instead of a bigger catalog of presets:

1. **Ground in real pixels, not descriptions.** Give it reference images and it extracts real color/contrast tokens deterministically from the actual pixels (`scripts/extract_palette.py`) — not a text summary of the vibe, regenerated from that summary. Text-mediated style transfer is lossy; that's most of why AI UI looks generic even from a detailed prompt.
2. **Remember, don't re-derive.** Once a project's style is locked (`.tastemaker/style-lock.md`), every later screen/component reuses it instead of drifting. Across projects, a lightweight personal profile (`~/.tastemaker/profile.md`) carries forward what you keep vs. reject, so your second project starts warm instead of cold.
3. **Scope to what's actually being built.** Reads your PRD/spec first to figure out which screens/components need design work, instead of dumping a generic design system disconnected from the real product.

## Install

Drop the `tastemaker/` folder into your project's skills directory (or wherever your agent loads skills from — Claude Code, Cursor, and Windsurf all support this). Everything here runs locally; no hosted backend.

Requires Python 3 + Pillow for the deterministic color extraction script (`pip install Pillow`). Falls back gracefully to a vision-based read if Pillow isn't installed.

**Optional, for real photography**: register a free app at [unsplash.com/developers](https://unsplash.com/developers) and set `export UNSPLASH_ACCESS_KEY=your_key_here`. `scripts/fetch_unsplash.py` uses Unsplash's official API and handles the attribution + download-tracking their API Guidelines require — nothing extra to configure beyond the key.

**A deliberate non-feature**: this skill does not auto-fetch from unDraw. unDraw's license explicitly prohibits automated scraping/downloading of their assets (a prior third-party CDN for it was shut down over exactly this), so instead the workflow asks you to spend one minute at [undraw.co/illustrations](https://undraw.co/illustrations), use *their own* built-in recolor tool, and drop the SVGs into the project — everything after that is automatic.

## How it's different from "design system" skills

Most existing design skills for coding agents (e.g. curated style/palette libraries with search) give the model a bigger menu of canned presets to pick from. That's still generic — a library of options, not *your* taste, and it forgets everything once the session ends.

Tastemaker's actual differentiators:
- Reference images are the primary input, extracted deterministically, not just described in a prompt.
- Style, once established for a project, is locked and reused — no drift between screens generated in separate sessions.
- Personal taste persists and compounds across projects via a local profile file — the tool gets more accurate for a given developer the more they use it.
- Includes an asset-consistency step (one anchor asset, everything else conditioned on it) and an SVG validator (`scripts/validate_assets.py`) that catches malformed generated assets before they ship — a real bug class (illegal `--` inside SVG `<!-- -->` comments silently breaking rendering) this project found during its own testing.
- A curated style/pattern library (`references/`) exists as a fallback for cold starts with no references — but it's explicitly scaffolding to adapt, not a catalog to apply unchanged.

## Structure

```
tastemaker/
├── SKILL.md                          — the workflow, read this first
├── references/
│   ├── style-lock-format.md          — schema for .tastemaker/style-lock.md
│   ├── style-tokens.md               — starter palettes/type/shape by mood (cold-start fallback)
│   ├── component-patterns.md         — layout patterns by screen type
│   ├── anti-slop-checklist.md        — pre-delivery checks
│   ├── tech-stack-guides.md          — wiring tokens into React/Vue/SwiftUI/Flutter/plain CSS
│   └── animation-guidelines.md       — motion principles + how to use assets/reveal.*
├── scripts/
│   ├── extract_palette.py            — deterministic color/contrast extraction from images
│   ├── validate_assets.py            — SVG well-formedness validation
│   ├── fetch_unsplash.py             — real photography via Unsplash's official API
│   └── recolor_svg.py                — recolor local SVGs (already on disk) to the locked accent
└── assets/
    ├── reveal.css                    — scroll-reveal/stagger starter (prefers-reduced-motion aware)
    └── reveal.js                     — pairs with reveal.css, no dependencies
```

## License

MIT.
