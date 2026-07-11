# QA checklist (generation path)

Run every generated image against this before delivering. If it fails, regenerate or edit (see the iteration prompts in `prompt-template.md`) rather than shipping it. This is what separates "an AI image" from "a designed illustration."

- [ ] **One idea, one focal point.** The eye lands in one place first, and that place is the accent color. If attention scatters, it's too busy — simplify.
- [ ] **The character earned its place.** If a person is present, they're *performing the core action*, not standing beside the scene. (Remove-them test: does the metaphor still fully read without them? If yes, rewrite.)
- [ ] **It's a scene, not a floating object.** There's a background/ground, a subtle shadow, some depth — not a subject stranded on blank white.
- [ ] **Palette is disciplined.** Neutrals + skin + exactly one saturated accent. No rainbow, no default indigo/purple gradient, no second unrelated hue.
- [ ] **No anti-slop tells.** No glossy 3D, glow, glassmorphism, busy/textured background, stock clip-art stiffness, cutesy cartoon, or dense-infographic look.
- [ ] **Whitespace intact.** At least ~35% calm space; subject ~50–65% of the frame. Not cramped.
- [ ] **People render cleanly.** Proportions natural (~7–8 heads), no deformed hands/faces. If a hand or face broke, regenerate or crop it out of frame.
- [ ] **Minimal/no baked-in text.** No title, no caption, ≤3 short label words and only if essential. If the model wrote gibberish text, edit it out.
- [ ] **On-brand.** The accent is actually the requested brand hex (or visually equivalent), and it's on the focal point.
- [ ] **Fresh, not generic.** The metaphor isn't the first cliché (analytics≠plain bar chart, idea≠plain lightbulb). If it is, try the metaphor recipe again.
- [ ] **Consistent with siblings.** If this is one of a set, it shares the palette, character style, and level of detail with the others — reads as one system.

## Honesty on delivery

Say which path produced the image (generated vs. recolored real unDraw), how many images, and which are the strongest vs. optional. Don't present a generated image with a broken hand or gibberish text as finished — fix it or say it needs another pass.
