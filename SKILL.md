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

### Step 3 — Real assets, all of them, in the same pass — and attribution-free by design

A site with no real photography, no illustrations, and no motion reads as static and generic no matter how good the color/type tokens are — this step is what makes a generated site feel dynamic and alive. The goal is a **complete site in a single pass**: every section that needs a photo has a real photo, every concept has an illustration, every icon is in place, and it all animates — the first time, with no follow-up round of "now add the images." Every source below is chosen to make that possible: API-first (fetchable automatically, no human browsing step) and **attribution-free** (nothing the end user ever has to see). This is deliberate — an attribution credit sitting on a finished marketing site is a visual hindrance no real product ships, so this skill sources only from places that don't require one.

For every asset the scoped screens need:

- **Decide illustration vs. real photography per section.** Sections showing something factual or physical (office, product-in-use, people, places) call for real photography; sections conveying an abstract concept (mission, values, an idea, a feature benefit) call for illustration. Both get filled in this same pass — neither is optional.
- **Real photography → Pixabay, via `scripts/fetch_photos.py`, automatically.** Run `scripts/fetch_photos.py "<search terms>" --out design/assets/photos` for every photo-appropriate section (needs a one-time free `PIXABAY_API_KEY` — see `--help`). Pixabay's Content License requires **no attribution at all** — no caption, no footer credit, nothing on the site. Use the photos directly. (Pexels is an equally attribution-free alternative if preferred; `references/illustration-sources.md` notes the distinction. Both are chosen over Unsplash specifically because Unsplash's API forces visible on-site attribution, which this skill deliberately avoids.)
- **Illustrations → the `ideagram` skill, automatically.** It generates original artwork on the spot, matched to this project's locked accent color, with zero manual steps, zero licensing question, and zero attribution — use it for every concept-driven section whenever it's available in this session. This is the default illustration path, full stop.
- **Icons → Iconify, via `scripts/fetch_icons.py`, automatically.** Iconify's public API needs no key, returns SVGs already tinted to the accent color, and draws from permissively-licensed open sets (Lucide, Tabler, Phosphor, …) that require **no attribution**. Pick one set per project and stay in it so every icon shares one stroke weight: `scripts/fetch_icons.py --search "<terms>" --set lucide` to discover names, then `--icons name1 name2 --set lucide --color "#<accent>" --out design/assets/icons` to fetch. Don't fall back to emoji-as-icons or hand-drawn one-offs when a two-line fetch gets a consistent, real icon set.
- **When `ideagram` genuinely doesn't fit** a section (it needs more detail than its flat-primitive style produces), or an image-gen tool is available for a bespoke style: `references/illustration-sources.md` covers the options, including manual sources (unDraw, Streamline — both also attribution-free). These are the exception, and they involve a human browse step; the automatic ideagram + Pixabay + Iconify trio is the norm.
- **Last-resort fallback, never the plan:** if a specific asset can't be sourced (no key, no network, no ideagram), build it code-native — SVG shapes / CSS gradients from the locked palette — rather than leaving a gap or a grey box. Say plainly when this happened; don't imply a real photo/illustration exists where a placeholder does.
- Save everything into `design/assets/` (photos, illustrations, icons in their own subfolders) so it's reusable across screens, and run `scripts/validate_assets.py` over any SVGs before use — a malformed SVG (classically a `--` inside a `<!-- -->` comment) reads fine as text but renders as a broken image in strict browsers, invisible unless actually parsed.
- **Motion → GSAP + ScrollTrigger, in the same pass, not a later polish step.** Wire up `assets/gsap-starter.js` for scroll-driven reveals and staggered entrances, and for anything with a narrative/storytelling shape (a landing page that unfolds section by section) build a GSAP scroll timeline per `references/animation-guidelines.md` — pinned sections, scrubbed reveals, sequenced hero moments. This is what turns a stack of static sections into a site that tells a story as you scroll, and it's default, not optional. The dependency-free `reveal.css`/`reveal.js` pair remains only as a fallback for contexts that can't take a GSAP dependency.

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
| `references/animation-guidelines.md` | Adding motion (Step 3/4) — GSAP + ScrollTrigger is the default engine, including scroll-storytelling timelines; read this first |
| `references/illustration-sources.md` | The attribution-free asset sourcing map (Step 3) — Pixabay/Pexels for photos, ideagram/Iconify for generated & icon assets, unDraw/Streamline as manual exceptions; why every default is attribution-free |

## Scripts

| Script | Purpose |
|---|---|
| `scripts/extract_palette.py` | Deterministic color/contrast extraction from reference image(s). Usage: `python3 scripts/extract_palette.py <image_path> [image_path ...]` |
| `scripts/validate_assets.py` | Validate SVG assets are well-formed before shipping them (Step 3/4). Usage: `python3 scripts/validate_assets.py <file_or_directory>` |
| `scripts/fetch_photos.py` | Fetch real photography from Pixabay — **attribution-free**, no on-site credit needed. Usage: `python3 scripts/fetch_photos.py "<query>" --out design/assets/photos` (needs a free `PIXABAY_API_KEY`) |
| `scripts/fetch_icons.py` | Fetch icons from Iconify — **no API key, attribution-free**, pre-tinted to the accent. Usage: `python3 scripts/fetch_icons.py --search "<terms>" --set lucide` then `--icons a b c --set lucide --color "#hex" --out design/assets/icons` |
| `scripts/recolor_svg.py` | Recolor local SVG files (already on disk) to match the locked accent color. Usage: `python3 scripts/recolor_svg.py <path> --accent "#hex" --preserve-dark` |

## Assets

| File | Use when |
|---|---|
| `assets/gsap-starter.js` | **Default motion for every project.** Wires the `data-reveal`/`data-reveal-group` markup convention to GSAP + ScrollTrigger — reduced-motion-aware via `gsap.matchMedia()`. Requires GSAP/ScrollTrigger loaded first (see `references/tech-stack-guides.md` for CDN vs. npm per stack). |
| `assets/reveal.css` + `assets/reveal.js` | Fallback only, for contexts that can't take a GSAP dependency — same markup convention as `gsap-starter.js`, so switching between them requires no markup changes. |

## A note on honesty

Don't claim a step happened if it didn't. If there was no image-generation tool available and you fell back to curated icons + code-native visuals, say so plainly rather than implying custom illustrations were generated. If no references were given and the style came from the starter scaffolding, say that too. The whole point of this skill is to close the gap between "looks AI-generated" and "looks intentional" — silently overclaiming what happened undermines the exact trust it's trying to build.
