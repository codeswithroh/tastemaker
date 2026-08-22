import { useGSAP } from "@gsap/react"
import { gsap } from "@/lib/gsap"

/**
 * The hero's load-in sequence — four coherent beats, per the skill's own
 * hero-guidelines.md: nav/context, headline, subhead+actions, the single
 * proof visual. Renders nothing itself; it just animates elements tagged
 * with data-hero inside the hero section, once, on mount.
 *
 * Visible-by-default: none of the targeted elements carry any pre-hide
 * styling in their own JSX/CSS, so if this effect never ran at all (JS
 * disabled, a script error) everything still renders normally. GSAP only
 * ever hides them for the instant between mount and animating back in.
 */
export function HeroTimeline() {
  useGSAP(() => {
    const mm = gsap.matchMedia()
    mm.add("(prefers-reduced-motion: no-preference)", () => {
      const nav = document.querySelector('[data-hero="nav"]')
      const headline = document.querySelector('[data-hero="headline"]')
      const stagger = document.querySelectorAll('[data-hero="stagger"]')
      const visual = document.querySelector('[data-hero="visual"]')
      if (!nav || !headline || !visual) return

      const tl = gsap.timeline({ defaults: { ease: "power3.out" } })
      tl.from(nav, { y: -16, opacity: 0, duration: 0.5 })
        .from(headline, { y: 22, opacity: 0, duration: 0.68 }, "-=0.2")
        .from(stagger, { y: 16, opacity: 0, duration: 0.5, stagger: 0.08 }, "-=0.35")
        .from(visual, { y: 24, opacity: 0, scale: 0.98, duration: 0.7 }, "-=0.25")

      const watchdog = window.setTimeout(() => tl.progress(1), 3000)
      return () => window.clearTimeout(watchdog)
    })

    return () => mm.revert()
  }, [])

  return null
}
