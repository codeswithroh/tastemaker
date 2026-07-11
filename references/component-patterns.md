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

## Landing / marketing page
- **Hero-centric**: single bold headline + subhead + one CTA + supporting visual. Use when the product needs a single clear pitch (most SaaS).
- **Social-proof-first**: logos/testimonials above the fold, hero secondary. Use when credibility is the biggest conversion blocker (enterprise, higher price point).
- **Problem/solution narrative**: scroll-driven sections walking through a pain point then the fix. Use for products solving a non-obvious problem that needs explaining before the pitch lands.
- Common failure: stacking 6+ generic feature cards with icon + heading + one line, identical structure repeated — the text-wall tell. Apply the show-don't-tell table above: convert feature cards into feature *mockups*, vary rhythm (a full-width visual, an alternating two-column showing the feature in use, a comparison table, a real chart) so the page is a sequence of things to look at, not a stack of paragraphs.

## Dashboard
- Lead with the one number/status the user opens the app to check — don't bury it below navigation chrome.
- Group related metrics; don't scatter unrelated KPIs in one uniform grid just because a grid is easy to build.
- Empty and loading states matter as much as the populated state — design them explicitly, don't leave them as an afterthought default.

## Pricing
- 3 tiers is the safe default (2 feels thin, 4+ causes decision paralysis) unless the product genuinely needs more.
- Highlight one tier visually (border, subtle background shift) — don't rely on a "Most Popular" ribbon alone to do that work.
- Put the annual/monthly toggle and the actual price close together; don't make users hunt for what a plan costs.

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
