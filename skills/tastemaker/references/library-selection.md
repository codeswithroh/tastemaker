# Library selection

Use this before adding or hand-rolling complex interface behavior. Tastemaker should raise the floor by picking proven parts for hard interaction problems, then spend design energy on hierarchy, fit, and polish.

**Read alongside `references/component-sourcing.md`.** This file covers *behavioral* primitives — the things that are hard to get **right** (focus management, keyboard access, virtualization, gesture physics). That file covers *visual* components and whole blocks — the things that are hard to make **look finished** (heroes, pricing tables, bento grids, dashboards, charts), and the shadcn-compatible registries they come from. A page usually needs both: a Base UI dialog for correctness, a registry block for finish.

## Decision order

1. Identify the task, not the library the user mentioned.
2. Check `package.json`, lockfiles, and existing imports.
3. Prefer the healthy library already in the repo when it covers the task.
4. If the repo has no answer, pick one library from the table below.
5. Hand-roll only when the behavior is static, simple, or the project forbids dependencies.

Do not replace an existing working library just because this file names a different default. Flag the better choice, then change dependencies only when the user asks or the current library blocks the requested experience.

## Defaults

| Task | Default | Use when |
|---|---|---|
| Accessible dialogs, popovers, menus, selects | Base UI | You need focus management, dismissal, keyboard behavior, anchored overlays, or trigger-aware positioning |
| Command palette | cmdk | Users search, jump, or run actions from a keyboard-first palette |
| Toasts | Sonner | You need stacked notifications with polished entrance, exit, swipe, and timing behavior |
| One-time password input | input-otp | You need paste handling, focus movement, and accessible segmented codes |
| General animation in React | Motion | You need springs, layout animation, exit animation, gesture animation, or interruptible values |
| Simple hover, press, reveal | CSS transitions or GSAP | The motion is predetermined and does not need a spring or gesture state |
| Numbers and counters | NumberFlow | Digits change and should not jitter or reflow |
| Static or dashboard charts | Recharts, or a **bklit** registry chart | Recharts for ordinary product charts with tooltips and responsive layouts. On a shadcn project, prefer pulling a bklit chart (`npx shadcn@latest add @bklit/<name>`) — 17+ types including candlestick, sankey, and heatmap, arriving as editable source already styled to a coherent system rather than assembled from primitives. Not benchmarked head-to-head against Recharts here; the argument is finish and breadth of chart type, not raw capability. Either way: **never hand-roll a chart.** |
| Real-time charts | Liveline | Data streams over time and the chart advances continuously |
| Drag and drop | dnd kit | Users reorder, drag between containers, or need accessible drag behavior |
| Long lists and large tables | Virtuoso | Rendering every row would hurt scrolling or memory |
| Shared client state | Zustand | Multiple distant components read and write the same state |
| Conditional class names | clsx | Classes depend on state but do not deserve a variant API |
| Variant-driven Tailwind components | cva | A component has intent, size, state, or density variants |
| Theme switching | next-themes | A Next.js app needs dark mode without a flash on load |

## Mismatches to catch

- A custom dropdown, dialog, or menu with manual focus handling: use Base UI unless the project already has a strong primitive layer.
- A toast built with a modal or alert component: use Sonner.
- A number ticker built by replacing text each render: use NumberFlow.
- A 1,000-row table rendered directly: use Virtuoso before inventing pagination.
- A hand-built drag system without keyboard behavior or pointer capture: use dnd kit.
- A large component with nested ternary class strings: move to `clsx` or `cva`.

## Motion library boundary

Use CSS for simple state feedback: hover, press, opacity, transform, and small entrances. Use GSAP for scroll storytelling, sequenced page moments, and static marketing timelines. Use Motion for React components that need springs, layout animation, exit states, or gesture-driven values.

Do not install an animation library for a button press. Do not hand-roll a spring.
