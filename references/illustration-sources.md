# Asset sourcing — attribution-free by design

The governing rule: **every default source here requires zero attribution on the finished site.** A visible photo credit or "icons by X" line on a real marketing site is a visual hindrance no shipped product tolerates — so this skill sources only from places whose license lets the asset be used cleanly, with nothing for the end user to see. Sources that *require* on-site attribution (notably Unsplash's API) are deliberately not used as defaults, even though the imagery is good, because that requirement fights the end-user experience.

## Photos — Openverse (default, keyless), Pixabay (optional upgrade)

- **Openverse** — `scripts/fetch_photos.py`, **no API key at all**. Searches 800M+ openly-licensed images and filters by default to CC0 + Public-Domain-Mark, licenses that legally require **zero attribution** anywhere. This is the default specifically because it's keyless — combined with keyless Iconify icons, photos and icons need no accounts, no setup. (Illustrations, below, are the one asset type that may need a single one-time manual step — see that section.) Anonymous rate limits (20/min, 200/day) are ample for build-time fetching. The script tries the full-res source URL first and falls back to Openverse's own image proxy when a source blocks hotlinking, so a download rarely fails.
- **Pixabay** — `--source pixabay` (needs a free `PIXABAY_API_KEY`). More stock-polished, higher-curation, full-resolution imagery; also attribution-free. Use it only when Openverse's more eclectic pool (which mixes in museum/wiki/rawpixel content) doesn't have a clean match for a section. It's an upgrade for a specific need, not the default, precisely because it reintroduces a key.
- **Why not Unsplash** — its imagery is excellent, but its API Guidelines require *visible* photographer + Unsplash attribution wherever a photo appears, enforced as a condition of API access. That's an on-site hindrance with no compliant way around it, so it's off the path entirely.

## Crediting sources in the code, never on the page

CC0/PDM require no attribution — but crediting the creators anyway, as a voluntary thank-you, is a decent thing to do, and it costs the end user nothing if it lives in the source rather than on the page. `fetch_photos.py` writes a `CREDITS` comment block (per-photo creator + source + license + link) into the photos folder for exactly this. Paste it into a code comment at the top of the HTML/CSS. Two rules: (1) it's a comment, never rendered text — a viewer of the live site should never see it; (2) it's genuinely optional for CC0/PDM, so never let it become a reason to add *visible* credit. If a source ever actually requires visible attribution (e.g. Unsplash, or Streamline's free tier), that source simply isn't used here — the code-comment courtesy is for attribution-free assets only, not a loophole for attribution-required ones.

## Illustrations — the vendored `ideagram/` (default)

`ideagram/` is bundled directly inside this skill (not a sibling skill that may or may not be installed — see `ideagram/SKILL.md`) and is the default for every concept-driven section, and for any request that uses the word "illustration"/"illustrate" explicitly. Its current approach: **match a real unDraw illustration from a local library, then recolor it to the project's locked accent** — real illustrator path data, reused and rebranded, rather than an LLM hand-drawing SVG paths from scratch (which reliably produces crude pictograms, per `ideagram/references/undraw-anatomy.md`).

This means illustrations have a genuine **one-time setup step, unlike photos/icons**: the local library (`~/.ideagram/undraw/`) needs 20-30 unDraw SVGs in it before matching works. unDraw's own license permits free, no-attribution personal use and download, but bars *redistributing a compiled collection* of their files — so this library lives on the user's machine, downloaded once from undraw.co, never bundled into this skill or any repo it produces. If the library doesn't exist yet when this step runs, say so plainly and either prompt the user to populate it (fast, one-time, reused across every future project) or fall back to `ideagram/assets/primitives` — a real quality drop, and say so rather than presenting the fallback as equivalent.

Once matched: `ideagram/scripts/recolor_undraw.py` → `ideagram/scripts/validate_assets.py` → save to `design/assets/illustrations/` → reference the actual file in the page markup. See `ideagram/SKILL.md` for the full step-by-step and the Step 4 "compose a custom scene from real components" escape hatch for when no single library illustration fits.

## Icons — Iconify (default)

`scripts/fetch_icons.py` hits Iconify's public API (`api.iconify.design`) — **no API key required**. It draws from permissively-licensed open sets (Lucide ISC, Tabler MIT, Phosphor MIT, Heroicons MIT, Material Symbols Apache-2.0, …) that need **no attribution** in a finished product, and returns SVGs already tinted to the accent color server-side. Pick one set per project and stay in it so every icon shares a stroke weight and corner style — mixing sets is a fast way to look unintentional.

That does not mean the same set every project, though. Pass `--mood <the project's locked mood>` and the script picks a set matched to that mood (premium → heroicons, warm → tabler, technical → lucide, playful → ph, elegant → material-symbols) instead of silently defaulting to lucide regardless of what's being built — that default-to-one-set habit is exactly the icon half of the sameness complaint this file's "through-line" section already warns against for photos and illustrations. Discover names with `--search --mood <mood>`, then fetch with `--icons --mood <mood>`. Name `--set` directly only when the mood mapping is a genuine mismatch for a specific project.

> One nuance to respect: Iconify/its sets are for using icons *in* your design. Don't build a product feature that re-exposes these icons as a *pickable library to your own end users* (an "insert icon" picker in a builder app) — that's a different use some sets restrict. Using an icon directly in a client's UI, which is all this skill does, is fine.

## Manual exception — Streamline

unDraw is no longer a fallback here — it's the primary illustration source via `ideagram/` above. The remaining manual exception is for when even a populated unDraw library has no real fit for a concept (per `ideagram/SKILL.md` Step 2's "don't force a bad match" rule):

- **Streamline** (streamlinehq.com) — larger, more detailed library. Free tier requires visible attribution for open-source sets (premium removes it); their Fair Use Policy also prohibits scripted bulk downloading. Because the free tier *does* carry an attribution string, prefer the unDraw/`ideagram` path when the goal is a clean, credit-free site — reach for Streamline only if the user has a premium license (attribution-free) or explicitly accepts the credit. If the user has Streamline's own official MCP connected, that's the sanctioned automated channel; otherwise it's a manual step.

After any manual download: validate with `scripts/validate_assets.py`, recolor to the locked accent with `scripts/recolor_svg.py` if needed, then reuse across screens.

## Logos — logoyoyo.com (also manual, license unverified)

The project's logo mark is its own sourcing step, not an illustration — see `references/logo-sourcing.md`. Same manual-browse category as the unDraw-library setup above (no API), done once per project. Unlike unDraw (confirmed no-attribution license) and Streamline (confirmed attribution terms), logoyoyo.com's license is unverified — see `references/logo-sourcing.md` for what was actually checked.

## The through-line

Photos (Openverse) and icons (Iconify) are fully automatic, **keyless**, and attribution-free — no setup, every session. Illustrations (`ideagram/`) and logos (logoyoyo.com) both need a one-time manual step (populating the unDraw library; browsing a symbol), but are otherwise attribution-free and, once that one-time step is done, reused across every future project without repeating it. Streamline and the keyed upgrade (Pixabay) exist for fit, not because the defaults are lacking. If you ever find yourself about to add an on-site credit line to satisfy a source's license, stop: that means the wrong source was chosen for this skill's goal. Switch to an attribution-free one instead.

## On sameness across projects

Color and icon set both now vary by project on purpose: the palette is generated fresh per project (`scripts/generate_palette.py`, see `references/style-tokens.md`), and the icon set is chosen by mood instead of always defaulting to one (`--mood` on `fetch_icons.py`, above). Illustrations are recolored to that same generated accent every time, so the color half of an illustration's identity varies with the project too, even though the underlying artwork is matched from a shared local library.

Being honest about what is not solved: the underlying unDraw scene an illustration is matched from can still recur, since the matching in `ideagram/SKILL.md` picks the closest scene from whatever is in `~/.ideagram/undraw/`, and that library is finite. Two projects that both need a "team collaborating" illustration and draw from a similarly-populated library can land on the same base scene, just recolored differently. This is a real, known limitation, not a solved one — populating a broader personal library reduces it, but does not remove it. A genuinely different fix (generating original illustration artwork instead of matching an existing library) is a larger change than fits here.
