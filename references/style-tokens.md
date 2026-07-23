# Starter style scaffolding (cold start, no references given)

Use this only when the user has no references to ground on. The goal is to pick a palette + font pairing **automatically from the app idea**, as a matched set — not to ask "what colors do you want?" on every cold start. Only fall back to a direct question when the idea genuinely doesn't lean toward one mood over another (see "When to actually ask" below).

## Step A — Classify the app idea into a mood

Read the user's description of what they're building and match it against these keyword clusters. Most requests contain enough signal (industry, audience, tone words) to classify without asking.

| Mood | Idea signals (industry / audience / tone words) |
|---|---|
| **Premium / confident** | fintech, banking, investing, B2B, SaaS, analytics, enterprise, professional tools, legal, insurance, "for teams," admin/ops dashboard |
| **Warm / approachable** | wellness, health, therapy, coaching, community, parenting, nonprofit, education (general audience), recipes/food, hobby, marketplace for individuals |
| **Technical / builder-facing** | developer tool, API, CLI, infra, devops, database, monitoring, open source, engineering/ops platform, terminal-adjacent |
| **Playful / consumer social** | game, gaming, creator tools, youth/teen audience, dating, music/streaming, meme, social app, anything explicitly "fun" |
| **Elegant / editorial** | publishing, magazine, blog, portfolio, luxury/fashion, jewelry, art gallery, boutique, agency site, anything explicitly "premium but soft" rather than "premium but corporate" |

If the request already states or implies the mood directly (e.g. "premium fintech tool for freelancers," "playful app for teens"), use that instead of re-deriving from the table — the user already answered the question.

**Before locking type, also check the target script.** Mood is one dimension; script is a separate one, and a non-Latin script (Korean, Japanese, Chinese, and others) is not a font-swap inside the same model — it changes the typography model itself. If the PRD, the user's request, or the actual UI copy is in a non-Latin script, stop and read the Non-Latin script typography section below before applying the two-family Latin pairing catalog. Building a Korean product with an English-only font pairing is the same class of mistake as picking a palette that fails contrast — it ships something that doesn't actually work for the real content.

## Step B — Generate a fresh palette for that mood (don't reuse a fixed set)

**The palette is generated per project, not picked from a list.** A fixed catalog of options would mean two similar prompts produce the same site, which is just a new monoculture in five flavors. Instead, run:

```
python3 scripts/generate_palette.py --mood <mood> [--mode light|dark]
```

This produces a **new** palette every run: a base hue chosen within the mood's range, a color-harmony rule for the accent (analogous / complementary / triadic / split / mono), and per-role lightness solved so the required contrast pairings clear their floors by construction (the same target-ratio idea Adobe Leonardo uses, worked in OKLCH so contrast stays predictable). Two projects in the same mood get two genuinely different, legible palettes. Omit `--seed` for a fresh result each time; pass `--seed <n>` only when you need to reproduce one exactly.

The script prints the roles (text, bg, surface, primary, on-primary, secondary, accent, border), a realtimecolors preview URL, and the contrast matrix. Take the matrix output straight into `.tastemaker/style-lock.md`'s Color contract section (see `references/style-lock-format.md`). Pair it with a font set for the mood from the **type pairing catalog** below.

If a generated palette genuinely doesn't fit after a couple of tries (a specific brand constraint, a client's fixed color), fall back to hand-picking, but still run `scripts/check_contrast.py --matrix` on the result and record the legal pairings the same way.

### Mood → type pairing (the fonts stay curated; the color is generated)

Each mood has a font character that pairs with its generated palette. Use these pairings (all Google Fonts, so no licensing question); the hex values under each mood below are **reference anchors** that show the intended character of the mood, not the palette to ship.

| Mood | Type pairing (heading + body) | Alt |
|---|---|---|
| Premium / confident | Unbounded + Albert Sans | Inter + Inter, tight heading tracking |
| Warm / approachable | Zain + Nunito | Epilogue + Baskervville (softer, editorial) |
| Technical / builder | Archivo + IBM Plex Sans (mono reserved for code/data) | IBM Plex Sans + IBM Plex Mono-for-data |
| Playful / consumer | Urbanist + Open Sans | Fredoka + Nunito |
| Elegant / editorial | Gloock + Inter | EB Garamond + DM Mono (accents) |

### Reference anchors (the character each mood aims for, not fixed palettes to ship)

