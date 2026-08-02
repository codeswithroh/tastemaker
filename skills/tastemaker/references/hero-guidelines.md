# Clean hero guidelines

Use this reference whenever building or revising the first viewport of a landing page, marketing site, or public front door for an application. The goal is not minimalism for its own sake. The goal is a decisive attention hierarchy: the visitor should understand the product before noticing the composition.

## Start with the five-second answer

Before writing markup, complete this sentence in plain language:

> This product helps [specific user] achieve [valuable outcome] by [distinct mechanism].

Turn the valuable outcome into the headline. Let the subhead clarify the mechanism. If the hero needs a workflow diagram, four metrics, or a paragraph to explain the product, the message is not yet sharp enough.

## Default attention budget

Treat this as the starting limit, not a quota to fill:

- One optional eyebrow, only when it adds context the headline cannot.
- One headline: one promise, usually 6-12 words. Tighten display line-height and allow the strongest phrase to carry the accent — but tightening has a floor: at the weight and size actually used, descenders (g/y/p/j/q) and punctuation (apostrophes, commas) on one line must clear the line below without touching or overlapping it. Check this visually, not just by the line-height number — the same value that's safe at 400-weight/3rem can clip at 800-weight/6rem+. `line-height: 0.87` or lower on a bold, large-clamp display headline is a known way to cause this; see `references/anti-slop-checklist.md`'s line-height item for the numeric floor.
  - **Word count and display size move together — they are not independent rules.** A headline within the 6-12 word budget can still render oversized if the type size doesn't scale down as the word count climbs toward the long end. Split the range: **6-8 words** gets the full display size (the top of whatever `clamp()` range the project's type scale defines). **9-12 words** steps down to a visibly smaller size — roughly one clamp tier down, about 15-20% smaller across the whole `clamp()` range, not just the same size left to wrap across more lines. If a headline needs the long end of the word budget *and* the full display size to say what it needs to say, that's a signal to cut the headline, not to let the type carry the overflow.
  - **Under 6 words still has a ceiling — a shorter headline is not a license to go bigger.** The instinct to size inversely with word count (fewer words, so make each one huge) is exactly the failure real output has shown: a 4-word headline like "Block blind agent releases." rendering one word per line at near-viewport scale. **3-5 words caps at the same full display size the 6-8 word band uses — never above it.** Real premium product heroes (Linear, Stripe, Vercel) run short headlines at that same top-tier size, not a scaled-up outlier; punchiness comes from word choice and whitespace, not from exceeding the scale's own ceiling. A 1-2 word headline is rare enough it should be treated as a deliberate art-directed statement piece (mood note in the acceptance checks below), not the default case.
  - **A short headline must not be forced into one-word-per-line stacking.** At the display size in use, a headline under 6 words should read on 1-2 lines. If it's breaking into 3+ lines — especially one word per line — the type size is too large for the container at that word count; step it down rather than letting the layout stretch vertically to accommodate it. This is the same failure as the long-headline wrapping check below, just triggered from the opposite direction (oversized type forcing a short line count to fragment, instead of a long headline overflowing a fixed size).
- One subhead: one sentence, ideally 16-28 words and no more than two lines on desktop.
- One primary CTA. Add one secondary CTA only when it serves a distinct lower-commitment path such as proof, demo, or documentation.
- One focused visual that proves the outcome.
- Navigation stays quiet. Do not let its controls compete with the hero CTA.

Do not add trust rows, feature chips, workflow rails, contract/metric sidebars, floating badges, decorative stamps, orbit lines, file/status footers, or multiple mockups merely because there is room. Move them into the next section where they can become real proof instead of hero clutter.

## Choose one proof visual

Show the product's desirable result, not the machinery used to produce it.

- For a builder or generation tool, show one excellent finished output.
- For a dashboard, crop to the one decision or result users care about instead of reproducing the entire app shell.
- For a workflow product, show the completed state in the hero and explain the steps below the fold.
- For a physical product, use one strong product-in-context image rather than a collage of supporting assets.
- For an abstract service, use one clear illustration or before/after moment tied directly to the promise.

Use at most one outer presentation frame around the visual. Avoid a dashboard inside a dashboard. Small chrome may establish context, but every label inside it must earn its place.

## Compose for hierarchy

- Give the headline and visual clear, separate territories with generous negative space.
- Let one side dominate slightly; equal-weight columns can feel mechanically templated.
- Use one intentional rule-break at most: a controlled bleed, an off-grid edge, or a restrained accent bar. Do not stack several decorative gestures.
- Keep the hero palette quieter than the sections below it. Accent color should identify the key phrase, action, or visual detail—not all three at maximum intensity.
- When an established logo does not match the new theme, preserve the logo and solve the mismatch through its surrounding space, scale, or container.

## Optional: a floating metric chip as annotation, not a second hero group

