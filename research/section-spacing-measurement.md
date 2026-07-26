# Real section spacing, measured — not guessed

## The question

Generated landing pages were reading as cramped, with no section getting the visual weight it deserved. The obvious response — "just increase the padding" — isn't research, it's a guess with a plausible-sounding justification. The actual question: what does a real, well-regarded premium page's section spacing look like, in real numbers?

## The method

Studied [make.design](https://make.design/) as a named reference and measured its actual section spacing via DOM introspection — reading real computed padding/gap values off the live page, not eyeballing a screenshot and estimating.

## The finding

At a 1280px viewport:

- Individual section padding runs **64–192px per side**, not one flat value.
- Boundary gaps between adjacent sections average **~165px**, ranging 112–248px.
- Separation comes from generous whitespace alone — most section backgrounds are transparent, not alternating tints doing the visual-separation work instead.
- Padding is deliberately **uneven by section weight**: a slim trust-bar section sits at ~68px combined padding, while the heaviest section reaches 320px combined — not one repeated number applied uniformly down the page.

## What this exposed

`references/style-tokens.md`'s spacing scale capped section padding at `space-24` (96px) as its "generous" ceiling, and instructed picking **one** value for the whole project. Both were directly contradicted by the measurement — the real reference runs up to double that ceiling for its most important sections, and varies the value by section weight rather than fixing it. This was a plausible, concrete explanation for why generated landing pages read as cramped even when they were technically "on the scale": the scale's own ceiling was set too low, based on assumption rather than measurement.

## What it changed

- Added `space-32`/`space-40`/`space-48` (128/160/192px) tokens to `references/style-tokens.md`.
- Rewrote the Section-level padding rule into a landing-page-specific, weight-tiered system: connective sections `space-12–16`, standard sections `space-16–24`, pivotal sections (hero, primary proof) `space-32–48`, with a target boundary gap of ~120–250px on desktop — explicitly scoped away from app shells, which keep their existing density guidance.
- Added a new anti-slop gate checking that section padding is actually generous and weight-tiered, distinct from the existing mechanism-consistency gate (a page can use one consistent separation *mechanism* and still fail this if that mechanism is applied at a cramped value everywhere).
- Updated the style-lock format to record per-role padding tiers instead of one flat token.

Shipped in [#48](https://github.com/codeswithroh/tastemaker/pull/48).
