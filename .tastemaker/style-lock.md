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

## Structure
- Macrostructure(s) used: homepage uses Product Demo / Workbench plus Bento Showcase; the proof page remains a live before/after comparison.
- Narrative arc per page: homepage hook(Product Demo hero) -> problem(anti-default positioning) -> solution(capability console) -> how(workflow rail) -> proof(live before/after + scanner receipts) -> close(install).
- Shared chrome: preserved Tastemaker mark, compact product nav, final masthead footer.
- Per-page body archetypes: homepage H2 split demo with artifact console, F2 capability bento, F5 annotated receipt panels, C2 install close.
- Build stamp / log: `.tastemaker/log.json` carries structural history; CSS stamp records this revamp.

## Reference intelligence
- Reference board: `.tastemaker/reference-board.md` viewed sources
- Design read: homepage for builders comparing AI coding tools, mode Persuade, with a technical proof-lab language
- Dials: variance 8, motion 7, density 5, art direction 9
- Foundation: static HTML/CSS/JS in the existing site stack; no new dependency required
- Quality bar: v0 for artifact-led AI builder framing; Cursor for live-feeling product proof; Linear for restrained hierarchy; Framer for visual-output proof; 21st.dev for builder-community credibility
- Direction contract: Thesis Tastemaker is a local design operating system for agents; First viewport product name, install command, and capability console; System dark technical surface, orchid taste signals, teal execution states, screenshots, scanner findings, and memory files; Risk detail overload, solved by keeping the hero focused and moving receipts below the fold
- Anti-references: generic AI gradient hero, fake chrome, feature-card text walls, repeated numbered eyebrows, invented proof

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