A small chip (a real number + a one-to-three-word label, e.g. "6.60:1 contrast" or "5.2K active users") laid directly on top of the single proof visual — not beside it — reads as an annotation of that one visual, not a competing hero group, and premium references (motionsites.ai's higher-end hero examples among them) use this well. It is still governed by the same restraint budget, not exempt from it:

- **Cap at one, or at most two** chips per hero, and they must sit ON the proof visual (overlapping its edge/corner), never floating independently in empty hero space — that reads as a fourth hero group, exactly what line 27 above forbids.
- **The number must be real** — pulled from the product's own verified output (a contrast ratio actually computed for this build, a real usage count), never invented to fill the space.
- Keep them small and quiet: this is a caption-scale detail noticed on a second look, not a headline-scale claim competing with the actual headline.
- This does not relax the "one focused visual" rule — the chip is part of that one visual's presentation, not a second one.

## Turn a static proof visual into a real animated comparison

When the product's proof is fundamentally a *comparison* (before/after, with-skill/without-skill, old-way/new-way) and you have both real states as separate assets, don't compose them into one flat static image. Build an animated wipe/reveal instead: layer the two real screenshots absolutely, clip the top layer with `clip-path: inset()` driven by a CSS custom property (e.g. `--wipe`), and animate that property back and forth on a slow loop (GSAP supports tweening CSS custom properties directly: `gsap.to(el, { "--wipe": "80%", duration: 4, ease: "sine.inOut", yoyo: true, repeat: -1 })`).

This is the single highest-leverage move for a hero that otherwise reads as "just a screenshot" — it turns real, honest content into something that visually reads as continuous motion (the "it looks like a video plays in the background" reaction premium references get), without fabricating a video asset or a synthetic 3D render. Both layers must be genuinely real captures of the actual product/comparison — never stage one side to look worse than it actually is.

Constraints: this replaces the single proof visual, it doesn't add to it — still one visual, one frame, one job. Cap the wipe range so it never fully hides either state for long (e.g. 15%-85%, not 0%-100%) so a viewer glancing at any moment still sees both sides represented. Always respect `prefers-reduced-motion`: freeze at a fixed midpoint (e.g. 50%) rather than animating.

## Optional: ambient depth behind the proof visual

A soft radial glow (using the project's existing accent color at low opacity, positioned behind the proof visual) or a subtle idle drift/pulse on the visual itself (a few px of float, GSAP `yoyo: true, repeat: -1`, several-second duration) can make a static screenshot or product shot feel alive without adding a new competing element.

**A stronger option when the brief calls for real production value**: an animated generative background — two or three soft radial-gradient "blobs" in the project's locked accent colors, drawn on a `<canvas>` and slowly drifted with `Math.sin`/`Math.cos` on a `requestAnimationFrame` loop — sitting behind the entire hero section (not just the proof visual). This is the honest substitute for a licensed stock-video background loop: genuinely continuous motion, zero licensing/sourcing cost, and it never competes with content because it's decorative and kept to low opacity. Draw one static frame and stop under `prefers-reduced-motion` instead of starting the loop.

Either technique: keep the motion slow and low-amplitude enough that it reads as ambient texture, not attention-grabbing animation — and always gate it behind `prefers-reduced-motion` like any other motion in the hero.

## A real reference check before calling a hero "done"

Before finishing a hero pass, look at one current, genuinely award-caliber site in the same category as the product (not just a general inspiration gallery) and name what it's actually doing. A concrete finding from doing this against Linear.app while building this exact section: its hero is almost entirely restraint — huge type, a real (not glamorized) product screenshot at full width fading into the background via a top vignette, and *one* tiny text-link secondary action instead of a second button. No floating badges, no chips, no glow. That's a legitimate answer to "make it award-winning" that looks nothing like a maximalist agency-showcase hero — restraint, at sufficient scale and fidelity, reads as premium on its own. Don't assume "award-winning" means "add more decoration"; check a real reference in the product's own category before deciding which direction it means here.

## Motion should reveal, not multiply

Use a short GSAP sequence with at most four coherent beats:

1. navigation or context,
2. headline,
3. subhead and actions,
4. the single proof visual.

Animate the visual as one composition. Do not stagger every label, tile, metric, or decorative shape separately. Avoid decorative parallax/orbits in the first viewport unless they communicate product behavior. Respect `prefers-reduced-motion`.

## Responsive acceptance checks

- At 390px, no horizontal overflow.
- The headline remains readable in roughly 3-5 lines; no orphaned one-word line caused by an avoidable width constraint.
- **At the top of the display size range, the headline fits comfortably in 2-3 lines.** If it's wrapping into 5+ lines at full size, that's not a responsive-width problem to accept — it's a signal the headline is too long for the size in use. Step the display size down a tier (see the word-count/size rule above) or shorten the headline; don't let a long headline dominate the hero by taking up more vertical space at full size instead of stepping down.
- The subhead remains one compact paragraph.
- CTAs either fit cleanly side by side or stack as full-width actions; they never squeeze into awkward labels.
- The proof visual remains legible when stacked. Crop or simplify its internals rather than shrinking a dense desktop composition until it becomes unreadable.
- On a short desktop viewport, the primary promise and action remain visible without scrolling. The visual may continue below the fold if necessary.

## Subtraction pass

Before delivery, list every distinct hero group and ask what user question it answers. Keep only groups that answer one of these:

1. What is this?
2. Why should I care?
3. What should I do next?
4. What does a good result look like?

Move everything else below the fold. If two groups answer the same question, keep the stronger one.
