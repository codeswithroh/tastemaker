import { useRef, type ReactNode } from "react"
import { useGSAP } from "@gsap/react"
import { gsap } from "@/lib/gsap"

/**
 * Staggers its direct children in as one coordinated group, via GSAP —
 * for a grid (the six "how it works" cards, the four mode cards) this
 * reads as the whole group cascading in together, rather than each card
 * independently firing its own reveal on a hand-tuned delay.
 *
 * Same visible-by-default + watchdog contract as Reveal: children are real
 * DOM by default, only hidden once GSAP has actually mounted and is about
 * to animate them, with a timeout that force-completes if a trigger is
 * ever missed.
 */
export function RevealGroup({
  children,
  className = "",
  stagger = 0.08,
}: {
  children: ReactNode
  className?: string
  stagger?: number
}) {
  const ref = useRef<HTMLDivElement>(null)

  useGSAP(
    () => {
      const el = ref.current
      if (!el) return
      const items = Array.from(el.children)
      if (!items.length) return

      const mm = gsap.matchMedia()
      mm.add("(prefers-reduced-motion: no-preference)", () => {
        gsap.set(items, { opacity: 0, y: 20 })
        const tween = gsap.to(items, {
          opacity: 1,
          y: 0,
          duration: 0.56,
          ease: "power3.out",
          stagger,
          scrollTrigger: { trigger: el, start: "top 85%", once: true },
        })

        const watchdog = window.setTimeout(() => {
          const stuck = items.some((it) => gsap.getProperty(it, "opacity") !== 1)
          if (stuck) tween.progress(1)
        }, 2500)

        return () => window.clearTimeout(watchdog)
      })

      return () => mm.revert()
    },
    { scope: ref, dependencies: [stagger] },
  )

  return (
    <div ref={ref} className={className}>
      {children}
    </div>
  )
}
