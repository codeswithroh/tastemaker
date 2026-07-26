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

## anime.js — a scoped alternative, not a GSAP replacement

GSAP stays the default for every project (above). anime.js was evaluated as a second option — a real side-by-side test (bundle weight measured directly, the reveal/reduced-motion pattern hand-built and run in a browser, not assumed from docs) found it's not a better general-purpose default, but it does have two genuine, narrow use cases where it's the better tool:

1. **A page that needs both scroll-reveals and SVG motion-path/shape-morphing for constructed logo marks or hand-built illustrations** (`references/logo-sourcing.md`). Measured directly via each library's current CDN "latest" tag, the same one this repo's own install snippets point at: anime.js v4's full bundle — animation engine, ScrollObserver, Draggable, spring physics, *and* the SVG toolset (`svg.morphTo`, `svg.createMotionPath`, `svg.createDrawable`), everything included — is **~118KB minified / ~41KB gzipped**. Matching that same feature set in GSAP means core + ScrollTrigger + Draggable + MorphSVGPlugin + DrawSVGPlugin, which comes to **~179KB minified / ~69KB gzipped** — genuinely, verifiably larger (~34% more over the wire, gzipped). For a page whose brief calls for both scroll storytelling *and* a morphing/drawing SVG mark, anime.js's single bundle is the lighter way to get both.
2. **SVG motion-path/shape-morphing alone, on a page that otherwise doesn't need scroll-triggered motion.** Same tools, same reasoning as above, just without the reveal engine attached — reach for anime.js's SVG toolset directly rather than adding two more GSAP plugin files for one moment on the page.

**Bundle size alone does not justify anime.js for simple reveals with no SVG need — this was checked and doesn't hold up.** The obvious-sounding case ("anime.js is lighter, use it for basic scroll-reveals") was tested and rejected: loaded via a plain `<script>` CDN tag (this project's default, no-build-step pattern), anime.js's bundle is **~118KB min / ~41KB gzip** against GSAP core + ScrollTrigger's **~117KB min / ~46KB gzip** — a wash on minified size, and only a modest ~11% gzip difference, because a plain script tag can't tree-shake away the Draggable/spring/SVG code a reveal-only page never uses. (A project actually using a bundler with anime.js's ESM submodule exports could tree-shake further, but that's a different build setup than the CDN-tag default this skill assumes — not a reason to switch the default.) Reach for anime.js on bundle-size grounds *only* when the SVG toolset is also genuinely needed, per the two cases above.

**Everything else stays on GSAP.** The reasoning that ruled out a full swap: this project has a real, working, tested investment in GSAP already (`assets/gsap-starter.js`, the `data-reveal` convention, the App-shell/marketing motion-track split, `gsap.matchMedia()` as the reduced-motion backbone) — porting all of that gets no payoff for the standard case, since what actually makes a page feel premium is choreography and restraint, not which engine executes the tween. anime.js's `createScope({ mediaQueries })` is a real, working equivalent to `gsap.matchMedia()` — verified, not assumed — so reduced-motion support isn't a blocker where anime.js *is* used. Spring-based draggable micro-interactions (a real gap in current App-shell motion guidance) were identified as a plausible third use case but not built into a starter yet — flagged as open follow-up work, not silently dropped.

If a project's brief calls for anime.js under either scoped case, use `assets/anime-starter.js` — it mirrors `gsap-starter.js`'s `[data-reveal]`/`[data-reveal-group]` convention so a project can use either engine without touching markup. Two real porting gotchas found by hands-on testing, not by reading docs:

