# Narrative arc — why each section exists, not just what it looks like

Three files now govern a landing page, and they answer three different questions. `references/macrostructures.md` answers **what shape is the whole page**. `references/component-catalog.md` answers **what does each section look like**. This file answers **why does each section exist, and in what order** — the one question nothing answered before, and the gap that produces a page where every section is individually well-built but the page as a whole doesn't add up to an argument.

This is not a taste preference. It's grounded in real, established frameworks:

- **StoryBrand (SB7)** — the dominant framework in current landing-page copywriting practice: the customer is the hero, the brand is the guide. Seven parts: Character, Problem, Guide (empathy + authority), Plan, Call to Action, Failure (the stakes of not acting), Success (the transformation).
- **PAS** (Problem–Agitate–Solution) — a narrower copy-level pattern: name the pain, make its real consequences concrete, then present the fix.
- **The converged modern SaaS convention**: Hero → Problem → Solution → How it works → Social proof → CTA — cited consistently across current landing-page structure guidance, not invented for this file.

## The default arc

Six beats, adapted from StoryBrand/PAS into what a page actually builds:

1. **Hook** (the hero) — the promise, sized and scoped per `references/hero-guidelines.md`.
2. **Problem / stakes** — what's actually broken or at risk. Specific to *this* product, never generic ("teams struggle with X" is not a story beat — it's a placeholder for one). This is StoryBrand's Problem plus a dose of Failure: what happens if nothing changes.
3. **Solution / mechanism** — how the product actually solves it, *shown* per the show-don't-tell table in `references/component-patterns.md`, not just asserted. This is StoryBrand's Guide moment — the product demonstrates it understands the problem and has the authority to fix it.
4. **How it works** — the concrete steps or flow. StoryBrand's Plan: keep it simple, a handful of steps, not an exhaustive manual.
5. **Proof** — real evidence: logos, a testimonial, real numbers. Honest per the existing no-invented-metrics rule (`references/anti-slop-checklist.md` gate 45) — a fabricated proof beat is worse than no proof beat. Also has its own visual-density floor: a label + description + small icon in a bordered box is not enough to carry a proof beat — see `references/component-patterns.md`'s show-don't-tell section for the specific floor.
6. **Close / CTA** — the ask, tied back to the hook's promise. StoryBrand's Success: what the visitor's world looks like after they act.

## Mapping beats to archetypes (the arc picks the job; the catalog still picks the look)

| Beat | Typical archetypes (from `component-catalog.md`) | Notes |
|---|---|---|
| Hook | Any `H#` hero | Governed by `hero-guidelines.md`, not re-litigated here. |
| Problem / stakes | A section built from prose + a supporting visual (an `F#` band showing the *broken* state, a before/after), or folded into the hero's subhead for a short arc | Rarely needs its own dedicated archetype — often the shortest, sharpest beat on the page. Resist turning it into a wall of text just because it doesn't map to a named archetype. |
| Solution / mechanism | `F1` alternating bands, `F2` bento tiles, `F5` annotated capture | Pick per the show-don't-tell table — this beat exists specifically to *show* the fix. |
| How it works | `F4` numbered step sequence, `F3` spec sheet, `F6` spec sheet for technical detail | Keep it simple — 3-5 steps, not an exhaustive walkthrough. |
| Proof | `P1` logo wall, `P2` pull-quote, `P3` single quote, `P4` stat strip | Every number and quote real, per gate 45. |
| Close | `C1` inline form, `C2` statement + action, `C4` sticky bar | Echo the hook's actual promise, don't introduce a new pitch here. |

## Minimum section count: 4-5

Hook + Problem + Solution + Proof + Close is already five. **Never collapse below four distinct beats** — a page that goes straight from hook to proof to close skips the part that actually persuades (why this is a problem, how the product fixes it). Thinness here is exactly what real output was caught doing: a handful of sections stretched to fill a page, not a page built from enough real beats to carry an argument.

`How it works` is the one beat that can legitimately fold into `Solution` for a simple enough product — that's a deliberate merge, not an accidental omission (see below).

## Skipping or merging beats — deliberately, and say so

Not every product needs all six beats at full weight. A Manifesto macrostructure might spend most of its length on Problem/stakes with a single-line Solution and no separate How-it-works. A Stat-Led page might fold Proof into the hero itself. That's fine — **when it happens, it should be a stated choice tied to the macrostructure and the brief's actual argument, not a section that quietly never got built.** State which beats were merged or skipped and why, the same way macrostructure and archetype picks get stated out loud at Step 2.5.

## The self-check, before finalizing

The page, read top to bottom, should answer these questions in order:

1. Who is this for, and what's the promise? (Hook)
2. What's actually wrong, or at stake? (Problem)
3. How does this fix it? (Solution)
4. Why should I believe it? (Proof)
5. What do I do now? (Close)

If a section on the page doesn't serve one of these — or a deliberately stated variant, per the merging rule above — that's a gap in the arc, not just a design choice to shrug off. This is a distinct check from the diversification engine's structural-variety gates: a page can pass every structure gate (real macrostructure, varied archetypes, no generic template) and still fail this one, because variety and coherence are different properties. A page needs both.

## Recording the arc

State the beat sequence out loud at Step 2.5, alongside the macrostructure and archetype rotation: *"Arc: Hook (H2 split demo) → Problem (prose + before/after) → Solution (F1 bands) → How it works (F4 steps) → Proof (P4 stat strip) → Close (C2 statement). No beats skipped."* Note it in the build stamp the same way the structural picks are recorded (see `references/diversification.md`) so a later `audit` pass (per `references/verbs/audit.md`) can check the arc held together, not just that the structure varied.
