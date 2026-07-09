---
name: tastemaker
description: Generate genuinely beautiful, on-brand UI instead of generic "AI slop" — use whenever the user asks to build, design, style, or improve a UI, landing page, dashboard, app screen, or component, whenever a PRD/spec needs a design pass before implementation, whenever the user pastes reference images/Pinterest/Dribbble links and wants the app to look like them, or whenever the user complains the AI-generated UI looks generic, boring, cookie-cutter, or "like every other AI app." Make sure to trigger this even if the user doesn't say "design" explicitly — phrases like "make this look good", "build the frontend for X", "this looks like every other SaaS site", or "match this vibe" all qualify.
---

# Tastemaker

## The problem this solves

Ask an LLM to build a UI and it defaults to the same handful of patterns: indigo-to-purple gradients, the same rounded card with a soft shadow, the same generic hero layout. This isn't a prompting failure — it's what happens when a model has to invent visual taste from scratch, from a text description, with no grounding and no memory of what the person asking actually likes.

Most "design skill" approaches try to fix this by handing the model a bigger catalog of canned styles and palettes to pick from. That helps a little, but it's still generic — a library of presets, not *your* taste, and it forgets everything the moment the session ends.

Tastemaker works differently, on three ideas:

1. **Ground in real pixels, not descriptions.** If the user gives you references (images, screenshots, URLs), extract tokens from the actual reference — deterministically, with a script — instead of writing a text summary of the vibe and generating from that summary. Text-mediated style transfer is lossy; that's most of why AI UI looks generic even when the prompt describes something specific.
2. **Remember, don't re-derive.** Once a project's style is established, lock it and reuse it for every subsequent screen or component in that project. Across projects, keep a lightweight personal profile of what this specific developer keeps vs. rejects, so returning users start warm instead of from zero.
3. **Scope to what's actually being built.** If a PRD or spec exists, use it to figure out exactly which screens/components need design work, and target effort there — not a generic "here's a design system" dump disconnected from the real product.

Read this file top to bottom before starting. It's short by design; the reference files below hold the deep material and are only worth opening when the step calls for them.

## Workflow

### Step 0 — Load memory, don't start cold

Check for `.tastemaker/style-lock.md` in the project root first.

- **Exists** → this project already has an established style. Read it and reuse those exact tokens/assets for the new work. Do not re-derive a palette or type pairing from scratch — that's exactly the drift this file exists to prevent. Only revisit it if the user explicitly asks to change direction.
- **Doesn't exist** → this is a fresh project. Also check `~/.tastemaker/profile.md` (outside the repo, in the user's home directory) for a personal taste profile accumulated across their other projects. If it exists, treat it as a strong prior — propose starting from it rather than starting neutral. If neither file exists, this is a genuinely cold start; go to Step 1.

### Step 1 — Figure out what you're actually building

Before touching color or type, scope the work:

- If a PRD, spec, issue, or design brief exists in the project, read it and extract the concrete list of screens/components that need UI (e.g. "onboarding: 3 steps," "empty state for no results," "pricing table," "settings page"). Design effort should map onto this list — don't generate a generic design system disconnected from what's actually being shipped.
- If no spec exists, ask the user directly (briefly) what screens are in scope, rather than guessing. A design system for the wrong surface area is wasted work.

### Step 2 — Establish the style, grounded in something real

This only runs on a cold start (Step 0 found neither file), or when the user explicitly asks to change the project's direction.

- **If the user has references** (pasted images, a Pinterest board export, screenshots, URLs to sites they like): run `scripts/extract_palette.py` against the image(s) to get deterministic dominant colors, contrast ratios, and lightness stats — real numbers pulled from real pixels, not a guess. Combine that with your own visual read of the reference (layout density, corner radii, shadow depth, whether it leans playful/serious/technical) to write a concrete style brief. Anchor every token to something visible in the reference — if you can't point to why a color or pattern is in the brief, don't include it.
- **If the user has no references**, use `references/style-tokens.md` and `references/component-patterns.md` as a starting point, but treat them as scaffolding to adapt, not a catalog to pick from unchanged. Narrow the selection using industry + mood (playful vs. serious vs. premium) — if the user's request already states or implies these (e.g. "premium fintech tool for freelancers"), use that directly instead of re-asking a question they've effectively already answered; only ask when the request genuinely leaves it open.
- Either way, write the result to `.tastemaker/style-lock.md` (see `references/style-lock-format.md` for the exact structure) so every later step in this project reuses it instead of re-deriving.

