# Non-Latin script typography isn't a font swap — it changes the model

## The question

An early tester building Korean-language internal apps hit a real wall: tastemaker's whole type system — the mood table, display/body font pairing, tightened display line-height, tight heading tracking — is a Latin-typography model, and nothing in the skill said so. Would just substituting a Korean font into the existing Latin rules actually produce good Korean typography, or is that a category error?

## The method

Researched rather than guessed, and cross-checked against independent sources rather than trusting one:

- Pretendard's actual license (SIL OFL), weight range (100–900, variable font), and CDN loading pattern — verified from its own README, and the exact CDN snippet was checked live (`curl -sI` returning 200), not copied from a possibly-stale example.
- Hangul letter-spacing and word-breaking conventions, cross-checked against three independent references: Typotheque's CJK typesetting guide, SymbolFYI's CJK web typography guide, and the W3C's Hangul text layout requirements (klreq).

## The finding

A non-Latin script isn't a font substitution inside the same typographic model — it changes the model itself:

- **Single-family, not a display/body pairing.** The Latin two-family pairing convention doesn't carry over cleanly; a single family across a weight scale (e.g. Pretendard: light for body, semibold/bold for headings) is the more idiomatic approach for Korean.
- **Latin's negative-tracking instinct actively hurts Hangul.** Tightened letter-spacing on display type is a real, verified win for Latin display headlines (see the line-height/tracking guidance elsewhere in the skill) — but Hangul syllable blocks are pre-composed square units, and negative tracking that reads as "confident and tight" in Latin reads as cramped and harder to parse in Hangul.
- **`word-break: keep-all` as the default for Korean UI text**, not the Latin `overflow-wrap: anywhere` default — Korean word-breaking conventions differ from Latin's, and applying the Latin default breaks words at the wrong points.
- **Looser line-height than the Latin display floor.** The skill's Latin display-headline line-height floor (documented alongside the descender-clipping fix) doesn't directly transfer — Hangul needs more vertical breathing room even at large display sizes.
- **Mixed Latin+CJK text needs distinct optical sizing.** Product names, numerals, and deliberately-Latin strings inside otherwise-Korean copy commonly need different optical sizing than the surrounding CJK text at the same nominal font-size, since Latin glyphs read smaller next to CJK glyphs at an identical point size — a real, documented CJK-typesetting concern, not a hunch.

The research was explicit about its own limits: the guidance is Korean-*tested*, with Japanese and Chinese noted as reasonable but less-verified starting points from the same family of conventions, not claimed with the same confidence.

## What it changed

- `references/style-tokens.md` gained a "Non-Latin script typography (CJK, Korean specifically)" section covering the single-family model, Pretendard as the concrete, live-verified Korean starting point, the tracking/line-height/word-break differences from the Latin defaults, and the mixed-script optical-sizing note.
- Added an explicit script check early in the build flow (right after the mood-selection step), so a non-Latin project routes to the right typographic model from the start rather than defaulting to Latin conventions and needing a later correction.
- `references/style-lock-format.md` gained a note for recording the single-family model when a project uses it, instead of forcing the two-family Latin template onto a lock that doesn't fit it.

Shipped in [#39](https://github.com/codeswithroh/tastemaker/pull/39), closing [#2](https://github.com/codeswithroh/tastemaker/issues/2).
