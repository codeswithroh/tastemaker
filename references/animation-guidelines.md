# Motion

Animation is one of the fastest ways to make a UI feel expensive or feel cheap, often more than any single color choice. The rule that separates the two: **motion should clarify, not decorate.** Every animation should answer "what changed" or "what's about to happen" — if it's just movement for its own sake, it reads as noise, not polish.

## GSAP is the default motion engine

A static-looking site is one of the fastest ways a generated UI reads as a template rather than a real product. **GSAP + ScrollTrigger is the default for every Tastemaker project** — not an optional nice-to-have — because it's what actually produces the dynamic, interactive feel (scroll-driven reveals, staggered entrances, smooth hover/press feedback, timeline-sequenced hero moments) that separates a site that feels alive from one that feels like a static mockup. GSAP's full library, including ScrollTrigger and every previously-paid Club plugin, has been free for commercial use since Webflow's 2024 acquisition of GreenSock — there's no licensing reason to reach for anything more limited.

Install it per `references/tech-stack-guides.md` (CDN tags for plain HTML, `npm install gsap` for React/Vue/etc.), then wire up `assets/gsap-starter.js` — tested end-to-end (immediate-viewport reveal, scroll-triggered reveal, and real staggered timing all verified in a browser, not just written blind):

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="gsap-starter.js"></script>
<script>
  TastemakerMotion.init({
    duration: 0.22,      // seconds — pull from .tastemaker/style-lock.md's Motion section
    distance: 16,        // px
    ease: "power2.out",
    staggerStep: 0.06,   // seconds between staggered children
  });
</script>
```

```html
<div data-reveal>Fades/rises in on scroll</div>
<div data-reveal data-reveal-group>
  <div>Child 1</div>  <!-- staggers automatically within a data-reveal-group -->
  <div>Child 2</div>
</div>
```

`gsap-starter.js` uses `gsap.matchMedia()` to branch on `prefers-reduced-motion` automatically — no separate reduced-motion code path to remember. Beyond scroll-reveal, reach for GSAP timelines for anything that needs real sequencing (a hero's headline, subhead, and CTA entering in order rather than all at once) and for hover/press micro-interactions where a plain CSS transition feels flat — GSAP handles both without a different library or mental model.

**`assets/reveal.css` + `assets/reveal.js`** (the zero-dependency vanilla version) still exist and use the exact same `data-reveal` / `data-reveal-group` markup convention — use them only when a project genuinely can't take on GSAP (a constrained embed context, a CDN-blocked environment). Don't reach for them by default; GSAP is the default, the vanilla pair is the fallback.

## What to animate, and how much

- **Entrances** (page load, scroll-into-view): a small, consistent fade + upward translate (8-16px) is almost always right. Bouncy easing, large distances, or rotation on entrance reads as playful/consumer — only use it if the locked mood (`.tastemaker/style-lock.md`) actually calls for playful. A "premium/confident" project should use a quick, restrained fade (150-250ms, ease-out), not a bounce.
- **Hover/focus states**: fast (100-150ms), subtle (a slight scale, a border/background shift, a shadow lift) — the point is to confirm interactivity, not to perform. Anything longer than ~200ms on hover starts to feel laggy rather than smooth.
- **Loading states**: skeleton screens that mirror the actual layout beat a generic spinner — they set an expectation of what's coming, which is what makes a wait feel shorter.
- **Page/state transitions**: keep direction consistent (things that mean "forward" always animate the same way) — inconsistent transition direction is disorienting even when each individual transition looks fine in isolation.

## Performance rule, non-negotiable regardless of style

Animate only `transform` and `opacity`. Anything that animates `width`, `height`, `top`/`left`, or box-shadow spread triggers layout recalculation on every frame and will visibly stutter on anything but a high-end device — this is true no matter how good the animation curve is conceptually.

## Always respect `prefers-reduced-motion`

Every animation must have a reduced-motion fallback (instant or near-instant state change instead of the animated transition). This isn't an accessibility afterthought to bolt on later — `gsap-starter.js` handles it automatically via `gsap.matchMedia()`, and the vanilla `reveal.css` fallback handles it via the media query below. If you write custom GSAP timelines beyond what `gsap-starter.js` covers (e.g. a bespoke hero sequence), branch them through `gsap.matchMedia()` the same way rather than skipping the check:

```css
/* only needed for custom animation outside gsap-starter.js / reveal.css */
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
```

## Locking motion per project, same as color

Once a project settles on a motion feel (duration scale, easing curve, how much distance entrances travel), record it in `.tastemaker/style-lock.md`'s Motion section (see `references/style-lock-format.md`) so later screens reuse the same feel instead of each one inventing its own timing — motion inconsistency is as noticeable as color inconsistency, just harder to point at directly.