### Step 3 — Assets, consistently

For any icons, illustrations, hero imagery, or textures the scoped screens need:

- If an image-generation tool is available in this session, generate them conditioned on the locked style tokens *and* on one already-generated "anchor" asset for the project, so the whole set shares one visual DNA instead of drifting per-call. Generate the anchor first, confirm it fits, then condition everything after it on that anchor. Be honest with yourself about fidelity here: matching a distinctive, specific illustration style (a particular character linework, a particular fill treatment) consistently across many assets is genuinely hard even with a good image-gen tool — treat the anchor as a checkpoint to actually verify against, not a formality, and flag to the user early if the style isn't converging rather than shipping a set that only sort-of matches.
- **Decide illustration vs. real photography per section, don't default to one for the whole project.** Sections claiming something factual or physical (office locations, real team headshots) usually call for real photography; sections conveying an abstract concept (mission, values, product feel) are where illustration fits. Ask if it's ambiguous — guessing wrong here (illustrating something that should look "real," like an office) is a common, easy-to-avoid tell.
- **Real photography → Unsplash, via their actual API, automatically.** Run `scripts/fetch_unsplash.py "<search terms>" --out design/assets/photos` (requires a one-time free `UNSPLASH_ACCESS_KEY`, see the script's `--help`). This is a legitimate documented API, not scraping, and the script handles the two things Unsplash's API Guidelines require: it writes photographer + Unsplash attribution to `ATTRIBUTION.md` next to the photos (surface that credit near the photo in the actual UI, not just in the file), and it pings the required download-tracking endpoint. Don't skip the attribution step to save a line of markup — it's a condition of using the API, not a suggestion.
- **Illustrations in an unDraw-like style → one human step, then automatic.** unDraw's own license explicitly prohibits automated scraping or bulk downloading of their assets (a prior third-party CDN for it was shut down for exactly this) — so this skill does not and will not fetch from undraw.co programmatically. Instead: ask the user to spend one minute at undraw.co/illustrations, use unDraw's *own* built-in recolor tool to tint the illustrations they pick to the locked accent color, and drop the downloaded SVGs into `design/assets/`. Everything after that (validation, consistency reuse across screens) proceeds automatically — the one unavoidable manual step is a single visit to unDraw's site, not a repeated ask from you. If assets from other sources need normalizing to the locked palette, `scripts/recolor_svg.py` recolors local SVG files already on disk (it does not fetch anything remote, so it doesn't raise the same licensing concern).
- If no image-generation tool and no human-provided illustrations are available, don't fabricate either — build assets from what you can actually produce reliably: curated open icon sets filtered to match the locked stroke-width/corner-style/fill-vs-outline, and code-native visuals (SVG shapes, CSS gradients/patterns) built directly from the locked palette. These are fully achievable without external APIs and, done well, read as intentional rather than as a placeholder.
- Save generated/curated assets into the project (e.g. `/design/assets/`) rather than inlining them ad hoc, so they're reusable across screens.
- Run `scripts/validate_assets.py` against any SVG assets before using them. SVGs are XML, and a file can read as fine text while still being malformed in a way that renders as a broken image in strict browsers (the most common real case: a `<!-- -->` comment that itself contains `--`, which is illegal XML) — this is invisible unless the file is actually parsed or rendered, so don't skip this in favor of eyeballing the source.
- Bring in motion once the static screens are right, not before: copy `assets/reveal.css` + `assets/reveal.js` into the project (see `references/animation-guidelines.md`) rather than writing scroll/entrance animation from scratch — it's a small, dependency-free scroll-reveal system that already respects `prefers-reduced-motion`.

### Step 4 — Build the actual screens

