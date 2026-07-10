# Illustration sources, and keeping Unsplash attribution honest

## Priority order

1. **`ideagram` skill** — original artwork generated on the spot, matched to the locked accent color, zero manual steps, zero licensing gray area. Default whenever it's available.
2. **unDraw or Streamline** — human-assisted fallback, used only when `ideagram` isn't available or its flat-primitive style genuinely isn't the right fit for what a section needs. Neither is "the" fallback over the other — pick whichever's actual illustration style is the closer visual match for the project. Both require the same one-time manual step and both explicitly prohibit automated bulk downloading; see below for why, and what stays compliant.
3. **Image-generation tool + custom style**, or **code-native fallback** — covered in `SKILL.md`'s Step 3, for when neither of the above fits.

## unDraw

- **License**: free for commercial and personal use, no attribution required for their standard sets.
- **What's prohibited**: automated scraping or bulk downloading — their license explicitly excludes "automated and non-automated ways to link, embed, scrape, search or download the assets without consent," and a prior third-party CDN mirroring their catalog was shut down over exactly this.
- **Compliant flow**: ask the user to spend a minute at undraw.co/illustrations, use unDraw's own built-in recolor tool to tint their pick to the locked accent color, then drop the downloaded SVG into `design/assets/`. Everything after that (validation via `scripts/validate_assets.py`, reuse across screens) proceeds automatically.

## Streamline

- **License**: free tier permits commercial use with no per-project asset cap, but requires visible attribution (credited, linked to streamlinehq.com) for open-source/Creative-Commons sets. Their Premium plans remove the attribution requirement.
- **What's prohibited**: their own Fair Use Policy states plainly that "downloading a high volume of assets with the help of scripts or automation tools does not fall within fair use," and can lead to account suspension — so this skill does not scrape streamlinehq.com or guess at undocumented API calls. Streamline does offer an official API/MCP for developers, but their public docs don't expose enough concrete technical detail (endpoints, auth) to wire up here with confidence — if the user has Streamline's own MCP connected in their session, use its tools directly (that's the sanctioned channel); otherwise, treat this the same as unDraw.
- **Also prohibited**: using Streamline assets as selectable assets exposed to *other* end users inside a product you're building (e.g. a "pick your icon" feature in a website builder or Canva-style app) — that's a distinct restriction from using an asset directly in a client site's design, which is what this skill does. Don't extend usage into that territory.
- **Compliant flow**: ask the user to browse streamlinehq.com/illustrations (or use Streamline's official app/MCP if they have it), pick and download whatever matches the project's style, drop the SVG into `design/assets/`. If the set requires attribution, add a small, unobtrusive credit + link to streamlinehq.com near the illustration or grouped in the footer — same spirit as the Unsplash pattern below.

## Keeping Unsplash's required attribution unobtrusive, not hidden

Unsplash's API Guidelines require visible attribution (photographer name + Unsplash, both linked) wherever a photo is actually displayed — this is enforced, not a suggestion, and there is no compliant version of this that hides it in a code comment or a file that never ships to the browser. What *is* legitimate is making it small and quiet rather than prominent. Two patterns that satisfy the requirement without fighting the design:

**Subtle caption directly on the photo** (good for a single hero image):
```html
<figure class="hero-photo">
  <img src="design/assets/photos/office-1.jpg" alt="...">
  <figcaption class="photo-credit">
    Photo by <a href="https://unsplash.com/@photographer?utm_source=...">Name</a> on
    <a href="https://unsplash.com/?utm_source=...">Unsplash</a>
  </figcaption>
</figure>
```
```css
.photo-credit {
  position: absolute;
  bottom: 8px;
  right: 8px;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.7);
  background: rgba(0, 0, 0, 0.35);
  padding: 2px 8px;
  border-radius: 4px;
}
```

**Grouped footer credits** (good for multiple photos across a page — keeps every individual photo caption-free):
```html
<footer>
  ...
  <p class="photo-credits">Photos: <a href="...">Name</a>, <a href="...">Name</a> — via Unsplash</p>
</footer>
```

Either pattern is fine; what's not fine is omitting both and relying on a source-code comment, since the requirement is specifically that it's visible on the site a viewer actually sees.
