# Asset Curation

Use this before Step 3 on landing pages, visual product sites, galleries, launch pages, and any request where the user expects a premium or artistic result.

Good pages do not use assets as decoration. They build a small visual cast, then reuse that cast with changing scale, crop, material, and motion.

## The Asset Cast

Pick 4-6 asset roles before writing markup:

- **Hero anchor:** the main object that proves the product exists. Use a real screenshot, generated hero artwork, product photo, or constructed scene.
- **Mode range:** 3-5 different visual registers that prove the system can change taste, not just recolor one layout.
- **Process artifacts:** files, commands, checklists, contrast matrices, logs, receipts, or annotations that explain how the product works.
- **Human or market proof:** real logos, avatars, demos, repo links, public artifacts, or deployment receipts. Do not invent these.
- **Texture object:** one tactile element such as paper, stone, fabric, poster, card, device, plant, or stamp to keep the page from feeling purely digital.
- **Micro assets:** icons, swatches, cursors, arrows, labels, pins, and small crops used to connect the larger pieces.

If a page repeats one screenshot family more than twice, add another asset role or crop family. Repetition needs a story reason.

### Brand/logo walls — fetch the real mark, never a text chip

A "works with," "compatible with," "as seen in," "compare across models," or integration-partner section names real, identifiable companies or products. **The default failure mode is rendering those names as plain text chips** ("ChatGPT", "Vercel", "Webflow" in a `<span>`) instead of the actual logo — it's the fastest way this specific section reads as a stub, because every real product's version of this section shows the mark, not the word. Treat a named-brand row as an asset-sourcing task under Human/market proof, not a copy-writing one:

1. **Fetch the real mark via Iconify**, the same keyless, attribution-free source `scripts/fetch_icons.py` already uses for UI icons — it also carries `simple-icons` (monochrome brand marks, tintable to one color, the usual fit for a mono-tone logo wall) and `logos` (official multi-color marks, for a wall that wants brand color variety). Target either directly: `python3 scripts/fetch_icons.py --icons vercel netlify shopify webflow --set simple-icons --color "#<accent-or-muted>" --out design/assets/logos`.
2. **Check the exact slug before assuming a miss means "unavailable."** Brand slugs don't always match the obvious name — ChatGPT's mark is filed under `openai`, Gemini under `googlegemini`, Bing Copilot under `microsoftbing`, generic Google-attributed features (e.g. "AI Overviews") reasonably borrow the plain `google` mark. `curl -s -o /dev/null -w "%{http_code}" "https://api.iconify.design/simple-icons:<slug>.svg"` returning 200 confirms a slug before spending a fetch call on a guess.
3. **A genuine miss is a real gap, not a placeholder license.** If neither `simple-icons` nor `logos` has a specific brand (this does happen for smaller/niche products), drop that item from the wall rather than rendering it as the one text-only chip in an otherwise-real row — a mixed row (eight real logos, one bare word) is more visibly unfinished than a row of seven.
4. **Validate before shipping**, same as any other fetched SVG: `python3 scripts/validate_assets.py design/assets/logos`.
5. **This is still "real logos… do not invent these."** Fetching the actual mark is what makes that rule operational instead of aspirational — a hand-drawn approximation of a brand's logo is exactly the kind of invented asset that line already forbids.
6. **On a stack that can't run `fetch_icons.py`'s output as-is** (rare — it's just SVG files, so this applies almost everywhere) or where brand trademark policy is a genuine concern for the client, say so plainly rather than silently falling back to text and calling it done.

**Social platform icons (X, LinkedIn, YouTube, GitHub, Discord, TikTok, Instagram, and similar) are the same task, not a separate one** — `simple-icons` covers essentially every platform a footer or "follow us" row would need (`x`, `linkedin`, `youtube`, `github`, `discord`, `tiktok`, `instagram`, `facebook`, and dozens more), so reach for the exact same `fetch_icons.py --set simple-icons` path rather than a separate source. One specific thing to check before pulling from *any* third-party icon repo found by search or by name (a GitHub project, a Dribbble freebie, a "social icons pack"): **verify it actually carries a license before using it.** A public GitHub repo with no `LICENSE` file is not a green light — under default copyright, "no license" means no usage rights were granted, public visibility notwithstanding. This is exactly the gap `simple-icons` (MIT) and the rest of Iconify's sets close by construction, which is why they're the default here rather than "any icon pack that turns up in a search." If a named repo is genuinely richer for a specific brand `simple-icons` lacks, check its license file directly before using it, and say so if it has none rather than treating "it's on GitHub" as sufficient clearance.

### Character / mascot sourcing — an honest answer, not a fabricated one

A custom character or mascot (a brand's own illustrated or 3D-rendered figure, distinct from a stock unDraw scene or a generic icon) is a real, legitimate asset request — especially for a playful/consumer mood — but it does not have a free, attribution-free source the way icons and photos do. There is no "unDraw for bespoke 3D mascots." Handle this honestly rather than quietly substituting something weaker and calling it equivalent:

1. **Check for an image-generation tool before doing anything else.** If this session has one connected (a Recraft/Replicate/Hugging Face/similar MCP, or an API key the user has supplied), generating a custom mascot is the real answer and should be used — following the same consistency discipline as any generated asset: one clear style prompt (medium, palette, proportions, mood) reused across every pose/use so the character reads as one system, not a different mascot each time it's regenerated. Save the winning prompt in `.tastemaker/style-lock.md` so later sessions reuse it instead of drifting.
2. **If no image-generation tool is available, say so plainly and do not fabricate the gap.** Don't imply a "custom mascot" was created when what actually shipped is a generic stock character, and don't silently downgrade the ask into something else without saying that's what happened — the same honesty rule this skill applies everywhere else (see SKILL.md's closing note).
3. **The default fallback: a geometric SVG character built from primitives**, the same technique `references/logo-sourcing.md` uses for a cold-start logo mark — simple shapes (circles, rounded rects, arcs) composed in the locked palette, not a letter dropped in a box. This is free, code-native, infinitely reusable at any size, and — critically for the cursor-interaction pattern in `references/animation-guidelines.md` — trivial to give a tracking eye or a reactive detail, since it's real DOM/SVG, not a flat raster image. It reads as intentional and on-brand rather than photoreal, and that's the honest trade: simpler art, in exchange for free/instant/consistent.
4. **Never approximate a specific real product's mascot.** If a reference shows a particular brand's character (a specific illustrated figure, a specific 3D-rendered mascot), do not attempt to recreate a close likeness of it — that is someone else's commissioned art. Extract the *technique* (bold rounded type, flat saturated color, a character present in the hero, cursor-reactive detail) per `references/verbs/study.md`'s DNA-not-pixels rule, and build an entirely original character for this project instead.
5. **Scale expectations to the source.** A geometric SVG character is a good fit for a simple reactive hero detail (a blob with tracking eyes, an abstract on-brand shape). It is not going to substitute for a full illustrated character system with multiple outfits/poses — set that expectation with the user up front rather than after delivering something smaller than what they pictured.

## Curation Pass

Create a short asset board in `.tastemaker/reference-board.md` or the style lock:

```markdown
## Asset cast
- Hero anchor:
- Mode range:
- Process artifacts:
- Proof:
- Texture object:
- Micro assets:
- Rejected:
```

For each section, assign one primary asset role. A section with no assigned asset role must be intentionally text-led, such as a manifesto poster.

## Composition Patterns

Use the bundled artifact kit when the project has no mature design system:

- `assets/artifact-kit.css` for artifact boards, proof stacks, mode runways, command strips, swatch rails, and tactile cards.
- `assets/artifact-kit.js` for GSAP helpers that animate artifact boards, mode cards, pinned ledgers, and parallax proof images.

The kit is not a theme. Treat it like composition scaffolding, then map it to the project tokens.

Patterns:

- **Artifact board:** layered screenshots, notes, swatches, and command blocks around one anchor image.
- **Mode runway:** overlapping cards that each show a different aesthetic lane.
- **Process ledger:** dark or calm file cards that explain the system with real paths or commands.
- **Poster break:** one typographic section with 1-2 tiny image fragments.
- **Tactile close:** a physical-feeling object or still-life tied to the brand.

## Asset Quality Gates

- Every important image must have a distinct role. Do not reuse the same poster or screenshot as hero, demo, and proof unless the page is explicitly about that artifact.
- At least one section must show range: different product category, mode, layout density, or mood.
- At least one section must show process: files, commands, scans, or decisions.
- At least one section must show physicality: texture, paper, object, shadow, or material.
- Motion must belong to assets, not only text. Scroll should move, reveal, pin, scrub, or transform the visual cast.
- Captures must be local or deploy-safe. If a static site deploys only `site/`, copy needed assets into `site/assets/...`.

## When To Add A Component Library

For production React or Next apps, prefer a real primitive library for interaction and build the visual kit on top of it:

- Radix or shadcn/ui for dialogs, menus, popovers, tabs, selects, sheets, tooltips, and command palettes.
- Motion or GSAP for choreographed asset movement. Use GSAP for scroll-storytelling landing pages.
- React Aria for complex accessible components when design needs custom structure.

For static marketing pages, do not install a full UI library only for cards. Use `artifact-kit.css` plus GSAP. A heavy component library cannot fix weak asset taste.

## Anti-Patterns

- A whole page made from the same screenshot repeated in different card sizes.
- Decorative screenshots that do not teach anything.
- A mode claim with no visible mode gallery.
- Motion only on opacity while all assets sit still.
- Stock assets that could belong to any AI tool.
- Product claims without visual proof beside them.
