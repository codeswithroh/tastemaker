# Layout patterns by screen type

Pick the pattern that fits the PRD's actual goal for the screen, not the first one on the list. These are structural starting points — the locked style tokens (palette/type/shape) from `.tastemaker/style-lock.md` determine how they're skinned.

## Show, don't tell — the default that overrides all the patterns below

Before picking any pattern, apply the visual-over-text default from SKILL.md Step 4. The failure mode every layout below can collapse into is "heading + two sentences of prose," repeated down the page. Each pattern has a *show* version that carries the same meaning with a visual and a caption instead of a paragraph — reach for that version first:

| Instead of telling (text) | Show it (visual) |
|---|---|
| A feature card: heading + 2-sentence description | A small mockup of the feature's actual UI, with a one-line caption |
| "Fast / powerful / real-time analytics" | An actual chart or dashboard fragment rendered in the locked palette |
| "Simple 3-step setup" as a bulleted list | Three side-by-side visual panels, each a screen state, numbered |
| "See the difference" prose | A literal before/after split or slider |
| A stat buried in a sentence | A big number + one-word label, as its own tile |
| "Works with your stack" paragraph | A logo/icon grid of the integrations |
| "Trusted by teams" claim | The actual logo strip, or a real testimonial with a face |
| An abstract benefit (calm, focus, security) | The project's `ideagram` illustration for that concept |

The point isn't to delete all copy — a headline, a short subhead, captions, and CTA labels are text doing real work. The point is that the *primary content of each section is something to look at*, and text captions it. A section that's mostly words with a decorative icon on top is the thing to catch and rebuild.

## Column balance — a default that applies across every two-column pattern below

Two-column sections show up constantly: a pricing headline next to a stack of tier cards, a feature row of short labels next to a headline-and-CTA block, an About page's alternating text/image rows. Their columns are rarely the same natural height — a headline-and-paragraph column commonly runs taller than a short card stack or a handful of labels next to it.

Left alone, the default failure mode is: each column renders at its own natural height, the shorter one stops short, and the section reads unbalanced — a cluster of content near the top with a block of unclaimed space below it. This isn't a padding problem (see `references/style-tokens.md`'s Spacing scale for that); it's a layout decision nothing was making by default.

When a two-column section's columns differ noticeably in natural height, pick one deliberate treatment instead of leaving it to chance:

1. **Vertically center the shorter column** against the taller column's height (`align-items: center` on the row). Best when the shorter column reads fine as a self-contained block wherever it lands — three pricing cards centered next to a tall headline column, rather than pinned to the top with dead space below.
2. **Add a real filler element that intentionally uses the remaining height.** A stat callout, a short testimonial, a small supporting illustration, a secondary CTA note. This fills the gap with actual content instead of blank space — the "show, don't tell" default above applies here too, so reach for a visual filler over another paragraph.
3. **Cap the taller column** so both sides land closer to the same length — tighten the headline, shorten the paragraph, or cap the column's max-width/line count. Best when the taller column's extra length is prose creep rather than content that has to be there.

Pick whichever treatment fits the specific section; the failure to catch is leaving the shorter column to trail into empty space by default because nothing decided otherwise.

## Section-to-section separation

For a page with several stacked sections to read as distinct, intentional beats rather than one long scroll of similar-looking blocks, pick **one** separation mechanism for the whole project and apply it consistently at every section boundary — don't decide it per section:

- **Alternating surface tint** (Background/Surface alternating section by section) — a solid default for a content-dense marketing page with many stacked sections; the tint alone marks the boundary without adding a visible line.
- **Hairline divider** (a 1px border at the section boundary) — fits a project already using hairline borders elsewhere instead of shadows (the semi-brutalist treatment in `references/anti-slop-checklist.md`); mixing a divider into a project that otherwise uses soft shadows reads as inconsistent.
- **Fixed minimum section padding**, applied regardless of content, with no tint or divider — works when the mood already commits to generous whitespace (an "editorial/generous" project per `references/style-tokens.md`) and additional visual noise would undercut that.

