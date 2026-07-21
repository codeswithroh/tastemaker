# Style lock — Tastemaker marketing site

Established: 2026-07-21. Source: Tastemaker technical/builder mood, generated with `scripts/generate_palette.py --mood technical --mode dark --seed 20260721` and adapted around the existing product identity.

## Palette
- Background: #0C1414 (role: page background)
- Surface: #171F1F (role: panels and product mockups)
- Primary: #008286 (role: primary actions and execution states)
- Accent: #BE85CE (role: judgment, taste, links, and highlights)
- Text primary: #E5F6F6 — contrast vs background: 16.74 (WCAG AA pass)
- Text muted: #A8BABA — contrast vs background: 9.24; vs surface: 8.30 (WCAG AA pass)
- Button label color: #FFFFFF — contrast vs Primary: 4.63 (WCAG AA pass)
- Border: #232B2C (role: decorative panel boundaries)
- Dark mode: native palette; no companion mode required

## Color contract

- Text-safe (>=4.5): bg/on-primary, surface/on-primary, text/bg, text/surface, border/on-primary, text/border, bg/accent, surface/accent, accent/border, primary/on-primary, muted/bg, muted/surface
- UI-safe (>=3.0 and <4.5): text/primary, bg/primary, surface/primary, primary/border
- Decorative (<3.0): accent/on-primary, text/accent, primary/accent, bg/border, surface/border, text/on-primary, bg/surface

## Typography
- Display/heading font: Archivo — direct, condensed enough for high-impact builder language
- Body font: IBM Plex Sans — readable and neutral beside technical UI
- Data/code font: IBM Plex Mono — reserved for commands, file trees, ratios, and state labels
- Scale: fluid clamp-based display scale with 16px body base

## Shape language
- Corner radius: 6px controls, 12px panels, 20px major stages
- Shadow depth: flat surfaces; depth comes from overlap and crisp borders
- Border usage: 1px decorative hairlines, with color-plus-label for meaningful states

## Density & spacing
- Base spacing unit: 8px
- Overall density: editorial landing page with information-rich product demonstrations

## Mood descriptors
technical, discerning, alive, exact

## Assets
- Anchor asset: `site/assets/mark-tastemaker.svg` — the established layered-swatch Tastemaker brand mark already used across distribution channels
- Asset style: Lucide line icons, 2px stroke, orchid tint; code-native product UI mockups
- Illustration vs. photography split: product UI mockups carry every feature explanation; no factual physical section requires photography and no redistributed illustration is used
- Illustration source used: not applicable; local unDraw assets were deliberately not redistributed into the public repository
- Logo: `site/assets/mark-tastemaker.svg` — preserve this exact established logo and do not replace or recolor it; wordmark uses Archivo

## Motion
- Feel: quick, precise, and state-driven
- Entrance duration/distance: 420ms, 18px rise
- Easing: power3.out

## Do not
- Never replace or reinterpret the established `site/assets/mark-tastemaker.svg` logo
- No indigo-to-purple hero gradient
- No repeated pill eyebrow on every section
- No emoji icons
- No long body copy in monospace
- No feature claim without a visual proof beside it
