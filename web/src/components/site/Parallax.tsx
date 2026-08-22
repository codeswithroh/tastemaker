import { useRef, type ReactNode } from "react"
import { useGSAP } from "@gsap/react"
import { gsap } from "@/lib/gsap"

/**
 * Scroll-linked parallax via ScrollTrigger's scrub — GSAP drives the
 * transform directly against scroll position, on the compositor, with no
 * React state involved. (An earlier component on this site, CompareReveal,
 * drove its own scroll-linked value through setState and re-rendered the
 * page ~60x/second; this never touches React's render loop at all.)
 *
 * strength: px of vertical drift across the element's transit through the
 * viewport. Small values (20-40) read as depth; large ones read as a gimmick.
 */
export function Parallax({
  children,
  strength = 28,
  className = "",
}: {
  children: ReactNode
  strength?: number
  className?: string
}) {
  const ref = useRef<HTMLDivElement>(null)

  useGSAP(
    () => {
      const el = ref.current
      if (!el) return

      const mm = gsap.matchMedia()
      mm.add("(prefers-reduced-motion: no-preference)", () => {
        gsap.fromTo(
          el,
          { y: -strength },
          {
            y: strength,
            ease: "none",
            scrollTrigger: {
              trigger: el,
              start: "top bottom",
              end: "bottom top",
              scrub: 0.6,
            },
          },
        )
      })

      return () => mm.revert()
    },
    { scope: ref, dependencies: [strength] },
  )

  return (
    <div ref={ref} className={className}>
      {children}
    </div>
  )
}

/** Slow, low-amplitude idle bob for character illustrations — a GSAP yoyo
 * tween instead of a CSS keyframe, so it shares the same reduced-motion
 * gate (gsap.matchMedia) as everything else on the page. */
export function Float({
  children,
  className = "",
  duration = 5,
}: {
  children: ReactNode
  className?: string
  duration?: number
}) {
  const ref = useRef<HTMLDivElement>(null)

  useGSAP(
    () => {
      const el = ref.current
      if (!el) return

      const mm = gsap.matchMedia()
      mm.add("(prefers-reduced-motion: no-preference)", () => {
        gsap.to(el, {
          y: -10,
          duration: duration / 2,
          ease: "sine.inOut",
          yoyo: true,
          repeat: -1,
        })
      })

      return () => mm.revert()
    },
    { scope: ref, dependencies: [duration] },
  )

  return (
    <div ref={ref} className={className}>
      {children}
    </div>
  )
}
