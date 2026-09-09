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

## Cross-project memory — `~/.tastemaker/structure-history.json`

`.tastemaker/log.json` only stops *one* project from repeating itself. It does nothing about two different projects both defaulting to Feature Stack every time — which is the failure mode that actually makes tastemaker output feel common: not one site repeating its own shape, but many *different* sites converging on the same "safe" shape independently. This file closes that gap. It lives outside any repo, next to `~/.tastemaker/profile.md`, and is shared across every project this skill touches.

Same entry shape as the project log, plus a `project` field, an `id`, and an `outcome`:

```json
[
  { "id": "tracejam-2026-07-23", "date": "2026-07-23", "project": "tracejam", "page": "landing", "macrostructure": "Feature Stack", "nav": "N2", "hero": "H2", "footer": "Ft1", "outcome": "kept" },
  { "id": "meridian-studio-2026-07-20", "date": "2026-07-20", "project": "meridian-studio", "page": "landing", "macrostructure": "Editorial Index", "nav": "N4", "hero": "H1", "footer": "Ft4", "outcome": "pending" }
]
```

- **Append a new entry in the same pass** that writes the project's `log.json` entry and the CSS stamp — all three record one build, from three angles (cross-project frequency, project-local rotation, in-code record). Set `outcome` to `"pending"` at write time — it isn't known yet.
- **Trim to the last ~40 entries.** Create the file (and `~/.tastemaker/`) if absent.
- **Check it as part of Step 2.5**, alongside the project's own `log.json` — before picking, not after.
- **Run the mechanical check**: `python3 scripts/check_structure_history.py --current <picks.json> [--project-log .tastemaker/log.json] [--global-log ~/.tastemaker/structure-history.json]`, where `<picks.json>` is a small JSON object of the build's chosen `{macrostructure, nav, hero, footer}`. It flags (non-fatal — a nudge, not a block) when a pick makes up 60%+ of the last 5 global entries, i.e. it's the thing every recent project reached for regardless of brief. Run it right after stating the rotation out loud, before Step 4's build — catching an over-hot pick here is cheaper than catching it in the finished page.
- If the check flags something and the pick is kept anyway (the brief genuinely calls for it), say so explicitly in the rotation statement — same honesty rule as everywhere else in this skill.
- **Update `outcome` at Step 5**, when the design pass gets a real keep/reject verdict (see "Close the loop" below) — don't leave every entry sitting at `"pending"` forever, or the outcome data never accumulates enough to be useful.

## Close the loop — outcome-weighted picking

Blind rotation (never repeat the last pick) prevents monoculture but has no opinion about *quality* — it will just as happily rotate toward a macrostructure that keeps getting rejected as one that keeps getting kept. Once `structure-history.json` has enough resolved entries to say something, use that signal too, without letting it override rotation:

1. **At Step 5**, when a design pass resolves to `kept` or `rejected` (per `references/taste-memory.md`'s decision log), also patch the matching `structure-history.json` entry's `outcome` field to `"kept"` or `"rejected"` — match it by `id`, or by date + project if the id wasn't recorded. This is a small edit to an existing entry, not a new one; `.tastemaker/log.json` stays as the immutable per-build record.
2. **At Step 2.5**, once the rotation rule has produced a shortlist of legal candidates (the ones that pass "differs from the last 3-5 builds"), run `python3 scripts/summarize_outcomes.py` to see each macrostructure/nav/hero/footer archetype's kept-vs-rejected rate across resolved global entries. Use it only as a **tie-break among already-legal candidates** — never to justify breaking the rotation rule and repeating last build's pick because it "tested well." Variety is still mandatory; this only helps decide *which* fresh direction to reach for when more than one would fit the brief.
3. **Small samples say nothing.** An archetype with 1-2 resolved outcomes is noise, not signal — `summarize_outcomes.py` marks anything under 4 resolved entries as low-confidence and it should be read as "no real data yet," not weighted into the pick.
4. **A high reject rate is a prompt to ask why, not to blacklist the shape.** A macrostructure might read as rejected because it was genuinely wrong for those briefs, or because it was executed poorly each time (thin content, bad archetype pairing, weak copy). If the rejections cluster around a specific reason in the decision log, note that reason rather than avoiding the shape wholesale.

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
> *Nav: last was N2, this build N3 floating pill. Footer: last was Ft1, this build Ft4 statement. Hero: last was H2, this build H6 letter.*
> *Cross-project check (`check_structure_history.py`): clean, no axis over 60% of the last 5 global builds."*

Three shapes to imitate:

- **First build** (no `log.json`): no rotation block — just the pick. *"First build for this project. Picking Feature Stack — fits the observability brief."*
- **Mature project** (5+ entries): the full frequency-count + exclusion + pick block above.
- **User asked for the same shape again** (*"use the same layout"*): honor it, but change knobs. *"You asked for Feature Stack again — same shape, different fingerprint: features go F2 bento this time (was F1 bands), hero right-bias (was left)."*

## The build stamp

The first non-empty line of the built CSS (or the top of an inline `<style>`) records what was chosen, so the next run can read and rotate against it:

```css
/* tastemaker · macrostructure: Long-Scroll Narrative · mood: warm · page: landing
 * arc: hook(H6) -> problem(prose) -> solution(F1) -> how(F4) -> proof(P4) -> close(C2)
 * nav: N3 · hero: H6 · footer: Ft4 · knobs: hero=letter/1-para/typed-signoff
 * palette: seed 4 (warm/light) · contrast: pass (matrix)
 * critique: ShowTell 5 · Phil 4 · Hier 5 · Spec 4 · Restr 5 · Var 5 */
```

The stamp is the durable record. It carries the structural picks (for diversification), the narrative arc's beat sequence (see `references/narrative-arc.md` — so a later `audit` pass can check the arc held together, not just that structure varied), the mood + palette seed (so the exact palette is reproducible), the contrast result (so a later run knows the color contract was actually verified, not assumed), and the pre-emit self-critique scores (see `references/anti-slop-checklist.md`). Keep it in sync with the `log.json` entry — they record the same build from two angles.

## Recording in the style lock

`.tastemaker/style-lock.md` gets a **Structure** section (see `references/style-lock-format.md`) recording the macrostructure and archetype family this project's pages use. Note the intent difference from the log:

- **Across projects** — structure *varies* (that's this engine; the log enforces it).
- **Within one project** — structure stays *coherent*: a multi-page site should feel like one site, so its pages share a nav/footer/type system even as each page's body can use a different macrostructure. The style lock records the shared frame; the log records what each build did so builds don't repeat.

Don't over-rotate inside a single project to the point that its own pages feel unrelated — the rotation rule is about not repeating *the same page build*, not about making every page of one site look foreign to the others.
