# Motion

Animation is one of the fastest ways to make a UI feel expensive or feel cheap, often more than any single color choice. The rule that separates the two: **motion should clarify, not decorate.** Every animation should answer "what changed" or "what's about to happen" — if it's just movement for its own sake, it reads as noise, not polish.

## Bundled starter (use this instead of writing motion from scratch each time)

`assets/reveal.css` + `assets/reveal.js` provide a small, dependency-free scroll-reveal + stagger system: elements fade/rise in as they enter the viewport, respecting `prefers-reduced-motion` automatically. Copy both into the project and:

```html
<link rel="stylesheet" href="reveal.css">
<script src="reveal.js" defer></script>
```

```html
<div data-reveal>Fades/rises in on scroll</div>
<div data-reveal data-reveal-group>
  <div>Child 1</div>  <!-- staggers automatically within a data-reveal-group -->
  <div>Child 2</div>
</div>
```

Don't reinvent this per project — extend the CSS variables at the top of `reveal.css` (duration, distance, easing) to match the locked style instead of writing new keyframes each time.

## What to animate, and how much

- **Entrances** (page load, scroll-into-view): a small, consistent fade + upward translate (8-16px) is almost always right. Bouncy easing, large distances, or rotation on entrance reads as playful/consumer — only use it if the locked mood (`.tastemaker/style-lock.md`) actually calls for playful. A "premium/confident" project should use a quick, restrained fade (150-250ms, ease-out), not a bounce.
- **Hover/focus states**: fast (100-150ms), subtle (a slight scale, a border/background shift, a shadow lift) — the point is to confirm interactivity, not to perform. Anything longer than ~200ms on hover starts to feel laggy rather than smooth.
- **Loading states**: skeleton screens that mirror the actual layout beat a generic spinner — they set an expectation of what's coming, which is what makes a wait feel shorter.
- **Page/state transitions**: keep direction consistent (things that mean "forward" always animate the same way) — inconsistent transition direction is disorienting even when each individual transition looks fine in isolation.

## Performance rule, non-negotiable regardless of style

Animate only `transform` and `opacity`. Anything that animates `width`, `height`, `top`/`left`, or box-shadow spread triggers layout recalculation on every frame and will visibly stutter on anything but a high-end device — this is true no matter how good the animation curve is conceptually.

## Always respect `prefers-reduced-motion`

Every animation must have a reduced-motion fallback (instant or near-instant state change instead of the animated transition). This isn't an accessibility afterthought to bolt on later — the bundled `reveal.css` handles it by default; if you write custom animation beyond what's bundled, wrap it the same way:

```css
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```

## Locking motion per project, same as color

Once a project settles on a motion feel (duration scale, easing curve, how much distance entrances travel), record it in `.tastemaker/style-lock.md`'s Motion section (see `references/style-lock-format.md`) so later screens reuse the same feel instead of each one inventing its own timing — motion inconsistency is as noticeable as color inconsistency, just harder to point at directly.