Record the chosen mechanism once in `.tastemaker/style-lock.md` the same way other per-project decisions are recorded, and reuse it — a page that alternates tint on some boundaries and adds dividers on others reads as unplanned, the same failure mode inconsistent spacing produces.

## Landing / marketing page
- **Hero-centric**: one sharp promise + one short explanation + one primary CTA (optionally one secondary) + one supporting visual. This is the default for most products. Read `references/hero-guidelines.md` before building it; the hero is an attention hierarchy, not a compressed feature tour.
- **Social-proof-first**: logos/testimonials above the fold, hero secondary. Use when credibility is the biggest conversion blocker (enterprise, higher price point).
- **Problem/solution narrative**: scroll-driven sections walking through a pain point then the fix. Use for products solving a non-obvious problem that needs explaining before the pitch lands.
- **Default fold boundary**: keep workflow steps, metrics, integration grids, detailed proof, and secondary product states below the hero. If the pitch needs them to make sense, simplify the pitch rather than attaching more modules above the fold.
- Common failure: stacking 6+ generic feature cards with icon + heading + one line, identical structure repeated — the text-wall tell. Apply the show-don't-tell table above: convert feature cards into feature *mockups*, vary rhythm (a full-width visual, an alternating two-column showing the feature in use, a comparison table, a real chart) so the page is a sequence of things to look at, not a stack of paragraphs.

## App shell (dashboards, internal tools, anything behind a sidebar)

This is a first-class pattern, not a footnote under "Dashboard." A meaningful share of what gets built with a coding agent is internal tooling, not a marketing site, and it has a genuinely different shape: a persistent navigation frame the user works *inside*, not a page they scroll through once. Don't reach for `references/hero-guidelines.md` here — there is no hero, the shell is the whole first impression, every session.

### The shape

The default shell for anything with more than a handful of screens is sidebar plus topbar, content in between:

```
┌─────────┬──────────────────────────────┐
│         │  topbar: breadcrumb / search / account   │
│ sidebar │──────────────────────────────│
│  nav    │                              │
│         │        content area          │
│         │   (the one thing this        │
│         │    screen is actually for)   │
└─────────┴──────────────────────────────┘
```

- **Sidebar**: primary navigation, persistent across every screen. Sections/groups if the product has more than ~7 top-level destinations; a flat list otherwise. Collapsible to icon-only on narrow viewports, not hidden entirely — internal tool users live in this thing for hours, don't make them reopen it constantly.
- **Topbar**: contextual, not navigational. Breadcrumb or current-section label, search, account/notifications. It should never duplicate what the sidebar already tells the user.
- **Content area**: exactly one job per screen. See the existing dashboard guidance below for how to lead with it.

### Map the locked palette onto persistent chrome, not just one-off sections

A marketing page skins each section once. A shell skins the *frame* once and reuses it on every screen, so get this mapping right at Step 2, record it in `.tastemaker/style-lock.md`, and don't re-derive it per screen:

- **Sidebar background**: usually `Surface`, one step off `Background`, so the content area reads as the "canvas" and the sidebar reads as structural chrome around it. In a dark-mode-native project (e.g. the Technical/builder mood), this can invert — a near-black sidebar against a very slightly lighter content area — either direction is fine as long as it's deliberate and consistent.
- **Content area background**: `Background`. This is where the user's actual work/data lives; it should be the quietest surface in the shell.
- **Topbar**: usually shares the content area's `Background` with a `Border` hairline underneath, not its own distinct fill — it's contextual chrome, not a second nav surface competing with the sidebar.
- **Active nav item**: the one place `Primary` earns a dedicated treatment outside a button — a filled pill/row, or a `Primary`-colored left-border accent on an otherwise-transparent row. Pick one treatment and use it for every active state in the shell, not a different one per section.
- **Hover state on inactive nav items**: a subtle `Surface`-on-`Surface` shift (or `Background`-on-`Surface`, whichever is lighter in context) — never the same visual weight as the active state, or users lose track of where they actually are.
- **Breadcrumbs**: `Text muted` for all but the current segment, which gets `Text primary`. Don't spend `Primary` or `Accent` on breadcrumb links; they're wayfinding, not calls to action.

