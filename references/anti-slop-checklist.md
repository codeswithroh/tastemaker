# Anti-slop gates + pre-emit self-critique

Two checks stand between a build and handoff: a **pre-emit self-critique** (run *before* you finalize, to catch weakness while it's cheap to fix) and the **numbered gate list** (run *after* build, as a precise sweep). These are the specific, recognizable tells that make output read as AI-generated regardless of how good the underlying tokens were — catching them is often higher-leverage than getting the palette exactly right.

---

## Pre-emit self-critique (run before you finalize)

Before handing anything back, score the planned output **1-5 on each of six axes**. Anything **< 3 on any axis triggers a revision pass** before the gate sweep — don't carry a known weakness into a 40-gate review. Two passes is normal; a third is usually a sign the *brief* is underspecified, not the design — re-read it.

| Axis | What you're scoring |
|---|---|
| **Show-don't-tell** | Is each section mostly something to *look at* (mockup, chart, comparison, illustration, real photo) with text as caption — or mostly prose with a decorative icon? This is tastemaker's top principle; score it first. |
| **Philosophy** | Is there a clear *why* — a position this design takes, a reason it looks like *this* — or is it just a competent layout? |
| **Hierarchy** | Can a viewer tell, in 2 seconds, what's primary, secondary, tertiary? Or is everything the same weight? |
| **Specificity** | Does this look like *this* product/brief — or like a generic page that could be anyone's, just in different colors? |
| **Restraint** | Has everything that isn't earning its place been removed — decoration, redundancy, padding-for-padding's-sake, motion that carries no information? |
| **Variety** | Does this share a structural fingerprint (macrostructure, nav/footer/hero archetype) with a previous build in this project? Score by *structural* distance — a palette swap doesn't count as variety. See `references/diversification.md`. |

Record the six scores in the build's CSS stamp so a later run can see them: `/* tastemaker · critique: ShowTell 5 · Phil 4 · Hier 5 · Spec 4 · Restr 5 · Var 5 */`.

---

## The gate list (run after build)

Run through these before handing back any generated UI. Every answer must land on the safe side. **Gates are universal unless a *Mood note* scopes them** — tastemaker's five moods are premium, warm, technical, playful, elegant (from `references/style-tokens.md`). A mood note loosens or tightens a gate for a specific mood; where there's no note, the gate binds every mood.

### Show, don't tell & structure

1. **Shows, doesn't tell — visuals carry meaning, not paragraphs.** Go section by section: is each one mostly something to *look at* (a UI mockup, a chart, a comparison, a diagram, a numbered visual flow, a stat callout, an illustration) with text as its caption — or is it mostly prose with a decorative icon? A page where most sections are heading-plus-two-sentences-of-explanation is the text-wall failure mode, and it reads as generic even with perfect tokens. Replace explanatory paragraphs with the thing they describe: "fast analytics" → an actual chart; "simple 3-step setup" → three visual panels; "powerful editor" → a mockup of the editor. Text stays only where a visual genuinely can't carry it (headline, short subhead, caption, CTA). This is the highest-leverage anti-slop check there is — a beautiful palette on a wall of text still reads as AI slop.
2. **Structure is a named macrostructure, not the generic template.** The page is one of `references/macrostructures.md`'s named shapes, not the reflexive hero → 3-feature-cards → testimonial → CTA → footer rhythm that reads as "an AI built this" even with a perfect palette. Within one page, no two sections use the same archetype from `references/component-catalog.md`.
3. **Structure differs from the last build.** The build carries the CSS stamp and a `.tastemaker/log.json` entry (`references/diversification.md`), and its macrostructure + nav + footer + hero archetypes each differ from the last build's per the rotation rule. Reaching for the mood's default nav/footer on every build is the specific failure this catches.
4. **No generic-template chrome tells.** Nav isn't the reflexive wordmark-left + inline-links + button-right minimal bar unless the page genuinely has ≤2 destinations (reach for a real product bar instead); footer isn't the reflexive 4-column Product/Company/Resources/Legal + social-row unless it's a genuine docs root; no eyebrow-left/heading-right two-column section head (stack the eyebrow above the heading); no hand-drawn fake browser/phone/IDE chrome (use a real screenshot or omit — the environment already supplies real chrome). See `references/component-catalog.md`'s cross-cutting rules.
5. **One intentional rule-break exists.** The hardest gate, and the most important. A design where everything sits on the grid, evenly spaced and perfectly safe, reads as generated even when every token is right. Human-authored work usually has one deliberate break: an element that bleeds past its column, an oversized number, an asymmetric moment, a bit of tension or delight the system didn't require. Find the one intentional break that makes this feel made by a person. If there isn't one, the page is probably too safe.

### Hero & logo

6. **Hero passes the five-second and subtraction tests.** In five seconds, can a new visitor identify the product, its main value, and the primary action? Then remove every hero element that doesn't improve one of those answers. The default budget: one optional eyebrow, one headline, one short subhead, one primary CTA, at most one secondary CTA, one focused visual. Process rails, metric sidebars, floating proof badges, decorative stamps/orbits, file footers, and multiple competing mockups belong below the fold unless the product truly can't be understood without one.
7. **Hero fits the fold and sizes to its copy.** At 1280×800, the headline, lede, and primary CTA are all visible without scrolling; the headline is sized to its word count and its line-height clears descenders (see `references/hero-guidelines.md`). *Mood note: elegant/premium may run a taller art-directed statement fold, but even then the first screen must read as a complete, deliberate composition, never a headline sliced by the fold.*
8. **Hero motion preserves the hierarchy.** The entrance sequence reveals the message and focused visual in at most four coherent beats. It doesn't animate every internal label independently or use decorative motion that competes with the headline.
9. **Hero isn't centered-everything.** The eyebrow, headline, lede, and CTA are not all stacked on one centered vertical axis — pick at most two centered elements and break alignment for the rest (eyebrow or CTA sits off-axis). *Mood note: playful and elegant-narrow may center the hero when the canvas itself is the design, but even then the eyebrow or CTA sits off-axis.*
10. **Logo is a real mark, not a letter in a box.** A single letter set inside a rounded/colored square or circle is the logo equivalent of the indigo gradient — the instant "AI generated this" tell. The mark is a simple, memorable geometric symbol (or a recolored library symbol per `references/logo-sourcing.md`), recognizable at 16px, paired with a wordmark in the locked heading font — not a monospace/system letterform dropped in a colored tile.
11. **Existing brand assets were preserved.** If the repository or brief already contained a logo/favicon/brand kit, the build reuses it unchanged unless the user explicitly requested a rebrand. Visual mismatch is a styling problem, not automatic permission to replace a distributed identity.

### Color & contrast

12. **Not the default gradient.** Indigo-to-purple (or blue-to-cyan) diagonal gradients on hero sections/buttons are the single most recognizable "AI made this" signal — including a `background-clip: text` gradient headline, which no mood allows. If the locked style didn't call for a gradient, don't add one out of habit.
13. **Contrast checked for every pairing used, not just body-on-background.** Body text vs. its background hits 4.5:1 (WCAG AA), verified against the real hex values. But that's not enough: check the palette *as used*. Run `scripts/check_contrast.py --matrix ...` to get the legal-pairings set, and confirm every pairing the build actually introduced (a badge fill with its label, a disabled state, a hover, a state-carrying border) is in the text-safe or UI-safe list for its purpose. A palette color used as a fill with white text is the classic miss: it can pass body-on-background and still be illegible as a button. See `references/style-lock-format.md`'s Color contract. Purely decorative hairline borders are exempt from the 3:1 floor; a border that's the only thing conveying state is not.
14. **The contrast failures that ship most often.** Fail on any: **button text ≈ button fill** (text color and fill within ~5% lightness in OKLCH — the black-on-black bug where the model forgot the on-fill color); **a dark section left with ink-on-ink** (any panel with OKLCH lightness < 50% must also swap its text to a light color in the same rule, and nested children must inherit it); **an accent used as a text-bearing fill with no verified on-accent color**. These are the real-world failures a single body-on-bg check misses.
15. **Neutrals are tinted toward the anchor hue, not flat grey.** Pure `oklch(... 0 ...)` neutrals read as flat and disconnected from the palette. *Mood note: technical (and any deliberately monochrome/minimal build) may use zero-chroma neutrals — the Stripe/Linear school; every other mood tints neutrals toward the anchor hue.*
16. **Accent stays an accent (~≤5% of any viewport).** If the accent covers more than ~5% of a screen by area (solid fills, large accent headings, full-bleed accent bands), retreat — accent is for emphasis, not filling. *Mood note: playful may run a higher accent footprint when the color energy is the point.*
17. **Nothing contradicts the "Do not" list** in `.tastemaker/style-lock.md`, if the project has accumulated specific rejections.

### Spacing & layout

18. **Spacing follows the scale, and internal padding never exceeds external gaps.** Per `references/style-tokens.md`'s Spacing scale: content cards (pricing tiers, feature cards, testimonials) have a real internal-padding floor (`space-6`/24px). Check the relationship, not just raw numbers: a card's internal padding ≤ the gap between it and its neighbors — if padding is *larger* than the space around it, the layout reads as cramped inside and empty outside at once. Every gap/margin/padding value is on the named scale; an arbitrary `padding: 17px` is a tell.
19. **Two-column sections have a deliberate column-balance treatment.** If one column (a headline block) is visibly taller than the other (a card stack, a short label list), it was vertically centered, filled with a real supporting element, or capped to match — not left to trail into empty space. A pricing section with three cards clustered at the top and dead space beneath them is this failure, concretely. See `references/component-patterns.md`'s Column balance section.
20. **Section-to-section separation is one consistent mechanism.** Every section boundary uses the same treatment (alternating tint, hairline divider, or fixed padding alone) recorded in the style lock — a page that mixes them boundary to boundary reads as unplanned.
21. **Density matches the mood.** A premium/confident project shouldn't be cramped and cluttered; a dense/information-heavy dashboard shouldn't have so much whitespace that scanning takes longer than it should.
22. **No horizontal scroll at any width 320-1920px.** `overflow-x: clip` (not `hidden`, which breaks `position: sticky`) on both `html` and `body`; any `grid-template-columns` track holding an image uses `minmax(0, 1fr)`, never bare `1fr` (bare `1fr` takes the image's intrinsic width as its floor and blows past the viewport on phones); display headers set `overflow-wrap: anywhere; min-width: 0` so long compound words break instead of overflowing.
23. **No two-line clickable text.** No button label, primary nav link, footer link, tab label, breadcrumb, or CTA wraps to two lines at any width 320-1920px — it reads as a styling error, not intent. Fix by shortening the label, `white-space: nowrap` + parent reflow, or collapsing the nav into a menu. Hit targets ≥44×44px below 40rem.

### Motion & microinteractions

24. **Not static.** GSAP + ScrollTrigger (`assets/gsap-starter.js`) is wired for scroll-reveal, staggered entrances, and hover/press feedback — a finished page with zero motion is a skipped step, not a minimalist choice. Check for it explicitly. (App-shell screens get the App-shell motion track instead of a scroll timeline — see `references/animation-guidelines.md`.)
25. **No `transition: all`.** Name the specific properties that transition. `transition: all` animates layout and paint properties you didn't intend and is a reliable tell.
26. **Animate only `transform` and `opacity`.** Never animate `width`, `height`, `top`, `left`, `margin`, or `padding` (they trigger layout on every frame). Motion that needs to move something uses `transform`.
27. **No uniform hover-scale, no stacked hover effects, no bouncy easing on UI state.** No `hover:scale-105` applied across unrelated elements; no single element carrying translate + scale + shadow + color at once; no overshoot/bounce easing (`cubic-bezier(0.34, 1.56, …)`) on buttons/modals/tooltips — reserve overshoot for genuinely physical interactions. Use the named easings, not the browser default `ease`.
28. **Focus ring appears instantly and is visible.** Every interactive element has `:focus-visible` with a ring at ≥3:1 contrast, and the ring **never** fades/transitions into existence — keyboard users need it immediately.
29. **Every motion has a `prefers-reduced-motion: reduce` fallback.** Spatial motion collapses to a ≤150ms opacity crossfade, not nothing-and-not-full-motion. `gsap-starter.js` handles this via `matchMedia`; bespoke timelines branch the same way.
30. **Motion carries information, and there's not too much of it.** Prefer silent success over a celebratory toast for an effect the user can already see; prefer optimistic update + Undo over a confirmation dialog; hover-tooltips delay ~800ms, focus-tooltips 0ms. If removing an animation wouldn't lose the user any information, remove it — most pages have too much motion, not too little.

### Typography

31. **No emoji as icons.** Emoji standing in for icons in a "real" product UI is an instant tell. Use the mood's fetched Iconify set, a built SVG, or lead with the visual.
32. **Body copy is not set in a monospace face.** Mono/semi-mono for paragraph text reads as "developer template." Reserve mono for code, data, timestamps, and short technical labels. Holds even for a technical mood — see the note in `references/style-tokens.md`.
33. **Headline line-height is tightened but never below its floor.** Tighten as size grows, but 1.0 is the floor for a bold, large-clamp display headline — below it (e.g. 0.87), descenders and punctuation touch the line below. Verify visually at the actual weight/size, not by reading the CSS number. (For non-Latin scripts, the floor is higher — see `references/style-tokens.md`'s Non-Latin section.)
34. **No italic headers.** Headings and display type are roman (`font-style: normal`). An italicized emphasis word inside an upright heading (`Built to <em>think</em>`) is one of the most reliable AI tells; so is an all-italic display face. Carry emphasis with weight, accent color, or a drawn underline. Italic survives only as body-copy emphasis inside running paragraphs.
35. **At most three font families on the page.** Display + body + at most one outlier (wordmark / hero stat / pull quote), and the outlier appears in at most two slots. Same family at different weights counts once. A fourth family — or an outlier used as a third body font — is slop.

### Assets, states & honesty

36. **Not asset-empty.** Every section that calls for real photography has a real photo, every concept-driven section (mission, values, feature explainers) has an illustration, and icons are real fetched icons — not flat color blocks, emoji, or placeholders. All present in this pass, not deferred.
37. **Assets share one visual DNA.** Multiple icons/illustrations in a batch visibly belong to the same family (consistent stroke width, consistent color treatment), not independently sourced. One icon library per page — never two mixed.
38. **SVG assets pass `scripts/validate_assets.py`.** A malformed SVG (classically a `--` inside a comment) reads as normal text but renders broken in strict browsers — check by parsing, not by reading the source.
39. **Every chart/graph card has a caption, and its geometry was actually looked at.** A chart with axis labels but no title is still unlabeled — state what it shows in one line, and connect it to any related stats nearby. `validate_assets.py` only confirms well-formed XML; before shipping, render the chart and visually confirm the marks are internally consistent — a trend line spans the plotted range, bar heights reflect their labeled values, segments sum to a sensible whole.
40. **Interactive states exist.** Hover / `:focus-visible` / `:active` / disabled / loading states are specified, not left to browser defaults. Inputs specifically: border-width stays constant across states (state goes to color/outline/shadow, never `border-width` — it shifts layout); disabled is signalled by three channels (opacity + `cursor: not-allowed` + the native attribute), not opacity alone; input height matches adjacent button height.
41. **Real content, not lorem-ipsum-adjacent placeholders**, wherever the PRD gives enough to write real copy. "Lorem ipsum," "Sample text," and placeholder names ("Jane Doe," "Acme," "Nexus") read as unfinished even in a first draft.
42. **No invented metrics or fabricated proof.** Any quantitative claim — "10× faster," "trusted by 50,000+ teams," "+47% conversion," "99.9% uptime" — that the user didn't supply and the model made up to fill a stat-led layout or proof bar is slop the moment it's invented. Replace with a real number, an honest `—` + "metric to confirm" placeholder, or a section that doesn't need the proof slot. Same rule for testimonials, logos, and case-study counts.

### Token & honesty discipline

43. **No mid-render token improvisation.** Every color and every `font-family` in the artifact references a named token (`var(--color-accent)`, `font-family: var(--font-display)`). An inline hex / `oklch()` / `rgb()` value, or a `font-family: "Some Font"` that bypasses the token block, means the model picked the palette then freestyled past it. Lift the value into the token block as a named variable, or replace it with an existing token.
44. **No attribution hindrance anywhere on the page.** No "Photo by …," no "Icons by …," no visible credit line. The default sources (Openverse CC0 photos, ideagram illustrations, Iconify icons) are attribution-free by license — a *visible* credit means an attribution-requiring source slipped in; swap it. Voluntary source credits belong in a code comment (the `CREDITS` block `fetch_photos.py` writes), never rendered as page text.
45. **Honest about fallbacks.** If asset generation fell back to curated icons + code-native visuals because no image-gen tool was available, that's stated plainly, not implied to be custom-generated.

---

## Generic aesthetic tells (the "AI taste" cluster)

The gates above catch process failures: a missing asset, wrong contrast, a wall of text. This group catches something harder. A page can pass every gate and still read as generated, because its visual language is the safe, generic, modern default one-shot output keeps reaching for. Treat these as reflective prompts, not just boxes.

46. **Not the same pill eyebrow on every section.** The little rounded label above a heading — often with a leading dot or trailing hairline — is a template signature. Once is fine; the identical treatment on every section is a tell. Vary how section context is signalled, or drop the label where the heading already carries it.
47. **Semi-brutalist is a deliberate choice, not the reflex.** Hairline borders instead of shadows, flat fills, high-contrast mono, sharp/minimal radius — a legitimate style when it fits the product, a tell when it's the house default applied regardless of mood. Ask whether this aesthetic actually fits *this* product, or whether it's just the safe modern look reached for again.