- **Scroll-threshold syntax does not carry over from GSAP.** GSAP's `"top 85%"` string means nothing to anime.js's `ScrollObserver` — it silently matches nothing and the element never reveals. anime.js's own syntax (position keywords `top`/`bottom`/`start`/`end`, on both target and container) is different enough that copying a GSAP trigger string is a real, silent failure mode. Use the library's own defaults unless a specific threshold is actually needed.
- **No automatic on-creation visibility check.** GSAP's `ScrollTrigger` checks whether a target is already in view at creation and fires immediately if so. anime.js's `ScrollObserver` only fires `onEnter` on an actual scroll-crossing transition — left alone, anything already above the fold (a hero's own `[data-reveal]` group) sits invisible until the user's first scroll. `anime-starter.js` fixes this by calling each observer's own `handleScroll()` once right after wiring it; any bespoke anime.js scroll animation needs the same explicit initial check.

## Scroll storytelling — for landing/marketing pages that should unfold as you scroll

`gsap-starter.js` covers the baseline (things fade/rise in on scroll). A *storytelling* page goes further: it uses scroll position as a timeline, so scrolling feels like advancing through a narrative rather than paging past static blocks. This is what makes a landing page feel crafted rather than assembled. Build these directly with ScrollTrigger (they're page-specific, so they live in the project, not in the shared starter):

- **Scrubbed reveals** (`scrub: true`) tie an animation's progress to scroll position, so an element draws/moves *as* the user scrolls rather than firing once. Great for a hero visual that assembles, a number that counts up, a path that draws.
- **Pinned sections** (`pin: true`) hold a section in place while its content advances through steps — the classic "one sticky panel, content changes as you scroll" storytelling beat. Use sparingly (one, maybe two per page); pinning everything is disorienting.
- **Sequenced hero timeline**: a `gsap.timeline()` on load with at most four coherent beats — context/navigation → headline → subhead + actions → the single proof visual. Animate the visual as one composition rather than staggering all its internal labels. This preserves the hierarchy established in `references/hero-guidelines.md` instead of making every element ask for attention.
- **Parallax depth**: move background/foreground layers at slightly different scroll rates (small `y` offsets tied to scroll) for a sense of depth — subtle is the whole game; large offsets read as a gimmick.

Keep it coherent with the locked motion feel (`.tastemaker/style-lock.md`): a "premium/confident" project storytells with restraint (slow, smooth, minimal), a "playful" one can be more energetic. And every one of these must degrade under `prefers-reduced-motion` — wrap them in the same `gsap.matchMedia()` pattern `gsap-starter.js` uses, showing the end state without the scroll-driven motion.

## App shell motion — for internal tools, dashboards, and anything that isn't a scroll narrative

The scroll-storytelling track above is the right model for a page the user scrolls through once, top to bottom. It is close to meaningless for a sidebar-plus-topbar internal tool: most of the screen loads once and stays in place while the user works, there is no scroll narrative to tell, and a scrubbed hero reveal or a pinned section has nothing to attach to. Motion is still not optional here (per this file's own "motion should clarify, not decorate" rule), it just answers different questions: what changed, what's about to happen, is this still loading.

- **Panel/tab switches**: a short cross-fade or directional slide (8-12px translate + opacity) tied to the navigation direction, so moving forward and back through the app reads consistently rather than a generic fade every time. Ties to the "page/state transitions" rule below.
- **List/table entrances**: when a view first populates, stagger rows/cards in with the same `data-reveal`/`data-reveal-group` convention `gsap-starter.js` already provides, just triggered on data-load instead of on scroll-into-view, rather than letting the whole table snap into existence at once.
- **State changes**: a KPI ticking to a new value, a status badge changing, a row being added or removed, a field validating. Animate the specific thing that changed, not the surrounding layout. This is what "what changed" from the top of this file actually looks like in an app shell.
- **Loading states, promoted to first-class**: skeleton screens that mirror the real layout, not a generic spinner. This used to be a single bullet under the marketing-oriented guidance below; it earns the promotion because it is the motion moment most internal tools actually need right, and it is a genuinely different problem from a scroll reveal.
- **Draggable, spring-based micro-interactions**: a draggable panel with snap points, a reorderable list row, a snap-to-position control — physics-based release motion reads as more tactile than an eased tween for anything the user directly manipulates with a pointer. See the dedicated section below for which engine and how.

None of this needs ScrollTrigger. `gsap.to()`/`gsap.from()` with the same duration and easing recorded in `.tastemaker/style-lock.md`'s Motion section is enough, wired reduced-motion-aware the same way as everything else in this file.

### Draggable interactions: use whichever engine the project is already on

Evaluated GSAP's `Draggable` + `InertiaPlugin` against anime.js's `createDraggable` + `createSpring` for this specific case — a draggable panel with snap points — the same rigor the original GSAP-vs-anime.js evaluation used (`references/animation-guidelines.md`'s anime.js section above). The finding here is the same shape as that one, for the same underlying reason: **bundle size is a wash between the two options on their own** (GSAP core + `Draggable` + `InertiaPlugin` measures ~116KB minified / ~44KB gzipped; anime.js's full bundle, which already includes its draggable and spring tools, measures ~118KB minified / ~41KB gzipped) — so it is never worth loading a *second* motion engine just to get draggable support. Extend whichever engine the project is already using:

- **GSAP-track projects (the default)**: `Draggable.create(target, { type: "x" | "y" | "x,y", bounds: containerSelector, inertia: true, snap: [...points], onDragEnd })`. `InertiaPlugin` is what makes the release feel like it has real momentum instead of stopping dead where the pointer let go — it's free (see the GSAP-is-the-default section above), so there's no reason to skip it once `Draggable` is in use.
- **anime.js-track projects** (per this file's anime.js section — a page already using anime.js for SVG motion-path/shape-morphing): `anime.createDraggable(target, { x: true, snap: [...points], releaseMass, releaseStiffness, releaseDamping, onSnap })`. `releaseMass`/`releaseStiffness`/`releaseDamping` are anime.js's spring-physics equivalent of `InertiaPlugin` — tune stiffness/damping together (higher damping relative to stiffness settles faster with less overshoot) rather than reaching for `InertiaPlugin`'s more velocity-based feel; they're different physical models, not drop-in equivalents of each other.

**The drag-follow itself is never gated by `prefers-reduced-motion`** — it's direct manipulation tracking the user's own pointer 1:1, not decorative or autoplaying motion, so reduced-motion doesn't apply to it any more than it applies to scrolling itself. What *does* need a reduced-motion branch is the **release/snap settle** — the bouncy, physics-driven motion after the user lets go. Branch it the same way every other animation in this file does (`gsap.matchMedia()` / anime.js's `createScope({ mediaQueries })`): a lower-damping, more visibly springy settle by default, and a critically-damped or near-instant snap (no overshoot) under `prefers-reduced-motion: reduce` — overshoot on release is exactly the kind of motion that reads as uncomfortable for vestibular sensitivity, even though the drag itself is user-initiated.

**Which track applies is a per-screen decision, not a per-project one.** A marketing/landing page uses scroll storytelling; a dashboard, settings screen, or any persistent app shell uses this track instead. A single project can need both (a public landing page plus an authenticated app behind it), in which case each screen gets the track that actually fits it rather than one default applied everywhere. See `SKILL.md` Step 4 for where this branch happens in the build.

## What to animate, and how much

- **Entrances** (page load, scroll-into-view): a small, consistent fade + upward translate (8-16px) is almost always right. Bouncy easing, large distances, or rotation on entrance reads as playful/consumer — only use it if the locked mood (`.tastemaker/style-lock.md`) actually calls for playful. A "premium/confident" project should use a quick, restrained fade (150-250ms, ease-out), not a bounce.
- **Hover/focus states**: fast (100-150ms), subtle (a slight scale, a border/background shift, a shadow lift) — the point is to confirm interactivity, not to perform. Anything longer than ~200ms on hover starts to feel laggy rather than smooth.
- **Loading states**: skeleton screens that mirror the actual layout beat a generic spinner — they set an expectation of what's coming, which is what makes a wait feel shorter. See the App shell motion section above for this promoted to a first-class pattern, not an afterthought.
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
