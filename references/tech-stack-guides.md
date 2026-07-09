# Implementing a style lock per stack

The style lock is stack-agnostic; here's how to turn it into real config/code per framework so tokens stay centralized instead of hardcoded ad hoc across components.

## React / Next.js + Tailwind
- Put palette, radius, and spacing tokens into `tailwind.config.js` `theme.extend` (custom color names matching the lock's role names, e.g. `surface`, `accent`, not raw hex scattered through className strings).
- Load fonts via `next/font` (self-hosted, no render-blocking Google Fonts request) and reference them through a CSS variable wired into the Tailwind font family config.
- Centralize repeated patterns (card, button variants) as components, not copy-pasted className strings — drift creeps in fastest when the same "card" is hand-typed in five files.

## Vue / Nuxt
- Same token approach via a Tailwind config if using Tailwind, or a CSS custom-properties file (`:root { --color-surface: ...; }`) if not — either way, one file is the source of truth, components consume variables/utility classes, never raw hex.

## Plain CSS / no framework
- Define all tokens as CSS custom properties on `:root` (and a `[data-theme="dark"]` override block if dark mode is in scope). Every component references `var(--token-name)`, never a literal color/spacing value, so the lock file and the CSS stay in sync by construction.

## SwiftUI
- Define a `Color` and `Font` extension (or an `.xcassets` color set) mirroring the lock's palette/type roles, so views reference `Color.accent`/`Font.heading` rather than literal `Color(hex:)` calls scattered through views.

## Flutter
- Centralize in a `ThemeData`/`ColorScheme` built from the lock's tokens at app root; widgets pull from `Theme.of(context)` rather than hardcoding colors per widget.

## General principle across all stacks
However it's implemented, there should be exactly one place a token is defined and every component reads from it. If you find yourself writing a hex value or a magic spacing number directly in component code, that's a sign the token setup is being bypassed — go back and add it to the central source instead.
