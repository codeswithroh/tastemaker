# Studying Hallmark: what a 15.7k-star anti-slop skill does that we didn't

## The question

tastemaker already varies **color** per project — a fresh, contrast-verified palette every run, never a fixed swatch. But was that the whole picture, or was there a structural gap hiding behind a good color story? The honest way to answer that is to study the strongest comparable tool in the field directly, not assume tastemaker's approach was already complete.

## The method

Studied [Nutlope/hallmark](https://github.com/Nutlope/hallmark) (15.7k stars, by Together AI) end to end: its 558-line router `SKILL.md`, ~90-file reference tree, 50-archetype component cookbook, 58-gate slop test, and token architecture — not a skim of its README, a real read of the mechanism.

## The finding

Hallmark's core mechanism is a **combinatorial catalog of named page shapes and component archetypes with stable IDs**, plus a **project-memory diversification engine** that forces each build to differ structurally from the last one. That's the thing tastemaker didn't have.

The gap it exposed: tastemaker's *structure* was monocultured even while its *color* wasn't. Every generated landing page reached for the same hero → three-feature-cards → CTA → footer rhythm. That's the strongest "an AI built this" tell at the page level, and it survives a perfect palette — two color-swaps of the same template still read as the same template.

## The honest head-to-head

Hallmark isn't strictly better across the board — the study was explicit about where each tool actually leads, not a one-sided "we were behind" writeup:

- **Where Hallmark led:** the structural-variety mechanism itself — named macrostructures, a component catalog with stable IDs and variation knobs, a project-memory rotation rule that actually enforces the variety rather than just suggesting it.
- **Where tastemaker already led, and kept:** the per-project generated palette + contrast contract (Hallmark ships fixed themes, not a generator), and a real-asset pipeline (Hallmark's component cookbook is typography-only with placeholders; tastemaker's archetypes are asset-forward — real mockups, charts, photos, illustrations).

## What it changed

Grafted Hallmark's structural machinery onto tastemaker's foundation, keeping the two axes where tastemaker already won:

- `references/macrostructures.md` — twelve named whole-page shapes (Feature Stack, Editorial Index, Long-Scroll Narrative, Bento Showcase, Stat-Led, Gallery Grid, Product Demo, Split Diptych, Conversational FAQ, Manifesto, Catalogue, Poster Fold), each with mood affinity and an honesty rule binding proof-led shapes to real evidence.
- `references/component-catalog.md` — named archetypes with stable IDs and variation knobs (Nav N1–N7, Hero H1–H6, Feature F1–F7, Proof P1–P4, CTA C1–C4, Footer Ft1–Ft6, Section-head S1–S4), routed per mood, plus cross-cutting rules (no fake chrome, one icon family per page, a banned eyebrow-left/heading-right section head).
- `references/diversification.md` — the project-memory engine: a `.tastemaker/log.json` schema, the rotation rule (macrostructure, nav, footer, and hero archetype must each differ from the last build), the "state it out loud" accountability step, and the CSS build stamp that records what a build actually chose. Palette is explicitly exempt from the rotation rule — it already varies by generation, so tastemaker's diversification is purely structural, a real simplification the generator earns versus Hallmark's multi-axis theme rotation.

This was phase 1 of a three-phase plan: the structural-variety engine (this study), followed by upgrading the anti-slop checklist into a numbered, mood-scoped gate list with a pre-emit self-critique pass, followed by the `study` and `audit` verbs.

Shipped in [#40](https://github.com/codeswithroh/tastemaker/pull/40), [#41](https://github.com/codeswithroh/tastemaker/pull/41), [#42](https://github.com/codeswithroh/tastemaker/pull/42).
