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

Re-verified 2026-08-01 against the actual shipped hex values via `check_contrast.py` (the version below replaces an earlier draft that listed `bg/accent`/`surface/accent` as text-safe without having actually run the numbers — they measure 2.51 and 2.72, both decorative. Accent only clears the text-safe floor against the dark surface, not the paper background.).

- Text-safe (>=4.5): dark/on-primary (18.65), text/on-primary (18.20), surface/dark (17.94), surface/text (17.50), dark/on-dark (16.74), bg/dark (16.55), text/on-dark (16.33), bg/text (16.15), muted/on-primary (9.05), surface/muted (8.70), muted/on-dark (8.12), bg/muted (8.03), dark/accent (6.60), text/accent (6.44), primary/on-primary (4.63)
- UI-safe (>=3.0 and <4.5): surface/primary (4.45), on-dark/primary (4.15), bg/primary (4.11), dark/primary (4.03), text/primary (3.93), muted/accent (3.20)
- Decorative (<3.0): accent/on-primary, surface/accent, on-dark/accent, bg/accent, dark/muted, text/muted, muted/primary, primary/accent, bg/on-primary, on-dark/on-primary, bg/surface, surface/on-dark, surface/on-primary, dark/text, bg/on-dark

Practical read: accent (orchid) is only usable as *text* against the dark surface or the light-page text/muted colors — never directly on `bg` or `surface`. On light panels, use accent for borders/icons/decorative accents, not body text.

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
- Macrostructure(s) used: homepage uses Feature Stack (editorial variant), replacing the prior Editorial Artifact Gallery; the proof page remains a live before/after comparison.
- Narrative arc per page (2026-08-01 rebuild): hook (single real product visual, no collage) -> proof-strip (real file/link wall) -> problem (every agent defaults to the same page) -> how-it-works (6 real capability checks) -> proof (real, re-verified contrast matrix + link to full comparison) -> range (4-up mode grid) -> memory (pinned ledger) -> close (install panel).
- Shared chrome: preserved Tastemaker mark, split floating nav islands, final masthead footer.
- Per-page body archetypes: single-visual hero, file proof wall, tell-card problem grid, 6-card capability grid, contrast-matrix proof rows, clean 4-up mode grid, 3-card memory ledger, dark install panel.
- Rebuild reason: the prior Editorial Artifact Gallery (and its 4 predecessor iterations, all built on absolute-positioned collage sections) produced clipped headlines and cluttered/overlapping hero artifacts at multiple breakpoints — verified via Playwright, not just visual inspection. This rebuild replaces every absolute-positioned collage with CSS grid/flex, verified to produce zero horizontal overflow at desktop/tablet/mobile.
- Build stamp / log: `.tastemaker/log.json` carries structural history; CSS stamp at the top of `site/styles.css` records this Feature Stack rebuild.

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

## Illustration style (web/ React app, 2026-08-22)

Eight custom illustrations (`web/public/assets/illustrations/`) replaced the terminal-chrome
visual language as the primary storytelling device — one per major section, each mapping
1:1 onto that section's real argument (hero: transformation; problem: the identical-output
assembly line; how-it-works: the literal 6-step workflow; proof: measuring, not eyeballing;
modes: four outfits for four registers; memory: rejected-pile to organized-archive; install:
developer plus mascot). Source files live in `~/Documents/Tastemaker/design/assets/illustrations/`.

**Reusable generation prompt** — append this to any prompt generating a new illustration for
this project, so future additions match the existing eight instead of drifting:

> Vintage editorial hand-drawn illustration, inspired by mid-century magazine spot
> illustrations and old technical editorial cartoons. Thin imperfect black ink lines, loose
> confident pen strokes, subtle hand-drawn wobble, charming human proportions, minimal
> cross-hatching, very sparse detail, clever visual metaphor, whimsical but sophisticated,
> modern technology represented through simple physical metaphors. Mostly black ink with a
> very small amount of muted golden-yellow accent color. No gradients, no 3D, no glossy
> effects, no photorealism, no vector-perfect geometry, no thick cartoon outlines, no anime
> style, no corporate stock illustration style, no AI-generated aesthetic. No text, no
> letters, no labels, no UI text. Isolated composition with generous negative space.
> Transparent PNG background, true alpha transparency, absolutely no white, cream, beige, or
> colored rectangular background.

**Real gap found applying this:** the prompt's own "muted golden-yellow" didn't hold in the
actual output — the illustrations' baked-in gold samples at `#fab832` (verified by direct
pixel sampling, not eyeballing), which measures 1.56:1 against the site's paper background
(`#f4f1eb`) — nowhere near text-safe. For any *typography* echoing this gold (not the
illustrations themselves, which are a fixed asset), use `--gold: #8b5e03` instead — same hue,
darkened until `check_contrast.py` cleared 4.5:1 (measures 5.03:1). The illustrations stay
untouched; only text color pulls double duty as "goldish" safely.

**Handwritten accent**: Caveat (`--font-hand`, Google Font "Caveat") on one emphasized
phrase per major headline, sized ~1.15em relative to the surrounding bold sans since script
faces read lighter at equal font-size. Never for body copy, labels, or anything read at a
glance — matches the mid-century-editorial brief's "whimsical but sophisticated," not a
children's-cartoon voice.

**Framing rule**: four of the eight illustrations (hero, proof, memory, install) came back
with a dark vignette baked into the source image rather than true alpha transparency, despite
the prompt requesting it. On the site's light background those need a rounded-card wrapper
with a soft shadow so they read as an intentional framed piece rather than a stray dark
rectangle; the other four (problem, how-it-works, modes, and the alt install) are genuinely
transparent and sit borderless. Check each new illustration for this before placing it.
