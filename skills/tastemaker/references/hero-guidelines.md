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
