# Style contract

Every illustration this skill produces follows the same visual grammar, on purpose — a set of illustrations that all follow one grammar reads as one system (shareable, brandable); a set that each improvise their own style reads as clip art.

## Color: exactly two, always

- **One base/outline color** — near-black, used for figures, outlines, and structural elements. Default: `#262631`.
- **One accent color** — used for the single "pop" element per illustration (the thing the concept is actually about: the shield's face, the bulb's glass, the chart's highlighted bar). Default: `#6C5CE7`, but this is the one thing a caller should expect to customize per brand.
- **Never a third color, never a gradient.** If a scene seems to need a third color, that's a sign the composition is trying to depict too much at once — simplify the scene instead of expanding the palette. This constraint is what makes recoloring reliable (`scripts/recolor_svg.py` assumes exactly this two-color convention) and what makes the output actually look like one coherent family rather than assorted clip art.

## Shape language

- Flat fills only. No shadows, no bevels, no gradients, no photorealistic rendering.
- Rounded corners on human-made objects (devices, furniture, signage) — sharp corners read as colder/more technical than the friendly, approachable register this style targets.
- Circles and capsule shapes for anything organic (heads, limbs) — this is what keeps figures reading as simple/abstract rather than attempting (and failing at) realistic anatomy.
- Generous negative space. A cluttered illustration with 6 objects competing for attention explains nothing; a spare one with 2 objects and a clear focal point explains instantly.

## Composition

- **One concept, one scene.** Resist the urge to depict every aspect of the input content — pick the single idea that explains it fastest and build the whole illustration around that (see `references/metaphor-library.md` for how to choose it).
- **One clear focal point.** The accent color should land on the thing that matters most in the scene, not be spread evenly across several elements — if everything is accented, nothing is.
- **Default to including a human figure, not a bare object.** This is the single biggest thing that makes unDraw-style illustration read as "explaining an idea to a person" rather than "a stock icon" — almost every unDraw illustration has a character *doing something* with the concept, not just the concept floating alone. So the default composition is a figure (usually `figure-pointing.svg`, gesturing toward the prop as if presenting or explaining it) plus the prop that carries the actual concept — not the prop by itself. Reach for a bare, figure-less prop only when the illustration is meant to work as a small standalone icon (e.g. inline next to a heading) rather than as a scene — that's the exception, not the starting point.
- Canvas: build on a `400 400` viewBox per primitive; when composing a scene from multiple primitives, lay them out with simple `transform="translate(x y)"` groups rather than editing each primitive's internal coordinates — this keeps primitives reusable and each new composition low-risk.
- **Mirroring is a legitimate composition tool, not just translation.** Most figures/props are symmetric, so two copies placed side by side read as identical twins, not as "facing each other" or "moving in a direction." Wrap a copy in `<g transform="translate(x y) scale(-1,1) translate(-w 0)">` (mirror around its own width `w`) when a scene needs orientation or facing — e.g. two figures flanking a shared object read more intentionally when mirrored toward it.
- **When a concept needs to distinguish multiple actors of the same kind** (two different people's cursors, two competing options), don't reach for a third color — that breaks the two-color rule this whole system depends on. Vary fill-vs-outline instead: one instance solid-filled in the base color, the other outlined in the base color with an accent fill. This preserves the two-color contract while still making two things visually distinct.

## What this style is not

Be upfront about this rather than overclaiming: this produces clean, simple, geometric flat illustration — closer to a flat icon-illustration hybrid than to unDraw's own more detailed, organically-posed artwork. It's a legitimate, widely-used register (plenty of real products ship exactly this level of simplicity) and it composes and recolors reliably, which is the actual point — but it is not a pixel-for-pixel match to any specific illustrator's hand-drawn style, and shouldn't be presented as one.