The hex values below are what the generator's mood ranges were tuned to produce the *character* of. Read them to understand each mood's intended feel; do not paste them as the project palette (that is what the generator is for). Each still uses the five-role model (Text / Background / Primary / Secondary / Accent), previewable via `realtimecolors.com/?colors=text-bg-primary-secondary-accent&fonts=Heading-Body`.

### Premium / confident (fintech, B2B SaaS, professional tools)
- **Palette**: Text `#050315` · Background `#FBFBFE` · Primary `#2F27CE` · Secondary `#DEDCFF` · Accent `#433BFF`
  Preview: `realtimecolors.com/?colors=050315-fbfbfe-2f27ce-dedcff-433bff&fonts=Inter-Inter`
- **Type**: Unbounded (headings) + Albert Sans (body) — a bold geometric display keeps it confident without tipping playful. Safer fallback if the display face reads too loud for the product: Inter (headings) + Inter (body), tight tracking on headings.
- **Shape**: flat or hairline-bordered, minimal shadow, 4-8px radius.
- **Avoid**: gradients as a crutch, more than one saturated color, drop shadows for depth.
- **Dark mode**: Text `#F2F1FB` · Background `#0A0A12` · Primary `#5850E0` · Secondary `#17162A` · Accent `#8F87FF` — verified clean (`check_contrast.py --palette ...` exits 0). Primary is lightened from the light-mode `#2F27CE` because button-label contrast isn't the issue here (the light-mode indigo already clears 9.12:1 with white text, independent of page background) — the issue is *visibility*: `#2F27CE` only hits 2.16:1 against the dark `#0A0A12` background, under the 3:1 UI-component floor, so it visually disappears as a button fill. `#5850E0` clears 3.42:1 and still reads as the same indigo family.

### Warm / approachable (consumer, community, wellness)
- **Palette**: Text `#2B2118` · Background `#FBF7F0` · Primary `#B85A38` · Secondary `#F0E4D3` · Accent `#7A8C6E`
  Preview: `realtimecolors.com/?colors=2b2118-fbf7f0-b85a38-f0e4d3-7a8c6e&fonts=Zain-Nunito`
  (Primary darkened from an earlier `#C96F4A` terracotta draft — that shade only cleared 3.59:1 with white button labels, below the 4.5:1 AA floor; `#B85A38` clears 4.61:1 while staying in the same terracotta family.)
- **Type**: Zain (headings) + Nunito (body) — rounded and friendly, legible at body size. Editorial-leaning alt: Epilogue (headings) + Baskervville (serif body/accent) when the product wants a softer, more literary feel.
- **Shape**: larger radius (12-20px), soft shadows acceptable, illustration-friendly.
- **Avoid**: corporate blue, harsh contrast, overly saturated primaries.
- **Dark mode**: Text `#F5EFE6` · Background `#14100C` · Primary `#B85A38` (unchanged — already clears both the label and visibility floors against the dark background, checked directly rather than assumed) · Secondary `#241C15` · Accent `#9BAF8E`. Verified clean.

### Technical / builder-facing (dev tools, infra, CLI-adjacent products)
- **Palette**: Text `#E6E6EA` · Background `#0B0D12` · Primary `#047857` · Secondary `#161A21` · Accent `#34D399`
  Preview: `realtimecolors.com/?colors=e6e6ea-0b0d12-047857-161a21-34d399&fonts=Archivo-IBMPlexSans`
  (Primary darkened from an earlier `#10B981` — that brighter emerald only cleared 2.54:1 with white button labels, well below AA; `#047857` clears 5.48:1 and still reads as "terminal green" against the near-black background. Keep the brighter `#34D399` as Accent, used sparingly for highlights rather than solid button fills.)
