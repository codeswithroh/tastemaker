# tastemaker — marketing site

The landing page for the tastemaker skill, plus one live demo. Static HTML/CSS
with GSAP (loaded from CDN) — no build step.

It is itself built to the skill's own rules, as proof:

- **`index.html`** — the marketing page, using tastemaker's **Technical/builder** mood
  (verified palette `#0B0D12` / `#047857` / `#34D399`, Archivo + IBM Plex Mono).
- **`demo.html`** — a fictional mindfulness app ("Calmly") using the **Warm/approachable**
  mood (Zain + Nunito), embedded on the landing page as the live demo.
- **`assets/mark-tastemaker.svg`**, **`assets/mark-calmly.svg`** — constructed geometric
  logo marks (a layered-swatch mark; a lotus), not letters-in-boxes, legible down to 16px.

Both pages follow the skill's non-negotiable defaults: **visual-over-text** (sections lead
with a mockup/chart/comparison, text only captions it), **motion by default** (GSAP hero
timeline + IntersectionObserver scroll reveals, reduced-motion-aware, with fallbacks that
never leave content hidden), and a **real logo + favicon**.

## Deploy

Static — publish this folder as-is. Currently deployed to Netlify:

```bash
# from this directory
npx netlify deploy --dir=. --prod
```

Live: https://tastemaker-ai-skill.netlify.app
