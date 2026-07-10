# Implementing a style lock per stack

The style lock is stack-agnostic; here's how to turn it into real config/code per framework so tokens stay centralized instead of hardcoded ad hoc across components. GSAP (the default motion engine — see `references/animation-guidelines.md`) installs differently per stack too; each section below covers both.

## React / Next.js + Tailwind
- Put palette, radius, and spacing tokens into `tailwind.config.js` `theme.extend` (custom color names matching the lock's role names, e.g. `surface`, `accent`, not raw hex scattered through className strings).
- Load fonts via `next/font` (self-hosted, no render-blocking Google Fonts request) and reference them through a CSS variable wired into the Tailwind font family config.
- Centralize repeated patterns (card, button variants) as components, not copy-pasted className strings — drift creeps in fastest when the same "card" is hand-typed in five files.
- GSAP: `npm install gsap`. Register ScrollTrigger once (e.g. in a small `lib/motion.ts`): `import { gsap } from "gsap"; import { ScrollTrigger } from "gsap/ScrollTrigger"; gsap.registerPlugin(ScrollTrigger);` — then drive it from a `useEffect`/`useGSAP` hook (the `@gsap/react` package's `useGSAP` hook handles cleanup on unmount correctly, which plain `useEffect` easily gets wrong with ScrollTrigger instances).

## Vue / Nuxt
- Same token approach via a Tailwind config if using Tailwind, or a CSS custom-properties file (`:root { --color-surface: ...; }`) if not — either way, one file is the source of truth, components consume variables/utility classes, never raw hex.
- GSAP: `npm install gsap`, register ScrollTrigger in a composable, initialize in `onMounted`, and `kill()` any ScrollTrigger instances in `onUnmounted` — Vue's component teardown won't do this for you.

## Plain CSS / no framework
- Define all tokens as CSS custom properties on `:root` (and a `[data-theme="dark"]` override block if dark mode is in scope). Every component references `var(--token-name)`, never a literal color/spacing value, so the lock file and the CSS stay in sync by construction.
- GSAP: load via CDN `<script>` tags (no build step needed) — `assets/gsap-starter.js` is written for exactly this setup:
  ```html
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
  <script src="gsap-starter.js"></script>
  ```

## SwiftUI
- Define a `Color` and `Font` extension (or an `.xcassets` color set) mirroring the lock's palette/type roles, so views reference `Color.accent`/`Font.heading` rather than literal `Color(hex:)` calls scattered through views.

## Flutter
- Centralize in a `ThemeData`/`ColorScheme` built from the lock's tokens at app root; widgets pull from `Theme.of(context)` rather than hardcoding colors per widget.

## General principle across all stacks
However it's implemented, there should be exactly one place a token is defined and every component reads from it. If you find yourself writing a hex value or a magic spacing number directly in component code, that's a sign the token setup is being bypassed — go back and add it to the central source instead.
