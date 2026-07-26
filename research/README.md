# Research

Background writing that shaped tastemaker's rules — the actual investigation behind a fix, not a restatement of its PR description. Each writeup here answers a real question with a real method (something measured, read, or tested), states the finding, and links the PR that shipped the result.

This exists because a rule like "section padding should be generous" or "check contrast on every pairing, not just body text" is easy to state and easy to disagree with if there's no visible work behind it. These are the receipts.

- **[Real section spacing, measured — not guessed](section-spacing-measurement.md)** — DOM-measured a real reference page's actual padding numbers instead of eyeballing "more space," and found tastemaker's spacing ceiling was set roughly half of what a real premium page uses.
- **[Studying Hallmark: what a 15.7k-star anti-slop skill does that we didn't](hallmark-architecture-study.md)** — an end-to-end study of the strongest comparable tool in the field, including an honest account of where tastemaker already led and where it didn't.
- **[The contrast check certifies the palette as authored, not as used](contrast-as-authored-vs-as-used.md)** — why a pre-verified palette preset is a weaker guarantee than a check that re-fires on every pairing a build actually introduces.
- **[Non-Latin script typography isn't a font swap — it changes the model](non-latin-typography.md)** — Korean typography research (Pretendard, Hangul letter-spacing/word-break conventions) cross-checked against three independent sources, showing why substituting a Korean font into Latin typographic rules doesn't actually work.
