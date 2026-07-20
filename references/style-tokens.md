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

## Step B — Apply the matched palette + font pair for that mood

Each mood below is a **matched set**: palette and type were chosen together and should be applied together, not mixed across moods. Every palette uses the five-role model (Text / Background / Primary / Secondary / Accent) — paste the hex string straight into a `realtimecolors.com/?colors=text-bg-primary-secondary-accent&fonts=Heading-Body` URL to preview it live before locking it in. Font names with spaces should have the spaces stripped for the URL param (e.g. "Albert Sans" → `AlbertSans`) — this is the pattern, not independently re-verified for every font on this list, so open the link once and eyeball it before committing.

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
- **Dark mode**: this preset is dark-mode-native (per the mood's own "dark mode by default" convention) — no separate light companion is provided here. If a project genuinely needs a light variant of this mood, treat it as a fresh derivation (swap Background/Text, re-pick a Primary that clears both floors against a light surface) rather than assuming a naive invert of these values will pass — run `scripts/check_contrast.py` on whatever comes out, same as any other new palette.

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
- **Dark mode**: Text `#EFE9DC` · Background `#171310` · Primary `#9C6524` · Secondary `#241E17` · Accent `#D9A54A`. This is the one preset where Primary can't just carry over: light-mode Primary (`#2F2A24`) is a near-black text-adjacent color chosen for a light background, so on a dark background it nearly disappears (1.30:1 vs. the 3:1 visibility floor). `#9C6524` — a darkened version of the mood's own gold Accent — replaces it as the dark-mode Primary. Verified clean.

## When to actually ask instead of auto-selecting

- The idea genuinely spans two moods with no lean (e.g. "a tool that's both a serious analytics dashboard and a fun social feed") — ask which should dominate rather than guessing.
- The user pastes references (images, URLs, screenshots) — that overrides everything above; go straight to `scripts/extract_palette.py` per Step 2 of `SKILL.md`.
- The user explicitly asks to see options before committing.

Otherwise, pick the matched set, write it to `.tastemaker/style-lock.md`, and say in one line which mood you classified the idea as and why — that's enough for the user to redirect if the read was wrong, without making them answer a design questionnaire before seeing anything.

## Broader font-pairing catalog

All fonts referenced above are Google Fonts (loadable via the standard Google Fonts `<link>`/`@import`, no license question). If none of the five matched sets fits a specific project's mood, fontpair.co (fontpair.co/all) is a larger curated catalog of Google Font pairings to browse manually — pick a pairing there and slot it into the same five-role palette structure rather than inventing a sixth mood category ad hoc, unless the project genuinely recurs enough to be worth formalizing as a new preset here.

## Spacing & radius baseline
- 8px base grid unless the mood calls for tighter (dense dashboards: 4px) or looser (editorial/marketing: sometimes 12px)
- Pick one radius scale and stick to it project-wide (e.g. 4/8/16px for sm/md/lg) — mixing arbitrary radius values across components is a fast way to look unintentional

## Contrast floor
Whatever palette gets chosen — including the presets above — verify with `scripts/check_contrast.py <hex1> <hex2>` (or `--palette text=.. bg=.. primary=.. accent=..` for all the pairings that matter at once) rather than eyeballing it. Two separate checks matter, not just one:

1. **Body text vs. background** — 4.5:1 minimum (WCAG AA). This is the pairing people usually remember to check.
2. **Button label vs. Primary fill** — also 4.5:1, and easy to miss because it's a downstream consequence of the palette rather than a value in the palette itself. Two of the five presets above originally shipped a Primary color (a terracotta and an emerald green) that looked fine as a swatch but only cleared ~2.5-3.6:1 with white button text — below the floor. Both were caught and fixed by actually running the numbers instead of trusting the hex value on sight; the same failure mode applies to any new palette derived from a reference image or a user-supplied brand color, so re-run the check rather than assuming a "reasonable-looking" primary is safe for its label color.

All five presets above are now verified: `scripts/check_contrast.py --palette ...` exits clean for each, and **white is the correct button-label color on every one of their Primary fills** (dark-text-on-primary fails for all five — don't default to the mood's text color for button labels, use white). Accent is checked only against the background at the lighter 3:1 UI-component floor, not a full text-contrast check, because its role (hyperlinks, highlights, small pops) isn't a solid button fill the way Primary is.

A beautiful palette that fails either check just looks broken (or illegible), not stylish — this is non-negotiable regardless of mood.
