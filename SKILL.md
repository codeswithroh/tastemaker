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

- **If the user has references** (pasted images, a Pinterest board export, screenshots, URLs to sites they like): run `scripts/extract_palette.py` against the image(s) to get deterministic dominant colors, contrast ratios, and lightness stats — real numbers pulled from real pixels, not a guess. Combine that with your own visual read of the reference (layout density, corner radii, shadow depth, whether it leans playful/serious/technical) to write a concrete style brief. Anchor every token to something visible in the reference — if you can't point to why a color or pattern is in the brief, don't include it. Once you've assigned extracted colors to Primary/Accent roles, run `scripts/check_contrast.py --palette ...` on the assignment — a color that looked fine as a dominant swatch in the source image can still fail as a button-label background once it's assigned that role (see `references/style-tokens.md`'s Contrast floor section for a concrete example of this exact failure).
- **If the user has no references**, use `references/style-tokens.md` to **auto-select a matched palette + font pairing from the app idea itself** — classify the idea's mood from the keyword table there and apply that mood's pre-built palette/type set, rather than asking the user to pick colors and fonts from scratch. Only ask a direct question when the idea genuinely spans two moods with no lean, per that file's "When to actually ask" section. State in one line which mood was inferred and why, so the user can redirect if the read was wrong. Use `references/component-patterns.md` for layout pattern choice the same way (adapt, don't apply unchanged).
- Either way, write the result to `.tastemaker/style-lock.md` (see `references/style-lock-format.md` for the exact structure) so every later step in this project reuses it instead of re-deriving.

### Step 3 — Real assets, all of them, in the same pass — and attribution-free by design

A site with no real photography, no illustrations, and no motion reads as static and generic no matter how good the color/type tokens are — this step is what makes a generated site feel dynamic and alive. The goal is a **complete site in a single pass**: every section that needs a photo has a real photo, every concept has an illustration, every icon is in place, and it all animates — the first time, with no follow-up round of "now add the images." Every source below is chosen to make that possible: API-first (fetchable automatically, no human browsing step) and **attribution-free** (nothing the end user ever has to see). This is deliberate — an attribution credit sitting on a finished marketing site is a visual hindrance no real product ships, so this skill sources only from places that don't require one.

For every asset the scoped screens need:

