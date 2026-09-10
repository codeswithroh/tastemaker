# Component sourcing — Tastemaker as director, not fabricator

Tastemaker's job is **art direction and coherence**, not reinventing a date picker. Hand-rolling a bento grid, a pricing table, an animated accordion, or a chart from scratch reliably produces something that works but looks half-finished — the exact "AI-built" tell this skill exists to kill.

There is a large ecosystem of production-grade, free, copy-pasteable components. **Use them.** Then spend the design effort on what only a director can do: choosing which parts, enforcing one visual system across them, and cutting what doesn't serve the page.

Read this file at Step 1.5, alongside `references/library-selection.md`. That file covers **behavioral primitives** (dialogs, toasts, drag, virtualization — things that are hard to get *right*). This file covers **visual components and blocks** (heroes, pricing tables, bento grids, charts, marketing sections — things that are hard to make *look finished*). They are complementary; read both.

---

## Step 0 — Detect the stack first. Everything below depends on it.

**This is not optional and it is the most common way this step goes wrong.** Most registries below are React + Tailwind + shadcn/ui. If the target project is static HTML/CSS, a Rails app, SwiftUI, or anything else, `npx shadcn add …` is meaningless and running it (or telling the user to) is a real failure, not a small mismatch.

Check, in this order:

1. `package.json` — is React present? Next.js? Tailwind? What version of Tailwind (v3 vs v4 matters for several registries below)?
2. `components.json` — does shadcn/ui already exist in this project? If yes, its `registries` field is where new namespaces get added.
3. The actual files — `.tsx`/`.jsx` vs `.html`. Existing component conventions.

Then branch:

