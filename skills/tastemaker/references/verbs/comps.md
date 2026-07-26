# `comps` — reference comps only, no code

The user wants **visual comps, not a built page** — hero mockups, key section layouts, or a brand-kit board (logo directions, palette, type, identity applications) — to hand to an image generator (ChatGPT Images, Codex image mode, Midjourney, or similar) before any coding agent touches the project. `comps` produces the **brief**, not the pixels: tastemaker has no image-generation API of its own wired in, and users bring their own tool. What it *does* own is the palette, the composition, and the identity rules the brief is built from, so the comp is grounded in the same real system a coded build would use, not a vague prompt the image tool has to guess at.

## Why the mechanism is a brief, not an API call

Two real constraints ruled out anything else:

- **No image-generation tool is uniform enough to hardcode.** The target user is explicitly bringing their own (ChatGPT Images, Codex image mode, Midjourney, Recraft, whatever they already pay for) — building against one specific API would lock most of them out.
- **tastemaker stays markdown + small Python scripts**, on purpose (see the README's own framing). Wiring a paid image-gen API as a hard dependency would break that, for a mode that's explicitly a pre-code, optional detour.

So `comps` reuses the parts of tastemaker that already produce real, checkable output, then writes them into a structured prompt the user pastes into their own tool. It doesn't reinvent palette generation, structure, or logo rules for this mode. It assembles what already exists into a brief.

## When this runs

The user says "just give me some comps," "I want to see directions before we build," "mock up a few hero options," or wants a brand-kit board (logo directions + palette + type + identity applications) before committing to a coded build. If they ask for a "mockup" of something that already has code (an existing app screen), that's not this verb; that's a normal Design pass on real markup.

## What `comps` reuses, not reinvents

1. **Palette** — run `scripts/generate_palette.py` exactly as Step 1 of the normal flow does. The comp's color input is the same contrast-verified, per-project palette a coded build would get, not the image generator's own guess at "professional blue." Hand the resulting hex values and role assignments (background, surface, primary, accent, text) straight into the brief.
2. **Structure** — pick a macrostructure (`references/macrostructures.md`) and the specific archetypes it needs (`references/component-catalog.md`) exactly as Step 2.5 does. A comp brief that says "hero: H2 split-demo, left-bias, real product mockup on the right" produces a dramatically more specific, more on-brand image than "make a nice hero section" — the same reason the coded flow doesn't build from a vague brief either.
3. **Logo/mark** — if the brand-kit board includes a logo direction, it follows `references/logo-sourcing.md`'s rules directly: a real constructed geometric mark, never a letter dropped in a colored box. State this constraint explicitly in the brief handed to the image tool, since an image generator's own instinct defaults to exactly the letter-in-a-box tell this skill exists to avoid.

Do **not** run Step 3 (real asset sourcing) or Step 4 (build) for this mode — there's no code to source assets into yet.

## Building the brief

One structured brief per comp, not a single vague paragraph covering everything:

```
Comp: [Hero — split-demo direction]
Palette: bg #0C1414 (page background) · surface #171F1F (panels/cards) ·
  primary #008286 (primary actions, links) · accent #BE85CE (sparingly, emphasis only) ·
  text #E5F6F6 on bg (contrast X.XX:1, verified)
Composition: [macrostructure name] — [archetype ID + description, e.g.
  "H2 split-demo: headline + subhead + CTA left, one real product screenshot
  mockup right, asymmetric weighting, left side dominant"]
Type register: [role, e.g. "geometric sans display, confident weight"] — name real
  candidate fonts if the project has committed to specific ones already
Mood: [one of tastemaker's five: premium / warm / technical / playful / elegant]
Explicit constraints: no default indigo-to-purple gradient; no letter-in-a-box logo
  mark if a mark is in frame; [any other anti-slop constraints relevant to this comp]
```

Write one of these per comp requested (a hero direction, a pricing-section layout, a full brand-kit board), each grounded in the *same* generated palette and, where relevant, the same macrostructure pick, so a set of comps reads as one coherent direction rather than three unrelated images that happen to share a prompt template.

## State the picks out loud, same as every other mode

Before handing back the brief(s): *"Palette: seed 7 (technical/dark), contrast-verified. Structure: Feature Stack macrostructure, H2 split-demo hero. Building 3 comps: hero, pricing section, brand-kit board — all from this palette and hero archetype."* This is the same accountability step Step 2.5 and the diversification engine already use elsewhere; comps mode isn't exempt from stating its picks just because the output is a prompt instead of code.

## The handoff artifact

Write `.tastemaker/comps-brief.md`: the generated palette (hex + roles + contrast verification), the macrostructure/archetype picks, and the individual prompts actually used, in one file. This is what makes the mode's output usable by a *later* coding pass, not a dead-end:

- When the user comes back with "now build this for real" (with or without the generated images in hand), the normal Design flow reads `.tastemaker/comps-brief.md` first. The palette and structure picks are already decided — skip re-deriving them in Step 1/2.5, write them straight to `.tastemaker/style-lock.md`, and proceed to Step 3 (real asset sourcing).
- If the user *does* bring back generated images they liked from one of the comps, treat those the same way Step 2's extract-palette path treats any reference image: grounding for the specific screen, not a source to pixel-clone. `study` mode's "extracts structure, not pixels" rule applies here too — an image generator's rendering of "a product mockup" is a visual direction, never a literal asset to embed as-is in the shipped build.

## Limits to state every time

- **The comp is only as good as the image tool executing the brief.** tastemaker verifies the palette and names the composition; it can't verify that the external image generator actually followed either one. Look at what comes back before treating it as locked.
- **Comps are not assets.** A generated hero mockup image is a direction to build toward, not something to ship as-is in the final page — real screenshots, real product UI, and real photography still come from Step 3 of the normal flow.
- **This mode doesn't replace `study`.** `study` extracts DNA from something that already exists; `comps` generates new directions from tastemaker's own system before anything exists yet. Different direction of travel.
