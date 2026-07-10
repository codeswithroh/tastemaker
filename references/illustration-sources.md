# Asset sourcing — attribution-free by design

The governing rule: **every default source here requires zero attribution on the finished site.** A visible photo credit or "icons by X" line on a real marketing site is a visual hindrance no shipped product tolerates — so this skill sources only from places whose license lets the asset be used cleanly, with nothing for the end user to see. Sources that *require* on-site attribution (notably Unsplash's API) are deliberately not used as defaults, even though the imagery is good, because that requirement fights the end-user experience.

## Photos — Pixabay (default), Pexels (alt)

- **Pixabay** — `scripts/fetch_photos.py`. The Pixabay Content License requires **no attribution** for downloaded assets used in a site: no caption, no footer credit, nothing. (Its API terms ask for source display only if you're building an app that shows Pixabay *search results* to your own users — a stock-photo browser UI — which a finished website is not.) Use the fetched photos directly. Needs a free `PIXABAY_API_KEY`.
- **Pexels** — equally attribution-free for downloaded photos used in a site (credit "appreciated, not required"). A fine alternative if its library has a better match for a given brief; would need a small `fetch_pexels.py` sibling or the user's own Pexels MCP if connected. Same net result: no on-site attribution.
- **Why not Unsplash** — its imagery is excellent, but its API Guidelines require *visible* photographer + Unsplash attribution wherever a photo appears, enforced as a condition of API access. That's an on-site hindrance with no compliant way around it, so it's off the default path on purpose.

## Illustrations — ideagram (default)

The sibling `ideagram` skill generates original flat illustrations on the spot, tinted to the project's locked accent color. Original artwork → no attribution, no licensing question, no manual step. This is the default for every concept-driven section whenever `ideagram` is available in the session.

## Icons — Iconify (default)

`scripts/fetch_icons.py` hits Iconify's public API (`api.iconify.design`) — **no API key required**. It draws from permissively-licensed open sets (Lucide ISC, Tabler MIT, Phosphor MIT, Material Symbols Apache-2.0, …) that need **no attribution** in a finished product, and returns SVGs already tinted to the accent color server-side. Pick one set per project and stay in it so every icon shares a stroke weight and corner style — mixing sets is a fast way to look unintentional. Discover names with `--search`, then fetch with `--icons`.

> One nuance to respect: Iconify/its sets are for using icons *in* your design. Don't build a product feature that re-exposes these icons as a *pickable library to your own end users* (an "insert icon" picker in a builder app) — that's a different use some sets restrict. Using an icon directly in a client's UI, which is all this skill does, is fine.

## Manual exceptions — unDraw, Streamline

Only when `ideagram` genuinely doesn't fit a section (needs more detail than its flat-primitive style produces) or a bespoke image-gen style is wanted:

- **unDraw** (undraw.co) — free, **no attribution required**, has an on-site recolor tool. Constraint is only that automated scraping/bulk-download is prohibited by its license, so this is a manual browse-pick-download step, not an auto-fetch.
- **Streamline** (streamlinehq.com) — larger, more detailed library. Free tier requires visible attribution for open-source sets (premium removes it); their Fair Use Policy also prohibits scripted bulk downloading. Because the free tier *does* carry an attribution string, prefer unDraw or ideagram when the goal is a clean, credit-free site — reach for Streamline only if the user has a premium license (attribution-free) or explicitly accepts the credit. If the user has Streamline's own official MCP connected, that's the sanctioned automated channel; otherwise it's a manual step.

After any manual download: validate with `scripts/validate_assets.py`, recolor to the locked accent with `scripts/recolor_svg.py` if needed, then reuse across screens.

## The through-line

Defaults (Pixabay + ideagram + Iconify) are all automatic *and* attribution-free — which is what makes a complete, credit-free, single-pass site possible. The manual exceptions exist for fit, not because the defaults are lacking. If you ever find yourself about to add an on-site credit line to satisfy a source's license, stop: that means the wrong source was chosen for this skill's goal. Switch to an attribution-free one instead.