| Stack detected | What applies |
|---|---|
| **React + Tailwind + shadcn** | Everything in this file. Full registry access. This is the happy path. |
| **React + Tailwind, no shadcn** | Run `npx shadcn@latest init` first (it's additive, not a framework lock-in), then full access. Confirm with the user before adding it to an established repo. |
| **React, no Tailwind** | Registries below mostly won't drop in cleanly (they ship Tailwind classes). Port the *pattern* by reading the component source, not the file. Motion still applies fully. |
| **Static HTML / CSS (no build step)** | **Registries do not apply.** Do not emit `npx shadcn add` commands. What still applies: Motion via CDN, the interface-quality rules, and reading registry components as *reference* for visual treatment you then write in plain CSS. Say plainly that you're porting a pattern rather than installing a component. |
| **Vue / Svelte / React Native** | shadcn-ui-mcp-server supports these (`--framework svelte\|vue\|react-native`). The Tailwind-based registries generally do not. |
| **SwiftUI / Flutter / native** | None of the registries apply. Direction, motion principles, and interface rules still do. |

**Never emit an install command for a stack that can't consume it.** If the project is static HTML and a bento layout is needed, write the CSS grid yourself — informed by how the good registries structure theirs — and say that's what happened.

---

## The registry map (verified, with exact commands)

All of these were checked directly, not recalled. Free/open-source unless marked.

### shadcn-compatible registries (React + Tailwind)

These install real component source into the project (copy-in, not a dependency you can't edit). That's the point: you own and can restyle the code to match the project's locked palette.

| Registry | Namespace / URL | Best for | Notes |
|---|---|---|---|
| **shadcn/ui** (the base) | `npx shadcn@latest add <name>` | The foundation layer: button, input, dialog, table, form, sidebar, chart. Also official **blocks** (dashboards, login, sidebar layouts). | Set this up first. Everything else layers on top. |
| **Watermelon UI** | `@watermelon` → `https://registry.watermelon.sh/r/{name}.json`<br>`npx shadcn@latest add @watermelon/<name>` | 260+ components **and full blocks** — dashboards, login forms, page sections. Broadest single source. | Open source. Categories: inputs, data display, feedback, navigation, layout, charts (Recharts), blocks. **Note the `/r/` path** — Watermelon's own docs print the URL without it, which returns the site's HTML instead of JSON and fails with `Unexpected token '<'`. Verified working path is `/r/{name}.json`. |
| **KokonutUI** | `@kokonutui` → `https://kokonutui.com/r/{name}.json`<br>`npx shadcn@latest add @kokonutui/<name>` | Higher-polish, more *designed* components — the ones with real motion and visual character (e.g. `particle-button`). | **Tailwind v4** + lucide-icons. Verify the project's Tailwind major version before pulling. Utils: `https://kokonutui.com/r/utils.json`. |
| **bklit UI** | `@bklit` → `https://ui.bklit.com/r/{name}.json`<br>`npx shadcn@latest add @bklit/<name>` | **Charts, specifically.** 17+ types: area, bar, line, pie, scatter, candlestick, sankey, heatmap. Plus legends, grids, tooltips, axes, brushes. | Free/open source. Reach for this over hand-rolling any chart. Some components auto-pull `@bklit/shimmering-text`. |
| **lucide-animated** (pqoqubbw) | `https://lucide-animated.com/r/{name}.json`<br>`npx shadcn@latest add "https://lucide-animated.com/r/<name>.json"` | **Icons, specifically — the default icon source on this stack.** 467+ animated Lucide-based icons that play a small motion on hover/trigger instead of sitting static. | MIT. Built on Motion (`motion/react`) — the CLI adds it automatically. Drops a component at `components/icons/<name>.tsx`; import as a PascalCase component (`import { Activity } from "@/components/icons/activity"`), not an inline SVG string. See "Icon precedence" below for when this beats `scripts/fetch_icons.py`. |
| **itshover** | `https://itshover.com/r/{name}.json`<br>`npx shadcn@latest add https://itshover.com/r/<name>.json` | **Icons, specifically — second source.** 186+ animated icons, broader coverage of brand/tech-stack marks (GitHub, Docker, Node, Python, TypeScript, etc.) that lucide-animated doesn't cover as a design-language set. | Apache 2.0. Same Motion dependency and copy-in pattern as lucide-animated. Reach for this when a needed icon (a specific brand mark, a less common action) isn't in lucide-animated's set — don't mix the two for icons that exist in both, to keep one visual language. |

To register a namespace once in an existing project, add to `components.json`:

```json
{
  "registries": {
    "@kokonutui": "https://kokonutui.com/r/{name}.json",
    "@bklit": "https://ui.bklit.com/r/{name}.json",
    "@watermelon": "https://registry.watermelon.sh/r/{name}.json"
  }
}
```

Two things that bite in practice, both hit while wiring this up for real:

- **`shadcn init` overwrites the palette.** It writes its own neutral oklch defaults into the CSS token block, silently replacing a locked palette that was already there. Re-apply the lock's values *after* init, not before — and keep the `--chart-*` and `--sidebar-*` token names it adds, since pulled components reference them. Point them at the locked palette so charts and sidebars land on-brand without per-component overrides.
- **Some registry items prompt interactively** (`utils.ts already exists, overwrite?`). In a non-interactive agent context that hangs. Pass `--yes`, and pipe `y` when a component legitimately needs to overwrite a shared file.

### MCP servers (live component search/retrieval, if configured)

These give the agent *searchable* access rather than a fixed catalog. Check whether they're actually connected in the current session before planning around them — if they aren't, fall back to the registry URLs above, which need no setup beyond the shadcn CLI.

| Server | Install | What it gives |
|---|---|---|
| **shadcn-ui-mcp-server** | `npx @jpisnice/shadcn-ui-mcp-server` (optionally `--github-api-key <token>`, `--framework svelte\|vue\|react-native`) | Source, demos, blocks, and metadata for shadcn/ui v4. Rate limit is 60 req/hr without a GitHub token, 5,000 with one (token needs no scopes). |
| **21st.dev** (`magic-mcp` → now `21st`) | `npx @21st-dev/cli@latest init --client <cursor\|claude-code\|windsurf>`, or HTTP MCP at `https://21st.dev/api/mcp` with an `x-api-key` header | Search 10,000+ React/Tailwind components; tools: `generate`, `get_inspiration`, `search_logo`. | **Requires an API key from 21st.dev/mcp** (old Magic keys are dead). Treat as optional — never make a build depend on it. `search_logo` is genuinely useful alongside `references/logo-sourcing.md`. |

### Motion — the animation engine for *components*

`motion` (motion.dev, formerly Framer Motion) — verified install and usage:

```bash
npm install motion
```

Vanilla JS with **no build step** (this is the important one — it means Motion works on static HTML sites too, where the registries above don't):

```html
<script type="module">
  import { animate, scroll, inView, stagger } from "https://cdn.jsdelivr.net/npm/motion@12/+esm"
</script>
```

Pin a major version rather than `@latest` in anything shipped — the docs say this explicitly.

Real API, verified:

```js
animate(".box", { rotate: 360 }, { ease: "circInOut", duration: 1.2 })
animate(el, { rotate: 90 }, { type: "spring", stiffness: 300 })
animate("li", { y: 0, opacity: 1 }, { delay: stagger(0.1) })

inView("section", () => { animate("section", { opacity: [0, 1] }) })

// scroll-linked (scrubbed): pass an animation into scroll()
const a = animate("div", { transform: ["none", "rotate(90deg)"] }, { ease: "linear" })
scroll(a, { target: document.getElementById("item"), offset: ["start end", "end start"] })
```

### Paper Shaders — real WebGL backgrounds instead of a hand-rolled canvas loop

`@paper-design/shaders` (vanilla, zero-dependency) and `@paper-design/shaders-react` — real animated GPU shaders (mesh gradients, grain gradients, warp, dot orbit, voronoi, metaballs, smoke ring, and more), Apache-2.0, no attribution required. This is the upgrade path for `references/hero-guidelines.md`'s "ambient generative background" — a real WebGL shader instead of a hand-rolled `requestAnimationFrame` canvas blob loop, and the single highest-leverage move for making two builds in the same mood stop looking like the same template with different words, since two hand-drawn CSS radial-glow heroes converge fast and two shader choices genuinely don't.

**Install (React):** `npm install @paper-design/shaders-react`, then use the exported components (`MeshGradient`, `GrainGradient`, `Warp`, `DotOrbit`, and the rest) directly as JSX.

**Vanilla / static HTML, no build step** (verified against the published CDN build):

```html
<script type="module">
  import { ShaderMount, meshGradientFragmentShader, getShaderColorFromString }
    from "https://cdn.jsdelivr.net/npm/@paper-design/shaders@0.0.80/+esm"

  const mount = new ShaderMount(
    document.querySelector(".hero-shader"),   // parent element — the mount creates its own <canvas> inside it
    meshGradientFragmentShader,               // imported from the package, not retyped by hand
    {
      u_colors: [
        getShaderColorFromString("#148568"),  // pull straight from the locked palette
        getShaderColorFromString("#c382d2"),
        getShaderColorFromString("#050b09"),
      ],
      u_colorsCount: 3,
      u_distortion: 0.5,
      u_swirl: 0.3,
    },
    undefined,   // webGlContextAttributes
    prefersReducedMotion ? 0 : 0.3   // speed — 0 renders one static frame and stops the render loop entirely
  )
</script>
```

Pin the exact version in the CDN URL (as shown), the same rule as Motion above. Each shader module exports its own fragment shader constant and a `<name>Meta` object (e.g. `meshGradientMeta.maxColorCount`) — import what a given effect needs rather than assuming every shader takes the same uniform set; some (grain gradient, dithering) also need a generated noise texture via the package's own `getShaderNoiseTexture` helper, which adds a step — **mesh gradient needs neither a texture nor a color-panel setup, making it the simplest reliable default** for a first shader background in a project.

**Picking an effect — vary it the same way palette and macrostructure vary, don't default to mesh gradient every time.** Two candidate effects per mood, alternate between them the way `fetch_icons.py` alternates icon sets:

| Mood | Effects | Character |
|---|---|---|
| Premium / confident | Mesh Gradient, Static Radial Gradient | Smooth, confident, minimal noise |
| Warm / approachable | Waves, Neuro Noise | Organic, soft motion |
| Technical / builder-facing | Grain Gradient, Warp | Structured, textured, data-adjacent |
| Playful / consumer | Metaballs, Dot Orbit | Bouncy, literally playful motion |
| Elegant / editorial | Smoke Ring, God Rays | Restrained, atmospheric, low-saturation |

**Contrast discipline (non-negotiable, same rule as everything else in this skill):** a shader sitting directly behind body text is a contrast hazard — motion and color variance under text is exactly what the color-contract rules in `references/style-tokens.md` exist to prevent. Never place a shader as the literal background of a text block. Instead: confine it to the hero's outer field (a full-bleed layer behind the whole section, `opacity` reduced to roughly 0.3-0.6) and add a **vignette** — a radial-gradient overlay from the locked `bg` color (opaque at the text's center, transparent toward the edges) — so the headline/CTA zone always sits on a near-solid, contrast-safe backdrop while the shader's color and motion show at the margins. Verify the actual rendered text against the gate in `references/anti-slop-checklist.md`, not just the token pairing in isolation — a shader is dynamic, and a contrast check on the static palette doesn't account for a bright frame sitting under a headline.

**Motion does not replace GSAP as this skill's default** (see `references/animation-guidelines.md` — GSAP + ScrollTrigger stays the default engine, with a real tested investment behind it). Use Motion when:
- The project is **React** and components need springs, layout animation, exit animation, or gesture values (this is already `library-selection.md`'s standing recommendation).
- A pulled component **already ships with Motion** as its animation dependency — don't rip it out to re-do it in GSAP. Let the component keep its own engine and match its timing to the project's locked motion values instead.

Never load both GSAP and Motion just to get one effect. One engine per project unless a pulled component forces the second, and if it does, say so. **The one default exception**, now common enough to name explicitly: lucide-animated/itshover icons (below) bring Motion for their own hover/trigger micro-interaction, while GSAP still drives page-level scroll motion. That's two engines with two distinct, non-overlapping jobs, not a mixed-engine mistake — say so in the handoff the same way any second-engine exception gets called out, but don't treat it as something to fix. `scripts/check_component_coherence.py` recognizes this pattern (Motion usage confined to an `icons/` component directory) and won't flag it as a coherence violation; it still flags Motion used for general page/section motion alongside GSAP, which is the real mixed-engine failure.

### Not agent-consumable (documented so it isn't attempted)

- **GrayBlocks** (grayblocks.net) — 5,600+ blocks, but it is **Figma / Framer / Webflow only, and paid**. Its delivery model is one-click copy *inside those design tools*; there is no npm package, registry URL, or API a coding agent can pull from. It's a genuine resource **for the user working in Figma/Framer**, and worth recommending to them for that. It is not something this skill can install. Don't imply otherwise.

---

## Precedence — what to reach for, in order

1. **What's already in the repo.** A healthy existing component beats a new dependency every time. Extend it.
2. **shadcn/ui base** for foundational primitives.
3. **Watermelon** for breadth, including whole blocks/sections.
4. **KokonutUI** for a component that needs visual character and motion out of the box.
5. **bklit** for anything chart-shaped. Always. Hand-rolled charts are a reliable slop tell.
6. **lucide-animated, then itshover, for icons** on any React + Tailwind + shadcn stack. See "Icon precedence" below.
7. **MCP search** (shadcn-ui-mcp / 21st) when you need to *discover* rather than pick from the known list.
8. **Hand-roll** only when: the stack can't consume any of the above, the interaction is genuinely simple (a static section, a plain card), or the project forbids dependencies.

## Icon precedence — animated registries first, static fetch as the fallback

Icons are a component-sourcing decision like any other, not a separate system, and the default changed: **on a React + Tailwind + shadcn stack, lucide-animated and itshover are the default icon source, ahead of `scripts/fetch_icons.py`.** A static SVG that never moves is a missed opportunity for exactly the kind of small, purposeful motion this skill otherwise asks for everywhere else (Step 4's motion non-negotiable) — an icon that plays a short animation on hover reads as considered; the same icon sitting inert next to buttons that do animate reads as unfinished.

1. **Stack check first, same gate as every other registry in this file (Step 0).** These are shadcn-compatible React registries — they do not apply to Vue/Svelte/static-HTML/native projects. On those stacks, skip straight to `scripts/fetch_icons.py` (Iconify), which is stack-agnostic and remains the default there.
2. **On React + Tailwind + shadcn: try lucide-animated first** (`https://lucide-animated.com/r/{name}.json`) — broadest set (467+), matches Lucide's shapes (which shadcn/KokonutUI already lean on), so it stays visually consistent with any non-animated Lucide icons already in the project.
3. **Fall back to itshover** (`https://itshover.com/r/{name}.json`) for an icon lucide-animated doesn't have — its broader brand/tech-mark coverage fills the more common gap. Don't pull the same concept from both; pick one source per icon and keep the whole set from one registry wherever both carry it.
4. **Fall back to `scripts/fetch_icons.py` (Iconify)** only when: the stack can't consume either registry, a specific icon exists in neither, or the project has a hard reason to avoid the Motion dependency. Static Iconify icons stay the right call for non-React builds — that hasn't changed.
5. **Still one icon *family* per project**, same rule as always (`references/anti-slop-checklist.md` gates this) — don't mix lucide-animated icons with a KokonutUI component's own bundled lucide-static icons for the same concept; convert one to match the other. `scripts/check_component_coherence.py` still flags multiple icon packages in the same project.
6. **Restyle to the locked accent regardless of source**, same as any pulled component — these registries ship their own default stroke color; set it to `.tastemaker/style-lock.md`'s accent as part of pulling them in, the same restyle pass every other registry component gets.

---

## The director's actual job — the part that matters most

**Pulling six components from six registries and stacking them produces worse slop than hand-rolling.** Mixed radii, three icon families, four shadow depths, competing motion feels, five type scales. It reads as assembled, because it was.

Sourcing is the cheap part. These are the rules that make it design work:

1. **Restyle every pulled component to the locked palette and tokens.** Registry components ship with their own defaults (`bg-zinc-900`, `rounded-xl`, their own shadows). Rewrite those to `.tastemaker/style-lock.md`'s tokens as part of the same pass. A pulled component still carrying its origin registry's colors is an unfinished component, and it's visible instantly. This is non-negotiable and it's where most of the work goes.
2. **One icon family across the whole project.** On React stacks that's lucide-animated (falling back to itshover for gaps — see "Icon precedence" above), not a static set pulled alongside it out of habit; on stacks that can't consume those registries it's the mood-matched `scripts/fetch_icons.py` set. If a pulled block (KokonutUI, Watermelon) brings its own static lucide icons, convert them to the animated set too rather than leaving a mix of moving and inert icons on the same page. Never ship two icon families — `anti-slop-checklist.md` gates this.
3. **One radius scale, one shadow scale, one spacing scale.** Take them from the lock, not from whichever component happened to arrive first.
4. **One motion feel.** Match every pulled component's durations/easings to the lock's Motion section. A component that springs at 300 stiffness next to one that eases at 200ms linear reads as broken.
5. **Delete what the page doesn't need.** A registry block often ships with a stat row, a logo wall, and a testimonial slot. If the brief has no real numbers and no real testimonials, **cut those slots** — do not fill them with invented content. That's `anti-slop-checklist.md` item 47 (no invented metrics) and it's the most common way pulled blocks introduce fabrication.
6. **Structure still comes from Step 2.5.** Registries supply parts; the macrostructure, narrative arc, and rotation decisions in `references/macrostructures.md` / `references/narrative-arc.md` still govern the page shape. Don't let a block's built-in section order silently become the page's architecture.

**Run the mechanical check before calling the coherence pass done:** `python3 scripts/check_component_coherence.py <changed-ui-paths>`. Rules 1-4 above are otherwise self-reported — easy to state as intent and skip under time pressure, the same way structural rotation and copy specificity used to be before their own mechanical checks existed. This script scans built source for the actual symptoms: more than one icon package imported, more than one motion engine imported (GSAP alongside Motion/Framer Motion), and a spread of hard-coded `box-shadow`/`border-radius` literals that aren't reading from the lock's tokens (a strong signal that shadow/radius scale never got unified after the pull). It won't catch a mismatched *type scale* or a genuinely bad restyle by eye — that's still a human/model judgment call — but it catches the mechanically detectable half of "stitched together from six registries" before it ships.

## Honesty requirement

Say what was pulled and from where — in the handoff, and where it matters, in a code comment. "Pricing table from Watermelon, restyled to the locked palette; chart from bklit" is useful, verifiable information for whoever maintains this next. Implying that pulled components were designed from scratch is the same failure as implying a fallback asset was custom-generated (SKILL.md's honesty rule).

Also state it plainly when a registry **didn't** apply — a static-HTML project where you ported a pattern by hand should say that, not quietly present it as a library install.
