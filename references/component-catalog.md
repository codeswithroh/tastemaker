# Component catalog — named archetypes with stable IDs

A macrostructure (`references/macrostructures.md`) is the page shape; this file is the **parts inside it**. Each archetype has a stable ID (so builds and the project log can reference it precisely), a one-line shape, a "use when," a "don't confuse with," and a set of **variation knobs** so the *same* archetype built twice is not identical.

Two axes of variety, both mandatory:

1. **Across pages** — no two consecutive builds (per `.tastemaker/log.json`, see `references/diversification.md`) share the same nav archetype, footer archetype, or hero archetype. Reaching for the mood's *default* on every build is exactly the monoculture this catalog exists to break.
2. **Within a page** — no two sections use the same archetype (two identical feature blocks read as templated), and if you must reuse an archetype across builds, change at least one knob value.

**This catalog is asset-forward on purpose.** tastemaker sources real photos, illustrations, icons, and builds real mockups (Step 3) — so the feature and hero archetypes here *show* (a live-looking UI fragment, a real chart, an annotated capture, a sourced illustration) rather than settling for a heading + two sentences + a decorative icon. That is the show-don't-tell default from `SKILL.md` Step 4, expressed as concrete parts. An archetype that would collapse into a text-wall is marked as such.

**Loading discipline:** read this index, pick your archetype IDs, and carry only those forward — you don't need every archetype's detail in context to build one page. A typical page uses one each of Nav / Hero / Footer, one or two Feature, one Proof, one CTA, and a Section-head treatment.

---

## Navigation — `N#`

- **N1 · Minimal wordmark** — Wordmark left, at most two text links + one action right. *Use when:* the page genuinely has ≤2 destinations. *Don't confuse with:* N2 (dense SaaS bar). ⚠️ **This is the most-recognized AI nav fingerprint when used reflexively** — reach for it only when the page really is that minimal.
- **N2 · Balanced product bar** — Wordmark left · a centered cluster of 3-6 links (some with hover panels) · sign-in + filled CTA right. Frosts/blurs on scroll. The dense, deliberate marketing nav. *Use when:* a real product with several destinations. *Default for* premium/technical/warm product sites (in place of the reflexive N1).
- **N3 · Floating pill** — A rounded, visibly-detached pill sitting a margin off the top, blur backdrop, soft shadow. *Use when:* the hero has a surface/imagery beneath for the blur to sit over; contemporary feel. *Don't confuse with:* N1 (full-width). ⚠️ A pill that's ~95% viewport-wide is just a rounded full-width bar — keep it content-sized.
- **N4 · Editorial masthead** — Full-width header, larger centered wordmark, a thin issue/date/section line, optional inline link row, a rule beneath. *Use when:* Editorial Index / Manifesto / publication feel. *Mood:* elegant, premium.
- **N5 · Side rail** — A thin vertical strip on one edge — rotated wordmark + a few section indicators. Collapses to a menu trigger on mobile. *Use when:* portfolio/editorial, or a docs-adjacent page. *Mood:* elegant, technical.
- **N6 · Command bar / ⌘K** — A visible search pill (or a hidden ⌘K) opening a spotlight of grouped, keyboard-navigable destinations. *Use when:* search/docs-heavy or keyboard-first audiences (dev tools). *Mood:* technical.
- **N7 · Announcement + retract** — A colored promo banner above one real nav; banner retracts on scroll-down, returns on scroll-up, dismissible. *Use when:* a launch/commerce moment with something genuinely worth announcing. *Mood:* playful, warm, commerce.
- **Knobs:** *Position* (static · sticky · frost-on-scroll) · *Link density* (2 · 4 · 5-6) · *Action* (filled CTA · outline · text+arrow · none).
- **Routing (default → also OK):** premium **N2** → N4, N3, N1 · warm **N2** → N7, N3 · technical **N2** → N6, N5, N1 · playful **N7** → N3, N2 · elegant **N4** → N5, N1, N3.

## Hero — `H#`

