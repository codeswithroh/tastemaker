import { useRef, type ReactNode } from "react"
import { useGSAP } from "@gsap/react"
import { gsap } from "@/lib/gsap"

/**
 * GSAP + ScrollTrigger reveal. Content is real, visible DOM by default —
 * the animation only ever hides it *after* GSAP has actually mounted and
 * taken over, via an explicit gsap.set(), never via a CSS/inline pre-hide.
 * That ordering is deliberate: a previous version of this site hid content
 * with plain CSS by default and only GSAP could reveal it, and a missed
 * scroll trigger left whole sections permanently invisible for real users.
 * The watchdog below is a second, independent safety net on top of that.
 */
export function Reveal({
  children,
  delay = 0,
  className = "",
}: {
  children: ReactNode
  delay?: number
  className?: string
}) {
  const ref = useRef<HTMLDivElement>(null)

  useGSAP(
    () => {
      const el = ref.current
      if (!el) return

      const mm = gsap.matchMedia()
      mm.add("(prefers-reduced-motion: no-preference)", () => {
        gsap.set(el, { opacity: 0, y: 18 })
        const tween = gsap.to(el, {
          opacity: 1,
          y: 0,
          duration: 0.62,
          delay: delay / 1000,
          ease: "power3.out",
          scrollTrigger: { trigger: el, start: "top 90%", once: true },
        })

        const watchdog = window.setTimeout(() => {
          if (gsap.getProperty(el, "opacity") !== 1) tween.progress(1)
        }, 2500)

        return () => window.clearTimeout(watchdog)
      })

      return () => mm.revert()
    },
    { scope: ref, dependencies: [delay] },
  )

  return (
    <div ref={ref} className={className}>
      {children}
    </div>
  )
}