Now generate the PRD-scoped screens/components, constrained to `.tastemaker/style-lock.md` and the asset files from Step 3. Point explicitly at file paths and token values rather than re-describing the vibe in prose each time — concrete constraints produce consistent output; restated vibes drift.

Before handing back the result, run through `references/anti-slop-checklist.md` — it catches the specific tells (generic gradient defaults, emoji-as-icons, low contrast, unearned skeuomorphism) that make output read as AI-generated regardless of how good the underlying tokens were.

### Step 5 — Close the loop: curate fast, remember what was learned

Taste lives in what gets kept vs. rejected, not in the first draft. What this looks like depends on whether you can actually get a response back:

- **Interactive session** (the normal case): ask a quick, specific keep/reject question rather than an open-ended "thoughts?" — e.g. "keep this hero treatment, or try a variant?" — and log the real answer to `.tastemaker/decisions.log`.
- **Autonomous/single-pass run** (no one available to answer, e.g. a background task): don't fabricate an approval that never happened. Log the decision entry as `status: pending-review` with what was shown and why you chose it, so a later session (or the human, whenever they do look) has the reasoning available and can convert it to a real kept/rejected verdict then. A pending entry is honest; an invented "user approved this" is not.
- Periodically (e.g. every handful of resolved decisions, or when the user says a project is done) summarize durable patterns from *resolved* log entries up into `~/.tastemaker/profile.md` — the kind of preference that would matter on a *different* project too (e.g. "prefers muted/desaturated palettes over saturated ones," "consistently rejects skeuomorphic shadows"), not project-specific detail that belongs only in that project's lock file. Don't promote pending/unresolved entries into the global profile — only real revealed preference should shape future cold starts.

This is what makes the second project faster than the first, and the tenth faster than the second — the tool is meant to get more accurate for a given developer the more they use it, not stay static.

## Reference files

| File | Read when |
|---|---|
| `references/style-lock-format.md` | Writing or updating `.tastemaker/style-lock.md` |
| `references/style-tokens.md` | Cold start with no references — starter palettes, type pairings, spacing/radius/shadow scales by mood |
| `references/component-patterns.md` | Choosing a layout pattern for a given screen type (landing, dashboard, pricing, onboarding, empty states) |
| `references/anti-slop-checklist.md` | Before handing back any generated UI (Step 4) |
| `references/tech-stack-guides.md` | Implementing tokens/components in a specific stack (React/Next/Tailwind, Vue, SwiftUI, Flutter) |
| `references/animation-guidelines.md` | Adding motion/scroll-reveal to a screen (Step 3/4, after statics are settled) |

## Scripts

| Script | Purpose |
|---|---|
| `scripts/extract_palette.py` | Deterministic color/contrast extraction from reference image(s). Usage: `python3 scripts/extract_palette.py <image_path> [image_path ...]` |
| `scripts/validate_assets.py` | Validate generated/curated SVG assets are well-formed before shipping them (Step 3/4). Usage: `python3 scripts/validate_assets.py <file_or_directory>` |
| `scripts/fetch_unsplash.py` | Fetch real photography via Unsplash's official API, with required attribution + download-tracking handled automatically. Usage: `python3 scripts/fetch_unsplash.py "<query>" --out design/assets/photos` (needs a free `UNSPLASH_ACCESS_KEY`) |
| `scripts/recolor_svg.py` | Recolor local SVG files (already on disk, not fetched) to match the locked accent color. Usage: `python3 scripts/recolor_svg.py <path> --accent "#hex" --preserve-dark` |

## Assets

| File | Use when |
|---|---|
| `assets/reveal.css` + `assets/reveal.js` | Adding scroll-reveal/entrance motion to a project — copy both in rather than writing new animation from scratch (Step 3/4, see `references/animation-guidelines.md`) |

## A note on honesty

Don't claim a step happened if it didn't. If there was no image-generation tool available and you fell back to curated icons + code-native visuals, say so plainly rather than implying custom illustrations were generated. If no references were given and the style came from the starter scaffolding, say that too. The whole point of this skill is to close the gap between "looks AI-generated" and "looks intentional" — silently overclaiming what happened undermines the exact trust it's trying to build.