- **Decide illustration vs. real photography per section.** Sections showing something factual or physical (office, product-in-use, people, places) call for real photography; sections conveying an abstract concept (mission, values, an idea, a feature benefit) call for illustration. Both get filled in this same pass — neither is optional.
- **Real photography → Openverse, via `scripts/fetch_photos.py`, automatically and with no API key.** Run `scripts/fetch_photos.py "<search terms>" --out design/assets/photos` for every photo-appropriate section — **no key, no signup, nothing to set up**. It searches Openverse (800M+ openly-licensed images), filtered by default to CC0 + Public-Domain-Mark, which legally require **zero attribution** — nothing on the site, ever. This is what makes photos and icons zero-setup: keyless in every session, no accounts, no keys. (Illustrations are the one asset type that may need a single one-time setup step — populating `~/.ideagram/undraw/` — see the Illustrations bullet below; once that's done once, it's reused across every future project.) (Optional upgrade: `--source pixabay` uses Pixabay for more stock-polished, full-res imagery if a section needs it — also attribution-free, but needs a free `PIXABAY_API_KEY`. Use it only when Openverse's more eclectic pool doesn't have a clean match. Unsplash is deliberately not used at all, because its API forces visible on-site attribution.)
- **Credit the sources in the code, never on the page.** `fetch_photos.py` writes a `CREDITS` comment block (creator + source + license per photo) into the photos folder. This is a *voluntary courtesy* — CC0/PDM require nothing — so paste it into a code comment at the top of your HTML/CSS as a genuine thank-you to the people whose work you're using. It's visible to any developer reading the source and invisible to the end user. That's the honest middle ground: generous credit, zero visual hindrance. Never promote it to visible on-page text.
- **Logo → logoyoyo.com mark + locked heading-font wordmark.** See `references/logo-sourcing.md`. Every project scoped in Step 1 that has a landing page or nav bar needs one — pick a symbol from logoyoyo.com's browsable SVG library that echoes the project's concept, recolor it to the locked accent with `scripts/recolor_svg.py`, and pair it with a wordmark set in the project's locked heading font. This is a manual browse step (no API), same category as `ideagram`'s own manual unDraw-library-population step below, done once per project rather than per screen. Once the mark exists, run `scripts/export_favicons.py <mark>.svg --out design/assets/favicons/` to produce the actual browser-tab/home-screen/manifest icon files (favicon.ico, apple-touch-icon, icon-192/512, an OG-card render) — a logo that only exists as a loose SVG never reaches the `<head>` of the page, and a shipped site with no favicon reads as unfinished. Same graceful degradation as PNG export elsewhere: if cairo isn't available it says so and exits cleanly, the SVG itself still works as a modern `<link rel="icon" type="image/svg+xml">`.
- **Illustrations → the vendored `ideagram/` skill, always available, no cross-skill dependency.** `ideagram/` is bundled directly inside this skill (see `ideagram/SKILL.md`) specifically so illustration sourcing never depends on whether a separate `ideagram` skill happens to be installed in the current session — it's part of tastemaker now, not an optional sibling. Two things trigger this step, and both use the exact same workflow:
  1. **Implicit** — Step 3's own illustration-vs-photography split above identifies a concept-driven section (mission, values, an abstract feature benefit) that calls for illustration rather than a photo.
  2. **Explicit** — the user's own request uses the word "illustration" (or "illustrate") anywhere, for anything — a whole site, one section, or an ad-hoc "add an illustration of X here." Treat that word as a direct instruction to run this workflow for that concept immediately, not just a hint to weigh against other options.

  The workflow itself (full detail in `ideagram/SKILL.md`, read it before the first use in a project): distill the concept to one sentence, match it against a **local unDraw library** at `~/.ideagram/undraw/` (real illustrator-grade SVGs, not hand-drawn-by-LLM path data), recolor the match to this project's locked accent with `ideagram/scripts/recolor_undraw.py`, validate with `ideagram/scripts/validate_assets.py`. **If `~/.ideagram/undraw/` doesn't exist yet or has no index**, say so plainly and either ask the user to grab 20-30 free illustrations from undraw.co (30 seconds, no attribution needed) or fall back to `ideagram/assets/primitives` composition — and be upfront that the fallback is a real quality drop from real unDraw art, per `ideagram`'s own honesty rule. Don't silently accept the downgrade as if it were the intended result.
  - **The illustration isn't done until it's in the page.** Save the finished SVG to `design/assets/illustrations/`, then actually reference that file path in the section's markup (`<img src="design/assets/illustrations/<name>.svg" alt="...">` or inlined `<svg>`) as part of the same pass — generating an on-brand illustration and leaving it unused on disk isn't a completed step.
  - Record what happened in `.tastemaker/style-lock.md`'s Assets section (illustration vs. photography split line) — including whether the library was populated or the primitive fallback was used, so a later session in this project doesn't have to rediscover that state.
- **Icons → Iconify, via `scripts/fetch_icons.py`, automatically.** Iconify's public API needs no key, returns SVGs already tinted to the accent color, and draws from permissively-licensed open sets (Lucide, Tabler, Phosphor, …) that require **no attribution**. Pick one set per project and stay in it so every icon shares one stroke weight: `scripts/fetch_icons.py --search "<terms>" --set lucide` to discover names, then `--icons name1 name2 --set lucide --color "#<accent>" --out design/assets/icons` to fetch. Don't fall back to emoji-as-icons or hand-drawn one-offs when a two-line fetch gets a consistent, real icon set.
- **When even a populated unDraw library has no real fit for a concept** (per `ideagram/SKILL.md` Step 2's "don't force a bad match" rule), or an image-gen tool happens to be available for a bespoke style: `references/illustration-sources.md` covers the remaining options, including Streamline as a manual, attribution-aware exception. This is now the rarer path — `ideagram`'s unDraw-match workflow (once the library is populated) is the norm, not Openverse/Iconify-style full automation, because the win here is real illustrator-grade art, not a zero-touch fetch.
- **Last-resort fallback, never the plan:** if a specific asset genuinely can't be sourced (no network, no populated unDraw library and the user can't add one), build it code-native — SVG shapes / CSS gradients from the locked palette — rather than leaving a gap or a grey box. Say plainly when this happened; don't imply a real photo/illustration exists where a placeholder does. Note this should be rare for photos and icons specifically, since both fetch without any key — the illustration path is the one place a one-time manual step (populating `~/.ideagram/undraw/`) may genuinely still be needed.
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
| `references/style-tokens.md` | Cold start with no references — auto-selects a matched palette + Google-Font pairing from the app idea's mood, plus spacing/radius/shadow scales |
| `references/component-patterns.md` | Choosing a layout pattern for a given screen type (landing, dashboard, pricing, onboarding, empty states) |
| `references/logo-sourcing.md` | Step 3 — sourcing a mark from logoyoyo.com and pairing it with the locked heading font into a logo |
| `references/anti-slop-checklist.md` | Before handing back any generated UI (Step 4) |
| `references/tech-stack-guides.md` | Implementing tokens/components in a specific stack (React/Next/Tailwind, Vue, SwiftUI, Flutter) |
| `references/animation-guidelines.md` | Adding motion (Step 3/4) — GSAP + ScrollTrigger is the default engine, including scroll-storytelling timelines; read this first |
| `references/illustration-sources.md` | The attribution-free asset sourcing map (Step 3) — Openverse for photos, the vendored `ideagram/` for illustrations, Iconify for icons, Streamline as a manual exception; plus the "credit in code, never on the page" pattern |
| `ideagram/SKILL.md` | Step 3, Illustrations — the vendored illustration workflow itself (unDraw-library match → recolor → validate). Read before the first illustration in a project. Triggered implicitly by a concept-driven section, or explicitly whenever the user says "illustration"/"illustrate." |

