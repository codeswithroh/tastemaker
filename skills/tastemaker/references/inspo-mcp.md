# Inspo MCP — real, measured reference data instead of a text search

When the `inspo` MCP is connected in this session (tools named `mcp__inspo__*` — check the tool list, don't assume), it replaces the *default* path in `references/reference-intelligence.md` for building a reference board. It is not a general web-search tool: it's a curated archive of real, captured production sites with **measured** design data attached to each one — extracted palettes (real hex values, not guessed), detected typefaces, a macrostructure tag, and a fold-by-fold "autopsy" written by the archive, plus aggregate evidence (what % of a category is dark-mode, grotesk-sans, cool-accent, etc.) computed across dozens of real sites at once. This is strictly better grounding than a `WebSearch` + a handful of `WebFetch` calls for the same step, because the data is already structured and already measured rather than something a screenshot has to be re-interpreted from scratch.

**Precedence: if `inspo` is connected, it is the default for Step 1.25's reference board and Step 2.5's macrostructure pick — not an optional extra alongside `WebSearch`.** Fall back to `WebSearch`/`WebFetch` (per `reference-intelligence.md`) only when `inspo` is not in this session's tool list, or when the brief needs something inspo's archive genuinely doesn't cover (a narrow local/regional business category, a very recent launch not yet captured).

## Budget discipline (the tool's own stated rule — respect it)

`inspo`'s own tool descriptions are explicit about this: **one `recommend` call, one or two `search_screens` calls, then `get_screen` (or the inline autopsy) on the 3-5 references actually kept is a complete study.** Results are re-read on every later turn in the same session, so a fourth or fifth search costs more context than it finds. Don't loop calling `search_screens` with minor filter tweaks hoping for a better hit — `get_filters` up front (zero-cost, returns every valid enum value) prevents most of the wasted calls that come from guessing at a filter value and getting a validation error.

- `detail: "concise"` or the default `"standard"` almost always suffices — only ask for `detail: "full"` (the fold-by-fold autopsy on every row, ~300 tokens each) when you will actually read all of them, per the tool's own guidance.
- `find_reference_components` is an index (cheap); only call `get_reference_jsx` on the one or two archetypes actually being built from, not every entry in the index.

## Where this plugs into the existing workflow

### Step 1.25 — the reference board (`references/reference-intelligence.md`)

Replace the manual "search the category, fetch 2-3 sites" sequence with:

1. **`mcp__inspo__recommend({ brief })`** — pass the same one-line design read `reference-intelligence.md` already asks you to state (surface type, audience, mood). One call returns: a macrostructure pick with rationale, a shortlist of runner-up macrostructures with real exemplar counts (`macrostructureCoverage`), 5 real exemplar sites with palette/fonts/autopsy, a suggested palette, and an **evidence packet** — the measured consensus for paper band (light/mid/dark), display-face class, and accent hue across the whole matching category, with outlier sites that break the consensus named explicitly.
2. **Write the evidence packet straight into `.tastemaker/reference-board.md`'s Quality bar section** — this is a stronger, citable version of what that section already asks for, now backed by a real measured number instead of an impression ("71% of 24 matching sites use a grotesk-sans display face; going with it" is a materially different claim than "this category tends toward sans-serif").
3. **Read the `note` field in the evidence packet as an instruction, not a trivia fact.** It reads something like *"the category's strongest pull is X — this is the gravity to take a position on, with it or against it, not a template to match."* That line is the tool's own version of this skill's anti-genericness stance: matching the consensus exactly is the generic choice; the reference board should say explicitly whether this build is going *with* the gravity or deliberately *against* it, and why.
4. **`heroGuidance` and `spacingGuidance` fields (when present) are measured rules, not filler** — real numbers pulled from the matching sites (e.g. a real median section-rhythm figure, a real container-padding gotcha). Treat them as a supplement to `references/hero-guidelines.md` and `references/style-tokens.md`'s own spacing scale, not a replacement — where they agree, that's extra confidence; where they conflict, the project's own locked scale in `.tastemaker/style-lock.md` still wins once it exists.

### Step 2.5 — the macrostructure pick (`references/macrostructures.md`, `references/diversification.md`)

`inspo`'s macrostructure vocabulary (19 named shapes: Bento Grid, Marquee Hero, Feature Stack, Split Studio, Specimen, Manifesto, and more — `get_filters` returns the full list with a live count of exemplars per shape) is a different taxonomy than this skill's own 12 macrostructures, not a 1:1 mapping. Don't force one onto the other. Use `inspo` here as **evidence for the pick, not as the pick itself**:

- `mcp__inspo__find_examples_for_macrostructure({ name })` — real sites for a shape already under consideration, useful for checking "does this shape actually work for a brief like this" against real examples before committing.
- The rotation rule in `references/diversification.md` (don't repeat this *project's* last macrostructure) is still mandatory and is **not** something `inspo` knows about — it has no memory of this specific project's build history, only of the wider archive. Cross-project rotation stays `~/.tastemaker/structure-history.json`'s job; `inspo`'s `macrostructureCoverage` counts are about the category at large, not about what *this* project or *this* user has already shipped. Use both: `inspo` to ground the pick in what's real, the structure-history files to keep it from repeating.

### Component sourcing (`references/component-sourcing.md`)

`mcp__inspo__find_reference_components({ type })` returns an index of named archetypes per component category (hero, pricing, cta, nav, footer, testimonial, logo-cloud, faq, stat) — each with a one-line description of the composition pattern (e.g. hero archetypes named "Marquee" — a type-only anti-slop hero with no imagery — or "Stat-Led" — leads with a real number, explicitly "refuse otherwise, don't invent one," matching this skill's own honesty rule). `mcp__inspo__get_reference_jsx({ type, id })` returns the full React + Tailwind source for one.

- Add this as another entry in Step 1.5's precedence order, alongside the shadcn registries — reach for it when the brief needs a specific *composition* (not just a functional primitive) and none of the existing registries have quite the right shape.
- **React + Tailwind source, same stack caveat as everywhere else in this skill**: on a stack that can't consume it directly, read the JSX for structure/spacing/hierarchy and port the pattern by hand, the same rule `component-sourcing.md`'s Step 0 already applies to every other registry.
- `mcp__inspo__find_components({ type })` (plural) is the visual-crop version — real captured components from real sites, useful for browsing what a category's pricing tables or footers actually look like before picking an archetype to build from.

### Color grounding (`references/style-tokens.md`)

`mcp__inspo__find_by_color({ hex })` finds real shipped sites whose extracted palette sits near a given hex (OKLAB distance — same color family, not just same hue). Use this when a brief names a fixed brand color and you want to see how that color family reads in real, shipped products before running `scripts/generate_palette.py` — it's a sense-check on the generated palette's character, not a replacement for the generator (the generator still owns making the actual contract pass contrast).

## The non-negotiable rule: DNA, not pixels

Everything `inspo` returns is a **real, captured, third-party site** — real screenshots, real measured palettes, real copy in the autopsy text. The same rule `references/verbs/study.md` already states for any reference screenshot applies here without exception: **extract the reusable pattern (macrostructure, type pairing, spacing rhythm, color role, the *shape* of a hero) — never the specific pixels, never a specific site's exact copy or composition.** Two things follow directly:

- **Never reproduce a specific exemplar's headline, body copy, or exact layout verbatim.** The autopsy text describes what a real site's hero says — that's *their* copy, not a template to fill with a new brand name. Write this project's own copy per `references/copy-voice.md`, informed by the *pattern* (a Marquee hero is type-only with a mono dateline; that's a structural fact you can reuse) not the *words*.
- **The evidence packet's job is to prevent convergence, not cause it.** If every build in a category reaches for the same top exemplar's exact composition, `inspo` has been used backwards — as a template library instead of as evidence for an informed, sometimes deliberately contrarian, choice. The `note` field saying "this is the gravity to take a position on" is the tool telling you the same thing this skill's diversification engine exists to prevent.

## When `inspo` isn't connected — supahero.io as a manual fallback

supahero.io is a human-curated directory of real hero sections (Linear, Stripe, Raycast, Resend, Ramp, Figma, and hundreds more, each linking to the live site) — not an MCP, no structured data, just a fast way to browse to a specific real reference when `inspo` isn't available this session. It's narrower than `inspo` (hero sections only, no measured evidence, no palette/font extraction) but useful specifically for `references/hero-guidelines.md`'s mandatory "real reference check" — open 2-3 entries in the project's category, then study the live site the same way `inspo`'s exemplars are meant to be studied: extract the specific device or restraint, never the pixels or copy (same DNA-not-pixels rule as everywhere else in this file).

## Reference

`get_filters` (zero-cost, call when unsure of a valid enum value) — `recommend` (orchestrator, start here for a brief) — `search_screens` / `find_similar` / `find_by_color` (targeted lookups) — `find_examples_for_macrostructure` / `find_components` / `find_reference_components` + `get_reference_jsx` (structure and component sourcing) — `compare` (triangulate a house style from 2-4 known references) — `get_screen` / `get_design_system` (full record for one known site) — `list_collections` / `get_collection` (editor-curated thematic sets) — `get_site_pages` (how a real product sequences landing → pricing → features, useful for a multi-page site's own page-to-page flow).
