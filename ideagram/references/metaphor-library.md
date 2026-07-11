# Concept → visual metaphor library

The single hardest part of this whole skill isn't drawing — it's picking *what to draw*. Given a paragraph of content, the temptation is to try to depict everything in it. Don't. Pick the one concrete object or scene that a viewer would recognize in under a second, even with zero context. This file is a starting lookup for that translation; treat it as scaffolding, not an exhaustive catalog — extend it as new concepts come up.

Every row below defaults to **figure + prop together**, per `style-contract.md`'s "default to including a human figure" rule — `figure-pointing.svg` is the usual choice since its gesture reads naturally as presenting/explaining whatever the prop represents. Treat the "prop alone" variant as the exception, for cases where the output needs to work as a small inline icon rather than a scene.

| Abstract concept | Concrete visual metaphor | Primitives to compose |
|---|---|---|
| Idea / innovation / brainstorming | A figure gesturing toward a lit lightbulb | `figure-pointing.svg` + `prop-lightbulb.svg` |
| Security / privacy / protection | A figure gesturing toward a shield with a checkmark | `figure-pointing.svg` + `prop-shield.svg` |
| Communication / feedback / conversation | A figure gesturing toward a speech bubble, or two figures facing each other with a bubble between them | `figure-pointing.svg` + `prop-speech-bubble.svg` |
| Growth / progress / analytics / success metrics | A figure gesturing toward an upward bar chart | `figure-pointing.svg` + `prop-chart-bar.svg` |
| Email / messaging / notifications | A figure gesturing toward (or a `figure-standing.svg` holding) an envelope | `figure-pointing.svg` + `prop-envelope.svg` |
| Speed / launch / momentum / going live | A figure gesturing toward a rocket | `figure-pointing.svg` + `prop-rocket.svg` |
| Remote work / focus / desk work / building something | A figure already sitting at a desk with a laptop — the figure is built into this primitive, no separate pairing needed | `figure-sitting-desk.svg` |
| A single user / person / individual contributor | A standing figure alone | `figure-standing.svg` |
| Collaboration / teamwork | Two `figure-standing.svg` instances, mirrored toward each other (see `style-contract.md`'s mirroring note — a plain side-by-side placement doesn't read as "facing"), with a shared object (chart, speech bubble) between them | multiple figures + one shared prop |
| Real-time co-editing / live presence / multiple people in one document | Two figures flanking a `prop-document.svg`, with two small cursor markers (a simple triangle + a small rounded-rect "nameplate") pointing at different lines of text — use the fill-vs-outline technique from `style-contract.md` to make the two cursors distinguishable without a third color | 2× `figure-standing.svg` (mirrored) + `prop-document.svg` + two small hand-built cursor markers |
| Writing / content / documents / notes | A figure gesturing toward a document with visible text lines | `figure-pointing.svg` + `prop-document.svg` |
| Onboarding / getting started | A standing figure + an open envelope or a lit path forward — pick whichever the actual product does (welcome email vs. guided steps) | context-dependent |
| Data / cloud / storage | Not yet in the primitive kit — until a dedicated primitive exists, compose from simple shapes (rounded rectangle stack) following the style contract rather than skipping the concept, and still pair it with a figure by default |

## How to pick when nothing matches directly

1. Strip the input down to one sentence: "this is fundamentally about ___." If that sentence still has two unrelated nouns in it, the content needs two illustrations, not one overloaded scene.
2. Ask what a five-year-old would draw for this concept with three crayons. That instinct — the single, obvious, almost-too-simple image — is usually the right one. Sophistication in this style comes from restraint, not from adding detail.
3. If the concept is genuinely abstract (e.g. "reliability," "scale," "trust") and no object maps to it directly, pick the closest adjacent concrete thing (trust → shield or handshake; scale → upward chart or multiplying figures) rather than inventing a literal abstraction (there's no good visual noun for "trust" itself — the shield stands in for it).
4. When composing multiple primitives into one scene, keep the same one-focal-point rule from `style-contract.md` — one element (usually the prop, not the figure) should carry the accent color and be the thing the eye lands on first.

## When a new concept doesn't map to anything here

Don't force it into a bad-fit existing primitive. The default move is still to compose a new simple flat shape following `style-contract.md`'s shape language (circles, rounded rects, capsules, flat fill, two colors only) — this keeps the illustration original artwork with zero licensing questions, which is the whole point of this skill existing rather than just pointing people at an existing illustration site. Validate it with `scripts/validate_assets.py`, and add it to `assets/primitives/` if it's likely to recur.

Only if the concept needs a level of detail this flat-primitive system genuinely can't produce well (see `style-contract.md`'s "what this style is not" note), mention to the user that browsing an existing illustration library — unDraw (undraw.co/illustrations) or Streamline (streamlinehq.com/illustrations) — for a closer pre-made match is a reasonable alternative for that one asset. That's a manual, occasional escape hatch, not something this skill automates: both sites explicitly prohibit automated scraping/bulk downloading in their own terms (unDraw's license bans it outright; Streamline's Fair Use Policy states downloading via scripts "does not fall within fair use"), and pulling from either changes the artwork from "generated by this skill" to "sourced from a third party," which the user should make deliberately, not by default.