## Scripts

| Script | Purpose |
|---|---|
| `scripts/extract_palette.py` | Deterministic color/contrast extraction from reference image(s). Usage: `python3 scripts/extract_palette.py <image_path> [image_path ...]` |
| `scripts/check_contrast.py` | WCAG contrast check for a palette — body text/background AND button-label/Primary fill (the pairing that's easy to miss; see `references/style-tokens.md`'s Contrast floor section). Usage: `python3 scripts/check_contrast.py --palette text=hex bg=hex primary=hex accent=hex`, or `check_contrast.py <hex1> <hex2>` for a single pair. Run this on any palette — the presets, an extracted reference-image palette, or a user-supplied brand color — not just the starter ones. |
| `scripts/validate_assets.py` | Validate SVG assets are well-formed before shipping them (Step 3/4). Usage: `python3 scripts/validate_assets.py <file_or_directory>` |
| `scripts/fetch_photos.py` | Fetch real photography from Openverse — **no API key**, CC0/public-domain (attribution-free), writes a voluntary code-comment `CREDITS` block. Usage: `python3 scripts/fetch_photos.py "<query>" --out design/assets/photos`. Optional `--source pixabay` (needs `PIXABAY_API_KEY`) for higher-curation imagery. |
| `scripts/fetch_icons.py` | Fetch icons from Iconify — **no API key, attribution-free**, pre-tinted to the accent. Usage: `python3 scripts/fetch_icons.py --search "<terms>" --set lucide` then `--icons a b c --set lucide --color "#hex" --out design/assets/icons` |
| `scripts/recolor_svg.py` | Recolor local SVG files (already on disk) to match the locked accent color. Usage: `python3 scripts/recolor_svg.py <path> --accent "#hex" --preserve-dark` |
| `scripts/export_favicons.py` | Export a logo mark SVG to favicon.ico, apple-touch-icon, PWA manifest icons, and an OG-card PNG (needs cairosvg + system cairo, same as `ideagram/scripts/export_png.py`). Usage: `python3 scripts/export_favicons.py <mark>.svg --out design/assets/favicons/` |
| `ideagram/scripts/build_library_index.py` | Index a local unDraw library (`~/.ideagram/undraw/`) into `index.md`/`index.json` for matching. Run once after populating/updating the library. |
| `ideagram/scripts/recolor_undraw.py` | Recolor a matched unDraw illustration's accent to the project's locked accent, preserving skin/ink/clothing/neutrals. The illustration workhorse — see `ideagram/SKILL.md` Step 3. |
| `ideagram/scripts/extract_component.py` | Lift a whole figure/device/panel out of a source unDraw SVG to compose a custom scene, for the rare case no single library illustration fits (`ideagram/SKILL.md` Step 4). |
| `ideagram/scripts/export_png.py` | Export a finished illustration to social/presentation PNG sizes (needs cairosvg + system cairo). |

## Assets

| File | Use when |
|---|---|
| `assets/gsap-starter.js` | **Default motion for every project.** Wires the `data-reveal`/`data-reveal-group` markup convention to GSAP + ScrollTrigger — reduced-motion-aware via `gsap.matchMedia()`. Requires GSAP/ScrollTrigger loaded first (see `references/tech-stack-guides.md` for CDN vs. npm per stack). |
| `assets/reveal.css` + `assets/reveal.js` | Fallback only, for contexts that can't take a GSAP dependency — same markup convention as `gsap-starter.js`, so switching between them requires no markup changes. |

## A note on honesty

Don't claim a step happened if it didn't. If there was no image-generation tool available and you fell back to curated icons + code-native visuals, say so plainly rather than implying custom illustrations were generated. If no references were given and the style came from the starter scaffolding, say that too. The whole point of this skill is to close the gap between "looks AI-generated" and "looks intentional" — silently overclaiming what happened undermines the exact trust it's trying to build.
