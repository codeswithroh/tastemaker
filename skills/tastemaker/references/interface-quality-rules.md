# Interface quality rules

The craft details that separate a page that *looks* designed from one that *is* built well. `references/anti-slop-checklist.md` catches output that reads as AI-generated; this file catches output that reads as amateur — broken keyboard access, layout shift, dead paste handlers, hardcoded date formats.

Adapted from **Vercel's Web Interface Guidelines** (`github.com/vercel-labs/web-interface-guidelines`), which is the best public codification of this layer. Fetch the current version when it matters — it's actively maintained and this is a snapshot:

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Apply at **Step 4 (build)** and verify at the gate sweep. Framework-agnostic in principle; the syntax examples are React/Tailwind because that's the source's idiom.

---

## Accessibility

- Icon-only buttons need `aria-label`.
- Every form control needs a `<label>` or `aria-label`.
- Interactive elements must work from the keyboard.
- `<button>` for actions, `<a>`/`<Link>` for navigation. Never `<div onClick>`.
- Images need `alt`; decorative images take `alt=""`, decorative icons take `aria-hidden="true"`.
- Async updates announce via `aria-live="polite"` (toasts, validation).
- Semantic HTML before ARIA. Reach for `<button>`, `<a>`, `<label>`, `<table>` first.
- Headings follow `<h1>`–`<h6>` order. Include a skip link to main content.
- Heading anchors need `scroll-margin-top`.

## Focus

- Every interactive element has a visible focus indicator.
- Never remove a focus outline without replacing it.
- Prefer `:focus-visible` over `:focus` (no ring on mouse click).
- `:focus-within` for compound controls.

## Forms

- Inputs need `autocomplete` and a meaningful `name`.
- Correct `type` (`email`, `tel`, `url`, `number`) with matching `inputmode`.
- **Never block paste.**
- Labels clickable via `htmlFor` or by wrapping the control.
- `spellCheck={false}` on emails, codes, usernames.
- Checkbox/radio: label and control are one hit target, no dead zones.
- Submit stays enabled until the request starts; show a spinner during.
- Errors inline next to the field; focus the first error on submit.
- Placeholders end with `…` and show a real example of the pattern.
- Warn before navigating away from unsaved changes.

## Animation

These overlap with `references/animation-guidelines.md`'s motion gate and `scripts/audit_motion.py` — both should pass.

- Respect `prefers-reduced-motion`.
- Animate `transform` and `opacity` only (compositor-friendly).
- **Never `transition: all`** — list properties explicitly.
- Set an intentional `transform-origin`.
- SVG: transform a `<g>` wrapper with `transform-box: fill-box; transform-origin: center`.
- Animations must be interruptible and respond to input mid-flight.

## Typography

- Ellipsis character `…`, never three periods.
- Curly quotes, not straight ones.
- Non-breaking spaces in measurements (`10&nbsp;MB`), shortcuts (`⌘&nbsp;K`), brand names.
- Loading states end with an ellipsis: `Loading…`, `Saving…`.
- Numeric columns and comparisons use `font-variant-numeric: tabular-nums`.
- Headings use `text-wrap: balance`.

## Content handling

- Text containers handle overflow: `truncate`, `line-clamp-*`, or `break-words`.
- Flex children need `min-w-0` for truncation to work at all.
- Design the empty state — don't render broken UI for an empty array.
- Test copy at short, medium, and very long. Real user content is not one line.

## Images

- Explicit `width`/`height` to prevent layout shift.
- `loading="lazy"` below the fold; `fetchpriority="high"` for the critical above-fold image.

> Related real bug worth remembering: setting HTML `width`/`height` attributes *and* a CSS `aspect-ratio` without `height: auto` makes the browser use the literal attribute height. It silently blew up a card layout on this project's own site. Set `height: auto` when `aspect-ratio` drives the box.

## Performance

- Lists over ~50 items: virtualize (`virtua`, or `content-visibility: auto`).
- Don't read layout during render (`getBoundingClientRect`, `offsetHeight`, `scrollTop`).
- Batch DOM reads and writes; never interleave.
- Prefer uncontrolled inputs.
- `<link rel="preconnect">` for CDN/asset domains; `preload` critical fonts with `font-display: swap`.

## Navigation & state

- **URL reflects state** — filters, tabs, pagination, expanded panels belong in query params.
- Navigation uses real `<a>`/`<Link>` so Cmd-click and middle-click work.
- Deep-link stateful UI.
- Destructive actions get a confirmation or an undo window. Never immediate.

## Touch

- `touch-action: manipulation` to kill the double-tap zoom delay.
- Set `-webkit-tap-highlight-color` deliberately.
- Modals/drawers use `overscroll-behavior: contain`.
- While dragging: disable text selection, mark the dragged element `inert`.
- `autoFocus` sparingly — desktop only, one primary input, never on mobile.

## Layout & safe areas

- Full-bleed layouts handle `env(safe-area-inset-*)` for notches.
- No unwanted horizontal scrollbars.
- Flex/Grid over JavaScript measurement.

## Theming

- `color-scheme: dark` on `<html>` for dark themes — fixes native scrollbars and inputs.
- `<meta name="theme-color">` matches the page background.
- Native `<select>` needs explicit `background-color` and `color` (Windows dark mode).

## Locale

- `Intl.DateTimeFormat` and `Intl.NumberFormat`. Never hardcode date or currency formats.
- Detect language from `Accept-Language`/`navigator.languages`, not IP.
- `translate="no"` on brand names, code tokens, identifiers.

## Hydration (SSR frameworks)

- An input with `value` needs `onChange`, or use `defaultValue`.
- Guard date/time rendering against server/client mismatch.
- `suppressHydrationWarning` only when genuinely necessary.

## Interactive states

- Buttons and links need a `hover:` state.
- Hover/active/focus increase contrast relative to rest — see `references/style-tokens.md`'s contrast floor; a hover state that drops below the floor is a real failure, not a style choice.

## Copy

Overlaps with the stop-slop discipline; both apply.

- Active voice: "Install the CLI," not "The CLI will be installed."
- Second person. Avoid first person.
- Numerals for quantities: "8 deployments," not "eight."
- Specific button labels: "Save API Key," not "Continue."
- Error messages state the resolution, not just the problem.
- `&` over "and" only where space is genuinely constrained.

---

## Flag these on sight

`user-scalable=no` or `maximum-scale=1` · `onPaste` + `preventDefault` · `transition: all` · `outline-none` with no `:focus-visible` replacement · `<div>`/`<span>` with click handlers · images without dimensions · big `.map()` with no virtualization · inputs without labels · icon buttons without `aria-label` · hardcoded date/number formats · unjustified `autoFocus`
