# Logo sourcing — logoyoyo.com

Every project scoped in Step 1 that includes a landing page, nav bar, or favicon needs a small mark (+ wordmark) logo. logoyoyo.com (2900+ SVG symbols, browsable by category — flowers, blocks, blobs, asterisks, animals, etc.) is the default source for the mark half of that logo.

## What it actually is

logoyoyo.com is a browsable SVG symbol library, not an automated logo generator and not an API. There's no key or account requirement to browse it — but selecting one is a manual browse step, in the same category as unDraw/Streamline in `references/illustration-sources.md`, not an auto-fetch like Iconify/Openverse.

**License is unverified — check before shipping commercially.** Unlike unDraw (explicit no-attribution license) or Streamline (documented free-tier attribution requirement), logoyoyo.com has no discoverable license/terms/FAQ page as of this writing — checking the homepage, `/license`, `/about`, and `/faq` all turned up nothing. Don't assert "free to use, no attribution" as if it were confirmed the way the other sources in this file are. Before using a symbol on a real project, check the site itself for licensing terms (footer links, a terms page that may exist under a different path, or a note on the symbol's own page) and tell the user what was actually found — or, if genuinely nothing turns up, say the license is unconfirmed and let the user decide whether that's acceptable for their use case, the same way an unverified-license asset would be treated anywhere else.

## Workflow

1. **Pick a symbol that echoes the project's concept**, the same way a metaphor is chosen in the `ideagram` skill's `references/metaphor-library.md` — one simple, recognizable shape, not a literal illustration of the whole product. A geometric/abstract symbol (blob, asterisk, block) usually reads as more "logo-like" than a literal object; save literal objects for illustrations elsewhere on the site.
2. **Download the SVG** from logoyoyo.com's category browser.
3. **Recolor it to the locked accent** with `scripts/recolor_svg.py --accent "#<accent-hex>" --preserve-dark`, so the mark matches `.tastemaker/style-lock.md` instead of whatever color it shipped in.
4. **Validate it** with `scripts/validate_assets.py` before use, same as any other sourced SVG.
5. **Pair the mark with a wordmark** set in the project's locked heading font (from `references/style-tokens.md`'s matched set) at a weight/size that reads clearly next to the mark — don't introduce a separate logo-only typeface unless the user specifically asks for a custom lettermark.
6. Save the result to `design/assets/logo/` (mark SVG + a combined mark+wordmark SVG if the layout is simple enough to compose directly, otherwise document the pairing so it's reproducible in code).

## When it doesn't fit

If the concept needs something more custom than an abstract symbol — a literal lettermark, a monogram, or a highly specific icon no symbol library covers — say so rather than forcing a mismatched logoyoyo symbol onto the project, and treat a hand-built SVG (following the same flat two-color style as `ideagram`'s style contract) as the fallback, same as the "last-resort" rule in `references/illustration-sources.md`.

## Honesty

Same rule as every other asset source in this skill: don't imply the logo was custom-designed for the brand if it's a recolored library symbol + wordmark. That's a legitimate, common way to get a clean logo fast — just don't overclaim it as bespoke illustration work. And per the license note above, don't tell the user the symbol is "free to use" as settled fact unless you actually found terms confirming that on the site — say what you checked and what you found (or didn't).
