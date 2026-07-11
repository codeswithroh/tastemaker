# Image-generation prompt template (generation path)

Fill the variables from the brief and the decisions made in `composition-patterns.md`. Generate ONE image per prompt — never ask for a grid or multiple concepts in one call. Keep the whole Style DNA in every prompt; image models forget constraints that aren't restated.

```text
Generate one standalone modern flat-vector editorial illustration, landscape orientation, on a calm near-white background.

Visual DNA:
Clean modern flat illustration in the register of unDraw / Storyset / premium SaaS landing pages. Proportioned, natural characters (roughly 7-8 heads tall, relaxed pose, simple face). Flat shapes with at most one subtle shade for depth — no heavy 3D. Restrained neutral palette (off-white, greys, charcoal) plus natural skin tones, and exactly ONE saturated accent color: {BRAND_ACCENT_HEX}. The accent is the loudest thing in the frame and marks the single focal point. Generous whitespace; the subject fills about 50-65% of the frame. Confident, tasteful, a little clever — art-directed, not auto-generated.

Absolutely avoid: rainbow or multi-hue palettes; indigo-to-purple or blue-to-cyan gradients; glossy 3D, bevels, glow, glassmorphism; busy or textured backgrounds; realistic photography; corporate clip-art or generic stock-team scenes; cute children's-book cartoon style; dense infographic / PowerPoint / flowchart look; baked-in paragraphs of text; deformed hands or faces.

Concept:
{ONE_SENTENCE_CORE_IDEA}

Structure:
{STRUCTURE from composition-patterns.md: hero scene / before-after / character state / concept metaphor / workflow / layers / journey}

Fresh metaphor:
{THE_METAPHOR — the physical action + the low-key object, from the 3-step recipe. e.g. "a person tuning the dials of a control panel that raises a set of bars" rather than "a bar chart"}

Scene (build depth, not a floating subject):
Background: {calm large shape / suggested environment}. Midground: {the metaphor object/device, in the accent}. Foreground: {the character performing the core action, interacting with the midground}. Grounding: soft shadow under the subject; {one or two sparse decorative accents}.

Focal point:
{the one element the accent lands on}

Optional labels:
{zero to three very short words, only if essential — else "none"}

Constraints:
One idea, one focal point. The character must be performing the core action, not standing beside the scene. One or two objects maximum; keep at least 35% of the frame as calm whitespace. Only the accent color is saturated; everything else neutral. No title, no caption, no baked-in body text. Clean but not sterile, simple but not empty, characterful but not busy.
```

## Iteration prompts (image-edit / regenerate)

**Make the character central to the idea (fixes "figure is decoration"):**
```text
Regenerate with the same concept, palette, and simple layout, but make the character clearly perform the core action — operating/building/riding the metaphor object, not standing beside it. Keep it clean, flat, sparse, one accent color, plenty of whitespace.
```

**Calm it down (fixes "too busy / too many colors"):**
```text
Regenerate simpler: remove secondary objects and any extra colors, keep only the focal subject and one accent color, add more whitespace. One clear idea, nothing decorative competing with it.
```

**Remove unwanted baked-in text:**
```text
Edit the provided image: remove the text "{TEXT}" and fill that area with the matching clean background. Preserve everything else exactly — characters, shapes, colors, composition, aspect ratio. Add no new text or objects.
```
