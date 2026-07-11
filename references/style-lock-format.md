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
- Dark mode: <"not needed for this project" | the companion palette (same roles/format as above) — see `references/style-tokens.md`'s per-preset Dark mode entries for the pattern: reuse a light-mode color only if it independently re-verifies against the dark background, don't assume it carries over>

## Typography
- Display/heading font: <name> — <why: e.g. "matches reference's geometric sans">
- Body font: <name>
- Scale: <e.g. "1.25 ratio, base 16px">

## Shape language
- Corner radius: <value(s) and where each is used>
- Shadow depth: <e.g. "flat, no shadow" | "soft, 2-4px blur" | "hard drop shadow, brutalist">
- Border usage: <e.g. "1px hairline borders instead of shadows for separation">

## Density & spacing
- Base spacing unit: <e.g. "8px grid">
- Overall density: <e.g. "generous whitespace, editorial" | "dense, information-heavy">

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
