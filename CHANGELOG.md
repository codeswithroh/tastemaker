# Changelog

This file is a condensed, version-anchored summary. The **canonical, detailed, per-PR record is [site/changelog.html](https://tastemaker-skill.online/changelog.html)**, where every entry links to the real merged pull request. This file exists because that's where GitHub itself, and anyone browsing the repo rather than the site, expects to find it. The two are kept consistent by hand; if they ever disagree, the site's PR-linked entries are the source of truth.

This is the first version cut for the project, and there's no prior tagged history to diff against, so `1.0.0` below summarizes everything shipped to date, not just what changed since a previous release.

## [1.0.0] - 2026-07-26

**A production-ready core.** The generative engine (palette generation with a verified contrast contract, a structure/diversification system that enforces real page-to-page variety, a numbered anti-slop gate list, and the `study`/`audit` verbs) is stable and has been exercised across many real builds, not just written and left untested. `1.0.0` reflects that maturity, not a promise that nothing will ever change again.

Highlights, newest work first (full detail: [site/changelog.html](https://tastemaker-skill.online/changelog.html)):

- **Narrative-arc discipline, headline-sizing ceilings, and a proof-section density floor.** Three fixes shipped in response to real critique of a generated site, closing gaps in storytelling, type scale, and visual weight.
- **anime.js evaluated and scoped-adopted** for SVG motion-path/shape-morphing only, based on measured bundle sizes and hands-on browser testing. GSAP remains the default motion engine everywhere else.
- **Registered as a Claude Code plugin marketplace**, restructuring the skill under `skills/tastemaker/`, and fixed `npx skills add` compatibility.
- **Closed the structural gap** against the strongest comparable anti-slop skill in the field: named macrostructures, a component catalog, a project-memory diversification engine, a numbered mood-scoped gate list with pre-emit self-critique, and the `study`/`audit` verbs.
- **Real section spacing**, measured via DOM introspection against a named reference rather than guessed, replacing an under-generous fixed scale.
- **The palette generator replaces five fixed presets**: a fresh, contrast-verified palette every run instead of a swatch library.
- **The contrast contract**: a real, checkable color-pairing system (`scripts/check_contrast.py --matrix`), not just a body-text-on-background check.
- Sponsorship support, a real app-shell layout pattern, non-Latin typography, runtime dark/light toggling, and the initial marketing site and demo.

## Versioning going forward

No breaking changes have shipped or are currently planned. If one ever does, this file is where it gets documented along with the migration path, a habit that starts now, before it's actually needed.