- **H1 · Statement fold** — A single bold headline (one promise) fills the fold; one primary action; no feature dump. Typography *is* the visual, or one restrained supporting mark. *Use when:* the brand/promise is the message (Manifesto, Poster Fold, single-voice products). *Don't confuse with:* a text-wall — it's one line done large, not paragraphs.
- **H2 · Split demo** — Headline + one-line lede + primary CTA on one side; a real product mockup / annotated capture on the other, often tilted 1-3° or clipped by the viewport edge to imply "there's more." *Use when:* a product whose value is obvious once seen (Product Demo, Feature Stack). *Mood:* technical, premium. **Asset-forward:** the mockup is a real capture or a built UI fragment, never a redrawn fake browser bar (see the no-fake-chrome rule below).
- **H3 · Photographic fold** — One full-bleed sourced photograph carries the fold; headline and caption sit in a corner or below. *Use when:* commerce, food, travel, physical product, brand launch (Gallery Grid, Poster Fold). **Asset-forward:** real Openverse/Pixabay photography from Step 3, never an invented stock look.
- **H4 · Stat hero** — A giant real number (with a short qualifier line that says what it means) anchors the fold. *Use when:* Stat-Led, and the figure is real. *Never* a bare number with no words, and *never* an invented metric.
- **H5 · Illustration centerpiece** — A single sourced-and-recolored `ideagram`/unDraw illustration (or a Tier-A CSS/Tier-B SVG build) sits as the hero's one illustrative element, recolored to the locked accent. *Use when:* an abstract/concept-led product (warm, wellness, community), or a bakery/studio/atelier brief. *Mood:* warm, playful, elegant.
- **H6 · Letter / first-person** — Opens like personal correspondence ("Dear reader,"), no buttons in the fold, reads as a piece of writing. *Use when:* Long-Scroll Narrative, founder-voice, community. *Mood:* warm, elegant.
- **Knobs:** *Display size* (xl · xxl) · *Alignment* (left-bias · centered · right-bias — never all four of eyebrow/headline/lede/CTA stacked on one centered axis) · *Support* (none/typographic · real mockup · photo · illustration · stat).
- **Governing rule:** every hero obeys `references/hero-guidelines.md` — one job, one visual focus, headline sized to word count, line-height above its clipping floor, fits the fold at 1280×800.

## Feature / showcase — `F#`

- **F1 · Alternating bands** — Each feature is a full-width band, text and a real visual alternating sides down the scroll. *Use when:* 3-6 features that each deserve a real mockup/chart/diagram. *Don't confuse with:* a 3-up card grid (the generic tell). **Asset-forward:** every band's visual is real, not a paragraph with an icon.
- **F2 · Bento tiles** — Asymmetric grid of mixed-span tiles, each a small live-looking UI fragment or a stat or a mini-visual. *Use when:* many small features better shown-at-a-glance than sequenced. *Knob:* tiles (4·6·9), spans (regular·irregular·mosaic), border (hairline·accent-corner·none).
- **F3 · Sticky scroll stack** — A pinned pane (the running visual) beside a scrolling column of steps that swaps the visual as you pass each step. *Use when:* a workflow or a multi-part product told in sequence. *Mood:* technical, premium.
- **F4 · Numbered step sequence** — Ordered stages (1 → 2 → 3) flow down the page, each with a heading, a short line, and a small real visual. *Use when:* onboarding, "how it works," a process. **Not** a bulleted list — each step shows a state.
- **F5 · Annotated capture** — One real product capture centre-stage with numbered pins / margin labels pointing at real UI detail. *Use when:* one screen carries most of the value and the detail is the story. **Asset-forward:** a real capture, real annotations.
- **F6 · Spec sheet** — Each row is a feature; hairline rules, tabular figures, editorial restraint. *Use when:* spec-heavy/technical products, comparisons, Catalogue. *Mood:* technical, elegant.
- **F7 · Product card grid** — Each card is a real product (image · name · price · one micro-action), reads like a shop floor. *Use when:* commerce (Gallery Grid, Catalogue). **Asset-forward:** real product photography.
- **Knobs (cross-cutting):** *Visual source* (mockup · chart · photo · illustration · diagram) · *Density* · *Rhythm* (even · irregular).

## Proof — `P#`

(All bind the honesty rule: real logos, real quotes, real numbers, or an honest placeholder — never invented.)

- **P1 · Logo wall (hairline)** — A monochrome row/grid of real customer logos separated by hairlines, no card boxes. *Use when:* credibility is a real conversion blocker and the logos are real.
- **P2 · Pull-quote with marginalia** — One real testimonial in the wide column; attribution + source in the narrow margin. *Use when:* one strong, real quote carries more than five weak ones.
- **P3 · Single huge quote** — One real quote set big, a small-caps attribution beneath, a whole section. *Mood:* elegant, warm.
- **P4 · Stat strip** — A horizontal row of 3-5 real metrics (figure + qualifier), tabular figures. *Use when:* the numbers are real and worth a dedicated band.
- **Knob:** treatment (row · grid · single) · figure weight · attribution position.

