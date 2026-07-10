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

### Step 3 — Assets, consistently, and by default (not just when convenient)

A site with no real photography, no illustrations, and no motion reads as static and generic no matter how good the color/type tokens are — this step is what actually makes a generated site feel dynamic and alive rather than a flat mockup. Treat real assets and motion as standard for every project, not something to add only if it happens to be easy.

For any icons, illustrations, hero imagery, or textures the scoped screens need:

- **Decide illustration vs. real photography per section, don't default to one for the whole project.** Sections claiming something factual or physical (office locations, real team headshots, product-in-use) call for real photography; sections conveying an abstract concept (mission, values, an idea, a feature benefit) call for illustration. Ask if it's ambiguous — guessing wrong here (illustrating something that should look "real," like an office) is a common, easy-to-avoid tell.
- **Real photography → Unsplash, via their actual API, by default.** Run `scripts/fetch_unsplash.py "<search terms>" --out design/assets/photos` for every section that calls for real photography (requires a one-time free `UNSPLASH_ACCESS_KEY`, see the script's `--help`) — don't skip this and settle for a flat color block or a placeholder where a photo-appropriate section exists. This is a legitimate documented API, not scraping, and the script handles the two things Unsplash's API Guidelines require: it writes photographer + Unsplash attribution to `ATTRIBUTION.md` next to the photos, and it pings the required download-tracking endpoint. **Attribution must be visible on the actual site, not just in a code comment or a file that never ships** — that's a condition of API access Unsplash actively enforces, not a style preference, and there's no compliant way around it. It does not have to be prominent: a small, unobtrusive credit line (e.g. a subtle caption on the image itself, or a compact "Photo credits" line grouped in the footer) satisfies the requirement without fighting the rest of the design — see `references/illustration-sources.md` for a concrete pattern.
- **Illustrations: the `ideagram` skill is the default, not one option among several.** It generates original artwork on the spot, matched to this project's locked accent color, with zero manual steps and zero licensing gray area — use it whenever it's available in this session. Only when `ideagram` isn't available, or its flat-primitive-composition style genuinely doesn't fit what a section needs, fall back to a human-assisted external source — and don't treat unDraw as the only option there. `references/illustration-sources.md` covers unDraw and Streamline side by side; pick whichever's actual illustration style is the closer match for the project, not whichever is more familiar. Both require the same one-time manual step (a human browses, picks, and downloads — neither can be scraped automatically, for license/fair-use reasons covered in that file) and the same thing after that: validate, recolor to the locked accent if needed, reuse. Whichever source ends up used, having a real illustration in every concept-driven section is the default — a mission/values/feature section with no illustration at all is usually a sign this step got skipped, not a legitimate style choice.
- If an image-generation tool is separately available in this session and a genuinely custom illustration style is wanted (beyond what `ideagram`'s primitive-composition system covers), generate assets conditioned on the locked style tokens *and* one already-generated "anchor" asset so the whole set shares one visual DNA instead of drifting per-call. Be honest about fidelity here: matching a distinctive illustration style consistently across many assets is genuinely hard even with a good image-gen tool — treat the anchor as a checkpoint to actually verify against, and flag early if the style isn't converging rather than shipping a set that only sort-of matches.
- If none of the above are available for a given asset, don't leave a gap — build from what you can actually produce reliably: curated open icon sets filtered to match the locked stroke-width/corner-style/fill-vs-outline, and code-native visuals (SVG shapes, CSS gradients/patterns) built directly from the locked palette. These are fully achievable without external APIs and, done well, still read as intentional rather than as a placeholder.
- Save generated/curated assets into the project (e.g. `/design/assets/`) rather than inlining them ad hoc, so they're reusable across screens.
- Run `scripts/validate_assets.py` against any SVG assets before using them. SVGs are XML, and a file can read as fine text while still being malformed in a way that renders as a broken image in strict browsers (the most common real case: a `<!-- -->` comment that itself contains `--`, which is illegal XML) — this is invisible unless the file is actually parsed or rendered, so don't skip this in favor of eyeballing the source.
- **Motion is a default too, via GSAP.** Once the static screens are right, wire up `assets/gsap-starter.js` on top of GSAP + ScrollTrigger (see `references/animation-guidelines.md`) for scroll-driven reveals, staggered entrances, and hover/press micro-interactions — this is what makes a site feel interactive rather than static, and it's the default motion system for every project, not an optional add-on. The dependency-free `reveal.css`/`reveal.js` pair exists only as a fallback for contexts that genuinely can't take a GSAP dependency.

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
| `references/animation-guidelines.md` | Adding motion (Step 3/4, after statics are settled) — GSAP + ScrollTrigger is the default engine, read this first |
| `references/illustration-sources.md` | Sourcing illustrations when `ideagram` isn't available or doesn't fit (Step 3) — covers unDraw and Streamline, their fair-use/attribution terms, and how to keep Unsplash's required attribution unobtrusive |

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
| `assets/gsap-starter.js` | **Default motion for every project.** Wires the `data-reveal`/`data-reveal-group` markup convention to GSAP + ScrollTrigger — reduced-motion-aware via `gsap.matchMedia()`. Requires GSAP/ScrollTrigger loaded first (see `references/tech-stack-guides.md` for CDN vs. npm per stack). |
| `assets/reveal.css` + `assets/reveal.js` | Fallback only, for contexts that can't take a GSAP dependency — same markup convention as `gsap-starter.js`, so switching between them requires no markup changes. |

## A note on honesty

Don't claim a step happened if it didn't. If there was no image-generation tool available and you fell back to curated icons + code-native visuals, say so plainly rather than implying custom illustrations were generated. If no references were given and the style came from the starter scaffolding, say that too. The whole point of this skill is to close the gap between "looks AI-generated" and "looks intentional" — silently overclaiming what happened undermines the exact trust it's trying to build.