- **Type**: Archivo (headings) + IBM Plex Sans (body) + IBM Plex Mono for code, data, timestamps, and short technical labels. Keeping the Plex family across sans and mono holds the cohesive, technical feel, and Archivo carries the display headings. **Do not set long-form body copy in mono.** Monospace body text is a recognizable AI-template tell (see `references/anti-slop-checklist.md`), even for a builder-facing product. Mono earns its place on the code and data it was designed for, not on paragraphs.
- **Shape**: sharp corners or none, visible grid/borders over shadows.
- **Avoid**: playful illustration, rounded-full buttons, pastel colors.
- **Dark mode**: this mood is dark-mode-native (per the mood's own "dark mode by default" convention) — no separate light companion is provided here. If a project genuinely needs a light variant of this mood, treat it as a fresh derivation (swap Background/Text, re-pick a Primary that clears both floors against a light surface) rather than assuming a naive invert of these values will pass — run `scripts/check_contrast.py` on whatever comes out, same as any other new palette.

### Playful / consumer social (games, creator tools, youth-oriented)
- **Palette**: Text `#14042B` · Background `#FFFFFF` · Primary `#4361EE` · Secondary `#7209B7` · Accent `#F72585`
  Extended gradient stops (for hero backgrounds/illustration fills, not flat UI roles): `#3A0CA3`, `#4CC9F0`
  Preview: `realtimecolors.com/?colors=14042b-ffffff-4361ee-7209b7-f72585&fonts=Urbanist-OpenSans`
  This palette is a saturated 5-stop family (sourced from a coolors.co gradient set), not five independent flat roles — treat Primary/Accent as the two colors actually used on solid UI (buttons, links), and the remaining stops as a reusable gradient for hero sections or illustration fills, per the "quiet base to pop against" rule below.
- **Type**: Urbanist (headings) + Open Sans (body) — rounded geometric display, plain legible body.
- **Shape**: large radius, layered shadows/depth acceptable, motion-friendly.
- **Avoid**: making everything loud at once — even playful UI needs a quiet base (the white background here) to pop against.
- **Dark mode**: Text `#F2EEFB` · Background `#0D0620` (deep violet-black, keeps the family's hue rather than going neutral gray) · Primary `#4361EE` (unchanged — clears both floors as-is) · Secondary `#2A0F52` · Accent `#F72585` (unchanged). Verified clean.

### Elegant / editorial (publishing, portfolio, luxury/boutique, agency)
- **Palette**: Text `#211F1C` · Background `#F7F4EE` · Primary `#2F2A24` · Secondary `#E8E1D3` · Accent `#B5762C`
  Preview: `realtimecolors.com/?colors=211f1c-f7f4ee-2f2a24-e8e1d3-b5762c&fonts=Gloock-Inter`
- **Type**: Gloock (headings, serif display) + Inter (body) — classic editorial pairing, serif carries the "considered" feel while the sans body stays fast to read. Alt with a technical edge: EB Garamond (headings) + DM Mono (small caps/accents, e.g. bylines, dates).
- **Shape**: generous margins, minimal or no shadow, thin hairline rules between sections instead of cards.
- **Avoid**: rounded-full buttons, playful iconography, tight line length on body copy.
- **Dark mode**: Text `#EFE9DC` · Background `#171310` · Primary `#9C6524` · Secondary `#241E17` · Accent `#D9A54A`. This is the one mood where Primary can't just carry over: light-mode Primary (`#2F2A24`) is a near-black text-adjacent color chosen for a light background, so on a dark background it nearly disappears (1.30:1 vs. the 3:1 visibility floor). `#9C6524` — a darkened version of the mood's own gold Accent — replaces it as the dark-mode Primary. Verified clean.

## When to actually ask instead of auto-selecting

- The idea genuinely spans two moods with no lean (e.g. "a tool that's both a serious analytics dashboard and a fun social feed") — ask which should dominate rather than guessing.
- The user pastes references (images, URLs, screenshots) — that overrides everything above; go straight to `scripts/extract_palette.py` per Step 2 of `SKILL.md`.
- The user explicitly asks to see options before committing.

Otherwise, pick the matched set, write it to `.tastemaker/style-lock.md`, and say in one line which mood you classified the idea as and why — that's enough for the user to redirect if the read was wrong, without making them answer a design questionnaire before seeing anything.

## Runtime dark/light toggle (when a project needs both modes, not one locked mode)

Everything above locks a single palette for the project. Plenty of real products, especially internal tools, instead ship a light **and** dark mode with an actual switch — that's a different, explicit decision to make at Step 2, not a default, and it changes what gets generated and recorded.

**Generate a true companion pair, not two unrelated palettes.** `scripts/generate_palette.py` draws its base hue, harmony rule, and chroma from the RNG before mode-specific lightness solving branches — so running the **same `--seed` with `--mode light` and `--mode dark`** produces two palettes sharing the same hue family and harmony, each independently solved against its own mode's contrast floors:

```bash
python3 scripts/generate_palette.py --mood warm --mode light --seed 7
python3 scripts/generate_palette.py --mood warm --mode dark --seed 7
```

Both come back as the same triadic warm-orange family — a genuine light/dark companion pair, not two coincidentally-similar runs. Using two different seeds (or letting one run go unseeded) produces two palettes that merely share a mood, not a coherent pair; don't do that for a project that needs a real toggle.

**Verify both, not just the one you happened to look at.** Run `scripts/check_contrast.py --matrix` against each mode's full role set before considering the style genuinely locked. A palette that's clean in light mode and unchecked in dark mode is not "dark mode done," it's dark mode assumed.

**Implementation pattern:**
- Define both role sets as CSS custom properties, one set per mode, swapped via a `data-theme="light"`/`data-theme="dark"` attribute on `<html>` (a class works too; the attribute is more common). Every component reads `var(--text)`, `var(--bg)`, etc. — never a hardcoded hex — so the swap is a single attribute change, not a re-render.
- Default from `prefers-color-scheme` on first load (`@media (prefers-color-scheme: dark)` sets the initial attribute, or a small inline script reads `matchMedia` before first paint to avoid a flash of the wrong theme).
- An explicit user toggle overrides the system default and persists (`localStorage`), read back on load ahead of the `prefers-color-scheme` check so a returning user's choice sticks.

**Record the decision in `.tastemaker/style-lock.md`.** The Palette section's Dark mode line should state plainly whether this project ships one locked mode or both as a runtime toggle — see `references/style-lock-format.md` — so a later screen in the same project doesn't have to rediscover which case it's in.

## Broader font-pairing catalog

All fonts referenced above are Google Fonts (loadable via the standard Google Fonts `<link>`/`@import`, no license question). If none of the five matched sets fits a specific project's mood, fontpair.co (fontpair.co/all) is a larger curated catalog of Google Font pairings to browse manually — pick a pairing there and slot it into the same five-role palette structure rather than inventing a sixth mood category ad hoc, unless the project genuinely recurs enough to be worth formalizing as a new mood here.

## Non-Latin script typography (CJK, Korean specifically)

Everything above — the mood table, the display/body font-pairing model, "tighten display line-height," "tight tracking on headings" — is a Latin-typography model. It does not transfer to a non-Latin script by swapping in a font with the right glyphs; the model itself is wrong for CJK, and applying it wholesale produces broken-looking type even with correct glyph coverage.

### The pairing model doesn't carry over

Latin design pairs two families: a display face for headings, a body face for paragraphs. Korean (and CJK generally) typically runs **one well-built family across a full weight scale** instead — mixing families in Hangul reads as visually inconsistent in a way it doesn't in Latin, because CJK glyphs are denser and more structurally rigid, so a second family's different stroke contrast and proportions clash more visibly than a Latin display/body pairing ever would ([Typotheque on CJK typesetting principles](https://www.typotheque.com/articles/typesetting-cjk-text)).

So for a CJK project, the `.tastemaker/style-lock.md` Typography section records **one family with roles assigned by weight**, not two families:

- Heading/display: SemiBold or Bold weight of the one locked family.
- Body: Regular weight.
- UI chrome (buttons, labels, nav): Medium weight — a distinct step from body without the jump straight to display weight.

### Korean starting point: Pretendard

[Pretendard](https://github.com/orioncactus/pretendard) is the concrete, well-established starting point for Korean UI type — a system-ui-style variable font covering 9 weights (100 Thin through 900 Black), released under the **SIL Open Font License** (free for commercial use, modification, and redistribution, no attribution required).

**It is not on Google Fonts** — this is a real difference from every other font in this file, which loads via a no-license-question Google Fonts `<link>`. Pretendard loads from its own CDN instead:

```html
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable.min.css" />
```

```css
body {
  font-family: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont, system-ui,
    Roboto, "Helvetica Neue", "Segoe UI", "Apple SD Gothic Neo", "Noto Sans KR", "Malgun Gothic",
    "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", sans-serif;
}
```

(Verified against the project's own README at build time this was written — [pretendard's English webfont docs](https://github.com/orioncactus/pretendard/blob/main/packages/pretendard/docs/en/README.md).)

Verify the CDN link resolves and the font actually renders Hangul glyphs before shipping — don't assume the snippet above still points at a live version; check the current recommended embed on the project's own README/CDN page at build time, since CDN paths for variable-font releases can change between versions.

Japanese and Chinese need their own equivalent research rather than assuming Pretendard's Korean-specific choices transfer — Noto Sans JP / Noto Sans SC (both Google-Fonts-hosted, so they don't have Pretendard's CDN wrinkle) are reasonable starting points for those scripts specifically, but have not been vetted here to the same depth as the Korean case, which had a real tester driving it. Say so plainly rather than presenting Japanese/Chinese guidance as equally verified.

### Letter-spacing: don't reuse the Latin "tighten it" instinct

The Premium/confident mood's Latin guidance leans on tight, even negative, tracking for display headings. **Do not carry that instinct into Hangul.** A Hangul syllable block is already a tightly-composed unit of 2-3 stacked jamo; negative tracking compresses the gaps between whole syllable blocks rather than between individual letterforms the way it does in Latin, and it degrades legibility much faster. Default to `letter-spacing: 0` (or Pretendard's own metrics, unadjusted) and only tighten slightly, visually, if the specific weight/size combination looks loose — never reach for the same negative values used in this file's Latin mood guidance.

### Line-breaking: `word-break: keep-all` for UI text

For headings, buttons, short labels, and most app-shell/marketing copy — the kind of short-to-medium text this skill builds most of — set `word-break: keep-all` so Korean text wraps at word boundaries instead of breaking mid-word at arbitrary character boundaries, which is the default and reads as broken. Long-form article or dense-paragraph content is the one place traditional CJK typesetting instead prefers unrestricted breaking; that's a real exception but not the common case for the layouts in `references/component-patterns.md`. ([SymbolFYI's CJK web typography guide](https://symbolfyi.com/guides/cjk-web-typography/), [W3C klreq](https://www.w3.org/TR/klreq/))

### Line-height: looser than the Latin display convention

`references/hero-guidelines.md`'s tightened display line-height (1.0-1.15 floor) is a Latin-specific instruction tied to Latin ascender/descender geometry. CJK glyphs are visually denser and roughly square, so CJK type — including CJK display headings — generally wants more breathing room between lines than the Latin floor allows; verify visually rather than importing the Latin number directly, and expect to land higher than 1.15 even on a tightened display heading.

### Mixed Latin+CJK content

Product names, numerals, and any deliberately-Latin UI strings inside otherwise-Korean copy commonly need slightly different optical sizing than the surrounding CJK text at the same nominal font-size, since Latin glyphs read smaller next to CJK ones at an identical point size — a real, documented CJK-typesetting concern ([Typotheque](https://www.typotheque.com/articles/typesetting-cjk-text)), not something to fix by guessing; check it visually in the actual rendered UI.

## Spacing scale

"8px base grid" is a starting unit, not a spacing system on its own — it doesn't say how much padding a pricing card needs, or how a section's outer padding should relate to what's inside it. Both of those were real, visible failures in generated output (cramped pricing cards, sections that felt sparse in one place and empty in another) traced back to having no actual scale to reach for. This is that scale.

### The token set

Built on a 4px base unit (Tailwind's default, and half of the 8px grid Material Design and Apple's HIG both standardize on — halving cleanly is what makes 4px/8px multiples the industry default rather than an arbitrary choice). Named steps, each with a role, not just a number:

| Token | Value | Use for |
|---|---|---|
| `space-1` | 4px | Hairline gaps: icon-to-label, a badge's internal padding, the tightest relationship on the page |
| `space-2` | 8px | Tightly related elements: a label and its value, stacked lines of related text |
| `space-3` | 12px | Compact component internals: a dense table cell, an app-shell nav row (see `references/component-patterns.md`'s App shell density note — this is the floor for that context, not a violation of it) |
| `space-4` | 16px | Standard component padding: a button's internal padding, a compact stat tile |
| `space-6` | 24px | Group separation: gap between a card's internal sections (heading / body / footer), minimum internal padding for a **content card** (pricing tier, feature card, testimonial) |
| `space-8` | 32px | Spacious card padding for a card carrying real weight (a highlighted pricing tier, a hero showcase panel); gap between distinct groups within a section |
| `space-12` | 48px | Small section padding (a compact/dense-mood project); gap between major elements within a hero |
| `space-16` | 64px | Default section padding (top/bottom) for most moods |
| `space-24` | 96px | Generous section padding (premium/editorial moods, hero sections specifically) |

Skip the gaps between named steps deliberately — 20px, 28px, 40px, 56px are legal but should be rare, reached for only when a specific alignment genuinely needs it, not a default choice. A project that uses six different arbitrary values between 16 and 32 reads as unintentional the same way mixed radius values do.

### The rule that decides which token applies: internal ≤ external

This is the actual governing principle, not the token list by itself. **The space around a group of elements should be equal to or greater than the space within it.** This is Gestalt proximity: elements spaced closer together read as one group, elements spaced farther apart read as separate groups. If a card's internal padding is larger than the gap between that card and its neighbor, the eye can't tell where one card ends and the next begins — which is exactly the "cramped but also somehow unclear" feeling dense, badly-spaced layouts produce.

Concretely: if three pricing cards sit in a row with `space-6` (24px) between them, each card's internal padding should be `space-6` or more, not less. If a section uses `space-16` (64px) of outer padding, the gaps between its internal content groups should generally be smaller than that, not competing with it.

### Card padding minimums by type

Generic "add padding" instructions are how cards end up inconsistent. Use a floor per card type instead:

- **Compact/dense card** (a stat tile, a nav row, an app-shell list item): `space-3`–`space-4` (12–16px) internal padding. This is the one place tighter is correct — see the App shell density guidance in `references/component-patterns.md`.
- **Content card** (a feature card, a pricing tier, a testimonial, anything holding a heading plus body copy): `space-6` (24px) minimum internal padding. This is the floor that was being violated in the pricing-card example that motivated this section — tier name, price, and description sitting close together with no room to breathe.
- **Showcase/hero card** (a hero's proof visual frame, a highlighted/featured pricing tier): `space-8` (32px) or more. The one card in a layout meant to carry the most visual weight should have the most internal room, not the same padding as everything around it.

### Section-level padding

Pick one section padding value for the whole project (from `space-12` through `space-24` depending on density and mood — a "dense/information-heavy" project per `references/style-tokens.md`'s mood-to-density mapping stays at the low end, an "editorial/generous whitespace" project goes higher) and apply it consistently top and bottom on every section. A project that varies section padding per section without a reason reads as unplanned. Column-length imbalance within a section (a tall headline column next to a short card stack) is a separate, real problem, not fixed by more padding — that's tracked and addressed on its own, not by this section.

### Radius scale

Pick one radius scale and stick to it project-wide (e.g. 4/8/16px for sm/md/lg) — mixing arbitrary radius values across components is a fast way to look unintentional, the same failure mode as spacing.

### Recording the scale

Once a project's spacing decisions are made, record the actual tokens used (not just "8px grid") in `.tastemaker/style-lock.md`'s Density & spacing section — see `references/style-lock-format.md` — so the second screen reuses the same scale instead of re-deriving it.

## Contrast floor
Whatever palette gets chosen — including the reference anchors above — verify with `scripts/check_contrast.py <hex1> <hex2>` (or `--palette text=.. bg=.. primary=.. accent=..` for all the pairings that matter at once) rather than eyeballing it. Two separate checks matter, not just one:

1. **Body text vs. background** — 4.5:1 minimum (WCAG AA). This is the pairing people usually remember to check.
2. **Button label vs. Primary fill** — also 4.5:1, and easy to miss because it's a downstream consequence of the palette rather than a value in the palette itself. Two of the five reference-anchor drafts above originally shipped a Primary color (a terracotta and an emerald green) that looked fine as a swatch but only cleared ~2.5-3.6:1 with white button text — below the floor. Both were caught and fixed by actually running the numbers instead of trusting the hex value on sight; the same failure mode applies to any new palette derived from a reference image or a user-supplied brand color, so re-run the check rather than assuming a "reasonable-looking" primary is safe for its label color.

All five reference anchors above are now verified: `scripts/check_contrast.py --palette ...` exits clean for each, and **white is the correct button-label color on every one of their Primary fills** (dark-text-on-primary fails for all five — don't default to the mood's text color for button labels, use white). Accent is checked only against the background at the lighter 3:1 UI-component floor, not a full text-contrast check, because its role (hyperlinks, highlights, small pops) isn't a solid button fill the way Primary is.

A beautiful palette that fails either check just looks broken (or illegible), not stylish — this is non-negotiable regardless of mood.
