# Style lock — Tastemaker marketing site

Established: 2026-07-21. Source: Tastemaker technical/builder mood, generated with `scripts/generate_palette.py --mood technical --mode dark --seed 20260721` and adapted around the existing product identity.

## Palette
- Background: #F4F1EB (role: tactile paper page background)
- Surface: #FFFAF1 (role: light editorial panels)
- Dark surface: #0C1414 (role: technical proof bands and command surfaces)
- Primary: #008286 (role: primary actions and execution states)
- Accent: #BE85CE (role: judgment, taste, links, and highlights)
- Text primary: #171514 (role: light-page text)
- Text muted: #4D4842 (role: light-page secondary copy)
- On-dark text: #E5F6F6 (role: dark-band text)
- Button label color: #FFFFFF (role: dark and teal actions)
- Border: rgba(23, 21, 20, .12) (role: light paper hairlines)
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
- Macrostructure(s) used: homepage uses Editorial Artifact Gallery; the proof page remains a live before/after comparison.
- Narrative arc per page: homepage hook(real proof-collage hero) -> proof(repo-file wall) -> compatibility(agent/file scene) -> problem(anti-slop poster) -> premium range(mode runway) -> solution(capability shelf) -> memory(pinned ledger) -> demos(proof gallery) -> close(tactile install panel).
- Shared chrome: preserved Tastemaker mark, split floating nav islands, final masthead footer.
- Per-page body archetypes: homepage H2 proof-collage hero, file proof wall, agent compatibility scene, typographic poster statement, premium mode runway, asymmetric capability shelf with print stack, pinned memory ledger, large proof gallery, tactile still-life command close.
- Build stamp / log: `.tastemaker/log.json` carries structural history; CSS stamp records this artifact-gallery revamp.

## Reference intelligence
- Reference board: `.tastemaker/reference-board.md` viewed sources
- Design read: homepage for builders comparing AI coding tools, mode Persuade, with a technical proof-lab language
- Dials: variance 8, motion 7, density 5, art direction 9
- Foundation: static HTML/CSS/JS in the existing site stack; no new dependency required
- Quality bar: v0 for artifact-led AI builder framing; Cursor for live-feeling product proof; Linear for restrained hierarchy; Framer for visual-output proof; 21st.dev for builder-community credibility
- Direction contract: Thesis Tastemaker is the taste layer for coding agents; First viewport product name, install command, and layered collage; System tactile paper sections, dark proof bands, orchid taste signals, teal execution states, screenshots, visible motion, and memory files; Risk over-copying Taste Skill, solved by borrowing section roles while preserving Tastemaker identity
- Anti-references: generic AI gradient hero, fake chrome, feature-card text walls, repeated numbered eyebrows, invented proof, dense proof-lab card wall, tiny card headers, dark-only administrative proof board

## Mood descriptors
technical, discerning, alive, exact

## Assets
- Anchor asset: `site/assets/mark-tastemaker.svg` — the established layered-swatch Tastemaker brand mark already used across distribution channels
- Asset style: custom SVG orchestration artwork, layered proof screenshots, mode-gallery screenshots, paper notes, minimal utility icons only where the interaction needs them
- Asset cast: hero anchor `launch-poster.png`; mode range `minimalist.jpg`, `soft-calm.jpg`, `glassmorphic.jpg`, `brutalist.jpg`; process artifacts `style-lock.md`, `decisions.log`, `reference-board.md`, `asset-cast.md`; proof `before-after-poster.png` and `capabilities-section.png`; texture object custom still-life; micro assets swatches, notes, file cards, and command chips
- Illustration vs. photography split: abstract concept sections use the custom `site/assets/art/taste-orchestration.svg`; proof/demo sections use real local screenshots; no factual physical section requires photography
- Illustration source used: hand-built SVG in the repo, not stock artwork
- Logo: `site/assets/mark-tastemaker.svg` — preserve this exact established logo and do not replace or recolor it; wordmark uses Archivo
- Rejected asset pattern: do not let one Product Hunt poster family carry hero, proof, demo, and close at the same time; each major section needs a distinct asset role

## Motion
- Feel: visible, editorial, precise, and narrative
- Entrance duration/distance: 320-640ms, 12-30px rise depending on visual weight
- Easing: power3.out
- Story motion: GSAP hero collage assembly, scroll-tied asset curation board, mode runway drift, pinned memory ledger, reveal groups, demo parallax, and still-life drift, all reduced-motion aware

## Do not
- Never replace or reinterpret the established `site/assets/mark-tastemaker.svg` logo
- No indigo-to-purple hero gradient
- No repeated pill eyebrow on every section
- No emoji icons
- No long body copy in monospace
- No feature claim without a visual proof beside it
