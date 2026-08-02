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

**Motion does not replace GSAP as this skill's default** (see `references/animation-guidelines.md` — GSAP + ScrollTrigger stays the default engine, with a real tested investment behind it). Use Motion when:
- The project is **React** and components need springs, layout animation, exit animation, or gesture values (this is already `library-selection.md`'s standing recommendation).
- A pulled component **already ships with Motion** as its animation dependency — don't rip it out to re-do it in GSAP. Let the component keep its own engine and match its timing to the project's locked motion values instead.

Never load both GSAP and Motion just to get one effect. One engine per project unless a pulled component forces the second, and if it does, say so.

### Not agent-consumable (documented so it isn't attempted)

- **GrayBlocks** (grayblocks.net) — 5,600+ blocks, but it is **Figma / Framer / Webflow only, and paid**. Its delivery model is one-click copy *inside those design tools*; there is no npm package, registry URL, or API a coding agent can pull from. It's a genuine resource **for the user working in Figma/Framer**, and worth recommending to them for that. It is not something this skill can install. Don't imply otherwise.

---

## Precedence — what to reach for, in order

1. **What's already in the repo.** A healthy existing component beats a new dependency every time. Extend it.
2. **shadcn/ui base** for foundational primitives.
3. **Watermelon** for breadth, including whole blocks/sections.
4. **KokonutUI** for a component that needs visual character and motion out of the box.
5. **bklit** for anything chart-shaped. Always. Hand-rolled charts are a reliable slop tell.
6. **MCP search** (shadcn-ui-mcp / 21st) when you need to *discover* rather than pick from the known list.
7. **Hand-roll** only when: the stack can't consume any of the above, the interaction is genuinely simple (a static section, a plain card), or the project forbids dependencies.

---

## The director's actual job — the part that matters most

**Pulling six components from six registries and stacking them produces worse slop than hand-rolling.** Mixed radii, three icon families, four shadow depths, competing motion feels, five type scales. It reads as assembled, because it was.

Sourcing is the cheap part. These are the rules that make it design work:

1. **Restyle every pulled component to the locked palette and tokens.** Registry components ship with their own defaults (`bg-zinc-900`, `rounded-xl`, their own shadows). Rewrite those to `.tastemaker/style-lock.md`'s tokens as part of the same pass. A pulled component still carrying its origin registry's colors is an unfinished component, and it's visible instantly. This is non-negotiable and it's where most of the work goes.
2. **One icon family across the whole project.** shadcn and KokonutUI both lean lucide; if the project's mood-matched set from `scripts/fetch_icons.py` is different, pick one and convert. Never ship two icon families — `anti-slop-checklist.md` gates this.
3. **One radius scale, one shadow scale, one spacing scale.** Take them from the lock, not from whichever component happened to arrive first.
4. **One motion feel.** Match every pulled component's durations/easings to the lock's Motion section. A component that springs at 300 stiffness next to one that eases at 200ms linear reads as broken.
5. **Delete what the page doesn't need.** A registry block often ships with a stat row, a logo wall, and a testimonial slot. If the brief has no real numbers and no real testimonials, **cut those slots** — do not fill them with invented content. That's `anti-slop-checklist.md` item 47 (no invented metrics) and it's the most common way pulled blocks introduce fabrication.
6. **Structure still comes from Step 2.5.** Registries supply parts; the macrostructure, narrative arc, and rotation decisions in `references/macrostructures.md` / `references/narrative-arc.md` still govern the page shape. Don't let a block's built-in section order silently become the page's architecture.

## Honesty requirement

Say what was pulled and from where — in the handoff, and where it matters, in a code comment. "Pricing table from Watermelon, restyled to the locked palette; chart from bklit" is useful, verifiable information for whoever maintains this next. Implying that pulled components were designed from scratch is the same failure as implying a fallback asset was custom-generated (SKILL.md's honesty rule).

Also state it plainly when a registry **didn't** apply — a static-HTML project where you ported a pattern by hand should say that, not quietly present it as a library install.
