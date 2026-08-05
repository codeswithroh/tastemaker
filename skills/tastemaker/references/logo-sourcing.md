# Logo design

Every project scoped in Step 1 with a landing page, nav bar, or favicon needs a logo. First determine whether the project already has one. Search the repository, public assets, manifest, favicon links, brief, and supplied references. An existing mark is a brand constraint, especially if it is already distributed: reuse the exact asset and do not recolor, redraw, or replace it unless the user explicitly asks for a rebrand. If it feels visually disconnected from the new page, adapt spacing, surrounding color, scale, or lockup—not the mark itself.

Only when no identity exists should you create a **mark** (a small symbol) paired with a **wordmark** (the product name set in the locked heading font). The rest of this file covers that cold-start path.

## The one rule that matters most: no letter-in-a-box

A single letter dropped inside a rounded square or circle — `[t]`, `[C]`, a monospace character on a colored tile — is the logo equivalent of the indigo-to-purple gradient. It's what every AI generates when it isn't really trying, and it reads as "placeholder someone forgot to replace," not "brand." **Never ship this as the final mark.** It fails the anti-slop checklist. A real mark is a *symbol* — an abstract geometric form or a single concrete object — that could stand on its own without the letter.

## What a good mark actually is

- **Simple and geometric.** 2-5 primitive shapes (circles, arcs, rounded rects, triangles, a single custom path), flat fill, following the same visual language as `ideagram/references/style-contract.md`. If you can't describe it in one sentence ("two overlapping leaves," "a stack of offset swatches," "an upward arc breaking a circle"), it's too complex for a logo.
- **On-concept, one idea.** Pick the single concept the product is about and find the simplest shape for it — the same discipline as choosing an illustration metaphor in `ideagram/references/metaphor-library.md`, but reduced further. A mindfulness app → a lotus/petal or a calm arc. A design-taste tool → stacked color swatches or a refracting prism (raw input → refined output). A finance tool → an upward path. Don't try to encode the whole product; encode one thing.
- **Recognizable at 16px.** The mark has to survive being a favicon. If its details disappear or it turns to mud at favicon size, simplify until it doesn't. Test this deliberately (render it small), don't assume.
- **Two colors max**, from the locked palette — base + accent, per the style contract. A mark that needs three colors to read is too busy.
- **Balanced negative space.** The shape should sit comfortably in a rough square bounding box with even optical weight — not crammed to one edge, not floating tiny in a large tile.

## How to produce the mark — two paths

**Path A — construct it (the reliable default).** A logo mark is just a very small, very simple illustration, and `ideagram` (vendored, always available) is already built for flat geometric SVG. Compose the mark directly from primitive shapes in the locked palette, following `ideagram/references/style-contract.md`. This is the default because it's automatic, original (no licensing question), on-brand by construction, and doesn't depend on a manual browse step. Build it, then validate with `scripts/validate_assets.py`.

**Path B — an existing brand asset already in the repo.** If the project already has a mark, favicon, or brand kit anywhere in the repository or the brief, that is the mark. Reuse it byte-for-byte (see the preservation rule above) rather than producing a new one.

> **Removed: third-party symbol libraries.** An earlier version of this file recommended a browsable third-party SVG symbol site as an optional manual source. It was removed after a security audit flagged the domain as a phishing risk, and because its license was never verifiable (no terms, license, or FAQ page existed). Do not reintroduce it or a substitute without a verifiable license **and** a clean reputation check — `scripts/check_domains.py` will fail the build on any domain not in the vetted allowlist. Constructing the mark (Path A) has no licensing question at all, which is why it is the default.

## Assemble mark + wordmark

- Set the product name in the project's **locked heading font** (from `references/style-tokens.md`'s matched set) at a weight that balances the mark — don't introduce a separate logo-only typeface unless asked.
- Place the mark left of the wordmark (or above it for a stacked/centered lockup) with generous, consistent spacing. The mark and the wordmark's cap height should feel optically aligned.
- Save the mark SVG and a combined mark+wordmark SVG (or lockup markup) to `design/assets/logo/`.

## Export the favicon set

Once the mark exists, run `scripts/export_favicons.py <mark>.svg --out design/assets/favicons/` for favicon.ico, apple-touch-icon, manifest icons, and an OG-card render — and actually wire them into the page `<head>`. A shipped site with a browser-default blank favicon reads as unfinished. (Degrades gracefully if cairo is missing; the SVG still works as `<link rel="icon" type="image/svg+xml">`.)

## Record it in the style lock

Note the mark's concept, the shapes it's built from, and the wordmark font in `.tastemaker/style-lock.md`'s Assets/Logo line, so later work reuses the same mark instead of reinventing it.

## Honesty

Don't imply a constructed mark is bespoke agency work — it's a clean, fast, legitimate logo, just don't oversell it.