Run every pairing this introduces (active-row text on its fill, hover-state text on its background) through `scripts/check_contrast.py --matrix` the same as any other new pairing — Step 4's color-contract non-negotiable applies to shell chrome exactly like it applies to a marketing hero.

### Density is correct here, not a mistake to fix

A "premium/confident" marketing page wants generous whitespace. An app shell showing the same mood should still be *denser* than its own marketing page — more rows visible without scrolling, tighter row height, smaller default type size in data-heavy areas. This is not a contradiction of the locked mood; it is what that mood looks like applied to a tool instead of a pitch. Don't inherit the marketing page's spacing scale wholesale into the shell; use `references/style-tokens.md`'s "dense/information-heavy" spacing guidance instead, per project.

### Motion in the shell

Covered in full in `references/animation-guidelines.md`'s "App shell motion" section — panel/tab-switch transitions, staggered list/table entrances on data-load, animated state changes, skeleton loading. The scroll-storytelling track from that same file does not apply to a shell; there is no scroll narrative to tell.

### The screen content itself

Once the shell and its chrome are locked, individual screens follow:
- Lead with the one number/status the user opens the app to check — don't bury it below navigation chrome.
- Group related metrics; don't scatter unrelated KPIs in one uniform grid just because a grid is easy to build.
- Empty and loading states matter as much as the populated state — design them explicitly, don't leave them as an afterthought default.

## Pricing
- 3 tiers is the safe default (2 feels thin, 4+ causes decision paralysis) unless the product genuinely needs more.
- Highlight one tier visually (border, subtle background shift) — don't rely on a "Most Popular" ribbon alone to do that work.
- Put the annual/monthly toggle and the actual price close together; don't make users hunt for what a plan costs.
- If the section pairs a headline column with the tier cards side by side, that's the Column balance case above — a headline column running the full section height next to cards clustered near the top is the concrete failure that rule exists to catch. Center the cards against the headline's height, or add a real element (a short FAQ note, a guarantee callout) below them rather than leaving the gap.

## Onboarding
- Map directly to the PRD's step list — don't invent extra steps or collapse necessary ones for the sake of a "clean 3-step flow" if the product actually needs 5.
- Show progress (steps remaining, not just a generic spinner) — abandonment correlates with uncertainty about how much is left.
- First-run empty states should teach by example (a pre-filled sample, not a blank field with placeholder text) wherever the product allows it.

## Empty states
- Explain what will appear here and how to make it appear (one clear action), not just "No data yet."
- This is a legitimate place for the project's anchor illustration/asset — empty states are low-stakes, high-visibility real estate for personality.

## About / company / mission page
- Structure that reads as intentional rather than a template dump: hero statement → a small row of illustrated concept icons (not literal feature icons) → credibility stats → logo strip (social proof) → a values grid (2x2 or 3-column, icon + heading + one line) → team grid → physical presence (real office photography, not illustration).
- **This is the page type most likely to mix asset kinds on purpose**: illustrations for abstract concepts (mission, values, team personality) but real photography for anything claiming physical/factual presence (offices, sometimes real team headshots instead of illustrated avatars). Don't illustrate everything by default — ask which sections are meant to feel "real" (offices, actual team photos) vs. "conceptual" (mission, values) before generating assets, since guessing wrong here is a common way this page type ends up feeling like a template.
- Stats and logo-strip rows work best restrained — 3-4 stats, 5-6 logos, plenty of whitespace. Cramming more in reads as filler rather than credibility.

## Settings / forms
- Group by relatedness, not alphabetically or by database schema order.
- Destructive actions (delete account, remove data) visually separated and never styled identically to safe actions.
- Save state should be obvious (either autosave with a clear confirmation, or an explicit save action that's unambiguous about what it commits).
