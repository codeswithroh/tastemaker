# Style DNA (generation path)

This is the style contract for **generating** original illustrations with an image model — the path that lifts ideagram past "recolor what's in the library" to "create a beautiful, on-brand illustration for any concept." Every generated image obeys this DNA so a set of them reads as one designed system, not assorted stock art.

The aesthetic target is *modern editorial flat illustration* — the register of unDraw, Storyset, and top SaaS marketing sites: clean, confident, characterful, a little bit art-directed. Not corporate clip art, not AI-slop.

## One sentence

Clean modern flat-vector illustration on a calm background: proportioned, characterful people or a single strong metaphor object, one confident brand accent against a restrained neutral palette, generous whitespace, one clear focal point — the kind of image a tasteful design studio would ship on a product's landing page.

## Must

- **One idea per image.** Depict a single concept, action, or metaphor — not a busy montage. If the brief has two ideas, that's two images.
- **One clear focal point**, carried by the brand accent. The eye should land in one place first.
- **A real scene, not a floating object.** Ground the subject: a surface, a soft background shape, a subtle shadow, a suggested environment. (See `composition-patterns.md` — this is the thing amateur output most often misses.)
- **Generous whitespace / calm negative space** — the subject occupies ~50–65% of the frame; the rest breathes.
- **Proportioned characters** when people are used: natural ~7–8 head proportions, relaxed poses, simple faces. People should look designed, not deformed.
- **Cohesive palette:** a restrained set of neutrals + skin tones + exactly one **brand accent** color (passed in per request). The accent is the only saturated color and it lands on the focal point.
- **Consistent light, flat rendering:** soft flat shapes, gentle long shadows or a single soft drop shadow at most — depth through layering and one subtle shade, not heavy 3D.

## Palette model

- **Neutrals:** off-white/very-light background, mid-grey and charcoal for structure and line, near-black sparingly.
- **Skin/organic:** natural muted skin tones (never one flat silhouette for a person).
- **Accent:** ONE brand color (the request's hex). It is the loudest thing in the frame and marks the focal point. Optionally one *tint/shade* of it for a secondary surface — never a second unrelated hue.
- Restraint beats variety. If a third color feels needed, the scene is trying to say too much — simplify.

## Absolutely never (the anti-slop list)

These are the tells that make generated illustration look cheap or generic — forbid them explicitly in every prompt:

- No rainbow/multi-hue palettes; no indigo→purple or blue→cyan default gradients.
- No glossy 3D, no bevels, no drop-shadow-everywhere, no glassmorphism, no neon glow.
- No busy or textured backgrounds, no photo-collage, no realistic photography mixed in.
- No corporate clip-art, no generic "diverse team high-fiving," no stock-vector stiffness.
- No cute children's-book or mascot-poster cartooniness (unless the brand is explicitly playful).
- No dense infographic / PowerPoint / flowchart-with-every-node-labeled look.
- No text baked into the image unless a label is essential (and then ≤3 short words).
- No deformed hands/faces — prefer simple, confident features over ambitious detail that breaks.

## Aesthetic direction

Confident, tasteful, a little bit clever. Clean but not sterile; simple but not empty; characterful but not busy. It should feel *art-directed by someone with taste*, not auto-generated. When in doubt: fewer elements, more whitespace, one strong idea, one accent.
