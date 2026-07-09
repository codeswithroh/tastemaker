# Starter style scaffolding (cold start, no references given)

Use this only when the user has no references to ground on. Treat every entry as a starting point to adapt after asking 1-2 quick questions (industry + mood), not a catalog to apply unchanged — picking #3 verbatim because it's third in a list is exactly the genericness this skill exists to avoid.

## Mood → direction

**Premium / confident** (fintech, B2B SaaS, professional tools)
- Palette: near-black or deep navy surface, one restrained accent (never more than one saturated color), generous negative space
- Type: a single geometric or grotesque sans (Inter, Söhne-alikes, General Sans), tight tracking on headings
- Shape: flat or hairline-bordered, minimal shadow, sharp-to-moderate radius (4-8px)
- Avoid: gradients as a crutch, multiple accent colors, drop shadows for depth

**Warm / approachable** (consumer, community, wellness)
- Palette: warm neutrals (cream, sand) with one soft accent (terracotta, sage, dusty blue) — desaturated, not candy-bright
- Type: a humanist sans or a serif for headings paired with a plain sans body
- Shape: larger radius (12-20px), soft shadows acceptable, illustration-friendly
- Avoid: corporate blue, harsh contrast, overly saturated primaries

**Technical / builder-facing** (dev tools, infra, CLI-adjacent products)
- Palette: dark mode by default, monochrome base, a single high-contrast accent used sparingly (terminal green, electric blue)
- Type: monospace accents for code/data, a plain sans for prose
- Shape: sharp corners or none, visible grid/borders over shadows
- Avoid: playful illustration, rounded-full buttons, pastel colors

**Playful / consumer social** (games, creator tools, youth-oriented)
- Palette: higher saturation permitted, 2-3 colors in active rotation, high contrast
- Type: rounded or display-leaning headings, plain sans body for legibility
- Shape: large radius, layered shadows/depth acceptable, motion-friendly
- Avoid: making everything loud at once — even playful UI needs a quiet base to pop against

## Type pairing starting points
- Inter (body) + a heavier weight of Inter or a geometric display face for headings — safe, works almost everywhere
- A serif (Fraunces, Lora) for headings + Inter/system sans for body — warm/editorial feel
- IBM Plex Sans + IBM Plex Mono for accents — technical/builder feel, cohesive family

## Spacing & radius baseline
- 8px base grid unless the mood calls for tighter (dense dashboards: 4px) or looser (editorial/marketing: sometimes 12px)
- Pick one radius scale and stick to it project-wide (e.g. 4/8/16px for sm/md/lg) — mixing arbitrary radius values across components is a fast way to look unintentional

## Contrast floor
Whatever palette gets chosen, verify body text against its background hits at least 4.5:1 (WCAG AA). This is non-negotiable regardless of mood — a beautiful palette that fails contrast just looks broken, not stylish.
