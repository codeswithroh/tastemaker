# `.tastemaker/style-lock.md` format

This file is the single source of truth for a project's visual style once established. Every later request in the project should read tokens from here rather than re-deriving them — that's what prevents the second screen from drifting away from the first.

Write it in this shape (adapt fields, don't pad with values you didn't actually derive):

```markdown
# Style lock — <project name>

Established: <date>. Source: <"reference images: list them" | "starter scaffolding + user answers" | "user-specified">

## Palette
- Background: #hex (role: e.g. "page background")
- Surface: #hex (role: e.g. "cards/panels")
- Primary: #hex (role: e.g. "primary actions, links")
- Accent: #hex (role: e.g. "sparingly, for emphasis only")
- Text primary: #hex — contrast vs background: X.XX (WCAG AA pass/fail, from `scripts/check_contrast.py`)
- Text muted: #hex
- Button label color: <"white" | "text primary"> — contrast vs Primary: X.XX (from `scripts/check_contrast.py`; don't assume white without checking, see `references/style-tokens.md`'s Contrast floor section for why)
- Dark mode: <"not needed for this project — single mode only" | "companion palette provided, author-time choice only, no runtime switch" | "runtime toggle — both modes ship, user-switchable"> — if either dark-mode case applies, give the companion palette (same roles/format as above) and confirm it independently re-verifies against the dark background, don't assume a light-mode color carries over. If it's the runtime-toggle case, see `references/style-tokens.md`'s Runtime dark/light toggle section: the companion pair must come from the same `generate_palette.py --seed` run in both `--mode light` and `--mode dark` (not two unrelated palettes that merely share a mood), and both role sets need their own passing `check_contrast.py --matrix` before the lock counts as verified.

## Color contract

The palette above is not a set of five approved hexes the model may combine freely. It is a contract: for each pairing of colors, a required contrast ratio. This is what stops the palette from passing at authoring time and then failing the first time the model uses two of its colors in a pairing you never listed (a badge fill with a white label, a disabled state, a hover). Record the contract, not just the colors.

Required ratios by pairing:

| Foreground on background | Floor | Why |
|---|---|---|
| body/muted text on bg or surface | 4.5:1 | WCAG AA text |
| button label on its fill (Primary, or any color used as a solid fill) | 4.5:1 | text on a fill |
| link/accent used as text | 4.5:1 | text |
| a fill vs the page (does the button/badge show up at all) | 3:1 | UI component (1.4.11) |
| accent used as a highlight or icon | 3:1 | graphical object |
| a border that conveys state (focus ring, error/active edge, the only boundary between two regions) | 3:1 | UI component. A purely decorative hairline is exempt: record it as decorative. |

Legal pairings (run `scripts/check_contrast.py --matrix text=.. bg=.. surface=.. primary=.. accent=.. border=.. on-primary=..` and paste the summary):

- Text-safe (>=4.5): <list the pairings the matrix cleared for text/labels>
- UI-safe (>=3.0 and <4.5): <the pairings usable for large text, icons, and state-carrying borders>
- Decorative (<3.0): <the pairings that must never carry text or be the only thing conveying state>

The model may only compose color pairings that appear in the text-safe or UI-safe lists (matched to the pairing's purpose). If it needs a pairing that lands in Decorative for a purpose that requires more (a fill that needs a readable label, a border that must convey state), that is a flag: switch to a legal pairing, or darken/lighten a color and re-run the matrix. Do not ship the failing pairing. **Re-run the matrix whenever the palette grows** (a new semantic color, a locked hex used in a new role). The lock is only true for the tokens the matrix last covered. See `SKILL.md` Step 4's non-negotiable #5 for the ordered failure path (reuse a legal pairing → nudge lightness within the hue family → fall back to a known-safe neutral → surface a genuine conflict to the user) — don't just retry the same failing value.

If a token's value was adjusted mid-build to clear a pairing it originally failed (a lightness nudge per that failure path), note it here — e.g. "Accent nudged from #xxxxxx to #yyyyyy to clear UI-safe against Surface" — so a later session in this project sees the final value already reflects a contrast fix, not an arbitrary change.

## Typography
- Display/heading font: <name> — <why: e.g. "matches reference's geometric sans">
- Body font: <name>
- Scale: <e.g. "1.25 ratio, base 16px">
- <For a non-Latin-script project (Korean, CJK), this section records one family across a weight scale instead of two families — see `references/style-tokens.md`'s Non-Latin script typography section. Replace the two lines above with: "Family: <name> (e.g. Pretendard) — Heading: <weight>, Body: <weight>, UI chrome: <weight>." Also record letter-spacing and word-break decisions here (e.g. "letter-spacing: 0, word-break: keep-all for headings/UI text") since the Latin defaults elsewhere in this lock don't apply.>

## Shape language
- Corner radius: <value(s) and where each is used>
- Shadow depth: <e.g. "flat, no shadow" | "soft, 2-4px blur" | "hard drop shadow, brutalist">
- Border usage: <e.g. "1px hairline borders instead of shadows for separation">

## Density & spacing
See `references/style-tokens.md`'s Spacing scale section for the token set and the internal ≤ external rule this records.
- Base unit: 4px (the scale's foundation; name the specific tokens actually in use below, don't just restate this)
- Section padding: <the one token chosen for this project's section top/bottom padding, e.g. "space-16 (64px)">
- Content card internal padding: <the token used as the floor for feature/pricing/testimonial cards, e.g. "space-6 (24px)">
- Compact/dense card internal padding: <the token used for stat tiles, nav rows, app-shell list items, e.g. "space-3 (12px)" — only if the project has this context>
- Showcase/hero card internal padding: <the token used for the one highest-weight card in the layout, e.g. "space-8 (32px)">
- Overall density: <e.g. "generous whitespace, editorial" | "dense, information-heavy">
- Section separation: <"alternating surface tint" | "hairline divider" | "fixed section padding, no tint/divider" — see `references/component-patterns.md`'s Section-to-section separation section; apply the same choice at every section boundary in the project>

## Structure
The whole-page composition, recorded so a multi-page project stays coherent and so later builds can rotate against what's been done — see `references/macrostructures.md`, `references/component-catalog.md`, and `references/diversification.md`. Omit for app-shell-only projects (their shape is the sidebar+topbar frame in `references/component-patterns.md`).
- Macrostructure(s) used: <the named page shape(s) this project's marketing pages use, e.g. "landing: Feature Stack; about: Editorial Index">
- Shared chrome (stays consistent across the project's pages): <nav archetype + footer archetype, e.g. "Nav N2 balanced product bar; Footer Ft1 masthead">
- Per-page body archetypes: <the hero/feature/proof/CTA picks per page, e.g. "landing: H2 split-demo · F1 bands · P1 logo-wall · C2 statement">
- Build stamp / log: <note that `.tastemaker/log.json` carries the per-build record; the CSS stamp format is in `references/diversification.md`>

## Navigation chrome
Only for projects with an app shell (sidebar plus topbar) — see `references/component-patterns.md`'s App shell section. Omit this whole section for marketing-only projects.
- Sidebar background: <role, e.g. "Surface"> · Content area background: <role, e.g. "Background">
- Active nav item treatment: <e.g. "Primary-filled pill" | "transparent row, 3px Primary left-border">
- Inactive hover treatment: <e.g. "Surface-on-Surface shift, 8% lighter">
- Breadcrumb treatment: <e.g. "Text muted for parents, Text primary for current segment">
- Shell density: <e.g. "36px row height, 13px body type" — per `references/style-tokens.md`'s dense/information-heavy guidance, distinct from the marketing-page spacing above>

## Mood descriptors
2-4 words that capture the intent, e.g. "quiet, confident, technical" — useful as a quick gut-check when reviewing new output ("does this still feel quiet and confident?").

## Assets
- Anchor asset: <path> — everything else should visually match this
- Asset style: <e.g. "outline icons, 1.5px stroke, rounded caps" | "flat geometric illustrations, palette-matched">
- Illustration vs. photography split: <e.g. "ideagram/unDraw illustrations for mission/values/team personality; real Pixabay photography for office/location sections">
- Illustration source used: <"matched from populated ~/.ideagram/undraw/ library" | "ideagram/assets/primitives fallback — no library available, quality tradeoff noted to user"> — so a later session in this project knows without re-checking
- Logo: <path to mark/mark+wordmark SVG> — <symbol source, e.g. "logoyoyo.com blob mark, recolored to accent"> + <heading font used for wordmark>

## Motion
- Feel: <e.g. "quick and restrained" | "soft and slightly bouncy" — should match the mood descriptors above>
- Entrance duration/distance: <e.g. "220ms, 12px rise" — see references/animation-guidelines.md defaults if unset>
- Easing: <e.g. "ease-out" | "cubic-bezier(0.16, 1, 0.3, 1)">

## Do not
Concrete things to avoid for this project specifically, if any came up during curation (e.g. "no gradients — user rejected twice", "avoid rounded-full buttons, feels too playful for this brand").
```

Keep it factual and specific. A style lock that just restates generic advice ("use clean typography, good contrast") isn't doing its job — every line should be something a different project might plausibly do differently.
