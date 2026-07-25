# Diversification engine — enforced structural variety across builds

Picking a named macrostructure and named archetypes (per `references/macrostructures.md` and `references/component-catalog.md`) only produces variety if the picks actually *change* build to build. Left to instinct, the model reaches for the same default shape every time — the generic hero → 3-feature-cards → CTA → footer — because that's the on-distribution attractor. This file is the mechanism that forces the pick to differ: a small project-memory file, a rotation rule, and a build stamp the next run reads.

**What this axis does and doesn't cover.** tastemaker already prevents *color* monoculture at the source: `scripts/generate_palette.py` produces a fresh, contrast-verified palette per project, so two projects never share a palette by construction. This engine is the complement — it prevents *structural* monoculture. Both axes moving together is what makes two tastemaker sites feel like different sites rather than two color-swaps of one template. (This is also why tastemaker doesn't need a Hallmark-style multi-axis *theme* rotation: our color axis varies by generation, so diversification here is purely structural.)

## The memory file — `.tastemaker/log.json`

Lives alongside `.tastemaker/style-lock.md` in the project root. A JSON array, newest entry first, one entry per build:

```json
[
  { "date": "2026-07-23", "page": "landing", "macrostructure": "Feature Stack", "nav": "N2", "hero": "H2", "footer": "Ft1", "knobs": "hero=split/left-bias/mockup; features=F1/irregular", "brief": "Tracejam · SaaS observability" },
  { "date": "2026-07-20", "page": "landing", "macrostructure": "Editorial Index", "nav": "N4", "hero": "H1", "footer": "Ft4", "knobs": "hero=statement/xxl/centered", "brief": "Meridian · design studio" }
]
```

- **Read it before picking** the macrostructure or any archetype (this is part of Step 0's memory check).
- **Append a new entry at the front** after each build, in the same pass that writes the CSS stamp.
- **Trim to the last ~20 entries.** Create `.tastemaker/` and the file if absent; respect the project's `.gitignore` (the user may or may not want it committed).
- If a build's CSS carries a stamp but there's no `log.json`, infer one entry from the stamp and proceed.

## The rotation rule (mandatory)

Using the **last 3-5 entries**:

1. **Macrostructure** must differ from the last build's (and ideally from all of the last three). Marketing pages only — an App shell page is governed by `component-patterns.md`'s App shell section and doesn't rotate against marketing macrostructures.
2. **Nav archetype** and **footer archetype** must each differ from the last build's. These are the single most-violated rule in practice: the failure mode is reaching for the mood's *default* nav/footer on every build, so four builds ship two navs. A mood with four builds should show four different navs — rotate deliberately through the "also OK" column in the catalog's routing tables.
3. **Hero archetype** must differ from the last build's.
4. **If you must reuse an archetype** (small catalog, genuine best-fit), change **at least one variation knob** — two heroes built `split/left-bias/mockup` are the same hero. State the knob delta.

**Palette is exempt** — it's regenerated per project and already differs by construction; don't try to "rotate" it.

## State the rotation out loud (the accountability step)

Before writing any code, say the rotation in plain text — picking on the page, not in your head, is what actually breaks the default-attractor. Format:

> *"Last 3 builds: Feature Stack (Tracejam) · Editorial Index (Meridian) · Bento Showcase (Cobalt). Picking from {Long-Scroll Narrative, Stat-Led, Gallery Grid, Product Demo} — going with Long-Scroll Narrative; the brief is a non-obvious product that needs explaining.*
> *Nav: last was N2, this build N3 floating pill. Footer: last was Ft1, this build Ft4 statement. Hero: last was H2, this build H6 letter."*

Three shapes to imitate:

- **First build** (no `log.json`): no rotation block — just the pick. *"First build for this project. Picking Feature Stack — fits the observability brief."*
- **Mature project** (5+ entries): the full frequency-count + exclusion + pick block above.
- **User asked for the same shape again** (*"use the same layout"*): honor it, but change knobs. *"You asked for Feature Stack again — same shape, different fingerprint: features go F2 bento this time (was F1 bands), hero right-bias (was left)."*

## The build stamp

The first non-empty line of the built CSS (or the top of an inline `<style>`) records what was chosen, so the next run can read and rotate against it:

```css
/* tastemaker · macrostructure: Long-Scroll Narrative · mood: warm · page: landing
 * nav: N3 · hero: H6 · footer: Ft4 · knobs: hero=letter/1-para/typed-signoff
 * palette: seed 4 (warm/light) · contrast: pass (matrix)
 * critique: ShowTell 5 · Phil 4 · Hier 5 · Spec 4 · Restr 5 · Var 5 */
```

The stamp is the durable record. It carries the structural picks (for diversification), the mood + palette seed (so the exact palette is reproducible), the contrast result (so a later run knows the color contract was actually verified, not assumed), and the pre-emit self-critique scores (see `references/anti-slop-checklist.md`). Keep it in sync with the `log.json` entry — they record the same build from two angles.

## Recording in the style lock

`.tastemaker/style-lock.md` gets a **Structure** section (see `references/style-lock-format.md`) recording the macrostructure and archetype family this project's pages use. Note the intent difference from the log:

- **Across projects** — structure *varies* (that's this engine; the log enforces it).
- **Within one project** — structure stays *coherent*: a multi-page site should feel like one site, so its pages share a nav/footer/type system even as each page's body can use a different macrostructure. The style lock records the shared frame; the log records what each build did so builds don't repeat.

Don't over-rotate inside a single project to the point that its own pages feel unrelated — the rotation rule is about not repeating *the same page build*, not about making every page of one site look foreign to the others.