## CTA — `C#`

- **C1 · Inline form** — The CTA *is* the form (one email input + "Submit →"), no separate landing. *Use when:* newsletter/waitlist/signup is the one action. *Mood:* warm, technical, playful.
- **C2 · Statement + action** — One large closing line (not a sitemap) with a single primary action beneath. *Use when:* Long-Scroll/Manifesto closes. *Mood:* any.
- **C3 · Typographic link** — Just a word, an arrow, a 1px underline — no box. *Use when:* editorial/minimal pages where a heavy button would break the voice. *Mood:* elegant, premium.
- **C4 · Sticky bottom bar** — A pinned bar holding a CTA + a one-line reassurance. *Use when:* a long page where the action should stay reachable. *Knob:* reveal (always · scroll-up · after-fold).

## Footer — `Ft#`

- **Ft1 · Masthead** — Wordmark + tagline anchor one band; a few links, address/license beneath. *Default for* editorial/premium.
- **Ft2 · Inline single line** — One horizontal line of credits/address/copyright, hairline above, no columns. *Default for* modern-minimal/technical.
- **Ft3 · Index columns** — 3-4 short link columns under small-caps headings. ⚠️ **The 4-column Product/Company/Resources/Legal + social-row footer is an AI fingerprint when used reflexively** — reach for it only on a genuine docs root or hub.
- **Ft4 · Statement close** — One large display sentence dominates (a closing line, not a sitemap); wordmark + minimal links beneath in muted type. *Mood:* atmospheric/premium.
- **Ft5 · Newsletter-first** — The signup form is the primary footer element; everything else is small muted type beneath. *Use when:* audience-building is a real goal.
- **Ft6 · Marquee** — A horizontal infinite-scroll tagline line. *Mood:* playful, brand-forward.
- **Knobs:** wordmark size · separator style · link density.
- **Routing (default → also OK):** premium/elegant **Ft1** → Ft4, Ft2 · technical/minimal **Ft2** → Ft1, Ft5 · playful **Ft6** → Ft4, Ft5 · commerce **Ft5** → Ft3, Ft2.

## Section heads — `S#`

How a section announces itself (a quieter axis, but repeating the same treatment down a page is its own tell):

- **S1 · Hanging** — Heading floats in negative space above the section; no rule, no eyebrow.
- **S2 · Inline** — A small-caps phrase emerges inside the body flow; no spatial break.
- **S3 · Sticky pinned** — Heading stays in view while its content scrolls beneath (orientation aid for long sections).
- **S4 · Stacked eyebrow** — An eyebrow/label sits **directly above** the heading, same column, vertical stack only.
- ⚠️ **Banned: the eyebrow-left / heading-right two-column head** (`01 · THE TOUR` in a left column beside the heading). It is the single most reliable templated-editorial tell. When an eyebrow is used at all (default OFF — most sections don't need one), stack it above the heading in one column. Cap eyebrows at 1-2 per page.

---

## Cross-cutting build rules (bind every archetype)

- **No fake chrome.** Never hand-build a fake browser bar (URL pill + traffic-light dots), fake phone frame, fake code-window, or fake IDE chrome. Use a real screenshot in a `<figure>` (hairline border at most), or omit the chrome. Redrawn chrome is a strong AI tell — the model invented UI the environment already supplies.
- **One icon family per page.** Never mix two icon libraries on one page, and never use an emoji (✨🚀⚡🔥🎯✅) as a feature/step/value icon. Use the mood's fetched Iconify set (`scripts/fetch_icons.py`), a built SVG, or drop the icon and lead with the visual.
- **Asset-forward, not text-wall.** If an F-archetype ends up as heading + two sentences + a decorative icon, it failed — swap in the real mockup/chart/illustration/photo the archetype calls for (Step 3 sourced them). This is the show-don't-tell default made concrete.
- **State every archetype's picks out loud** before building, and stamp them (see `references/diversification.md`): *"Nav: N2. Hero: H2 (split demo, real mockup, left-bias). Features: F1 alternating bands. Proof: P1 logo wall. CTA: C2 statement. Footer: Ft1 masthead."*
- **Mobile:** every archetype collapses to a single column below ~60rem and steps display type down below ~40rem; hit targets ≥44px; no two-line clickable text; no horizontal scroll. See `references/component-patterns.md` and `references/hero-guidelines.md` for the per-type collapse behavior.
