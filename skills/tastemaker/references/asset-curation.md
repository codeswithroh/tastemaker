# Asset Curation

Use this before Step 3 on landing pages, visual product sites, galleries, launch pages, and any request where the user expects a premium or artistic result.

Good pages do not use assets as decoration. They build a small visual cast, then reuse that cast with changing scale, crop, material, and motion.

## The Asset Cast

Pick 4-6 asset roles before writing markup:

- **Hero anchor:** the main object that proves the product exists. Use a real screenshot, generated hero artwork, product photo, or constructed scene.
- **Mode range:** 3-5 different visual registers that prove the system can change taste, not just recolor one layout.
- **Process artifacts:** files, commands, checklists, contrast matrices, logs, receipts, or annotations that explain how the product works.
- **Human or market proof:** real logos, avatars, demos, repo links, public artifacts, or deployment receipts. Do not invent these.
- **Texture object:** one tactile element such as paper, stone, fabric, poster, card, device, plant, or stamp to keep the page from feeling purely digital.
- **Micro assets:** icons, swatches, cursors, arrows, labels, pins, and small crops used to connect the larger pieces.

If a page repeats one screenshot family more than twice, add another asset role or crop family. Repetition needs a story reason.

## Curation Pass

Create a short asset board in `.tastemaker/reference-board.md` or the style lock:

```markdown
## Asset cast
- Hero anchor:
- Mode range:
- Process artifacts:
- Proof:
- Texture object:
- Micro assets:
- Rejected:
```

For each section, assign one primary asset role. A section with no assigned asset role must be intentionally text-led, such as a manifesto poster.

## Composition Patterns

Use the bundled artifact kit when the project has no mature design system:

- `assets/artifact-kit.css` for artifact boards, proof stacks, mode runways, command strips, swatch rails, and tactile cards.
- `assets/artifact-kit.js` for GSAP helpers that animate artifact boards, mode cards, pinned ledgers, and parallax proof images.

The kit is not a theme. Treat it like composition scaffolding, then map it to the project tokens.

Patterns:

- **Artifact board:** layered screenshots, notes, swatches, and command blocks around one anchor image.
- **Mode runway:** overlapping cards that each show a different aesthetic lane.
- **Process ledger:** dark or calm file cards that explain the system with real paths or commands.
- **Poster break:** one typographic section with 1-2 tiny image fragments.
- **Tactile close:** a physical-feeling object or still-life tied to the brand.

## Asset Quality Gates

- Every important image must have a distinct role. Do not reuse the same poster or screenshot as hero, demo, and proof unless the page is explicitly about that artifact.
- At least one section must show range: different product category, mode, layout density, or mood.
- At least one section must show process: files, commands, scans, or decisions.
- At least one section must show physicality: texture, paper, object, shadow, or material.
- Motion must belong to assets, not only text. Scroll should move, reveal, pin, scrub, or transform the visual cast.
- Captures must be local or deploy-safe. If a static site deploys only `site/`, copy needed assets into `site/assets/...`.

## When To Add A Component Library

For production React or Next apps, prefer a real primitive library for interaction and build the visual kit on top of it:

- Radix or shadcn/ui for dialogs, menus, popovers, tabs, selects, sheets, tooltips, and command palettes.
- Motion or GSAP for choreographed asset movement. Use GSAP for scroll-storytelling landing pages.
- React Aria for complex accessible components when design needs custom structure.

For static marketing pages, do not install a full UI library only for cards. Use `artifact-kit.css` plus GSAP. A heavy component library cannot fix weak asset taste.

## Anti-Patterns

- A whole page made from the same screenshot repeated in different card sizes.
- Decorative screenshots that do not teach anything.
- A mode claim with no visible mode gallery.
- Motion only on opacity while all assets sit still.
- Stock assets that could belong to any AI tool.
- Product claims without visual proof beside them.
