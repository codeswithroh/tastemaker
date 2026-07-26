# The contrast check certifies the palette as authored, not as used

## The question

tastemaker shipped `scripts/check_contrast.py` and five fixed, pre-verified palette presets — each one checked and passing. Was that actually a durable guarantee, or did it only hold for the specific combinations someone thought to test at authoring time?

## The method

Not a solo investigation — this one came from independent design review, and the finding is worth recording precisely because multiple reviewers converged on the same root cause without coordinating, which is a stronger signal than any single critique.

## The finding

> Contrast ratio is pairwise: text-on-background, border-on-fill, disabled-on-surface. A preset that passes for your locked heading-on-hero can still fail the moment the model uses one of your palette colors as a badge background with white text, which it will, because you handed it a palette and no contract for how each color gets used. You checked the combinations you designed; the AI improvises combinations you didn't.

The check as it existed ran once, against the pairings someone happened to enumerate when the preset was written. Nothing re-fired it when the model later invented a new pairing — a palette color used as a fill with white text it had never been tested against, say. The five presets passed *the day they were authored*. Whether they kept passing depended entirely on the model never composing a pairing outside that original test set, which was never a safe assumption:

> The lock is also a write-time artifact in time. The day someone adds a semantic color, or uses a locked hex in a pairing the original run never listed, the lock still reports green while the new combination fails, because nothing re-fires the check on the extension. The lock certifies the palette as authored, not the palette as used. So the reusable thing you built is not the locked system, it is the runnable check. The value holds only as long as the check keeps firing every time the system grows past what it originally covered.

A third reviewer flagged the necessary follow-up question — not just "does it check," but "what happens when the check fails":

> The one thing I'd watch with the iterate-until-it-passes approach is how it fails. When the model can't satisfy the check, does it degrade the design gracefully or just keep flailing on the same pairing? That's usually where the interesting bugs hide.

## What it changed

This reframed the whole feature. The durable artifact was never the five pre-verified presets — it was the checker itself, made to run continuously rather than once:

- The palette generator (`scripts/generate_palette.py`) replaced the five fixed presets entirely, producing a fresh palette every run, solved against the contrast contract at generation time rather than pre-verified once and reused.
- `scripts/check_contrast.py` gained a `--matrix` mode, checking every real pairing a build introduces (a badge fill with its label, a disabled state, a hover, a state-carrying border), not just body-text-on-background.
- The style-lock format gained a **Color contract** section: required ratios by pairing purpose (text vs. UI-component vs. decorative), a legal-pairings list the model may compose from, and a re-run requirement whenever the palette grows a new semantic color or reuses a locked hex in a new role.
- An explicit, ordered failure path was defined for when a pairing fails its ratio — reuse a legal pairing, nudge lightness within the same hue family, fall back to a known-safe neutral, or surface a genuine conflict to the user — so a failing check has a defined next step instead of looping on the same pairing or silently shipping it.

Shipped starting in [#16](https://github.com/codeswithroh/tastemaker/pull/16) (the contrast contract) and [#18](https://github.com/codeswithroh/tastemaker/pull/18) (the palette generator that made the contract continuously enforceable instead of a one-time check).
